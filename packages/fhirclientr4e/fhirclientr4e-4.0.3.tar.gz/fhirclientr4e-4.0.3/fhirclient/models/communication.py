#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Communication) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Communication(domainresource.DomainResource):
    """ A record of information transmitted from a sender to a receiver.
    
    An occurrence of information being transmitted; e.g. an alert that was sent
    to a responsible provider, a public health agency that was notified about a
    reportable condition.
    """
    
    resource_type = "Communication"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Unique identifier."""
    _attribute_docstrings['instantiatesCanonical'] = """Instantiates FHIR protocol or definition."""
    _attribute_docstrings['instantiatesUri'] = """Instantiates external protocol or definition."""
    _attribute_docstrings['basedOn'] = """Request fulfilled by this communication."""
    _attribute_docstrings['partOf'] = """Part of this action."""
    _attribute_docstrings['inResponseTo'] = """Reply to."""
    _attribute_docstrings['status'] = """The status of the transmission."""
    _attribute_docstrings['statusReason'] = """Captures the reason for the current state of the Communication."""
    _attribute_docstrings['category'] = """The type of message conveyed such as alert, notification, reminder, instruction, etc."""
    _attribute_docstrings['priority'] = """Characterizes how quickly the planned or in progress communication must be addressed. Includes concepts such as stat, urgent, routine."""
    _attribute_docstrings['medium'] = """A channel of communication."""
    _attribute_docstrings['subject'] = """Focus of message."""
    _attribute_docstrings['topic'] = """Description of the purpose/content, similar to a subject line in an email."""
    _attribute_docstrings['about'] = """Resources that pertain to this communication."""
    _attribute_docstrings['encounter'] = """Encounter created as part of."""
    _attribute_docstrings['sent'] = """When sent."""
    _attribute_docstrings['received'] = """When received."""
    _attribute_docstrings['recipient'] = """Message recipient."""
    _attribute_docstrings['sender'] = """Message sender."""
    _attribute_docstrings['reasonCode'] = """Indication for message."""
    _attribute_docstrings['reasonReference'] = """Why was communication done?."""
    _attribute_docstrings['payload'] = """Message payload."""
    _attribute_docstrings['note'] = """Comments made about the communication."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/event-status',
        'restricted_to': ['preparation', 'in-progress', 'not-done', 'on-hold', 'stopped', 'completed', 'entered-in-error', 'unknown'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['statusReason'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/communication-not-done-reason',
        'restricted_to': ['unknown', 'system-error', 'invalid-phone-number', 'recipient-unavailable', 'family-objection', 'patient-objection'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['category'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/communication-category',
        'restricted_to': ['alert', 'notification', 'reminder', 'instruction'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['priority'] = {
        'url': 'http://hl7.org/fhir/request-priority',
        'restricted_to': ['routine', 'urgent', 'asap', 'stat'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['topic'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/communication-topic',
        'restricted_to': ['prescription-refill-request', 'progress-update', 'report-labs', 'appointment-reminder', 'phone-consult', 'summary-report'],
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
        
        self.identifier = None
        """ Unique identifier.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.instantiatesCanonical = None
        """ Instantiates FHIR protocol or definition.
        List of `str` items. """
        
        self.instantiatesUri = None
        """ Instantiates external protocol or definition.
        List of `str` items. """
        
        self.basedOn = None
        """ Request fulfilled by this communication.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.partOf = None
        """ Part of this action.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.inResponseTo = None
        """ Reply to.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.status = None
        """ The status of the transmission.
        Type `str`. """
        
        self.statusReason = None
        """ Captures the reason for the current state of the Communication.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.category = None
        """ The type of message conveyed such as alert, notification, reminder,
        instruction, etc.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.priority = None
        """ Characterizes how quickly the planned or in progress communication
        must be addressed. Includes concepts such as stat, urgent, routine.
        Type `str`. """
        
        self.medium = None
        """ A channel of communication.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.subject = None
        """ Focus of message.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.topic = None
        """ Description of the purpose/content, similar to a subject line in an
        email.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.about = None
        """ Resources that pertain to this communication.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Encounter created as part of.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.sent = None
        """ When sent.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.received = None
        """ When received.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.recipient = None
        """ Message recipient.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.sender = None
        """ Message sender.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.reasonCode = None
        """ Indication for message.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.reasonReference = None
        """ Why was communication done?.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.payload = None
        """ Message payload.
        List of `CommunicationPayload` items (represented as `dict` in JSON). """
        
        self.note = None
        """ Comments made about the communication.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        super(Communication, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Communication, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("instantiatesCanonical", "instantiatesCanonical", str, True, None, False),
            ("instantiatesUri", "instantiatesUri", str, True, None, False),
            ("basedOn", "basedOn", fhirreference.FHIRReference, True, None, False),
            ("partOf", "partOf", fhirreference.FHIRReference, True, None, False),
            ("inResponseTo", "inResponseTo", fhirreference.FHIRReference, True, None, False),
            ("status", "status", str, False, None, True),
            ("statusReason", "statusReason", codeableconcept.CodeableConcept, False, None, False),
            ("category", "category", codeableconcept.CodeableConcept, True, None, False),
            ("priority", "priority", str, False, None, False),
            ("medium", "medium", codeableconcept.CodeableConcept, True, None, False),
            ("subject", "subject", fhirreference.FHIRReference, False, None, False),
            ("topic", "topic", codeableconcept.CodeableConcept, False, None, False),
            ("about", "about", fhirreference.FHIRReference, True, None, False),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("sent", "sent", fhirdate.FHIRDate, False, None, False),
            ("received", "received", fhirdate.FHIRDate, False, None, False),
            ("recipient", "recipient", fhirreference.FHIRReference, True, None, False),
            ("sender", "sender", fhirreference.FHIRReference, False, None, False),
            ("reasonCode", "reasonCode", codeableconcept.CodeableConcept, True, None, False),
            ("reasonReference", "reasonReference", fhirreference.FHIRReference, True, None, False),
            ("payload", "payload", CommunicationPayload, True, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
        ])
        return js


from . import backboneelement

class CommunicationPayload(backboneelement.BackboneElement):
    """ Message payload.
    
    Text, attachment(s), or resource(s) that was communicated to the recipient.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['contentString'] = """Message part content."""
    _attribute_docstrings['contentAttachment'] = """Message part content."""
    _attribute_docstrings['contentReference'] = """Message part content."""

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
        
        self.contentString = None
        """ Message part content.
        Type `str`. """
        
        self.contentAttachment = None
        """ Message part content.
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.contentReference = None
        """ Message part content.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(CommunicationPayload, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CommunicationPayload, self).elementProperties()
        js.extend([
            ("contentString", "contentString", str, False, "content", True),
            ("contentAttachment", "contentAttachment", attachment.Attachment, False, "content", True),
            ("contentReference", "contentReference", fhirreference.FHIRReference, False, "content", True),
        ])
        return js


import sys
try:
    from . import annotation
except ImportError:
    annotation = sys.modules[__package__ + '.annotation']
try:
    from . import attachment
except ImportError:
    attachment = sys.modules[__package__ + '.attachment']
try:
    from . import codeableconcept
except ImportError:
    codeableconcept = sys.modules[__package__ + '.codeableconcept']
try:
    from . import fhirdate
except ImportError:
    fhirdate = sys.modules[__package__ + '.fhirdate']
try:
    from . import fhirreference
except ImportError:
    fhirreference = sys.modules[__package__ + '.fhirreference']
try:
    from . import identifier
except ImportError:
    identifier = sys.modules[__package__ + '.identifier']
