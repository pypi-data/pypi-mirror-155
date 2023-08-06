#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Composition) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Composition(domainresource.DomainResource):
    """ A set of resources composed into a single coherent clinical statement with
    clinical attestation.
    
    A set of healthcare-related information that is assembled together into a
    single logical package that provides a single coherent statement of
    meaning, establishes its own context and that has clinical attestation with
    regard to who is making the statement. A Composition defines the structure
    and narrative content necessary for a document. However, a Composition
    alone does not constitute a document. Rather, the Composition must be the
    first entry in a Bundle where Bundle.type=document, and any other resources
    referenced from Composition must be included as subsequent entries in the
    Bundle (for example Patient, Practitioner, Encounter, etc.).
    """
    
    resource_type = "Composition"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Version-independent identifier for the Composition."""
    _attribute_docstrings['status'] = """The workflow/clinical status of this composition. The status is a marker for the clinical standing of the document."""
    _attribute_docstrings['type'] = """Kind of composition (LOINC if possible)."""
    _attribute_docstrings['category'] = """Categorization of Composition."""
    _attribute_docstrings['subject'] = """Who and/or what the composition is about."""
    _attribute_docstrings['encounter'] = """Context of the Composition."""
    _attribute_docstrings['date'] = """Composition editing time."""
    _attribute_docstrings['author'] = """Who and/or what authored the composition."""
    _attribute_docstrings['title'] = """Human Readable name/title."""
    _attribute_docstrings['confidentiality'] = """As defined by affinity domain."""
    _attribute_docstrings['attester'] = """Attests to accuracy of composition."""
    _attribute_docstrings['custodian'] = """Organization which maintains the composition."""
    _attribute_docstrings['relatesTo'] = """Relationships to other compositions/documents."""
    _attribute_docstrings['event'] = """The clinical service(s) being documented."""
    _attribute_docstrings['section'] = """Composition is broken into sections."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
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
        
        self.identifier = None
        """ Version-independent identifier for the Composition.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.status = None
        """ The workflow/clinical status of this composition. The status is a
        marker for the clinical standing of the document.
        Type `str`. """
        
        self.type = None
        """ Kind of composition (LOINC if possible).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.category = None
        """ Categorization of Composition.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.subject = None
        """ Who and/or what the composition is about.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Context of the Composition.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.date = None
        """ Composition editing time.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.author = None
        """ Who and/or what authored the composition.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.title = None
        """ Human Readable name/title.
        Type `str`. """
        
        self.confidentiality = None
        """ As defined by affinity domain.
        Type `str`. """
        
        self.attester = None
        """ Attests to accuracy of composition.
        List of `CompositionAttester` items (represented as `dict` in JSON). """
        
        self.custodian = None
        """ Organization which maintains the composition.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.relatesTo = None
        """ Relationships to other compositions/documents.
        List of `CompositionRelatesTo` items (represented as `dict` in JSON). """
        
        self.event = None
        """ The clinical service(s) being documented.
        List of `CompositionEvent` items (represented as `dict` in JSON). """
        
        self.section = None
        """ Composition is broken into sections.
        List of `CompositionSection` items (represented as `dict` in JSON). """
        
        super(Composition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Composition, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, False, None, False),
            ("status", "status", str, False, None, True),
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("category", "category", codeableconcept.CodeableConcept, True, None, False),
            ("subject", "subject", fhirreference.FHIRReference, False, None, False),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, True),
            ("author", "author", fhirreference.FHIRReference, True, None, True),
            ("title", "title", str, False, None, True),
            ("confidentiality", "confidentiality", str, False, None, False),
            ("attester", "attester", CompositionAttester, True, None, False),
            ("custodian", "custodian", fhirreference.FHIRReference, False, None, False),
            ("relatesTo", "relatesTo", CompositionRelatesTo, True, None, False),
            ("event", "event", CompositionEvent, True, None, False),
            ("section", "section", CompositionSection, True, None, False),
        ])
        return js


from . import backboneelement

class CompositionAttester(backboneelement.BackboneElement):
    """ Attests to accuracy of composition.
    
    A participant who has attested to the accuracy of the composition/document.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['mode'] = """The type of attestation the authenticator offers."""
    _attribute_docstrings['time'] = """When the composition was attested."""
    _attribute_docstrings['party'] = """Who attested the composition."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['mode'] = {
        'url': 'http://hl7.org/fhir/composition-attestation-mode',
        'restricted_to': ['personal', 'professional', 'legal', 'official'],
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
        
        self.mode = None
        """ The type of attestation the authenticator offers.
        Type `str`. """
        
        self.time = None
        """ When the composition was attested.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.party = None
        """ Who attested the composition.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(CompositionAttester, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CompositionAttester, self).elementProperties()
        js.extend([
            ("mode", "mode", str, False, None, True),
            ("time", "time", fhirdate.FHIRDate, False, None, False),
            ("party", "party", fhirreference.FHIRReference, False, None, False),
        ])
        return js


class CompositionEvent(backboneelement.BackboneElement):
    """ The clinical service(s) being documented.
    
    The clinical service, such as a colonoscopy or an appendectomy, being
    documented.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Code(s) that apply to the event being documented."""
    _attribute_docstrings['period'] = """The period covered by the documentation."""
    _attribute_docstrings['detail'] = """The event(s) being documented."""

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
        
        self.code = None
        """ Code(s) that apply to the event being documented.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.period = None
        """ The period covered by the documentation.
        Type `Period` (represented as `dict` in JSON). """
        
        self.detail = None
        """ The event(s) being documented.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(CompositionEvent, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CompositionEvent, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, True, None, False),
            ("period", "period", period.Period, False, None, False),
            ("detail", "detail", fhirreference.FHIRReference, True, None, False),
        ])
        return js


class CompositionRelatesTo(backboneelement.BackboneElement):
    """ Relationships to other compositions/documents.
    
    Relationships that this composition has with other compositions or
    documents that already exist.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """The type of relationship that this composition has with anther composition or document."""
    _attribute_docstrings['targetIdentifier'] = """Target of the relationship."""
    _attribute_docstrings['targetReference'] = """Target of the relationship."""

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
        """ The type of relationship that this composition has with anther
        composition or document.
        Type `str`. """
        
        self.targetIdentifier = None
        """ Target of the relationship.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.targetReference = None
        """ Target of the relationship.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(CompositionRelatesTo, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CompositionRelatesTo, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, True),
            ("targetIdentifier", "targetIdentifier", identifier.Identifier, False, "target", True),
            ("targetReference", "targetReference", fhirreference.FHIRReference, False, "target", True),
        ])
        return js


class CompositionSection(backboneelement.BackboneElement):
    """ Composition is broken into sections.
    
    The root of the sections that make up the composition.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['title'] = """Label for section (e.g. for ToC)."""
    _attribute_docstrings['code'] = """Classification of section (recommended)."""
    _attribute_docstrings['author'] = """Who and/or what authored the section."""
    _attribute_docstrings['focus'] = """Who/what the section is about, when it is not about the subject of composition."""
    _attribute_docstrings['text'] = """Text summary of the section, for human interpretation."""
    _attribute_docstrings['mode'] = """How the entry list was prepared - whether it is a working list that is suitable for being maintained on an ongoing basis, or if it represents a snapshot of a list of items from another source, or whether it is a prepared list where items may be marked as added, modified or deleted."""
    _attribute_docstrings['orderedBy'] = """Specifies the order applied to the items in the section entries."""
    _attribute_docstrings['entry'] = """A reference to data that supports this section."""
    _attribute_docstrings['emptyReason'] = """If the section is empty, why the list is empty. An empty section typically has some text explaining the empty reason."""
    _attribute_docstrings['section'] = """Nested Section."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['mode'] = {
        'url': 'http://hl7.org/fhir/list-mode',
        'restricted_to': ['working', 'snapshot', 'changes'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['orderedBy'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/list-order',
        'restricted_to': ['user', 'system', 'event-date', 'entry-date', 'priority', 'alphabetic', 'category', 'patient'],
        'binding_strength': 'preferred',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['emptyReason'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/list-empty-reason',
        'restricted_to': ['nilknown', 'notasked', 'withheld', 'unavailable', 'notstarted', 'closed'],
        'binding_strength': 'preferred',
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
        
        self.title = None
        """ Label for section (e.g. for ToC).
        Type `str`. """
        
        self.code = None
        """ Classification of section (recommended).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.author = None
        """ Who and/or what authored the section.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.focus = None
        """ Who/what the section is about, when it is not about the subject of
        composition.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.text = None
        """ Text summary of the section, for human interpretation.
        Type `Narrative` (represented as `dict` in JSON). """
        
        self.mode = None
        """ How the entry list was prepared - whether it is a working list that
        is suitable for being maintained on an ongoing basis, or if it
        represents a snapshot of a list of items from another source, or
        whether it is a prepared list where items may be marked as added,
        modified or deleted.
        Type `str`. """
        
        self.orderedBy = None
        """ Specifies the order applied to the items in the section entries.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.entry = None
        """ A reference to data that supports this section.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.emptyReason = None
        """ If the section is empty, why the list is empty. An empty section
        typically has some text explaining the empty reason.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.section = None
        """ Nested Section.
        List of `CompositionSection` items (represented as `dict` in JSON). """
        
        super(CompositionSection, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CompositionSection, self).elementProperties()
        js.extend([
            ("title", "title", str, False, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("author", "author", fhirreference.FHIRReference, True, None, False),
            ("focus", "focus", fhirreference.FHIRReference, False, None, False),
            ("text", "text", narrative.Narrative, False, None, False),
            ("mode", "mode", str, False, None, False),
            ("orderedBy", "orderedBy", codeableconcept.CodeableConcept, False, None, False),
            ("entry", "entry", fhirreference.FHIRReference, True, None, False),
            ("emptyReason", "emptyReason", codeableconcept.CodeableConcept, False, None, False),
            ("section", "section", CompositionSection, True, None, False),
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
try:
    from . import narrative
except ImportError:
    narrative = sys.modules[__package__ + '.narrative']
try:
    from . import period
except ImportError:
    period = sys.modules[__package__ + '.period']
