#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/ContactPoint) on 2022-06-21.
#  2022, SMART Health IT.


from . import element

class ContactPoint(element.Element):
    """ Details of a Technology mediated contact point (phone, fax, email, etc.).
    
    Details for all kinds of technology mediated contact points for a person or
    organization, including telephone, email, etc.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['system'] = """Telecommunications form for contact point - what communications system is required to make use of the contact."""
    _attribute_docstrings['value'] = """The actual contact point details."""
    _attribute_docstrings['use'] = """Identifies the purpose for the contact point."""
    _attribute_docstrings['rank'] = """Specify preferred order of use (1 = highest)."""
    _attribute_docstrings['period'] = """Time period when the contact point was/is in use."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['system'] = {
        'url': 'http://hl7.org/fhir/contact-point-system',
        'restricted_to': ['phone', 'fax', 'email', 'pager', 'url', 'sms', 'other'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['use'] = {
        'url': 'http://hl7.org/fhir/contact-point-use',
        'restricted_to': ['home', 'work', 'temp', 'old', 'mobile'],
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
        
        self.system = None
        """ Telecommunications form for contact point - what communications
        system is required to make use of the contact.
        Type `str`. """
        
        self.value = None
        """ The actual contact point details.
        Type `str`. """
        
        self.use = None
        """ Identifies the purpose for the contact point.
        Type `str`. """
        
        self.rank = None
        """ Specify preferred order of use (1 = highest).
        Type `int`. """
        
        self.period = None
        """ Time period when the contact point was/is in use.
        Type `Period` (represented as `dict` in JSON). """
        
        super(ContactPoint, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ContactPoint, self).elementProperties()
        js.extend([
            ("system", "system", str, False, None, False),
            ("value", "value", str, False, None, False),
            ("use", "use", str, False, None, False),
            ("rank", "rank", int, False, None, False),
            ("period", "period", period.Period, False, None, False),
        ])
        return js


import sys
try:
    from . import period
except ImportError:
    period = sys.modules[__package__ + '.period']
