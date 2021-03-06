# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/ALCATEL-IND1-BASE.py
# Compiled at: 2016-02-13 18:04:42
(Integer, OctetString, ObjectIdentifier) = mibBuilder.importSymbols('ASN1', 'Integer', 'OctetString', 'ObjectIdentifier')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueRangeConstraint, ConstraintsUnion, SingleValueConstraint, ConstraintsIntersection, ValueSizeConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueRangeConstraint', 'ConstraintsUnion', 'SingleValueConstraint', 'ConstraintsIntersection', 'ValueSizeConstraint')
(ModuleCompliance, NotificationGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'ModuleCompliance', 'NotificationGroup')
(ObjectIdentity, TimeTicks, Unsigned32, NotificationType, IpAddress, MibScalar, MibTable, MibTableRow, MibTableColumn, Gauge32, MibIdentifier, Counter64, Integer32, Bits, Counter32, enterprises, iso, ModuleIdentity) = mibBuilder.importSymbols('SNMPv2-SMI', 'ObjectIdentity', 'TimeTicks', 'Unsigned32', 'NotificationType', 'IpAddress', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Gauge32', 'MibIdentifier', 'Counter64', 'Integer32', 'Bits', 'Counter32', 'enterprises', 'iso', 'ModuleIdentity')
(DisplayString, TextualConvention) = mibBuilder.importSymbols('SNMPv2-TC', 'DisplayString', 'TextualConvention')
alcatelIND1BaseMIB = ModuleIdentity((1, 3, 6, 1, 4, 1, 6486, 800)).setRevisions(('2007-04-02 00:08', ))
if mibBuilder.loadTexts:
    alcatelIND1BaseMIB.setLastUpdated('200704020008Z')
if mibBuilder.loadTexts:
    alcatelIND1BaseMIB.setOrganization('Alcatel-Lucent')
if mibBuilder.loadTexts:
    alcatelIND1BaseMIB.setContactInfo('Please consult with Customer Service to ensure the most appropriate\n         version of this document is used with the products in question:\n\n                    Alcatel-Lucent, Enterprise Solutions Division\n                   (Formerly Alcatel Internetworking, Incorporated)\n                           26801 West Agoura Road\n                        Agoura Hills, CA  91301-5122\n                          United States Of America\n\n        Telephone:               North America  +1 800 995 2696\n                                 Latin America  +1 877 919 9526\n                                 Europe         +31 23 556 0100\n                                 Asia           +65 394 7933\n                                 All Other      +1 818 878 4507\n\n        Electronic Mail:         support@ind.alcatel.com\n        World Wide Web:          http://alcatel-lucent.com/wps/portal/enterprise\n        File Transfer Protocol:  ftp://ftp.ind.alcatel.com/pub/products/mibs')
if mibBuilder.loadTexts:
    alcatelIND1BaseMIB.setDescription('This module describes an authoritative enterprise-specific Simple\n         Network Management Protocol (SNMP) Management Information Base (MIB):\n\n             This module provides base definitions for modules\n             developed to manage Alcatel-Lucent infrastructure products.\n\n         The right to make changes in specification and other information\n         contained in this document without prior notice is reserved.\n\n         No liability shall be assumed for any incidental, indirect, special, or\n         consequential damages whatsoever arising from or related to this\n         document or the information contained herein.\n\n         Vendors, end-users, and other interested parties are granted\n         non-exclusive license to use this specification in connection with\n         management of the products for which it is intended to be used.\n\n                     Copyright (C) 1995-2007 Alcatel-Lucent\n                         ALL RIGHTS RESERVED WORLDWIDE')
alcatel = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486))
if mibBuilder.loadTexts:
    alcatel.setDescription('Alcatel-Lucent Corporate Private Enterprise Number.')
alcatelIND1Management = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1))
if mibBuilder.loadTexts:
    alcatelIND1Management.setDescription('Internetworking Division 1 Management Branch.')
managementIND1Hardware = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 1))
if mibBuilder.loadTexts:
    managementIND1Hardware.setDescription('Hardware Feature Management Branch.')
managementIND1Software = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2))
if mibBuilder.loadTexts:
    managementIND1Software.setDescription('Software Feature Management Branch.')
managementIND1Notifications = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3))
if mibBuilder.loadTexts:
    managementIND1Notifications.setDescription('Notifications Related Management Branch.')
managementIND1AgentCapabilities = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 4))
if mibBuilder.loadTexts:
    managementIND1AgentCapabilities.setDescription('Notifications Related Management Branch.')
hardwareIND1Entities = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 1, 1))
if mibBuilder.loadTexts:
    hardwareIND1Entities.setDescription('Branch For Hardware Feature Related ENTITY-MIB Extensions.')
hardwareIND1Devices = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 1, 2))
if mibBuilder.loadTexts:
    hardwareIND1Devices.setDescription('Branch Where Object Indentifiers For Chassis And Modules Are Defined.')
softwareIND1Entities = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1))
if mibBuilder.loadTexts:
    softwareIND1Entities.setDescription('Branch For Software Feature Related Extensions.')
softwareIND1Services = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 2))
if mibBuilder.loadTexts:
    softwareIND1Services.setDescription('Branch For Software Features Related to any service related extensions.\n        Usually management for non AOS devices or software.')
notificationIND1Entities = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 1))
if mibBuilder.loadTexts:
    notificationIND1Entities.setDescription('Branch For Notification Related ENTITY-MIB Extensions.')
notificationIND1Traps = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 2))
if mibBuilder.loadTexts:
    notificationIND1Traps.setDescription('Branch For Notification/Trap Definitions.')
aipAMAPTraps = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 2, 1))
if mibBuilder.loadTexts:
    aipAMAPTraps.setDescription('Branch For Alcatel-Lucent/Xylan Mapping Adjaceny Protocol Notification/Trap Definitions.')
aipGMAPTraps = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 2, 2))
if mibBuilder.loadTexts:
    aipGMAPTraps.setDescription('Branch For Group Mobility Advertising Protocol Notification/Trap Definitions.')
policyManagerTraps = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 2, 3))
if mibBuilder.loadTexts:
    policyManagerTraps.setDescription('Branch For Policy Manager Notification/Trap Definitions.')
chassisTraps = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 2, 4))
if mibBuilder.loadTexts:
    chassisTraps.setDescription('Branch For Chassis Notification/Trap Definitions.')
healthMonTraps = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 2, 5))
if mibBuilder.loadTexts:
    healthMonTraps.setDescription('Branch For Chassis Notification/Trap Definitions.')
cmmEsmDrvTraps = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 2, 6))
if mibBuilder.loadTexts:
    cmmEsmDrvTraps.setDescription('Branch For CMM Ethernet Driver Notification/Trap Definitions.')
spanningTreeTraps = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 2, 7))
if mibBuilder.loadTexts:
    spanningTreeTraps.setDescription('Branch For CMM Spanning Tree Notification/Trap Definitions.')
portMirroringMonitoringTraps = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 2,
                                               8))
if mibBuilder.loadTexts:
    portMirroringMonitoringTraps.setDescription('Branch for Port mirroring and monitoring Notification/Trap Definitions.')
sourceLearningTraps = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 2, 9))
if mibBuilder.loadTexts:
    sourceLearningTraps.setDescription('Branch for Source Learning Notification/Trap Definitioins.')
slbTraps = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 2, 10))
if mibBuilder.loadTexts:
    slbTraps.setDescription('Branch for Server Load Balancing Notification/Trap Definitions.')
switchMgtTraps = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 2, 11))
if mibBuilder.loadTexts:
    switchMgtTraps.setDescription('Branch for Switch Management Notification/Trap Definitions.')
trapMgrTraps = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 2, 12))
if mibBuilder.loadTexts:
    trapMgrTraps.setDescription('Branch for Trap Manager Notification Definitions.')
groupmobilityTraps = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 2, 13))
if mibBuilder.loadTexts:
    groupmobilityTraps.setDescription('Branch for Group Mobility Notification/Trap Definitions.')
lnkaggTraps = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 2, 14))
if mibBuilder.loadTexts:
    lnkaggTraps.setDescription('Branch for Link Aggregation  Notification/Trap Definitions.')
trafficEventTraps = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 2, 15))
if mibBuilder.loadTexts:
    trafficEventTraps.setDescription('OID branch for network traffic event Trap/Notification Definitions.')
atmTraps = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 2, 16))
if mibBuilder.loadTexts:
    atmTraps.setDescription('Branch for ATM Notification/Trap Definitions.')
pethTraps = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 2, 17))
if mibBuilder.loadTexts:
    pethTraps.setDescription('Branch for power over ethernet Notification/Trap Definitions.')
wccpTraps = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 2, 18))
if mibBuilder.loadTexts:
    wccpTraps.setDescription('Branch for Web Cache Coordination Protocol Notification/Trap Definitions.')
alaNMSTraps = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 2, 19))
if mibBuilder.loadTexts:
    alaNMSTraps.setDescription('Branch for Network Management Software Notification/Trap Definitions.')
alaNetSecTraps = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 2, 20))
if mibBuilder.loadTexts:
    alaNetSecTraps.setDescription('Branch for Network Security Notification/Trap Definitions.')
alaAaaTraps = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 2, 21))
if mibBuilder.loadTexts:
    alaAaaTraps.setDescription('Branch for AAA Notification/Trap Definitions.')
alaLbdTraps = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 2, 22))
if mibBuilder.loadTexts:
    alaLbdTraps.setDescription('Branch for Loop Back Detection Notification/Trap Definitions.')
alaDhcpClientTraps = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 3, 2, 23))
if mibBuilder.loadTexts:
    alaDhcpClientTraps.setDescription('Branch for DHCP Client Notification/Trap Definitions.')
hardentIND1Physical = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 1, 1, 1))
if mibBuilder.loadTexts:
    hardentIND1Physical.setDescription('Branch For Physical Hardware Feature Related ENTITY-MIB Extensions.')
hardentIND1System = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 1, 1, 2))
if mibBuilder.loadTexts:
    hardentIND1System.setDescription('Branch For System Wide Hardware Feature Related ENTITY-MIB Extensions.')
hardentIND1Chassis = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 1, 1, 3))
if mibBuilder.loadTexts:
    hardentIND1Chassis.setDescription('Branch For Chassis Hardware Feature Related ENTITY-MIB Extensions.')
hardentIND1Pcam = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 1, 1, 4))
if mibBuilder.loadTexts:
    hardentIND1Pcam.setDescription('Branch For Pseudo-CAM Hardware Feature Related ENTITY-MIB Extensions.')
softentIND1SnmpAgt = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 1))
if mibBuilder.loadTexts:
    softentIND1SnmpAgt.setDescription('Branch For SNMP Agent Information.')
softentIND1TrapMgr = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 2))
if mibBuilder.loadTexts:
    softentIND1TrapMgr.setDescription('Branch For Trap Manager Information.')
softentIND1VlanMgt = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 3))
if mibBuilder.loadTexts:
    softentIND1VlanMgt.setDescription('Branch For VLAN Manager Information.')
softentIND1GroupMobility = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 4))
if mibBuilder.loadTexts:
    softentIND1GroupMobility.setDescription('Branch For Group Mobility Information.')
softentIND1Port = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 5))
if mibBuilder.loadTexts:
    softentIND1Port.setDescription('Branch For Port Manager Information.')
softentIND1Sesmgr = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 7))
if mibBuilder.loadTexts:
    softentIND1Sesmgr.setDescription('Branch For Session Manager Information.')
softentIND1MacAddress = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 8))
if mibBuilder.loadTexts:
    softentIND1MacAddress.setDescription('Branch For Source Learning MAC Address Information.')
softentIND1Aip = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 9))
if mibBuilder.loadTexts:
    softentIND1Aip.setDescription('Branch For Interswitch Protocol Information.')
softentIND1Routing = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 10))
if mibBuilder.loadTexts:
    softentIND1Routing.setDescription('Branch For Routing Information.')
softentIND1Confmgr = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 11))
if mibBuilder.loadTexts:
    softentIND1Confmgr.setDescription('Branch For Configuration Manager Information.')
softentIND1VlanStp = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 12))
if mibBuilder.loadTexts:
    softentIND1VlanStp.setDescription('Branch For VLAN Spanning Tree Protocol Information.')
softentIND1LnkAgg = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 13))
if mibBuilder.loadTexts:
    softentIND1LnkAgg.setDescription('Branch For Link Aggregation Information.')
softentIND1Policy = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 14))
if mibBuilder.loadTexts:
    softentIND1Policy.setDescription('Branch For Policy Information.')
softentIND1AAA = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 15))
if mibBuilder.loadTexts:
    softentIND1AAA.setDescription('Branch For Authentication, Authorization, and Accounting (AAA) Information.')
softentIND1Health = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 16))
if mibBuilder.loadTexts:
    softentIND1Health.setDescription('Branch For Health Information.')
softentIND1WebMgt = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 17))
if mibBuilder.loadTexts:
    softentIND1WebMgt.setDescription('Branch For WebView Information.')
softentIND1Ipms = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 18))
if mibBuilder.loadTexts:
    softentIND1Ipms.setDescription('Branch For IPMS Information.')
softentIND1PortMirroringMonitoring = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1,
                                                     2, 1, 19))
if mibBuilder.loadTexts:
    softentIND1PortMirroringMonitoring.setDescription(' Branch for Port Mirroring and Monitoring information.')
softentIND1Slb = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 20))
if mibBuilder.loadTexts:
    softentIND1Slb.setDescription(' Branch for Server Load Balancing information.')
softentIND1Dot1Q = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 21))
if mibBuilder.loadTexts:
    softentIND1Dot1Q.setDescription('Branch For 802.1Q Information.')
softentIND1QoS = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 22))
if mibBuilder.loadTexts:
    softentIND1QoS.setDescription('Branch For QoS and Filtering Information.')
softentIND1Ip = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 23))
if mibBuilder.loadTexts:
    softentIND1Ip.setDescription('Branch for IP private information.')
softentIND1StackMgr = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 24))
if mibBuilder.loadTexts:
    softentIND1StackMgr.setDescription('Branch for Stack Manager private information.')
softentIND1Partmgr = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 25))
if mibBuilder.loadTexts:
    softentIND1Partmgr.setDescription('Branch For Partitioned Manager Information.')
softentIND1Ntp = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 26))
if mibBuilder.loadTexts:
    softentIND1Ntp.setDescription('Branch for Network Time Protocol Information.')
softentIND1InLinePower = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 27))
if mibBuilder.loadTexts:
    softentIND1InLinePower.setDescription('Branch for In Line Power management Information.')
softentIND1Vrrp = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 28))
if mibBuilder.loadTexts:
    softentIND1Vrrp.setDescription('Branch for VRRP.')
softentIND1Ipv6 = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 29))
if mibBuilder.loadTexts:
    softentIND1Ipv6.setDescription('Branch for IPv6 private information.')
softentIND1Dot1X = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 30))
if mibBuilder.loadTexts:
    softentIND1Dot1X.setDescription('Branch for 802.1x private information.')
softentIND1Sonet = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 31))
if mibBuilder.loadTexts:
    softentIND1Sonet.setDescription('Branch For Software Feature Related to Sonet')
softentIND1Atm = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 32))
if mibBuilder.loadTexts:
    softentIND1Atm.setDescription('Branch for ATM information.')
softentIND1PortMapping = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 33))
if mibBuilder.loadTexts:
    softentIND1PortMapping.setDescription('Branch for Port Mapping private information.')
softentIND1Igmp = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 34))
if mibBuilder.loadTexts:
    softentIND1Igmp.setDescription('Branch for IGMP proprietary information.')
softentIND1Mld = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 35))
if mibBuilder.loadTexts:
    softentIND1Mld.setDescription('Branch for MLD proprietary nformation.')
softentIND1Gvrp = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 36))
if mibBuilder.loadTexts:
    softentIND1Gvrp.setDescription('Branch for GVRP information.')
softentIND1VlanStackingMgt = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1,
                                             37))
if mibBuilder.loadTexts:
    softentIND1VlanStackingMgt.setDescription('Branch for Vlan Stacking Management proprietary information.')
softentIND1Wccp = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 38))
if mibBuilder.loadTexts:
    softentIND1Wccp.setDescription('Branch for Web Cache Coordination Protocol information.')
softentIND1Ssh = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 39))
if mibBuilder.loadTexts:
    softentIND1Ssh.setDescription('Branch for SSH proprietary information.')
softentIND1EthernetOam = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 40))
if mibBuilder.loadTexts:
    softentIND1EthernetOam.setDescription('Branch for Configuration Fault Management Information for Ethernet OAM')
softentIND1IPMVlanMgt = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 41))
if mibBuilder.loadTexts:
    softentIND1IPMVlanMgt.setDescription('Branch for IPM Vlan Management proprietary information.')
softentIND1IPsec = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 43))
if mibBuilder.loadTexts:
    softentIND1IPsec.setDescription('Branch for IPsec proprietary information.')
softentIND1Udld = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 44))
if mibBuilder.loadTexts:
    softentIND1Udld.setDescription('Branch for UDLD information.')
softentIND1BFD = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 45))
if mibBuilder.loadTexts:
    softentIND1BFD.setDescription('Branch for BFD information.')
softentIND1Erp = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 46))
if mibBuilder.loadTexts:
    softentIND1Erp.setDescription('Branch for Ethernet Ring Protection proprietary information.')
softentIND1NetSec = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 48))
if mibBuilder.loadTexts:
    softentIND1NetSec.setDescription('Branch for Network Security information.')
softentIND1eService = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 50))
if mibBuilder.loadTexts:
    softentIND1eService.setDescription('Branch for E-Serices proprietary information.')
softentIND1serviceMgr = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 51))
if mibBuilder.loadTexts:
    softentIND1serviceMgr.setDescription('Branch for Service Manager proprietary information.')
softentIND1Dot3Oam = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 52))
if mibBuilder.loadTexts:
    softentIND1Dot3Oam.setDescription('Branch for 802.3ah proprietary information.')
softentIND1MplsFrr = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 53))
if mibBuilder.loadTexts:
    softentIND1MplsFrr.setDescription('Branch for MPLS FRR proprietary information.')
softentIND1LicenseManager = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 54))
if mibBuilder.loadTexts:
    softentIND1LicenseManager.setDescription('Branch for License Manager proprietary information.')
softentIND1Saa = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 55))
if mibBuilder.loadTexts:
    softentIND1Saa.setDescription('Branch for Service Assurance Agent proprietary information.')
softentIND1Lbd = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 56))
if mibBuilder.loadTexts:
    softentIND1Lbd.setDescription('Branch for Loop Back Detection information.')
softentIND1Mvrp = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 57))
if mibBuilder.loadTexts:
    softentIND1Mvrp.setDescription('Branch for MVRP information.')
softentIND1LldpMed = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 58))
if mibBuilder.loadTexts:
    softentIND1LldpMed.setDescription('Branch for LLDP MED information.')
softentIND1DhcpSrv = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 59))
if mibBuilder.loadTexts:
    softentIND1DhcpSrv.setDescription('Branch for DHCP Server information.')
routingIND1Tm = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 10, 1))
if mibBuilder.loadTexts:
    routingIND1Tm.setDescription('Branch For DRC Task Manager Information.')
routingIND1Iprm = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 10, 2))
if mibBuilder.loadTexts:
    routingIND1Iprm.setDescription('Branch For IP Route Manager Information.')
routingIND1Rip = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 10, 3))
if mibBuilder.loadTexts:
    routingIND1Rip.setDescription('Branch For Routing Information Protocol (RIP) Information.')
routingIND1Ospf = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 10, 4))
if mibBuilder.loadTexts:
    routingIND1Ospf.setDescription('Branch For Open Shortest Path First (OSPF) Information.')
routingIND1Bgp = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 10, 5))
if mibBuilder.loadTexts:
    routingIND1Bgp.setDescription('Branch For Border Gateway Protocol (BGP) Information.')
routingIND1Pim = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 10, 6))
if mibBuilder.loadTexts:
    routingIND1Pim.setDescription('Branch For Protocol Independent Multicast (PIM-SM and PIM-DM) Information.')
routingIND1Dvmrp = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 10, 7))
if mibBuilder.loadTexts:
    routingIND1Dvmrp.setDescription('Branch For Distance-Vector Multicast Routing Protocol (DVMRP) Information.')
routingIND1Ipx = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 10, 8))
if mibBuilder.loadTexts:
    routingIND1Ipx.setDescription('Branch For Novell Internetwork Packet Exchange (IPX) Protocol Information.')
routingIND1UdpRelay = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 10, 9))
if mibBuilder.loadTexts:
    routingIND1UdpRelay.setDescription('Branch For UDP Relay Agent.')
routingIND1Ipmrm = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 10, 10))
if mibBuilder.loadTexts:
    routingIND1Ipmrm.setDescription('Branch For IP Multicast Route Manager Information.')
routingIND1RDP = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 10, 11))
if mibBuilder.loadTexts:
    routingIND1RDP.setDescription('Branch For IP Multicast Route Manager Information.')
routingIND1Ripng = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 10, 12))
if mibBuilder.loadTexts:
    routingIND1Ripng.setDescription('Branch For RIPng.')
routingIND1Ospf3 = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 10, 13))
if mibBuilder.loadTexts:
    routingIND1Ospf3.setDescription('Branch For OSPF3.')
routingIND1ISIS = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 10, 14))
if mibBuilder.loadTexts:
    routingIND1ISIS.setDescription('Branch For ISIS Routing.')
routingIND1Vrf = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 1, 10, 15))
if mibBuilder.loadTexts:
    routingIND1Vrf.setDescription('Branch For Virtual Router support.')
serventIND1Aqe = ObjectIdentity((1, 3, 6, 1, 4, 1, 6486, 800, 1, 2, 2, 1))
if mibBuilder.loadTexts:
    serventIND1Aqe.setDescription('Branch For AQE.')
mibBuilder.exportSymbols('ALCATEL-IND1-BASE', softentIND1IPMVlanMgt=softentIND1IPMVlanMgt, softentIND1Udld=softentIND1Udld, softentIND1NetSec=softentIND1NetSec, softentIND1Lbd=softentIND1Lbd, softentIND1Dot1Q=softentIND1Dot1Q, softentIND1Wccp=softentIND1Wccp, routingIND1Ospf=routingIND1Ospf, softentIND1Vrrp=softentIND1Vrrp, softentIND1VlanMgt=softentIND1VlanMgt, groupmobilityTraps=groupmobilityTraps, spanningTreeTraps=spanningTreeTraps, routingIND1Rip=routingIND1Rip, routingIND1Vrf=routingIND1Vrf, serventIND1Aqe=serventIND1Aqe, softentIND1Port=softentIND1Port, hardentIND1System=hardentIND1System, softentIND1Mvrp=softentIND1Mvrp, managementIND1Notifications=managementIND1Notifications, PYSNMP_MODULE_ID=alcatelIND1BaseMIB, hardwareIND1Entities=hardwareIND1Entities, aipAMAPTraps=aipAMAPTraps, alaNetSecTraps=alaNetSecTraps, softentIND1BFD=softentIND1BFD, softentIND1Ipv6=softentIND1Ipv6, softentIND1TrapMgr=softentIND1TrapMgr, pethTraps=pethTraps, alaNMSTraps=alaNMSTraps, routingIND1UdpRelay=routingIND1UdpRelay, softentIND1Atm=softentIND1Atm, softentIND1Erp=softentIND1Erp, lnkaggTraps=lnkaggTraps, softentIND1Saa=softentIND1Saa, switchMgtTraps=switchMgtTraps, routingIND1Iprm=routingIND1Iprm, softentIND1Igmp=softentIND1Igmp, softentIND1Sesmgr=softentIND1Sesmgr, softentIND1Ntp=softentIND1Ntp, softentIND1LnkAgg=softentIND1LnkAgg, sourceLearningTraps=sourceLearningTraps, softentIND1InLinePower=softentIND1InLinePower, managementIND1Hardware=managementIND1Hardware, wccpTraps=wccpTraps, softentIND1WebMgt=softentIND1WebMgt, routingIND1Ipmrm=routingIND1Ipmrm, softentIND1Aip=softentIND1Aip, softentIND1Ssh=softentIND1Ssh, softentIND1EthernetOam=softentIND1EthernetOam, portMirroringMonitoringTraps=portMirroringMonitoringTraps, alaDhcpClientTraps=alaDhcpClientTraps, softentIND1VlanStackingMgt=softentIND1VlanStackingMgt, aipGMAPTraps=aipGMAPTraps, routingIND1Ripng=routingIND1Ripng, alcatelIND1Management=alcatelIND1Management, softentIND1AAA=softentIND1AAA, routingIND1Ospf3=routingIND1Ospf3, softentIND1eService=softentIND1eService, chassisTraps=chassisTraps, trafficEventTraps=trafficEventTraps, softentIND1PortMirroringMonitoring=softentIND1PortMirroringMonitoring, softentIND1Policy=softentIND1Policy, softentIND1QoS=softentIND1QoS, slbTraps=slbTraps, softentIND1Dot1X=softentIND1Dot1X, softentIND1serviceMgr=softentIND1serviceMgr, alaLbdTraps=alaLbdTraps, routingIND1Pim=routingIND1Pim, policyManagerTraps=policyManagerTraps, trapMgrTraps=trapMgrTraps, softentIND1MacAddress=softentIND1MacAddress, alcatelIND1BaseMIB=alcatelIND1BaseMIB, softentIND1MplsFrr=softentIND1MplsFrr, routingIND1RDP=routingIND1RDP, routingIND1ISIS=routingIND1ISIS, softentIND1Partmgr=softentIND1Partmgr, softentIND1VlanStp=softentIND1VlanStp, cmmEsmDrvTraps=cmmEsmDrvTraps, hardentIND1Pcam=hardentIND1Pcam, softentIND1Slb=softentIND1Slb, healthMonTraps=healthMonTraps, managementIND1Software=managementIND1Software, alaAaaTraps=alaAaaTraps, softentIND1Sonet=softentIND1Sonet, softentIND1StackMgr=softentIND1StackMgr, softentIND1SnmpAgt=softentIND1SnmpAgt, routingIND1Tm=routingIND1Tm, softentIND1Confmgr=softentIND1Confmgr, hardentIND1Physical=hardentIND1Physical, softentIND1Routing=softentIND1Routing, softentIND1PortMapping=softentIND1PortMapping, softentIND1Health=softentIND1Health, softwareIND1Entities=softwareIND1Entities, softentIND1DhcpSrv=softentIND1DhcpSrv, routingIND1Ipx=routingIND1Ipx, notificationIND1Traps=notificationIND1Traps, atmTraps=atmTraps, softentIND1Dot3Oam=softentIND1Dot3Oam, softentIND1Ip=softentIND1Ip, softwareIND1Services=softwareIND1Services, hardwareIND1Devices=hardwareIND1Devices, routingIND1Dvmrp=routingIND1Dvmrp, softentIND1LicenseManager=softentIND1LicenseManager, softentIND1IPsec=softentIND1IPsec, softentIND1LldpMed=softentIND1LldpMed, softentIND1Ipms=softentIND1Ipms, managementIND1AgentCapabilities=managementIND1AgentCapabilities, notificationIND1Entities=notificationIND1Entities, hardentIND1Chassis=hardentIND1Chassis, softentIND1Gvrp=softentIND1Gvrp, softentIND1Mld=softentIND1Mld, alcatel=alcatel, softentIND1GroupMobility=softentIND1GroupMobility, routingIND1Bgp=routingIND1Bgp)