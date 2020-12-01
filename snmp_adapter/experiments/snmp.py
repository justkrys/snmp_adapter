# -*- coding: utf-8 -*-

"""Main module."""

import asyncio
import warnings

from pysnmp import hlapi
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncio.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp.smi import builder, compiler, view, rfc1902

DEFAULT_ADDRESSS = "0.0.0.0"
DEFAULT_PORT = 162
DEFAULT_COMMUNITY = "public"
DEFAULT_MIBS = ("SNMPv2-MIB", "IF-MIB", "XYTRONIX-MIB")  # Must be a tuple not a list.

_view_controller = None


def _make_object(*id_parts):
    """Construct a pySNMP ObjectType from the given identity."""
    return hlapi.ObjectType(hlapi.ObjectIdentity(*id_parts))


def _make_get(address, community, *objects, port=161, mp_model=1):
    """Construct a pySNMP get command.

    Defaults to SNMPv2c and port 161.

    """
    engine = hlapi.SnmpEngine()
    community = hlapi.CommunityData(community, mpModel=mp_model)
    target = hlapi.UdpTransportTarget((address, port))
    context = hlapi.ContextData()
    return hlapi.getCmd(engine, community, target, context, *objects)


def _run_command(command):
    """Runs the command and returns a list of all results."""
    # Implicitly calls next() repeatdly on the command iterator until there is nothing left.
    # Supports both single GETs as well as GETBULKs.
    return [result for result in command]


def _extract_errors(results):
    """Returns a list of error tuples if any errors exist in the results.

    Each error tuple consists of (error_indication, error_status, error_index).

    """
    errors = []
    for error_indication, error_status, error_index, var_binds in results:
        if error_indication or error_status:
            error_text = error_status.prettyPrint() if error_status else error_status
            object_id = var_binds[int(error_index) - 1][0] if error_index else "?"
            errors.append((error_indication, error_text, object_id))
    return errors


def _extract_values(results):
    """Returns a dict of data values from the results."""
    values = {}
    for result in results:
        var_binds = result[-1]
        for var_bind in var_binds:
            values[var_bind[0].prettyPrint()] = var_bind[1]
    return values


def _print_errors(errors):
    """Prints errors to the screen."""
    for error_indication, error_text, object_id in errors:
        if error_indication:
            print(error_indication)
        elif error_text:
            print(f"{error_text} at {object_id}")


def _print_values(values):
    """Prints object ids and their data values to the screen."""
    for object_id, value in values.items():
        print(object_id, "=", value)


def _print_results(results):
    """Prints the results of snmp commands and/or any related errors."""
    _print_errors(_extract_errors(results))
    _print_values(_extract_values(results))


def _old_print_results(command):
    """Prints the results of snmp commands and/or any related errors. (Deprecated)"""
    warnings.warn("Deprecated.", DeprecationWarning)
    errorIndication, errorStatus, errorIndex, varBinds = next(command)
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print(
            "%s at %s"
            % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
            )
        )
    else:
        for varBind in varBinds:
            print(" = ".join([x.prettyPrint() for x in varBind]))


def quickstart():
    """PySNMP Quick Start Example"""
    iterator = hlapi.getCmd(
        hlapi.SnmpEngine(),
        hlapi.CommunityData("public", mpModel=0),
        hlapi.UdpTransportTarget(("192.168.0.59", 161)),
        hlapi.ContextData(),
        hlapi.ObjectType(hlapi.ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
    )
    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print(
            "%s at %s"
            % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
            )
        )
    else:
        for varBind in varBinds:
            print(" = ".join([x.prettyPrint() for x in varBind]))


def common():
    """PySNMP Tutorial Common Operations Example"""
    engine = hlapi.SnmpEngine()
    community = hlapi.CommunityData("public", mpModel=1)  # SNMPv2c
    target = hlapi.UdpTransportTarget(("192.168.0.59", 161))
    context = hlapi.ContextData()

    # object_id = hlapi.ObjectIdentity(
    #     "iso.org.dod.internet.mgmt.mib-2.system.sysDescr.0"
    # )
    sysDescr = hlapi.ObjectType(hlapi.ObjectIdentity("SNMPv2-MIB", "sysDescr", 0))
    sysUpTime = hlapi.ObjectType(hlapi.ObjectIdentity("SNMPv2-MIB", "sysUpTime", 0))
    ifInOctets = hlapi.ObjectType(hlapi.ObjectIdentity("IF-MIB", "ifInOctets", 1))
    command = hlapi.getCmd(
        engine, community, target, context, sysDescr, sysUpTime, ifInOctets
    )
    _old_print_results(command)


def temperature():
    """One-Wire Temperature sensor on ControlByWeb X-410 module."""
    temp = _make_object("XYTRONIX-MIB", "temp", 0)
    command = _make_get("192.168.0.132", "webrelay", temp)
    results = _run_command(command)
    _print_results(results)


def rewrite():
    """PySNMP Tutorial Common Operations Example, rewritten"""
    sysDescr = _make_object("SNMPv2-MIB", "sysDescr", 0)
    sysUpTime = _make_object("SNMPv2-MIB", "sysUpTime", 0)
    ifInOctets = _make_object("IF-MIB", "ifInOctets", 1)
    command = _make_get("192.168.0.59", "public", sysDescr, sysUpTime, ifInOctets)
    results = _run_command(command)
    _print_results(results)


def _listen_callback(
    snmp_engine,
    state_reference,
    context_engine_id,
    context_name,
    var_binds,
    callback_context,
):
    transport_domain, transport_address = snmp_engine.msgAndPduDsp.getTransportInfo(
        state_reference
    )
    print(
        f"\nNotification from {transport_address}, "
        f"SNMP Engine {context_engine_id.prettyPrint()}, "
        f"Context {context_name.prettyPrint()}"
    )
    for oid, value in var_binds:
        name = rfc1902.ObjectIdentity(oid.prettyPrint())
        name.resolveWithMib(_view_controller)
        print(f"    {name.prettyPrint()} ({oid.prettyPrint()}) = {value.prettyPrint()}")


def listen(
    address=DEFAULT_ADDRESSS,
    port=DEFAULT_PORT,
    community=DEFAULT_COMMUNITY,
    mibs=DEFAULT_MIBS,
):
    """Listen to and SNMP trap and print events."""
    # Based on pySNMP example code.
    mib_builder = builder.MibBuilder()
    compiler.addMibCompiler(mib_builder)
    mib_builder.loadModules(*mibs)
    global _view_controller
    _view_controller = view.MibViewController(mib_builder)
    loop = asyncio.get_event_loop()
    snmp_engine = engine.SnmpEngine()
    print(f"Agent is listening SNMP Trap on {address}, Port: {port}")
    if port < 1024:
        print(
            "WARNING: Port < 1024. Root priviledges or authbind required on *nix systems."
        )
    print("-" * 79)
    config.addTransport(
        snmp_engine,
        udp.domainName + (1,),
        udp.UdpTransport().openServerMode((address, port)),
    )
    config.addV1System(snmp_engine, community, community)
    ntfrcv.NotificationReceiver(snmp_engine, _listen_callback)
    print("Press CTRL-C to quit.")
    loop.run_forever()
