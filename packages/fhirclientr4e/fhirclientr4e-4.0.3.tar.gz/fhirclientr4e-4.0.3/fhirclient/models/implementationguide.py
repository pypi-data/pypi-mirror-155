#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/ImplementationGuide) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class ImplementationGuide(domainresource.DomainResource):
    """ A set of rules about how FHIR is used.
    
    A set of rules of how a particular interoperability or standards problem is
    solved - typically through the use of FHIR resources. This resource is used
    to gather all the parts of an implementation guide into a logical whole and
    to publish a computable definition of all the parts.
    """
    
    resource_type = "ImplementationGuide"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['url'] = """Canonical identifier for this implementation guide, represented as a URI (globally unique)."""
    _attribute_docstrings['version'] = """Business version of the implementation guide."""
    _attribute_docstrings['name'] = """Name for this implementation guide (computer friendly)."""
    _attribute_docstrings['title'] = """Name for this implementation guide (human friendly)."""
    _attribute_docstrings['status'] = """The status of this implementation guide. Enables tracking the life-cycle of the content."""
    _attribute_docstrings['experimental'] = """For testing purposes, not real usage."""
    _attribute_docstrings['date'] = """Date last changed."""
    _attribute_docstrings['publisher'] = """Name of the publisher (organization or individual)."""
    _attribute_docstrings['contact'] = """Contact details for the publisher."""
    _attribute_docstrings['description'] = """Natural language description of the implementation guide."""
    _attribute_docstrings['useContext'] = """The context that the content is intended to support."""
    _attribute_docstrings['jurisdiction'] = """Intended jurisdiction for implementation guide (if applicable)."""
    _attribute_docstrings['copyright'] = """Use and/or publishing restrictions."""
    _attribute_docstrings['packageId'] = """NPM Package name for IG."""
    _attribute_docstrings['license'] = """SPDX license code for this IG (or not-open-source)."""
    _attribute_docstrings['fhirVersion'] = """FHIR Version(s) this Implementation Guide targets."""
    _attribute_docstrings['dependsOn'] = """Another Implementation guide this depends on."""
    _attribute_docstrings['global_fhir'] = """Profiles that apply globally."""
    _attribute_docstrings['definition'] = """Information needed to build the IG."""
    _attribute_docstrings['manifest'] = """Information about an assembled IG."""

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
        """ Canonical identifier for this implementation guide, represented as
        a URI (globally unique).
        Type `str`. """
        
        self.version = None
        """ Business version of the implementation guide.
        Type `str`. """
        
        self.name = None
        """ Name for this implementation guide (computer friendly).
        Type `str`. """
        
        self.title = None
        """ Name for this implementation guide (human friendly).
        Type `str`. """
        
        self.status = None
        """ The status of this implementation guide. Enables tracking the life-
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
        """ Natural language description of the implementation guide.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for implementation guide (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.copyright = None
        """ Use and/or publishing restrictions.
        Type `str`. """
        
        self.packageId = None
        """ NPM Package name for IG.
        Type `str`. """
        
        self.license = None
        """ SPDX license code for this IG (or not-open-source).
        Type `str`. """
        
        self.fhirVersion = None
        """ FHIR Version(s) this Implementation Guide targets.
        List of `str` items. """
        
        self.dependsOn = None
        """ Another Implementation guide this depends on.
        List of `ImplementationGuideDependsOn` items (represented as `dict` in JSON). """
        
        self.global_fhir = None
        """ Profiles that apply globally.
        List of `ImplementationGuideGlobal` items (represented as `dict` in JSON). """
        
        self.definition = None
        """ Information needed to build the IG.
        Type `ImplementationGuideDefinition` (represented as `dict` in JSON). """
        
        self.manifest = None
        """ Information about an assembled IG.
        Type `ImplementationGuideManifest` (represented as `dict` in JSON). """
        
        super(ImplementationGuide, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ImplementationGuide, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, True),
            ("version", "version", str, False, None, False),
            ("name", "name", str, False, None, True),
            ("title", "title", str, False, None, False),
            ("status", "status", str, False, None, True),
            ("experimental", "experimental", bool, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("publisher", "publisher", str, False, None, False),
            ("contact", "contact", contactdetail.ContactDetail, True, None, False),
            ("description", "description", str, False, None, False),
            ("useContext", "useContext", usagecontext.UsageContext, True, None, False),
            ("jurisdiction", "jurisdiction", codeableconcept.CodeableConcept, True, None, False),
            ("copyright", "copyright", str, False, None, False),
            ("packageId", "packageId", str, False, None, True),
            ("license", "license", str, False, None, False),
            ("fhirVersion", "fhirVersion", str, True, None, True),
            ("dependsOn", "dependsOn", ImplementationGuideDependsOn, True, None, False),
            ("global_fhir", "global", ImplementationGuideGlobal, True, None, False),
            ("definition", "definition", ImplementationGuideDefinition, False, None, False),
            ("manifest", "manifest", ImplementationGuideManifest, False, None, False),
        ])
        return js


from . import backboneelement

class ImplementationGuideDefinition(backboneelement.BackboneElement):
    """ Information needed to build the IG.
    
    The information needed by an IG publisher tool to publish the whole
    implementation guide.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['grouping'] = """Grouping used to present related resources in the IG."""
    _attribute_docstrings['resource'] = """Resource in the implementation guide."""
    _attribute_docstrings['page'] = """Page/Section in the Guide."""
    _attribute_docstrings['parameter'] = """Defines how IG is built by tools."""
    _attribute_docstrings['template'] = """A template for building resources."""

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
        
        self.grouping = None
        """ Grouping used to present related resources in the IG.
        List of `ImplementationGuideDefinitionGrouping` items (represented as `dict` in JSON). """
        
        self.resource = None
        """ Resource in the implementation guide.
        List of `ImplementationGuideDefinitionResource` items (represented as `dict` in JSON). """
        
        self.page = None
        """ Page/Section in the Guide.
        Type `ImplementationGuideDefinitionPage` (represented as `dict` in JSON). """
        
        self.parameter = None
        """ Defines how IG is built by tools.
        List of `ImplementationGuideDefinitionParameter` items (represented as `dict` in JSON). """
        
        self.template = None
        """ A template for building resources.
        List of `ImplementationGuideDefinitionTemplate` items (represented as `dict` in JSON). """
        
        super(ImplementationGuideDefinition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ImplementationGuideDefinition, self).elementProperties()
        js.extend([
            ("grouping", "grouping", ImplementationGuideDefinitionGrouping, True, None, False),
            ("resource", "resource", ImplementationGuideDefinitionResource, True, None, True),
            ("page", "page", ImplementationGuideDefinitionPage, False, None, False),
            ("parameter", "parameter", ImplementationGuideDefinitionParameter, True, None, False),
            ("template", "template", ImplementationGuideDefinitionTemplate, True, None, False),
        ])
        return js


class ImplementationGuideDefinitionGrouping(backboneelement.BackboneElement):
    """ Grouping used to present related resources in the IG.
    
    A logical group of resources. Logical groups can be used when building
    pages.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['name'] = """Descriptive name for the package."""
    _attribute_docstrings['description'] = """Human readable text describing the package."""

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
        
        self.name = None
        """ Descriptive name for the package.
        Type `str`. """
        
        self.description = None
        """ Human readable text describing the package.
        Type `str`. """
        
        super(ImplementationGuideDefinitionGrouping, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ImplementationGuideDefinitionGrouping, self).elementProperties()
        js.extend([
            ("name", "name", str, False, None, True),
            ("description", "description", str, False, None, False),
        ])
        return js


class ImplementationGuideDefinitionPage(backboneelement.BackboneElement):
    """ Page/Section in the Guide.
    
    A page / section in the implementation guide. The root page is the
    implementation guide home page.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['nameUrl'] = """Where to find that page."""
    _attribute_docstrings['nameReference'] = """Where to find that page."""
    _attribute_docstrings['title'] = """Short title shown for navigational assistance."""
    _attribute_docstrings['generation'] = """A code that indicates how the page is generated."""
    _attribute_docstrings['page'] = """Nested Pages / Sections."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['generation'] = {
        'url': 'http://hl7.org/fhir/guide-page-generation',
        'restricted_to': ['html', 'markdown', 'xml', 'generated'],
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
        
        self.nameUrl = None
        """ Where to find that page.
        Type `str`. """
        
        self.nameReference = None
        """ Where to find that page.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.title = None
        """ Short title shown for navigational assistance.
        Type `str`. """
        
        self.generation = None
        """ A code that indicates how the page is generated.
        Type `str`. """
        
        self.page = None
        """ Nested Pages / Sections.
        List of `ImplementationGuideDefinitionPage` items (represented as `dict` in JSON). """
        
        super(ImplementationGuideDefinitionPage, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ImplementationGuideDefinitionPage, self).elementProperties()
        js.extend([
            ("nameUrl", "nameUrl", str, False, "name", True),
            ("nameReference", "nameReference", fhirreference.FHIRReference, False, "name", True),
            ("title", "title", str, False, None, True),
            ("generation", "generation", str, False, None, True),
            ("page", "page", ImplementationGuideDefinitionPage, True, None, False),
        ])
        return js


class ImplementationGuideDefinitionParameter(backboneelement.BackboneElement):
    """ Defines how IG is built by tools.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """None"""
    _attribute_docstrings['value'] = """Value for named type."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['code'] = {
        'url': 'http://hl7.org/fhir/guide-parameter-code',
        'restricted_to': ['apply', 'path-resource', 'path-pages', 'path-tx-cache', 'expansion-parameter', 'rule-broken-links', 'generate-xml', 'generate-json', 'generate-turtle', 'html-template'],
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
        """ None.
        Type `str`. """
        
        self.value = None
        """ Value for named type.
        Type `str`. """
        
        super(ImplementationGuideDefinitionParameter, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ImplementationGuideDefinitionParameter, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, True),
            ("value", "value", str, False, None, True),
        ])
        return js


class ImplementationGuideDefinitionResource(backboneelement.BackboneElement):
    """ Resource in the implementation guide.
    
    A resource that is part of the implementation guide. Conformance resources
    (value set, structure definition, capability statements etc.) are obvious
    candidates for inclusion, but any kind of resource can be included as an
    example resource.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['reference'] = """Location of the resource."""
    _attribute_docstrings['fhirVersion'] = """Versions this applies to (if different to IG)."""
    _attribute_docstrings['name'] = """Human Name for the resource."""
    _attribute_docstrings['description'] = """Reason why included in guide."""
    _attribute_docstrings['exampleBoolean'] = """Is an example/What is this an example of?."""
    _attribute_docstrings['exampleCanonical'] = """Is an example/What is this an example of?."""
    _attribute_docstrings['groupingId'] = """Grouping this is part of."""

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
        
        self.reference = None
        """ Location of the resource.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.fhirVersion = None
        """ Versions this applies to (if different to IG).
        List of `str` items. """
        
        self.name = None
        """ Human Name for the resource.
        Type `str`. """
        
        self.description = None
        """ Reason why included in guide.
        Type `str`. """
        
        self.exampleBoolean = None
        """ Is an example/What is this an example of?.
        Type `bool`. """
        
        self.exampleCanonical = None
        """ Is an example/What is this an example of?.
        Type `str`. """
        
        self.groupingId = None
        """ Grouping this is part of.
        Type `str`. """
        
        super(ImplementationGuideDefinitionResource, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ImplementationGuideDefinitionResource, self).elementProperties()
        js.extend([
            ("reference", "reference", fhirreference.FHIRReference, False, None, True),
            ("fhirVersion", "fhirVersion", str, True, None, False),
            ("name", "name", str, False, None, False),
            ("description", "description", str, False, None, False),
            ("exampleBoolean", "exampleBoolean", bool, False, "example", False),
            ("exampleCanonical", "exampleCanonical", str, False, "example", False),
            ("groupingId", "groupingId", str, False, None, False),
        ])
        return js


class ImplementationGuideDefinitionTemplate(backboneelement.BackboneElement):
    """ A template for building resources.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Type of template specified."""
    _attribute_docstrings['source'] = """The source location for the template."""
    _attribute_docstrings['scope'] = """The scope in which the template applies."""

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
        
        self.code = None
        """ Type of template specified.
        Type `str`. """
        
        self.source = None
        """ The source location for the template.
        Type `str`. """
        
        self.scope = None
        """ The scope in which the template applies.
        Type `str`. """
        
        super(ImplementationGuideDefinitionTemplate, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ImplementationGuideDefinitionTemplate, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, True),
            ("source", "source", str, False, None, True),
            ("scope", "scope", str, False, None, False),
        ])
        return js


class ImplementationGuideDependsOn(backboneelement.BackboneElement):
    """ Another Implementation guide this depends on.
    
    Another implementation guide that this implementation depends on.
    Typically, an implementation guide uses value sets, profiles etc.defined in
    other implementation guides.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['uri'] = """Identity of the IG that this depends on."""
    _attribute_docstrings['packageId'] = """NPM Package name for IG this depends on."""
    _attribute_docstrings['version'] = """Version of the IG."""

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
        
        self.uri = None
        """ Identity of the IG that this depends on.
        Type `str`. """
        
        self.packageId = None
        """ NPM Package name for IG this depends on.
        Type `str`. """
        
        self.version = None
        """ Version of the IG.
        Type `str`. """
        
        super(ImplementationGuideDependsOn, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ImplementationGuideDependsOn, self).elementProperties()
        js.extend([
            ("uri", "uri", str, False, None, True),
            ("packageId", "packageId", str, False, None, False),
            ("version", "version", str, False, None, False),
        ])
        return js


class ImplementationGuideGlobal(backboneelement.BackboneElement):
    """ Profiles that apply globally.
    
    A set of profiles that all resources covered by this implementation guide
    must conform to.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """The type of resource that all instances must conform to."""
    _attribute_docstrings['profile'] = """Profile that all resources must conform to."""

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
        """ The type of resource that all instances must conform to.
        Type `str`. """
        
        self.profile = None
        """ Profile that all resources must conform to.
        Type `str`. """
        
        super(ImplementationGuideGlobal, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ImplementationGuideGlobal, self).elementProperties()
        js.extend([
            ("type", "type", str, False, None, True),
            ("profile", "profile", str, False, None, True),
        ])
        return js


class ImplementationGuideManifest(backboneelement.BackboneElement):
    """ Information about an assembled IG.
    
    Information about an assembled implementation guide, created by the
    publication tooling.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['rendering'] = """Location of rendered implementation guide."""
    _attribute_docstrings['resource'] = """Resource in the implementation guide."""
    _attribute_docstrings['page'] = """HTML page within the parent IG."""
    _attribute_docstrings['image'] = """Image within the IG."""
    _attribute_docstrings['other'] = """Additional linkable file in IG."""

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
        
        self.rendering = None
        """ Location of rendered implementation guide.
        Type `str`. """
        
        self.resource = None
        """ Resource in the implementation guide.
        List of `ImplementationGuideManifestResource` items (represented as `dict` in JSON). """
        
        self.page = None
        """ HTML page within the parent IG.
        List of `ImplementationGuideManifestPage` items (represented as `dict` in JSON). """
        
        self.image = None
        """ Image within the IG.
        List of `str` items. """
        
        self.other = None
        """ Additional linkable file in IG.
        List of `str` items. """
        
        super(ImplementationGuideManifest, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ImplementationGuideManifest, self).elementProperties()
        js.extend([
            ("rendering", "rendering", str, False, None, False),
            ("resource", "resource", ImplementationGuideManifestResource, True, None, True),
            ("page", "page", ImplementationGuideManifestPage, True, None, False),
            ("image", "image", str, True, None, False),
            ("other", "other", str, True, None, False),
        ])
        return js


class ImplementationGuideManifestPage(backboneelement.BackboneElement):
    """ HTML page within the parent IG.
    
    Information about a page within the IG.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['name'] = """HTML page name."""
    _attribute_docstrings['title'] = """Title of the page, for references."""
    _attribute_docstrings['anchor'] = """Anchor available on the page."""

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
        
        self.name = None
        """ HTML page name.
        Type `str`. """
        
        self.title = None
        """ Title of the page, for references.
        Type `str`. """
        
        self.anchor = None
        """ Anchor available on the page.
        List of `str` items. """
        
        super(ImplementationGuideManifestPage, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ImplementationGuideManifestPage, self).elementProperties()
        js.extend([
            ("name", "name", str, False, None, True),
            ("title", "title", str, False, None, False),
            ("anchor", "anchor", str, True, None, False),
        ])
        return js


class ImplementationGuideManifestResource(backboneelement.BackboneElement):
    """ Resource in the implementation guide.
    
    A resource that is part of the implementation guide. Conformance resources
    (value set, structure definition, capability statements etc.) are obvious
    candidates for inclusion, but any kind of resource can be included as an
    example resource.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['reference'] = """Location of the resource."""
    _attribute_docstrings['exampleBoolean'] = """Is an example/What is this an example of?."""
    _attribute_docstrings['exampleCanonical'] = """Is an example/What is this an example of?."""
    _attribute_docstrings['relativePath'] = """Relative path for page in IG."""

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
        
        self.reference = None
        """ Location of the resource.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.exampleBoolean = None
        """ Is an example/What is this an example of?.
        Type `bool`. """
        
        self.exampleCanonical = None
        """ Is an example/What is this an example of?.
        Type `str`. """
        
        self.relativePath = None
        """ Relative path for page in IG.
        Type `str`. """
        
        super(ImplementationGuideManifestResource, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ImplementationGuideManifestResource, self).elementProperties()
        js.extend([
            ("reference", "reference", fhirreference.FHIRReference, False, None, True),
            ("exampleBoolean", "exampleBoolean", bool, False, "example", False),
            ("exampleCanonical", "exampleCanonical", str, False, "example", False),
            ("relativePath", "relativePath", str, False, None, False),
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
    from . import fhirreference
except ImportError:
    fhirreference = sys.modules[__package__ + '.fhirreference']
try:
    from . import usagecontext
except ImportError:
    usagecontext = sys.modules[__package__ + '.usagecontext']
