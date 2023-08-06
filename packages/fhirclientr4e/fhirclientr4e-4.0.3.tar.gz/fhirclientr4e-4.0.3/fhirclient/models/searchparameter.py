#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/SearchParameter) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class SearchParameter(domainresource.DomainResource):
    """ Search parameter for a resource.
    
    A search parameter that defines a named search item that can be used to
    search/filter on a resource.
    """
    
    resource_type = "SearchParameter"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['url'] = """Canonical identifier for this search parameter, represented as a URI (globally unique)."""
    _attribute_docstrings['version'] = """Business version of the search parameter."""
    _attribute_docstrings['name'] = """Name for this search parameter (computer friendly)."""
    _attribute_docstrings['derivedFrom'] = """Original definition for the search parameter."""
    _attribute_docstrings['status'] = """The status of this search parameter. Enables tracking the life-cycle of the content."""
    _attribute_docstrings['experimental'] = """For testing purposes, not real usage."""
    _attribute_docstrings['date'] = """Date last changed."""
    _attribute_docstrings['publisher'] = """Name of the publisher (organization or individual)."""
    _attribute_docstrings['contact'] = """Contact details for the publisher."""
    _attribute_docstrings['description'] = """Natural language description of the search parameter."""
    _attribute_docstrings['useContext'] = """The context that the content is intended to support."""
    _attribute_docstrings['jurisdiction'] = """Intended jurisdiction for search parameter (if applicable)."""
    _attribute_docstrings['purpose'] = """Why this search parameter is defined."""
    _attribute_docstrings['code'] = """Code used in URL."""
    _attribute_docstrings['base'] = """The base resource type(s) that this search parameter can be used against."""
    _attribute_docstrings['type'] = """The type of value that a search parameter may contain, and how the content is interpreted."""
    _attribute_docstrings['expression'] = """FHIRPath expression that extracts the values."""
    _attribute_docstrings['xpath'] = """XPath that extracts the values."""
    _attribute_docstrings['xpathUsage'] = """How the search parameter relates to the set of elements returned by evaluating the xpath query."""
    _attribute_docstrings['target'] = """Types of resource (if a resource is referenced)."""
    _attribute_docstrings['multipleOr'] = """Allow multiple values per parameter (or)."""
    _attribute_docstrings['multipleAnd'] = """Allow multiple parameters (and)."""
    _attribute_docstrings['comparator'] = """Comparators supported for the search parameter."""
    _attribute_docstrings['modifier'] = """A modifier supported for the search parameter."""
    _attribute_docstrings['chain'] = """Chained names supported."""
    _attribute_docstrings['component'] = """For Composite resources to define the parts."""

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
    _attribute_enums['base'] = {
        'url': 'http://hl7.org/fhir/resource-types',
        'restricted_to': ['Account', 'ActivityDefinition', 'AdverseEvent', 'AllergyIntolerance', 'Appointment', 'AppointmentResponse', 'AuditEvent', 'Basic', 'Binary', 'BiologicallyDerivedProduct', 'BodyStructure', 'Bundle', 'CapabilityStatement', 'CarePlan', 'CareTeam', 'CatalogEntry', 'ChargeItem', 'ChargeItemDefinition', 'Claim', 'ClaimResponse', 'ClinicalImpression', 'CodeSystem', 'Communication', 'CommunicationRequest', 'CompartmentDefinition', 'Composition', 'ConceptMap', 'Condition', 'Consent', 'Contract', 'Coverage', 'CoverageEligibilityRequest', 'CoverageEligibilityResponse', 'DetectedIssue', 'Device', 'DeviceDefinition', 'DeviceMetric', 'DeviceRequest', 'DeviceUseStatement', 'DiagnosticReport', 'DocumentManifest', 'DocumentReference', 'DomainResource', 'EffectEvidenceSynthesis', 'Encounter', 'Endpoint', 'EnrollmentRequest', 'EnrollmentResponse', 'EpisodeOfCare', 'EventDefinition', 'Evidence', 'EvidenceVariable', 'ExampleScenario', 'ExplanationOfBenefit', 'FamilyMemberHistory', 'Flag', 'Goal', 'GraphDefinition', 'Group', 'GuidanceResponse', 'HealthcareService', 'ImagingStudy', 'Immunization', 'ImmunizationEvaluation', 'ImmunizationRecommendation', 'ImplementationGuide', 'InsurancePlan', 'Invoice', 'Library', 'Linkage', 'List', 'Location', 'Measure', 'MeasureReport', 'Media', 'Medication', 'MedicationAdministration', 'MedicationDispense', 'MedicationKnowledge', 'MedicationRequest', 'MedicationStatement', 'MedicinalProduct', 'MedicinalProductAuthorization', 'MedicinalProductContraindication', 'MedicinalProductIndication', 'MedicinalProductIngredient', 'MedicinalProductInteraction', 'MedicinalProductManufactured', 'MedicinalProductPackaged', 'MedicinalProductPharmaceutical', 'MedicinalProductUndesirableEffect', 'MessageDefinition', 'MessageHeader', 'MolecularSequence', 'NamingSystem', 'NutritionOrder', 'Observation', 'ObservationDefinition', 'OperationDefinition', 'OperationOutcome', 'Organization', 'OrganizationAffiliation', 'Parameters', 'Patient', 'PaymentNotice', 'PaymentReconciliation', 'Person', 'PlanDefinition', 'Practitioner', 'PractitionerRole', 'Procedure', 'Provenance', 'Questionnaire', 'QuestionnaireResponse', 'RelatedPerson', 'RequestGroup', 'ResearchDefinition', 'ResearchElementDefinition', 'ResearchStudy', 'ResearchSubject', 'Resource', 'RiskAssessment', 'RiskEvidenceSynthesis', 'Schedule', 'SearchParameter', 'ServiceRequest', 'Slot', 'Specimen', 'SpecimenDefinition', 'StructureDefinition', 'StructureMap', 'Subscription', 'Substance', 'SubstanceNucleicAcid', 'SubstancePolymer', 'SubstanceProtein', 'SubstanceReferenceInformation', 'SubstanceSourceMaterial', 'SubstanceSpecification', 'SupplyDelivery', 'SupplyRequest', 'Task', 'TerminologyCapabilities', 'TestReport', 'TestScript', 'ValueSet', 'VerificationResult', 'VisionPrescription'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['type'] = {
        'url': 'http://hl7.org/fhir/search-param-type',
        'restricted_to': ['number', 'date', 'string', 'token', 'reference', 'composite', 'quantity', 'uri', 'special'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['xpathUsage'] = {
        'url': 'http://hl7.org/fhir/search-xpath-usage',
        'restricted_to': ['normal', 'phonetic', 'nearby', 'distance', 'other'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['target'] = {
        'url': 'http://hl7.org/fhir/resource-types',
        'restricted_to': ['Account', 'ActivityDefinition', 'AdverseEvent', 'AllergyIntolerance', 'Appointment', 'AppointmentResponse', 'AuditEvent', 'Basic', 'Binary', 'BiologicallyDerivedProduct', 'BodyStructure', 'Bundle', 'CapabilityStatement', 'CarePlan', 'CareTeam', 'CatalogEntry', 'ChargeItem', 'ChargeItemDefinition', 'Claim', 'ClaimResponse', 'ClinicalImpression', 'CodeSystem', 'Communication', 'CommunicationRequest', 'CompartmentDefinition', 'Composition', 'ConceptMap', 'Condition', 'Consent', 'Contract', 'Coverage', 'CoverageEligibilityRequest', 'CoverageEligibilityResponse', 'DetectedIssue', 'Device', 'DeviceDefinition', 'DeviceMetric', 'DeviceRequest', 'DeviceUseStatement', 'DiagnosticReport', 'DocumentManifest', 'DocumentReference', 'DomainResource', 'EffectEvidenceSynthesis', 'Encounter', 'Endpoint', 'EnrollmentRequest', 'EnrollmentResponse', 'EpisodeOfCare', 'EventDefinition', 'Evidence', 'EvidenceVariable', 'ExampleScenario', 'ExplanationOfBenefit', 'FamilyMemberHistory', 'Flag', 'Goal', 'GraphDefinition', 'Group', 'GuidanceResponse', 'HealthcareService', 'ImagingStudy', 'Immunization', 'ImmunizationEvaluation', 'ImmunizationRecommendation', 'ImplementationGuide', 'InsurancePlan', 'Invoice', 'Library', 'Linkage', 'List', 'Location', 'Measure', 'MeasureReport', 'Media', 'Medication', 'MedicationAdministration', 'MedicationDispense', 'MedicationKnowledge', 'MedicationRequest', 'MedicationStatement', 'MedicinalProduct', 'MedicinalProductAuthorization', 'MedicinalProductContraindication', 'MedicinalProductIndication', 'MedicinalProductIngredient', 'MedicinalProductInteraction', 'MedicinalProductManufactured', 'MedicinalProductPackaged', 'MedicinalProductPharmaceutical', 'MedicinalProductUndesirableEffect', 'MessageDefinition', 'MessageHeader', 'MolecularSequence', 'NamingSystem', 'NutritionOrder', 'Observation', 'ObservationDefinition', 'OperationDefinition', 'OperationOutcome', 'Organization', 'OrganizationAffiliation', 'Parameters', 'Patient', 'PaymentNotice', 'PaymentReconciliation', 'Person', 'PlanDefinition', 'Practitioner', 'PractitionerRole', 'Procedure', 'Provenance', 'Questionnaire', 'QuestionnaireResponse', 'RelatedPerson', 'RequestGroup', 'ResearchDefinition', 'ResearchElementDefinition', 'ResearchStudy', 'ResearchSubject', 'Resource', 'RiskAssessment', 'RiskEvidenceSynthesis', 'Schedule', 'SearchParameter', 'ServiceRequest', 'Slot', 'Specimen', 'SpecimenDefinition', 'StructureDefinition', 'StructureMap', 'Subscription', 'Substance', 'SubstanceNucleicAcid', 'SubstancePolymer', 'SubstanceProtein', 'SubstanceReferenceInformation', 'SubstanceSourceMaterial', 'SubstanceSpecification', 'SupplyDelivery', 'SupplyRequest', 'Task', 'TerminologyCapabilities', 'TestReport', 'TestScript', 'ValueSet', 'VerificationResult', 'VisionPrescription'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['comparator'] = {
        'url': 'http://hl7.org/fhir/search-comparator',
        'restricted_to': ['eq', 'ne', 'gt', 'lt', 'ge', 'le', 'sa', 'eb', 'ap'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['modifier'] = {
        'url': 'http://hl7.org/fhir/search-modifier-code',
        'restricted_to': ['missing', 'exact', 'contains', 'not', 'text', 'in', 'not-in', 'below', 'above', 'type', 'identifier', 'ofType'],
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
        """ Canonical identifier for this search parameter, represented as a
        URI (globally unique).
        Type `str`. """
        
        self.version = None
        """ Business version of the search parameter.
        Type `str`. """
        
        self.name = None
        """ Name for this search parameter (computer friendly).
        Type `str`. """
        
        self.derivedFrom = None
        """ Original definition for the search parameter.
        Type `str`. """
        
        self.status = None
        """ The status of this search parameter. Enables tracking the life-
        cycle of the content.
        Type `str`. """
        
        self.experimental = None
        """ For testing purposes, not real usage.
        Type `bool`. """
        
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
        """ Natural language description of the search parameter.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for search parameter (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.purpose = None
        """ Why this search parameter is defined.
        Type `str`. """
        
        self.code = None
        """ Code used in URL.
        Type `str`. """
        
        self.base = None
        """ The base resource type(s) that this search parameter can be used
        against.
        List of `str` items. """
        
        self.type = None
        """ The type of value that a search parameter may contain, and how the
        content is interpreted.
        Type `str`. """
        
        self.expression = None
        """ FHIRPath expression that extracts the values.
        Type `str`. """
        
        self.xpath = None
        """ XPath that extracts the values.
        Type `str`. """
        
        self.xpathUsage = None
        """ How the search parameter relates to the set of elements returned by
        evaluating the xpath query.
        Type `str`. """
        
        self.target = None
        """ Types of resource (if a resource is referenced).
        List of `str` items. """
        
        self.multipleOr = None
        """ Allow multiple values per parameter (or).
        Type `bool`. """
        
        self.multipleAnd = None
        """ Allow multiple parameters (and).
        Type `bool`. """
        
        self.comparator = None
        """ Comparators supported for the search parameter.
        List of `str` items. """
        
        self.modifier = None
        """ A modifier supported for the search parameter.
        List of `str` items. """
        
        self.chain = None
        """ Chained names supported.
        List of `str` items. """
        
        self.component = None
        """ For Composite resources to define the parts.
        List of `SearchParameterComponent` items (represented as `dict` in JSON). """
        
        super(SearchParameter, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SearchParameter, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, True),
            ("version", "version", str, False, None, False),
            ("name", "name", str, False, None, True),
            ("derivedFrom", "derivedFrom", str, False, None, False),
            ("status", "status", str, False, None, True),
            ("experimental", "experimental", bool, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("publisher", "publisher", str, False, None, False),
            ("contact", "contact", contactdetail.ContactDetail, True, None, False),
            ("description", "description", str, False, None, True),
            ("useContext", "useContext", usagecontext.UsageContext, True, None, False),
            ("jurisdiction", "jurisdiction", codeableconcept.CodeableConcept, True, None, False),
            ("purpose", "purpose", str, False, None, False),
            ("code", "code", str, False, None, True),
            ("base", "base", str, True, None, True),
            ("type", "type", str, False, None, True),
            ("expression", "expression", str, False, None, False),
            ("xpath", "xpath", str, False, None, False),
            ("xpathUsage", "xpathUsage", str, False, None, False),
            ("target", "target", str, True, None, False),
            ("multipleOr", "multipleOr", bool, False, None, False),
            ("multipleAnd", "multipleAnd", bool, False, None, False),
            ("comparator", "comparator", str, True, None, False),
            ("modifier", "modifier", str, True, None, False),
            ("chain", "chain", str, True, None, False),
            ("component", "component", SearchParameterComponent, True, None, False),
        ])
        return js


from . import backboneelement

class SearchParameterComponent(backboneelement.BackboneElement):
    """ For Composite resources to define the parts.
    
    Used to define the parts of a composite search parameter.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['definition'] = """Defines how the part works."""
    _attribute_docstrings['expression'] = """Subexpression relative to main expression."""

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
        
        self.definition = None
        """ Defines how the part works.
        Type `str`. """
        
        self.expression = None
        """ Subexpression relative to main expression.
        Type `str`. """
        
        super(SearchParameterComponent, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SearchParameterComponent, self).elementProperties()
        js.extend([
            ("definition", "definition", str, False, None, True),
            ("expression", "expression", str, False, None, True),
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
    from . import fhirdate
except ImportError:
    fhirdate = sys.modules[__package__ + '.fhirdate']
try:
    from . import usagecontext
except ImportError:
    usagecontext = sys.modules[__package__ + '.usagecontext']
