#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/MedicinalProductUndesirableEffect) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class MedicinalProductUndesirableEffect(domainresource.DomainResource):
    """ MedicinalProductUndesirableEffect.
    
    Describe the undesirable effects of the medicinal product.
    """
    
    resource_type = "MedicinalProductUndesirableEffect"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['subject'] = """The medication for which this is an indication."""
    _attribute_docstrings['symptomConditionEffect'] = """The symptom, condition or undesirable effect."""
    _attribute_docstrings['classification'] = """Classification of the effect."""
    _attribute_docstrings['frequencyOfOccurrence'] = """The frequency of occurrence of the effect."""
    _attribute_docstrings['population'] = """The population group to which this applies."""

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
        """ The medication for which this is an indication.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.symptomConditionEffect = None
        """ The symptom, condition or undesirable effect.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.classification = None
        """ Classification of the effect.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.frequencyOfOccurrence = None
        """ The frequency of occurrence of the effect.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.population = None
        """ The population group to which this applies.
        List of `Population` items (represented as `dict` in JSON). """
        
        super(MedicinalProductUndesirableEffect, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicinalProductUndesirableEffect, self).elementProperties()
        js.extend([
            ("subject", "subject", fhirreference.FHIRReference, True, None, False),
            ("symptomConditionEffect", "symptomConditionEffect", codeableconcept.CodeableConcept, False, None, False),
            ("classification", "classification", codeableconcept.CodeableConcept, False, None, False),
            ("frequencyOfOccurrence", "frequencyOfOccurrence", codeableconcept.CodeableConcept, False, None, False),
            ("population", "population", population.Population, True, None, False),
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
try:
    from . import population
except ImportError:
    population = sys.modules[__package__ + '.population']
