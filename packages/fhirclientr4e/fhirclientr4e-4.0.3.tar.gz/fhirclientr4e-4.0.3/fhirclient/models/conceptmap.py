#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/ConceptMap) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class ConceptMap(domainresource.DomainResource):
    """ A map from one set of concepts to one or more other concepts.
    
    A statement of relationships from one set of concepts to one or more other
    concepts - either concepts in code systems, or data element/data element
    concepts, or classes in class models.
    """
    
    resource_type = "ConceptMap"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['url'] = """Canonical identifier for this concept map, represented as a URI (globally unique)."""
    _attribute_docstrings['identifier'] = """Additional identifier for the concept map."""
    _attribute_docstrings['version'] = """Business version of the concept map."""
    _attribute_docstrings['name'] = """Name for this concept map (computer friendly)."""
    _attribute_docstrings['title'] = """Name for this concept map (human friendly)."""
    _attribute_docstrings['status'] = """The status of this concept map. Enables tracking the life-cycle of the content."""
    _attribute_docstrings['experimental'] = """For testing purposes, not real usage."""
    _attribute_docstrings['date'] = """Date last changed."""
    _attribute_docstrings['publisher'] = """Name of the publisher (organization or individual)."""
    _attribute_docstrings['contact'] = """Contact details for the publisher."""
    _attribute_docstrings['description'] = """Natural language description of the concept map."""
    _attribute_docstrings['useContext'] = """The context that the content is intended to support."""
    _attribute_docstrings['jurisdiction'] = """Intended jurisdiction for concept map (if applicable)."""
    _attribute_docstrings['purpose'] = """Why this concept map is defined."""
    _attribute_docstrings['copyright'] = """Use and/or publishing restrictions."""
    _attribute_docstrings['sourceUri'] = """The source value set that contains the concepts that are being mapped."""
    _attribute_docstrings['sourceCanonical'] = """The source value set that contains the concepts that are being mapped."""
    _attribute_docstrings['targetUri'] = """The target value set which provides context for the mappings."""
    _attribute_docstrings['targetCanonical'] = """The target value set which provides context for the mappings."""
    _attribute_docstrings['group'] = """Same source and target systems."""

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
        """ Canonical identifier for this concept map, represented as a URI
        (globally unique).
        Type `str`. """
        
        self.identifier = None
        """ Additional identifier for the concept map.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.version = None
        """ Business version of the concept map.
        Type `str`. """
        
        self.name = None
        """ Name for this concept map (computer friendly).
        Type `str`. """
        
        self.title = None
        """ Name for this concept map (human friendly).
        Type `str`. """
        
        self.status = None
        """ The status of this concept map. Enables tracking the life-cycle of
        the content.
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
        """ Natural language description of the concept map.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for concept map (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.purpose = None
        """ Why this concept map is defined.
        Type `str`. """
        
        self.copyright = None
        """ Use and/or publishing restrictions.
        Type `str`. """
        
        self.sourceUri = None
        """ The source value set that contains the concepts that are being
        mapped.
        Type `str`. """
        
        self.sourceCanonical = None
        """ The source value set that contains the concepts that are being
        mapped.
        Type `str`. """
        
        self.targetUri = None
        """ The target value set which provides context for the mappings.
        Type `str`. """
        
        self.targetCanonical = None
        """ The target value set which provides context for the mappings.
        Type `str`. """
        
        self.group = None
        """ Same source and target systems.
        List of `ConceptMapGroup` items (represented as `dict` in JSON). """
        
        super(ConceptMap, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ConceptMap, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, False),
            ("identifier", "identifier", identifier.Identifier, False, None, False),
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
            ("sourceUri", "sourceUri", str, False, "source", False),
            ("sourceCanonical", "sourceCanonical", str, False, "source", False),
            ("targetUri", "targetUri", str, False, "target", False),
            ("targetCanonical", "targetCanonical", str, False, "target", False),
            ("group", "group", ConceptMapGroup, True, None, False),
        ])
        return js


from . import backboneelement

class ConceptMapGroup(backboneelement.BackboneElement):
    """ Same source and target systems.
    
    A group of mappings that all have the same source and target system.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['source'] = """Source system where concepts to be mapped are defined."""
    _attribute_docstrings['sourceVersion'] = """Specific version of the  code system."""
    _attribute_docstrings['target'] = """Target system that the concepts are to be mapped to."""
    _attribute_docstrings['targetVersion'] = """Specific version of the  code system."""
    _attribute_docstrings['element'] = """Mappings for a concept from the source set."""
    _attribute_docstrings['unmapped'] = """What to do when there is no mapping for the source concept."""

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
        """ Source system where concepts to be mapped are defined.
        Type `str`. """
        
        self.sourceVersion = None
        """ Specific version of the  code system.
        Type `str`. """
        
        self.target = None
        """ Target system that the concepts are to be mapped to.
        Type `str`. """
        
        self.targetVersion = None
        """ Specific version of the  code system.
        Type `str`. """
        
        self.element = None
        """ Mappings for a concept from the source set.
        List of `ConceptMapGroupElement` items (represented as `dict` in JSON). """
        
        self.unmapped = None
        """ What to do when there is no mapping for the source concept.
        Type `ConceptMapGroupUnmapped` (represented as `dict` in JSON). """
        
        super(ConceptMapGroup, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ConceptMapGroup, self).elementProperties()
        js.extend([
            ("source", "source", str, False, None, False),
            ("sourceVersion", "sourceVersion", str, False, None, False),
            ("target", "target", str, False, None, False),
            ("targetVersion", "targetVersion", str, False, None, False),
            ("element", "element", ConceptMapGroupElement, True, None, True),
            ("unmapped", "unmapped", ConceptMapGroupUnmapped, False, None, False),
        ])
        return js


class ConceptMapGroupElement(backboneelement.BackboneElement):
    """ Mappings for a concept from the source set.
    
    Mappings for an individual concept in the source to one or more concepts in
    the target.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Identifies element being mapped."""
    _attribute_docstrings['display'] = """Display for the code."""
    _attribute_docstrings['target'] = """Concept in target system for element."""

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
        """ Identifies element being mapped.
        Type `str`. """
        
        self.display = None
        """ Display for the code.
        Type `str`. """
        
        self.target = None
        """ Concept in target system for element.
        List of `ConceptMapGroupElementTarget` items (represented as `dict` in JSON). """
        
        super(ConceptMapGroupElement, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ConceptMapGroupElement, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, False),
            ("display", "display", str, False, None, False),
            ("target", "target", ConceptMapGroupElementTarget, True, None, False),
        ])
        return js


class ConceptMapGroupElementTarget(backboneelement.BackboneElement):
    """ Concept in target system for element.
    
    A concept from the target value set that this concept maps to.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Code that identifies the target element."""
    _attribute_docstrings['display'] = """Display for the code."""
    _attribute_docstrings['equivalence'] = """The equivalence between the source and target concepts (counting for the dependencies and products). The equivalence is read from target to source (e.g. the target is 'wider' than the source)."""
    _attribute_docstrings['comment'] = """Description of status/issues in mapping."""
    _attribute_docstrings['dependsOn'] = """Other elements required for this mapping (from context)."""
    _attribute_docstrings['product'] = """Other concepts that this mapping also produces."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['equivalence'] = {
        'url': 'http://hl7.org/fhir/concept-map-equivalence',
        'restricted_to': ['relatedto', 'equivalent', 'equal', 'wider', 'subsumes', 'narrower', 'specializes', 'inexact', 'unmatched', 'disjoint'],
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
        """ Code that identifies the target element.
        Type `str`. """
        
        self.display = None
        """ Display for the code.
        Type `str`. """
        
        self.equivalence = None
        """ The equivalence between the source and target concepts (counting
        for the dependencies and products). The equivalence is read from
        target to source (e.g. the target is 'wider' than the source).
        Type `str`. """
        
        self.comment = None
        """ Description of status/issues in mapping.
        Type `str`. """
        
        self.dependsOn = None
        """ Other elements required for this mapping (from context).
        List of `ConceptMapGroupElementTargetDependsOn` items (represented as `dict` in JSON). """
        
        self.product = None
        """ Other concepts that this mapping also produces.
        List of `ConceptMapGroupElementTargetDependsOn` items (represented as `dict` in JSON). """
        
        super(ConceptMapGroupElementTarget, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ConceptMapGroupElementTarget, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, False),
            ("display", "display", str, False, None, False),
            ("equivalence", "equivalence", str, False, None, True),
            ("comment", "comment", str, False, None, False),
            ("dependsOn", "dependsOn", ConceptMapGroupElementTargetDependsOn, True, None, False),
            ("product", "product", ConceptMapGroupElementTargetDependsOn, True, None, False),
        ])
        return js


class ConceptMapGroupElementTargetDependsOn(backboneelement.BackboneElement):
    """ Other elements required for this mapping (from context).
    
    A set of additional dependencies for this mapping to hold. This mapping is
    only applicable if the specified element can be resolved, and it has the
    specified value.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['property'] = """Reference to property mapping depends on."""
    _attribute_docstrings['system'] = """Code System (if necessary)."""
    _attribute_docstrings['value'] = """Value of the referenced element."""
    _attribute_docstrings['display'] = """Display for the code (if value is a code)."""

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
        
        self.property = None
        """ Reference to property mapping depends on.
        Type `str`. """
        
        self.system = None
        """ Code System (if necessary).
        Type `str`. """
        
        self.value = None
        """ Value of the referenced element.
        Type `str`. """
        
        self.display = None
        """ Display for the code (if value is a code).
        Type `str`. """
        
        super(ConceptMapGroupElementTargetDependsOn, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ConceptMapGroupElementTargetDependsOn, self).elementProperties()
        js.extend([
            ("property", "property", str, False, None, True),
            ("system", "system", str, False, None, False),
            ("value", "value", str, False, None, True),
            ("display", "display", str, False, None, False),
        ])
        return js


class ConceptMapGroupUnmapped(backboneelement.BackboneElement):
    """ What to do when there is no mapping for the source concept.
    
    What to do when there is no mapping for the source concept. "Unmapped" does
    not include codes that are unmatched, and the unmapped element is ignored
    in a code is specified to have equivalence = unmatched.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['mode'] = """Defines which action to take if there is no match for the source concept in the target system designated for the group. One of 3 actions are possible: use the unmapped code (this is useful when doing a mapping between versions, and only a few codes have changed), use a fixed code (a default code), or alternatively, a reference to a different concept map can be provided (by canonical URL)."""
    _attribute_docstrings['code'] = """Fixed code when mode = fixed."""
    _attribute_docstrings['display'] = """Display for the code."""
    _attribute_docstrings['url'] = """canonical reference to an additional ConceptMap to use for mapping if the source concept is unmapped."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['mode'] = {
        'url': 'http://hl7.org/fhir/conceptmap-unmapped-mode',
        'restricted_to': ['provided', 'fixed', 'other-map'],
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
        """ Defines which action to take if there is no match for the source
        concept in the target system designated for the group. One of 3
        actions are possible: use the unmapped code (this is useful when
        doing a mapping between versions, and only a few codes have
        changed), use a fixed code (a default code), or alternatively, a
        reference to a different concept map can be provided (by canonical
        URL).
        Type `str`. """
        
        self.code = None
        """ Fixed code when mode = fixed.
        Type `str`. """
        
        self.display = None
        """ Display for the code.
        Type `str`. """
        
        self.url = None
        """ canonical reference to an additional ConceptMap to use for mapping
        if the source concept is unmapped.
        Type `str`. """
        
        super(ConceptMapGroupUnmapped, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ConceptMapGroupUnmapped, self).elementProperties()
        js.extend([
            ("mode", "mode", str, False, None, True),
            ("code", "code", str, False, None, False),
            ("display", "display", str, False, None, False),
            ("url", "url", str, False, None, False),
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
