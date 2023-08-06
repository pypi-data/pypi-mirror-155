#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/SupplyDelivery) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class SupplyDelivery(domainresource.DomainResource):
    """ Delivery of bulk Supplies.
    
    Record of delivery of what is supplied.
    """
    
    resource_type = "SupplyDelivery"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """External identifier."""
    _attribute_docstrings['basedOn'] = """Fulfills plan, proposal or order."""
    _attribute_docstrings['partOf'] = """Part of referenced event."""
    _attribute_docstrings['status'] = """A code specifying the state of the dispense event."""
    _attribute_docstrings['patient'] = """Patient for whom the item is supplied."""
    _attribute_docstrings['type'] = """Indicates the type of dispensing event that is performed. Examples include: Trial Fill, Completion of Trial, Partial Fill, Emergency Fill, Samples, etc."""
    _attribute_docstrings['suppliedItem'] = """The item that is delivered or supplied."""
    _attribute_docstrings['occurrenceDateTime'] = """When event occurred."""
    _attribute_docstrings['occurrencePeriod'] = """When event occurred."""
    _attribute_docstrings['occurrenceTiming'] = """When event occurred."""
    _attribute_docstrings['supplier'] = """Dispenser."""
    _attribute_docstrings['destination'] = """Where the Supply was sent."""
    _attribute_docstrings['receiver'] = """Who collected the Supply."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/supplydelivery-status',
        'restricted_to': ['in-progress', 'completed', 'abandoned', 'entered-in-error'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/supply-item-type',
        'restricted_to': ['medication', 'device'],
        'binding_strength': 'required',
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
        """ External identifier.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.basedOn = None
        """ Fulfills plan, proposal or order.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.partOf = None
        """ Part of referenced event.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.status = None
        """ A code specifying the state of the dispense event.
        Type `str`. """
        
        self.patient = None
        """ Patient for whom the item is supplied.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.type = None
        """ Indicates the type of dispensing event that is performed. Examples
        include: Trial Fill, Completion of Trial, Partial Fill, Emergency
        Fill, Samples, etc.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.suppliedItem = None
        """ The item that is delivered or supplied.
        Type `SupplyDeliverySuppliedItem` (represented as `dict` in JSON). """
        
        self.occurrenceDateTime = None
        """ When event occurred.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.occurrencePeriod = None
        """ When event occurred.
        Type `Period` (represented as `dict` in JSON). """
        
        self.occurrenceTiming = None
        """ When event occurred.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.supplier = None
        """ Dispenser.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.destination = None
        """ Where the Supply was sent.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.receiver = None
        """ Who collected the Supply.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(SupplyDelivery, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SupplyDelivery, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("basedOn", "basedOn", fhirreference.FHIRReference, True, None, False),
            ("partOf", "partOf", fhirreference.FHIRReference, True, None, False),
            ("status", "status", str, False, None, False),
            ("patient", "patient", fhirreference.FHIRReference, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("suppliedItem", "suppliedItem", SupplyDeliverySuppliedItem, False, None, False),
            ("occurrenceDateTime", "occurrenceDateTime", fhirdate.FHIRDate, False, "occurrence", False),
            ("occurrencePeriod", "occurrencePeriod", period.Period, False, "occurrence", False),
            ("occurrenceTiming", "occurrenceTiming", timing.Timing, False, "occurrence", False),
            ("supplier", "supplier", fhirreference.FHIRReference, False, None, False),
            ("destination", "destination", fhirreference.FHIRReference, False, None, False),
            ("receiver", "receiver", fhirreference.FHIRReference, True, None, False),
        ])
        return js


from . import backboneelement

class SupplyDeliverySuppliedItem(backboneelement.BackboneElement):
    """ The item that is delivered or supplied.
    
    The item that is being delivered or has been supplied.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['quantity'] = """Amount dispensed."""
    _attribute_docstrings['itemCodeableConcept'] = """Medication, Substance, or Device supplied."""
    _attribute_docstrings['itemReference'] = """Medication, Substance, or Device supplied."""

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
        
        self.quantity = None
        """ Amount dispensed.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.itemCodeableConcept = None
        """ Medication, Substance, or Device supplied.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.itemReference = None
        """ Medication, Substance, or Device supplied.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(SupplyDeliverySuppliedItem, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SupplyDeliverySuppliedItem, self).elementProperties()
        js.extend([
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("itemCodeableConcept", "itemCodeableConcept", codeableconcept.CodeableConcept, False, "item", False),
            ("itemReference", "itemReference", fhirreference.FHIRReference, False, "item", False),
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
    from . import timing
except ImportError:
    timing = sys.modules[__package__ + '.timing']
