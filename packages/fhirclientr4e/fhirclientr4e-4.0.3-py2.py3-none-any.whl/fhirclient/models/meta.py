#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Meta) on 2022-06-21.
#  2022, SMART Health IT.


from . import element

class Meta(element.Element):
    """ Metadata about a resource.
    
    The metadata about a resource. This is content in the resource that is
    maintained by the infrastructure. Changes to the content might not always
    be associated with version changes to the resource.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['versionId'] = """Version specific identifier."""
    _attribute_docstrings['lastUpdated'] = """When the resource version last changed."""
    _attribute_docstrings['source'] = """Identifies where the resource comes from."""
    _attribute_docstrings['profile'] = """Profiles this resource claims to conform to."""
    _attribute_docstrings['security'] = """Security Labels applied to this resource."""
    _attribute_docstrings['tag'] = """Tags applied to this resource."""

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
        
        self.versionId = None
        """ Version specific identifier.
        Type `str`. """
        
        self.lastUpdated = None
        """ When the resource version last changed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.source = None
        """ Identifies where the resource comes from.
        Type `str`. """
        
        self.profile = None
        """ Profiles this resource claims to conform to.
        List of `str` items. """
        
        self.security = None
        """ Security Labels applied to this resource.
        List of `Coding` items (represented as `dict` in JSON). """
        
        self.tag = None
        """ Tags applied to this resource.
        List of `Coding` items (represented as `dict` in JSON). """
        
        super(Meta, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Meta, self).elementProperties()
        js.extend([
            ("versionId", "versionId", str, False, None, False),
            ("lastUpdated", "lastUpdated", fhirdate.FHIRDate, False, None, False),
            ("source", "source", str, False, None, False),
            ("profile", "profile", str, True, None, False),
            ("security", "security", coding.Coding, True, None, False),
            ("tag", "tag", coding.Coding, True, None, False),
        ])
        return js


import sys
try:
    from . import coding
except ImportError:
    coding = sys.modules[__package__ + '.coding']
try:
    from . import fhirdate
except ImportError:
    fhirdate = sys.modules[__package__ + '.fhirdate']
