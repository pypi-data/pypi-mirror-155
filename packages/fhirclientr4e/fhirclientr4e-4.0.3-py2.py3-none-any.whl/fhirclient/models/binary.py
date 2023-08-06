#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Binary) on 2022-06-21.
#  2022, SMART Health IT.


from . import resource

class Binary(resource.Resource):
    """ Pure binary content defined by a format other than FHIR.
    
    A resource that represents the data of a single raw artifact as digital
    content accessible in its native format.  A Binary resource can contain any
    content, whether text, image, pdf, zip archive, etc.
    """
    
    resource_type = "Binary"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['contentType'] = """MimeType of the binary content."""
    _attribute_docstrings['securityContext'] = """Identifies another resource to use as proxy when enforcing access control."""
    _attribute_docstrings['data'] = """The actual content."""

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
        
        self.contentType = None
        """ MimeType of the binary content.
        Type `str`. """
        
        self.securityContext = None
        """ Identifies another resource to use as proxy when enforcing access
        control.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.data = None
        """ The actual content.
        Type `str`. """
        
        super(Binary, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Binary, self).elementProperties()
        js.extend([
            ("contentType", "contentType", str, False, None, True),
            ("securityContext", "securityContext", fhirreference.FHIRReference, False, None, False),
            ("data", "data", str, False, None, False),
        ])
        return js


import sys
try:
    from . import fhirreference
except ImportError:
    fhirreference = sys.modules[__package__ + '.fhirreference']
