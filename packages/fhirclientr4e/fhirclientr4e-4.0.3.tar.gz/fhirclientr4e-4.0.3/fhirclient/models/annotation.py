#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Annotation) on 2022-06-21.
#  2022, SMART Health IT.


from . import element

class Annotation(element.Element):
    """ Text node with attribution.
    
    A  text note which also  contains information about who made the statement
    and when.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['authorReference'] = """Individual responsible for the annotation."""
    _attribute_docstrings['authorString'] = """Individual responsible for the annotation."""
    _attribute_docstrings['time'] = """When the annotation was made."""
    _attribute_docstrings['text'] = """The annotation  - text content (as markdown)."""

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
        
        self.authorReference = None
        """ Individual responsible for the annotation.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.authorString = None
        """ Individual responsible for the annotation.
        Type `str`. """
        
        self.time = None
        """ When the annotation was made.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.text = None
        """ The annotation  - text content (as markdown).
        Type `str`. """
        
        super(Annotation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Annotation, self).elementProperties()
        js.extend([
            ("authorReference", "authorReference", fhirreference.FHIRReference, False, "author", False),
            ("authorString", "authorString", str, False, "author", False),
            ("time", "time", fhirdate.FHIRDate, False, None, False),
            ("text", "text", str, False, None, True),
        ])
        return js


import sys
try:
    from . import fhirdate
except ImportError:
    fhirdate = sys.modules[__package__ + '.fhirdate']
try:
    from . import fhirreference
except ImportError:
    fhirreference = sys.modules[__package__ + '.fhirreference']
