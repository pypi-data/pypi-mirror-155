#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/MoneyQuantity) on 2022-06-21.
#  2022, SMART Health IT.


from . import element

class Quantity(element.Element):
    """ A measured or measurable amount.
    
    A measured amount (or an amount that can potentially be measured). Note
    that measured amounts include amounts that are not precisely quantified,
    including amounts involving arbitrary units and floating currencies.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['value'] = """Numerical value (with implicit precision)."""
    _attribute_docstrings['comparator'] = """How the value should be understood and represented - whether the actual value is greater or less than the stated value due to measurement issues; e.g. if the comparator is "<" , then the real value is < stated value."""
    _attribute_docstrings['unit'] = """Unit representation."""
    _attribute_docstrings['system'] = """System that defines coded unit form."""
    _attribute_docstrings['code'] = """Coded form of the unit."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['comparator'] = {
        'url': 'http://hl7.org/fhir/quantity-comparator',
        'restricted_to': ['<', '<=', '>=', '>'],
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
        
        self.value = None
        """ Numerical value (with implicit precision).
        Type `float`. """
        
        self.comparator = None
        """ How the value should be understood and represented - whether the
        actual value is greater or less than the stated value due to
        measurement issues; e.g. if the comparator is "<" , then the real
        value is < stated value.
        Type `str`. """
        
        self.unit = None
        """ Unit representation.
        Type `str`. """
        
        self.system = None
        """ System that defines coded unit form.
        Type `str`. """
        
        self.code = None
        """ Coded form of the unit.
        Type `str`. """
        
        super(Quantity, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Quantity, self).elementProperties()
        js.extend([
            ("value", "value", float, False, None, False),
            ("comparator", "comparator", str, False, None, False),
            ("unit", "unit", str, False, None, False),
            ("system", "system", str, False, None, False),
            ("code", "code", str, False, None, False),
        ])
        return js


