#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/MedicinalProductInteraction) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class MedicinalProductInteraction(domainresource.DomainResource):
    """ MedicinalProductInteraction.
    
    The interactions of the medicinal product with other medicinal products, or
    other forms of interactions.
    """
    
    resource_type = "MedicinalProductInteraction"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['subject'] = """The medication for which this is a described interaction."""
    _attribute_docstrings['description'] = """The interaction described."""
    _attribute_docstrings['interactant'] = """The specific medication, food or laboratory test that interacts."""
    _attribute_docstrings['type'] = """The type of the interaction e.g. drug-drug interaction, drug-food interaction, drug-lab test interaction."""
    _attribute_docstrings['effect'] = """The effect of the interaction, for example "reduced gastric absorption of primary medication"."""
    _attribute_docstrings['incidence'] = """The incidence of the interaction, e.g. theoretical, observed."""
    _attribute_docstrings['management'] = """Actions for managing the interaction."""

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
        
        self.subject = None
        """ The medication for which this is a described interaction.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.description = None
        """ The interaction described.
        Type `str`. """
        
        self.interactant = None
        """ The specific medication, food or laboratory test that interacts.
        List of `MedicinalProductInteractionInteractant` items (represented as `dict` in JSON). """
        
        self.type = None
        """ The type of the interaction e.g. drug-drug interaction, drug-food
        interaction, drug-lab test interaction.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.effect = None
        """ The effect of the interaction, for example "reduced gastric
        absorption of primary medication".
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.incidence = None
        """ The incidence of the interaction, e.g. theoretical, observed.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.management = None
        """ Actions for managing the interaction.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(MedicinalProductInteraction, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicinalProductInteraction, self).elementProperties()
        js.extend([
            ("subject", "subject", fhirreference.FHIRReference, True, None, False),
            ("description", "description", str, False, None, False),
            ("interactant", "interactant", MedicinalProductInteractionInteractant, True, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("effect", "effect", codeableconcept.CodeableConcept, False, None, False),
            ("incidence", "incidence", codeableconcept.CodeableConcept, False, None, False),
            ("management", "management", codeableconcept.CodeableConcept, False, None, False),
        ])
        return js


from . import backboneelement

class MedicinalProductInteractionInteractant(backboneelement.BackboneElement):
    """ The specific medication, food or laboratory test that interacts.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['itemReference'] = """The specific medication, food or laboratory test that interacts."""
    _attribute_docstrings['itemCodeableConcept'] = """The specific medication, food or laboratory test that interacts."""

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
        
        self.itemReference = None
        """ The specific medication, food or laboratory test that interacts.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.itemCodeableConcept = None
        """ The specific medication, food or laboratory test that interacts.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(MedicinalProductInteractionInteractant, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicinalProductInteractionInteractant, self).elementProperties()
        js.extend([
            ("itemReference", "itemReference", fhirreference.FHIRReference, False, "item", True),
            ("itemCodeableConcept", "itemCodeableConcept", codeableconcept.CodeableConcept, False, "item", True),
        ])
        return js


import sys
try:
    from . import codeableconcept
except ImportError:
    codeableconcept = sys.modules[__package__ + '.codeableconcept']
try:
    from . import fhirreference
except ImportError:
    fhirreference = sys.modules[__package__ + '.fhirreference']
