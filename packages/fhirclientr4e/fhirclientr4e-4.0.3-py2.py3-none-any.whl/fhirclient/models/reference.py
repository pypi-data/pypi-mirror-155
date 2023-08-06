#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Reference) on 2022-06-21.
#  2022, SMART Health IT.


from . import element

class Reference(element.Element):
    """ A reference from one resource to another.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['reference'] = """Literal reference, Relative, internal or absolute URL."""
    _attribute_docstrings['type'] = """Type the reference refers to (e.g. "Patient")."""
    _attribute_docstrings['identifier'] = """Logical reference, when literal reference is not known."""
    _attribute_docstrings['display'] = """Text alternative for the resource."""

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
        
        self.reference = None
        """ Literal reference, Relative, internal or absolute URL.
        Type `str`. """
        
        self.type = None
        """ Type the reference refers to (e.g. "Patient").
        Type `str`. """
        
        self.identifier = None
        """ Logical reference, when literal reference is not known.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.display = None
        """ Text alternative for the resource.
        Type `str`. """
        
        super(Reference, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Reference, self).elementProperties()
        js.extend([
            ("reference", "reference", str, False, None, False),
            ("type", "type", str, False, None, False),
            ("identifier", "identifier", identifier.Identifier, False, None, False),
            ("display", "display", str, False, None, False),
        ])
        return js


import sys
try:
    from . import identifier
except ImportError:
    identifier = sys.modules[__package__ + '.identifier']
