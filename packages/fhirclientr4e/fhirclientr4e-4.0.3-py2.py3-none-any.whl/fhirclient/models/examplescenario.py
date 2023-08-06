#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/ExampleScenario) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class ExampleScenario(domainresource.DomainResource):
    """ Example of workflow instance.
    """
    
    resource_type = "ExampleScenario"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['url'] = """Canonical identifier for this example scenario, represented as a URI (globally unique)."""
    _attribute_docstrings['identifier'] = """Additional identifier for the example scenario."""
    _attribute_docstrings['version'] = """Business version of the example scenario."""
    _attribute_docstrings['name'] = """Name for this example scenario (computer friendly)."""
    _attribute_docstrings['status'] = """The status of this example scenario. Enables tracking the life-cycle of the content."""
    _attribute_docstrings['experimental'] = """For testing purposes, not real usage."""
    _attribute_docstrings['date'] = """Date last changed."""
    _attribute_docstrings['publisher'] = """Name of the publisher (organization or individual)."""
    _attribute_docstrings['contact'] = """Contact details for the publisher."""
    _attribute_docstrings['useContext'] = """The context that the content is intended to support."""
    _attribute_docstrings['jurisdiction'] = """Intended jurisdiction for example scenario (if applicable)."""
    _attribute_docstrings['copyright'] = """Use and/or publishing restrictions."""
    _attribute_docstrings['purpose'] = """The purpose of the example, e.g. to illustrate a scenario."""
    _attribute_docstrings['actor'] = """Actor participating in the resource."""
    _attribute_docstrings['instance'] = """Each resource and each version that is present in the workflow."""
    _attribute_docstrings['process'] = """Each major process - a group of operations."""
    _attribute_docstrings['workflow'] = """Another nested workflow."""

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
        """ Canonical identifier for this example scenario, represented as a
        URI (globally unique).
        Type `str`. """
        
        self.identifier = None
        """ Additional identifier for the example scenario.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.version = None
        """ Business version of the example scenario.
        Type `str`. """
        
        self.name = None
        """ Name for this example scenario (computer friendly).
        Type `str`. """
        
        self.status = None
        """ The status of this example scenario. Enables tracking the life-
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
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for example scenario (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.copyright = None
        """ Use and/or publishing restrictions.
        Type `str`. """
        
        self.purpose = None
        """ The purpose of the example, e.g. to illustrate a scenario.
        Type `str`. """
        
        self.actor = None
        """ Actor participating in the resource.
        List of `ExampleScenarioActor` items (represented as `dict` in JSON). """
        
        self.instance = None
        """ Each resource and each version that is present in the workflow.
        List of `ExampleScenarioInstance` items (represented as `dict` in JSON). """
        
        self.process = None
        """ Each major process - a group of operations.
        List of `ExampleScenarioProcess` items (represented as `dict` in JSON). """
        
        self.workflow = None
        """ Another nested workflow.
        List of `str` items. """
        
        super(ExampleScenario, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExampleScenario, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("version", "version", str, False, None, False),
            ("name", "name", str, False, None, False),
            ("status", "status", str, False, None, True),
            ("experimental", "experimental", bool, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("publisher", "publisher", str, False, None, False),
            ("contact", "contact", contactdetail.ContactDetail, True, None, False),
            ("useContext", "useContext", usagecontext.UsageContext, True, None, False),
            ("jurisdiction", "jurisdiction", codeableconcept.CodeableConcept, True, None, False),
            ("copyright", "copyright", str, False, None, False),
            ("purpose", "purpose", str, False, None, False),
            ("actor", "actor", ExampleScenarioActor, True, None, False),
            ("instance", "instance", ExampleScenarioInstance, True, None, False),
            ("process", "process", ExampleScenarioProcess, True, None, False),
            ("workflow", "workflow", str, True, None, False),
        ])
        return js


from . import backboneelement

class ExampleScenarioActor(backboneelement.BackboneElement):
    """ Actor participating in the resource.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['actorId'] = """ID or acronym of the actor."""
    _attribute_docstrings['type'] = """The type of actor - person or system."""
    _attribute_docstrings['name'] = """The name of the actor as shown in the page."""
    _attribute_docstrings['description'] = """The description of the actor."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://hl7.org/fhir/examplescenario-actor-type',
        'restricted_to': ['person', 'entity'],
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
        
        self.actorId = None
        """ ID or acronym of the actor.
        Type `str`. """
        
        self.type = None
        """ The type of actor - person or system.
        Type `str`. """
        
        self.name = None
        """ The name of the actor as shown in the page.
        Type `str`. """
        
        self.description = None
        """ The description of the actor.
        Type `str`. """
        
        super(ExampleScenarioActor, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExampleScenarioActor, self).elementProperties()
        js.extend([
            ("actorId", "actorId", str, False, None, True),
            ("type", "type", str, False, None, True),
            ("name", "name", str, False, None, False),
            ("description", "description", str, False, None, False),
        ])
        return js


class ExampleScenarioInstance(backboneelement.BackboneElement):
    """ Each resource and each version that is present in the workflow.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['resourceId'] = """The id of the resource for referencing."""
    _attribute_docstrings['resourceType'] = """None"""
    _attribute_docstrings['name'] = """A short name for the resource instance."""
    _attribute_docstrings['description'] = """Human-friendly description of the resource instance."""
    _attribute_docstrings['version'] = """A specific version of the resource."""
    _attribute_docstrings['containedInstance'] = """Resources contained in the instance."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['resourceType'] = {
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
        
        self.resourceId = None
        """ The id of the resource for referencing.
        Type `str`. """
        
        self.resourceType = None
        """ None.
        Type `str`. """
        
        self.name = None
        """ A short name for the resource instance.
        Type `str`. """
        
        self.description = None
        """ Human-friendly description of the resource instance.
        Type `str`. """
        
        self.version = None
        """ A specific version of the resource.
        List of `ExampleScenarioInstanceVersion` items (represented as `dict` in JSON). """
        
        self.containedInstance = None
        """ Resources contained in the instance.
        List of `ExampleScenarioInstanceContainedInstance` items (represented as `dict` in JSON). """
        
        super(ExampleScenarioInstance, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExampleScenarioInstance, self).elementProperties()
        js.extend([
            ("resourceId", "resourceId", str, False, None, True),
            ("resourceType", "resourceType", str, False, None, True),
            ("name", "name", str, False, None, False),
            ("description", "description", str, False, None, False),
            ("version", "version", ExampleScenarioInstanceVersion, True, None, False),
            ("containedInstance", "containedInstance", ExampleScenarioInstanceContainedInstance, True, None, False),
        ])
        return js


class ExampleScenarioInstanceContainedInstance(backboneelement.BackboneElement):
    """ Resources contained in the instance.
    
    Resources contained in the instance (e.g. the observations contained in a
    bundle).
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['resourceId'] = """Each resource contained in the instance."""
    _attribute_docstrings['versionId'] = """A specific version of a resource contained in the instance."""

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
        
        self.resourceId = None
        """ Each resource contained in the instance.
        Type `str`. """
        
        self.versionId = None
        """ A specific version of a resource contained in the instance.
        Type `str`. """
        
        super(ExampleScenarioInstanceContainedInstance, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExampleScenarioInstanceContainedInstance, self).elementProperties()
        js.extend([
            ("resourceId", "resourceId", str, False, None, True),
            ("versionId", "versionId", str, False, None, False),
        ])
        return js


class ExampleScenarioInstanceVersion(backboneelement.BackboneElement):
    """ A specific version of the resource.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['versionId'] = """The identifier of a specific version of a resource."""
    _attribute_docstrings['description'] = """The description of the resource version."""

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
        
        self.versionId = None
        """ The identifier of a specific version of a resource.
        Type `str`. """
        
        self.description = None
        """ The description of the resource version.
        Type `str`. """
        
        super(ExampleScenarioInstanceVersion, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExampleScenarioInstanceVersion, self).elementProperties()
        js.extend([
            ("versionId", "versionId", str, False, None, True),
            ("description", "description", str, False, None, True),
        ])
        return js


class ExampleScenarioProcess(backboneelement.BackboneElement):
    """ Each major process - a group of operations.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['title'] = """The diagram title of the group of operations."""
    _attribute_docstrings['description'] = """A longer description of the group of operations."""
    _attribute_docstrings['preConditions'] = """Description of initial status before the process starts."""
    _attribute_docstrings['postConditions'] = """Description of final status after the process ends."""
    _attribute_docstrings['step'] = """Each step of the process."""

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
        
        self.title = None
        """ The diagram title of the group of operations.
        Type `str`. """
        
        self.description = None
        """ A longer description of the group of operations.
        Type `str`. """
        
        self.preConditions = None
        """ Description of initial status before the process starts.
        Type `str`. """
        
        self.postConditions = None
        """ Description of final status after the process ends.
        Type `str`. """
        
        self.step = None
        """ Each step of the process.
        List of `ExampleScenarioProcessStep` items (represented as `dict` in JSON). """
        
        super(ExampleScenarioProcess, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExampleScenarioProcess, self).elementProperties()
        js.extend([
            ("title", "title", str, False, None, True),
            ("description", "description", str, False, None, False),
            ("preConditions", "preConditions", str, False, None, False),
            ("postConditions", "postConditions", str, False, None, False),
            ("step", "step", ExampleScenarioProcessStep, True, None, False),
        ])
        return js


class ExampleScenarioProcessStep(backboneelement.BackboneElement):
    """ Each step of the process.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['process'] = """Nested process."""
    _attribute_docstrings['pause'] = """If there is a pause in the flow."""
    _attribute_docstrings['operation'] = """Each interaction or action."""
    _attribute_docstrings['alternative'] = """Alternate non-typical step action."""

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
        
        self.process = None
        """ Nested process.
        List of `ExampleScenarioProcess` items (represented as `dict` in JSON). """
        
        self.pause = None
        """ If there is a pause in the flow.
        Type `bool`. """
        
        self.operation = None
        """ Each interaction or action.
        Type `ExampleScenarioProcessStepOperation` (represented as `dict` in JSON). """
        
        self.alternative = None
        """ Alternate non-typical step action.
        List of `ExampleScenarioProcessStepAlternative` items (represented as `dict` in JSON). """
        
        super(ExampleScenarioProcessStep, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExampleScenarioProcessStep, self).elementProperties()
        js.extend([
            ("process", "process", ExampleScenarioProcess, True, None, False),
            ("pause", "pause", bool, False, None, False),
            ("operation", "operation", ExampleScenarioProcessStepOperation, False, None, False),
            ("alternative", "alternative", ExampleScenarioProcessStepAlternative, True, None, False),
        ])
        return js


class ExampleScenarioProcessStepAlternative(backboneelement.BackboneElement):
    """ Alternate non-typical step action.
    
    Indicates an alternative step that can be taken instead of the operations
    on the base step in exceptional/atypical circumstances.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['title'] = """Label for alternative."""
    _attribute_docstrings['description'] = """A human-readable description of each option."""
    _attribute_docstrings['step'] = """What happens in each alternative option."""

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
        
        self.title = None
        """ Label for alternative.
        Type `str`. """
        
        self.description = None
        """ A human-readable description of each option.
        Type `str`. """
        
        self.step = None
        """ What happens in each alternative option.
        List of `ExampleScenarioProcessStep` items (represented as `dict` in JSON). """
        
        super(ExampleScenarioProcessStepAlternative, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExampleScenarioProcessStepAlternative, self).elementProperties()
        js.extend([
            ("title", "title", str, False, None, True),
            ("description", "description", str, False, None, False),
            ("step", "step", ExampleScenarioProcessStep, True, None, False),
        ])
        return js


class ExampleScenarioProcessStepOperation(backboneelement.BackboneElement):
    """ Each interaction or action.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['number'] = """The sequential number of the interaction."""
    _attribute_docstrings['type'] = """The type of operation - CRUD."""
    _attribute_docstrings['name'] = """The human-friendly name of the interaction."""
    _attribute_docstrings['initiator'] = """Who starts the transaction."""
    _attribute_docstrings['receiver'] = """Who receives the transaction."""
    _attribute_docstrings['description'] = """A comment to be inserted in the diagram."""
    _attribute_docstrings['initiatorActive'] = """Whether the initiator is deactivated right after the transaction."""
    _attribute_docstrings['receiverActive'] = """Whether the receiver is deactivated right after the transaction."""
    _attribute_docstrings['request'] = """Each resource instance used by the initiator."""
    _attribute_docstrings['response'] = """Each resource instance used by the responder."""

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
        
        self.number = None
        """ The sequential number of the interaction.
        Type `str`. """
        
        self.type = None
        """ The type of operation - CRUD.
        Type `str`. """
        
        self.name = None
        """ The human-friendly name of the interaction.
        Type `str`. """
        
        self.initiator = None
        """ Who starts the transaction.
        Type `str`. """
        
        self.receiver = None
        """ Who receives the transaction.
        Type `str`. """
        
        self.description = None
        """ A comment to be inserted in the diagram.
        Type `str`. """
        
        self.initiatorActive = None
        """ Whether the initiator is deactivated right after the transaction.
        Type `bool`. """
        
        self.receiverActive = None
        """ Whether the receiver is deactivated right after the transaction.
        Type `bool`. """
        
        self.request = None
        """ Each resource instance used by the initiator.
        Type `ExampleScenarioInstanceContainedInstance` (represented as `dict` in JSON). """
        
        self.response = None
        """ Each resource instance used by the responder.
        Type `ExampleScenarioInstanceContainedInstance` (represented as `dict` in JSON). """
        
        super(ExampleScenarioProcessStepOperation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExampleScenarioProcessStepOperation, self).elementProperties()
        js.extend([
            ("number", "number", str, False, None, True),
            ("type", "type", str, False, None, False),
            ("name", "name", str, False, None, False),
            ("initiator", "initiator", str, False, None, False),
            ("receiver", "receiver", str, False, None, False),
            ("description", "description", str, False, None, False),
            ("initiatorActive", "initiatorActive", bool, False, None, False),
            ("receiverActive", "receiverActive", bool, False, None, False),
            ("request", "request", ExampleScenarioInstanceContainedInstance, False, None, False),
            ("response", "response", ExampleScenarioInstanceContainedInstance, False, None, False),
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
    from . import identifier
except ImportError:
    identifier = sys.modules[__package__ + '.identifier']
try:
    from . import usagecontext
except ImportError:
    usagecontext = sys.modules[__package__ + '.usagecontext']
