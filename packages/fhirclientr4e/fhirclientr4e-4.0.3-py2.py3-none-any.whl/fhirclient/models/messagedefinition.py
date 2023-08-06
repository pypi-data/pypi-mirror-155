#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/MessageDefinition) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class MessageDefinition(domainresource.DomainResource):
    """ A resource that defines a type of message that can be exchanged between
    systems.
    
    Defines the characteristics of a message that can be shared between
    systems, including the type of event that initiates the message, the
    content to be transmitted and what response(s), if any, are permitted.
    """
    
    resource_type = "MessageDefinition"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['url'] = """Business Identifier for a given MessageDefinition."""
    _attribute_docstrings['identifier'] = """Primary key for the message definition on a given server."""
    _attribute_docstrings['version'] = """Business version of the message definition."""
    _attribute_docstrings['name'] = """Name for this message definition (computer friendly)."""
    _attribute_docstrings['title'] = """Name for this message definition (human friendly)."""
    _attribute_docstrings['replaces'] = """Takes the place of."""
    _attribute_docstrings['status'] = """The status of this message definition. Enables tracking the life-cycle of the content."""
    _attribute_docstrings['experimental'] = """For testing purposes, not real usage."""
    _attribute_docstrings['date'] = """Date last changed."""
    _attribute_docstrings['publisher'] = """Name of the publisher (organization or individual)."""
    _attribute_docstrings['contact'] = """Contact details for the publisher."""
    _attribute_docstrings['description'] = """Natural language description of the message definition."""
    _attribute_docstrings['useContext'] = """The context that the content is intended to support."""
    _attribute_docstrings['jurisdiction'] = """Intended jurisdiction for message definition (if applicable)."""
    _attribute_docstrings['purpose'] = """Why this message definition is defined."""
    _attribute_docstrings['copyright'] = """Use and/or publishing restrictions."""
    _attribute_docstrings['base'] = """Definition this one is based on."""
    _attribute_docstrings['parent'] = """Protocol/workflow this is part of."""
    _attribute_docstrings['eventCoding'] = """Event code  or link to the EventDefinition."""
    _attribute_docstrings['eventUri'] = """Event code  or link to the EventDefinition."""
    _attribute_docstrings['category'] = """The impact of the content of the message."""
    _attribute_docstrings['focus'] = """Resource(s) that are the subject of the event."""
    _attribute_docstrings['responseRequired'] = """Declare at a message definition level whether a response is required or only upon error or success, or never."""
    _attribute_docstrings['allowedResponse'] = """Responses to this message."""
    _attribute_docstrings['graph'] = """Canonical reference to a GraphDefinition."""

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
    _attribute_enums['category'] = {
        'url': 'http://hl7.org/fhir/message-significance-category',
        'restricted_to': ['consequence', 'currency', 'notification'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['responseRequired'] = {
        'url': 'http://hl7.org/fhir/messageheader-response-request',
        'restricted_to': ['always', 'on-error', 'never', 'on-success'],
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
        """ Business Identifier for a given MessageDefinition.
        Type `str`. """
        
        self.identifier = None
        """ Primary key for the message definition on a given server.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.version = None
        """ Business version of the message definition.
        Type `str`. """
        
        self.name = None
        """ Name for this message definition (computer friendly).
        Type `str`. """
        
        self.title = None
        """ Name for this message definition (human friendly).
        Type `str`. """
        
        self.replaces = None
        """ Takes the place of.
        List of `str` items. """
        
        self.status = None
        """ The status of this message definition. Enables tracking the life-
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
        """ Natural language description of the message definition.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for message definition (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.purpose = None
        """ Why this message definition is defined.
        Type `str`. """
        
        self.copyright = None
        """ Use and/or publishing restrictions.
        Type `str`. """
        
        self.base = None
        """ Definition this one is based on.
        Type `str`. """
        
        self.parent = None
        """ Protocol/workflow this is part of.
        List of `str` items. """
        
        self.eventCoding = None
        """ Event code  or link to the EventDefinition.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.eventUri = None
        """ Event code  or link to the EventDefinition.
        Type `str`. """
        
        self.category = None
        """ The impact of the content of the message.
        Type `str`. """
        
        self.focus = None
        """ Resource(s) that are the subject of the event.
        List of `MessageDefinitionFocus` items (represented as `dict` in JSON). """
        
        self.responseRequired = None
        """ Declare at a message definition level whether a response is
        required or only upon error or success, or never.
        Type `str`. """
        
        self.allowedResponse = None
        """ Responses to this message.
        List of `MessageDefinitionAllowedResponse` items (represented as `dict` in JSON). """
        
        self.graph = None
        """ Canonical reference to a GraphDefinition.
        List of `str` items. """
        
        super(MessageDefinition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MessageDefinition, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("version", "version", str, False, None, False),
            ("name", "name", str, False, None, False),
            ("title", "title", str, False, None, False),
            ("replaces", "replaces", str, True, None, False),
            ("status", "status", str, False, None, True),
            ("experimental", "experimental", bool, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, True),
            ("publisher", "publisher", str, False, None, False),
            ("contact", "contact", contactdetail.ContactDetail, True, None, False),
            ("description", "description", str, False, None, False),
            ("useContext", "useContext", usagecontext.UsageContext, True, None, False),
            ("jurisdiction", "jurisdiction", codeableconcept.CodeableConcept, True, None, False),
            ("purpose", "purpose", str, False, None, False),
            ("copyright", "copyright", str, False, None, False),
            ("base", "base", str, False, None, False),
            ("parent", "parent", str, True, None, False),
            ("eventCoding", "eventCoding", coding.Coding, False, "event", True),
            ("eventUri", "eventUri", str, False, "event", True),
            ("category", "category", str, False, None, False),
            ("focus", "focus", MessageDefinitionFocus, True, None, False),
            ("responseRequired", "responseRequired", str, False, None, False),
            ("allowedResponse", "allowedResponse", MessageDefinitionAllowedResponse, True, None, False),
            ("graph", "graph", str, True, None, False),
        ])
        return js


from . import backboneelement

class MessageDefinitionAllowedResponse(backboneelement.BackboneElement):
    """ Responses to this message.
    
    Indicates what types of messages may be sent as an application-level
    response to this message.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['message'] = """Reference to allowed message definition response."""
    _attribute_docstrings['situation'] = """When should this response be used."""

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
        
        self.message = None
        """ Reference to allowed message definition response.
        Type `str`. """
        
        self.situation = None
        """ When should this response be used.
        Type `str`. """
        
        super(MessageDefinitionAllowedResponse, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MessageDefinitionAllowedResponse, self).elementProperties()
        js.extend([
            ("message", "message", str, False, None, True),
            ("situation", "situation", str, False, None, False),
        ])
        return js


class MessageDefinitionFocus(backboneelement.BackboneElement):
    """ Resource(s) that are the subject of the event.
    
    Identifies the resource (or resources) that are being addressed by the
    event.  For example, the Encounter for an admit message or two Account
    records for a merge.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """The kind of resource that must be the focus for this message."""
    _attribute_docstrings['profile'] = """Profile that must be adhered to by focus."""
    _attribute_docstrings['min'] = """Minimum number of focuses of this type."""
    _attribute_docstrings['max'] = """Maximum number of focuses of this type."""

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
        """ The kind of resource that must be the focus for this message.
        Type `str`. """
        
        self.profile = None
        """ Profile that must be adhered to by focus.
        Type `str`. """
        
        self.min = None
        """ Minimum number of focuses of this type.
        Type `int`. """
        
        self.max = None
        """ Maximum number of focuses of this type.
        Type `str`. """
        
        super(MessageDefinitionFocus, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MessageDefinitionFocus, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, True),
            ("profile", "profile", str, False, None, False),
            ("min", "min", int, False, None, True),
            ("max", "max", str, False, None, False),
        ])
        return js


import sys
try:
    from . import codeableconcept
except ImportError:
    codeableconcept = sys.modules[__package__ + '.codeableconcept']
try:
    from . import coding
except ImportError:
    coding = sys.modules[__package__ + '.coding']
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
