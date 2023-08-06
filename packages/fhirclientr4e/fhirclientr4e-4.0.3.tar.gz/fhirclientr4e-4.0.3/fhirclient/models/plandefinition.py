#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/PlanDefinition) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class PlanDefinition(domainresource.DomainResource):
    """ The definition of a plan for a series of actions, independent of any
    specific patient or context.
    
    This resource allows for the definition of various types of plans as a
    sharable, consumable, and executable artifact. The resource is general
    enough to support the description of a broad range of clinical artifacts
    such as clinical decision support rules, order sets and protocols.
    """
    
    resource_type = "PlanDefinition"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['url'] = """Canonical identifier for this plan definition, represented as a URI (globally unique)."""
    _attribute_docstrings['identifier'] = """Additional identifier for the plan definition."""
    _attribute_docstrings['version'] = """Business version of the plan definition."""
    _attribute_docstrings['name'] = """Name for this plan definition (computer friendly)."""
    _attribute_docstrings['title'] = """Name for this plan definition (human friendly)."""
    _attribute_docstrings['subtitle'] = """Subordinate title of the plan definition."""
    _attribute_docstrings['type'] = """A high-level category for the plan definition that distinguishes the kinds of systems that would be interested in the plan definition."""
    _attribute_docstrings['status'] = """The status of this plan definition. Enables tracking the life-cycle of the content."""
    _attribute_docstrings['experimental'] = """For testing purposes, not real usage."""
    _attribute_docstrings['subjectCodeableConcept'] = """A code or group definition that describes the intended subject of the plan definition."""
    _attribute_docstrings['subjectReference'] = """Type of individual the plan definition is focused on."""
    _attribute_docstrings['date'] = """Date last changed."""
    _attribute_docstrings['publisher'] = """Name of the publisher (organization or individual)."""
    _attribute_docstrings['contact'] = """Contact details for the publisher."""
    _attribute_docstrings['description'] = """Natural language description of the plan definition."""
    _attribute_docstrings['useContext'] = """The context that the content is intended to support."""
    _attribute_docstrings['jurisdiction'] = """Intended jurisdiction for plan definition (if applicable)."""
    _attribute_docstrings['purpose'] = """Why this plan definition is defined."""
    _attribute_docstrings['usage'] = """Describes the clinical usage of the plan."""
    _attribute_docstrings['copyright'] = """Use and/or publishing restrictions."""
    _attribute_docstrings['approvalDate'] = """When the plan definition was approved by publisher."""
    _attribute_docstrings['lastReviewDate'] = """When the plan definition was last reviewed."""
    _attribute_docstrings['effectivePeriod'] = """When the plan definition is expected to be used."""
    _attribute_docstrings['topic'] = """Descriptive topics related to the content of the plan definition. Topics provide a high-level categorization of the definition that can be useful for filtering and searching."""
    _attribute_docstrings['author'] = """Who authored the content."""
    _attribute_docstrings['editor'] = """Who edited the content."""
    _attribute_docstrings['reviewer'] = """Who reviewed the content."""
    _attribute_docstrings['endorser'] = """Who endorsed the content."""
    _attribute_docstrings['relatedArtifact'] = """Additional documentation, citations."""
    _attribute_docstrings['library'] = """Logic used by the plan definition."""
    _attribute_docstrings['goal'] = """What the plan is trying to accomplish."""
    _attribute_docstrings['action'] = """Action defined by the plan."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/plan-definition-type',
        'restricted_to': ['order-set', 'clinical-protocol', 'eca-rule', 'workflow-definition'],
        'binding_strength': 'extensible',
        'class_name': 'CodeableConcept'
    }
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
        """ Canonical identifier for this plan definition, represented as a URI
        (globally unique).
        Type `str`. """
        
        self.identifier = None
        """ Additional identifier for the plan definition.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.version = None
        """ Business version of the plan definition.
        Type `str`. """
        
        self.name = None
        """ Name for this plan definition (computer friendly).
        Type `str`. """
        
        self.title = None
        """ Name for this plan definition (human friendly).
        Type `str`. """
        
        self.subtitle = None
        """ Subordinate title of the plan definition.
        Type `str`. """
        
        self.type = None
        """ A high-level category for the plan definition that distinguishes
        the kinds of systems that would be interested in the plan
        definition.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.status = None
        """ The status of this plan definition. Enables tracking the life-cycle
        of the content.
        Type `str`. """
        
        self.experimental = None
        """ For testing purposes, not real usage.
        Type `bool`. """
        
        self.subjectCodeableConcept = None
        """ A code or group definition that describes the intended subject of
        the plan definition.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subjectReference = None
        """ Type of individual the plan definition is focused on.
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
        """ Natural language description of the plan definition.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for plan definition (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.purpose = None
        """ Why this plan definition is defined.
        Type `str`. """
        
        self.usage = None
        """ Describes the clinical usage of the plan.
        Type `str`. """
        
        self.copyright = None
        """ Use and/or publishing restrictions.
        Type `str`. """
        
        self.approvalDate = None
        """ When the plan definition was approved by publisher.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.lastReviewDate = None
        """ When the plan definition was last reviewed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.effectivePeriod = None
        """ When the plan definition is expected to be used.
        Type `Period` (represented as `dict` in JSON). """
        
        self.topic = None
        """ Descriptive topics related to the content of the plan definition.
        Topics provide a high-level categorization of the definition that
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
        """ Additional documentation, citations.
        List of `RelatedArtifact` items (represented as `dict` in JSON). """
        
        self.library = None
        """ Logic used by the plan definition.
        List of `str` items. """
        
        self.goal = None
        """ What the plan is trying to accomplish.
        List of `PlanDefinitionGoal` items (represented as `dict` in JSON). """
        
        self.action = None
        """ Action defined by the plan.
        List of `PlanDefinitionAction` items (represented as `dict` in JSON). """
        
        super(PlanDefinition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PlanDefinition, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("version", "version", str, False, None, False),
            ("name", "name", str, False, None, False),
            ("title", "title", str, False, None, False),
            ("subtitle", "subtitle", str, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
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
            ("goal", "goal", PlanDefinitionGoal, True, None, False),
            ("action", "action", PlanDefinitionAction, True, None, False),
        ])
        return js


from . import backboneelement

class PlanDefinitionAction(backboneelement.BackboneElement):
    """ Action defined by the plan.
    
    An action or group of actions to be taken as part of the plan.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['prefix'] = """User-visible prefix for the action (e.g. 1. or A.)."""
    _attribute_docstrings['title'] = """User-visible title."""
    _attribute_docstrings['description'] = """Brief description of the action."""
    _attribute_docstrings['textEquivalent'] = """Static text equivalent of the action, used if the dynamic aspects cannot be interpreted by the receiving system."""
    _attribute_docstrings['priority'] = """Indicates how quickly the action should be addressed with respect to other actions."""
    _attribute_docstrings['code'] = """Code representing the meaning of the action or sub-actions."""
    _attribute_docstrings['reason'] = """Why the action should be performed."""
    _attribute_docstrings['documentation'] = """Supporting documentation for the intended performer of the action."""
    _attribute_docstrings['goalId'] = """What goals this action supports."""
    _attribute_docstrings['subjectCodeableConcept'] = """A code or group definition that describes the intended subject of the action and its children, if any."""
    _attribute_docstrings['subjectReference'] = """Type of individual the action is focused on."""
    _attribute_docstrings['trigger'] = """When the action should be triggered."""
    _attribute_docstrings['condition'] = """Whether or not the action is applicable."""
    _attribute_docstrings['input'] = """Input data requirements."""
    _attribute_docstrings['output'] = """Output data definition."""
    _attribute_docstrings['relatedAction'] = """Relationship to another action."""
    _attribute_docstrings['timingDateTime'] = """When the action should take place."""
    _attribute_docstrings['timingAge'] = """When the action should take place."""
    _attribute_docstrings['timingPeriod'] = """When the action should take place."""
    _attribute_docstrings['timingDuration'] = """When the action should take place."""
    _attribute_docstrings['timingRange'] = """When the action should take place."""
    _attribute_docstrings['timingTiming'] = """When the action should take place."""
    _attribute_docstrings['participant'] = """Who should participate in the action."""
    _attribute_docstrings['type'] = """The type of action to perform (create, update, remove)."""
    _attribute_docstrings['groupingBehavior'] = """Defines the grouping behavior for the action and its children."""
    _attribute_docstrings['selectionBehavior'] = """Defines the selection behavior for the action and its children."""
    _attribute_docstrings['requiredBehavior'] = """Defines the required behavior for the action."""
    _attribute_docstrings['precheckBehavior'] = """Defines whether the action should usually be preselected."""
    _attribute_docstrings['cardinalityBehavior'] = """Defines whether the action can be selected multiple times."""
    _attribute_docstrings['definitionCanonical'] = """Description of the activity to be performed."""
    _attribute_docstrings['definitionUri'] = """Description of the activity to be performed."""
    _attribute_docstrings['transform'] = """Transform to apply the template."""
    _attribute_docstrings['dynamicValue'] = """Dynamic aspects of the definition."""
    _attribute_docstrings['action'] = """A sub-action."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['priority'] = {
        'url': 'http://hl7.org/fhir/request-priority',
        'restricted_to': ['routine', 'urgent', 'asap', 'stat'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['subjectCodeableConcept'] = {
        'url': 'http://hl7.org/fhir/resource-types',
        'restricted_to': ['Account', 'ActivityDefinition', 'AdverseEvent', 'AllergyIntolerance', 'Appointment', 'AppointmentResponse', 'AuditEvent', 'Basic', 'Binary', 'BiologicallyDerivedProduct', 'BodyStructure', 'Bundle', 'CapabilityStatement', 'CarePlan', 'CareTeam', 'CatalogEntry', 'ChargeItem', 'ChargeItemDefinition', 'Claim', 'ClaimResponse', 'ClinicalImpression', 'CodeSystem', 'Communication', 'CommunicationRequest', 'CompartmentDefinition', 'Composition', 'ConceptMap', 'Condition', 'Consent', 'Contract', 'Coverage', 'CoverageEligibilityRequest', 'CoverageEligibilityResponse', 'DetectedIssue', 'Device', 'DeviceDefinition', 'DeviceMetric', 'DeviceRequest', 'DeviceUseStatement', 'DiagnosticReport', 'DocumentManifest', 'DocumentReference', 'DomainResource', 'EffectEvidenceSynthesis', 'Encounter', 'Endpoint', 'EnrollmentRequest', 'EnrollmentResponse', 'EpisodeOfCare', 'EventDefinition', 'Evidence', 'EvidenceVariable', 'ExampleScenario', 'ExplanationOfBenefit', 'FamilyMemberHistory', 'Flag', 'Goal', 'GraphDefinition', 'Group', 'GuidanceResponse', 'HealthcareService', 'ImagingStudy', 'Immunization', 'ImmunizationEvaluation', 'ImmunizationRecommendation', 'ImplementationGuide', 'InsurancePlan', 'Invoice', 'Library', 'Linkage', 'List', 'Location', 'Measure', 'MeasureReport', 'Media', 'Medication', 'MedicationAdministration', 'MedicationDispense', 'MedicationKnowledge', 'MedicationRequest', 'MedicationStatement', 'MedicinalProduct', 'MedicinalProductAuthorization', 'MedicinalProductContraindication', 'MedicinalProductIndication', 'MedicinalProductIngredient', 'MedicinalProductInteraction', 'MedicinalProductManufactured', 'MedicinalProductPackaged', 'MedicinalProductPharmaceutical', 'MedicinalProductUndesirableEffect', 'MessageDefinition', 'MessageHeader', 'MolecularSequence', 'NamingSystem', 'NutritionOrder', 'Observation', 'ObservationDefinition', 'OperationDefinition', 'OperationOutcome', 'Organization', 'OrganizationAffiliation', 'Parameters', 'Patient', 'PaymentNotice', 'PaymentReconciliation', 'Person', 'PlanDefinition', 'Practitioner', 'PractitionerRole', 'Procedure', 'Provenance', 'Questionnaire', 'QuestionnaireResponse', 'RelatedPerson', 'RequestGroup', 'ResearchDefinition', 'ResearchElementDefinition', 'ResearchStudy', 'ResearchSubject', 'Resource', 'RiskAssessment', 'RiskEvidenceSynthesis', 'Schedule', 'SearchParameter', 'ServiceRequest', 'Slot', 'Specimen', 'SpecimenDefinition', 'StructureDefinition', 'StructureMap', 'Subscription', 'Substance', 'SubstanceNucleicAcid', 'SubstancePolymer', 'SubstanceProtein', 'SubstanceReferenceInformation', 'SubstanceSourceMaterial', 'SubstanceSpecification', 'SupplyDelivery', 'SupplyRequest', 'Task', 'TerminologyCapabilities', 'TestReport', 'TestScript', 'ValueSet', 'VerificationResult', 'VisionPrescription'],
        'binding_strength': 'extensible',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/action-type',
        'restricted_to': ['create', 'update', 'remove', 'fire-event'],
        'binding_strength': 'extensible',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['groupingBehavior'] = {
        'url': 'http://hl7.org/fhir/action-grouping-behavior',
        'restricted_to': ['visual-group', 'logical-group', 'sentence-group'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['selectionBehavior'] = {
        'url': 'http://hl7.org/fhir/action-selection-behavior',
        'restricted_to': ['any', 'all', 'all-or-none', 'exactly-one', 'at-most-one', 'one-or-more'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['requiredBehavior'] = {
        'url': 'http://hl7.org/fhir/action-required-behavior',
        'restricted_to': ['must', 'could', 'must-unless-documented'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['precheckBehavior'] = {
        'url': 'http://hl7.org/fhir/action-precheck-behavior',
        'restricted_to': ['yes', 'no'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['cardinalityBehavior'] = {
        'url': 'http://hl7.org/fhir/action-cardinality-behavior',
        'restricted_to': ['single', 'multiple'],
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
        
        self.prefix = None
        """ User-visible prefix for the action (e.g. 1. or A.).
        Type `str`. """
        
        self.title = None
        """ User-visible title.
        Type `str`. """
        
        self.description = None
        """ Brief description of the action.
        Type `str`. """
        
        self.textEquivalent = None
        """ Static text equivalent of the action, used if the dynamic aspects
        cannot be interpreted by the receiving system.
        Type `str`. """
        
        self.priority = None
        """ Indicates how quickly the action should be addressed with respect
        to other actions.
        Type `str`. """
        
        self.code = None
        """ Code representing the meaning of the action or sub-actions.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.reason = None
        """ Why the action should be performed.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.documentation = None
        """ Supporting documentation for the intended performer of the action.
        List of `RelatedArtifact` items (represented as `dict` in JSON). """
        
        self.goalId = None
        """ What goals this action supports.
        List of `str` items. """
        
        self.subjectCodeableConcept = None
        """ A code or group definition that describes the intended subject of
        the action and its children, if any.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subjectReference = None
        """ Type of individual the action is focused on.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.trigger = None
        """ When the action should be triggered.
        List of `TriggerDefinition` items (represented as `dict` in JSON). """
        
        self.condition = None
        """ Whether or not the action is applicable.
        List of `PlanDefinitionActionCondition` items (represented as `dict` in JSON). """
        
        self.input = None
        """ Input data requirements.
        List of `DataRequirement` items (represented as `dict` in JSON). """
        
        self.output = None
        """ Output data definition.
        List of `DataRequirement` items (represented as `dict` in JSON). """
        
        self.relatedAction = None
        """ Relationship to another action.
        List of `PlanDefinitionActionRelatedAction` items (represented as `dict` in JSON). """
        
        self.timingDateTime = None
        """ When the action should take place.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.timingAge = None
        """ When the action should take place.
        Type `Age` (represented as `dict` in JSON). """
        
        self.timingPeriod = None
        """ When the action should take place.
        Type `Period` (represented as `dict` in JSON). """
        
        self.timingDuration = None
        """ When the action should take place.
        Type `Duration` (represented as `dict` in JSON). """
        
        self.timingRange = None
        """ When the action should take place.
        Type `Range` (represented as `dict` in JSON). """
        
        self.timingTiming = None
        """ When the action should take place.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.participant = None
        """ Who should participate in the action.
        List of `PlanDefinitionActionParticipant` items (represented as `dict` in JSON). """
        
        self.type = None
        """ The type of action to perform (create, update, remove).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.groupingBehavior = None
        """ Defines the grouping behavior for the action and its children.
        Type `str`. """
        
        self.selectionBehavior = None
        """ Defines the selection behavior for the action and its children.
        Type `str`. """
        
        self.requiredBehavior = None
        """ Defines the required behavior for the action.
        Type `str`. """
        
        self.precheckBehavior = None
        """ Defines whether the action should usually be preselected.
        Type `str`. """
        
        self.cardinalityBehavior = None
        """ Defines whether the action can be selected multiple times.
        Type `str`. """
        
        self.definitionCanonical = None
        """ Description of the activity to be performed.
        Type `str`. """
        
        self.definitionUri = None
        """ Description of the activity to be performed.
        Type `str`. """
        
        self.transform = None
        """ Transform to apply the template.
        Type `str`. """
        
        self.dynamicValue = None
        """ Dynamic aspects of the definition.
        List of `PlanDefinitionActionDynamicValue` items (represented as `dict` in JSON). """
        
        self.action = None
        """ A sub-action.
        List of `PlanDefinitionAction` items (represented as `dict` in JSON). """
        
        super(PlanDefinitionAction, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PlanDefinitionAction, self).elementProperties()
        js.extend([
            ("prefix", "prefix", str, False, None, False),
            ("title", "title", str, False, None, False),
            ("description", "description", str, False, None, False),
            ("textEquivalent", "textEquivalent", str, False, None, False),
            ("priority", "priority", str, False, None, False),
            ("code", "code", codeableconcept.CodeableConcept, True, None, False),
            ("reason", "reason", codeableconcept.CodeableConcept, True, None, False),
            ("documentation", "documentation", relatedartifact.RelatedArtifact, True, None, False),
            ("goalId", "goalId", str, True, None, False),
            ("subjectCodeableConcept", "subjectCodeableConcept", codeableconcept.CodeableConcept, False, "subject", False),
            ("subjectReference", "subjectReference", fhirreference.FHIRReference, False, "subject", False),
            ("trigger", "trigger", triggerdefinition.TriggerDefinition, True, None, False),
            ("condition", "condition", PlanDefinitionActionCondition, True, None, False),
            ("input", "input", datarequirement.DataRequirement, True, None, False),
            ("output", "output", datarequirement.DataRequirement, True, None, False),
            ("relatedAction", "relatedAction", PlanDefinitionActionRelatedAction, True, None, False),
            ("timingDateTime", "timingDateTime", fhirdate.FHIRDate, False, "timing", False),
            ("timingAge", "timingAge", age.Age, False, "timing", False),
            ("timingPeriod", "timingPeriod", period.Period, False, "timing", False),
            ("timingDuration", "timingDuration", duration.Duration, False, "timing", False),
            ("timingRange", "timingRange", range.Range, False, "timing", False),
            ("timingTiming", "timingTiming", timing.Timing, False, "timing", False),
            ("participant", "participant", PlanDefinitionActionParticipant, True, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("groupingBehavior", "groupingBehavior", str, False, None, False),
            ("selectionBehavior", "selectionBehavior", str, False, None, False),
            ("requiredBehavior", "requiredBehavior", str, False, None, False),
            ("precheckBehavior", "precheckBehavior", str, False, None, False),
            ("cardinalityBehavior", "cardinalityBehavior", str, False, None, False),
            ("definitionCanonical", "definitionCanonical", str, False, "definition", False),
            ("definitionUri", "definitionUri", str, False, "definition", False),
            ("transform", "transform", str, False, None, False),
            ("dynamicValue", "dynamicValue", PlanDefinitionActionDynamicValue, True, None, False),
            ("action", "action", PlanDefinitionAction, True, None, False),
        ])
        return js


class PlanDefinitionActionCondition(backboneelement.BackboneElement):
    """ Whether or not the action is applicable.
    
    An expression that describes applicability criteria or start/stop
    conditions for the action.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['kind'] = """The kind of condition."""
    _attribute_docstrings['expression'] = """Boolean-valued expression."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['kind'] = {
        'url': 'http://hl7.org/fhir/action-condition-kind',
        'restricted_to': ['applicability', 'start', 'stop'],
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
        
        self.kind = None
        """ The kind of condition.
        Type `str`. """
        
        self.expression = None
        """ Boolean-valued expression.
        Type `Expression` (represented as `dict` in JSON). """
        
        super(PlanDefinitionActionCondition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PlanDefinitionActionCondition, self).elementProperties()
        js.extend([
            ("kind", "kind", str, False, None, True),
            ("expression", "expression", expression.Expression, False, None, False),
        ])
        return js


class PlanDefinitionActionDynamicValue(backboneelement.BackboneElement):
    """ Dynamic aspects of the definition.
    
    Customizations that should be applied to the statically defined resource.
    For example, if the dosage of a medication must be computed based on the
    patient's weight, a customization would be used to specify an expression
    that calculated the weight, and the path on the resource that would contain
    the result.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['path'] = """The path to the element to be set dynamically."""
    _attribute_docstrings['expression'] = """An expression that provides the dynamic value for the customization."""

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
        """ The path to the element to be set dynamically.
        Type `str`. """
        
        self.expression = None
        """ An expression that provides the dynamic value for the customization.
        Type `Expression` (represented as `dict` in JSON). """
        
        super(PlanDefinitionActionDynamicValue, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PlanDefinitionActionDynamicValue, self).elementProperties()
        js.extend([
            ("path", "path", str, False, None, False),
            ("expression", "expression", expression.Expression, False, None, False),
        ])
        return js


class PlanDefinitionActionParticipant(backboneelement.BackboneElement):
    """ Who should participate in the action.
    
    Indicates who should participate in performing the action described.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """The type of participant in the action."""
    _attribute_docstrings['role'] = """E.g. Nurse, Surgeon, Parent."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://hl7.org/fhir/action-participant-type',
        'restricted_to': ['patient', 'practitioner', 'related-person', 'device'],
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
        """ The type of participant in the action.
        Type `str`. """
        
        self.role = None
        """ E.g. Nurse, Surgeon, Parent.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(PlanDefinitionActionParticipant, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PlanDefinitionActionParticipant, self).elementProperties()
        js.extend([
            ("type", "type", str, False, None, True),
            ("role", "role", codeableconcept.CodeableConcept, False, None, False),
        ])
        return js


class PlanDefinitionActionRelatedAction(backboneelement.BackboneElement):
    """ Relationship to another action.
    
    A relationship to another action such as "before" or "30-60 minutes after
    start of".
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['actionId'] = """What action is this related to."""
    _attribute_docstrings['relationship'] = """The relationship of this action to the related action."""
    _attribute_docstrings['offsetDuration'] = """Time offset for the relationship."""
    _attribute_docstrings['offsetRange'] = """Time offset for the relationship."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['relationship'] = {
        'url': 'http://hl7.org/fhir/action-relationship-type',
        'restricted_to': ['before-start', 'before', 'before-end', 'concurrent-with-start', 'concurrent', 'concurrent-with-end', 'after-start', 'after', 'after-end'],
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
        
        self.actionId = None
        """ What action is this related to.
        Type `str`. """
        
        self.relationship = None
        """ The relationship of this action to the related action.
        Type `str`. """
        
        self.offsetDuration = None
        """ Time offset for the relationship.
        Type `Duration` (represented as `dict` in JSON). """
        
        self.offsetRange = None
        """ Time offset for the relationship.
        Type `Range` (represented as `dict` in JSON). """
        
        super(PlanDefinitionActionRelatedAction, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PlanDefinitionActionRelatedAction, self).elementProperties()
        js.extend([
            ("actionId", "actionId", str, False, None, True),
            ("relationship", "relationship", str, False, None, True),
            ("offsetDuration", "offsetDuration", duration.Duration, False, "offset", False),
            ("offsetRange", "offsetRange", range.Range, False, "offset", False),
        ])
        return js


class PlanDefinitionGoal(backboneelement.BackboneElement):
    """ What the plan is trying to accomplish.
    
    Goals that describe what the activities within the plan are intended to
    achieve. For example, weight loss, restoring an activity of daily living,
    obtaining herd immunity via immunization, meeting a process improvement
    objective, etc.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['category'] = """Indicates a category the goal falls within."""
    _attribute_docstrings['description'] = """Code or text describing the goal."""
    _attribute_docstrings['priority'] = """Identifies the expected level of importance associated with reaching/sustaining the defined goal."""
    _attribute_docstrings['start'] = """When goal pursuit begins."""
    _attribute_docstrings['addresses'] = """What does the goal address."""
    _attribute_docstrings['documentation'] = """Supporting documentation for the goal."""
    _attribute_docstrings['target'] = """Target outcome for the goal."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['category'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/goal-category',
        'restricted_to': ['dietary', 'safety', 'behavioral', 'nursing', 'physiotherapy'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['priority'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/goal-priority',
        'restricted_to': ['high-priority', 'medium-priority', 'low-priority'],
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
        
        self.category = None
        """ Indicates a category the goal falls within.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.description = None
        """ Code or text describing the goal.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.priority = None
        """ Identifies the expected level of importance associated with
        reaching/sustaining the defined goal.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.start = None
        """ When goal pursuit begins.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.addresses = None
        """ What does the goal address.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.documentation = None
        """ Supporting documentation for the goal.
        List of `RelatedArtifact` items (represented as `dict` in JSON). """
        
        self.target = None
        """ Target outcome for the goal.
        List of `PlanDefinitionGoalTarget` items (represented as `dict` in JSON). """
        
        super(PlanDefinitionGoal, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PlanDefinitionGoal, self).elementProperties()
        js.extend([
            ("category", "category", codeableconcept.CodeableConcept, False, None, False),
            ("description", "description", codeableconcept.CodeableConcept, False, None, True),
            ("priority", "priority", codeableconcept.CodeableConcept, False, None, False),
            ("start", "start", codeableconcept.CodeableConcept, False, None, False),
            ("addresses", "addresses", codeableconcept.CodeableConcept, True, None, False),
            ("documentation", "documentation", relatedartifact.RelatedArtifact, True, None, False),
            ("target", "target", PlanDefinitionGoalTarget, True, None, False),
        ])
        return js


class PlanDefinitionGoalTarget(backboneelement.BackboneElement):
    """ Target outcome for the goal.
    
    Indicates what should be done and within what timeframe.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['measure'] = """The parameter whose value is to be tracked."""
    _attribute_docstrings['detailQuantity'] = """The target value to be achieved."""
    _attribute_docstrings['detailRange'] = """The target value to be achieved."""
    _attribute_docstrings['detailCodeableConcept'] = """The target value to be achieved."""
    _attribute_docstrings['due'] = """Reach goal within."""

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
        
        self.measure = None
        """ The parameter whose value is to be tracked.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.detailQuantity = None
        """ The target value to be achieved.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.detailRange = None
        """ The target value to be achieved.
        Type `Range` (represented as `dict` in JSON). """
        
        self.detailCodeableConcept = None
        """ The target value to be achieved.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.due = None
        """ Reach goal within.
        Type `Duration` (represented as `dict` in JSON). """
        
        super(PlanDefinitionGoalTarget, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PlanDefinitionGoalTarget, self).elementProperties()
        js.extend([
            ("measure", "measure", codeableconcept.CodeableConcept, False, None, False),
            ("detailQuantity", "detailQuantity", quantity.Quantity, False, "detail", False),
            ("detailRange", "detailRange", range.Range, False, "detail", False),
            ("detailCodeableConcept", "detailCodeableConcept", codeableconcept.CodeableConcept, False, "detail", False),
            ("due", "due", duration.Duration, False, None, False),
        ])
        return js


import sys
try:
    from . import age
except ImportError:
    age = sys.modules[__package__ + '.age']
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
    from . import quantity
except ImportError:
    quantity = sys.modules[__package__ + '.quantity']
try:
    from . import range
except ImportError:
    range = sys.modules[__package__ + '.range']
try:
    from . import relatedartifact
except ImportError:
    relatedartifact = sys.modules[__package__ + '.relatedartifact']
try:
    from . import timing
except ImportError:
    timing = sys.modules[__package__ + '.timing']
try:
    from . import triggerdefinition
except ImportError:
    triggerdefinition = sys.modules[__package__ + '.triggerdefinition']
try:
    from . import usagecontext
except ImportError:
    usagecontext = sys.modules[__package__ + '.usagecontext']
