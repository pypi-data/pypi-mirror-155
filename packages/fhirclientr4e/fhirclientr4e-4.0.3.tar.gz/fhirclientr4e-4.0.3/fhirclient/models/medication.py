#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Medication) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Medication(domainresource.DomainResource):
    """ Definition of a Medication.
    
    This resource is primarily used for the identification and definition of a
    medication for the purposes of prescribing, dispensing, and administering a
    medication as well as for making statements about medication use.
    """
    
    resource_type = "Medication"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business identifier for this medication."""
    _attribute_docstrings['code'] = """Codes that identify this medication."""
    _attribute_docstrings['status'] = """A code to indicate if the medication is in active use."""
    _attribute_docstrings['manufacturer'] = """Manufacturer of the item."""
    _attribute_docstrings['form'] = """powder | tablets | capsule +."""
    _attribute_docstrings['amount'] = """Amount of drug in package."""
    _attribute_docstrings['ingredient'] = """Active or inactive ingredient."""
    _attribute_docstrings['batch'] = """Details about packaged medications."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/CodeSystem/medication-status',
        'restricted_to': ['active', 'inactive', 'entered-in-error'],
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
        """ Business identifier for this medication.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.code = None
        """ Codes that identify this medication.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.status = None
        """ A code to indicate if the medication is in active use.
        Type `str`. """
        
        self.manufacturer = None
        """ Manufacturer of the item.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.form = None
        """ powder | tablets | capsule +.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.amount = None
        """ Amount of drug in package.
        Type `Ratio` (represented as `dict` in JSON). """
        
        self.ingredient = None
        """ Active or inactive ingredient.
        List of `MedicationIngredient` items (represented as `dict` in JSON). """
        
        self.batch = None
        """ Details about packaged medications.
        Type `MedicationBatch` (represented as `dict` in JSON). """
        
        super(Medication, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Medication, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("status", "status", str, False, None, False),
            ("manufacturer", "manufacturer", fhirreference.FHIRReference, False, None, False),
            ("form", "form", codeableconcept.CodeableConcept, False, None, False),
            ("amount", "amount", ratio.Ratio, False, None, False),
            ("ingredient", "ingredient", MedicationIngredient, True, None, False),
            ("batch", "batch", MedicationBatch, False, None, False),
        ])
        return js


from . import backboneelement

class MedicationBatch(backboneelement.BackboneElement):
    """ Details about packaged medications.
    
    Information that only applies to packages (not products).
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['lotNumber'] = """Identifier assigned to batch."""
    _attribute_docstrings['expirationDate'] = """When batch will expire."""

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
        
        self.lotNumber = None
        """ Identifier assigned to batch.
        Type `str`. """
        
        self.expirationDate = None
        """ When batch will expire.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        super(MedicationBatch, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationBatch, self).elementProperties()
        js.extend([
            ("lotNumber", "lotNumber", str, False, None, False),
            ("expirationDate", "expirationDate", fhirdate.FHIRDate, False, None, False),
        ])
        return js


class MedicationIngredient(backboneelement.BackboneElement):
    """ Active or inactive ingredient.
    
    Identifies a particular constituent of interest in the product.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['itemCodeableConcept'] = """The actual ingredient or content."""
    _attribute_docstrings['itemReference'] = """The actual ingredient or content."""
    _attribute_docstrings['isActive'] = """Active ingredient indicator."""
    _attribute_docstrings['strength'] = """Quantity of ingredient present."""

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
        
        self.itemCodeableConcept = None
        """ The actual ingredient or content.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.itemReference = None
        """ The actual ingredient or content.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.isActive = None
        """ Active ingredient indicator.
        Type `bool`. """
        
        self.strength = None
        """ Quantity of ingredient present.
        Type `Ratio` (represented as `dict` in JSON). """
        
        super(MedicationIngredient, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationIngredient, self).elementProperties()
        js.extend([
            ("itemCodeableConcept", "itemCodeableConcept", codeableconcept.CodeableConcept, False, "item", True),
            ("itemReference", "itemReference", fhirreference.FHIRReference, False, "item", True),
            ("isActive", "isActive", bool, False, None, False),
            ("strength", "strength", ratio.Ratio, False, None, False),
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
    from . import ratio
except ImportError:
    ratio = sys.modules[__package__ + '.ratio']
