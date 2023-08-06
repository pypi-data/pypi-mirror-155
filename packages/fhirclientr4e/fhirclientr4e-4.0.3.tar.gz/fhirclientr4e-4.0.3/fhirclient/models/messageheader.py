#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/MessageHeader) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class MessageHeader(domainresource.DomainResource):
    """ A resource that describes a message that is exchanged between systems.
    
    The header for a message exchange that is either requesting or responding
    to an action.  The reference(s) that are the subject of the action as well
    as other information related to the action are typically transmitted in a
    bundle in which the MessageHeader resource instance is the first resource
    in the bundle.
    """
    
    resource_type = "MessageHeader"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['eventCoding'] = """Code for the event this message represents or link to event definition."""
    _attribute_docstrings['eventUri'] = """Code for the event this message represents or link to event definition."""
    _attribute_docstrings['destination'] = """Message destination application(s)."""
    _attribute_docstrings['sender'] = """Real world sender of the message."""
    _attribute_docstrings['enterer'] = """The source of the data entry."""
    _attribute_docstrings['author'] = """The source of the decision."""
    _attribute_docstrings['source'] = """Message source application."""
    _attribute_docstrings['responsible'] = """Final responsibility for event."""
    _attribute_docstrings['reason'] = """Coded indication of the cause for the event - indicates  a reason for the occurrence of the event that is a focus of this message."""
    _attribute_docstrings['response'] = """If this is a reply to prior message."""
    _attribute_docstrings['focus'] = """The actual content of the message."""
    _attribute_docstrings['definition'] = """Link to the definition for this message."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['reason'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/message-reasons-encounter',
        'restricted_to': ['admit', 'discharge', 'absent', 'return', 'moved', 'edit'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
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
        
        self.eventCoding = None
        """ Code for the event this message represents or link to event
        definition.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.eventUri = None
        """ Code for the event this message represents or link to event
        definition.
        Type `str`. """
        
        self.destination = None
        """ Message destination application(s).
        List of `MessageHeaderDestination` items (represented as `dict` in JSON). """
        
        self.sender = None
        """ Real world sender of the message.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.enterer = None
        """ The source of the data entry.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.author = None
        """ The source of the decision.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.source = None
        """ Message source application.
        Type `MessageHeaderSource` (represented as `dict` in JSON). """
        
        self.responsible = None
        """ Final responsibility for event.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.reason = None
        """ Coded indication of the cause for the event - indicates  a reason
        for the occurrence of the event that is a focus of this message.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.response = None
        """ If this is a reply to prior message.
        Type `MessageHeaderResponse` (represented as `dict` in JSON). """
        
        self.focus = None
        """ The actual content of the message.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.definition = None
        """ Link to the definition for this message.
        Type `str`. """
        
        super(MessageHeader, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MessageHeader, self).elementProperties()
        js.extend([
            ("eventCoding", "eventCoding", coding.Coding, False, "event", True),
            ("eventUri", "eventUri", str, False, "event", True),
            ("destination", "destination", MessageHeaderDestination, True, None, False),
            ("sender", "sender", fhirreference.FHIRReference, False, None, False),
            ("enterer", "enterer", fhirreference.FHIRReference, False, None, False),
            ("author", "author", fhirreference.FHIRReference, False, None, False),
            ("source", "source", MessageHeaderSource, False, None, True),
            ("responsible", "responsible", fhirreference.FHIRReference, False, None, False),
            ("reason", "reason", codeableconcept.CodeableConcept, False, None, False),
            ("response", "response", MessageHeaderResponse, False, None, False),
            ("focus", "focus", fhirreference.FHIRReference, True, None, False),
            ("definition", "definition", str, False, None, False),
        ])
        return js


from . import backboneelement

class MessageHeaderDestination(backboneelement.BackboneElement):
    """ Message destination application(s).
    
    The destination application which the message is intended for.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['name'] = """Name of system."""
    _attribute_docstrings['target'] = """Particular delivery destination within the destination."""
    _attribute_docstrings['endpoint'] = """Actual destination address or id."""
    _attribute_docstrings['receiver'] = """Intended "real-world" recipient for the data."""

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
        
        self.name = None
        """ Name of system.
        Type `str`. """
        
        self.target = None
        """ Particular delivery destination within the destination.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.endpoint = None
        """ Actual destination address or id.
        Type `str`. """
        
        self.receiver = None
        """ Intended "real-world" recipient for the data.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(MessageHeaderDestination, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MessageHeaderDestination, self).elementProperties()
        js.extend([
            ("name", "name", str, False, None, False),
            ("target", "target", fhirreference.FHIRReference, False, None, False),
            ("endpoint", "endpoint", str, False, None, True),
            ("receiver", "receiver", fhirreference.FHIRReference, False, None, False),
        ])
        return js


class MessageHeaderResponse(backboneelement.BackboneElement):
    """ If this is a reply to prior message.
    
    Information about the message that this message is a response to.  Only
    present if this message is a response.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Id of original message."""
    _attribute_docstrings['code'] = """Code that identifies the type of response to the message - whether it was successful or not, and whether it should be resent or not."""
    _attribute_docstrings['details'] = """Specific list of hints/warnings/errors."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['code'] = {
        'url': 'http://hl7.org/fhir/response-code',
        'restricted_to': ['ok', 'transient-error', 'fatal-error'],
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
        
        self.identifier = None
        """ Id of original message.
        Type `str`. """
        
        self.code = None
        """ Code that identifies the type of response to the message - whether
        it was successful or not, and whether it should be resent or not.
        Type `str`. """
        
        self.details = None
        """ Specific list of hints/warnings/errors.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(MessageHeaderResponse, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MessageHeaderResponse, self).elementProperties()
        js.extend([
            ("identifier", "identifier", str, False, None, True),
            ("code", "code", str, False, None, True),
            ("details", "details", fhirreference.FHIRReference, False, None, False),
        ])
        return js


class MessageHeaderSource(backboneelement.BackboneElement):
    """ Message source application.
    
    The source application from which this message originated.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['name'] = """Name of system."""
    _attribute_docstrings['software'] = """Name of software running the system."""
    _attribute_docstrings['version'] = """Version of software running."""
    _attribute_docstrings['contact'] = """Human contact for problems."""
    _attribute_docstrings['endpoint'] = """Actual message source address or id."""

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
        
        self.name = None
        """ Name of system.
        Type `str`. """
        
        self.software = None
        """ Name of software running the system.
        Type `str`. """
        
        self.version = None
        """ Version of software running.
        Type `str`. """
        
        self.contact = None
        """ Human contact for problems.
        Type `ContactPoint` (represented as `dict` in JSON). """
        
        self.endpoint = None
        """ Actual message source address or id.
        Type `str`. """
        
        super(MessageHeaderSource, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MessageHeaderSource, self).elementProperties()
        js.extend([
            ("name", "name", str, False, None, False),
            ("software", "software", str, False, None, False),
            ("version", "version", str, False, None, False),
            ("contact", "contact", contactpoint.ContactPoint, False, None, False),
            ("endpoint", "endpoint", str, False, None, True),
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
    from . import contactpoint
except ImportError:
    contactpoint = sys.modules[__package__ + '.contactpoint']
try:
    from . import fhirreference
except ImportError:
    fhirreference = sys.modules[__package__ + '.fhirreference']
