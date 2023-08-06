#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/CarePlan) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class CarePlan(domainresource.DomainResource):
    """ Healthcare plan for patient or group.
    
    Describes the intention of how one or more practitioners intend to deliver
    care for a particular patient, group or community for a period of time,
    possibly limited to care for a specific condition or set of conditions.
    """
    
    resource_type = "CarePlan"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """External Ids for this plan."""
    _attribute_docstrings['instantiatesCanonical'] = """Instantiates FHIR protocol or definition."""
    _attribute_docstrings['instantiatesUri'] = """Instantiates external protocol or definition."""
    _attribute_docstrings['basedOn'] = """Fulfills CarePlan."""
    _attribute_docstrings['replaces'] = """CarePlan replaced by this CarePlan."""
    _attribute_docstrings['partOf'] = """Part of referenced CarePlan."""
    _attribute_docstrings['status'] = """Indicates whether the plan is currently being acted upon, represents future intentions or is now a historical record."""
    _attribute_docstrings['intent'] = """Indicates the level of authority/intentionality associated with the care plan and where the care plan fits into the workflow chain."""
    _attribute_docstrings['category'] = """Type of plan."""
    _attribute_docstrings['title'] = """Human-friendly name for the care plan."""
    _attribute_docstrings['description'] = """Summary of nature of plan."""
    _attribute_docstrings['subject'] = """Who the care plan is for."""
    _attribute_docstrings['encounter'] = """Encounter created as part of."""
    _attribute_docstrings['period'] = """Time period plan covers."""
    _attribute_docstrings['created'] = """Date record was first recorded."""
    _attribute_docstrings['author'] = """Who is the designated responsible party."""
    _attribute_docstrings['contributor'] = """Who provided the content of the care plan."""
    _attribute_docstrings['careTeam'] = """Who's involved in plan?."""
    _attribute_docstrings['addresses'] = """Health issues this plan addresses."""
    _attribute_docstrings['supportingInfo'] = """Information considered as part of plan."""
    _attribute_docstrings['goal'] = """Desired outcome of plan."""
    _attribute_docstrings['activity'] = """Action to occur as part of plan."""
    _attribute_docstrings['note'] = """Comments about the plan."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/request-status',
        'restricted_to': ['draft', 'active', 'on-hold', 'revoked', 'completed', 'entered-in-error', 'unknown'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['intent'] = {
        'url': 'http://hl7.org/fhir/request-intent',
        'restricted_to': ['proposal', 'plan', 'directive', 'order', 'original-order', 'reflex-order', 'filler-order', 'instance-order', 'option'],
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
        """ External Ids for this plan.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.instantiatesCanonical = None
        """ Instantiates FHIR protocol or definition.
        List of `str` items. """
        
        self.instantiatesUri = None
        """ Instantiates external protocol or definition.
        List of `str` items. """
        
        self.basedOn = None
        """ Fulfills CarePlan.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.replaces = None
        """ CarePlan replaced by this CarePlan.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.partOf = None
        """ Part of referenced CarePlan.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.status = None
        """ Indicates whether the plan is currently being acted upon,
        represents future intentions or is now a historical record.
        Type `str`. """
        
        self.intent = None
        """ Indicates the level of authority/intentionality associated with the
        care plan and where the care plan fits into the workflow chain.
        Type `str`. """
        
        self.category = None
        """ Type of plan.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.title = None
        """ Human-friendly name for the care plan.
        Type `str`. """
        
        self.description = None
        """ Summary of nature of plan.
        Type `str`. """
        
        self.subject = None
        """ Who the care plan is for.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Encounter created as part of.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.period = None
        """ Time period plan covers.
        Type `Period` (represented as `dict` in JSON). """
        
        self.created = None
        """ Date record was first recorded.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.author = None
        """ Who is the designated responsible party.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.contributor = None
        """ Who provided the content of the care plan.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.careTeam = None
        """ Who's involved in plan?.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.addresses = None
        """ Health issues this plan addresses.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.supportingInfo = None
        """ Information considered as part of plan.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.goal = None
        """ Desired outcome of plan.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.activity = None
        """ Action to occur as part of plan.
        List of `CarePlanActivity` items (represented as `dict` in JSON). """
        
        self.note = None
        """ Comments about the plan.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        super(CarePlan, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CarePlan, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("instantiatesCanonical", "instantiatesCanonical", str, True, None, False),
            ("instantiatesUri", "instantiatesUri", str, True, None, False),
            ("basedOn", "basedOn", fhirreference.FHIRReference, True, None, False),
            ("replaces", "replaces", fhirreference.FHIRReference, True, None, False),
            ("partOf", "partOf", fhirreference.FHIRReference, True, None, False),
            ("status", "status", str, False, None, True),
            ("intent", "intent", str, False, None, True),
            ("category", "category", codeableconcept.CodeableConcept, True, None, False),
            ("title", "title", str, False, None, False),
            ("description", "description", str, False, None, False),
            ("subject", "subject", fhirreference.FHIRReference, False, None, True),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("period", "period", period.Period, False, None, False),
            ("created", "created", fhirdate.FHIRDate, False, None, False),
            ("author", "author", fhirreference.FHIRReference, False, None, False),
            ("contributor", "contributor", fhirreference.FHIRReference, True, None, False),
            ("careTeam", "careTeam", fhirreference.FHIRReference, True, None, False),
            ("addresses", "addresses", fhirreference.FHIRReference, True, None, False),
            ("supportingInfo", "supportingInfo", fhirreference.FHIRReference, True, None, False),
            ("goal", "goal", fhirreference.FHIRReference, True, None, False),
            ("activity", "activity", CarePlanActivity, True, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
        ])
        return js


from . import backboneelement

class CarePlanActivity(backboneelement.BackboneElement):
    """ Action to occur as part of plan.
    
    Identifies a planned action to occur as part of the plan.  For example, a
    medication to be used, lab tests to perform, self-monitoring, education,
    etc.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['outcomeCodeableConcept'] = """Results of the activity."""
    _attribute_docstrings['outcomeReference'] = """Appointment, Encounter, Procedure, etc.."""
    _attribute_docstrings['progress'] = """Comments about the activity status/progress."""
    _attribute_docstrings['reference'] = """Activity details defined in specific resource."""
    _attribute_docstrings['detail'] = """In-line definition of activity."""

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
        
        self.outcomeCodeableConcept = None
        """ Results of the activity.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.outcomeReference = None
        """ Appointment, Encounter, Procedure, etc.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.progress = None
        """ Comments about the activity status/progress.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        self.reference = None
        """ Activity details defined in specific resource.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.detail = None
        """ In-line definition of activity.
        Type `CarePlanActivityDetail` (represented as `dict` in JSON). """
        
        super(CarePlanActivity, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CarePlanActivity, self).elementProperties()
        js.extend([
            ("outcomeCodeableConcept", "outcomeCodeableConcept", codeableconcept.CodeableConcept, True, None, False),
            ("outcomeReference", "outcomeReference", fhirreference.FHIRReference, True, None, False),
            ("progress", "progress", annotation.Annotation, True, None, False),
            ("reference", "reference", fhirreference.FHIRReference, False, None, False),
            ("detail", "detail", CarePlanActivityDetail, False, None, False),
        ])
        return js


class CarePlanActivityDetail(backboneelement.BackboneElement):
    """ In-line definition of activity.
    
    A simple summary of a planned activity suitable for a general care plan
    system (e.g. form driven) that doesn't know about specific resources such
    as procedure etc.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['kind'] = """A description of the kind of resource the in-line definition of a care plan activity is representing.  The CarePlan.activity.detail is an in-line definition when a resource is not referenced using CarePlan.activity.reference.  For example, a MedicationRequest, a ServiceRequest, or a CommunicationRequest."""
    _attribute_docstrings['instantiatesCanonical'] = """Instantiates FHIR protocol or definition."""
    _attribute_docstrings['instantiatesUri'] = """Instantiates external protocol or definition."""
    _attribute_docstrings['code'] = """Detail type of activity."""
    _attribute_docstrings['reasonCode'] = """Why activity should be done or why activity was prohibited."""
    _attribute_docstrings['reasonReference'] = """Why activity is needed."""
    _attribute_docstrings['goal'] = """Goals this activity relates to."""
    _attribute_docstrings['status'] = """Identifies what progress is being made for the specific activity."""
    _attribute_docstrings['statusReason'] = """Reason for current status."""
    _attribute_docstrings['doNotPerform'] = """If true, activity is prohibiting action."""
    _attribute_docstrings['scheduledTiming'] = """When activity is to occur."""
    _attribute_docstrings['scheduledPeriod'] = """When activity is to occur."""
    _attribute_docstrings['scheduledString'] = """When activity is to occur."""
    _attribute_docstrings['location'] = """Where it should happen."""
    _attribute_docstrings['performer'] = """Who will be responsible?."""
    _attribute_docstrings['productCodeableConcept'] = """What is to be administered/supplied."""
    _attribute_docstrings['productReference'] = """What is to be administered/supplied."""
    _attribute_docstrings['dailyAmount'] = """How to consume/day?."""
    _attribute_docstrings['quantity'] = """How much to administer/supply/consume."""
    _attribute_docstrings['description'] = """Extra info describing activity to perform."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['kind'] = {
        'url': 'http://hl7.org/fhir/resource-types',
        'restricted_to': ['Account', 'ActivityDefinition', 'AdverseEvent', 'AllergyIntolerance', 'Appointment', 'AppointmentResponse', 'AuditEvent', 'Basic', 'Binary', 'BiologicallyDerivedProduct', 'BodyStructure', 'Bundle', 'CapabilityStatement', 'CarePlan', 'CareTeam', 'CatalogEntry', 'ChargeItem', 'ChargeItemDefinition', 'Claim', 'ClaimResponse', 'ClinicalImpression', 'CodeSystem', 'Communication', 'CommunicationRequest', 'CompartmentDefinition', 'Composition', 'ConceptMap', 'Condition', 'Consent', 'Contract', 'Coverage', 'CoverageEligibilityRequest', 'CoverageEligibilityResponse', 'DetectedIssue', 'Device', 'DeviceDefinition', 'DeviceMetric', 'DeviceRequest', 'DeviceUseStatement', 'DiagnosticReport', 'DocumentManifest', 'DocumentReference', 'DomainResource', 'EffectEvidenceSynthesis', 'Encounter', 'Endpoint', 'EnrollmentRequest', 'EnrollmentResponse', 'EpisodeOfCare', 'EventDefinition', 'Evidence', 'EvidenceVariable', 'ExampleScenario', 'ExplanationOfBenefit', 'FamilyMemberHistory', 'Flag', 'Goal', 'GraphDefinition', 'Group', 'GuidanceResponse', 'HealthcareService', 'ImagingStudy', 'Immunization', 'ImmunizationEvaluation', 'ImmunizationRecommendation', 'ImplementationGuide', 'InsurancePlan', 'Invoice', 'Library', 'Linkage', 'List', 'Location', 'Measure', 'MeasureReport', 'Media', 'Medication', 'MedicationAdministration', 'MedicationDispense', 'MedicationKnowledge', 'MedicationRequest', 'MedicationStatement', 'MedicinalProduct', 'MedicinalProductAuthorization', 'MedicinalProductContraindication', 'MedicinalProductIndication', 'MedicinalProductIngredient', 'MedicinalProductInteraction', 'MedicinalProductManufactured', 'MedicinalProductPackaged', 'MedicinalProductPharmaceutical', 'MedicinalProductUndesirableEffect', 'MessageDefinition', 'MessageHeader', 'MolecularSequence', 'NamingSystem', 'NutritionOrder', 'Observation', 'ObservationDefinition', 'OperationDefinition', 'OperationOutcome', 'Organization', 'OrganizationAffiliation', 'Parameters', 'Patient', 'PaymentNotice', 'PaymentReconciliation', 'Person', 'PlanDefinition', 'Practitioner', 'PractitionerRole', 'Procedure', 'Provenance', 'Questionnaire', 'QuestionnaireResponse', 'RelatedPerson', 'RequestGroup', 'ResearchDefinition', 'ResearchElementDefinition', 'ResearchStudy', 'ResearchSubject', 'Resource', 'RiskAssessment', 'RiskEvidenceSynthesis', 'Schedule', 'SearchParameter', 'ServiceRequest', 'Slot', 'Specimen', 'SpecimenDefinition', 'StructureDefinition', 'StructureMap', 'Subscription', 'Substance', 'SubstanceNucleicAcid', 'SubstancePolymer', 'SubstanceProtein', 'SubstanceReferenceInformation', 'SubstanceSourceMaterial', 'SubstanceSpecification', 'SupplyDelivery', 'SupplyRequest', 'Task', 'TerminologyCapabilities', 'TestReport', 'TestScript', 'ValueSet', 'VerificationResult', 'VisionPrescription'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/care-plan-activity-status',
        'restricted_to': ['not-started', 'scheduled', 'in-progress', 'on-hold', 'completed', 'cancelled', 'stopped', 'unknown', 'entered-in-error'],
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
        """ A description of the kind of resource the in-line definition of a
        care plan activity is representing.  The CarePlan.activity.detail
        is an in-line definition when a resource is not referenced using
        CarePlan.activity.reference.  For example, a MedicationRequest, a
        ServiceRequest, or a CommunicationRequest.
        Type `str`. """
        
        self.instantiatesCanonical = None
        """ Instantiates FHIR protocol or definition.
        List of `str` items. """
        
        self.instantiatesUri = None
        """ Instantiates external protocol or definition.
        List of `str` items. """
        
        self.code = None
        """ Detail type of activity.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.reasonCode = None
        """ Why activity should be done or why activity was prohibited.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.reasonReference = None
        """ Why activity is needed.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.goal = None
        """ Goals this activity relates to.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.status = None
        """ Identifies what progress is being made for the specific activity.
        Type `str`. """
        
        self.statusReason = None
        """ Reason for current status.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.doNotPerform = None
        """ If true, activity is prohibiting action.
        Type `bool`. """
        
        self.scheduledTiming = None
        """ When activity is to occur.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.scheduledPeriod = None
        """ When activity is to occur.
        Type `Period` (represented as `dict` in JSON). """
        
        self.scheduledString = None
        """ When activity is to occur.
        Type `str`. """
        
        self.location = None
        """ Where it should happen.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.performer = None
        """ Who will be responsible?.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.productCodeableConcept = None
        """ What is to be administered/supplied.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.productReference = None
        """ What is to be administered/supplied.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.dailyAmount = None
        """ How to consume/day?.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.quantity = None
        """ How much to administer/supply/consume.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.description = None
        """ Extra info describing activity to perform.
        Type `str`. """
        
        super(CarePlanActivityDetail, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CarePlanActivityDetail, self).elementProperties()
        js.extend([
            ("kind", "kind", str, False, None, False),
            ("instantiatesCanonical", "instantiatesCanonical", str, True, None, False),
            ("instantiatesUri", "instantiatesUri", str, True, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("reasonCode", "reasonCode", codeableconcept.CodeableConcept, True, None, False),
            ("reasonReference", "reasonReference", fhirreference.FHIRReference, True, None, False),
            ("goal", "goal", fhirreference.FHIRReference, True, None, False),
            ("status", "status", str, False, None, True),
            ("statusReason", "statusReason", codeableconcept.CodeableConcept, False, None, False),
            ("doNotPerform", "doNotPerform", bool, False, None, False),
            ("scheduledTiming", "scheduledTiming", timing.Timing, False, "scheduled", False),
            ("scheduledPeriod", "scheduledPeriod", period.Period, False, "scheduled", False),
            ("scheduledString", "scheduledString", str, False, "scheduled", False),
            ("location", "location", fhirreference.FHIRReference, False, None, False),
            ("performer", "performer", fhirreference.FHIRReference, True, None, False),
            ("productCodeableConcept", "productCodeableConcept", codeableconcept.CodeableConcept, False, "product", False),
            ("productReference", "productReference", fhirreference.FHIRReference, False, "product", False),
            ("dailyAmount", "dailyAmount", quantity.Quantity, False, None, False),
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("description", "description", str, False, None, False),
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
    from . import timing
except ImportError:
    timing = sys.modules[__package__ + '.timing']
