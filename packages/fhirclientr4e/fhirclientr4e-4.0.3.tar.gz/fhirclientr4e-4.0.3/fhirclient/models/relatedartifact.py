#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/RelatedArtifact) on 2022-06-21.
#  2022, SMART Health IT.


from . import element

class RelatedArtifact(element.Element):
    """ Related artifacts for a knowledge resource.
    
    Related artifacts such as additional documentation, justification, or
    bibliographic references.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """The type of relationship to the related artifact."""
    _attribute_docstrings['label'] = """Short label."""
    _attribute_docstrings['display'] = """Brief description of the related artifact."""
    _attribute_docstrings['citation'] = """Bibliographic citation for the artifact."""
    _attribute_docstrings['url'] = """Where the artifact can be accessed."""
    _attribute_docstrings['document'] = """What document is being referenced."""
    _attribute_docstrings['resource'] = """What resource is being referenced."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://hl7.org/fhir/related-artifact-type',
        'restricted_to': ['documentation', 'justification', 'citation', 'predecessor', 'successor', 'derived-from', 'depends-on', 'composed-of'],
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
        """ The type of relationship to the related artifact.
        Type `str`. """
        
        self.label = None
        """ Short label.
        Type `str`. """
        
        self.display = None
        """ Brief description of the related artifact.
        Type `str`. """
        
        self.citation = None
        """ Bibliographic citation for the artifact.
        Type `str`. """
        
        self.url = None
        """ Where the artifact can be accessed.
        Type `str`. """
        
        self.document = None
        """ What document is being referenced.
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.resource = None
        """ What resource is being referenced.
        Type `str`. """
        
        super(RelatedArtifact, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(RelatedArtifact, self).elementProperties()
        js.extend([
            ("type", "type", str, False, None, True),
            ("label", "label", str, False, None, False),
            ("display", "display", str, False, None, False),
            ("citation", "citation", str, False, None, False),
            ("url", "url", str, False, None, False),
            ("document", "document", attachment.Attachment, False, None, False),
            ("resource", "resource", str, False, None, False),
        ])
        return js


import sys
try:
    from . import attachment
except ImportError:
    attachment = sys.modules[__package__ + '.attachment']
