#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Contributor) on 2022-06-21.
#  2022, SMART Health IT.


from . import element

class Contributor(element.Element):
    """ Contributor information.
    
    A contributor to the content of a knowledge asset, including authors,
    editors, reviewers, and endorsers.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """The type of contributor."""
    _attribute_docstrings['name'] = """Who contributed the content."""
    _attribute_docstrings['contact'] = """Contact details of the contributor."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://hl7.org/fhir/contributor-type',
        'restricted_to': ['author', 'editor', 'reviewer', 'endorser'],
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
        
        self.type = None
        """ The type of contributor.
        Type `str`. """
        
        self.name = None
        """ Who contributed the content.
        Type `str`. """
        
        self.contact = None
        """ Contact details of the contributor.
        List of `ContactDetail` items (represented as `dict` in JSON). """
        
        super(Contributor, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Contributor, self).elementProperties()
        js.extend([
            ("type", "type", str, False, None, True),
            ("name", "name", str, False, None, True),
            ("contact", "contact", contactdetail.ContactDetail, True, None, False),
        ])
        return js


import sys
try:
    from . import contactdetail
except ImportError:
    contactdetail = sys.modules[__package__ + '.contactdetail']
