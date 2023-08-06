#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/SupplyRequest) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class SupplyRequest(domainresource.DomainResource):
    """ Request for a medication, substance or device.
    
    A record of a request for a medication, substance or device used in the
    healthcare setting.
    """
    
    resource_type = "SupplyRequest"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business Identifier for SupplyRequest."""
    _attribute_docstrings['status'] = """Status of the supply request."""
    _attribute_docstrings['category'] = """Category of supply, e.g.  central, non-stock, etc. This is used to support work flows associated with the supply process."""
    _attribute_docstrings['priority'] = """Indicates how quickly this SupplyRequest should be addressed with respect to other requests."""
    _attribute_docstrings['itemCodeableConcept'] = """Medication, Substance, or Device requested to be supplied."""
    _attribute_docstrings['itemReference'] = """Medication, Substance, or Device requested to be supplied."""
    _attribute_docstrings['quantity'] = """The requested amount of the item indicated."""
    _attribute_docstrings['parameter'] = """Ordered item details."""
    _attribute_docstrings['occurrenceDateTime'] = """When the request should be fulfilled."""
    _attribute_docstrings['occurrencePeriod'] = """When the request should be fulfilled."""
    _attribute_docstrings['occurrenceTiming'] = """When the request should be fulfilled."""
    _attribute_docstrings['authoredOn'] = """When the request was made."""
    _attribute_docstrings['requester'] = """Individual making the request."""
    _attribute_docstrings['supplier'] = """Who is intended to fulfill the request."""
    _attribute_docstrings['reasonCode'] = """None"""
    _attribute_docstrings['reasonReference'] = """The reason why the supply item was requested."""
    _attribute_docstrings['deliverFrom'] = """The origin of the supply."""
    _attribute_docstrings['deliverTo'] = """The destination of the supply."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/supplyrequest-status',
        'restricted_to': ['draft', 'active', 'suspended', 'cancelled', 'completed', 'entered-in-error', 'unknown'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['category'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/supply-kind',
        'restricted_to': ['central', 'nonstock'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['priority'] = {
        'url': 'http://hl7.org/fhir/request-priority',
        'restricted_to': ['routine', 'urgent', 'asap', 'stat'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['reasonCode'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/supplyrequest-reason',
        'restricted_to': ['patient-care', 'ward-stock'],
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
        """ Business Identifier for SupplyRequest.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ Status of the supply request.
        Type `str`. """
        
        self.category = None
        """ Category of supply, e.g.  central, non-stock, etc. This is used to
        support work flows associated with the supply process.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.priority = None
        """ Indicates how quickly this SupplyRequest should be addressed with
        respect to other requests.
        Type `str`. """
        
        self.itemCodeableConcept = None
        """ Medication, Substance, or Device requested to be supplied.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.itemReference = None
        """ Medication, Substance, or Device requested to be supplied.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.quantity = None
        """ The requested amount of the item indicated.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.parameter = None
        """ Ordered item details.
        List of `SupplyRequestParameter` items (represented as `dict` in JSON). """
        
        self.occurrenceDateTime = None
        """ When the request should be fulfilled.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.occurrencePeriod = None
        """ When the request should be fulfilled.
        Type `Period` (represented as `dict` in JSON). """
        
        self.occurrenceTiming = None
        """ When the request should be fulfilled.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.authoredOn = None
        """ When the request was made.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.requester = None
        """ Individual making the request.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.supplier = None
        """ Who is intended to fulfill the request.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.reasonCode = None
        """ None.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.reasonReference = None
        """ The reason why the supply item was requested.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.deliverFrom = None
        """ The origin of the supply.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.deliverTo = None
        """ The destination of the supply.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(SupplyRequest, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SupplyRequest, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, False),
            ("category", "category", codeableconcept.CodeableConcept, False, None, False),
            ("priority", "priority", str, False, None, False),
            ("itemCodeableConcept", "itemCodeableConcept", codeableconcept.CodeableConcept, False, "item", True),
            ("itemReference", "itemReference", fhirreference.FHIRReference, False, "item", True),
            ("quantity", "quantity", quantity.Quantity, False, None, True),
            ("parameter", "parameter", SupplyRequestParameter, True, None, False),
            ("occurrenceDateTime", "occurrenceDateTime", fhirdate.FHIRDate, False, "occurrence", False),
            ("occurrencePeriod", "occurrencePeriod", period.Period, False, "occurrence", False),
            ("occurrenceTiming", "occurrenceTiming", timing.Timing, False, "occurrence", False),
            ("authoredOn", "authoredOn", fhirdate.FHIRDate, False, None, False),
            ("requester", "requester", fhirreference.FHIRReference, False, None, False),
            ("supplier", "supplier", fhirreference.FHIRReference, True, None, False),
            ("reasonCode", "reasonCode", codeableconcept.CodeableConcept, True, None, False),
            ("reasonReference", "reasonReference", fhirreference.FHIRReference, True, None, False),
            ("deliverFrom", "deliverFrom", fhirreference.FHIRReference, False, None, False),
            ("deliverTo", "deliverTo", fhirreference.FHIRReference, False, None, False),
        ])
        return js


from . import backboneelement

class SupplyRequestParameter(backboneelement.BackboneElement):
    """ Ordered item details.
    
    Specific parameters for the ordered item.  For example, the size of the
    indicated item.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Item detail."""
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
        """ Item detail.
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
        
        super(SupplyRequestParameter, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SupplyRequestParameter, self).elementProperties()
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
