#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/CodeSystem) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class CodeSystem(domainresource.DomainResource):
    """ Declares the existence of and describes a code system or code system
    supplement.
    
    The CodeSystem resource is used to declare the existence of and describe a
    code system or code system supplement and its key properties, and
    optionally define a part or all of its content.
    """
    
    resource_type = "CodeSystem"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['url'] = """Canonical identifier for this code system, represented as a URI (globally unique) (Coding.system)."""
    _attribute_docstrings['identifier'] = """Additional identifier for the code system (business identifier)."""
    _attribute_docstrings['version'] = """Business version of the code system (Coding.version)."""
    _attribute_docstrings['name'] = """Name for this code system (computer friendly)."""
    _attribute_docstrings['title'] = """Name for this code system (human friendly)."""
    _attribute_docstrings['status'] = """The date (and optionally time) when the code system resource was created or revised."""
    _attribute_docstrings['experimental'] = """For testing purposes, not real usage."""
    _attribute_docstrings['date'] = """Date last changed."""
    _attribute_docstrings['publisher'] = """Name of the publisher (organization or individual)."""
    _attribute_docstrings['contact'] = """Contact details for the publisher."""
    _attribute_docstrings['description'] = """Natural language description of the code system."""
    _attribute_docstrings['useContext'] = """The context that the content is intended to support."""
    _attribute_docstrings['jurisdiction'] = """Intended jurisdiction for code system (if applicable)."""
    _attribute_docstrings['purpose'] = """Why this code system is defined."""
    _attribute_docstrings['copyright'] = """Use and/or publishing restrictions."""
    _attribute_docstrings['caseSensitive'] = """If code comparison is case sensitive."""
    _attribute_docstrings['valueSet'] = """Canonical reference to the value set with entire code system."""
    _attribute_docstrings['hierarchyMeaning'] = """The meaning of the hierarchy of concepts as represented in this resource."""
    _attribute_docstrings['compositional'] = """If code system defines a compositional grammar."""
    _attribute_docstrings['versionNeeded'] = """If definitions are not stable."""
    _attribute_docstrings['content'] = """The extent of the content of the code system (the concepts and codes it defines) are represented in this resource instance."""
    _attribute_docstrings['supplements'] = """Canonical URL of Code System this adds designations and properties to."""
    _attribute_docstrings['count'] = """Total concepts in the code system."""
    _attribute_docstrings['filter'] = """Filter that can be used in a value set."""
    _attribute_docstrings['property'] = """Additional information supplied about each concept."""
    _attribute_docstrings['concept'] = """Concepts in the code system."""

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
    _attribute_enums['hierarchyMeaning'] = {
        'url': 'http://hl7.org/fhir/codesystem-hierarchy-meaning',
        'restricted_to': ['grouped-by', 'is-a', 'part-of', 'classified-with'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['content'] = {
        'url': 'http://hl7.org/fhir/codesystem-content-mode',
        'restricted_to': ['not-present', 'example', 'fragment', 'complete', 'supplement'],
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
        """ Canonical identifier for this code system, represented as a URI
        (globally unique) (Coding.system).
        Type `str`. """
        
        self.identifier = None
        """ Additional identifier for the code system (business identifier).
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.version = None
        """ Business version of the code system (Coding.version).
        Type `str`. """
        
        self.name = None
        """ Name for this code system (computer friendly).
        Type `str`. """
        
        self.title = None
        """ Name for this code system (human friendly).
        Type `str`. """
        
        self.status = None
        """ The date (and optionally time) when the code system resource was
        created or revised.
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
        """ Natural language description of the code system.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for code system (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.purpose = None
        """ Why this code system is defined.
        Type `str`. """
        
        self.copyright = None
        """ Use and/or publishing restrictions.
        Type `str`. """
        
        self.caseSensitive = None
        """ If code comparison is case sensitive.
        Type `bool`. """
        
        self.valueSet = None
        """ Canonical reference to the value set with entire code system.
        Type `str`. """
        
        self.hierarchyMeaning = None
        """ The meaning of the hierarchy of concepts as represented in this
        resource.
        Type `str`. """
        
        self.compositional = None
        """ If code system defines a compositional grammar.
        Type `bool`. """
        
        self.versionNeeded = None
        """ If definitions are not stable.
        Type `bool`. """
        
        self.content = None
        """ The extent of the content of the code system (the concepts and
        codes it defines) are represented in this resource instance.
        Type `str`. """
        
        self.supplements = None
        """ Canonical URL of Code System this adds designations and properties
        to.
        Type `str`. """
        
        self.count = None
        """ Total concepts in the code system.
        Type `int`. """
        
        self.filter = None
        """ Filter that can be used in a value set.
        List of `CodeSystemFilter` items (represented as `dict` in JSON). """
        
        self.property = None
        """ Additional information supplied about each concept.
        List of `CodeSystemProperty` items (represented as `dict` in JSON). """
        
        self.concept = None
        """ Concepts in the code system.
        List of `CodeSystemConcept` items (represented as `dict` in JSON). """
        
        super(CodeSystem, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CodeSystem, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("version", "version", str, False, None, False),
            ("name", "name", str, False, None, False),
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
            ("caseSensitive", "caseSensitive", bool, False, None, False),
            ("valueSet", "valueSet", str, False, None, False),
            ("hierarchyMeaning", "hierarchyMeaning", str, False, None, False),
            ("compositional", "compositional", bool, False, None, False),
            ("versionNeeded", "versionNeeded", bool, False, None, False),
            ("content", "content", str, False, None, True),
            ("supplements", "supplements", str, False, None, False),
            ("count", "count", int, False, None, False),
            ("filter", "filter", CodeSystemFilter, True, None, False),
            ("property", "property", CodeSystemProperty, True, None, False),
            ("concept", "concept", CodeSystemConcept, True, None, False),
        ])
        return js


from . import backboneelement

class CodeSystemConcept(backboneelement.BackboneElement):
    """ Concepts in the code system.
    
    Concepts that are in the code system. The concept definitions are
    inherently hierarchical, but the definitions must be consulted to determine
    what the meanings of the hierarchical relationships are.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Code that identifies concept."""
    _attribute_docstrings['display'] = """Text to display to the user."""
    _attribute_docstrings['definition'] = """Formal definition."""
    _attribute_docstrings['designation'] = """Additional representations for the concept."""
    _attribute_docstrings['property'] = """Property value for the concept."""
    _attribute_docstrings['concept'] = """Child Concepts (is-a/contains/categorizes)."""

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
        """ Code that identifies concept.
        Type `str`. """
        
        self.display = None
        """ Text to display to the user.
        Type `str`. """
        
        self.definition = None
        """ Formal definition.
        Type `str`. """
        
        self.designation = None
        """ Additional representations for the concept.
        List of `CodeSystemConceptDesignation` items (represented as `dict` in JSON). """
        
        self.property = None
        """ Property value for the concept.
        List of `CodeSystemConceptProperty` items (represented as `dict` in JSON). """
        
        self.concept = None
        """ Child Concepts (is-a/contains/categorizes).
        List of `CodeSystemConcept` items (represented as `dict` in JSON). """
        
        super(CodeSystemConcept, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CodeSystemConcept, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, True),
            ("display", "display", str, False, None, False),
            ("definition", "definition", str, False, None, False),
            ("designation", "designation", CodeSystemConceptDesignation, True, None, False),
            ("property", "property", CodeSystemConceptProperty, True, None, False),
            ("concept", "concept", CodeSystemConcept, True, None, False),
        ])
        return js


class CodeSystemConceptDesignation(backboneelement.BackboneElement):
    """ Additional representations for the concept.
    
    Additional representations for the concept - other languages, aliases,
    specialized purposes, used for particular purposes, etc.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['language'] = """Human language of the designation."""
    _attribute_docstrings['use'] = """Details how this designation would be used."""
    _attribute_docstrings['value'] = """The text value for this designation."""

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
        
        self.language = None
        """ Human language of the designation.
        Type `str`. """
        
        self.use = None
        """ Details how this designation would be used.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.value = None
        """ The text value for this designation.
        Type `str`. """
        
        super(CodeSystemConceptDesignation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CodeSystemConceptDesignation, self).elementProperties()
        js.extend([
            ("language", "language", str, False, None, False),
            ("use", "use", coding.Coding, False, None, False),
            ("value", "value", str, False, None, True),
        ])
        return js


class CodeSystemConceptProperty(backboneelement.BackboneElement):
    """ Property value for the concept.
    
    A property value for this concept.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Reference to CodeSystem.property.code."""
    _attribute_docstrings['valueCode'] = """Value of the property for this concept."""
    _attribute_docstrings['valueCoding'] = """Value of the property for this concept."""
    _attribute_docstrings['valueString'] = """Value of the property for this concept."""
    _attribute_docstrings['valueInteger'] = """Value of the property for this concept."""
    _attribute_docstrings['valueBoolean'] = """Value of the property for this concept."""
    _attribute_docstrings['valueDateTime'] = """Value of the property for this concept."""
    _attribute_docstrings['valueDecimal'] = """Value of the property for this concept."""

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
        """ Reference to CodeSystem.property.code.
        Type `str`. """
        
        self.valueCode = None
        """ Value of the property for this concept.
        Type `str`. """
        
        self.valueCoding = None
        """ Value of the property for this concept.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.valueString = None
        """ Value of the property for this concept.
        Type `str`. """
        
        self.valueInteger = None
        """ Value of the property for this concept.
        Type `int`. """
        
        self.valueBoolean = None
        """ Value of the property for this concept.
        Type `bool`. """
        
        self.valueDateTime = None
        """ Value of the property for this concept.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valueDecimal = None
        """ Value of the property for this concept.
        Type `float`. """
        
        super(CodeSystemConceptProperty, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CodeSystemConceptProperty, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, True),
            ("valueCode", "valueCode", str, False, "value", True),
            ("valueCoding", "valueCoding", coding.Coding, False, "value", True),
            ("valueString", "valueString", str, False, "value", True),
            ("valueInteger", "valueInteger", int, False, "value", True),
            ("valueBoolean", "valueBoolean", bool, False, "value", True),
            ("valueDateTime", "valueDateTime", fhirdate.FHIRDate, False, "value", True),
            ("valueDecimal", "valueDecimal", float, False, "value", True),
        ])
        return js


class CodeSystemFilter(backboneelement.BackboneElement):
    """ Filter that can be used in a value set.
    
    A filter that can be used in a value set compose statement when selecting
    concepts using a filter.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Code that identifies the filter."""
    _attribute_docstrings['description'] = """How or why the filter is used."""
    _attribute_docstrings['operator'] = """A list of operators that can be used with the filter."""
    _attribute_docstrings['value'] = """What to use for the value."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['operator'] = {
        'url': 'http://hl7.org/fhir/filter-operator',
        'restricted_to': ['=', 'is-a', 'descendent-of', 'is-not-a', 'regex', 'in', 'not-in', 'generalizes', 'exists'],
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
        """ Code that identifies the filter.
        Type `str`. """
        
        self.description = None
        """ How or why the filter is used.
        Type `str`. """
        
        self.operator = None
        """ A list of operators that can be used with the filter.
        List of `str` items. """
        
        self.value = None
        """ What to use for the value.
        Type `str`. """
        
        super(CodeSystemFilter, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CodeSystemFilter, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, True),
            ("description", "description", str, False, None, False),
            ("operator", "operator", str, True, None, True),
            ("value", "value", str, False, None, True),
        ])
        return js


class CodeSystemProperty(backboneelement.BackboneElement):
    """ Additional information supplied about each concept.
    
    A property defines an additional slot through which additional information
    can be provided about a concept.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Identifies the property on the concepts, and when referred to in operations."""
    _attribute_docstrings['uri'] = """Formal identifier for the property."""
    _attribute_docstrings['description'] = """Why the property is defined, and/or what it conveys."""
    _attribute_docstrings['type'] = """The type of the property value. Properties of type "code" contain a code defined by the code system (e.g. a reference to another defined concept)."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://hl7.org/fhir/concept-property-type',
        'restricted_to': ['code', 'Coding', 'string', 'integer', 'boolean', 'dateTime', 'decimal'],
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
        """ Identifies the property on the concepts, and when referred to in
        operations.
        Type `str`. """
        
        self.uri = None
        """ Formal identifier for the property.
        Type `str`. """
        
        self.description = None
        """ Why the property is defined, and/or what it conveys.
        Type `str`. """
        
        self.type = None
        """ The type of the property value. Properties of type "code" contain a
        code defined by the code system (e.g. a reference to another
        defined concept).
        Type `str`. """
        
        super(CodeSystemProperty, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CodeSystemProperty, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, True),
            ("uri", "uri", str, False, None, False),
            ("description", "description", str, False, None, False),
            ("type", "type", str, False, None, True),
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
