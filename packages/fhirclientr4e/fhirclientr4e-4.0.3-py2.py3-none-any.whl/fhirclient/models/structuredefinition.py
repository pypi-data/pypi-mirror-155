#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/StructureDefinition) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class StructureDefinition(domainresource.DomainResource):
    """ Structural Definition.
    
    A definition of a FHIR structure. This resource is used to describe the
    underlying resources, data types defined in FHIR, and also for describing
    extensions and constraints on resources and data types.
    """
    
    resource_type = "StructureDefinition"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['url'] = """Canonical identifier for this structure definition, represented as a URI (globally unique)."""
    _attribute_docstrings['identifier'] = """Additional identifier for the structure definition."""
    _attribute_docstrings['version'] = """Business version of the structure definition."""
    _attribute_docstrings['name'] = """Name for this structure definition (computer friendly)."""
    _attribute_docstrings['title'] = """Name for this structure definition (human friendly)."""
    _attribute_docstrings['status'] = """The status of this structure definition. Enables tracking the life-cycle of the content."""
    _attribute_docstrings['experimental'] = """For testing purposes, not real usage."""
    _attribute_docstrings['date'] = """Date last changed."""
    _attribute_docstrings['publisher'] = """Name of the publisher (organization or individual)."""
    _attribute_docstrings['contact'] = """Contact details for the publisher."""
    _attribute_docstrings['description'] = """Natural language description of the structure definition."""
    _attribute_docstrings['useContext'] = """The context that the content is intended to support."""
    _attribute_docstrings['jurisdiction'] = """Intended jurisdiction for structure definition (if applicable)."""
    _attribute_docstrings['purpose'] = """Why this structure definition is defined."""
    _attribute_docstrings['copyright'] = """Use and/or publishing restrictions."""
    _attribute_docstrings['keyword'] = """Assist with indexing and finding."""
    _attribute_docstrings['fhirVersion'] = """FHIR Version this StructureDefinition targets."""
    _attribute_docstrings['mapping'] = """External specification that the content is mapped to."""
    _attribute_docstrings['kind'] = """Defines the kind of structure that this definition is describing."""
    _attribute_docstrings['abstract'] = """Whether the structure is abstract."""
    _attribute_docstrings['context'] = """If an extension, where it can be used in instances."""
    _attribute_docstrings['contextInvariant'] = """FHIRPath invariants - when the extension can be used."""
    _attribute_docstrings['type'] = """Type defined or constrained by this structure."""
    _attribute_docstrings['baseDefinition'] = """Definition that this type is constrained/specialized from."""
    _attribute_docstrings['derivation'] = """How the type relates to the baseDefinition."""
    _attribute_docstrings['snapshot'] = """Snapshot view of the structure."""
    _attribute_docstrings['differential'] = """Differential view of the structure."""

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
        'url': 'http://hl7.org/fhir/structure-definition-kind',
        'restricted_to': ['primitive-type', 'complex-type', 'resource', 'logical'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['derivation'] = {
        'url': 'http://hl7.org/fhir/type-derivation-rule',
        'restricted_to': ['specialization', 'constraint'],
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
        """ Canonical identifier for this structure definition, represented as
        a URI (globally unique).
        Type `str`. """
        
        self.identifier = None
        """ Additional identifier for the structure definition.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.version = None
        """ Business version of the structure definition.
        Type `str`. """
        
        self.name = None
        """ Name for this structure definition (computer friendly).
        Type `str`. """
        
        self.title = None
        """ Name for this structure definition (human friendly).
        Type `str`. """
        
        self.status = None
        """ The status of this structure definition. Enables tracking the life-
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
        """ Natural language description of the structure definition.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for structure definition (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.purpose = None
        """ Why this structure definition is defined.
        Type `str`. """
        
        self.copyright = None
        """ Use and/or publishing restrictions.
        Type `str`. """
        
        self.keyword = None
        """ Assist with indexing and finding.
        List of `Coding` items (represented as `dict` in JSON). """
        
        self.fhirVersion = None
        """ FHIR Version this StructureDefinition targets.
        Type `str`. """
        
        self.mapping = None
        """ External specification that the content is mapped to.
        List of `StructureDefinitionMapping` items (represented as `dict` in JSON). """
        
        self.kind = None
        """ Defines the kind of structure that this definition is describing.
        Type `str`. """
        
        self.abstract = None
        """ Whether the structure is abstract.
        Type `bool`. """
        
        self.context = None
        """ If an extension, where it can be used in instances.
        List of `StructureDefinitionContext` items (represented as `dict` in JSON). """
        
        self.contextInvariant = None
        """ FHIRPath invariants - when the extension can be used.
        List of `str` items. """
        
        self.type = None
        """ Type defined or constrained by this structure.
        Type `str`. """
        
        self.baseDefinition = None
        """ Definition that this type is constrained/specialized from.
        Type `str`. """
        
        self.derivation = None
        """ How the type relates to the baseDefinition.
        Type `str`. """
        
        self.snapshot = None
        """ Snapshot view of the structure.
        Type `StructureDefinitionSnapshot` (represented as `dict` in JSON). """
        
        self.differential = None
        """ Differential view of the structure.
        Type `StructureDefinitionDifferential` (represented as `dict` in JSON). """
        
        super(StructureDefinition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(StructureDefinition, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, True),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
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
            ("purpose", "purpose", str, False, None, False),
            ("copyright", "copyright", str, False, None, False),
            ("keyword", "keyword", coding.Coding, True, None, False),
            ("fhirVersion", "fhirVersion", str, False, None, False),
            ("mapping", "mapping", StructureDefinitionMapping, True, None, False),
            ("kind", "kind", str, False, None, True),
            ("abstract", "abstract", bool, False, None, True),
            ("context", "context", StructureDefinitionContext, True, None, False),
            ("contextInvariant", "contextInvariant", str, True, None, False),
            ("type", "type", str, False, None, True),
            ("baseDefinition", "baseDefinition", str, False, None, False),
            ("derivation", "derivation", str, False, None, False),
            ("snapshot", "snapshot", StructureDefinitionSnapshot, False, None, False),
            ("differential", "differential", StructureDefinitionDifferential, False, None, False),
        ])
        return js


from . import backboneelement

class StructureDefinitionContext(backboneelement.BackboneElement):
    """ If an extension, where it can be used in instances.
    
    Identifies the types of resource or data type elements to which the
    extension can be applied.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Defines how to interpret the expression that defines what the context of the extension is."""
    _attribute_docstrings['expression'] = """Where the extension can be used in instances."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://hl7.org/fhir/extension-context-type',
        'restricted_to': ['fhirpath', 'element', 'extension'],
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
        """ Defines how to interpret the expression that defines what the
        context of the extension is.
        Type `str`. """
        
        self.expression = None
        """ Where the extension can be used in instances.
        Type `str`. """
        
        super(StructureDefinitionContext, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(StructureDefinitionContext, self).elementProperties()
        js.extend([
            ("type", "type", str, False, None, True),
            ("expression", "expression", str, False, None, True),
        ])
        return js


class StructureDefinitionDifferential(backboneelement.BackboneElement):
    """ Differential view of the structure.
    
    A differential view is expressed relative to the base StructureDefinition -
    a statement of differences that it applies.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['element'] = """Definition of elements in the resource (if no StructureDefinition)."""

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
        
        self.element = None
        """ Definition of elements in the resource (if no StructureDefinition).
        List of `ElementDefinition` items (represented as `dict` in JSON). """
        
        super(StructureDefinitionDifferential, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(StructureDefinitionDifferential, self).elementProperties()
        js.extend([
            ("element", "element", elementdefinition.ElementDefinition, True, None, True),
        ])
        return js


class StructureDefinitionMapping(backboneelement.BackboneElement):
    """ External specification that the content is mapped to.
    
    An external specification that the content is mapped to.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identity'] = """Internal id when this mapping is used."""
    _attribute_docstrings['uri'] = """Identifies what this mapping refers to."""
    _attribute_docstrings['name'] = """Names what this mapping refers to."""
    _attribute_docstrings['comment'] = """Versions, Issues, Scope limitations etc.."""

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
        
        self.identity = None
        """ Internal id when this mapping is used.
        Type `str`. """
        
        self.uri = None
        """ Identifies what this mapping refers to.
        Type `str`. """
        
        self.name = None
        """ Names what this mapping refers to.
        Type `str`. """
        
        self.comment = None
        """ Versions, Issues, Scope limitations etc.
        Type `str`. """
        
        super(StructureDefinitionMapping, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(StructureDefinitionMapping, self).elementProperties()
        js.extend([
            ("identity", "identity", str, False, None, True),
            ("uri", "uri", str, False, None, False),
            ("name", "name", str, False, None, False),
            ("comment", "comment", str, False, None, False),
        ])
        return js


class StructureDefinitionSnapshot(backboneelement.BackboneElement):
    """ Snapshot view of the structure.
    
    A snapshot view is expressed in a standalone form that can be used and
    interpreted without considering the base StructureDefinition.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['element'] = """Definition of elements in the resource (if no StructureDefinition)."""

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
        
        self.element = None
        """ Definition of elements in the resource (if no StructureDefinition).
        List of `ElementDefinition` items (represented as `dict` in JSON). """
        
        super(StructureDefinitionSnapshot, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(StructureDefinitionSnapshot, self).elementProperties()
        js.extend([
            ("element", "element", elementdefinition.ElementDefinition, True, None, True),
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
    from . import elementdefinition
except ImportError:
    elementdefinition = sys.modules[__package__ + '.elementdefinition']
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
