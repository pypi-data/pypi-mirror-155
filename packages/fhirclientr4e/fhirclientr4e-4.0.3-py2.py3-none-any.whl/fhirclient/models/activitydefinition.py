#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/ActivityDefinition) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class ActivityDefinition(domainresource.DomainResource):
    """ The definition of a specific activity to be taken, independent of any
    particular patient or context.
    
    This resource allows for the definition of some activity to be performed,
    independent of a particular patient, practitioner, or other performance
    context.
    """
    
    resource_type = "ActivityDefinition"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['url'] = """Canonical identifier for this activity definition, represented as a URI (globally unique)."""
    _attribute_docstrings['identifier'] = """Additional identifier for the activity definition."""
    _attribute_docstrings['version'] = """Business version of the activity definition."""
    _attribute_docstrings['name'] = """Name for this activity definition (computer friendly)."""
    _attribute_docstrings['title'] = """Name for this activity definition (human friendly)."""
    _attribute_docstrings['subtitle'] = """Subordinate title of the activity definition."""
    _attribute_docstrings['status'] = """The status of this activity definition. Enables tracking the life-cycle of the content."""
    _attribute_docstrings['experimental'] = """For testing purposes, not real usage."""
    _attribute_docstrings['subjectCodeableConcept'] = """A code or group definition that describes the intended subject of the activity being defined."""
    _attribute_docstrings['subjectReference'] = """Type of individual the activity definition is intended for."""
    _attribute_docstrings['date'] = """Date last changed."""
    _attribute_docstrings['publisher'] = """Name of the publisher (organization or individual)."""
    _attribute_docstrings['contact'] = """Contact details for the publisher."""
    _attribute_docstrings['description'] = """Natural language description of the activity definition."""
    _attribute_docstrings['useContext'] = """The context that the content is intended to support."""
    _attribute_docstrings['jurisdiction'] = """Intended jurisdiction for activity definition (if applicable)."""
    _attribute_docstrings['purpose'] = """Why this activity definition is defined."""
    _attribute_docstrings['usage'] = """Describes the clinical usage of the activity definition."""
    _attribute_docstrings['copyright'] = """Use and/or publishing restrictions."""
    _attribute_docstrings['approvalDate'] = """When the activity definition was approved by publisher."""
    _attribute_docstrings['lastReviewDate'] = """When the activity definition was last reviewed."""
    _attribute_docstrings['effectivePeriod'] = """When the activity definition is expected to be used."""
    _attribute_docstrings['topic'] = """Descriptive topics related to the content of the activity. Topics provide a high-level categorization of the activity that can be useful for filtering and searching."""
    _attribute_docstrings['author'] = """Who authored the content."""
    _attribute_docstrings['editor'] = """Who edited the content."""
    _attribute_docstrings['reviewer'] = """Who reviewed the content."""
    _attribute_docstrings['endorser'] = """Who endorsed the content."""
    _attribute_docstrings['relatedArtifact'] = """Additional documentation, citations, etc.."""
    _attribute_docstrings['library'] = """Logic used by the activity definition."""
    _attribute_docstrings['kind'] = """A description of the kind of resource the activity definition is representing. For example, a MedicationRequest, a ServiceRequest, or a CommunicationRequest. Typically, but not always, this is a Request resource."""
    _attribute_docstrings['profile'] = """What profile the resource needs to conform to."""
    _attribute_docstrings['code'] = """Detail type of activity."""
    _attribute_docstrings['intent'] = """Indicates the level of authority/intentionality associated with the activity and where the request should fit into the workflow chain."""
    _attribute_docstrings['priority'] = """Indicates how quickly the activity  should be addressed with respect to other requests."""
    _attribute_docstrings['doNotPerform'] = """True if the activity should not be performed."""
    _attribute_docstrings['timingTiming'] = """When activity is to occur."""
    _attribute_docstrings['timingDateTime'] = """When activity is to occur."""
    _attribute_docstrings['timingAge'] = """When activity is to occur."""
    _attribute_docstrings['timingPeriod'] = """When activity is to occur."""
    _attribute_docstrings['timingRange'] = """When activity is to occur."""
    _attribute_docstrings['timingDuration'] = """When activity is to occur."""
    _attribute_docstrings['location'] = """Where it should happen."""
    _attribute_docstrings['participant'] = """Who should participate in the action."""
    _attribute_docstrings['productReference'] = """What's administered/supplied."""
    _attribute_docstrings['productCodeableConcept'] = """What's administered/supplied."""
    _attribute_docstrings['quantity'] = """How much is administered/consumed/supplied."""
    _attribute_docstrings['dosage'] = """Detailed dosage instructions."""
    _attribute_docstrings['bodySite'] = """What part of body to perform on."""
    _attribute_docstrings['specimenRequirement'] = """What specimens are required to perform this action."""
    _attribute_docstrings['observationRequirement'] = """What observations are required to perform this action."""
    _attribute_docstrings['observationResultRequirement'] = """What observations must be produced by this action."""
    _attribute_docstrings['transform'] = """Transform to apply the template."""
    _attribute_docstrings['dynamicValue'] = """Dynamic aspects of the definition."""

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
    _attribute_enums['kind'] = {
        'url': 'http://hl7.org/fhir/request-resource-types',
        'restricted_to': ['Appointment', 'AppointmentResponse', 'CarePlan', 'Claim', 'CommunicationRequest', 'Contract', 'DeviceRequest', 'EnrollmentRequest', 'ImmunizationRecommendation', 'MedicationRequest', 'NutritionOrder', 'ServiceRequest', 'SupplyRequest', 'Task', 'VisionPrescription'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['intent'] = {
        'url': 'http://hl7.org/fhir/request-intent',
        'restricted_to': ['proposal', 'plan', 'directive', 'order', 'original-order', 'reflex-order', 'filler-order', 'instance-order', 'option'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['priority'] = {
        'url': 'http://hl7.org/fhir/request-priority',
        'restricted_to': ['routine', 'urgent', 'asap', 'stat'],
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
        """ Canonical identifier for this activity definition, represented as a
        URI (globally unique).
        Type `str`. """
        
        self.identifier = None
        """ Additional identifier for the activity definition.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.version = None
        """ Business version of the activity definition.
        Type `str`. """
        
        self.name = None
        """ Name for this activity definition (computer friendly).
        Type `str`. """
        
        self.title = None
        """ Name for this activity definition (human friendly).
        Type `str`. """
        
        self.subtitle = None
        """ Subordinate title of the activity definition.
        Type `str`. """
        
        self.status = None
        """ The status of this activity definition. Enables tracking the life-
        cycle of the content.
        Type `str`. """
        
        self.experimental = None
        """ For testing purposes, not real usage.
        Type `bool`. """
        
        self.subjectCodeableConcept = None
        """ A code or group definition that describes the intended subject of
        the activity being defined.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subjectReference = None
        """ Type of individual the activity definition is intended for.
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
        """ Natural language description of the activity definition.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for activity definition (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.purpose = None
        """ Why this activity definition is defined.
        Type `str`. """
        
        self.usage = None
        """ Describes the clinical usage of the activity definition.
        Type `str`. """
        
        self.copyright = None
        """ Use and/or publishing restrictions.
        Type `str`. """
        
        self.approvalDate = None
        """ When the activity definition was approved by publisher.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.lastReviewDate = None
        """ When the activity definition was last reviewed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.effectivePeriod = None
        """ When the activity definition is expected to be used.
        Type `Period` (represented as `dict` in JSON). """
        
        self.topic = None
        """ Descriptive topics related to the content of the activity. Topics
        provide a high-level categorization of the activity that can be
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
        
        self.library = None
        """ Logic used by the activity definition.
        List of `str` items. """
        
        self.kind = None
        """ A description of the kind of resource the activity definition is
        representing. For example, a MedicationRequest, a ServiceRequest,
        or a CommunicationRequest. Typically, but not always, this is a
        Request resource.
        Type `str`. """
        
        self.profile = None
        """ What profile the resource needs to conform to.
        Type `str`. """
        
        self.code = None
        """ Detail type of activity.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.intent = None
        """ Indicates the level of authority/intentionality associated with the
        activity and where the request should fit into the workflow chain.
        Type `str`. """
        
        self.priority = None
        """ Indicates how quickly the activity  should be addressed with
        respect to other requests.
        Type `str`. """
        
        self.doNotPerform = None
        """ True if the activity should not be performed.
        Type `bool`. """
        
        self.timingTiming = None
        """ When activity is to occur.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.timingDateTime = None
        """ When activity is to occur.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.timingAge = None
        """ When activity is to occur.
        Type `Age` (represented as `dict` in JSON). """
        
        self.timingPeriod = None
        """ When activity is to occur.
        Type `Period` (represented as `dict` in JSON). """
        
        self.timingRange = None
        """ When activity is to occur.
        Type `Range` (represented as `dict` in JSON). """
        
        self.timingDuration = None
        """ When activity is to occur.
        Type `Duration` (represented as `dict` in JSON). """
        
        self.location = None
        """ Where it should happen.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.participant = None
        """ Who should participate in the action.
        List of `ActivityDefinitionParticipant` items (represented as `dict` in JSON). """
        
        self.productReference = None
        """ What's administered/supplied.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.productCodeableConcept = None
        """ What's administered/supplied.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.quantity = None
        """ How much is administered/consumed/supplied.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.dosage = None
        """ Detailed dosage instructions.
        List of `Dosage` items (represented as `dict` in JSON). """
        
        self.bodySite = None
        """ What part of body to perform on.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.specimenRequirement = None
        """ What specimens are required to perform this action.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.observationRequirement = None
        """ What observations are required to perform this action.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.observationResultRequirement = None
        """ What observations must be produced by this action.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.transform = None
        """ Transform to apply the template.
        Type `str`. """
        
        self.dynamicValue = None
        """ Dynamic aspects of the definition.
        List of `ActivityDefinitionDynamicValue` items (represented as `dict` in JSON). """
        
        super(ActivityDefinition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ActivityDefinition, self).elementProperties()
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
            ("kind", "kind", str, False, None, False),
            ("profile", "profile", str, False, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("intent", "intent", str, False, None, False),
            ("priority", "priority", str, False, None, False),
            ("doNotPerform", "doNotPerform", bool, False, None, False),
            ("timingTiming", "timingTiming", timing.Timing, False, "timing", False),
            ("timingDateTime", "timingDateTime", fhirdate.FHIRDate, False, "timing", False),
            ("timingAge", "timingAge", age.Age, False, "timing", False),
            ("timingPeriod", "timingPeriod", period.Period, False, "timing", False),
            ("timingRange", "timingRange", range.Range, False, "timing", False),
            ("timingDuration", "timingDuration", duration.Duration, False, "timing", False),
            ("location", "location", fhirreference.FHIRReference, False, None, False),
            ("participant", "participant", ActivityDefinitionParticipant, True, None, False),
            ("productReference", "productReference", fhirreference.FHIRReference, False, "product", False),
            ("productCodeableConcept", "productCodeableConcept", codeableconcept.CodeableConcept, False, "product", False),
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("dosage", "dosage", dosage.Dosage, True, None, False),
            ("bodySite", "bodySite", codeableconcept.CodeableConcept, True, None, False),
            ("specimenRequirement", "specimenRequirement", fhirreference.FHIRReference, True, None, False),
            ("observationRequirement", "observationRequirement", fhirreference.FHIRReference, True, None, False),
            ("observationResultRequirement", "observationResultRequirement", fhirreference.FHIRReference, True, None, False),
            ("transform", "transform", str, False, None, False),
            ("dynamicValue", "dynamicValue", ActivityDefinitionDynamicValue, True, None, False),
        ])
        return js


from . import backboneelement

class ActivityDefinitionDynamicValue(backboneelement.BackboneElement):
    """ Dynamic aspects of the definition.
    
    Dynamic values that will be evaluated to produce values for elements of the
    resulting resource. For example, if the dosage of a medication must be
    computed based on the patient's weight, a dynamic value would be used to
    specify an expression that calculated the weight, and the path on the
    request resource that would contain the result.
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
        
        super(ActivityDefinitionDynamicValue, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ActivityDefinitionDynamicValue, self).elementProperties()
        js.extend([
            ("path", "path", str, False, None, True),
            ("expression", "expression", expression.Expression, False, None, True),
        ])
        return js


class ActivityDefinitionParticipant(backboneelement.BackboneElement):
    """ Who should participate in the action.
    
    Indicates who should participate in performing the action described.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """The type of participant in the action."""
    _attribute_docstrings['role'] = """E.g. Nurse, Surgeon, Parent, etc.."""

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
        """ E.g. Nurse, Surgeon, Parent, etc.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(ActivityDefinitionParticipant, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ActivityDefinitionParticipant, self).elementProperties()
        js.extend([
            ("type", "type", str, False, None, True),
            ("role", "role", codeableconcept.CodeableConcept, False, None, False),
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
    from . import dosage
except ImportError:
    dosage = sys.modules[__package__ + '.dosage']
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
    from . import usagecontext
except ImportError:
    usagecontext = sys.modules[__package__ + '.usagecontext']
