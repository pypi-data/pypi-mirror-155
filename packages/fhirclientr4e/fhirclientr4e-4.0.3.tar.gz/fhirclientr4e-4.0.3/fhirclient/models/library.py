#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Library) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Library(domainresource.DomainResource):
    """ Represents a library of quality improvement components.
    
    The Library resource is a general-purpose container for knowledge asset
    definitions. It can be used to describe and expose existing knowledge
    assets such as logic libraries and information model descriptions, as well
    as to describe a collection of knowledge assets.
    """
    
    resource_type = "Library"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['url'] = """Canonical identifier for this library, represented as a URI (globally unique)."""
    _attribute_docstrings['identifier'] = """Additional identifier for the library."""
    _attribute_docstrings['version'] = """Business version of the library."""
    _attribute_docstrings['name'] = """Name for this library (computer friendly)."""
    _attribute_docstrings['title'] = """Name for this library (human friendly)."""
    _attribute_docstrings['subtitle'] = """Subordinate title of the library."""
    _attribute_docstrings['status'] = """The status of this library. Enables tracking the life-cycle of the content."""
    _attribute_docstrings['experimental'] = """For testing purposes, not real usage."""
    _attribute_docstrings['type'] = """Identifies the type of library such as a Logic Library, Model Definition, Asset Collection, or Module Definition."""
    _attribute_docstrings['subjectCodeableConcept'] = """A code or group definition that describes the intended subject of the contents of the library."""
    _attribute_docstrings['subjectReference'] = """Type of individual the library content is focused on."""
    _attribute_docstrings['date'] = """Date last changed."""
    _attribute_docstrings['publisher'] = """Name of the publisher (organization or individual)."""
    _attribute_docstrings['contact'] = """Contact details for the publisher."""
    _attribute_docstrings['description'] = """Natural language description of the library."""
    _attribute_docstrings['useContext'] = """The context that the content is intended to support."""
    _attribute_docstrings['jurisdiction'] = """Intended jurisdiction for library (if applicable)."""
    _attribute_docstrings['purpose'] = """Why this library is defined."""
    _attribute_docstrings['usage'] = """Describes the clinical usage of the library."""
    _attribute_docstrings['copyright'] = """Use and/or publishing restrictions."""
    _attribute_docstrings['approvalDate'] = """When the library was approved by publisher."""
    _attribute_docstrings['lastReviewDate'] = """When the library was last reviewed."""
    _attribute_docstrings['effectivePeriod'] = """When the library is expected to be used."""
    _attribute_docstrings['topic'] = """Descriptive topics related to the content of the library. Topics provide a high-level categorization of the library that can be useful for filtering and searching."""
    _attribute_docstrings['author'] = """Who authored the content."""
    _attribute_docstrings['editor'] = """Who edited the content."""
    _attribute_docstrings['reviewer'] = """Who reviewed the content."""
    _attribute_docstrings['endorser'] = """Who endorsed the content."""
    _attribute_docstrings['relatedArtifact'] = """Additional documentation, citations, etc.."""
    _attribute_docstrings['parameter'] = """Parameters defined by the library."""
    _attribute_docstrings['dataRequirement'] = """What data is referenced by this library."""
    _attribute_docstrings['content'] = """Contents of the library, either embedded or referenced."""

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
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/library-type',
        'restricted_to': ['logic-library', 'model-definition', 'asset-collection', 'module-definition'],
        'binding_strength': 'extensible',
        'class_name': 'CodeableConcept'
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
        """ Canonical identifier for this library, represented as a URI
        (globally unique).
        Type `str`. """
        
        self.identifier = None
        """ Additional identifier for the library.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.version = None
        """ Business version of the library.
        Type `str`. """
        
        self.name = None
        """ Name for this library (computer friendly).
        Type `str`. """
        
        self.title = None
        """ Name for this library (human friendly).
        Type `str`. """
        
        self.subtitle = None
        """ Subordinate title of the library.
        Type `str`. """
        
        self.status = None
        """ The status of this library. Enables tracking the life-cycle of the
        content.
        Type `str`. """
        
        self.experimental = None
        """ For testing purposes, not real usage.
        Type `bool`. """
        
        self.type = None
        """ Identifies the type of library such as a Logic Library, Model
        Definition, Asset Collection, or Module Definition.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subjectCodeableConcept = None
        """ A code or group definition that describes the intended subject of
        the contents of the library.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subjectReference = None
        """ Type of individual the library content is focused on.
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
        """ Natural language description of the library.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for library (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.purpose = None
        """ Why this library is defined.
        Type `str`. """
        
        self.usage = None
        """ Describes the clinical usage of the library.
        Type `str`. """
        
        self.copyright = None
        """ Use and/or publishing restrictions.
        Type `str`. """
        
        self.approvalDate = None
        """ When the library was approved by publisher.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.lastReviewDate = None
        """ When the library was last reviewed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.effectivePeriod = None
        """ When the library is expected to be used.
        Type `Period` (represented as `dict` in JSON). """
        
        self.topic = None
        """ Descriptive topics related to the content of the library. Topics
        provide a high-level categorization of the library that can be
        useful for filtering and searching.
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
        
        self.parameter = None
        """ Parameters defined by the library.
        List of `ParameterDefinition` items (represented as `dict` in JSON). """
        
        self.dataRequirement = None
        """ What data is referenced by this library.
        List of `DataRequirement` items (represented as `dict` in JSON). """
        
        self.content = None
        """ Contents of the library, either embedded or referenced.
        List of `Attachment` items (represented as `dict` in JSON). """
        
        super(Library, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Library, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("version", "version", str, False, None, False),
            ("name", "name", str, False, None, False),
            ("title", "title", str, False, None, False),
            ("subtitle", "subtitle", str, False, None, False),
            ("status", "status", str, False, None, True),
            ("experimental", "experimental", bool, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
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
            ("parameter", "parameter", parameterdefinition.ParameterDefinition, True, None, False),
            ("dataRequirement", "dataRequirement", datarequirement.DataRequirement, True, None, False),
            ("content", "content", attachment.Attachment, True, None, False),
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
    from . import contactdetail
except ImportError:
    contactdetail = sys.modules[__package__ + '.contactdetail']
try:
    from . import datarequirement
except ImportError:
    datarequirement = sys.modules[__package__ + '.datarequirement']
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
    from . import parameterdefinition
except ImportError:
    parameterdefinition = sys.modules[__package__ + '.parameterdefinition']
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
