#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Measure) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Measure(domainresource.DomainResource):
    """ A quality measure definition.
    
    The Measure resource provides the definition of a quality measure.
    """
    
    resource_type = "Measure"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['url'] = """Canonical identifier for this measure, represented as a URI (globally unique)."""
    _attribute_docstrings['identifier'] = """Additional identifier for the measure."""
    _attribute_docstrings['version'] = """Business version of the measure."""
    _attribute_docstrings['name'] = """Name for this measure (computer friendly)."""
    _attribute_docstrings['title'] = """Name for this measure (human friendly)."""
    _attribute_docstrings['subtitle'] = """Subordinate title of the measure."""
    _attribute_docstrings['status'] = """The status of this measure. Enables tracking the life-cycle of the content."""
    _attribute_docstrings['experimental'] = """For testing purposes, not real usage."""
    _attribute_docstrings['subjectCodeableConcept'] = """The intended subjects for the measure. If this element is not provided, a Patient subject is assumed, but the subject of the measure can be anything."""
    _attribute_docstrings['subjectReference'] = """E.g. Patient, Practitioner, RelatedPerson, Organization, Location, Device."""
    _attribute_docstrings['date'] = """Date last changed."""
    _attribute_docstrings['publisher'] = """Name of the publisher (organization or individual)."""
    _attribute_docstrings['contact'] = """Contact details for the publisher."""
    _attribute_docstrings['description'] = """Natural language description of the measure."""
    _attribute_docstrings['useContext'] = """The context that the content is intended to support."""
    _attribute_docstrings['jurisdiction'] = """Intended jurisdiction for measure (if applicable)."""
    _attribute_docstrings['purpose'] = """Why this measure is defined."""
    _attribute_docstrings['usage'] = """Describes the clinical usage of the measure."""
    _attribute_docstrings['copyright'] = """Use and/or publishing restrictions."""
    _attribute_docstrings['approvalDate'] = """When the measure was approved by publisher."""
    _attribute_docstrings['lastReviewDate'] = """When the measure was last reviewed."""
    _attribute_docstrings['effectivePeriod'] = """When the measure is expected to be used."""
    _attribute_docstrings['topic'] = """Descriptive topics related to the content of the measure. Topics provide a high-level categorization grouping types of measures that can be useful for filtering and searching."""
    _attribute_docstrings['author'] = """Who authored the content."""
    _attribute_docstrings['editor'] = """Who edited the content."""
    _attribute_docstrings['reviewer'] = """Who reviewed the content."""
    _attribute_docstrings['endorser'] = """Who endorsed the content."""
    _attribute_docstrings['relatedArtifact'] = """Additional documentation, citations, etc.."""
    _attribute_docstrings['library'] = """Logic used by the measure."""
    _attribute_docstrings['disclaimer'] = """Disclaimer for use of the measure or its referenced content."""
    _attribute_docstrings['scoring'] = """Indicates how the calculation is performed for the measure, including proportion, ratio, continuous-variable, and cohort. The value set is extensible, allowing additional measure scoring types to be represented."""
    _attribute_docstrings['compositeScoring'] = """If this is a composite measure, the scoring method used to combine the component measures to determine the composite score."""
    _attribute_docstrings['type'] = """Indicates whether the measure is used to examine a process, an outcome over time, a patient-reported outcome, or a structure measure such as utilization."""
    _attribute_docstrings['riskAdjustment'] = """How risk adjustment is applied for this measure."""
    _attribute_docstrings['rateAggregation'] = """How is rate aggregation performed for this measure."""
    _attribute_docstrings['rationale'] = """Detailed description of why the measure exists."""
    _attribute_docstrings['clinicalRecommendationStatement'] = """Summary of clinical guidelines."""
    _attribute_docstrings['improvementNotation'] = """Information on whether an increase or decrease in score is the preferred result (e.g., a higher score indicates better quality OR a lower score indicates better quality OR quality is within a range)."""
    _attribute_docstrings['definition'] = """Defined terms used in the measure documentation."""
    _attribute_docstrings['guidance'] = """Additional guidance for implementers."""
    _attribute_docstrings['group'] = """Population criteria group."""
    _attribute_docstrings['supplementalData'] = """What other data should be reported with the measure."""

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
    _attribute_enums['scoring'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/measure-scoring',
        'restricted_to': ['proportion', 'ratio', 'continuous-variable', 'cohort'],
        'binding_strength': 'extensible',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['compositeScoring'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/composite-measure-scoring',
        'restricted_to': ['opportunity', 'all-or-nothing', 'linear', 'weighted'],
        'binding_strength': 'extensible',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/measure-type',
        'restricted_to': ['process', 'outcome', 'structure', 'patient-reported-outcome', 'composite'],
        'binding_strength': 'extensible',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['improvementNotation'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/measure-improvement-notation',
        'restricted_to': ['increase', 'decrease'],
        'binding_strength': 'required',
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
        """ Canonical identifier for this measure, represented as a URI
        (globally unique).
        Type `str`. """
        
        self.identifier = None
        """ Additional identifier for the measure.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.version = None
        """ Business version of the measure.
        Type `str`. """
        
        self.name = None
        """ Name for this measure (computer friendly).
        Type `str`. """
        
        self.title = None
        """ Name for this measure (human friendly).
        Type `str`. """
        
        self.subtitle = None
        """ Subordinate title of the measure.
        Type `str`. """
        
        self.status = None
        """ The status of this measure. Enables tracking the life-cycle of the
        content.
        Type `str`. """
        
        self.experimental = None
        """ For testing purposes, not real usage.
        Type `bool`. """
        
        self.subjectCodeableConcept = None
        """ The intended subjects for the measure. If this element is not
        provided, a Patient subject is assumed, but the subject of the
        measure can be anything.
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
        """ Natural language description of the measure.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for measure (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.purpose = None
        """ Why this measure is defined.
        Type `str`. """
        
        self.usage = None
        """ Describes the clinical usage of the measure.
        Type `str`. """
        
        self.copyright = None
        """ Use and/or publishing restrictions.
        Type `str`. """
        
        self.approvalDate = None
        """ When the measure was approved by publisher.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.lastReviewDate = None
        """ When the measure was last reviewed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.effectivePeriod = None
        """ When the measure is expected to be used.
        Type `Period` (represented as `dict` in JSON). """
        
        self.topic = None
        """ Descriptive topics related to the content of the measure. Topics
        provide a high-level categorization grouping types of measures that
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
        """ Logic used by the measure.
        List of `str` items. """
        
        self.disclaimer = None
        """ Disclaimer for use of the measure or its referenced content.
        Type `str`. """
        
        self.scoring = None
        """ Indicates how the calculation is performed for the measure,
        including proportion, ratio, continuous-variable, and cohort. The
        value set is extensible, allowing additional measure scoring types
        to be represented.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.compositeScoring = None
        """ If this is a composite measure, the scoring method used to combine
        the component measures to determine the composite score.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.type = None
        """ Indicates whether the measure is used to examine a process, an
        outcome over time, a patient-reported outcome, or a structure
        measure such as utilization.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.riskAdjustment = None
        """ How risk adjustment is applied for this measure.
        Type `str`. """
        
        self.rateAggregation = None
        """ How is rate aggregation performed for this measure.
        Type `str`. """
        
        self.rationale = None
        """ Detailed description of why the measure exists.
        Type `str`. """
        
        self.clinicalRecommendationStatement = None
        """ Summary of clinical guidelines.
        Type `str`. """
        
        self.improvementNotation = None
        """ Information on whether an increase or decrease in score is the
        preferred result (e.g., a higher score indicates better quality OR
        a lower score indicates better quality OR quality is within a
        range).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.definition = None
        """ Defined terms used in the measure documentation.
        List of `str` items. """
        
        self.guidance = None
        """ Additional guidance for implementers.
        Type `str`. """
        
        self.group = None
        """ Population criteria group.
        List of `MeasureGroup` items (represented as `dict` in JSON). """
        
        self.supplementalData = None
        """ What other data should be reported with the measure.
        List of `MeasureSupplementalData` items (represented as `dict` in JSON). """
        
        super(Measure, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Measure, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("version", "version", str, False, None, False),
            ("name", "name", str, False, None, False),
            ("title", "title", str, False, None, False),
            ("subtitle", "subtitle", str, False, None, False),
            ("status", "status", str, False, None, True),
            ("experimental", "experimental", bool, False, None, False),
            ("subjectCodeableConcept", "subjectCodeableConcept", codeableconcept.CodeableConcept, False, "subject", False),
            ("subjectReference", "subjectReference", fhirreference.FHIRReference, False, "subject", False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("publisher", "publisher", str, False, None, False),
            ("contact", "contact", contactdetail.ContactDetail, True, None, False),
            ("description", "description", str, False, None, False),
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
            ("disclaimer", "disclaimer", str, False, None, False),
            ("scoring", "scoring", codeableconcept.CodeableConcept, False, None, False),
            ("compositeScoring", "compositeScoring", codeableconcept.CodeableConcept, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, True, None, False),
            ("riskAdjustment", "riskAdjustment", str, False, None, False),
            ("rateAggregation", "rateAggregation", str, False, None, False),
            ("rationale", "rationale", str, False, None, False),
            ("clinicalRecommendationStatement", "clinicalRecommendationStatement", str, False, None, False),
            ("improvementNotation", "improvementNotation", codeableconcept.CodeableConcept, False, None, False),
            ("definition", "definition", str, True, None, False),
            ("guidance", "guidance", str, False, None, False),
            ("group", "group", MeasureGroup, True, None, False),
            ("supplementalData", "supplementalData", MeasureSupplementalData, True, None, False),
        ])
        return js


from . import backboneelement

class MeasureGroup(backboneelement.BackboneElement):
    """ Population criteria group.
    
    A group of population criteria for the measure.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Meaning of the group."""
    _attribute_docstrings['description'] = """Summary description."""
    _attribute_docstrings['population'] = """Population criteria."""
    _attribute_docstrings['stratifier'] = """Stratifier criteria for the measure."""

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
        """ Meaning of the group.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.description = None
        """ Summary description.
        Type `str`. """
        
        self.population = None
        """ Population criteria.
        List of `MeasureGroupPopulation` items (represented as `dict` in JSON). """
        
        self.stratifier = None
        """ Stratifier criteria for the measure.
        List of `MeasureGroupStratifier` items (represented as `dict` in JSON). """
        
        super(MeasureGroup, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MeasureGroup, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("description", "description", str, False, None, False),
            ("population", "population", MeasureGroupPopulation, True, None, False),
            ("stratifier", "stratifier", MeasureGroupStratifier, True, None, False),
        ])
        return js


class MeasureGroupPopulation(backboneelement.BackboneElement):
    """ Population criteria.
    
    A population criteria for the measure.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """The type of population criteria."""
    _attribute_docstrings['description'] = """The human readable description of this population criteria."""
    _attribute_docstrings['criteria'] = """The criteria that defines this population."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['code'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/measure-population',
        'restricted_to': ['initial-population', 'numerator', 'numerator-exclusion', 'denominator', 'denominator-exclusion', 'denominator-exception', 'measure-population', 'measure-population-exclusion', 'measure-observation'],
        'binding_strength': 'extensible',
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
        
        self.code = None
        """ The type of population criteria.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.description = None
        """ The human readable description of this population criteria.
        Type `str`. """
        
        self.criteria = None
        """ The criteria that defines this population.
        Type `Expression` (represented as `dict` in JSON). """
        
        super(MeasureGroupPopulation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MeasureGroupPopulation, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("description", "description", str, False, None, False),
            ("criteria", "criteria", expression.Expression, False, None, True),
        ])
        return js


class MeasureGroupStratifier(backboneelement.BackboneElement):
    """ Stratifier criteria for the measure.
    
    The stratifier criteria for the measure report, specified as either the
    name of a valid CQL expression defined within a referenced library or a
    valid FHIR Resource Path.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Meaning of the stratifier."""
    _attribute_docstrings['description'] = """The human readable description of this stratifier."""
    _attribute_docstrings['criteria'] = """How the measure should be stratified."""
    _attribute_docstrings['component'] = """Stratifier criteria component for the measure."""

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
        """ Meaning of the stratifier.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.description = None
        """ The human readable description of this stratifier.
        Type `str`. """
        
        self.criteria = None
        """ How the measure should be stratified.
        Type `Expression` (represented as `dict` in JSON). """
        
        self.component = None
        """ Stratifier criteria component for the measure.
        List of `MeasureGroupStratifierComponent` items (represented as `dict` in JSON). """
        
        super(MeasureGroupStratifier, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MeasureGroupStratifier, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("description", "description", str, False, None, False),
            ("criteria", "criteria", expression.Expression, False, None, False),
            ("component", "component", MeasureGroupStratifierComponent, True, None, False),
        ])
        return js


class MeasureGroupStratifierComponent(backboneelement.BackboneElement):
    """ Stratifier criteria component for the measure.
    
    A component of the stratifier criteria for the measure report, specified as
    either the name of a valid CQL expression defined within a referenced
    library or a valid FHIR Resource Path.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Meaning of the stratifier component."""
    _attribute_docstrings['description'] = """The human readable description of this stratifier component."""
    _attribute_docstrings['criteria'] = """Component of how the measure should be stratified."""

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
        """ Meaning of the stratifier component.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.description = None
        """ The human readable description of this stratifier component.
        Type `str`. """
        
        self.criteria = None
        """ Component of how the measure should be stratified.
        Type `Expression` (represented as `dict` in JSON). """
        
        super(MeasureGroupStratifierComponent, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MeasureGroupStratifierComponent, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("description", "description", str, False, None, False),
            ("criteria", "criteria", expression.Expression, False, None, True),
        ])
        return js


class MeasureSupplementalData(backboneelement.BackboneElement):
    """ What other data should be reported with the measure.
    
    The supplemental data criteria for the measure report, specified as either
    the name of a valid CQL expression within a referenced library, or a valid
    FHIR Resource Path.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Meaning of the supplemental data."""
    _attribute_docstrings['usage'] = """An indicator of the intended usage for the supplemental data element. Supplemental data indicates the data is additional information requested to augment the measure information. Risk adjustment factor indicates the data is additional information used to calculate risk adjustment factors when applying a risk model to the measure calculation."""
    _attribute_docstrings['description'] = """The human readable description of this supplemental data."""
    _attribute_docstrings['criteria'] = """Expression describing additional data to be reported."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['usage'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/measure-data-usage',
        'restricted_to': ['supplemental-data', 'risk-adjustment-factor'],
        'binding_strength': 'extensible',
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
        
        self.code = None
        """ Meaning of the supplemental data.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.usage = None
        """ An indicator of the intended usage for the supplemental data
        element. Supplemental data indicates the data is additional
        information requested to augment the measure information. Risk
        adjustment factor indicates the data is additional information used
        to calculate risk adjustment factors when applying a risk model to
        the measure calculation.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.description = None
        """ The human readable description of this supplemental data.
        Type `str`. """
        
        self.criteria = None
        """ Expression describing additional data to be reported.
        Type `Expression` (represented as `dict` in JSON). """
        
        super(MeasureSupplementalData, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MeasureSupplementalData, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("usage", "usage", codeableconcept.CodeableConcept, True, None, False),
            ("description", "description", str, False, None, False),
            ("criteria", "criteria", expression.Expression, False, None, True),
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
    from . import usagecontext
except ImportError:
    usagecontext = sys.modules[__package__ + '.usagecontext']
