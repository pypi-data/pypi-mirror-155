#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Substance) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Substance(domainresource.DomainResource):
    """ A homogeneous material with a definite composition.
    """
    
    resource_type = "Substance"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Unique identifier."""
    _attribute_docstrings['status'] = """A code to indicate if the substance is actively used."""
    _attribute_docstrings['category'] = """A code that classifies the general type of substance.  This is used  for searching, sorting and display purposes."""
    _attribute_docstrings['code'] = """What substance this is."""
    _attribute_docstrings['description'] = """Textual description of the substance, comments."""
    _attribute_docstrings['instance'] = """If this describes a specific package/container of the substance."""
    _attribute_docstrings['ingredient'] = """Composition information about the substance."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/substance-status',
        'restricted_to': ['active', 'inactive', 'entered-in-error'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['category'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/substance-category',
        'restricted_to': ['allergen', 'biological', 'body', 'chemical', 'food', 'drug', 'material'],
        'binding_strength': 'extensible',
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
        
        self.status = None
        """ A code to indicate if the substance is actively used.
        Type `str`. """
        
        self.category = None
        """ A code that classifies the general type of substance.  This is used
        for searching, sorting and display purposes.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.code = None
        """ What substance this is.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.description = None
        """ Textual description of the substance, comments.
        Type `str`. """
        
        self.instance = None
        """ If this describes a specific package/container of the substance.
        List of `SubstanceInstance` items (represented as `dict` in JSON). """
        
        self.ingredient = None
        """ Composition information about the substance.
        List of `SubstanceIngredient` items (represented as `dict` in JSON). """
        
        super(Substance, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Substance, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, False),
            ("category", "category", codeableconcept.CodeableConcept, True, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, True),
            ("description", "description", str, False, None, False),
            ("instance", "instance", SubstanceInstance, True, None, False),
            ("ingredient", "ingredient", SubstanceIngredient, True, None, False),
        ])
        return js


from . import backboneelement

class SubstanceIngredient(backboneelement.BackboneElement):
    """ Composition information about the substance.
    
    A substance can be composed of other substances.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['quantity'] = """Optional amount (concentration)."""
    _attribute_docstrings['substanceCodeableConcept'] = """A component of the substance."""
    _attribute_docstrings['substanceReference'] = """A component of the substance."""

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
        """ Optional amount (concentration).
        Type `Ratio` (represented as `dict` in JSON). """
        
        self.substanceCodeableConcept = None
        """ A component of the substance.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.substanceReference = None
        """ A component of the substance.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(SubstanceIngredient, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SubstanceIngredient, self).elementProperties()
        js.extend([
            ("quantity", "quantity", ratio.Ratio, False, None, False),
            ("substanceCodeableConcept", "substanceCodeableConcept", codeableconcept.CodeableConcept, False, "substance", True),
            ("substanceReference", "substanceReference", fhirreference.FHIRReference, False, "substance", True),
        ])
        return js


class SubstanceInstance(backboneelement.BackboneElement):
    """ If this describes a specific package/container of the substance.
    
    Substance may be used to describe a kind of substance, or a specific
    package/container of the substance: an instance.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Identifier of the package/container."""
    _attribute_docstrings['expiry'] = """When no longer valid to use."""
    _attribute_docstrings['quantity'] = """Amount of substance in the package."""

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
        
        self.identifier = None
        """ Identifier of the package/container.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.expiry = None
        """ When no longer valid to use.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.quantity = None
        """ Amount of substance in the package.
        Type `Quantity` (represented as `dict` in JSON). """
        
        super(SubstanceInstance, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SubstanceInstance, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, False, None, False),
            ("expiry", "expiry", fhirdate.FHIRDate, False, None, False),
            ("quantity", "quantity", quantity.Quantity, False, None, False),
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
    from . import quantity
except ImportError:
    quantity = sys.modules[__package__ + '.quantity']
try:
    from . import ratio
except ImportError:
    ratio = sys.modules[__package__ + '.ratio']
