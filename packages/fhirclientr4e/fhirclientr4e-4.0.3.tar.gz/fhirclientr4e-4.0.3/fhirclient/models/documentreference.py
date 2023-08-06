#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/DocumentReference) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class DocumentReference(domainresource.DomainResource):
    """ A reference to a document.
    
    A reference to a document of any kind for any purpose. Provides metadata
    about the document so that the document can be discovered and managed. The
    scope of a document is any seralized object with a mime-type, so includes
    formal patient centric documents (CDA), cliical notes, scanned paper, and
    non-patient specific documents like policy text.
    """
    
    resource_type = "DocumentReference"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['masterIdentifier'] = """Master Version Specific Identifier."""
    _attribute_docstrings['identifier'] = """Other identifiers for the document."""
    _attribute_docstrings['status'] = """The status of this document reference."""
    _attribute_docstrings['docStatus'] = """The status of the underlying document."""
    _attribute_docstrings['type'] = """Kind of document (LOINC if possible)."""
    _attribute_docstrings['category'] = """Categorization of document."""
    _attribute_docstrings['subject'] = """Who/what is the subject of the document."""
    _attribute_docstrings['date'] = """When this document reference was created."""
    _attribute_docstrings['author'] = """Who and/or what authored the document."""
    _attribute_docstrings['authenticator'] = """Who/what authenticated the document."""
    _attribute_docstrings['custodian'] = """Organization which maintains the document."""
    _attribute_docstrings['relatesTo'] = """Relationships to other documents."""
    _attribute_docstrings['description'] = """Human-readable description."""
    _attribute_docstrings['securityLabel'] = """Document security-tags."""
    _attribute_docstrings['content'] = """Document referenced."""
    _attribute_docstrings['context'] = """Clinical context of document."""

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
    _attribute_enums['docStatus'] = {
        'url': 'http://hl7.org/fhir/composition-status',
        'restricted_to': ['preliminary', 'final', 'amended', 'entered-in-error'],
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
        """ Master Version Specific Identifier.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.identifier = None
        """ Other identifiers for the document.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ The status of this document reference.
        Type `str`. """
        
        self.docStatus = None
        """ The status of the underlying document.
        Type `str`. """
        
        self.type = None
        """ Kind of document (LOINC if possible).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.category = None
        """ Categorization of document.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.subject = None
        """ Who/what is the subject of the document.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.date = None
        """ When this document reference was created.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.author = None
        """ Who and/or what authored the document.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.authenticator = None
        """ Who/what authenticated the document.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.custodian = None
        """ Organization which maintains the document.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.relatesTo = None
        """ Relationships to other documents.
        List of `DocumentReferenceRelatesTo` items (represented as `dict` in JSON). """
        
        self.description = None
        """ Human-readable description.
        Type `str`. """
        
        self.securityLabel = None
        """ Document security-tags.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.content = None
        """ Document referenced.
        List of `DocumentReferenceContent` items (represented as `dict` in JSON). """
        
        self.context = None
        """ Clinical context of document.
        Type `DocumentReferenceContext` (represented as `dict` in JSON). """
        
        super(DocumentReference, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DocumentReference, self).elementProperties()
        js.extend([
            ("masterIdentifier", "masterIdentifier", identifier.Identifier, False, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("docStatus", "docStatus", str, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("category", "category", codeableconcept.CodeableConcept, True, None, False),
            ("subject", "subject", fhirreference.FHIRReference, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("author", "author", fhirreference.FHIRReference, True, None, False),
            ("authenticator", "authenticator", fhirreference.FHIRReference, False, None, False),
            ("custodian", "custodian", fhirreference.FHIRReference, False, None, False),
            ("relatesTo", "relatesTo", DocumentReferenceRelatesTo, True, None, False),
            ("description", "description", str, False, None, False),
            ("securityLabel", "securityLabel", codeableconcept.CodeableConcept, True, None, False),
            ("content", "content", DocumentReferenceContent, True, None, True),
            ("context", "context", DocumentReferenceContext, False, None, False),
        ])
        return js


from . import backboneelement

class DocumentReferenceContent(backboneelement.BackboneElement):
    """ Document referenced.
    
    The document and format referenced. There may be multiple content element
    repetitions, each with a different format.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['attachment'] = """Where to access the document."""
    _attribute_docstrings['format'] = """Format/content rules for the document."""

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
        
        self.attachment = None
        """ Where to access the document.
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.format = None
        """ Format/content rules for the document.
        Type `Coding` (represented as `dict` in JSON). """
        
        super(DocumentReferenceContent, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DocumentReferenceContent, self).elementProperties()
        js.extend([
            ("attachment", "attachment", attachment.Attachment, False, None, True),
            ("format", "format", coding.Coding, False, None, False),
        ])
        return js


class DocumentReferenceContext(backboneelement.BackboneElement):
    """ Clinical context of document.
    
    The clinical context in which the document was prepared.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['encounter'] = """Context of the document  content."""
    _attribute_docstrings['event'] = """Main clinical acts documented."""
    _attribute_docstrings['period'] = """Time of service that is being documented."""
    _attribute_docstrings['facilityType'] = """Kind of facility where patient was seen."""
    _attribute_docstrings['practiceSetting'] = """Additional details about where the content was created (e.g. clinical specialty)."""
    _attribute_docstrings['sourcePatientInfo'] = """Patient demographics from source."""
    _attribute_docstrings['related'] = """Related identifiers or resources."""

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
        
        self.encounter = None
        """ Context of the document  content.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.event = None
        """ Main clinical acts documented.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.period = None
        """ Time of service that is being documented.
        Type `Period` (represented as `dict` in JSON). """
        
        self.facilityType = None
        """ Kind of facility where patient was seen.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.practiceSetting = None
        """ Additional details about where the content was created (e.g.
        clinical specialty).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.sourcePatientInfo = None
        """ Patient demographics from source.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.related = None
        """ Related identifiers or resources.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(DocumentReferenceContext, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DocumentReferenceContext, self).elementProperties()
        js.extend([
            ("encounter", "encounter", fhirreference.FHIRReference, True, None, False),
            ("event", "event", codeableconcept.CodeableConcept, True, None, False),
            ("period", "period", period.Period, False, None, False),
            ("facilityType", "facilityType", codeableconcept.CodeableConcept, False, None, False),
            ("practiceSetting", "practiceSetting", codeableconcept.CodeableConcept, False, None, False),
            ("sourcePatientInfo", "sourcePatientInfo", fhirreference.FHIRReference, False, None, False),
            ("related", "related", fhirreference.FHIRReference, True, None, False),
        ])
        return js


class DocumentReferenceRelatesTo(backboneelement.BackboneElement):
    """ Relationships to other documents.
    
    Relationships that this document has with other document references that
    already exist.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """The type of relationship that this document has with anther document."""
    _attribute_docstrings['target'] = """Target of the relationship."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['code'] = {
        'url': 'http://hl7.org/fhir/document-relationship-type',
        'restricted_to': ['replaces', 'transforms', 'signs', 'appends'],
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
        
        self.code = None
        """ The type of relationship that this document has with anther
        document.
        Type `str`. """
        
        self.target = None
        """ Target of the relationship.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(DocumentReferenceRelatesTo, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DocumentReferenceRelatesTo, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, True),
            ("target", "target", fhirreference.FHIRReference, False, None, True),
        ])
        return js


import sys
try:
    from . import attachment
except ImportError:
    attachment = sys.modules[__package__ + '.attachment']
try:
    from . import codeableconcept
except ImportError:
    codeableconcept = sys.modules[__package__ + '.codeableconcept']
try:
    from . import coding
except ImportError:
    coding = sys.modules[__package__ + '.coding']
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
