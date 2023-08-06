#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/ServiceRequest) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class ServiceRequest(domainresource.DomainResource):
    """ A request for a service to be performed.
    
    A record of a request for service such as diagnostic investigations,
    treatments, or operations to be performed.
    """
    
    resource_type = "ServiceRequest"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Identifiers assigned to this order."""
    _attribute_docstrings['instantiatesCanonical'] = """Instantiates FHIR protocol or definition."""
    _attribute_docstrings['instantiatesUri'] = """Instantiates external protocol or definition."""
    _attribute_docstrings['basedOn'] = """What request fulfills."""
    _attribute_docstrings['replaces'] = """What request replaces."""
    _attribute_docstrings['requisition'] = """Composite Request ID."""
    _attribute_docstrings['status'] = """The status of the order."""
    _attribute_docstrings['intent'] = """Whether the request is a proposal, plan, an original order or a reflex order."""
    _attribute_docstrings['category'] = """Classification of service."""
    _attribute_docstrings['priority'] = """Indicates how quickly the ServiceRequest should be addressed with respect to other requests."""
    _attribute_docstrings['doNotPerform'] = """True if service/procedure should not be performed."""
    _attribute_docstrings['code'] = """What is being requested/ordered."""
    _attribute_docstrings['orderDetail'] = """Additional order information."""
    _attribute_docstrings['quantityQuantity'] = """Service amount."""
    _attribute_docstrings['quantityRatio'] = """Service amount."""
    _attribute_docstrings['quantityRange'] = """Service amount."""
    _attribute_docstrings['subject'] = """Individual or Entity the service is ordered for."""
    _attribute_docstrings['encounter'] = """Encounter in which the request was created."""
    _attribute_docstrings['occurrenceDateTime'] = """When service should occur."""
    _attribute_docstrings['occurrencePeriod'] = """When service should occur."""
    _attribute_docstrings['occurrenceTiming'] = """When service should occur."""
    _attribute_docstrings['asNeededBoolean'] = """Preconditions for service."""
    _attribute_docstrings['asNeededCodeableConcept'] = """Preconditions for service."""
    _attribute_docstrings['authoredOn'] = """Date request signed."""
    _attribute_docstrings['requester'] = """Who/what is requesting service."""
    _attribute_docstrings['performerType'] = """Performer role."""
    _attribute_docstrings['performer'] = """Requested performer."""
    _attribute_docstrings['locationCode'] = """Requested location."""
    _attribute_docstrings['locationReference'] = """Requested location."""
    _attribute_docstrings['reasonCode'] = """Explanation/Justification for procedure or service."""
    _attribute_docstrings['reasonReference'] = """Explanation/Justification for service or service."""
    _attribute_docstrings['insurance'] = """Associated insurance coverage."""
    _attribute_docstrings['supportingInfo'] = """Additional clinical information."""
    _attribute_docstrings['specimen'] = """Procedure Samples."""
    _attribute_docstrings['bodySite'] = """Location on Body."""
    _attribute_docstrings['note'] = """Comments."""
    _attribute_docstrings['patientInstruction'] = """Patient or consumer-oriented instructions."""
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
        """ Identifiers assigned to this order.
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
        
        self.replaces = None
        """ What request replaces.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.requisition = None
        """ Composite Request ID.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.status = None
        """ The status of the order.
        Type `str`. """
        
        self.intent = None
        """ Whether the request is a proposal, plan, an original order or a
        reflex order.
        Type `str`. """
        
        self.category = None
        """ Classification of service.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.priority = None
        """ Indicates how quickly the ServiceRequest should be addressed with
        respect to other requests.
        Type `str`. """
        
        self.doNotPerform = None
        """ True if service/procedure should not be performed.
        Type `bool`. """
        
        self.code = None
        """ What is being requested/ordered.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.orderDetail = None
        """ Additional order information.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.quantityQuantity = None
        """ Service amount.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.quantityRatio = None
        """ Service amount.
        Type `Ratio` (represented as `dict` in JSON). """
        
        self.quantityRange = None
        """ Service amount.
        Type `Range` (represented as `dict` in JSON). """
        
        self.subject = None
        """ Individual or Entity the service is ordered for.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Encounter in which the request was created.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.occurrenceDateTime = None
        """ When service should occur.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.occurrencePeriod = None
        """ When service should occur.
        Type `Period` (represented as `dict` in JSON). """
        
        self.occurrenceTiming = None
        """ When service should occur.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.asNeededBoolean = None
        """ Preconditions for service.
        Type `bool`. """
        
        self.asNeededCodeableConcept = None
        """ Preconditions for service.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.authoredOn = None
        """ Date request signed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.requester = None
        """ Who/what is requesting service.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.performerType = None
        """ Performer role.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.performer = None
        """ Requested performer.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.locationCode = None
        """ Requested location.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.locationReference = None
        """ Requested location.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.reasonCode = None
        """ Explanation/Justification for procedure or service.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.reasonReference = None
        """ Explanation/Justification for service or service.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.insurance = None
        """ Associated insurance coverage.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.supportingInfo = None
        """ Additional clinical information.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.specimen = None
        """ Procedure Samples.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.bodySite = None
        """ Location on Body.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.note = None
        """ Comments.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        self.patientInstruction = None
        """ Patient or consumer-oriented instructions.
        Type `str`. """
        
        self.relevantHistory = None
        """ Request provenance.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(ServiceRequest, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ServiceRequest, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("instantiatesCanonical", "instantiatesCanonical", str, True, None, False),
            ("instantiatesUri", "instantiatesUri", str, True, None, False),
            ("basedOn", "basedOn", fhirreference.FHIRReference, True, None, False),
            ("replaces", "replaces", fhirreference.FHIRReference, True, None, False),
            ("requisition", "requisition", identifier.Identifier, False, None, False),
            ("status", "status", str, False, None, True),
            ("intent", "intent", str, False, None, True),
            ("category", "category", codeableconcept.CodeableConcept, True, None, False),
            ("priority", "priority", str, False, None, False),
            ("doNotPerform", "doNotPerform", bool, False, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("orderDetail", "orderDetail", codeableconcept.CodeableConcept, True, None, False),
            ("quantityQuantity", "quantityQuantity", quantity.Quantity, False, "quantity", False),
            ("quantityRatio", "quantityRatio", ratio.Ratio, False, "quantity", False),
            ("quantityRange", "quantityRange", range.Range, False, "quantity", False),
            ("subject", "subject", fhirreference.FHIRReference, False, None, True),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("occurrenceDateTime", "occurrenceDateTime", fhirdate.FHIRDate, False, "occurrence", False),
            ("occurrencePeriod", "occurrencePeriod", period.Period, False, "occurrence", False),
            ("occurrenceTiming", "occurrenceTiming", timing.Timing, False, "occurrence", False),
            ("asNeededBoolean", "asNeededBoolean", bool, False, "asNeeded", False),
            ("asNeededCodeableConcept", "asNeededCodeableConcept", codeableconcept.CodeableConcept, False, "asNeeded", False),
            ("authoredOn", "authoredOn", fhirdate.FHIRDate, False, None, False),
            ("requester", "requester", fhirreference.FHIRReference, False, None, False),
            ("performerType", "performerType", codeableconcept.CodeableConcept, False, None, False),
            ("performer", "performer", fhirreference.FHIRReference, True, None, False),
            ("locationCode", "locationCode", codeableconcept.CodeableConcept, True, None, False),
            ("locationReference", "locationReference", fhirreference.FHIRReference, True, None, False),
            ("reasonCode", "reasonCode", codeableconcept.CodeableConcept, True, None, False),
            ("reasonReference", "reasonReference", fhirreference.FHIRReference, True, None, False),
            ("insurance", "insurance", fhirreference.FHIRReference, True, None, False),
            ("supportingInfo", "supportingInfo", fhirreference.FHIRReference, True, None, False),
            ("specimen", "specimen", fhirreference.FHIRReference, True, None, False),
            ("bodySite", "bodySite", codeableconcept.CodeableConcept, True, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
            ("patientInstruction", "patientInstruction", str, False, None, False),
            ("relevantHistory", "relevantHistory", fhirreference.FHIRReference, True, None, False),
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
    from . import ratio
except ImportError:
    ratio = sys.modules[__package__ + '.ratio']
try:
    from . import timing
except ImportError:
    timing = sys.modules[__package__ + '.timing']
