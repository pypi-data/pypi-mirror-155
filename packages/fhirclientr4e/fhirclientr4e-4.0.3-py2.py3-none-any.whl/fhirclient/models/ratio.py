#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Ratio) on 2022-06-21.
#  2022, SMART Health IT.


from . import element

class Ratio(element.Element):
    """ A ratio of two Quantity values - a numerator and a denominator.
    
    A relationship of two Quantity values - expressed as a numerator and a
    denominator.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['numerator'] = """Numerator value."""
    _attribute_docstrings['denominator'] = """Denominator value."""

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
        
        self.numerator = None
        """ Numerator value.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.denominator = None
        """ Denominator value.
        Type `Quantity` (represented as `dict` in JSON). """
        
        super(Ratio, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Ratio, self).elementProperties()
        js.extend([
            ("numerator", "numerator", quantity.Quantity, False, None, False),
            ("denominator", "denominator", quantity.Quantity, False, None, False),
        ])
        return js


import sys
try:
    from . import quantity
except ImportError:
    quantity = sys.modules[__package__ + '.quantity']
