#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/OperationDefinition) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class OperationDefinition(domainresource.DomainResource):
    """ Definition of an operation or a named query.
    
    A formal computable definition of an operation (on the RESTful interface)
    or a named query (using the search interaction).
    """
    
    resource_type = "OperationDefinition"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['url'] = """Canonical identifier for this operation definition, represented as a URI (globally unique)."""
    _attribute_docstrings['version'] = """Business version of the operation definition."""
    _attribute_docstrings['name'] = """Name for this operation definition (computer friendly)."""
    _attribute_docstrings['title'] = """Name for this operation definition (human friendly)."""
    _attribute_docstrings['status'] = """The status of this operation definition. Enables tracking the life-cycle of the content."""
    _attribute_docstrings['kind'] = """Whether this is an operation or a named query."""
    _attribute_docstrings['experimental'] = """For testing purposes, not real usage."""
    _attribute_docstrings['date'] = """Date last changed."""
    _attribute_docstrings['publisher'] = """Name of the publisher (organization or individual)."""
    _attribute_docstrings['contact'] = """Contact details for the publisher."""
    _attribute_docstrings['description'] = """Natural language description of the operation definition."""
    _attribute_docstrings['useContext'] = """The context that the content is intended to support."""
    _attribute_docstrings['jurisdiction'] = """Intended jurisdiction for operation definition (if applicable)."""
    _attribute_docstrings['purpose'] = """Why this operation definition is defined."""
    _attribute_docstrings['affectsState'] = """Whether content is changed by the operation."""
    _attribute_docstrings['code'] = """Name used to invoke the operation."""
    _attribute_docstrings['comment'] = """Additional information about use."""
    _attribute_docstrings['base'] = """Marks this as a profile of the base."""
    _attribute_docstrings['resource'] = """The types on which this operation can be executed."""
    _attribute_docstrings['system'] = """Invoke at the system level?."""
    _attribute_docstrings['type'] = """Invoke at the type level?."""
    _attribute_docstrings['instance'] = """Invoke on an instance?."""
    _attribute_docstrings['inputProfile'] = """Validation information for in parameters."""
    _attribute_docstrings['outputProfile'] = """Validation information for out parameters."""
    _attribute_docstrings['parameter'] = """Parameters for the operation/query."""
    _attribute_docstrings['overload'] = """Define overloaded variants for when  generating code."""

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
    _attribute_enums['kind'] = {
        'url': 'http://hl7.org/fhir/operation-kind',
        'restricted_to': ['operation', 'query'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['resource'] = {
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
        """ Canonical identifier for this operation definition, represented as
        a URI (globally unique).
        Type `str`. """
        
        self.version = None
        """ Business version of the operation definition.
        Type `str`. """
        
        self.name = None
        """ Name for this operation definition (computer friendly).
        Type `str`. """
        
        self.title = None
        """ Name for this operation definition (human friendly).
        Type `str`. """
        
        self.status = None
        """ The status of this operation definition. Enables tracking the life-
        cycle of the content.
        Type `str`. """
        
        self.kind = None
        """ Whether this is an operation or a named query.
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
        """ Natural language description of the operation definition.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for operation definition (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.purpose = None
        """ Why this operation definition is defined.
        Type `str`. """
        
        self.affectsState = None
        """ Whether content is changed by the operation.
        Type `bool`. """
        
        self.code = None
        """ Name used to invoke the operation.
        Type `str`. """
        
        self.comment = None
        """ Additional information about use.
        Type `str`. """
        
        self.base = None
        """ Marks this as a profile of the base.
        Type `str`. """
        
        self.resource = None
        """ The types on which this operation can be executed.
        List of `str` items. """
        
        self.system = None
        """ Invoke at the system level?.
        Type `bool`. """
        
        self.type = None
        """ Invoke at the type level?.
        Type `bool`. """
        
        self.instance = None
        """ Invoke on an instance?.
        Type `bool`. """
        
        self.inputProfile = None
        """ Validation information for in parameters.
        Type `str`. """
        
        self.outputProfile = None
        """ Validation information for out parameters.
        Type `str`. """
        
        self.parameter = None
        """ Parameters for the operation/query.
        List of `OperationDefinitionParameter` items (represented as `dict` in JSON). """
        
        self.overload = None
        """ Define overloaded variants for when  generating code.
        List of `OperationDefinitionOverload` items (represented as `dict` in JSON). """
        
        super(OperationDefinition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(OperationDefinition, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, False),
            ("version", "version", str, False, None, False),
            ("name", "name", str, False, None, True),
            ("title", "title", str, False, None, False),
            ("status", "status", str, False, None, True),
            ("kind", "kind", str, False, None, True),
            ("experimental", "experimental", bool, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("publisher", "publisher", str, False, None, False),
            ("contact", "contact", contactdetail.ContactDetail, True, None, False),
            ("description", "description", str, False, None, False),
            ("useContext", "useContext", usagecontext.UsageContext, True, None, False),
            ("jurisdiction", "jurisdiction", codeableconcept.CodeableConcept, True, None, False),
            ("purpose", "purpose", str, False, None, False),
            ("affectsState", "affectsState", bool, False, None, False),
            ("code", "code", str, False, None, True),
            ("comment", "comment", str, False, None, False),
            ("base", "base", str, False, None, False),
            ("resource", "resource", str, True, None, False),
            ("system", "system", bool, False, None, True),
            ("type", "type", bool, False, None, True),
            ("instance", "instance", bool, False, None, True),
            ("inputProfile", "inputProfile", str, False, None, False),
            ("outputProfile", "outputProfile", str, False, None, False),
            ("parameter", "parameter", OperationDefinitionParameter, True, None, False),
            ("overload", "overload", OperationDefinitionOverload, True, None, False),
        ])
        return js


from . import backboneelement

class OperationDefinitionOverload(backboneelement.BackboneElement):
    """ Define overloaded variants for when  generating code.
    
    Defines an appropriate combination of parameters to use when invoking this
    operation, to help code generators when generating overloaded parameter
    sets for this operation.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['parameterName'] = """Name of parameter to include in overload."""
    _attribute_docstrings['comment'] = """Comments to go on overload."""

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
        
        self.parameterName = None
        """ Name of parameter to include in overload.
        List of `str` items. """
        
        self.comment = None
        """ Comments to go on overload.
        Type `str`. """
        
        super(OperationDefinitionOverload, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(OperationDefinitionOverload, self).elementProperties()
        js.extend([
            ("parameterName", "parameterName", str, True, None, False),
            ("comment", "comment", str, False, None, False),
        ])
        return js


class OperationDefinitionParameter(backboneelement.BackboneElement):
    """ Parameters for the operation/query.
    
    The parameters for the operation/query.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['name'] = """Name in Parameters.parameter.name or in URL."""
    _attribute_docstrings['use'] = """Whether this is an input or an output parameter."""
    _attribute_docstrings['min'] = """Minimum Cardinality."""
    _attribute_docstrings['max'] = """Maximum Cardinality (a number or *)."""
    _attribute_docstrings['documentation'] = """Description of meaning/use."""
    _attribute_docstrings['type'] = """What type this parameter has."""
    _attribute_docstrings['targetProfile'] = """If type is Reference | canonical, allowed targets."""
    _attribute_docstrings['searchType'] = """How the parameter is understood as a search parameter. This is only used if the parameter type is 'string'."""
    _attribute_docstrings['binding'] = """ValueSet details if this is coded."""
    _attribute_docstrings['referencedFrom'] = """References to this parameter."""
    _attribute_docstrings['part'] = """Parts of a nested Parameter."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['use'] = {
        'url': 'http://hl7.org/fhir/operation-parameter-use',
        'restricted_to': ['in', 'out'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['searchType'] = {
        'url': 'http://hl7.org/fhir/search-param-type',
        'restricted_to': ['number', 'date', 'string', 'token', 'reference', 'composite', 'quantity', 'uri', 'special'],
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
        
        self.name = None
        """ Name in Parameters.parameter.name or in URL.
        Type `str`. """
        
        self.use = None
        """ Whether this is an input or an output parameter.
        Type `str`. """
        
        self.min = None
        """ Minimum Cardinality.
        Type `int`. """
        
        self.max = None
        """ Maximum Cardinality (a number or *).
        Type `str`. """
        
        self.documentation = None
        """ Description of meaning/use.
        Type `str`. """
        
        self.type = None
        """ What type this parameter has.
        Type `str`. """
        
        self.targetProfile = None
        """ If type is Reference | canonical, allowed targets.
        List of `str` items. """
        
        self.searchType = None
        """ How the parameter is understood as a search parameter. This is only
        used if the parameter type is 'string'.
        Type `str`. """
        
        self.binding = None
        """ ValueSet details if this is coded.
        Type `OperationDefinitionParameterBinding` (represented as `dict` in JSON). """
        
        self.referencedFrom = None
        """ References to this parameter.
        List of `OperationDefinitionParameterReferencedFrom` items (represented as `dict` in JSON). """
        
        self.part = None
        """ Parts of a nested Parameter.
        List of `OperationDefinitionParameter` items (represented as `dict` in JSON). """
        
        super(OperationDefinitionParameter, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(OperationDefinitionParameter, self).elementProperties()
        js.extend([
            ("name", "name", str, False, None, True),
            ("use", "use", str, False, None, True),
            ("min", "min", int, False, None, True),
            ("max", "max", str, False, None, True),
            ("documentation", "documentation", str, False, None, False),
            ("type", "type", str, False, None, False),
            ("targetProfile", "targetProfile", str, True, None, False),
            ("searchType", "searchType", str, False, None, False),
            ("binding", "binding", OperationDefinitionParameterBinding, False, None, False),
            ("referencedFrom", "referencedFrom", OperationDefinitionParameterReferencedFrom, True, None, False),
            ("part", "part", OperationDefinitionParameter, True, None, False),
        ])
        return js


class OperationDefinitionParameterBinding(backboneelement.BackboneElement):
    """ ValueSet details if this is coded.
    
    Binds to a value set if this parameter is coded (code, Coding,
    CodeableConcept).
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['strength'] = """Indicates the degree of conformance expectations associated with this binding - that is, the degree to which the provided value set must be adhered to in the instances."""
    _attribute_docstrings['valueSet'] = """Source of value set."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['strength'] = {
        'url': 'http://hl7.org/fhir/binding-strength',
        'restricted_to': ['required', 'extensible', 'preferred', 'example'],
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
        
        self.strength = None
        """ Indicates the degree of conformance expectations associated with
        this binding - that is, the degree to which the provided value set
        must be adhered to in the instances.
        Type `str`. """
        
        self.valueSet = None
        """ Source of value set.
        Type `str`. """
        
        super(OperationDefinitionParameterBinding, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(OperationDefinitionParameterBinding, self).elementProperties()
        js.extend([
            ("strength", "strength", str, False, None, True),
            ("valueSet", "valueSet", str, False, None, True),
        ])
        return js


class OperationDefinitionParameterReferencedFrom(backboneelement.BackboneElement):
    """ References to this parameter.
    
    Identifies other resource parameters within the operation invocation that
    are expected to resolve to this resource.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['source'] = """Referencing parameter."""
    _attribute_docstrings['sourceId'] = """Element id of reference."""

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
        
        self.source = None
        """ Referencing parameter.
        Type `str`. """
        
        self.sourceId = None
        """ Element id of reference.
        Type `str`. """
        
        super(OperationDefinitionParameterReferencedFrom, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(OperationDefinitionParameterReferencedFrom, self).elementProperties()
        js.extend([
            ("source", "source", str, False, None, True),
            ("sourceId", "sourceId", str, False, None, False),
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
