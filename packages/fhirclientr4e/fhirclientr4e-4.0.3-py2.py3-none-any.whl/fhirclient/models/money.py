#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Money) on 2022-06-21.
#  2022, SMART Health IT.


from . import element

class Money(element.Element):
    """ An amount of economic utility in some recognized currency.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['value'] = """Numerical value (with implicit precision)."""
    _attribute_docstrings['currency'] = """ISO 4217 Currency Code."""

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
        
        self.value = None
        """ Numerical value (with implicit precision).
        Type `float`. """
        
        self.currency = None
        """ ISO 4217 Currency Code.
        Type `str`. """
        
        super(Money, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Money, self).elementProperties()
        js.extend([
            ("value", "value", float, False, None, False),
            ("currency", "currency", str, False, None, False),
        ])
        return js


