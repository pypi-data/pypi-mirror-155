#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/DomainResource) on 2022-06-21.
#  2022, SMART Health IT.


from . import resource

class DomainResource(resource.Resource):
    """ A resource with narrative, extensions, and contained resources.
    
    A resource that includes narrative, extensions, and contained resources.
    """
    
    resource_type = "DomainResource"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['text'] = """Text summary of the resource, for human interpretation."""
    _attribute_docstrings['contained'] = """Contained, inline Resources."""
    _attribute_docstrings['extension'] = """Additional content defined by implementations."""
    _attribute_docstrings['modifierExtension'] = """Extensions that cannot be ignored."""

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
        
        self.text = None
        """ Text summary of the resource, for human interpretation.
        Type `Narrative` (represented as `dict` in JSON). """
        
        self.contained = None
        """ Contained, inline Resources.
        List of `Resource` items (represented as `dict` in JSON). """
        
        self.extension = None
        """ Additional content defined by implementations.
        List of `Extension` items (represented as `dict` in JSON). """
        
        self.modifierExtension = None
        """ Extensions that cannot be ignored.
        List of `Extension` items (represented as `dict` in JSON). """
        
        super(DomainResource, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DomainResource, self).elementProperties()
        js.extend([
            ("text", "text", narrative.Narrative, False, None, False),
            ("contained", "contained", resource.Resource, True, None, False),
            ("extension", "extension", extension.Extension, True, None, False),
            ("modifierExtension", "modifierExtension", extension.Extension, True, None, False),
        ])
        return js


import sys
try:
    from . import extension
except ImportError:
    extension = sys.modules[__package__ + '.extension']
try:
    from . import narrative
except ImportError:
    narrative = sys.modules[__package__ + '.narrative']
