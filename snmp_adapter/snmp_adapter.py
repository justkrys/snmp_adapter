# -*- coding: utf-8 -*-

"""Main module."""

from pysnmp import hlapi


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
    _print_results(command)


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
