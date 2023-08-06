#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/SampledData) on 2022-06-21.
#  2022, SMART Health IT.


from . import element

class SampledData(element.Element):
    """ A series of measurements taken by a device.
    
    A series of measurements taken by a device, with upper and lower limits.
    There may be more than one dimension in the data.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['origin'] = """Zero value and units."""
    _attribute_docstrings['period'] = """Number of milliseconds between samples."""
    _attribute_docstrings['factor'] = """Multiply data by this before adding to origin."""
    _attribute_docstrings['lowerLimit'] = """Lower limit of detection."""
    _attribute_docstrings['upperLimit'] = """Upper limit of detection."""
    _attribute_docstrings['dimensions'] = """Number of sample points at each time point."""
    _attribute_docstrings['data'] = """Decimal values with spaces, or "E" | "U" | "L"."""

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
        
        self.origin = None
        """ Zero value and units.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.period = None
        """ Number of milliseconds between samples.
        Type `float`. """
        
        self.factor = None
        """ Multiply data by this before adding to origin.
        Type `float`. """
        
        self.lowerLimit = None
        """ Lower limit of detection.
        Type `float`. """
        
        self.upperLimit = None
        """ Upper limit of detection.
        Type `float`. """
        
        self.dimensions = None
        """ Number of sample points at each time point.
        Type `int`. """
        
        self.data = None
        """ Decimal values with spaces, or "E" | "U" | "L".
        Type `str`. """
        
        super(SampledData, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SampledData, self).elementProperties()
        js.extend([
            ("origin", "origin", quantity.Quantity, False, None, True),
            ("period", "period", float, False, None, True),
            ("factor", "factor", float, False, None, False),
            ("lowerLimit", "lowerLimit", float, False, None, False),
            ("upperLimit", "upperLimit", float, False, None, False),
            ("dimensions", "dimensions", int, False, None, True),
            ("data", "data", str, False, None, False),
        ])
        return js


import sys
try:
    from . import quantity
except ImportError:
    quantity = sys.modules[__package__ + '.quantity']
