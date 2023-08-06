#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Narrative) on 2022-06-21.
#  2022, SMART Health IT.


from . import element

class Narrative(element.Element):
    """ Human-readable summary of the resource (essential clinical and business
    information).
    
    A human-readable summary of the resource conveying the essential clinical
    and business information for the resource.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['status'] = """The status of the narrative - whether it's entirely generated (from just the defined data or the extensions too), or whether a human authored it and it may contain additional data."""
    _attribute_docstrings['div'] = """Limited xhtml content."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/narrative-status',
        'restricted_to': ['generated', 'extensions', 'additional', 'empty'],
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
        
        self.status = None
        """ The status of the narrative - whether it's entirely generated (from
        just the defined data or the extensions too), or whether a human
        authored it and it may contain additional data.
        Type `str`. """
        
        self.div = None
        """ Limited xhtml content.
        Type `str`. """
        
        super(Narrative, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Narrative, self).elementProperties()
        js.extend([
            ("status", "status", str, False, None, True),
            ("div", "div", str, False, None, True),
        ])
        return js


