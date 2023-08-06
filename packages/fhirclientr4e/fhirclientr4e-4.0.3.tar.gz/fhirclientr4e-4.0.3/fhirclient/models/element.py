#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Element) on 2022-06-21.
#  2022, SMART Health IT.


from . import fhirabstractbase

class Element(fhirabstractbase.FHIRAbstractBase):
    """ Base for all elements.
    
    Base definition for all elements in a resource.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['id'] = """Unique id for inter-element referencing."""
    _attribute_docstrings['extension'] = """Additional content defined by implementations."""

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
        
        self.id = None
        """ Unique id for inter-element referencing.
        Type `str`. """
        
        self.extension = None
        """ Additional content defined by implementations.
        List of `Extension` items (represented as `dict` in JSON). """
        
        super(Element, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Element, self).elementProperties()
        from . import extension
        js.extend([
            ("id", "id", str, False, None, False),
            ("extension", "extension", extension.Extension, True, None, False),
        ])
        return js


