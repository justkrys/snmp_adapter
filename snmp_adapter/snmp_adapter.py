# -*- coding: utf-8 -*-

"""Main module."""

from pysnmp import hlapi


def quickstart():
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
        return 1
    elif errorStatus:
        print(
            "%s at %s"
            % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
            )
        )
        return 1
    else:
        for varBind in varBinds:
            print(" = ".join([x.prettyPrint() for x in varBind]))
        return 0


def common():
    engine = hlapi.SnmpEngine()
    community = hlapi.CommunityData("public", mpModel=1)  # SNMPv2c
    target = hlapi.UdpTransportTarget(("192.168.0.59", 161))
    context = hlapi.ContextData()

    # object_id = hlapi.ObjectIdentity(
    #     "iso.org.dod.internet.mgmt.mib-2.system.sysDescr.0"
    # )
    sysDescr = hlapi.ObjectType(
        hlapi.ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)
    ).loadMibs("IF-MIB")
    sysUpTime = hlapi.ObjectType(hlapi.ObjectIdentity("SNMPv2-MIB", "sysUpTime", 0))
    foo = hlapi.ObjectType(hlapi.ObjectIdentity("IF-MIB", "ifInOctets", 1))
    command = hlapi.getCmd(engine, community, target, context, sysDescr, sysUpTime, foo)
    print(next(command))
