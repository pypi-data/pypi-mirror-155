#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Population) on 2022-06-21.
#  2022, SMART Health IT.


from . import backboneelement

class Population(backboneelement.BackboneElement):
    """ A definition of a set of people that apply to some clinically related
    context, for example people contraindicated for a certain medication.
    
    A populatioof people with some set of grouping criteria.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['ageRange'] = """The age of the specific population."""
    _attribute_docstrings['ageCodeableConcept'] = """The age of the specific population."""
    _attribute_docstrings['gender'] = """The gender of the specific population."""
    _attribute_docstrings['race'] = """Race of the specific population."""
    _attribute_docstrings['physiologicalCondition'] = """The existing physiological conditions of the specific population to which this applies."""

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
        
        self.ageRange = None
        """ The age of the specific population.
        Type `Range` (represented as `dict` in JSON). """
        
        self.ageCodeableConcept = None
        """ The age of the specific population.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.gender = None
        """ The gender of the specific population.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.race = None
        """ Race of the specific population.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.physiologicalCondition = None
        """ The existing physiological conditions of the specific population to
        which this applies.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(Population, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Population, self).elementProperties()
        js.extend([
            ("ageRange", "ageRange", range.Range, False, "age", False),
            ("ageCodeableConcept", "ageCodeableConcept", codeableconcept.CodeableConcept, False, "age", False),
            ("gender", "gender", codeableconcept.CodeableConcept, False, None, False),
            ("race", "race", codeableconcept.CodeableConcept, False, None, False),
            ("physiologicalCondition", "physiologicalCondition", codeableconcept.CodeableConcept, False, None, False),
        ])
        return js


import sys
try:
    from . import codeableconcept
except ImportError:
    codeableconcept = sys.modules[__package__ + '.codeableconcept']
try:
    from . import range
except ImportError:
    range = sys.modules[__package__ + '.range']
