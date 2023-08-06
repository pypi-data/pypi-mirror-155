#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/DocumentManifest) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class DocumentManifest(domainresource.DomainResource):
    """ A list that defines a set of documents.
    
    A collection of documents compiled for a purpose together with metadata
    that applies to the collection.
    """
    
    resource_type = "DocumentManifest"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['masterIdentifier'] = """Unique Identifier for the set of documents."""
    _attribute_docstrings['identifier'] = """Other identifiers for the manifest."""
    _attribute_docstrings['status'] = """The status of this document manifest."""
    _attribute_docstrings['type'] = """Kind of document set."""
    _attribute_docstrings['subject'] = """The subject of the set of documents."""
    _attribute_docstrings['created'] = """When this document manifest created."""
    _attribute_docstrings['author'] = """Who and/or what authored the DocumentManifest."""
    _attribute_docstrings['recipient'] = """Intended to get notified about this set of documents."""
    _attribute_docstrings['source'] = """The source system/application/software."""
    _attribute_docstrings['description'] = """Human-readable description (title)."""
    _attribute_docstrings['content'] = """Items in manifest."""
    _attribute_docstrings['related'] = """Related things."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/document-reference-status',
        'restricted_to': ['current', 'superseded', 'entered-in-error'],
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
        
        self.masterIdentifier = None
        """ Unique Identifier for the set of documents.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.identifier = None
        """ Other identifiers for the manifest.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ The status of this document manifest.
        Type `str`. """
        
        self.type = None
        """ Kind of document set.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subject = None
        """ The subject of the set of documents.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.created = None
        """ When this document manifest created.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.author = None
        """ Who and/or what authored the DocumentManifest.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.recipient = None
        """ Intended to get notified about this set of documents.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.source = None
        """ The source system/application/software.
        Type `str`. """
        
        self.description = None
        """ Human-readable description (title).
        Type `str`. """
        
        self.content = None
        """ Items in manifest.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.related = None
        """ Related things.
        List of `DocumentManifestRelated` items (represented as `dict` in JSON). """
        
        super(DocumentManifest, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DocumentManifest, self).elementProperties()
        js.extend([
            ("masterIdentifier", "masterIdentifier", identifier.Identifier, False, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("subject", "subject", fhirreference.FHIRReference, False, None, False),
            ("created", "created", fhirdate.FHIRDate, False, None, False),
            ("author", "author", fhirreference.FHIRReference, True, None, False),
            ("recipient", "recipient", fhirreference.FHIRReference, True, None, False),
            ("source", "source", str, False, None, False),
            ("description", "description", str, False, None, False),
            ("content", "content", fhirreference.FHIRReference, True, None, True),
            ("related", "related", DocumentManifestRelated, True, None, False),
        ])
        return js


from . import backboneelement

class DocumentManifestRelated(backboneelement.BackboneElement):
    """ Related things.
    
    Related identifiers or resources associated with the DocumentManifest.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Identifiers of things that are related."""
    _attribute_docstrings['ref'] = """Related Resource."""

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
        
        self.identifier = None
        """ Identifiers of things that are related.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.ref = None
        """ Related Resource.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(DocumentManifestRelated, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DocumentManifestRelated, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, False, None, False),
            ("ref", "ref", fhirreference.FHIRReference, False, None, False),
        ])
        return js


import sys
try:
    from . import codeableconcept
except ImportError:
    codeableconcept = sys.modules[__package__ + '.codeableconcept']
try:
    from . import fhirdate
except ImportError:
    fhirdate = sys.modules[__package__ + '.fhirdate']
try:
    from . import fhirreference
except ImportError:
    fhirreference = sys.modules[__package__ + '.fhirreference']
try:
    from . import identifier
except ImportError:
    identifier = sys.modules[__package__ + '.identifier']
