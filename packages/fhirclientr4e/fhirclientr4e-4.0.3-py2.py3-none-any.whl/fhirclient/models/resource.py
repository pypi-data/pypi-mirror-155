#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Resource) on 2022-06-21.
#  2022, SMART Health IT.


from . import fhirabstractresource

class Resource(fhirabstractresource.FHIRAbstractResource):
    """ Base Resource.
    
    This is the base resource type for everything.
    """
    
    resource_type = "Resource"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['id'] = """Logical id of this artifact."""
    _attribute_docstrings['meta'] = """Metadata about the resource."""
    _attribute_docstrings['implicitRules'] = """A set of rules under which this content was created."""
    _attribute_docstrings['language'] = """Language of the resource content."""

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
        """ Logical id of this artifact.
        Type `str`. """
        
        self.meta = None
        """ Metadata about the resource.
        Type `Meta` (represented as `dict` in JSON). """
        
        self.implicitRules = None
        """ A set of rules under which this content was created.
        Type `str`. """
        
        self.language = None
        """ Language of the resource content.
        Type `str`. """
        
        super(Resource, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Resource, self).elementProperties()
        js.extend([
            ("id", "id", str, False, None, False),
            ("meta", "meta", meta.Meta, False, None, False),
            ("implicitRules", "implicitRules", str, False, None, False),
            ("language", "language", str, False, None, False),
        ])
        return js


import sys
try:
    from . import meta
except ImportError:
    meta = sys.modules[__package__ + '.meta']
