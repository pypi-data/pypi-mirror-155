#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Evidence) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Evidence(domainresource.DomainResource):
    """ A research context or question.
    
    The Evidence resource describes the conditional state (population and any
    exposures being compared within the population) and outcome (if specified)
    that the knowledge (evidence, assertion, recommendation) is about.
    """
    
    resource_type = "Evidence"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['url'] = """Canonical identifier for this evidence, represented as a URI (globally unique)."""
    _attribute_docstrings['identifier'] = """Additional identifier for the evidence."""
    _attribute_docstrings['version'] = """Business version of the evidence."""
    _attribute_docstrings['name'] = """Name for this evidence (computer friendly)."""
    _attribute_docstrings['title'] = """Name for this evidence (human friendly)."""
    _attribute_docstrings['shortTitle'] = """Title for use in informal contexts."""
    _attribute_docstrings['subtitle'] = """Subordinate title of the Evidence."""
    _attribute_docstrings['status'] = """The status of this evidence. Enables tracking the life-cycle of the content."""
    _attribute_docstrings['date'] = """Date last changed."""
    _attribute_docstrings['publisher'] = """Name of the publisher (organization or individual)."""
    _attribute_docstrings['contact'] = """Contact details for the publisher."""
    _attribute_docstrings['description'] = """Natural language description of the evidence."""
    _attribute_docstrings['note'] = """Used for footnotes or explanatory notes."""
    _attribute_docstrings['useContext'] = """The context that the content is intended to support."""
    _attribute_docstrings['jurisdiction'] = """Intended jurisdiction for evidence (if applicable)."""
    _attribute_docstrings['copyright'] = """Use and/or publishing restrictions."""
    _attribute_docstrings['approvalDate'] = """When the evidence was approved by publisher."""
    _attribute_docstrings['lastReviewDate'] = """When the evidence was last reviewed."""
    _attribute_docstrings['effectivePeriod'] = """When the evidence is expected to be used."""
    _attribute_docstrings['topic'] = """Descriptive topics related to the content of the Evidence. Topics provide a high-level categorization grouping types of Evidences that can be useful for filtering and searching."""
    _attribute_docstrings['author'] = """Who authored the content."""
    _attribute_docstrings['editor'] = """Who edited the content."""
    _attribute_docstrings['reviewer'] = """Who reviewed the content."""
    _attribute_docstrings['endorser'] = """Who endorsed the content."""
    _attribute_docstrings['relatedArtifact'] = """Additional documentation, citations, etc.."""
    _attribute_docstrings['exposureBackground'] = """What population?."""
    _attribute_docstrings['exposureVariant'] = """What exposure?."""
    _attribute_docstrings['outcome'] = """What outcome?."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/publication-status',
        'restricted_to': ['draft', 'active', 'retired', 'unknown'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['topic'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/definition-topic',
        'restricted_to': ['treatment', 'education', 'assessment'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
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
        
        self.url = None
        """ Canonical identifier for this evidence, represented as a URI
        (globally unique).
        Type `str`. """
        
        self.identifier = None
        """ Additional identifier for the evidence.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.version = None
        """ Business version of the evidence.
        Type `str`. """
        
        self.name = None
        """ Name for this evidence (computer friendly).
        Type `str`. """
        
        self.title = None
        """ Name for this evidence (human friendly).
        Type `str`. """
        
        self.shortTitle = None
        """ Title for use in informal contexts.
        Type `str`. """
        
        self.subtitle = None
        """ Subordinate title of the Evidence.
        Type `str`. """
        
        self.status = None
        """ The status of this evidence. Enables tracking the life-cycle of the
        content.
        Type `str`. """
        
        self.date = None
        """ Date last changed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.publisher = None
        """ Name of the publisher (organization or individual).
        Type `str`. """
        
        self.contact = None
        """ Contact details for the publisher.
        List of `ContactDetail` items (represented as `dict` in JSON). """
        
        self.description = None
        """ Natural language description of the evidence.
        Type `str`. """
        
        self.note = None
        """ Used for footnotes or explanatory notes.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for evidence (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.copyright = None
        """ Use and/or publishing restrictions.
        Type `str`. """
        
        self.approvalDate = None
        """ When the evidence was approved by publisher.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.lastReviewDate = None
        """ When the evidence was last reviewed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.effectivePeriod = None
        """ When the evidence is expected to be used.
        Type `Period` (represented as `dict` in JSON). """
        
        self.topic = None
        """ Descriptive topics related to the content of the Evidence. Topics
        provide a high-level categorization grouping types of Evidences
        that can be useful for filtering and searching.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.author = None
        """ Who authored the content.
        List of `ContactDetail` items (represented as `dict` in JSON). """
        
        self.editor = None
        """ Who edited the content.
        List of `ContactDetail` items (represented as `dict` in JSON). """
        
        self.reviewer = None
        """ Who reviewed the content.
        List of `ContactDetail` items (represented as `dict` in JSON). """
        
        self.endorser = None
        """ Who endorsed the content.
        List of `ContactDetail` items (represented as `dict` in JSON). """
        
        self.relatedArtifact = None
        """ Additional documentation, citations, etc.
        List of `RelatedArtifact` items (represented as `dict` in JSON). """
        
        self.exposureBackground = None
        """ What population?.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.exposureVariant = None
        """ What exposure?.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.outcome = None
        """ What outcome?.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(Evidence, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Evidence, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("version", "version", str, False, None, False),
            ("name", "name", str, False, None, False),
            ("title", "title", str, False, None, False),
            ("shortTitle", "shortTitle", str, False, None, False),
            ("subtitle", "subtitle", str, False, None, False),
            ("status", "status", str, False, None, True),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("publisher", "publisher", str, False, None, False),
            ("contact", "contact", contactdetail.ContactDetail, True, None, False),
            ("description", "description", str, False, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
            ("useContext", "useContext", usagecontext.UsageContext, True, None, False),
            ("jurisdiction", "jurisdiction", codeableconcept.CodeableConcept, True, None, False),
            ("copyright", "copyright", str, False, None, False),
            ("approvalDate", "approvalDate", fhirdate.FHIRDate, False, None, False),
            ("lastReviewDate", "lastReviewDate", fhirdate.FHIRDate, False, None, False),
            ("effectivePeriod", "effectivePeriod", period.Period, False, None, False),
            ("topic", "topic", codeableconcept.CodeableConcept, True, None, False),
            ("author", "author", contactdetail.ContactDetail, True, None, False),
            ("editor", "editor", contactdetail.ContactDetail, True, None, False),
            ("reviewer", "reviewer", contactdetail.ContactDetail, True, None, False),
            ("endorser", "endorser", contactdetail.ContactDetail, True, None, False),
            ("relatedArtifact", "relatedArtifact", relatedartifact.RelatedArtifact, True, None, False),
            ("exposureBackground", "exposureBackground", fhirreference.FHIRReference, False, None, True),
            ("exposureVariant", "exposureVariant", fhirreference.FHIRReference, True, None, False),
            ("outcome", "outcome", fhirreference.FHIRReference, True, None, False),
        ])
        return js


import sys
try:
    from . import annotation
except ImportError:
    annotation = sys.modules[__package__ + '.annotation']
try:
    from . import codeableconcept
except ImportError:
    codeableconcept = sys.modules[__package__ + '.codeableconcept']
try:
    from . import contactdetail
except ImportError:
    contactdetail = sys.modules[__package__ + '.contactdetail']
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
try:
    from . import period
except ImportError:
    period = sys.modules[__package__ + '.period']
try:
    from . import relatedartifact
except ImportError:
    relatedartifact = sys.modules[__package__ + '.relatedartifact']
try:
    from . import usagecontext
except ImportError:
    usagecontext = sys.modules[__package__ + '.usagecontext']
