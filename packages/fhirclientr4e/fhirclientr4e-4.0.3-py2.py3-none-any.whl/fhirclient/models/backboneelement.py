#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/BackboneElement) on 2022-06-21.
#  2022, SMART Health IT.


from . import element

class BackboneElement(element.Element):
    """ Base for elements defined inside a resource.
    
    Base definition for all elements that are defined inside a resource - but
    not those in a data type.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['modifierExtension'] = """Extensions that cannot be ignored even if unrecognized."""

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
        
        self.modifierExtension = None
        """ Extensions that cannot be ignored even if unrecognized.
        List of `Extension` items (represented as `dict` in JSON). """
        
        super(BackboneElement, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(BackboneElement, self).elementProperties()
        js.extend([
            ("modifierExtension", "modifierExtension", extension.Extension, True, None, False),
        ])
        return js


import sys
try:
    from . import extension
except ImportError:
    extension = sys.modules[__package__ + '.extension']
