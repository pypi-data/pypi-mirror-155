#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/DeviceRequest) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class DeviceRequest(domainresource.DomainResource):
    """ Medical device request.
    
    Represents a request for a patient to employ a medical device. The device
    may be an implantable device, or an external assistive device, such as a
    walker.
    """
    
    resource_type = "DeviceRequest"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """External Request identifier."""
    _attribute_docstrings['instantiatesCanonical'] = """Instantiates FHIR protocol or definition."""
    _attribute_docstrings['instantiatesUri'] = """Instantiates external protocol or definition."""
    _attribute_docstrings['basedOn'] = """What request fulfills."""
    _attribute_docstrings['priorRequest'] = """What request replaces."""
    _attribute_docstrings['groupIdentifier'] = """Identifier of composite request."""
    _attribute_docstrings['status'] = """The status of the request."""
    _attribute_docstrings['intent'] = """Whether the request is a proposal, plan, an original order or a reflex order."""
    _attribute_docstrings['priority'] = """Indicates how quickly the {{title}} should be addressed with respect to other requests."""
    _attribute_docstrings['codeReference'] = """Device requested."""
    _attribute_docstrings['codeCodeableConcept'] = """Device requested."""
    _attribute_docstrings['parameter'] = """Device details."""
    _attribute_docstrings['subject'] = """Focus of request."""
    _attribute_docstrings['encounter'] = """Encounter motivating request."""
    _attribute_docstrings['occurrenceDateTime'] = """Desired time or schedule for use."""
    _attribute_docstrings['occurrencePeriod'] = """Desired time or schedule for use."""
    _attribute_docstrings['occurrenceTiming'] = """Desired time or schedule for use."""
    _attribute_docstrings['authoredOn'] = """When recorded."""
    _attribute_docstrings['requester'] = """Who/what is requesting diagnostics."""
    _attribute_docstrings['performerType'] = """Filler role."""
    _attribute_docstrings['performer'] = """Requested Filler."""
    _attribute_docstrings['reasonCode'] = """Coded Reason for request."""
    _attribute_docstrings['reasonReference'] = """Linked Reason for request."""
    _attribute_docstrings['insurance'] = """Associated insurance coverage."""
    _attribute_docstrings['supportingInfo'] = """Additional clinical information."""
    _attribute_docstrings['note'] = """Notes or comments."""
    _attribute_docstrings['relevantHistory'] = """Request provenance."""

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
    _attribute_enums['intent'] = {
        'url': 'http://hl7.org/fhir/request-intent',
        'restricted_to': ['proposal', 'plan', 'directive', 'order', 'original-order', 'reflex-order', 'filler-order', 'instance-order', 'option'],
        'binding_strength': 'required',
        'class_name': 'str'
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
        """ External Request identifier.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.instantiatesCanonical = None
        """ Instantiates FHIR protocol or definition.
        List of `str` items. """
        
        self.instantiatesUri = None
        """ Instantiates external protocol or definition.
        List of `str` items. """
        
        self.basedOn = None
        """ What request fulfills.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.priorRequest = None
        """ What request replaces.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.groupIdentifier = None
        """ Identifier of composite request.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.status = None
        """ The status of the request.
        Type `str`. """
        
        self.intent = None
        """ Whether the request is a proposal, plan, an original order or a
        reflex order.
        Type `str`. """
        
        self.priority = None
        """ Indicates how quickly the {{title}} should be addressed with
        respect to other requests.
        Type `str`. """
        
        self.codeReference = None
        """ Device requested.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.codeCodeableConcept = None
        """ Device requested.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.parameter = None
        """ Device details.
        List of `DeviceRequestParameter` items (represented as `dict` in JSON). """
        
        self.subject = None
        """ Focus of request.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Encounter motivating request.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.occurrenceDateTime = None
        """ Desired time or schedule for use.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.occurrencePeriod = None
        """ Desired time or schedule for use.
        Type `Period` (represented as `dict` in JSON). """
        
        self.occurrenceTiming = None
        """ Desired time or schedule for use.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.authoredOn = None
        """ When recorded.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.requester = None
        """ Who/what is requesting diagnostics.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.performerType = None
        """ Filler role.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.performer = None
        """ Requested Filler.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.reasonCode = None
        """ Coded Reason for request.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.reasonReference = None
        """ Linked Reason for request.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.insurance = None
        """ Associated insurance coverage.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.supportingInfo = None
        """ Additional clinical information.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.note = None
        """ Notes or comments.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        self.relevantHistory = None
        """ Request provenance.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(DeviceRequest, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DeviceRequest, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("instantiatesCanonical", "instantiatesCanonical", str, True, None, False),
            ("instantiatesUri", "instantiatesUri", str, True, None, False),
            ("basedOn", "basedOn", fhirreference.FHIRReference, True, None, False),
            ("priorRequest", "priorRequest", fhirreference.FHIRReference, True, None, False),
            ("groupIdentifier", "groupIdentifier", identifier.Identifier, False, None, False),
            ("status", "status", str, False, None, False),
            ("intent", "intent", str, False, None, True),
            ("priority", "priority", str, False, None, False),
            ("codeReference", "codeReference", fhirreference.FHIRReference, False, "code", True),
            ("codeCodeableConcept", "codeCodeableConcept", codeableconcept.CodeableConcept, False, "code", True),
            ("parameter", "parameter", DeviceRequestParameter, True, None, False),
            ("subject", "subject", fhirreference.FHIRReference, False, None, True),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("occurrenceDateTime", "occurrenceDateTime", fhirdate.FHIRDate, False, "occurrence", False),
            ("occurrencePeriod", "occurrencePeriod", period.Period, False, "occurrence", False),
            ("occurrenceTiming", "occurrenceTiming", timing.Timing, False, "occurrence", False),
            ("authoredOn", "authoredOn", fhirdate.FHIRDate, False, None, False),
            ("requester", "requester", fhirreference.FHIRReference, False, None, False),
            ("performerType", "performerType", codeableconcept.CodeableConcept, False, None, False),
            ("performer", "performer", fhirreference.FHIRReference, False, None, False),
            ("reasonCode", "reasonCode", codeableconcept.CodeableConcept, True, None, False),
            ("reasonReference", "reasonReference", fhirreference.FHIRReference, True, None, False),
            ("insurance", "insurance", fhirreference.FHIRReference, True, None, False),
            ("supportingInfo", "supportingInfo", fhirreference.FHIRReference, True, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
            ("relevantHistory", "relevantHistory", fhirreference.FHIRReference, True, None, False),
        ])
        return js


from . import backboneelement

class DeviceRequestParameter(backboneelement.BackboneElement):
    """ Device details.
    
    Specific parameters for the ordered item.  For example, the prism value for
    lenses.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Device detail."""
    _attribute_docstrings['valueCodeableConcept'] = """Value of detail."""
    _attribute_docstrings['valueQuantity'] = """Value of detail."""
    _attribute_docstrings['valueRange'] = """Value of detail."""
    _attribute_docstrings['valueBoolean'] = """Value of detail."""

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
        
        self.code = None
        """ Device detail.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.valueCodeableConcept = None
        """ Value of detail.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.valueQuantity = None
        """ Value of detail.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.valueRange = None
        """ Value of detail.
        Type `Range` (represented as `dict` in JSON). """
        
        self.valueBoolean = None
        """ Value of detail.
        Type `bool`. """
        
        super(DeviceRequestParameter, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DeviceRequestParameter, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("valueCodeableConcept", "valueCodeableConcept", codeableconcept.CodeableConcept, False, "value", False),
            ("valueQuantity", "valueQuantity", quantity.Quantity, False, "value", False),
            ("valueRange", "valueRange", range.Range, False, "value", False),
            ("valueBoolean", "valueBoolean", bool, False, "value", False),
        ])
        return js


import sys
try:
    from . import annotation
except ImportError:
    annotation = sys.modules[__package__ + '.annotation']
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
try:
    from . import quantity
except ImportError:
    quantity = sys.modules[__package__ + '.quantity']
try:
    from . import range
except ImportError:
    range = sys.modules[__package__ + '.range']
try:
    from . import timing
except ImportError:
    timing = sys.modules[__package__ + '.timing']
