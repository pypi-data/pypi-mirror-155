#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/GraphDefinition) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class GraphDefinition(domainresource.DomainResource):
    """ Definition of a graph of resources.
    
    A formal computable definition of a graph of resources - that is, a
    coherent set of resources that form a graph by following references. The
    Graph Definition resource defines a set and makes rules about the set.
    """
    
    resource_type = "GraphDefinition"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['url'] = """Canonical identifier for this graph definition, represented as a URI (globally unique)."""
    _attribute_docstrings['version'] = """Business version of the graph definition."""
    _attribute_docstrings['name'] = """Name for this graph definition (computer friendly)."""
    _attribute_docstrings['status'] = """The status of this graph definition. Enables tracking the life-cycle of the content."""
    _attribute_docstrings['experimental'] = """For testing purposes, not real usage."""
    _attribute_docstrings['date'] = """Date last changed."""
    _attribute_docstrings['publisher'] = """Name of the publisher (organization or individual)."""
    _attribute_docstrings['contact'] = """Contact details for the publisher."""
    _attribute_docstrings['description'] = """Natural language description of the graph definition."""
    _attribute_docstrings['useContext'] = """The context that the content is intended to support."""
    _attribute_docstrings['jurisdiction'] = """Intended jurisdiction for graph definition (if applicable)."""
    _attribute_docstrings['purpose'] = """Why this graph definition is defined."""
    _attribute_docstrings['start'] = """The type of FHIR resource at which instances of this graph start."""
    _attribute_docstrings['profile'] = """Profile on base resource."""
    _attribute_docstrings['link'] = """Links this graph makes rules about."""

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
    _attribute_enums['start'] = {
        'url': 'http://hl7.org/fhir/resource-types',
        'restricted_to': ['Account', 'ActivityDefinition', 'AdverseEvent', 'AllergyIntolerance', 'Appointment', 'AppointmentResponse', 'AuditEvent', 'Basic', 'Binary', 'BiologicallyDerivedProduct', 'BodyStructure', 'Bundle', 'CapabilityStatement', 'CarePlan', 'CareTeam', 'CatalogEntry', 'ChargeItem', 'ChargeItemDefinition', 'Claim', 'ClaimResponse', 'ClinicalImpression', 'CodeSystem', 'Communication', 'CommunicationRequest', 'CompartmentDefinition', 'Composition', 'ConceptMap', 'Condition', 'Consent', 'Contract', 'Coverage', 'CoverageEligibilityRequest', 'CoverageEligibilityResponse', 'DetectedIssue', 'Device', 'DeviceDefinition', 'DeviceMetric', 'DeviceRequest', 'DeviceUseStatement', 'DiagnosticReport', 'DocumentManifest', 'DocumentReference', 'DomainResource', 'EffectEvidenceSynthesis', 'Encounter', 'Endpoint', 'EnrollmentRequest', 'EnrollmentResponse', 'EpisodeOfCare', 'EventDefinition', 'Evidence', 'EvidenceVariable', 'ExampleScenario', 'ExplanationOfBenefit', 'FamilyMemberHistory', 'Flag', 'Goal', 'GraphDefinition', 'Group', 'GuidanceResponse', 'HealthcareService', 'ImagingStudy', 'Immunization', 'ImmunizationEvaluation', 'ImmunizationRecommendation', 'ImplementationGuide', 'InsurancePlan', 'Invoice', 'Library', 'Linkage', 'List', 'Location', 'Measure', 'MeasureReport', 'Media', 'Medication', 'MedicationAdministration', 'MedicationDispense', 'MedicationKnowledge', 'MedicationRequest', 'MedicationStatement', 'MedicinalProduct', 'MedicinalProductAuthorization', 'MedicinalProductContraindication', 'MedicinalProductIndication', 'MedicinalProductIngredient', 'MedicinalProductInteraction', 'MedicinalProductManufactured', 'MedicinalProductPackaged', 'MedicinalProductPharmaceutical', 'MedicinalProductUndesirableEffect', 'MessageDefinition', 'MessageHeader', 'MolecularSequence', 'NamingSystem', 'NutritionOrder', 'Observation', 'ObservationDefinition', 'OperationDefinition', 'OperationOutcome', 'Organization', 'OrganizationAffiliation', 'Parameters', 'Patient', 'PaymentNotice', 'PaymentReconciliation', 'Person', 'PlanDefinition', 'Practitioner', 'PractitionerRole', 'Procedure', 'Provenance', 'Questionnaire', 'QuestionnaireResponse', 'RelatedPerson', 'RequestGroup', 'ResearchDefinition', 'ResearchElementDefinition', 'ResearchStudy', 'ResearchSubject', 'Resource', 'RiskAssessment', 'RiskEvidenceSynthesis', 'Schedule', 'SearchParameter', 'ServiceRequest', 'Slot', 'Specimen', 'SpecimenDefinition', 'StructureDefinition', 'StructureMap', 'Subscription', 'Substance', 'SubstanceNucleicAcid', 'SubstancePolymer', 'SubstanceProtein', 'SubstanceReferenceInformation', 'SubstanceSourceMaterial', 'SubstanceSpecification', 'SupplyDelivery', 'SupplyRequest', 'Task', 'TerminologyCapabilities', 'TestReport', 'TestScript', 'ValueSet', 'VerificationResult', 'VisionPrescription'],
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
        """ Canonical identifier for this graph definition, represented as a
        URI (globally unique).
        Type `str`. """
        
        self.version = None
        """ Business version of the graph definition.
        Type `str`. """
        
        self.name = None
        """ Name for this graph definition (computer friendly).
        Type `str`. """
        
        self.status = None
        """ The status of this graph definition. Enables tracking the life-
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
        """ Natural language description of the graph definition.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for graph definition (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.purpose = None
        """ Why this graph definition is defined.
        Type `str`. """
        
        self.start = None
        """ The type of FHIR resource at which instances of this graph start.
        Type `str`. """
        
        self.profile = None
        """ Profile on base resource.
        Type `str`. """
        
        self.link = None
        """ Links this graph makes rules about.
        List of `GraphDefinitionLink` items (represented as `dict` in JSON). """
        
        super(GraphDefinition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(GraphDefinition, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, False),
            ("version", "version", str, False, None, False),
            ("name", "name", str, False, None, True),
            ("status", "status", str, False, None, True),
            ("experimental", "experimental", bool, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("publisher", "publisher", str, False, None, False),
            ("contact", "contact", contactdetail.ContactDetail, True, None, False),
            ("description", "description", str, False, None, False),
            ("useContext", "useContext", usagecontext.UsageContext, True, None, False),
            ("jurisdiction", "jurisdiction", codeableconcept.CodeableConcept, True, None, False),
            ("purpose", "purpose", str, False, None, False),
            ("start", "start", str, False, None, True),
            ("profile", "profile", str, False, None, False),
            ("link", "link", GraphDefinitionLink, True, None, False),
        ])
        return js


from . import backboneelement

class GraphDefinitionLink(backboneelement.BackboneElement):
    """ Links this graph makes rules about.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['path'] = """Path in the resource that contains the link."""
    _attribute_docstrings['sliceName'] = """Which slice (if profiled)."""
    _attribute_docstrings['min'] = """Minimum occurrences for this link."""
    _attribute_docstrings['max'] = """Maximum occurrences for this link."""
    _attribute_docstrings['description'] = """Why this link is specified."""
    _attribute_docstrings['target'] = """Potential target for the link."""

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
        
        self.path = None
        """ Path in the resource that contains the link.
        Type `str`. """
        
        self.sliceName = None
        """ Which slice (if profiled).
        Type `str`. """
        
        self.min = None
        """ Minimum occurrences for this link.
        Type `int`. """
        
        self.max = None
        """ Maximum occurrences for this link.
        Type `str`. """
        
        self.description = None
        """ Why this link is specified.
        Type `str`. """
        
        self.target = None
        """ Potential target for the link.
        List of `GraphDefinitionLinkTarget` items (represented as `dict` in JSON). """
        
        super(GraphDefinitionLink, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(GraphDefinitionLink, self).elementProperties()
        js.extend([
            ("path", "path", str, False, None, False),
            ("sliceName", "sliceName", str, False, None, False),
            ("min", "min", int, False, None, False),
            ("max", "max", str, False, None, False),
            ("description", "description", str, False, None, False),
            ("target", "target", GraphDefinitionLinkTarget, True, None, False),
        ])
        return js


class GraphDefinitionLinkTarget(backboneelement.BackboneElement):
    """ Potential target for the link.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """None"""
    _attribute_docstrings['params'] = """Criteria for reverse lookup."""
    _attribute_docstrings['profile'] = """Profile for the target resource."""
    _attribute_docstrings['compartment'] = """Compartment Consistency Rules."""
    _attribute_docstrings['link'] = """Additional links from target resource."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://hl7.org/fhir/resource-types',
        'restricted_to': ['Account', 'ActivityDefinition', 'AdverseEvent', 'AllergyIntolerance', 'Appointment', 'AppointmentResponse', 'AuditEvent', 'Basic', 'Binary', 'BiologicallyDerivedProduct', 'BodyStructure', 'Bundle', 'CapabilityStatement', 'CarePlan', 'CareTeam', 'CatalogEntry', 'ChargeItem', 'ChargeItemDefinition', 'Claim', 'ClaimResponse', 'ClinicalImpression', 'CodeSystem', 'Communication', 'CommunicationRequest', 'CompartmentDefinition', 'Composition', 'ConceptMap', 'Condition', 'Consent', 'Contract', 'Coverage', 'CoverageEligibilityRequest', 'CoverageEligibilityResponse', 'DetectedIssue', 'Device', 'DeviceDefinition', 'DeviceMetric', 'DeviceRequest', 'DeviceUseStatement', 'DiagnosticReport', 'DocumentManifest', 'DocumentReference', 'DomainResource', 'EffectEvidenceSynthesis', 'Encounter', 'Endpoint', 'EnrollmentRequest', 'EnrollmentResponse', 'EpisodeOfCare', 'EventDefinition', 'Evidence', 'EvidenceVariable', 'ExampleScenario', 'ExplanationOfBenefit', 'FamilyMemberHistory', 'Flag', 'Goal', 'GraphDefinition', 'Group', 'GuidanceResponse', 'HealthcareService', 'ImagingStudy', 'Immunization', 'ImmunizationEvaluation', 'ImmunizationRecommendation', 'ImplementationGuide', 'InsurancePlan', 'Invoice', 'Library', 'Linkage', 'List', 'Location', 'Measure', 'MeasureReport', 'Media', 'Medication', 'MedicationAdministration', 'MedicationDispense', 'MedicationKnowledge', 'MedicationRequest', 'MedicationStatement', 'MedicinalProduct', 'MedicinalProductAuthorization', 'MedicinalProductContraindication', 'MedicinalProductIndication', 'MedicinalProductIngredient', 'MedicinalProductInteraction', 'MedicinalProductManufactured', 'MedicinalProductPackaged', 'MedicinalProductPharmaceutical', 'MedicinalProductUndesirableEffect', 'MessageDefinition', 'MessageHeader', 'MolecularSequence', 'NamingSystem', 'NutritionOrder', 'Observation', 'ObservationDefinition', 'OperationDefinition', 'OperationOutcome', 'Organization', 'OrganizationAffiliation', 'Parameters', 'Patient', 'PaymentNotice', 'PaymentReconciliation', 'Person', 'PlanDefinition', 'Practitioner', 'PractitionerRole', 'Procedure', 'Provenance', 'Questionnaire', 'QuestionnaireResponse', 'RelatedPerson', 'RequestGroup', 'ResearchDefinition', 'ResearchElementDefinition', 'ResearchStudy', 'ResearchSubject', 'Resource', 'RiskAssessment', 'RiskEvidenceSynthesis', 'Schedule', 'SearchParameter', 'ServiceRequest', 'Slot', 'Specimen', 'SpecimenDefinition', 'StructureDefinition', 'StructureMap', 'Subscription', 'Substance', 'SubstanceNucleicAcid', 'SubstancePolymer', 'SubstanceProtein', 'SubstanceReferenceInformation', 'SubstanceSourceMaterial', 'SubstanceSpecification', 'SupplyDelivery', 'SupplyRequest', 'Task', 'TerminologyCapabilities', 'TestReport', 'TestScript', 'ValueSet', 'VerificationResult', 'VisionPrescription'],
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
        """ None.
        Type `str`. """
        
        self.params = None
        """ Criteria for reverse lookup.
        Type `str`. """
        
        self.profile = None
        """ Profile for the target resource.
        Type `str`. """
        
        self.compartment = None
        """ Compartment Consistency Rules.
        List of `GraphDefinitionLinkTargetCompartment` items (represented as `dict` in JSON). """
        
        self.link = None
        """ Additional links from target resource.
        List of `GraphDefinitionLink` items (represented as `dict` in JSON). """
        
        super(GraphDefinitionLinkTarget, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(GraphDefinitionLinkTarget, self).elementProperties()
        js.extend([
            ("type", "type", str, False, None, True),
            ("params", "params", str, False, None, False),
            ("profile", "profile", str, False, None, False),
            ("compartment", "compartment", GraphDefinitionLinkTargetCompartment, True, None, False),
            ("link", "link", GraphDefinitionLink, True, None, False),
        ])
        return js


class GraphDefinitionLinkTargetCompartment(backboneelement.BackboneElement):
    """ Compartment Consistency Rules.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['use'] = """Defines how the compartment rule is used - whether it it is used to test whether resources are subject to the rule, or whether it is a rule that must be followed."""
    _attribute_docstrings['code'] = """Identifies the compartment."""
    _attribute_docstrings['rule'] = """identical | matching | different | no-rule | custom."""
    _attribute_docstrings['expression'] = """Custom rule, as a FHIRPath expression."""
    _attribute_docstrings['description'] = """Documentation for FHIRPath expression."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['use'] = {
        'url': 'http://hl7.org/fhir/graph-compartment-use',
        'restricted_to': ['condition', 'requirement'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['code'] = {
        'url': 'http://hl7.org/fhir/compartment-type',
        'restricted_to': ['Patient', 'Encounter', 'RelatedPerson', 'Practitioner', 'Device'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['rule'] = {
        'url': 'http://hl7.org/fhir/graph-compartment-rule',
        'restricted_to': ['identical', 'matching', 'different', 'custom'],
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
        
        self.use = None
        """ Defines how the compartment rule is used - whether it it is used to
        test whether resources are subject to the rule, or whether it is a
        rule that must be followed.
        Type `str`. """
        
        self.code = None
        """ Identifies the compartment.
        Type `str`. """
        
        self.rule = None
        """ identical | matching | different | no-rule | custom.
        Type `str`. """
        
        self.expression = None
        """ Custom rule, as a FHIRPath expression.
        Type `str`. """
        
        self.description = None
        """ Documentation for FHIRPath expression.
        Type `str`. """
        
        super(GraphDefinitionLinkTargetCompartment, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(GraphDefinitionLinkTargetCompartment, self).elementProperties()
        js.extend([
            ("use", "use", str, False, None, True),
            ("code", "code", str, False, None, True),
            ("rule", "rule", str, False, None, True),
            ("expression", "expression", str, False, None, False),
            ("description", "description", str, False, None, False),
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
