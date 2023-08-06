#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/StructureMap) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class StructureMap(domainresource.DomainResource):
    """ A Map of relationships between 2 structures that can be used to transform
    data.
    """
    
    resource_type = "StructureMap"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['url'] = """Canonical identifier for this structure map, represented as a URI (globally unique)."""
    _attribute_docstrings['identifier'] = """Additional identifier for the structure map."""
    _attribute_docstrings['version'] = """Business version of the structure map."""
    _attribute_docstrings['name'] = """Name for this structure map (computer friendly)."""
    _attribute_docstrings['title'] = """Name for this structure map (human friendly)."""
    _attribute_docstrings['status'] = """The status of this structure map. Enables tracking the life-cycle of the content."""
    _attribute_docstrings['experimental'] = """For testing purposes, not real usage."""
    _attribute_docstrings['date'] = """Date last changed."""
    _attribute_docstrings['publisher'] = """Name of the publisher (organization or individual)."""
    _attribute_docstrings['contact'] = """Contact details for the publisher."""
    _attribute_docstrings['description'] = """Natural language description of the structure map."""
    _attribute_docstrings['useContext'] = """The context that the content is intended to support."""
    _attribute_docstrings['jurisdiction'] = """Intended jurisdiction for structure map (if applicable)."""
    _attribute_docstrings['purpose'] = """Why this structure map is defined."""
    _attribute_docstrings['copyright'] = """Use and/or publishing restrictions."""
    _attribute_docstrings['structure'] = """Structure Definition used by this map."""
    _attribute_docstrings['import_fhir'] = """Other maps used by this map (canonical URLs)."""
    _attribute_docstrings['group'] = """Named sections for reader convenience."""

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
        """ Canonical identifier for this structure map, represented as a URI
        (globally unique).
        Type `str`. """
        
        self.identifier = None
        """ Additional identifier for the structure map.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.version = None
        """ Business version of the structure map.
        Type `str`. """
        
        self.name = None
        """ Name for this structure map (computer friendly).
        Type `str`. """
        
        self.title = None
        """ Name for this structure map (human friendly).
        Type `str`. """
        
        self.status = None
        """ The status of this structure map. Enables tracking the life-cycle
        of the content.
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
        """ Natural language description of the structure map.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for structure map (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.purpose = None
        """ Why this structure map is defined.
        Type `str`. """
        
        self.copyright = None
        """ Use and/or publishing restrictions.
        Type `str`. """
        
        self.structure = None
        """ Structure Definition used by this map.
        List of `StructureMapStructure` items (represented as `dict` in JSON). """
        
        self.import_fhir = None
        """ Other maps used by this map (canonical URLs).
        List of `str` items. """
        
        self.group = None
        """ Named sections for reader convenience.
        List of `StructureMapGroup` items (represented as `dict` in JSON). """
        
        super(StructureMap, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(StructureMap, self).elementProperties()
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
            ("structure", "structure", StructureMapStructure, True, None, False),
            ("import_fhir", "import", str, True, None, False),
            ("group", "group", StructureMapGroup, True, None, True),
        ])
        return js


from . import backboneelement

class StructureMapGroup(backboneelement.BackboneElement):
    """ Named sections for reader convenience.
    
    Organizes the mapping into manageable chunks for human review/ease of
    maintenance.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['name'] = """Human-readable label."""
    _attribute_docstrings['extends'] = """Another group that this group adds rules to."""
    _attribute_docstrings['typeMode'] = """If this is the default rule set to apply for the source type or this combination of types."""
    _attribute_docstrings['documentation'] = """Additional description/explanation for group."""
    _attribute_docstrings['input'] = """Named instance provided when invoking the map."""
    _attribute_docstrings['rule'] = """Transform Rule from source to target."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['typeMode'] = {
        'url': 'http://hl7.org/fhir/map-group-type-mode',
        'restricted_to': ['none', 'types', 'type-and-types'],
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
        """ Human-readable label.
        Type `str`. """
        
        self.extends = None
        """ Another group that this group adds rules to.
        Type `str`. """
        
        self.typeMode = None
        """ If this is the default rule set to apply for the source type or
        this combination of types.
        Type `str`. """
        
        self.documentation = None
        """ Additional description/explanation for group.
        Type `str`. """
        
        self.input = None
        """ Named instance provided when invoking the map.
        List of `StructureMapGroupInput` items (represented as `dict` in JSON). """
        
        self.rule = None
        """ Transform Rule from source to target.
        List of `StructureMapGroupRule` items (represented as `dict` in JSON). """
        
        super(StructureMapGroup, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(StructureMapGroup, self).elementProperties()
        js.extend([
            ("name", "name", str, False, None, True),
            ("extends", "extends", str, False, None, False),
            ("typeMode", "typeMode", str, False, None, True),
            ("documentation", "documentation", str, False, None, False),
            ("input", "input", StructureMapGroupInput, True, None, True),
            ("rule", "rule", StructureMapGroupRule, True, None, True),
        ])
        return js


class StructureMapGroupInput(backboneelement.BackboneElement):
    """ Named instance provided when invoking the map.
    
    A name assigned to an instance of data. The instance must be provided when
    the mapping is invoked.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['name'] = """Name for this instance of data."""
    _attribute_docstrings['type'] = """Type for this instance of data."""
    _attribute_docstrings['mode'] = """Mode for this instance of data."""
    _attribute_docstrings['documentation'] = """Documentation for this instance of data."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['mode'] = {
        'url': 'http://hl7.org/fhir/map-input-mode',
        'restricted_to': ['source', 'target'],
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
        """ Name for this instance of data.
        Type `str`. """
        
        self.type = None
        """ Type for this instance of data.
        Type `str`. """
        
        self.mode = None
        """ Mode for this instance of data.
        Type `str`. """
        
        self.documentation = None
        """ Documentation for this instance of data.
        Type `str`. """
        
        super(StructureMapGroupInput, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(StructureMapGroupInput, self).elementProperties()
        js.extend([
            ("name", "name", str, False, None, True),
            ("type", "type", str, False, None, False),
            ("mode", "mode", str, False, None, True),
            ("documentation", "documentation", str, False, None, False),
        ])
        return js


class StructureMapGroupRule(backboneelement.BackboneElement):
    """ Transform Rule from source to target.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['name'] = """Name of the rule for internal references."""
    _attribute_docstrings['source'] = """Source inputs to the mapping."""
    _attribute_docstrings['target'] = """Content to create because of this mapping rule."""
    _attribute_docstrings['rule'] = """Rules contained in this rule."""
    _attribute_docstrings['dependent'] = """Which other rules to apply in the context of this rule."""
    _attribute_docstrings['documentation'] = """Documentation for this instance of data."""

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
        """ Name of the rule for internal references.
        Type `str`. """
        
        self.source = None
        """ Source inputs to the mapping.
        List of `StructureMapGroupRuleSource` items (represented as `dict` in JSON). """
        
        self.target = None
        """ Content to create because of this mapping rule.
        List of `StructureMapGroupRuleTarget` items (represented as `dict` in JSON). """
        
        self.rule = None
        """ Rules contained in this rule.
        List of `StructureMapGroupRule` items (represented as `dict` in JSON). """
        
        self.dependent = None
        """ Which other rules to apply in the context of this rule.
        List of `StructureMapGroupRuleDependent` items (represented as `dict` in JSON). """
        
        self.documentation = None
        """ Documentation for this instance of data.
        Type `str`. """
        
        super(StructureMapGroupRule, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(StructureMapGroupRule, self).elementProperties()
        js.extend([
            ("name", "name", str, False, None, True),
            ("source", "source", StructureMapGroupRuleSource, True, None, True),
            ("target", "target", StructureMapGroupRuleTarget, True, None, False),
            ("rule", "rule", StructureMapGroupRule, True, None, False),
            ("dependent", "dependent", StructureMapGroupRuleDependent, True, None, False),
            ("documentation", "documentation", str, False, None, False),
        ])
        return js


class StructureMapGroupRuleDependent(backboneelement.BackboneElement):
    """ Which other rules to apply in the context of this rule.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['name'] = """Name of a rule or group to apply."""
    _attribute_docstrings['variable'] = """Variable to pass to the rule or group."""

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
        """ Name of a rule or group to apply.
        Type `str`. """
        
        self.variable = None
        """ Variable to pass to the rule or group.
        List of `str` items. """
        
        super(StructureMapGroupRuleDependent, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(StructureMapGroupRuleDependent, self).elementProperties()
        js.extend([
            ("name", "name", str, False, None, True),
            ("variable", "variable", str, True, None, True),
        ])
        return js


class StructureMapGroupRuleSource(backboneelement.BackboneElement):
    """ Source inputs to the mapping.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['context'] = """Type or variable this rule applies to."""
    _attribute_docstrings['min'] = """Specified minimum cardinality."""
    _attribute_docstrings['max'] = """Specified maximum cardinality (number or *)."""
    _attribute_docstrings['type'] = """Rule only applies if source has this type."""
    _attribute_docstrings['defaultValueBase64Binary'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueBoolean'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueCanonical'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueCode'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueDate'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueDateTime'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueDecimal'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueId'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueInstant'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueInteger'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueMarkdown'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueOid'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValuePositiveInt'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueString'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueTime'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueUnsignedInt'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueUri'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueUrl'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueUuid'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueAddress'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueAge'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueAnnotation'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueAttachment'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueCodeableConcept'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueCoding'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueContactPoint'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueCount'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueDistance'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueDuration'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueHumanName'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueIdentifier'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueMoney'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValuePeriod'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueQuantity'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueRange'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueRatio'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueReference'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueSampledData'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueSignature'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueTiming'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueContactDetail'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueContributor'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueDataRequirement'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueExpression'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueParameterDefinition'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueRelatedArtifact'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueTriggerDefinition'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueUsageContext'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueDosage'] = """Default value if no value exists."""
    _attribute_docstrings['defaultValueMeta'] = """Default value if no value exists."""
    _attribute_docstrings['element'] = """Optional field for this source."""
    _attribute_docstrings['listMode'] = """How to handle the list mode for this element."""
    _attribute_docstrings['variable'] = """Named context for field, if a field is specified."""
    _attribute_docstrings['condition'] = """FHIRPath expression  - must be true or the rule does not apply."""
    _attribute_docstrings['check'] = """FHIRPath expression  - must be true or the mapping engine throws an error instead of completing."""
    _attribute_docstrings['logMessage'] = """Message to put in log if source exists (FHIRPath)."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['listMode'] = {
        'url': 'http://hl7.org/fhir/map-source-list-mode',
        'restricted_to': ['first', 'not_first', 'last', 'not_last', 'only_one'],
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
        
        self.context = None
        """ Type or variable this rule applies to.
        Type `str`. """
        
        self.min = None
        """ Specified minimum cardinality.
        Type `int`. """
        
        self.max = None
        """ Specified maximum cardinality (number or *).
        Type `str`. """
        
        self.type = None
        """ Rule only applies if source has this type.
        Type `str`. """
        
        self.defaultValueBase64Binary = None
        """ Default value if no value exists.
        Type `str`. """
        
        self.defaultValueBoolean = None
        """ Default value if no value exists.
        Type `bool`. """
        
        self.defaultValueCanonical = None
        """ Default value if no value exists.
        Type `str`. """
        
        self.defaultValueCode = None
        """ Default value if no value exists.
        Type `str`. """
        
        self.defaultValueDate = None
        """ Default value if no value exists.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.defaultValueDateTime = None
        """ Default value if no value exists.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.defaultValueDecimal = None
        """ Default value if no value exists.
        Type `float`. """
        
        self.defaultValueId = None
        """ Default value if no value exists.
        Type `str`. """
        
        self.defaultValueInstant = None
        """ Default value if no value exists.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.defaultValueInteger = None
        """ Default value if no value exists.
        Type `int`. """
        
        self.defaultValueMarkdown = None
        """ Default value if no value exists.
        Type `str`. """
        
        self.defaultValueOid = None
        """ Default value if no value exists.
        Type `str`. """
        
        self.defaultValuePositiveInt = None
        """ Default value if no value exists.
        Type `int`. """
        
        self.defaultValueString = None
        """ Default value if no value exists.
        Type `str`. """
        
        self.defaultValueTime = None
        """ Default value if no value exists.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.defaultValueUnsignedInt = None
        """ Default value if no value exists.
        Type `int`. """
        
        self.defaultValueUri = None
        """ Default value if no value exists.
        Type `str`. """
        
        self.defaultValueUrl = None
        """ Default value if no value exists.
        Type `str`. """
        
        self.defaultValueUuid = None
        """ Default value if no value exists.
        Type `str`. """
        
        self.defaultValueAddress = None
        """ Default value if no value exists.
        Type `Address` (represented as `dict` in JSON). """
        
        self.defaultValueAge = None
        """ Default value if no value exists.
        Type `Age` (represented as `dict` in JSON). """
        
        self.defaultValueAnnotation = None
        """ Default value if no value exists.
        Type `Annotation` (represented as `dict` in JSON). """
        
        self.defaultValueAttachment = None
        """ Default value if no value exists.
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.defaultValueCodeableConcept = None
        """ Default value if no value exists.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.defaultValueCoding = None
        """ Default value if no value exists.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.defaultValueContactPoint = None
        """ Default value if no value exists.
        Type `ContactPoint` (represented as `dict` in JSON). """
        
        self.defaultValueCount = None
        """ Default value if no value exists.
        Type `Count` (represented as `dict` in JSON). """
        
        self.defaultValueDistance = None
        """ Default value if no value exists.
        Type `Distance` (represented as `dict` in JSON). """
        
        self.defaultValueDuration = None
        """ Default value if no value exists.
        Type `Duration` (represented as `dict` in JSON). """
        
        self.defaultValueHumanName = None
        """ Default value if no value exists.
        Type `HumanName` (represented as `dict` in JSON). """
        
        self.defaultValueIdentifier = None
        """ Default value if no value exists.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.defaultValueMoney = None
        """ Default value if no value exists.
        Type `Money` (represented as `dict` in JSON). """
        
        self.defaultValuePeriod = None
        """ Default value if no value exists.
        Type `Period` (represented as `dict` in JSON). """
        
        self.defaultValueQuantity = None
        """ Default value if no value exists.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.defaultValueRange = None
        """ Default value if no value exists.
        Type `Range` (represented as `dict` in JSON). """
        
        self.defaultValueRatio = None
        """ Default value if no value exists.
        Type `Ratio` (represented as `dict` in JSON). """
        
        self.defaultValueReference = None
        """ Default value if no value exists.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.defaultValueSampledData = None
        """ Default value if no value exists.
        Type `SampledData` (represented as `dict` in JSON). """
        
        self.defaultValueSignature = None
        """ Default value if no value exists.
        Type `Signature` (represented as `dict` in JSON). """
        
        self.defaultValueTiming = None
        """ Default value if no value exists.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.defaultValueContactDetail = None
        """ Default value if no value exists.
        Type `ContactDetail` (represented as `dict` in JSON). """
        
        self.defaultValueContributor = None
        """ Default value if no value exists.
        Type `Contributor` (represented as `dict` in JSON). """
        
        self.defaultValueDataRequirement = None
        """ Default value if no value exists.
        Type `DataRequirement` (represented as `dict` in JSON). """
        
        self.defaultValueExpression = None
        """ Default value if no value exists.
        Type `Expression` (represented as `dict` in JSON). """
        
        self.defaultValueParameterDefinition = None
        """ Default value if no value exists.
        Type `ParameterDefinition` (represented as `dict` in JSON). """
        
        self.defaultValueRelatedArtifact = None
        """ Default value if no value exists.
        Type `RelatedArtifact` (represented as `dict` in JSON). """
        
        self.defaultValueTriggerDefinition = None
        """ Default value if no value exists.
        Type `TriggerDefinition` (represented as `dict` in JSON). """
        
        self.defaultValueUsageContext = None
        """ Default value if no value exists.
        Type `UsageContext` (represented as `dict` in JSON). """
        
        self.defaultValueDosage = None
        """ Default value if no value exists.
        Type `Dosage` (represented as `dict` in JSON). """
        
        self.defaultValueMeta = None
        """ Default value if no value exists.
        Type `Meta` (represented as `dict` in JSON). """
        
        self.element = None
        """ Optional field for this source.
        Type `str`. """
        
        self.listMode = None
        """ How to handle the list mode for this element.
        Type `str`. """
        
        self.variable = None
        """ Named context for field, if a field is specified.
        Type `str`. """
        
        self.condition = None
        """ FHIRPath expression  - must be true or the rule does not apply.
        Type `str`. """
        
        self.check = None
        """ FHIRPath expression  - must be true or the mapping engine throws an
        error instead of completing.
        Type `str`. """
        
        self.logMessage = None
        """ Message to put in log if source exists (FHIRPath).
        Type `str`. """
        
        super(StructureMapGroupRuleSource, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(StructureMapGroupRuleSource, self).elementProperties()
        js.extend([
            ("context", "context", str, False, None, True),
            ("min", "min", int, False, None, False),
            ("max", "max", str, False, None, False),
            ("type", "type", str, False, None, False),
            ("defaultValueBase64Binary", "defaultValueBase64Binary", str, False, "defaultValue", False),
            ("defaultValueBoolean", "defaultValueBoolean", bool, False, "defaultValue", False),
            ("defaultValueCanonical", "defaultValueCanonical", str, False, "defaultValue", False),
            ("defaultValueCode", "defaultValueCode", str, False, "defaultValue", False),
            ("defaultValueDate", "defaultValueDate", fhirdate.FHIRDate, False, "defaultValue", False),
            ("defaultValueDateTime", "defaultValueDateTime", fhirdate.FHIRDate, False, "defaultValue", False),
            ("defaultValueDecimal", "defaultValueDecimal", float, False, "defaultValue", False),
            ("defaultValueId", "defaultValueId", str, False, "defaultValue", False),
            ("defaultValueInstant", "defaultValueInstant", fhirdate.FHIRDate, False, "defaultValue", False),
            ("defaultValueInteger", "defaultValueInteger", int, False, "defaultValue", False),
            ("defaultValueMarkdown", "defaultValueMarkdown", str, False, "defaultValue", False),
            ("defaultValueOid", "defaultValueOid", str, False, "defaultValue", False),
            ("defaultValuePositiveInt", "defaultValuePositiveInt", int, False, "defaultValue", False),
            ("defaultValueString", "defaultValueString", str, False, "defaultValue", False),
            ("defaultValueTime", "defaultValueTime", fhirdate.FHIRDate, False, "defaultValue", False),
            ("defaultValueUnsignedInt", "defaultValueUnsignedInt", int, False, "defaultValue", False),
            ("defaultValueUri", "defaultValueUri", str, False, "defaultValue", False),
            ("defaultValueUrl", "defaultValueUrl", str, False, "defaultValue", False),
            ("defaultValueUuid", "defaultValueUuid", str, False, "defaultValue", False),
            ("defaultValueAddress", "defaultValueAddress", address.Address, False, "defaultValue", False),
            ("defaultValueAge", "defaultValueAge", age.Age, False, "defaultValue", False),
            ("defaultValueAnnotation", "defaultValueAnnotation", annotation.Annotation, False, "defaultValue", False),
            ("defaultValueAttachment", "defaultValueAttachment", attachment.Attachment, False, "defaultValue", False),
            ("defaultValueCodeableConcept", "defaultValueCodeableConcept", codeableconcept.CodeableConcept, False, "defaultValue", False),
            ("defaultValueCoding", "defaultValueCoding", coding.Coding, False, "defaultValue", False),
            ("defaultValueContactPoint", "defaultValueContactPoint", contactpoint.ContactPoint, False, "defaultValue", False),
            ("defaultValueCount", "defaultValueCount", count.Count, False, "defaultValue", False),
            ("defaultValueDistance", "defaultValueDistance", distance.Distance, False, "defaultValue", False),
            ("defaultValueDuration", "defaultValueDuration", duration.Duration, False, "defaultValue", False),
            ("defaultValueHumanName", "defaultValueHumanName", humanname.HumanName, False, "defaultValue", False),
            ("defaultValueIdentifier", "defaultValueIdentifier", identifier.Identifier, False, "defaultValue", False),
            ("defaultValueMoney", "defaultValueMoney", money.Money, False, "defaultValue", False),
            ("defaultValuePeriod", "defaultValuePeriod", period.Period, False, "defaultValue", False),
            ("defaultValueQuantity", "defaultValueQuantity", quantity.Quantity, False, "defaultValue", False),
            ("defaultValueRange", "defaultValueRange", range.Range, False, "defaultValue", False),
            ("defaultValueRatio", "defaultValueRatio", ratio.Ratio, False, "defaultValue", False),
            ("defaultValueReference", "defaultValueReference", fhirreference.FHIRReference, False, "defaultValue", False),
            ("defaultValueSampledData", "defaultValueSampledData", sampleddata.SampledData, False, "defaultValue", False),
            ("defaultValueSignature", "defaultValueSignature", signature.Signature, False, "defaultValue", False),
            ("defaultValueTiming", "defaultValueTiming", timing.Timing, False, "defaultValue", False),
            ("defaultValueContactDetail", "defaultValueContactDetail", contactdetail.ContactDetail, False, "defaultValue", False),
            ("defaultValueContributor", "defaultValueContributor", contributor.Contributor, False, "defaultValue", False),
            ("defaultValueDataRequirement", "defaultValueDataRequirement", datarequirement.DataRequirement, False, "defaultValue", False),
            ("defaultValueExpression", "defaultValueExpression", expression.Expression, False, "defaultValue", False),
            ("defaultValueParameterDefinition", "defaultValueParameterDefinition", parameterdefinition.ParameterDefinition, False, "defaultValue", False),
            ("defaultValueRelatedArtifact", "defaultValueRelatedArtifact", relatedartifact.RelatedArtifact, False, "defaultValue", False),
            ("defaultValueTriggerDefinition", "defaultValueTriggerDefinition", triggerdefinition.TriggerDefinition, False, "defaultValue", False),
            ("defaultValueUsageContext", "defaultValueUsageContext", usagecontext.UsageContext, False, "defaultValue", False),
            ("defaultValueDosage", "defaultValueDosage", dosage.Dosage, False, "defaultValue", False),
            ("defaultValueMeta", "defaultValueMeta", meta.Meta, False, "defaultValue", False),
            ("element", "element", str, False, None, False),
            ("listMode", "listMode", str, False, None, False),
            ("variable", "variable", str, False, None, False),
            ("condition", "condition", str, False, None, False),
            ("check", "check", str, False, None, False),
            ("logMessage", "logMessage", str, False, None, False),
        ])
        return js


class StructureMapGroupRuleTarget(backboneelement.BackboneElement):
    """ Content to create because of this mapping rule.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['context'] = """Type or variable this rule applies to."""
    _attribute_docstrings['contextType'] = """How to interpret the context."""
    _attribute_docstrings['element'] = """Field to create in the context."""
    _attribute_docstrings['variable'] = """Named context for field, if desired, and a field is specified."""
    _attribute_docstrings['listMode'] = """If field is a list, how to manage the list."""
    _attribute_docstrings['listRuleId'] = """Internal rule reference for shared list items."""
    _attribute_docstrings['transform'] = """How the data is copied / created."""
    _attribute_docstrings['parameter'] = """Parameters to the transform."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['contextType'] = {
        'url': 'http://hl7.org/fhir/map-context-type',
        'restricted_to': ['type', 'variable'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['listMode'] = {
        'url': 'http://hl7.org/fhir/map-target-list-mode',
        'restricted_to': ['first', 'share', 'last', 'collate'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['transform'] = {
        'url': 'http://hl7.org/fhir/map-transform',
        'restricted_to': ['create', 'copy', 'truncate', 'escape', 'cast', 'append', 'translate', 'reference', 'dateOp', 'uuid', 'pointer', 'evaluate', 'cc', 'c', 'qty', 'id', 'cp'],
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
        
        self.context = None
        """ Type or variable this rule applies to.
        Type `str`. """
        
        self.contextType = None
        """ How to interpret the context.
        Type `str`. """
        
        self.element = None
        """ Field to create in the context.
        Type `str`. """
        
        self.variable = None
        """ Named context for field, if desired, and a field is specified.
        Type `str`. """
        
        self.listMode = None
        """ If field is a list, how to manage the list.
        List of `str` items. """
        
        self.listRuleId = None
        """ Internal rule reference for shared list items.
        Type `str`. """
        
        self.transform = None
        """ How the data is copied / created.
        Type `str`. """
        
        self.parameter = None
        """ Parameters to the transform.
        List of `StructureMapGroupRuleTargetParameter` items (represented as `dict` in JSON). """
        
        super(StructureMapGroupRuleTarget, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(StructureMapGroupRuleTarget, self).elementProperties()
        js.extend([
            ("context", "context", str, False, None, False),
            ("contextType", "contextType", str, False, None, False),
            ("element", "element", str, False, None, False),
            ("variable", "variable", str, False, None, False),
            ("listMode", "listMode", str, True, None, False),
            ("listRuleId", "listRuleId", str, False, None, False),
            ("transform", "transform", str, False, None, False),
            ("parameter", "parameter", StructureMapGroupRuleTargetParameter, True, None, False),
        ])
        return js


class StructureMapGroupRuleTargetParameter(backboneelement.BackboneElement):
    """ Parameters to the transform.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['valueId'] = """Parameter value - variable or literal."""
    _attribute_docstrings['valueString'] = """Parameter value - variable or literal."""
    _attribute_docstrings['valueBoolean'] = """Parameter value - variable or literal."""
    _attribute_docstrings['valueInteger'] = """Parameter value - variable or literal."""
    _attribute_docstrings['valueDecimal'] = """Parameter value - variable or literal."""

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
        
        self.valueId = None
        """ Parameter value - variable or literal.
        Type `str`. """
        
        self.valueString = None
        """ Parameter value - variable or literal.
        Type `str`. """
        
        self.valueBoolean = None
        """ Parameter value - variable or literal.
        Type `bool`. """
        
        self.valueInteger = None
        """ Parameter value - variable or literal.
        Type `int`. """
        
        self.valueDecimal = None
        """ Parameter value - variable or literal.
        Type `float`. """
        
        super(StructureMapGroupRuleTargetParameter, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(StructureMapGroupRuleTargetParameter, self).elementProperties()
        js.extend([
            ("valueId", "valueId", str, False, "value", True),
            ("valueString", "valueString", str, False, "value", True),
            ("valueBoolean", "valueBoolean", bool, False, "value", True),
            ("valueInteger", "valueInteger", int, False, "value", True),
            ("valueDecimal", "valueDecimal", float, False, "value", True),
        ])
        return js


class StructureMapStructure(backboneelement.BackboneElement):
    """ Structure Definition used by this map.
    
    A structure definition used by this map. The structure definition may
    describe instances that are converted, or the instances that are produced.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['url'] = """Canonical reference to structure definition."""
    _attribute_docstrings['mode'] = """How the referenced structure is used in this mapping."""
    _attribute_docstrings['alias'] = """Name for type in this map."""
    _attribute_docstrings['documentation'] = """Documentation on use of structure."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['mode'] = {
        'url': 'http://hl7.org/fhir/map-model-mode',
        'restricted_to': ['source', 'queried', 'target', 'produced'],
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
        """ Canonical reference to structure definition.
        Type `str`. """
        
        self.mode = None
        """ How the referenced structure is used in this mapping.
        Type `str`. """
        
        self.alias = None
        """ Name for type in this map.
        Type `str`. """
        
        self.documentation = None
        """ Documentation on use of structure.
        Type `str`. """
        
        super(StructureMapStructure, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(StructureMapStructure, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, True),
            ("mode", "mode", str, False, None, True),
            ("alias", "alias", str, False, None, False),
            ("documentation", "documentation", str, False, None, False),
        ])
        return js


import sys
try:
    from . import address
except ImportError:
    address = sys.modules[__package__ + '.address']
try:
    from . import age
except ImportError:
    age = sys.modules[__package__ + '.age']
try:
    from . import annotation
except ImportError:
    annotation = sys.modules[__package__ + '.annotation']
try:
    from . import attachment
except ImportError:
    attachment = sys.modules[__package__ + '.attachment']
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
    from . import contactpoint
except ImportError:
    contactpoint = sys.modules[__package__ + '.contactpoint']
try:
    from . import contributor
except ImportError:
    contributor = sys.modules[__package__ + '.contributor']
try:
    from . import count
except ImportError:
    count = sys.modules[__package__ + '.count']
try:
    from . import datarequirement
except ImportError:
    datarequirement = sys.modules[__package__ + '.datarequirement']
try:
    from . import distance
except ImportError:
    distance = sys.modules[__package__ + '.distance']
try:
    from . import dosage
except ImportError:
    dosage = sys.modules[__package__ + '.dosage']
try:
    from . import duration
except ImportError:
    duration = sys.modules[__package__ + '.duration']
try:
    from . import expression
except ImportError:
    expression = sys.modules[__package__ + '.expression']
try:
    from . import fhirdate
except ImportError:
    fhirdate = sys.modules[__package__ + '.fhirdate']
try:
    from . import fhirreference
except ImportError:
    fhirreference = sys.modules[__package__ + '.fhirreference']
try:
    from . import humanname
except ImportError:
    humanname = sys.modules[__package__ + '.humanname']
try:
    from . import identifier
except ImportError:
    identifier = sys.modules[__package__ + '.identifier']
try:
    from . import meta
except ImportError:
    meta = sys.modules[__package__ + '.meta']
try:
    from . import money
except ImportError:
    money = sys.modules[__package__ + '.money']
try:
    from . import parameterdefinition
except ImportError:
    parameterdefinition = sys.modules[__package__ + '.parameterdefinition']
try:
    from . import period
except ImportError:
    period = sys.modules[__package__ + '.period']
try:
    from . import quantity
except ImportError:
    quantity = sys.modules[__package__ + '.quantity']
try:
    from . import range
except ImportError:
    range = sys.modules[__package__ + '.range']
try:
    from . import ratio
except ImportError:
    ratio = sys.modules[__package__ + '.ratio']
try:
    from . import relatedartifact
except ImportError:
    relatedartifact = sys.modules[__package__ + '.relatedartifact']
try:
    from . import sampleddata
except ImportError:
    sampleddata = sys.modules[__package__ + '.sampleddata']
try:
    from . import signature
except ImportError:
    signature = sys.modules[__package__ + '.signature']
try:
    from . import timing
except ImportError:
    timing = sys.modules[__package__ + '.timing']
try:
    from . import triggerdefinition
except ImportError:
    triggerdefinition = sys.modules[__package__ + '.triggerdefinition']
try:
    from . import usagecontext
except ImportError:
    usagecontext = sys.modules[__package__ + '.usagecontext']
