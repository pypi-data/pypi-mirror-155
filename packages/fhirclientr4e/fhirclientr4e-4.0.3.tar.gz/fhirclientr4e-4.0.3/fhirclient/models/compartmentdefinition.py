#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/CompartmentDefinition) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class CompartmentDefinition(domainresource.DomainResource):
    """ Compartment Definition for a resource.
    
    A compartment definition that defines how resources are accessed on a
    server.
    """
    
    resource_type = "CompartmentDefinition"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['url'] = """Canonical identifier for this compartment definition, represented as a URI (globally unique)."""
    _attribute_docstrings['version'] = """Business version of the compartment definition."""
    _attribute_docstrings['name'] = """Name for this compartment definition (computer friendly)."""
    _attribute_docstrings['status'] = """The status of this compartment definition. Enables tracking the life-cycle of the content."""
    _attribute_docstrings['experimental'] = """For testing purposes, not real usage."""
    _attribute_docstrings['date'] = """Date last changed."""
    _attribute_docstrings['publisher'] = """Name of the publisher (organization or individual)."""
    _attribute_docstrings['contact'] = """Contact details for the publisher."""
    _attribute_docstrings['description'] = """Natural language description of the compartment definition."""
    _attribute_docstrings['useContext'] = """The context that the content is intended to support."""
    _attribute_docstrings['purpose'] = """Why this compartment definition is defined."""
    _attribute_docstrings['code'] = """Which compartment this definition describes."""
    _attribute_docstrings['search'] = """Whether the search syntax is supported."""
    _attribute_docstrings['resource'] = """How a resource is related to the compartment."""

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
    _attribute_enums['code'] = {
        'url': 'http://hl7.org/fhir/compartment-type',
        'restricted_to': ['Patient', 'Encounter', 'RelatedPerson', 'Practitioner', 'Device'],
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
        """ Canonical identifier for this compartment definition, represented
        as a URI (globally unique).
        Type `str`. """
        
        self.version = None
        """ Business version of the compartment definition.
        Type `str`. """
        
        self.name = None
        """ Name for this compartment definition (computer friendly).
        Type `str`. """
        
        self.status = None
        """ The status of this compartment definition. Enables tracking the
        life-cycle of the content.
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
        """ Natural language description of the compartment definition.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.purpose = None
        """ Why this compartment definition is defined.
        Type `str`. """
        
        self.code = None
        """ Which compartment this definition describes.
        Type `str`. """
        
        self.search = None
        """ Whether the search syntax is supported.
        Type `bool`. """
        
        self.resource = None
        """ How a resource is related to the compartment.
        List of `CompartmentDefinitionResource` items (represented as `dict` in JSON). """
        
        super(CompartmentDefinition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CompartmentDefinition, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, True),
            ("version", "version", str, False, None, False),
            ("name", "name", str, False, None, True),
            ("status", "status", str, False, None, True),
            ("experimental", "experimental", bool, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("publisher", "publisher", str, False, None, False),
            ("contact", "contact", contactdetail.ContactDetail, True, None, False),
            ("description", "description", str, False, None, False),
            ("useContext", "useContext", usagecontext.UsageContext, True, None, False),
            ("purpose", "purpose", str, False, None, False),
            ("code", "code", str, False, None, True),
            ("search", "search", bool, False, None, True),
            ("resource", "resource", CompartmentDefinitionResource, True, None, False),
        ])
        return js


from . import backboneelement

class CompartmentDefinitionResource(backboneelement.BackboneElement):
    """ How a resource is related to the compartment.
    
    Information about how a resource is related to the compartment.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """The name of a resource supported by the server."""
    _attribute_docstrings['param'] = """Search Parameter Name, or chained parameters."""
    _attribute_docstrings['documentation'] = """Additional documentation about the resource and compartment."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['code'] = {
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
        
        self.code = None
        """ The name of a resource supported by the server.
        Type `str`. """
        
        self.param = None
        """ Search Parameter Name, or chained parameters.
        List of `str` items. """
        
        self.documentation = None
        """ Additional documentation about the resource and compartment.
        Type `str`. """
        
        super(CompartmentDefinitionResource, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CompartmentDefinitionResource, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, True),
            ("param", "param", str, True, None, False),
            ("documentation", "documentation", str, False, None, False),
        ])
        return js


import sys
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
