# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/BLDG-HVAC-MIB.py
# Compiled at: 2016-02-13 18:06:34
(OctetString, ObjectIdentifier, Integer) = mibBuilder.importSymbols('ASN1', 'OctetString', 'ObjectIdentifier', 'Integer')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ConstraintsIntersection, ConstraintsUnion, SingleValueConstraint, ValueSizeConstraint, ValueRangeConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ConstraintsIntersection', 'ConstraintsUnion', 'SingleValueConstraint', 'ValueSizeConstraint', 'ValueRangeConstraint')
(SnmpAdminString,) = mibBuilder.importSymbols('SNMP-FRAMEWORK-MIB', 'SnmpAdminString')
(ObjectGroup, ModuleCompliance, NotificationGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'ObjectGroup', 'ModuleCompliance', 'NotificationGroup')
(ObjectIdentity, iso, Counter32, Unsigned32, TimeTicks, experimental, Counter64, MibScalar, MibTable, MibTableRow, MibTableColumn, NotificationType, Gauge32, IpAddress, MibIdentifier, Integer32, Bits, ModuleIdentity) = mibBuilder.importSymbols('SNMPv2-SMI', 'ObjectIdentity', 'iso', 'Counter32', 'Unsigned32', 'TimeTicks', 'experimental', 'Counter64', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'NotificationType', 'Gauge32', 'IpAddress', 'MibIdentifier', 'Integer32', 'Bits', 'ModuleIdentity')
(DisplayString, TextualConvention, StorageType, TimeStamp, RowStatus) = mibBuilder.importSymbols('SNMPv2-TC', 'DisplayString', 'TextualConvention', 'StorageType', 'TimeStamp', 'RowStatus')
bldgHVACMIB = ModuleIdentity((1, 3, 6, 1, 3, 122)).setRevisions(('2003-03-27 00:00', ))
if mibBuilder.loadTexts:
    bldgHVACMIB.setLastUpdated('200303270000Z')
if mibBuilder.loadTexts:
    bldgHVACMIB.setOrganization('SNMPCONF working group\n                  E-mail: snmpconf@snmp.com')
if mibBuilder.loadTexts:
    bldgHVACMIB.setContactInfo('Jon Saperia\n        Postal:     JDS Consulting\n                    174 Chapman Street\n                    Watertown, MA 02472\n                    U.S.A.\n        Phone:      +1 617 744 1079\n        E-mail:     saperia@jdscons.com\n\n        Wayne Tackabury\n        Postal:     Gold Wire Technology\n                    411 Waverley Oaks Rd.\n                    Waltham, MA 02452\n                    U.S.A.\n        Phone:      +1 781 398 8800\n        E-mail:     wayne@goldwiretech.com\n\n        Michael MacFaden\n        Postal:     Riverstone Networks\n                    5200 Great America Pkwy.\n                    Santa Clara, CA 95054\n                    U.S.A.\n        Phone:      +1 408 878 6500\n        E-mail:     mrm@riverstonenet.com\n\n        David Partain\n        Postal:     Ericsson AB\n                    P.O. Box 1248\n                    SE-581 12  Linkoping\n                    Sweden\n        E-mail:     David.Partain@ericsson.com')
if mibBuilder.loadTexts:
    bldgHVACMIB.setDescription('This example MIB module defines a set of management objects\n        for heating ventilation and air conditioning systems.  It\n        also includes objects that can be used to create policies\n        that are applied to rooms.  This eliminates the need to send\n        per-instance configuration commands to the system.\n\n        Copyright (C) The Internet Society (2003).  This version of\n        this MIB module is part of RFC 3512; see the RFC itself for\n        full legal notices.')
bldgHVACObjects = MibIdentifier((1, 3, 6, 1, 3, 122, 1))
bldgConformance = MibIdentifier((1, 3, 6, 1, 3, 122, 2))

class BldgHvacOperation(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2))
    namedValues = NamedValues(('heat', 1), ('cool', 2))


bldgHVACTable = MibTable((1, 3, 6, 1, 3, 122, 1, 1))
if mibBuilder.loadTexts:
    bldgHVACTable.setDescription('This table is the representation and data control\n        for building HVAC by each individual office.\n        The table has rows for, and is indexed by a specific\n        floor and office number.  Each such row includes\n        HVAC statistical and current status information for\n        the associated office.  The row also contains a\n        bldgHVACCfgTemplate columnar object that relates the\n        bldgHVACTable row to a row in the bldgHVACCfgTemplateTable.\n        If this value is nonzero, then the instance in the row\n        that has a value for how the HVAC has been configured\n        in the associated template (bldgHVACCfgTeplateTable row).\n        Hence, the bldgHVACCfgTeplateTable row contains the\n        specific configuration values for the offices as described\n        in this table.')
bldgHVACEntry = MibTableRow((1, 3, 6, 1, 3, 122, 1, 1, 1)).setIndexNames((0, 'BLDG-HVAC-MIB',
                                                                          'bldgHVACFloor'), (0,
                                                                                             'BLDG-HVAC-MIB',
                                                                                             'bldgHVACOffice'))
if mibBuilder.loadTexts:
    bldgHVACEntry.setDescription('A row in the bldgHVACTable.  Each row represents a particular\n        office in the building, qualified by its floor and office\n        number.  A given row instance can be created or deleted by\n        set operations  upon its bldgHVACStatus columnar\n        object instance.')
bldgHVACFloor = MibTableColumn((1, 3, 6, 1, 3, 122, 1, 1, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 1000)))
if mibBuilder.loadTexts:
    bldgHVACFloor.setDescription('This portion of the index indicates the floor of the\n         building.  The ground floor is considered the\n         first floor.  For the purposes of this example,\n         floors under the ground floor cannot be\n         controlled using this MIB module.')
bldgHVACOffice = MibTableColumn((1, 3, 6, 1, 3, 122, 1, 1, 1, 2), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)))
if mibBuilder.loadTexts:
    bldgHVACOffice.setDescription('This second component of the index specifies the\n        office number.')
bldgHVACCfgTemplate = MibTableColumn((1, 3, 6, 1, 3, 122, 1, 1, 1, 3), Unsigned32()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    bldgHVACCfgTemplate.setDescription("The index (bldgHVACCfgTemplateIndex instance)\n        of an entry in the 'bldgHVACCfgTemplateTable'.\n        The bldgHVACCfgTable row instance referenced\n        is a pre-made configuration 'template'\n        that represents the configuration described\n        by the bldgHVACCfgTemplateInfoDescr object.  Note\n        that not all configurations will be under a\n        defined template.  As a result, a row in this\n        bldgHVACTable may point to an entry in the\n        bldgHVACCfgTemplateTable that does not in turn\n        have a reference (bldgHVACCfgTemplateInfo) to an\n        entry in the bldgHVACCfgTemplateInfoTable.  The\n        benefit of this approach is that all\n        configuration information is available in one\n        table whether all elements in the system are\n        derived from configured templates or not.\n\n        Where the instance value for this colunmar object\n        is zero, this row represents data for an office\n        whose HVAC status can be monitored using the\n        read-only columnar object instances of this\n        row, but is not under the configuration control\n\n        of the agent.")
bldgHVACFanSpeed = MibTableColumn((1, 3, 6, 1, 3, 122, 1, 1, 1, 4), Gauge32()).setUnits('revolutions per minute').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bldgHVACFanSpeed.setDescription('Shows the revolutions per minute of the fan.  Fan speed\n        will vary based on the difference between\n        bldgHVACCfgTemplateDesiredTemp and bldgHVACCurrentTemp.  The\n        speed is measured in revolutions of the fan blade per minute.')
bldgHVACCurrentTemp = MibTableColumn((1, 3, 6, 1, 3, 122, 1, 1, 1, 5), Gauge32()).setUnits('degrees in celsius').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bldgHVACCurrentTemp.setDescription('The current measured temperature in the office.  Should\n        the current temperature be measured at a value of less\n        than zero degrees celsius, a read of the instance\n        for this object will return a value of zero.')
bldgHVACCoolOrHeatMins = MibTableColumn((1, 3, 6, 1, 3, 122, 1, 1, 1, 6), Counter32()).setUnits('minutes').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bldgHVACCoolOrHeatMins.setDescription('The total number of heating or cooling minutes that have\n        been consumed since the row was activated.  Notice that\n        whether the minutes represent heating or cooling is a\n        function of the configuration of this row.  If the system\n        is re-initialized from a cooling to heating function or\n        vice versa, then the counter would start over again.  This\n        effect is similar to a reconfiguration of some network\n        interface cards.  When parameters that impact\n        configuration are changed, the subsystem must be\n        re-initialized.  Discontinuities in the value of this counter\n        can occur at re-initialization of the management system,\n        and at other times as indicated by the value of\n        bldgHVACDiscontinuityTime.')
bldgHVACDiscontinuityTime = MibTableColumn((1, 3, 6, 1, 3, 122, 1, 1, 1, 7), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bldgHVACDiscontinuityTime.setDescription('The value of sysUpTime on the most recent occasion at which\n        any heating or cooling operation for the office designated\n        by this row instance experienced a discontinuity.  If\n        no such discontinuities have occurred since the last re-\n        initialization of the this row, then this object contains a\n        zero value.')
bldgHVACOwner = MibTableColumn((1, 3, 6, 1, 3, 122, 1, 1, 1, 8), SnmpAdminString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    bldgHVACOwner.setDescription("The identity of the operator/system that\n        last modified this entry.  When a new entry\n        is created, a valid SnmpAdminString must\n        be supplied.  If, on the other hand, this\n        entry is populated by the agent 'discovering'\n        unconfigured rooms, the empty string is a valid\n        value for this object.")
bldgHVACStorageType = MibTableColumn((1, 3, 6, 1, 3, 122, 1, 1, 1, 9), StorageType()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    bldgHVACStorageType.setDescription("The persistence of this row of the table in system storage,\n        as it pertains to permanence across system resets.  A columnar\n        instance of this object with value 'permanent' need not allow\n        write-access to any of the columnar object instances in the\n        containing row.")
bldgHVACStatus = MibTableColumn((1, 3, 6, 1, 3, 122, 1, 1, 1, 10), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    bldgHVACStatus.setDescription('Controls and reflects the creation and activation status of\n        a row in this table.\n\n        No attempt to modify a row columnar object instance value in\n\n        the bldgHVACTable should be issued while the value of\n        bldgHVACStatus is active(1).  Should an agent receive a SET\n        PDU attempting such a modification in this state, an\n        inconsistentValue error should be returned as a result of\n        the SET attempt.')
bldgHVACCfgTemplateInfoTable = MibTable((1, 3, 6, 1, 3, 122, 1, 2))
if mibBuilder.loadTexts:
    bldgHVACCfgTemplateInfoTable.setDescription('This table provides unique string identification for\n        HVAC templates in a network.  If it were necessary to\n        configure rooms to deliver a particular quality of climate\n        control with regard to cooling or heating, the index string\n        of a row in this table could be the template name.\n        The bldgHVACCfgCfgTemplateInfoDescription\n        contains a brief description of the template service objective\n        such as: provides summer cooling settings for executive\n        offices.  The bldgHVACCfgTemplateInfo in the\n        bldgHVACCfgTemplateTable will contain the pointer to the\n        relevant row in this table if it is intended that items\n        that point to a row in the bldgHVACCfgTemplateInfoTable be\n        identifiable as being under template control though this\n        mechanism.')
bldgHVACCfgTemplateInfoEntry = MibTableRow((1, 3, 6, 1, 3, 122, 1, 2, 1)).setIndexNames((0,
                                                                                         'BLDG-HVAC-MIB',
                                                                                         'bldgHVACCfgTemplateInfoIndex'))
if mibBuilder.loadTexts:
    bldgHVACCfgTemplateInfoEntry.setDescription('Each row represents a particular template and\n        description.  A given row instance can be created or\n        deleted by set operations upon its\n        bldgHVACCfgTemplateInfoStatus columnar object\n        instance.')
bldgHVACCfgTemplateInfoIndex = MibTableColumn((1, 3, 6, 1, 3, 122, 1, 2, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)))
if mibBuilder.loadTexts:
    bldgHVACCfgTemplateInfoIndex.setDescription('The unique index to a row in this table.')
bldgHVACCfgTemplateInfoID = MibTableColumn((1, 3, 6, 1, 3, 122, 1, 2, 1, 2), SnmpAdminString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    bldgHVACCfgTemplateInfoID.setDescription("Textual identifier for this table row, and, consequently\n        the template.  This should be a unique name within\n        an administrative domain for a particular template so that\n        all systems in a network that are under the same template\n        can have the same 'handle' (e.g., 'Executive Offices',\n        'Lobby Areas').")
bldgHVACCfgTemplateInfoDescr = MibTableColumn((1, 3, 6, 1, 3, 122, 1, 2, 1, 3), SnmpAdminString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    bldgHVACCfgTemplateInfoDescr.setDescription('A general description of the template.  One example might\n        be - Controls the cooling for offices on higher floors\n        during the summer.')
bldgHVACCfgTemplateInfoOwner = MibTableColumn((1, 3, 6, 1, 3, 122, 1, 2, 1, 4), SnmpAdminString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    bldgHVACCfgTemplateInfoOwner.setDescription('The identity of the operator/system that last modified\n        this entry.')
bldgHVACCfgTemplateInfoStatus = MibTableColumn((1, 3, 6, 1, 3, 122, 1, 2, 1, 5), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    bldgHVACCfgTemplateInfoStatus.setDescription('The activation status of this row.\n\n        No attempt to modify a row columnar object instance value in\n        the bldgHVACCfgTemplateInfo Table should be issued while the\n        value of bldgHVACCfgTemplateInfoStatus is active(1).\n        Should an agent receive a SET PDU attempting such a modification\n        in this state, an inconsistentValue error should be returned as\n        a result of the SET attempt.')
bldgHVACCfgTemplateInfoStorType = MibTableColumn((1, 3, 6, 1, 3, 122, 1, 2, 1, 6), StorageType()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    bldgHVACCfgTemplateInfoStorType.setDescription("The persistence of this row of the table in system storage,\n         as it pertains to permanence across system resets.  A columnar\n        instance of this object with value 'permanent' need not allow\n        write-access to any of the columnar object instances in the\n        containing row.")
bldgHVACCfgTemplateTable = MibTable((1, 3, 6, 1, 3, 122, 1, 3))
if mibBuilder.loadTexts:
    bldgHVACCfgTemplateTable.setDescription("This table contains the templates, which\n        can be used to set defaults that will\n        be applied to specific offices.  The application\n        of those values is accomplished by having a row\n        instance of the bldgHVACTable reference a row of\n        this table (by the value of the former's\n        bldgHVACCfgTemplate columnar instance).  Identifying\n        information concerning a row instance of this table\n        can be found in the columnar data of the row instance\n        of the bldgHVACCfgTemplateInfoTable entry referenced\n        by the bldgHVACCfgTemplateInfo columnar object of\n        this table.")
bldgHVACCfgTemplateEntry = MibTableRow((1, 3, 6, 1, 3, 122, 1, 3, 1)).setIndexNames((0,
                                                                                     'BLDG-HVAC-MIB',
                                                                                     'bldgHVACCfgTemplateIndex'))
if mibBuilder.loadTexts:
    bldgHVACCfgTemplateEntry.setDescription('Each row represents a single set of template parameters\n        that can be applied to selected instances - in this case\n        offices.  These policies will be turned on and off by the\n        policy module through its scheduling facilities.\n\n        A given row instance can be created or\n        deleted by set operations upon its\n        bldgHVACCfgTemplateStatus columnar object instance.')
bldgHVACCfgTemplateIndex = MibTableColumn((1, 3, 6, 1, 3, 122, 1, 3, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)))
if mibBuilder.loadTexts:
    bldgHVACCfgTemplateIndex.setDescription('A unique value for each defined template in this\n        table.  This value can be referenced as a row index\n        by any MIB module that needs access to this information.\n        The bldgHVACCfgTemplate will point to entries in this\n        table.')
bldgHVACCfgTemplateDesiredTemp = MibTableColumn((1, 3, 6, 1, 3, 122, 1, 3, 1, 2), Gauge32()).setUnits('degrees in celsius').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    bldgHVACCfgTemplateDesiredTemp.setDescription('This is the desired temperature setting.  It might be\n        changed at different times of the day or based on\n        seasonal conditions.  It is permitted to change this value\n        by first moving the row to an inactive state, making the\n\n        change and then reactivating the row.')
bldgHVACCfgTemplateCoolOrHeat = MibTableColumn((1, 3, 6, 1, 3, 122, 1, 3, 1, 3), BldgHvacOperation()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    bldgHVACCfgTemplateCoolOrHeat.setDescription('This controls the heating and cooling mechanism and is\n        set-able by building maintenance.  It is permitted to\n        change this value by first moving the row to an inactive\n        state, making the change and then reactivating the row.')
bldgHVACCfgTemplateInfo = MibTableColumn((1, 3, 6, 1, 3, 122, 1, 3, 1, 4), Unsigned32()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    bldgHVACCfgTemplateInfo.setDescription('This object points to a row in the\n        bldgHVACCfgTemplateInfoTable.  This controls the\n        heating and cooling mechanism and is set-able by\n        building maintenance.  It is permissible to change\n        this value by first moving the row to an inactive\n        state, making the change and then reactivating\n        the row.  A value of zero means that this entry\n        is not associated with a named template found\n        in the bldgHVACCfgTemplateInfoTable.')
bldgHVACCfgTemplateOwner = MibTableColumn((1, 3, 6, 1, 3, 122, 1, 3, 1, 5), SnmpAdminString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    bldgHVACCfgTemplateOwner.setDescription('The identity of the administrative entity\n        that created this row of the table.')
bldgHVACCfgTemplateStorage = MibTableColumn((1, 3, 6, 1, 3, 122, 1, 3, 1, 6), StorageType()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    bldgHVACCfgTemplateStorage.setDescription("The persistence of this row of the table across\n         system resets.  A columnar instance of this object with\n         value 'permanent' need not allow write-access to any\n         of the columnar object instances in the containing row.")
bldgHVACCfgTemplateStatus = MibTableColumn((1, 3, 6, 1, 3, 122, 1, 3, 1, 7), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    bldgHVACCfgTemplateStatus.setDescription('The activation status of this row of the table.\n\n        No attempt to modify a row columnar object instance value in\n        the bldgHVACCfgTemplateTable should be issued while the\n        value of bldgHVACCfgTemplateStatus is active(1).\n        Should an agent receive a SET PDU attempting such a modification\n        in this state, an inconsistentValue error should be returned as\n        a result of the SET attempt.')
bldgCompliances = MibIdentifier((1, 3, 6, 1, 3, 122, 2, 1))
bldgGroups = MibIdentifier((1, 3, 6, 1, 3, 122, 2, 2))
bldgCompliance = ModuleCompliance((1, 3, 6, 1, 3, 122, 2, 1, 1)).setObjects(*(('BLDG-HVAC-MIB', 'bldgHVACObjectsGroup'), ))
if mibBuilder.loadTexts:
    bldgCompliance.setDescription('The requirements for conformance to the BLDG-HVAC-MIB.  The\n         bldgHVACObjects group must be implemented to conform to the\n         BLDG-HVAC-MIB.')
bldgHVACObjectsGroup = ObjectGroup((1, 3, 6, 1, 3, 122, 2, 2, 1)).setObjects(*(('BLDG-HVAC-MIB', 'bldgHVACCfgTemplate'), ('BLDG-HVAC-MIB', 'bldgHVACFanSpeed'), ('BLDG-HVAC-MIB', 'bldgHVACCurrentTemp'), ('BLDG-HVAC-MIB', 'bldgHVACCoolOrHeatMins'), ('BLDG-HVAC-MIB', 'bldgHVACDiscontinuityTime'), ('BLDG-HVAC-MIB', 'bldgHVACOwner'), ('BLDG-HVAC-MIB', 'bldgHVACStatus'), ('BLDG-HVAC-MIB', 'bldgHVACStorageType'), ('BLDG-HVAC-MIB', 'bldgHVACCfgTemplateInfoID'), ('BLDG-HVAC-MIB', 'bldgHVACCfgTemplateInfoDescr'), ('BLDG-HVAC-MIB', 'bldgHVACCfgTemplateInfoOwner'), ('BLDG-HVAC-MIB', 'bldgHVACCfgTemplateInfoStatus'), ('BLDG-HVAC-MIB', 'bldgHVACCfgTemplateInfoStorType'), ('BLDG-HVAC-MIB', 'bldgHVACCfgTemplateDesiredTemp'), ('BLDG-HVAC-MIB', 'bldgHVACCfgTemplateCoolOrHeat'), ('BLDG-HVAC-MIB', 'bldgHVACCfgTemplateInfo'), ('BLDG-HVAC-MIB', 'bldgHVACCfgTemplateOwner'), ('BLDG-HVAC-MIB', 'bldgHVACCfgTemplateStorage'), ('BLDG-HVAC-MIB', 'bldgHVACCfgTemplateStatus')))
if mibBuilder.loadTexts:
    bldgHVACObjectsGroup.setDescription('The bldgHVACObjects Group.')
mibBuilder.exportSymbols('BLDG-HVAC-MIB', bldgHVACOffice=bldgHVACOffice, bldgHVACCfgTemplateTable=bldgHVACCfgTemplateTable, bldgHVACTable=bldgHVACTable, bldgHVACCoolOrHeatMins=bldgHVACCoolOrHeatMins, bldgCompliances=bldgCompliances, bldgHVACStorageType=bldgHVACStorageType, bldgHVACEntry=bldgHVACEntry, BldgHvacOperation=BldgHvacOperation, bldgConformance=bldgConformance, bldgHVACCfgTemplateInfo=bldgHVACCfgTemplateInfo, bldgHVACOwner=bldgHVACOwner, bldgHVACCfgTemplateInfoDescr=bldgHVACCfgTemplateInfoDescr, bldgHVACCfgTemplateDesiredTemp=bldgHVACCfgTemplateDesiredTemp, bldgGroups=bldgGroups, bldgHVACCfgTemplateInfoIndex=bldgHVACCfgTemplateInfoIndex, bldgHVACCfgTemplateInfoStatus=bldgHVACCfgTemplateInfoStatus, bldgHVACCfgTemplateInfoTable=bldgHVACCfgTemplateInfoTable, bldgHVACCfgTemplateInfoEntry=bldgHVACCfgTemplateInfoEntry, bldgHVACCurrentTemp=bldgHVACCurrentTemp, bldgHVACCfgTemplateEntry=bldgHVACCfgTemplateEntry, PYSNMP_MODULE_ID=bldgHVACMIB, bldgHVACCfgTemplateOwner=bldgHVACCfgTemplateOwner, bldgHVACCfgTemplateStorage=bldgHVACCfgTemplateStorage, bldgHVACMIB=bldgHVACMIB, bldgHVACCfgTemplateIndex=bldgHVACCfgTemplateIndex, bldgHVACCfgTemplateStatus=bldgHVACCfgTemplateStatus, bldgHVACCfgTemplateInfoID=bldgHVACCfgTemplateInfoID, bldgHVACObjectsGroup=bldgHVACObjectsGroup, bldgHVACDiscontinuityTime=bldgHVACDiscontinuityTime, bldgHVACCfgTemplateCoolOrHeat=bldgHVACCfgTemplateCoolOrHeat, bldgHVACObjects=bldgHVACObjects, bldgHVACFanSpeed=bldgHVACFanSpeed, bldgCompliance=bldgCompliance, bldgHVACCfgTemplateInfoOwner=bldgHVACCfgTemplateInfoOwner, bldgHVACFloor=bldgHVACFloor, bldgHVACStatus=bldgHVACStatus, bldgHVACCfgTemplate=bldgHVACCfgTemplate, bldgHVACCfgTemplateInfoStorType=bldgHVACCfgTemplateInfoStorType)