#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/AuditEvent) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class AuditEvent(domainresource.DomainResource):
    """ Event record kept for security purposes.
    
    A record of an event made for purposes of maintaining a security log.
    Typical uses include detection of intrusion attempts and monitoring for
    inappropriate usage.
    """
    
    resource_type = "AuditEvent"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Type/identifier of event."""
    _attribute_docstrings['subtype'] = """More specific type/id for the event."""
    _attribute_docstrings['action'] = """Indicator for type of action performed during the event that generated the audit."""
    _attribute_docstrings['period'] = """When the activity occurred."""
    _attribute_docstrings['recorded'] = """Time when the event was recorded."""
    _attribute_docstrings['outcome'] = """Whether the event succeeded or failed."""
    _attribute_docstrings['outcomeDesc'] = """Description of the event outcome."""
    _attribute_docstrings['purposeOfEvent'] = """The purposeOfUse of the event."""
    _attribute_docstrings['agent'] = """Actor involved in the event."""
    _attribute_docstrings['source'] = """Audit Event Reporter."""
    _attribute_docstrings['entity'] = """Data or objects used."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['action'] = {
        'url': 'http://hl7.org/fhir/audit-event-action',
        'restricted_to': ['C', 'R', 'U', 'D', 'E'],
        'binding_strength': 'required',
        'class_name': 'str'
    }

    @classmethod
    def attribute_enums(cls):
        """Get dict of attributes with enums, Code or CodeableConcept."""
        return cls._attribute_enums

    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.type = None
        """ Type/identifier of event.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.subtype = None
        """ More specific type/id for the event.
        List of `Coding` items (represented as `dict` in JSON). """
        
        self.action = None
        """ Indicator for type of action performed during the event that
        generated the audit.
        Type `str`. """
        
        self.period = None
        """ When the activity occurred.
        Type `Period` (represented as `dict` in JSON). """
        
        self.recorded = None
        """ Time when the event was recorded.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.outcome = None
        """ Whether the event succeeded or failed.
        Type `str`. """
        
        self.outcomeDesc = None
        """ Description of the event outcome.
        Type `str`. """
        
        self.purposeOfEvent = None
        """ The purposeOfUse of the event.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.agent = None
        """ Actor involved in the event.
        List of `AuditEventAgent` items (represented as `dict` in JSON). """
        
        self.source = None
        """ Audit Event Reporter.
        Type `AuditEventSource` (represented as `dict` in JSON). """
        
        self.entity = None
        """ Data or objects used.
        List of `AuditEventEntity` items (represented as `dict` in JSON). """
        
        super(AuditEvent, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(AuditEvent, self).elementProperties()
        js.extend([
            ("type", "type", coding.Coding, False, None, True),
            ("subtype", "subtype", coding.Coding, True, None, False),
            ("action", "action", str, False, None, False),
            ("period", "period", period.Period, False, None, False),
            ("recorded", "recorded", fhirdate.FHIRDate, False, None, True),
            ("outcome", "outcome", str, False, None, False),
            ("outcomeDesc", "outcomeDesc", str, False, None, False),
            ("purposeOfEvent", "purposeOfEvent", codeableconcept.CodeableConcept, True, None, False),
            ("agent", "agent", AuditEventAgent, True, None, True),
            ("source", "source", AuditEventSource, False, None, True),
            ("entity", "entity", AuditEventEntity, True, None, False),
        ])
        return js


from . import backboneelement

class AuditEventAgent(backboneelement.BackboneElement):
    """ Actor involved in the event.
    
    An actor taking an active role in the event or activity that is logged.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """How agent participated."""
    _attribute_docstrings['role'] = """Agent role in the event."""
    _attribute_docstrings['who'] = """Identifier of who."""
    _attribute_docstrings['altId'] = """Alternative User identity."""
    _attribute_docstrings['name'] = """Human friendly name for the agent."""
    _attribute_docstrings['requestor'] = """Whether user is initiator."""
    _attribute_docstrings['location'] = """Where."""
    _attribute_docstrings['policy'] = """Policy that authorized event."""
    _attribute_docstrings['media'] = """Type of media."""
    _attribute_docstrings['network'] = """Logical network location for application activity."""
    _attribute_docstrings['purposeOfUse'] = """Reason given for this user."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""

    @classmethod
    def attribute_enums(cls):
        """Get dict of attributes with enums, Code or CodeableConcept."""
        return cls._attribute_enums

    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.type = None
        """ How agent participated.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.role = None
        """ Agent role in the event.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.who = None
        """ Identifier of who.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.altId = None
        """ Alternative User identity.
        Type `str`. """
        
        self.name = None
        """ Human friendly name for the agent.
        Type `str`. """
        
        self.requestor = None
        """ Whether user is initiator.
        Type `bool`. """
        
        self.location = None
        """ Where.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.policy = None
        """ Policy that authorized event.
        List of `str` items. """
        
        self.media = None
        """ Type of media.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.network = None
        """ Logical network location for application activity.
        Type `AuditEventAgentNetwork` (represented as `dict` in JSON). """
        
        self.purposeOfUse = None
        """ Reason given for this user.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        super(AuditEventAgent, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(AuditEventAgent, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("role", "role", codeableconcept.CodeableConcept, True, None, False),
            ("who", "who", fhirreference.FHIRReference, False, None, False),
            ("altId", "altId", str, False, None, False),
            ("name", "name", str, False, None, False),
            ("requestor", "requestor", bool, False, None, True),
            ("location", "location", fhirreference.FHIRReference, False, None, False),
            ("policy", "policy", str, True, None, False),
            ("media", "media", coding.Coding, False, None, False),
            ("network", "network", AuditEventAgentNetwork, False, None, False),
            ("purposeOfUse", "purposeOfUse", codeableconcept.CodeableConcept, True, None, False),
        ])
        return js


class AuditEventAgentNetwork(backboneelement.BackboneElement):
    """ Logical network location for application activity.
    
    Logical network location for application activity, if the activity has a
    network location.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['address'] = """Identifier for the network access point of the user device."""
    _attribute_docstrings['type'] = """The type of network access point."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""

    @classmethod
    def attribute_enums(cls):
        """Get dict of attributes with enums, Code or CodeableConcept."""
        return cls._attribute_enums

    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.address = None
        """ Identifier for the network access point of the user device.
        Type `str`. """
        
        self.type = None
        """ The type of network access point.
        Type `str`. """
        
        super(AuditEventAgentNetwork, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(AuditEventAgentNetwork, self).elementProperties()
        js.extend([
            ("address", "address", str, False, None, False),
            ("type", "type", str, False, None, False),
        ])
        return js


class AuditEventEntity(backboneelement.BackboneElement):
    """ Data or objects used.
    
    Specific instances of data or objects that have been accessed.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['what'] = """Specific instance of resource."""
    _attribute_docstrings['type'] = """Type of entity involved."""
    _attribute_docstrings['role'] = """What role the entity played."""
    _attribute_docstrings['lifecycle'] = """Life-cycle stage for the entity."""
    _attribute_docstrings['securityLabel'] = """Security labels on the entity."""
    _attribute_docstrings['name'] = """Descriptor for entity."""
    _attribute_docstrings['description'] = """Descriptive text."""
    _attribute_docstrings['query'] = """Query parameters."""
    _attribute_docstrings['detail'] = """Additional Information about the entity."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""

    @classmethod
    def attribute_enums(cls):
        """Get dict of attributes with enums, Code or CodeableConcept."""
        return cls._attribute_enums

    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.what = None
        """ Specific instance of resource.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.type = None
        """ Type of entity involved.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.role = None
        """ What role the entity played.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.lifecycle = None
        """ Life-cycle stage for the entity.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.securityLabel = None
        """ Security labels on the entity.
        List of `Coding` items (represented as `dict` in JSON). """
        
        self.name = None
        """ Descriptor for entity.
        Type `str`. """
        
        self.description = None
        """ Descriptive text.
        Type `str`. """
        
        self.query = None
        """ Query parameters.
        Type `str`. """
        
        self.detail = None
        """ Additional Information about the entity.
        List of `AuditEventEntityDetail` items (represented as `dict` in JSON). """
        
        super(AuditEventEntity, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(AuditEventEntity, self).elementProperties()
        js.extend([
            ("what", "what", fhirreference.FHIRReference, False, None, False),
            ("type", "type", coding.Coding, False, None, False),
            ("role", "role", coding.Coding, False, None, False),
            ("lifecycle", "lifecycle", coding.Coding, False, None, False),
            ("securityLabel", "securityLabel", coding.Coding, True, None, False),
            ("name", "name", str, False, None, False),
            ("description", "description", str, False, None, False),
            ("query", "query", str, False, None, False),
            ("detail", "detail", AuditEventEntityDetail, True, None, False),
        ])
        return js


class AuditEventEntityDetail(backboneelement.BackboneElement):
    """ Additional Information about the entity.
    
    Tagged value pairs for conveying additional information about the entity.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Name of the property."""
    _attribute_docstrings['valueString'] = """Property value."""
    _attribute_docstrings['valueBase64Binary'] = """Property value."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""

    @classmethod
    def attribute_enums(cls):
        """Get dict of attributes with enums, Code or CodeableConcept."""
        return cls._attribute_enums

    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.type = None
        """ Name of the property.
        Type `str`. """
        
        self.valueString = None
        """ Property value.
        Type `str`. """
        
        self.valueBase64Binary = None
        """ Property value.
        Type `str`. """
        
        super(AuditEventEntityDetail, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(AuditEventEntityDetail, self).elementProperties()
        js.extend([
            ("type", "type", str, False, None, True),
            ("valueString", "valueString", str, False, "value", True),
            ("valueBase64Binary", "valueBase64Binary", str, False, "value", True),
        ])
        return js


class AuditEventSource(backboneelement.BackboneElement):
    """ Audit Event Reporter.
    
    The system that is reporting the event.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['site'] = """Logical source location within the enterprise."""
    _attribute_docstrings['observer'] = """The identity of source detecting the event."""
    _attribute_docstrings['type'] = """The type of source where event originated."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""

    @classmethod
    def attribute_enums(cls):
        """Get dict of attributes with enums, Code or CodeableConcept."""
        return cls._attribute_enums

    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.site = None
        """ Logical source location within the enterprise.
        Type `str`. """
        
        self.observer = None
        """ The identity of source detecting the event.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.type = None
        """ The type of source where event originated.
        List of `Coding` items (represented as `dict` in JSON). """
        
        super(AuditEventSource, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(AuditEventSource, self).elementProperties()
        js.extend([
            ("site", "site", str, False, None, False),
            ("observer", "observer", fhirreference.FHIRReference, False, None, True),
            ("type", "type", coding.Coding, True, None, False),
        ])
        return js


import sys
try:
    from . import codeableconcept
except ImportError:
    codeableconcept = sys.modules[__package__ + '.codeableconcept']
try:
    from . import coding
except ImportError:
    coding = sys.modules[__package__ + '.coding']
try:
    from . import fhirdate
except ImportError:
    fhirdate = sys.modules[__package__ + '.fhirdate']
try:
    from . import fhirreference
except ImportError:
    fhirreference = sys.modules[__package__ + '.fhirreference']
try:
    from . import period
except ImportError:
    period = sys.modules[__package__ + '.period']
