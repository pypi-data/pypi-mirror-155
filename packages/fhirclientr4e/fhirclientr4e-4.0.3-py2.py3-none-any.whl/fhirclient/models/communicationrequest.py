#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/CommunicationRequest) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class CommunicationRequest(domainresource.DomainResource):
    """ A request for information to be sent to a receiver.
    
    A request to convey information; e.g. the CDS system proposes that an alert
    be sent to a responsible provider, the CDS system proposes that the public
    health agency be notified about a reportable condition.
    """
    
    resource_type = "CommunicationRequest"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Unique identifier."""
    _attribute_docstrings['basedOn'] = """Fulfills plan or proposal."""
    _attribute_docstrings['replaces'] = """Request(s) replaced by this request."""
    _attribute_docstrings['groupIdentifier'] = """Composite request this is part of."""
    _attribute_docstrings['status'] = """The status of the proposal or order."""
    _attribute_docstrings['statusReason'] = """Reason for current status."""
    _attribute_docstrings['category'] = """The type of message to be sent such as alert, notification, reminder, instruction, etc."""
    _attribute_docstrings['priority'] = """Characterizes how quickly the proposed act must be initiated. Includes concepts such as stat, urgent, routine."""
    _attribute_docstrings['doNotPerform'] = """True if request is prohibiting action."""
    _attribute_docstrings['medium'] = """A channel of communication."""
    _attribute_docstrings['subject'] = """Focus of message."""
    _attribute_docstrings['about'] = """Resources that pertain to this communication request."""
    _attribute_docstrings['encounter'] = """Encounter created as part of."""
    _attribute_docstrings['payload'] = """Message payload."""
    _attribute_docstrings['occurrenceDateTime'] = """When scheduled."""
    _attribute_docstrings['occurrencePeriod'] = """When scheduled."""
    _attribute_docstrings['authoredOn'] = """When request transitioned to being actionable."""
    _attribute_docstrings['requester'] = """Who/what is requesting service."""
    _attribute_docstrings['recipient'] = """Message recipient."""
    _attribute_docstrings['sender'] = """Message sender."""
    _attribute_docstrings['reasonCode'] = """Why is communication needed?."""
    _attribute_docstrings['reasonReference'] = """Why is communication needed?."""
    _attribute_docstrings['note'] = """Comments made about communication request."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/request-status',
        'restricted_to': ['draft', 'active', 'on-hold', 'revoked', 'completed', 'entered-in-error', 'unknown'],
        'binding_strength': 'required',
        'class_name': 'str'
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
        
        self.basedOn = None
        """ Fulfills plan or proposal.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.replaces = None
        """ Request(s) replaced by this request.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.groupIdentifier = None
        """ Composite request this is part of.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.status = None
        """ The status of the proposal or order.
        Type `str`. """
        
        self.statusReason = None
        """ Reason for current status.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.category = None
        """ The type of message to be sent such as alert, notification,
        reminder, instruction, etc.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.priority = None
        """ Characterizes how quickly the proposed act must be initiated.
        Includes concepts such as stat, urgent, routine.
        Type `str`. """
        
        self.doNotPerform = None
        """ True if request is prohibiting action.
        Type `bool`. """
        
        self.medium = None
        """ A channel of communication.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.subject = None
        """ Focus of message.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.about = None
        """ Resources that pertain to this communication request.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Encounter created as part of.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.payload = None
        """ Message payload.
        List of `CommunicationRequestPayload` items (represented as `dict` in JSON). """
        
        self.occurrenceDateTime = None
        """ When scheduled.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.occurrencePeriod = None
        """ When scheduled.
        Type `Period` (represented as `dict` in JSON). """
        
        self.authoredOn = None
        """ When request transitioned to being actionable.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.requester = None
        """ Who/what is requesting service.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.recipient = None
        """ Message recipient.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.sender = None
        """ Message sender.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.reasonCode = None
        """ Why is communication needed?.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.reasonReference = None
        """ Why is communication needed?.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.note = None
        """ Comments made about communication request.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        super(CommunicationRequest, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CommunicationRequest, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("basedOn", "basedOn", fhirreference.FHIRReference, True, None, False),
            ("replaces", "replaces", fhirreference.FHIRReference, True, None, False),
            ("groupIdentifier", "groupIdentifier", identifier.Identifier, False, None, False),
            ("status", "status", str, False, None, True),
            ("statusReason", "statusReason", codeableconcept.CodeableConcept, False, None, False),
            ("category", "category", codeableconcept.CodeableConcept, True, None, False),
            ("priority", "priority", str, False, None, False),
            ("doNotPerform", "doNotPerform", bool, False, None, False),
            ("medium", "medium", codeableconcept.CodeableConcept, True, None, False),
            ("subject", "subject", fhirreference.FHIRReference, False, None, False),
            ("about", "about", fhirreference.FHIRReference, True, None, False),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("payload", "payload", CommunicationRequestPayload, True, None, False),
            ("occurrenceDateTime", "occurrenceDateTime", fhirdate.FHIRDate, False, "occurrence", False),
            ("occurrencePeriod", "occurrencePeriod", period.Period, False, "occurrence", False),
            ("authoredOn", "authoredOn", fhirdate.FHIRDate, False, None, False),
            ("requester", "requester", fhirreference.FHIRReference, False, None, False),
            ("recipient", "recipient", fhirreference.FHIRReference, True, None, False),
            ("sender", "sender", fhirreference.FHIRReference, False, None, False),
            ("reasonCode", "reasonCode", codeableconcept.CodeableConcept, True, None, False),
            ("reasonReference", "reasonReference", fhirreference.FHIRReference, True, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
        ])
        return js


from . import backboneelement

class CommunicationRequestPayload(backboneelement.BackboneElement):
    """ Message payload.
    
    Text, attachment(s), or resource(s) to be communicated to the recipient.
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
        
        super(CommunicationRequestPayload, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CommunicationRequestPayload, self).elementProperties()
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
try:
    from . import period
except ImportError:
    period = sys.modules[__package__ + '.period']
