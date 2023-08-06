#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Address) on 2022-06-21.
#  2022, SMART Health IT.


from . import element

class Address(element.Element):
    """ An address expressed using postal conventions (as opposed to GPS or other
    location definition formats).
    
    An address expressed using postal conventions (as opposed to GPS or other
    location definition formats).  This data type may be used to convey
    addresses for use in delivering mail as well as for visiting locations
    which might not be valid for mail delivery.  There are a variety of postal
    address formats defined around the world.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['use'] = """The purpose of this address."""
    _attribute_docstrings['type'] = """Distinguishes between physical addresses (those you can visit) and mailing addresses (e.g. PO Boxes and care-of addresses). Most addresses are both."""
    _attribute_docstrings['text'] = """Text representation of the address."""
    _attribute_docstrings['line'] = """Street name, number, direction & P.O. Box etc.."""
    _attribute_docstrings['city'] = """Name of city, town etc.."""
    _attribute_docstrings['district'] = """District name (aka county)."""
    _attribute_docstrings['state'] = """Sub-unit of country (abbreviations ok)."""
    _attribute_docstrings['postalCode'] = """Postal code for area."""
    _attribute_docstrings['country'] = """Country (e.g. can be ISO 3166 2 or 3 letter code)."""
    _attribute_docstrings['period'] = """Time period when address was/is in use."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['use'] = {
        'url': 'http://hl7.org/fhir/address-use',
        'restricted_to': ['home', 'work', 'temp', 'old', 'billing'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['type'] = {
        'url': 'http://hl7.org/fhir/address-type',
        'restricted_to': ['postal', 'physical', 'both'],
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
        
        self.use = None
        """ The purpose of this address.
        Type `str`. """
        
        self.type = None
        """ Distinguishes between physical addresses (those you can visit) and
        mailing addresses (e.g. PO Boxes and care-of addresses). Most
        addresses are both.
        Type `str`. """
        
        self.text = None
        """ Text representation of the address.
        Type `str`. """
        
        self.line = None
        """ Street name, number, direction & P.O. Box etc.
        List of `str` items. """
        
        self.city = None
        """ Name of city, town etc.
        Type `str`. """
        
        self.district = None
        """ District name (aka county).
        Type `str`. """
        
        self.state = None
        """ Sub-unit of country (abbreviations ok).
        Type `str`. """
        
        self.postalCode = None
        """ Postal code for area.
        Type `str`. """
        
        self.country = None
        """ Country (e.g. can be ISO 3166 2 or 3 letter code).
        Type `str`. """
        
        self.period = None
        """ Time period when address was/is in use.
        Type `Period` (represented as `dict` in JSON). """
        
        super(Address, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Address, self).elementProperties()
        js.extend([
            ("use", "use", str, False, None, False),
            ("type", "type", str, False, None, False),
            ("text", "text", str, False, None, False),
            ("line", "line", str, True, None, False),
            ("city", "city", str, False, None, False),
            ("district", "district", str, False, None, False),
            ("state", "state", str, False, None, False),
            ("postalCode", "postalCode", str, False, None, False),
            ("country", "country", str, False, None, False),
            ("period", "period", period.Period, False, None, False),
        ])
        return js


import sys
try:
    from . import period
except ImportError:
    period = sys.modules[__package__ + '.period']
