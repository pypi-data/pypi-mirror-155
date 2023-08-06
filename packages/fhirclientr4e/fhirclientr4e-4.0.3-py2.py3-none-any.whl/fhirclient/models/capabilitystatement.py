#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/CapabilityStatement) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class CapabilityStatement(domainresource.DomainResource):
    """ A statement of system capabilities.
    
    A Capability Statement documents a set of capabilities (behaviors) of a
    FHIR Server for a particular version of FHIR that may be used as a
    statement of actual server functionality or a statement of required or
    desired server implementation.
    """
    
    resource_type = "CapabilityStatement"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['url'] = """Canonical identifier for this capability statement, represented as a URI (globally unique)."""
    _attribute_docstrings['version'] = """Business version of the capability statement."""
    _attribute_docstrings['name'] = """Name for this capability statement (computer friendly)."""
    _attribute_docstrings['title'] = """Name for this capability statement (human friendly)."""
    _attribute_docstrings['status'] = """The status of this capability statement. Enables tracking the life-cycle of the content."""
    _attribute_docstrings['experimental'] = """For testing purposes, not real usage."""
    _attribute_docstrings['date'] = """Date last changed."""
    _attribute_docstrings['publisher'] = """Name of the publisher (organization or individual)."""
    _attribute_docstrings['contact'] = """Contact details for the publisher."""
    _attribute_docstrings['description'] = """Natural language description of the capability statement."""
    _attribute_docstrings['useContext'] = """The context that the content is intended to support."""
    _attribute_docstrings['jurisdiction'] = """Intended jurisdiction for capability statement (if applicable)."""
    _attribute_docstrings['purpose'] = """Why this capability statement is defined."""
    _attribute_docstrings['copyright'] = """Use and/or publishing restrictions."""
    _attribute_docstrings['kind'] = """The way that this statement is intended to be used, to describe an actual running instance of software, a particular product (kind, not instance of software) or a class of implementation (e.g. a desired purchase)."""
    _attribute_docstrings['instantiates'] = """Canonical URL of another capability statement this implements."""
    _attribute_docstrings['imports'] = """Canonical URL of another capability statement this adds to."""
    _attribute_docstrings['software'] = """Software that is covered by this capability statement."""
    _attribute_docstrings['implementation'] = """If this describes a specific instance."""
    _attribute_docstrings['fhirVersion'] = """FHIR Version the system supports."""
    _attribute_docstrings['format'] = """formats supported (xml | json | ttl | mime type)."""
    _attribute_docstrings['patchFormat'] = """Patch formats supported."""
    _attribute_docstrings['implementationGuide'] = """Implementation guides supported."""
    _attribute_docstrings['rest'] = """If the endpoint is a RESTful one."""
    _attribute_docstrings['messaging'] = """If messaging is supported."""
    _attribute_docstrings['document'] = """Document definition."""

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
        'url': 'http://hl7.org/fhir/capability-statement-kind',
        'restricted_to': ['instance', 'capability', 'requirements'],
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
        """ Canonical identifier for this capability statement, represented as
        a URI (globally unique).
        Type `str`. """
        
        self.version = None
        """ Business version of the capability statement.
        Type `str`. """
        
        self.name = None
        """ Name for this capability statement (computer friendly).
        Type `str`. """
        
        self.title = None
        """ Name for this capability statement (human friendly).
        Type `str`. """
        
        self.status = None
        """ The status of this capability statement. Enables tracking the life-
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
        """ Natural language description of the capability statement.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for capability statement (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.purpose = None
        """ Why this capability statement is defined.
        Type `str`. """
        
        self.copyright = None
        """ Use and/or publishing restrictions.
        Type `str`. """
        
        self.kind = None
        """ The way that this statement is intended to be used, to describe an
        actual running instance of software, a particular product (kind,
        not instance of software) or a class of implementation (e.g. a
        desired purchase).
        Type `str`. """
        
        self.instantiates = None
        """ Canonical URL of another capability statement this implements.
        List of `str` items. """
        
        self.imports = None
        """ Canonical URL of another capability statement this adds to.
        List of `str` items. """
        
        self.software = None
        """ Software that is covered by this capability statement.
        Type `CapabilityStatementSoftware` (represented as `dict` in JSON). """
        
        self.implementation = None
        """ If this describes a specific instance.
        Type `CapabilityStatementImplementation` (represented as `dict` in JSON). """
        
        self.fhirVersion = None
        """ FHIR Version the system supports.
        Type `str`. """
        
        self.format = None
        """ formats supported (xml | json | ttl | mime type).
        List of `str` items. """
        
        self.patchFormat = None
        """ Patch formats supported.
        List of `str` items. """
        
        self.implementationGuide = None
        """ Implementation guides supported.
        List of `str` items. """
        
        self.rest = None
        """ If the endpoint is a RESTful one.
        List of `CapabilityStatementRest` items (represented as `dict` in JSON). """
        
        self.messaging = None
        """ If messaging is supported.
        List of `CapabilityStatementMessaging` items (represented as `dict` in JSON). """
        
        self.document = None
        """ Document definition.
        List of `CapabilityStatementDocument` items (represented as `dict` in JSON). """
        
        super(CapabilityStatement, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CapabilityStatement, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, False),
            ("version", "version", str, False, None, False),
            ("name", "name", str, False, None, False),
            ("title", "title", str, False, None, False),
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
            ("kind", "kind", str, False, None, True),
            ("instantiates", "instantiates", str, True, None, False),
            ("imports", "imports", str, True, None, False),
            ("software", "software", CapabilityStatementSoftware, False, None, False),
            ("implementation", "implementation", CapabilityStatementImplementation, False, None, False),
            ("fhirVersion", "fhirVersion", str, False, None, True),
            ("format", "format", str, True, None, True),
            ("patchFormat", "patchFormat", str, True, None, False),
            ("implementationGuide", "implementationGuide", str, True, None, False),
            ("rest", "rest", CapabilityStatementRest, True, None, False),
            ("messaging", "messaging", CapabilityStatementMessaging, True, None, False),
            ("document", "document", CapabilityStatementDocument, True, None, False),
        ])
        return js


from . import backboneelement

class CapabilityStatementDocument(backboneelement.BackboneElement):
    """ Document definition.
    
    A document definition.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['mode'] = """Mode of this document declaration - whether an application is a producer or consumer."""
    _attribute_docstrings['documentation'] = """Description of document support."""
    _attribute_docstrings['profile'] = """Constraint on the resources used in the document."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['mode'] = {
        'url': 'http://hl7.org/fhir/document-mode',
        'restricted_to': ['producer', 'consumer'],
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
        
        self.mode = None
        """ Mode of this document declaration - whether an application is a
        producer or consumer.
        Type `str`. """
        
        self.documentation = None
        """ Description of document support.
        Type `str`. """
        
        self.profile = None
        """ Constraint on the resources used in the document.
        Type `str`. """
        
        super(CapabilityStatementDocument, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CapabilityStatementDocument, self).elementProperties()
        js.extend([
            ("mode", "mode", str, False, None, True),
            ("documentation", "documentation", str, False, None, False),
            ("profile", "profile", str, False, None, True),
        ])
        return js


class CapabilityStatementImplementation(backboneelement.BackboneElement):
    """ If this describes a specific instance.
    
    Identifies a specific implementation instance that is described by the
    capability statement - i.e. a particular installation, rather than the
    capabilities of a software program.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['description'] = """Describes this specific instance."""
    _attribute_docstrings['url'] = """Base URL for the installation."""
    _attribute_docstrings['custodian'] = """Organization that manages the data."""

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
        
        self.description = None
        """ Describes this specific instance.
        Type `str`. """
        
        self.url = None
        """ Base URL for the installation.
        Type `str`. """
        
        self.custodian = None
        """ Organization that manages the data.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(CapabilityStatementImplementation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CapabilityStatementImplementation, self).elementProperties()
        js.extend([
            ("description", "description", str, False, None, True),
            ("url", "url", str, False, None, False),
            ("custodian", "custodian", fhirreference.FHIRReference, False, None, False),
        ])
        return js


class CapabilityStatementMessaging(backboneelement.BackboneElement):
    """ If messaging is supported.
    
    A description of the messaging capabilities of the solution.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['endpoint'] = """Where messages should be sent."""
    _attribute_docstrings['reliableCache'] = """Reliable Message Cache Length (min)."""
    _attribute_docstrings['documentation'] = """Messaging interface behavior details."""
    _attribute_docstrings['supportedMessage'] = """Messages supported by this system."""

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
        
        self.endpoint = None
        """ Where messages should be sent.
        List of `CapabilityStatementMessagingEndpoint` items (represented as `dict` in JSON). """
        
        self.reliableCache = None
        """ Reliable Message Cache Length (min).
        Type `int`. """
        
        self.documentation = None
        """ Messaging interface behavior details.
        Type `str`. """
        
        self.supportedMessage = None
        """ Messages supported by this system.
        List of `CapabilityStatementMessagingSupportedMessage` items (represented as `dict` in JSON). """
        
        super(CapabilityStatementMessaging, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CapabilityStatementMessaging, self).elementProperties()
        js.extend([
            ("endpoint", "endpoint", CapabilityStatementMessagingEndpoint, True, None, False),
            ("reliableCache", "reliableCache", int, False, None, False),
            ("documentation", "documentation", str, False, None, False),
            ("supportedMessage", "supportedMessage", CapabilityStatementMessagingSupportedMessage, True, None, False),
        ])
        return js


class CapabilityStatementMessagingEndpoint(backboneelement.BackboneElement):
    """ Where messages should be sent.
    
    An endpoint (network accessible address) to which messages and/or replies
    are to be sent.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['protocol'] = """http | ftp | mllp +."""
    _attribute_docstrings['address'] = """Network address or identifier of the end-point."""

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
        
        self.protocol = None
        """ http | ftp | mllp +.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.address = None
        """ Network address or identifier of the end-point.
        Type `str`. """
        
        super(CapabilityStatementMessagingEndpoint, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CapabilityStatementMessagingEndpoint, self).elementProperties()
        js.extend([
            ("protocol", "protocol", coding.Coding, False, None, True),
            ("address", "address", str, False, None, True),
        ])
        return js


class CapabilityStatementMessagingSupportedMessage(backboneelement.BackboneElement):
    """ Messages supported by this system.
    
    References to message definitions for messages this system can send or
    receive.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['mode'] = """The mode of this event declaration - whether application is sender or receiver."""
    _attribute_docstrings['definition'] = """Message supported by this system."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['mode'] = {
        'url': 'http://hl7.org/fhir/event-capability-mode',
        'restricted_to': ['sender', 'receiver'],
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
        
        self.mode = None
        """ The mode of this event declaration - whether application is sender
        or receiver.
        Type `str`. """
        
        self.definition = None
        """ Message supported by this system.
        Type `str`. """
        
        super(CapabilityStatementMessagingSupportedMessage, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CapabilityStatementMessagingSupportedMessage, self).elementProperties()
        js.extend([
            ("mode", "mode", str, False, None, True),
            ("definition", "definition", str, False, None, True),
        ])
        return js


class CapabilityStatementRest(backboneelement.BackboneElement):
    """ If the endpoint is a RESTful one.
    
    A definition of the restful capabilities of the solution, if any.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['mode'] = """Identifies whether this portion of the statement is describing the ability to initiate or receive restful operations."""
    _attribute_docstrings['documentation'] = """General description of implementation."""
    _attribute_docstrings['security'] = """Information about security of implementation."""
    _attribute_docstrings['resource'] = """Resource served on the REST interface."""
    _attribute_docstrings['interaction'] = """What operations are supported?."""
    _attribute_docstrings['searchParam'] = """Search parameters for searching all resources."""
    _attribute_docstrings['operation'] = """Definition of a system level operation."""
    _attribute_docstrings['compartment'] = """Compartments served/used by system."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['mode'] = {
        'url': 'http://hl7.org/fhir/restful-capability-mode',
        'restricted_to': ['client', 'server'],
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
        
        self.mode = None
        """ Identifies whether this portion of the statement is describing the
        ability to initiate or receive restful operations.
        Type `str`. """
        
        self.documentation = None
        """ General description of implementation.
        Type `str`. """
        
        self.security = None
        """ Information about security of implementation.
        Type `CapabilityStatementRestSecurity` (represented as `dict` in JSON). """
        
        self.resource = None
        """ Resource served on the REST interface.
        List of `CapabilityStatementRestResource` items (represented as `dict` in JSON). """
        
        self.interaction = None
        """ What operations are supported?.
        List of `CapabilityStatementRestInteraction` items (represented as `dict` in JSON). """
        
        self.searchParam = None
        """ Search parameters for searching all resources.
        List of `CapabilityStatementRestResourceSearchParam` items (represented as `dict` in JSON). """
        
        self.operation = None
        """ Definition of a system level operation.
        List of `CapabilityStatementRestResourceOperation` items (represented as `dict` in JSON). """
        
        self.compartment = None
        """ Compartments served/used by system.
        List of `str` items. """
        
        super(CapabilityStatementRest, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CapabilityStatementRest, self).elementProperties()
        js.extend([
            ("mode", "mode", str, False, None, True),
            ("documentation", "documentation", str, False, None, False),
            ("security", "security", CapabilityStatementRestSecurity, False, None, False),
            ("resource", "resource", CapabilityStatementRestResource, True, None, False),
            ("interaction", "interaction", CapabilityStatementRestInteraction, True, None, False),
            ("searchParam", "searchParam", CapabilityStatementRestResourceSearchParam, True, None, False),
            ("operation", "operation", CapabilityStatementRestResourceOperation, True, None, False),
            ("compartment", "compartment", str, True, None, False),
        ])
        return js


class CapabilityStatementRestInteraction(backboneelement.BackboneElement):
    """ What operations are supported?.
    
    A specification of restful operations supported by the system.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """A coded identifier of the operation, supported by the system."""
    _attribute_docstrings['documentation'] = """Anything special about operation behavior."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['code'] = {
        'url': 'http://hl7.org/fhir/restful-interaction',
        'restricted_to': ['read', 'vread', 'update', 'patch', 'delete', 'history', 'history-instance', 'history-type', 'history-system', 'create', 'search', 'search-type', 'search-system', 'capabilities', 'transaction', 'batch', 'operation'],
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
        """ A coded identifier of the operation, supported by the system.
        Type `str`. """
        
        self.documentation = None
        """ Anything special about operation behavior.
        Type `str`. """
        
        super(CapabilityStatementRestInteraction, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CapabilityStatementRestInteraction, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, True),
            ("documentation", "documentation", str, False, None, False),
        ])
        return js


class CapabilityStatementRestResource(backboneelement.BackboneElement):
    """ Resource served on the REST interface.
    
    A specification of the restful capabilities of the solution for a specific
    resource type.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """A type of resource exposed via the restful interface."""
    _attribute_docstrings['profile'] = """Base System profile for all uses of resource."""
    _attribute_docstrings['supportedProfile'] = """Profiles for use cases supported."""
    _attribute_docstrings['documentation'] = """Additional information about the use of the resource type."""
    _attribute_docstrings['interaction'] = """What operations are supported?."""
    _attribute_docstrings['versioning'] = """This field is set to no-version to specify that the system does not support (server) or use (client) versioning for this resource type. If this has some other value, the server must at least correctly track and populate the versionId meta-property on resources. If the value is 'versioned-update', then the server supports all the versioning features, including using e-tags for version integrity in the API."""
    _attribute_docstrings['readHistory'] = """Whether vRead can return past versions."""
    _attribute_docstrings['updateCreate'] = """If update can commit to a new identity."""
    _attribute_docstrings['conditionalCreate'] = """If allows/uses conditional create."""
    _attribute_docstrings['conditionalRead'] = """A code that indicates how the server supports conditional read."""
    _attribute_docstrings['conditionalUpdate'] = """If allows/uses conditional update."""
    _attribute_docstrings['conditionalDelete'] = """A code that indicates how the server supports conditional delete."""
    _attribute_docstrings['referencePolicy'] = """A set of flags that defines how references are supported."""
    _attribute_docstrings['searchInclude'] = """_include values supported by the server."""
    _attribute_docstrings['searchRevInclude'] = """_revinclude values supported by the server."""
    _attribute_docstrings['searchParam'] = """Search parameters supported by implementation."""
    _attribute_docstrings['operation'] = """Definition of a resource operation."""

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
    _attribute_enums['versioning'] = {
        'url': 'http://hl7.org/fhir/versioning-policy',
        'restricted_to': ['no-version', 'versioned', 'versioned-update'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['conditionalRead'] = {
        'url': 'http://hl7.org/fhir/conditional-read-status',
        'restricted_to': ['not-supported', 'modified-since', 'not-match', 'full-support'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['conditionalDelete'] = {
        'url': 'http://hl7.org/fhir/conditional-delete-status',
        'restricted_to': ['not-supported', 'single', 'multiple'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['referencePolicy'] = {
        'url': 'http://hl7.org/fhir/reference-handling-policy',
        'restricted_to': ['literal', 'logical', 'resolves', 'enforced', 'local'],
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
        """ A type of resource exposed via the restful interface.
        Type `str`. """
        
        self.profile = None
        """ Base System profile for all uses of resource.
        Type `str`. """
        
        self.supportedProfile = None
        """ Profiles for use cases supported.
        List of `str` items. """
        
        self.documentation = None
        """ Additional information about the use of the resource type.
        Type `str`. """
        
        self.interaction = None
        """ What operations are supported?.
        List of `CapabilityStatementRestResourceInteraction` items (represented as `dict` in JSON). """
        
        self.versioning = None
        """ This field is set to no-version to specify that the system does not
        support (server) or use (client) versioning for this resource type.
        If this has some other value, the server must at least correctly
        track and populate the versionId meta-property on resources. If the
        value is 'versioned-update', then the server supports all the
        versioning features, including using e-tags for version integrity
        in the API.
        Type `str`. """
        
        self.readHistory = None
        """ Whether vRead can return past versions.
        Type `bool`. """
        
        self.updateCreate = None
        """ If update can commit to a new identity.
        Type `bool`. """
        
        self.conditionalCreate = None
        """ If allows/uses conditional create.
        Type `bool`. """
        
        self.conditionalRead = None
        """ A code that indicates how the server supports conditional read.
        Type `str`. """
        
        self.conditionalUpdate = None
        """ If allows/uses conditional update.
        Type `bool`. """
        
        self.conditionalDelete = None
        """ A code that indicates how the server supports conditional delete.
        Type `str`. """
        
        self.referencePolicy = None
        """ A set of flags that defines how references are supported.
        List of `str` items. """
        
        self.searchInclude = None
        """ _include values supported by the server.
        List of `str` items. """
        
        self.searchRevInclude = None
        """ _revinclude values supported by the server.
        List of `str` items. """
        
        self.searchParam = None
        """ Search parameters supported by implementation.
        List of `CapabilityStatementRestResourceSearchParam` items (represented as `dict` in JSON). """
        
        self.operation = None
        """ Definition of a resource operation.
        List of `CapabilityStatementRestResourceOperation` items (represented as `dict` in JSON). """
        
        super(CapabilityStatementRestResource, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CapabilityStatementRestResource, self).elementProperties()
        js.extend([
            ("type", "type", str, False, None, True),
            ("profile", "profile", str, False, None, False),
            ("supportedProfile", "supportedProfile", str, True, None, False),
            ("documentation", "documentation", str, False, None, False),
            ("interaction", "interaction", CapabilityStatementRestResourceInteraction, True, None, False),
            ("versioning", "versioning", str, False, None, False),
            ("readHistory", "readHistory", bool, False, None, False),
            ("updateCreate", "updateCreate", bool, False, None, False),
            ("conditionalCreate", "conditionalCreate", bool, False, None, False),
            ("conditionalRead", "conditionalRead", str, False, None, False),
            ("conditionalUpdate", "conditionalUpdate", bool, False, None, False),
            ("conditionalDelete", "conditionalDelete", str, False, None, False),
            ("referencePolicy", "referencePolicy", str, True, None, False),
            ("searchInclude", "searchInclude", str, True, None, False),
            ("searchRevInclude", "searchRevInclude", str, True, None, False),
            ("searchParam", "searchParam", CapabilityStatementRestResourceSearchParam, True, None, False),
            ("operation", "operation", CapabilityStatementRestResourceOperation, True, None, False),
        ])
        return js


class CapabilityStatementRestResourceInteraction(backboneelement.BackboneElement):
    """ What operations are supported?.
    
    Identifies a restful operation supported by the solution.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Coded identifier of the operation, supported by the system resource."""
    _attribute_docstrings['documentation'] = """Anything special about operation behavior."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['code'] = {
        'url': 'http://hl7.org/fhir/restful-interaction',
        'restricted_to': ['read', 'vread', 'update', 'patch', 'delete', 'history', 'history-instance', 'history-type', 'history-system', 'create', 'search', 'search-type', 'search-system', 'capabilities', 'transaction', 'batch', 'operation'],
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
        """ Coded identifier of the operation, supported by the system resource.
        Type `str`. """
        
        self.documentation = None
        """ Anything special about operation behavior.
        Type `str`. """
        
        super(CapabilityStatementRestResourceInteraction, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CapabilityStatementRestResourceInteraction, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, True),
            ("documentation", "documentation", str, False, None, False),
        ])
        return js


class CapabilityStatementRestResourceOperation(backboneelement.BackboneElement):
    """ Definition of a resource operation.
    
    Definition of an operation or a named query together with its parameters
    and their meaning and type. Consult the definition of the operation for
    details about how to invoke the operation, and the parameters.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['name'] = """Name by which the operation/query is invoked."""
    _attribute_docstrings['definition'] = """The defined operation/query."""
    _attribute_docstrings['documentation'] = """Specific details about operation behavior."""

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
        """ Name by which the operation/query is invoked.
        Type `str`. """
        
        self.definition = None
        """ The defined operation/query.
        Type `str`. """
        
        self.documentation = None
        """ Specific details about operation behavior.
        Type `str`. """
        
        super(CapabilityStatementRestResourceOperation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CapabilityStatementRestResourceOperation, self).elementProperties()
        js.extend([
            ("name", "name", str, False, None, True),
            ("definition", "definition", str, False, None, True),
            ("documentation", "documentation", str, False, None, False),
        ])
        return js


class CapabilityStatementRestResourceSearchParam(backboneelement.BackboneElement):
    """ Search parameters supported by implementation.
    
    Search parameters for implementations to support and/or make use of -
    either references to ones defined in the specification, or additional ones
    defined for/by the implementation.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['name'] = """Name of search parameter."""
    _attribute_docstrings['definition'] = """Source of definition for parameter."""
    _attribute_docstrings['type'] = """The type of value a search parameter refers to, and how the content is interpreted."""
    _attribute_docstrings['documentation'] = """Server-specific usage."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
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
        """ Name of search parameter.
        Type `str`. """
        
        self.definition = None
        """ Source of definition for parameter.
        Type `str`. """
        
        self.type = None
        """ The type of value a search parameter refers to, and how the content
        is interpreted.
        Type `str`. """
        
        self.documentation = None
        """ Server-specific usage.
        Type `str`. """
        
        super(CapabilityStatementRestResourceSearchParam, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CapabilityStatementRestResourceSearchParam, self).elementProperties()
        js.extend([
            ("name", "name", str, False, None, True),
            ("definition", "definition", str, False, None, False),
            ("type", "type", str, False, None, True),
            ("documentation", "documentation", str, False, None, False),
        ])
        return js


class CapabilityStatementRestSecurity(backboneelement.BackboneElement):
    """ Information about security of implementation.
    
    Information about security implementation from an interface perspective -
    what a client needs to know.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['cors'] = """Adds CORS Headers (http://enable-cors.org/)."""
    _attribute_docstrings['service'] = """Types of security services that are supported/required by the system."""
    _attribute_docstrings['description'] = """General description of how security works."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['service'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/restful-security-service',
        'restricted_to': ['OAuth', 'SMART-on-FHIR', 'NTLM', 'Basic', 'Kerberos', 'Certificates'],
        'binding_strength': 'extensible',
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
        
        self.cors = None
        """ Adds CORS Headers (http://enable-cors.org/).
        Type `bool`. """
        
        self.service = None
        """ Types of security services that are supported/required by the
        system.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.description = None
        """ General description of how security works.
        Type `str`. """
        
        super(CapabilityStatementRestSecurity, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CapabilityStatementRestSecurity, self).elementProperties()
        js.extend([
            ("cors", "cors", bool, False, None, False),
            ("service", "service", codeableconcept.CodeableConcept, True, None, False),
            ("description", "description", str, False, None, False),
        ])
        return js


class CapabilityStatementSoftware(backboneelement.BackboneElement):
    """ Software that is covered by this capability statement.
    
    Software that is covered by this capability statement.  It is used when the
    capability statement describes the capabilities of a particular software
    version, independent of an installation.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['name'] = """A name the software is known by."""
    _attribute_docstrings['version'] = """Version covered by this statement."""
    _attribute_docstrings['releaseDate'] = """Date this version was released."""

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
        """ A name the software is known by.
        Type `str`. """
        
        self.version = None
        """ Version covered by this statement.
        Type `str`. """
        
        self.releaseDate = None
        """ Date this version was released.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        super(CapabilityStatementSoftware, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CapabilityStatementSoftware, self).elementProperties()
        js.extend([
            ("name", "name", str, False, None, True),
            ("version", "version", str, False, None, False),
            ("releaseDate", "releaseDate", fhirdate.FHIRDate, False, None, False),
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
    from . import fhirreference
except ImportError:
    fhirreference = sys.modules[__package__ + '.fhirreference']
try:
    from . import usagecontext
except ImportError:
    usagecontext = sys.modules[__package__ + '.usagecontext']
