#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/ResearchElementDefinition) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class ResearchElementDefinition(domainresource.DomainResource):
    """ A population, intervention, or exposure definition.
    
    The ResearchElementDefinition resource describes a "PICO" element that
    knowledge (evidence, assertion, recommendation) is about.
    """
    
    resource_type = "ResearchElementDefinition"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['url'] = """Canonical identifier for this research element definition, represented as a URI (globally unique)."""
    _attribute_docstrings['identifier'] = """Additional identifier for the research element definition."""
    _attribute_docstrings['version'] = """Business version of the research element definition."""
    _attribute_docstrings['name'] = """Name for this research element definition (computer friendly)."""
    _attribute_docstrings['title'] = """Name for this research element definition (human friendly)."""
    _attribute_docstrings['shortTitle'] = """Title for use in informal contexts."""
    _attribute_docstrings['subtitle'] = """Subordinate title of the ResearchElementDefinition."""
    _attribute_docstrings['status'] = """The status of this research element definition. Enables tracking the life-cycle of the content."""
    _attribute_docstrings['experimental'] = """For testing purposes, not real usage."""
    _attribute_docstrings['subjectCodeableConcept'] = """The intended subjects for the ResearchElementDefinition. If this element is not provided, a Patient subject is assumed, but the subject of the ResearchElementDefinition can be anything."""
    _attribute_docstrings['subjectReference'] = """E.g. Patient, Practitioner, RelatedPerson, Organization, Location, Device."""
    _attribute_docstrings['date'] = """Date last changed."""
    _attribute_docstrings['publisher'] = """Name of the publisher (organization or individual)."""
    _attribute_docstrings['contact'] = """Contact details for the publisher."""
    _attribute_docstrings['description'] = """Natural language description of the research element definition."""
    _attribute_docstrings['comment'] = """Used for footnotes or explanatory notes."""
    _attribute_docstrings['useContext'] = """The context that the content is intended to support."""
    _attribute_docstrings['jurisdiction'] = """Intended jurisdiction for research element definition (if applicable)."""
    _attribute_docstrings['purpose'] = """Why this research element definition is defined."""
    _attribute_docstrings['usage'] = """Describes the clinical usage of the ResearchElementDefinition."""
    _attribute_docstrings['copyright'] = """Use and/or publishing restrictions."""
    _attribute_docstrings['approvalDate'] = """When the research element definition was approved by publisher."""
    _attribute_docstrings['lastReviewDate'] = """When the research element definition was last reviewed."""
    _attribute_docstrings['effectivePeriod'] = """When the research element definition is expected to be used."""
    _attribute_docstrings['topic'] = """Descriptive topics related to the content of the ResearchElementDefinition. Topics provide a high-level categorization grouping types of ResearchElementDefinitions that can be useful for filtering and searching."""
    _attribute_docstrings['author'] = """Who authored the content."""
    _attribute_docstrings['editor'] = """Who edited the content."""
    _attribute_docstrings['reviewer'] = """Who reviewed the content."""
    _attribute_docstrings['endorser'] = """Who endorsed the content."""
    _attribute_docstrings['relatedArtifact'] = """Additional documentation, citations, etc.."""
    _attribute_docstrings['library'] = """Logic used by the ResearchElementDefinition."""
    _attribute_docstrings['type'] = """The type of research element, a population, an exposure, or an outcome."""
    _attribute_docstrings['variableType'] = """The type of the outcome (e.g. Dichotomous, Continuous, or Descriptive)."""
    _attribute_docstrings['characteristic'] = """What defines the members of the research element."""

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
    _attribute_enums['subjectCodeableConcept'] = {
        'url': 'http://hl7.org/fhir/resource-types',
        'restricted_to': ['Account', 'ActivityDefinition', 'AdverseEvent', 'AllergyIntolerance', 'Appointment', 'AppointmentResponse', 'AuditEvent', 'Basic', 'Binary', 'BiologicallyDerivedProduct', 'BodyStructure', 'Bundle', 'CapabilityStatement', 'CarePlan', 'CareTeam', 'CatalogEntry', 'ChargeItem', 'ChargeItemDefinition', 'Claim', 'ClaimResponse', 'ClinicalImpression', 'CodeSystem', 'Communication', 'CommunicationRequest', 'CompartmentDefinition', 'Composition', 'ConceptMap', 'Condition', 'Consent', 'Contract', 'Coverage', 'CoverageEligibilityRequest', 'CoverageEligibilityResponse', 'DetectedIssue', 'Device', 'DeviceDefinition', 'DeviceMetric', 'DeviceRequest', 'DeviceUseStatement', 'DiagnosticReport', 'DocumentManifest', 'DocumentReference', 'DomainResource', 'EffectEvidenceSynthesis', 'Encounter', 'Endpoint', 'EnrollmentRequest', 'EnrollmentResponse', 'EpisodeOfCare', 'EventDefinition', 'Evidence', 'EvidenceVariable', 'ExampleScenario', 'ExplanationOfBenefit', 'FamilyMemberHistory', 'Flag', 'Goal', 'GraphDefinition', 'Group', 'GuidanceResponse', 'HealthcareService', 'ImagingStudy', 'Immunization', 'ImmunizationEvaluation', 'ImmunizationRecommendation', 'ImplementationGuide', 'InsurancePlan', 'Invoice', 'Library', 'Linkage', 'List', 'Location', 'Measure', 'MeasureReport', 'Media', 'Medication', 'MedicationAdministration', 'MedicationDispense', 'MedicationKnowledge', 'MedicationRequest', 'MedicationStatement', 'MedicinalProduct', 'MedicinalProductAuthorization', 'MedicinalProductContraindication', 'MedicinalProductIndication', 'MedicinalProductIngredient', 'MedicinalProductInteraction', 'MedicinalProductManufactured', 'MedicinalProductPackaged', 'MedicinalProductPharmaceutical', 'MedicinalProductUndesirableEffect', 'MessageDefinition', 'MessageHeader', 'MolecularSequence', 'NamingSystem', 'NutritionOrder', 'Observation', 'ObservationDefinition', 'OperationDefinition', 'OperationOutcome', 'Organization', 'OrganizationAffiliation', 'Parameters', 'Patient', 'PaymentNotice', 'PaymentReconciliation', 'Person', 'PlanDefinition', 'Practitioner', 'PractitionerRole', 'Procedure', 'Provenance', 'Questionnaire', 'QuestionnaireResponse', 'RelatedPerson', 'RequestGroup', 'ResearchDefinition', 'ResearchElementDefinition', 'ResearchStudy', 'ResearchSubject', 'Resource', 'RiskAssessment', 'RiskEvidenceSynthesis', 'Schedule', 'SearchParameter', 'ServiceRequest', 'Slot', 'Specimen', 'SpecimenDefinition', 'StructureDefinition', 'StructureMap', 'Subscription', 'Substance', 'SubstanceNucleicAcid', 'SubstancePolymer', 'SubstanceProtein', 'SubstanceReferenceInformation', 'SubstanceSourceMaterial', 'SubstanceSpecification', 'SupplyDelivery', 'SupplyRequest', 'Task', 'TerminologyCapabilities', 'TestReport', 'TestScript', 'ValueSet', 'VerificationResult', 'VisionPrescription'],
        'binding_strength': 'extensible',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['topic'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/definition-topic',
        'restricted_to': ['treatment', 'education', 'assessment'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['type'] = {
        'url': 'http://hl7.org/fhir/research-element-type',
        'restricted_to': ['population', 'exposure', 'outcome'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['variableType'] = {
        'url': 'http://hl7.org/fhir/variable-type',
        'restricted_to': ['dichotomous', 'continuous', 'descriptive'],
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
        
        self.url = None
        """ Canonical identifier for this research element definition,
        represented as a URI (globally unique).
        Type `str`. """
        
        self.identifier = None
        """ Additional identifier for the research element definition.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.version = None
        """ Business version of the research element definition.
        Type `str`. """
        
        self.name = None
        """ Name for this research element definition (computer friendly).
        Type `str`. """
        
        self.title = None
        """ Name for this research element definition (human friendly).
        Type `str`. """
        
        self.shortTitle = None
        """ Title for use in informal contexts.
        Type `str`. """
        
        self.subtitle = None
        """ Subordinate title of the ResearchElementDefinition.
        Type `str`. """
        
        self.status = None
        """ The status of this research element definition. Enables tracking
        the life-cycle of the content.
        Type `str`. """
        
        self.experimental = None
        """ For testing purposes, not real usage.
        Type `bool`. """
        
        self.subjectCodeableConcept = None
        """ The intended subjects for the ResearchElementDefinition. If this
        element is not provided, a Patient subject is assumed, but the
        subject of the ResearchElementDefinition can be anything.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subjectReference = None
        """ E.g. Patient, Practitioner, RelatedPerson, Organization, Location,
        Device.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
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
        """ Natural language description of the research element definition.
        Type `str`. """
        
        self.comment = None
        """ Used for footnotes or explanatory notes.
        List of `str` items. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for research element definition (if
        applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.purpose = None
        """ Why this research element definition is defined.
        Type `str`. """
        
        self.usage = None
        """ Describes the clinical usage of the ResearchElementDefinition.
        Type `str`. """
        
        self.copyright = None
        """ Use and/or publishing restrictions.
        Type `str`. """
        
        self.approvalDate = None
        """ When the research element definition was approved by publisher.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.lastReviewDate = None
        """ When the research element definition was last reviewed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.effectivePeriod = None
        """ When the research element definition is expected to be used.
        Type `Period` (represented as `dict` in JSON). """
        
        self.topic = None
        """ Descriptive topics related to the content of the
        ResearchElementDefinition. Topics provide a high-level
        categorization grouping types of ResearchElementDefinitions that
        can be useful for filtering and searching.
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
        
        self.library = None
        """ Logic used by the ResearchElementDefinition.
        List of `str` items. """
        
        self.type = None
        """ The type of research element, a population, an exposure, or an
        outcome.
        Type `str`. """
        
        self.variableType = None
        """ The type of the outcome (e.g. Dichotomous, Continuous, or
        Descriptive).
        Type `str`. """
        
        self.characteristic = None
        """ What defines the members of the research element.
        List of `ResearchElementDefinitionCharacteristic` items (represented as `dict` in JSON). """
        
        super(ResearchElementDefinition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ResearchElementDefinition, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("version", "version", str, False, None, False),
            ("name", "name", str, False, None, False),
            ("title", "title", str, False, None, False),
            ("shortTitle", "shortTitle", str, False, None, False),
            ("subtitle", "subtitle", str, False, None, False),
            ("status", "status", str, False, None, True),
            ("experimental", "experimental", bool, False, None, False),
            ("subjectCodeableConcept", "subjectCodeableConcept", codeableconcept.CodeableConcept, False, "subject", False),
            ("subjectReference", "subjectReference", fhirreference.FHIRReference, False, "subject", False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("publisher", "publisher", str, False, None, False),
            ("contact", "contact", contactdetail.ContactDetail, True, None, False),
            ("description", "description", str, False, None, False),
            ("comment", "comment", str, True, None, False),
            ("useContext", "useContext", usagecontext.UsageContext, True, None, False),
            ("jurisdiction", "jurisdiction", codeableconcept.CodeableConcept, True, None, False),
            ("purpose", "purpose", str, False, None, False),
            ("usage", "usage", str, False, None, False),
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
            ("library", "library", str, True, None, False),
            ("type", "type", str, False, None, True),
            ("variableType", "variableType", str, False, None, False),
            ("characteristic", "characteristic", ResearchElementDefinitionCharacteristic, True, None, True),
        ])
        return js


from . import backboneelement

class ResearchElementDefinitionCharacteristic(backboneelement.BackboneElement):
    """ What defines the members of the research element.
    
    A characteristic that defines the members of the research element. Multiple
    characteristics are applied with "and" semantics.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['definitionCodeableConcept'] = """What code or expression defines members?."""
    _attribute_docstrings['definitionCanonical'] = """What code or expression defines members?."""
    _attribute_docstrings['definitionExpression'] = """What code or expression defines members?."""
    _attribute_docstrings['definitionDataRequirement'] = """What code or expression defines members?."""
    _attribute_docstrings['usageContext'] = """What code/value pairs define members?."""
    _attribute_docstrings['exclude'] = """Whether the characteristic includes or excludes members."""
    _attribute_docstrings['unitOfMeasure'] = """What unit is the outcome described in?."""
    _attribute_docstrings['studyEffectiveDescription'] = """What time period does the study cover."""
    _attribute_docstrings['studyEffectiveDateTime'] = """What time period does the study cover."""
    _attribute_docstrings['studyEffectivePeriod'] = """What time period does the study cover."""
    _attribute_docstrings['studyEffectiveDuration'] = """What time period does the study cover."""
    _attribute_docstrings['studyEffectiveTiming'] = """What time period does the study cover."""
    _attribute_docstrings['studyEffectiveTimeFromStart'] = """Observation time from study start."""
    _attribute_docstrings['studyEffectiveGroupMeasure'] = """Indicates how elements are aggregated within the study effective period."""
    _attribute_docstrings['participantEffectiveDescription'] = """What time period do participants cover."""
    _attribute_docstrings['participantEffectiveDateTime'] = """What time period do participants cover."""
    _attribute_docstrings['participantEffectivePeriod'] = """What time period do participants cover."""
    _attribute_docstrings['participantEffectiveDuration'] = """What time period do participants cover."""
    _attribute_docstrings['participantEffectiveTiming'] = """What time period do participants cover."""
    _attribute_docstrings['participantEffectiveTimeFromStart'] = """Observation time from study start."""
    _attribute_docstrings['participantEffectiveGroupMeasure'] = """Indicates how elements are aggregated within the study effective period."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['studyEffectiveGroupMeasure'] = {
        'url': 'http://hl7.org/fhir/group-measure',
        'restricted_to': ['mean', 'median', 'mean-of-mean', 'mean-of-median', 'median-of-mean', 'median-of-median'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['participantEffectiveGroupMeasure'] = {
        'url': 'http://hl7.org/fhir/group-measure',
        'restricted_to': ['mean', 'median', 'mean-of-mean', 'mean-of-median', 'median-of-mean', 'median-of-median'],
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
        
        self.definitionCodeableConcept = None
        """ What code or expression defines members?.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.definitionCanonical = None
        """ What code or expression defines members?.
        Type `str`. """
        
        self.definitionExpression = None
        """ What code or expression defines members?.
        Type `Expression` (represented as `dict` in JSON). """
        
        self.definitionDataRequirement = None
        """ What code or expression defines members?.
        Type `DataRequirement` (represented as `dict` in JSON). """
        
        self.usageContext = None
        """ What code/value pairs define members?.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.exclude = None
        """ Whether the characteristic includes or excludes members.
        Type `bool`. """
        
        self.unitOfMeasure = None
        """ What unit is the outcome described in?.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.studyEffectiveDescription = None
        """ What time period does the study cover.
        Type `str`. """
        
        self.studyEffectiveDateTime = None
        """ What time period does the study cover.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.studyEffectivePeriod = None
        """ What time period does the study cover.
        Type `Period` (represented as `dict` in JSON). """
        
        self.studyEffectiveDuration = None
        """ What time period does the study cover.
        Type `Duration` (represented as `dict` in JSON). """
        
        self.studyEffectiveTiming = None
        """ What time period does the study cover.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.studyEffectiveTimeFromStart = None
        """ Observation time from study start.
        Type `Duration` (represented as `dict` in JSON). """
        
        self.studyEffectiveGroupMeasure = None
        """ Indicates how elements are aggregated within the study effective
        period.
        Type `str`. """
        
        self.participantEffectiveDescription = None
        """ What time period do participants cover.
        Type `str`. """
        
        self.participantEffectiveDateTime = None
        """ What time period do participants cover.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.participantEffectivePeriod = None
        """ What time period do participants cover.
        Type `Period` (represented as `dict` in JSON). """
        
        self.participantEffectiveDuration = None
        """ What time period do participants cover.
        Type `Duration` (represented as `dict` in JSON). """
        
        self.participantEffectiveTiming = None
        """ What time period do participants cover.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.participantEffectiveTimeFromStart = None
        """ Observation time from study start.
        Type `Duration` (represented as `dict` in JSON). """
        
        self.participantEffectiveGroupMeasure = None
        """ Indicates how elements are aggregated within the study effective
        period.
        Type `str`. """
        
        super(ResearchElementDefinitionCharacteristic, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ResearchElementDefinitionCharacteristic, self).elementProperties()
        js.extend([
            ("definitionCodeableConcept", "definitionCodeableConcept", codeableconcept.CodeableConcept, False, "definition", True),
            ("definitionCanonical", "definitionCanonical", str, False, "definition", True),
            ("definitionExpression", "definitionExpression", expression.Expression, False, "definition", True),
            ("definitionDataRequirement", "definitionDataRequirement", datarequirement.DataRequirement, False, "definition", True),
            ("usageContext", "usageContext", usagecontext.UsageContext, True, None, False),
            ("exclude", "exclude", bool, False, None, False),
            ("unitOfMeasure", "unitOfMeasure", codeableconcept.CodeableConcept, False, None, False),
            ("studyEffectiveDescription", "studyEffectiveDescription", str, False, None, False),
            ("studyEffectiveDateTime", "studyEffectiveDateTime", fhirdate.FHIRDate, False, "studyEffective", False),
            ("studyEffectivePeriod", "studyEffectivePeriod", period.Period, False, "studyEffective", False),
            ("studyEffectiveDuration", "studyEffectiveDuration", duration.Duration, False, "studyEffective", False),
            ("studyEffectiveTiming", "studyEffectiveTiming", timing.Timing, False, "studyEffective", False),
            ("studyEffectiveTimeFromStart", "studyEffectiveTimeFromStart", duration.Duration, False, None, False),
            ("studyEffectiveGroupMeasure", "studyEffectiveGroupMeasure", str, False, None, False),
            ("participantEffectiveDescription", "participantEffectiveDescription", str, False, None, False),
            ("participantEffectiveDateTime", "participantEffectiveDateTime", fhirdate.FHIRDate, False, "participantEffective", False),
            ("participantEffectivePeriod", "participantEffectivePeriod", period.Period, False, "participantEffective", False),
            ("participantEffectiveDuration", "participantEffectiveDuration", duration.Duration, False, "participantEffective", False),
            ("participantEffectiveTiming", "participantEffectiveTiming", timing.Timing, False, "participantEffective", False),
            ("participantEffectiveTimeFromStart", "participantEffectiveTimeFromStart", duration.Duration, False, None, False),
            ("participantEffectiveGroupMeasure", "participantEffectiveGroupMeasure", str, False, None, False),
        ])
        return js


import sys
try:
    from . import codeableconcept
except ImportError:
    codeableconcept = sys.modules[__package__ + '.codeableconcept']
try:
    from . import contactdetail
except ImportError:
    contactdetail = sys.modules[__package__ + '.contactdetail']
try:
    from . import datarequirement
except ImportError:
    datarequirement = sys.modules[__package__ + '.datarequirement']
try:
    from . import duration
except ImportError:
    duration = sys.modules[__package__ + '.duration']
try:
    from . import expression
except ImportError:
    expression = sys.modules[__package__ + '.expression']
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
    from . import timing
except ImportError:
    timing = sys.modules[__package__ + '.timing']
try:
    from . import usagecontext
except ImportError:
    usagecontext = sys.modules[__package__ + '.usagecontext']
