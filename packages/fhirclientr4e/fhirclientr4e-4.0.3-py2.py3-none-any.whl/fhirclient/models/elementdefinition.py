#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/ElementDefinition) on 2022-06-21.
#  2022, SMART Health IT.


from . import backboneelement

class ElementDefinition(backboneelement.BackboneElement):
    """ Definition of an element in a resource or extension.
    
    Captures constraints on each element within the resource, profile, or
    extension.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['path'] = """Path of the element in the hierarchy of elements."""
    _attribute_docstrings['representation'] = """Codes that define how this element is represented in instances, when the deviation varies from the normal case."""
    _attribute_docstrings['sliceName'] = """Name for this particular element (in a set of slices)."""
    _attribute_docstrings['sliceIsConstraining'] = """If this slice definition constrains an inherited slice definition (or not)."""
    _attribute_docstrings['label'] = """Name for element to display with or prompt for element."""
    _attribute_docstrings['code'] = """Corresponding codes in terminologies."""
    _attribute_docstrings['slicing'] = """This element is sliced - slices follow."""
    _attribute_docstrings['short'] = """Concise definition for space-constrained presentation."""
    _attribute_docstrings['definition'] = """Full formal definition as narrative text."""
    _attribute_docstrings['comment'] = """Comments about the use of this element."""
    _attribute_docstrings['requirements'] = """Why this resource has been created."""
    _attribute_docstrings['alias'] = """Other names."""
    _attribute_docstrings['min'] = """Minimum Cardinality."""
    _attribute_docstrings['max'] = """Maximum Cardinality (a number or *)."""
    _attribute_docstrings['base'] = """Base definition information for tools."""
    _attribute_docstrings['contentReference'] = """Reference to definition of content for the element."""
    _attribute_docstrings['type'] = """Data type and Profile for this element."""
    _attribute_docstrings['defaultValueBase64Binary'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueBoolean'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueCanonical'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueCode'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueDate'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueDateTime'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueDecimal'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueId'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueInstant'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueInteger'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueMarkdown'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueOid'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValuePositiveInt'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueString'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueTime'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueUnsignedInt'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueUri'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueUrl'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueUuid'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueAddress'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueAge'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueAnnotation'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueAttachment'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueCodeableConcept'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueCoding'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueContactPoint'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueCount'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueDistance'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueDuration'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueHumanName'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueIdentifier'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueMoney'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValuePeriod'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueQuantity'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueRange'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueRatio'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueReference'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueSampledData'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueSignature'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueTiming'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueContactDetail'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueContributor'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueDataRequirement'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueExpression'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueParameterDefinition'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueRelatedArtifact'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueTriggerDefinition'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueUsageContext'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueDosage'] = """Specified value if missing from instance."""
    _attribute_docstrings['defaultValueMeta'] = """Specified value if missing from instance."""
    _attribute_docstrings['meaningWhenMissing'] = """Implicit meaning when this element is missing."""
    _attribute_docstrings['orderMeaning'] = """What the order of the elements means."""
    _attribute_docstrings['fixedBase64Binary'] = """Value must be exactly this."""
    _attribute_docstrings['fixedBoolean'] = """Value must be exactly this."""
    _attribute_docstrings['fixedCanonical'] = """Value must be exactly this."""
    _attribute_docstrings['fixedCode'] = """Value must be exactly this."""
    _attribute_docstrings['fixedDate'] = """Value must be exactly this."""
    _attribute_docstrings['fixedDateTime'] = """Value must be exactly this."""
    _attribute_docstrings['fixedDecimal'] = """Value must be exactly this."""
    _attribute_docstrings['fixedId'] = """Value must be exactly this."""
    _attribute_docstrings['fixedInstant'] = """Value must be exactly this."""
    _attribute_docstrings['fixedInteger'] = """Value must be exactly this."""
    _attribute_docstrings['fixedMarkdown'] = """Value must be exactly this."""
    _attribute_docstrings['fixedOid'] = """Value must be exactly this."""
    _attribute_docstrings['fixedPositiveInt'] = """Value must be exactly this."""
    _attribute_docstrings['fixedString'] = """Value must be exactly this."""
    _attribute_docstrings['fixedTime'] = """Value must be exactly this."""
    _attribute_docstrings['fixedUnsignedInt'] = """Value must be exactly this."""
    _attribute_docstrings['fixedUri'] = """Value must be exactly this."""
    _attribute_docstrings['fixedUrl'] = """Value must be exactly this."""
    _attribute_docstrings['fixedUuid'] = """Value must be exactly this."""
    _attribute_docstrings['fixedAddress'] = """Value must be exactly this."""
    _attribute_docstrings['fixedAge'] = """Value must be exactly this."""
    _attribute_docstrings['fixedAnnotation'] = """Value must be exactly this."""
    _attribute_docstrings['fixedAttachment'] = """Value must be exactly this."""
    _attribute_docstrings['fixedCodeableConcept'] = """Value must be exactly this."""
    _attribute_docstrings['fixedCoding'] = """Value must be exactly this."""
    _attribute_docstrings['fixedContactPoint'] = """Value must be exactly this."""
    _attribute_docstrings['fixedCount'] = """Value must be exactly this."""
    _attribute_docstrings['fixedDistance'] = """Value must be exactly this."""
    _attribute_docstrings['fixedDuration'] = """Value must be exactly this."""
    _attribute_docstrings['fixedHumanName'] = """Value must be exactly this."""
    _attribute_docstrings['fixedIdentifier'] = """Value must be exactly this."""
    _attribute_docstrings['fixedMoney'] = """Value must be exactly this."""
    _attribute_docstrings['fixedPeriod'] = """Value must be exactly this."""
    _attribute_docstrings['fixedQuantity'] = """Value must be exactly this."""
    _attribute_docstrings['fixedRange'] = """Value must be exactly this."""
    _attribute_docstrings['fixedRatio'] = """Value must be exactly this."""
    _attribute_docstrings['fixedReference'] = """Value must be exactly this."""
    _attribute_docstrings['fixedSampledData'] = """Value must be exactly this."""
    _attribute_docstrings['fixedSignature'] = """Value must be exactly this."""
    _attribute_docstrings['fixedTiming'] = """Value must be exactly this."""
    _attribute_docstrings['fixedContactDetail'] = """Value must be exactly this."""
    _attribute_docstrings['fixedContributor'] = """Value must be exactly this."""
    _attribute_docstrings['fixedDataRequirement'] = """Value must be exactly this."""
    _attribute_docstrings['fixedExpression'] = """Value must be exactly this."""
    _attribute_docstrings['fixedParameterDefinition'] = """Value must be exactly this."""
    _attribute_docstrings['fixedRelatedArtifact'] = """Value must be exactly this."""
    _attribute_docstrings['fixedTriggerDefinition'] = """Value must be exactly this."""
    _attribute_docstrings['fixedUsageContext'] = """Value must be exactly this."""
    _attribute_docstrings['fixedDosage'] = """Value must be exactly this."""
    _attribute_docstrings['fixedMeta'] = """Value must be exactly this."""
    _attribute_docstrings['patternBase64Binary'] = """Value must have at least these property values."""
    _attribute_docstrings['patternBoolean'] = """Value must have at least these property values."""
    _attribute_docstrings['patternCanonical'] = """Value must have at least these property values."""
    _attribute_docstrings['patternCode'] = """Value must have at least these property values."""
    _attribute_docstrings['patternDate'] = """Value must have at least these property values."""
    _attribute_docstrings['patternDateTime'] = """Value must have at least these property values."""
    _attribute_docstrings['patternDecimal'] = """Value must have at least these property values."""
    _attribute_docstrings['patternId'] = """Value must have at least these property values."""
    _attribute_docstrings['patternInstant'] = """Value must have at least these property values."""
    _attribute_docstrings['patternInteger'] = """Value must have at least these property values."""
    _attribute_docstrings['patternMarkdown'] = """Value must have at least these property values."""
    _attribute_docstrings['patternOid'] = """Value must have at least these property values."""
    _attribute_docstrings['patternPositiveInt'] = """Value must have at least these property values."""
    _attribute_docstrings['patternString'] = """Value must have at least these property values."""
    _attribute_docstrings['patternTime'] = """Value must have at least these property values."""
    _attribute_docstrings['patternUnsignedInt'] = """Value must have at least these property values."""
    _attribute_docstrings['patternUri'] = """Value must have at least these property values."""
    _attribute_docstrings['patternUrl'] = """Value must have at least these property values."""
    _attribute_docstrings['patternUuid'] = """Value must have at least these property values."""
    _attribute_docstrings['patternAddress'] = """Value must have at least these property values."""
    _attribute_docstrings['patternAge'] = """Value must have at least these property values."""
    _attribute_docstrings['patternAnnotation'] = """Value must have at least these property values."""
    _attribute_docstrings['patternAttachment'] = """Value must have at least these property values."""
    _attribute_docstrings['patternCodeableConcept'] = """Value must have at least these property values."""
    _attribute_docstrings['patternCoding'] = """Value must have at least these property values."""
    _attribute_docstrings['patternContactPoint'] = """Value must have at least these property values."""
    _attribute_docstrings['patternCount'] = """Value must have at least these property values."""
    _attribute_docstrings['patternDistance'] = """Value must have at least these property values."""
    _attribute_docstrings['patternDuration'] = """Value must have at least these property values."""
    _attribute_docstrings['patternHumanName'] = """Value must have at least these property values."""
    _attribute_docstrings['patternIdentifier'] = """Value must have at least these property values."""
    _attribute_docstrings['patternMoney'] = """Value must have at least these property values."""
    _attribute_docstrings['patternPeriod'] = """Value must have at least these property values."""
    _attribute_docstrings['patternQuantity'] = """Value must have at least these property values."""
    _attribute_docstrings['patternRange'] = """Value must have at least these property values."""
    _attribute_docstrings['patternRatio'] = """Value must have at least these property values."""
    _attribute_docstrings['patternReference'] = """Value must have at least these property values."""
    _attribute_docstrings['patternSampledData'] = """Value must have at least these property values."""
    _attribute_docstrings['patternSignature'] = """Value must have at least these property values."""
    _attribute_docstrings['patternTiming'] = """Value must have at least these property values."""
    _attribute_docstrings['patternContactDetail'] = """Value must have at least these property values."""
    _attribute_docstrings['patternContributor'] = """Value must have at least these property values."""
    _attribute_docstrings['patternDataRequirement'] = """Value must have at least these property values."""
    _attribute_docstrings['patternExpression'] = """Value must have at least these property values."""
    _attribute_docstrings['patternParameterDefinition'] = """Value must have at least these property values."""
    _attribute_docstrings['patternRelatedArtifact'] = """Value must have at least these property values."""
    _attribute_docstrings['patternTriggerDefinition'] = """Value must have at least these property values."""
    _attribute_docstrings['patternUsageContext'] = """Value must have at least these property values."""
    _attribute_docstrings['patternDosage'] = """Value must have at least these property values."""
    _attribute_docstrings['patternMeta'] = """Value must have at least these property values."""
    _attribute_docstrings['example'] = """Example value (as defined for type)."""
    _attribute_docstrings['minValueDate'] = """Minimum Allowed Value (for some types)."""
    _attribute_docstrings['minValueDateTime'] = """Minimum Allowed Value (for some types)."""
    _attribute_docstrings['minValueInstant'] = """Minimum Allowed Value (for some types)."""
    _attribute_docstrings['minValueTime'] = """Minimum Allowed Value (for some types)."""
    _attribute_docstrings['minValueDecimal'] = """Minimum Allowed Value (for some types)."""
    _attribute_docstrings['minValueInteger'] = """Minimum Allowed Value (for some types)."""
    _attribute_docstrings['minValuePositiveInt'] = """Minimum Allowed Value (for some types)."""
    _attribute_docstrings['minValueUnsignedInt'] = """Minimum Allowed Value (for some types)."""
    _attribute_docstrings['minValueQuantity'] = """Minimum Allowed Value (for some types)."""
    _attribute_docstrings['maxValueDate'] = """Maximum Allowed Value (for some types)."""
    _attribute_docstrings['maxValueDateTime'] = """Maximum Allowed Value (for some types)."""
    _attribute_docstrings['maxValueInstant'] = """Maximum Allowed Value (for some types)."""
    _attribute_docstrings['maxValueTime'] = """Maximum Allowed Value (for some types)."""
    _attribute_docstrings['maxValueDecimal'] = """Maximum Allowed Value (for some types)."""
    _attribute_docstrings['maxValueInteger'] = """Maximum Allowed Value (for some types)."""
    _attribute_docstrings['maxValuePositiveInt'] = """Maximum Allowed Value (for some types)."""
    _attribute_docstrings['maxValueUnsignedInt'] = """Maximum Allowed Value (for some types)."""
    _attribute_docstrings['maxValueQuantity'] = """Maximum Allowed Value (for some types)."""
    _attribute_docstrings['maxLength'] = """Max length for strings."""
    _attribute_docstrings['condition'] = """Reference to invariant about presence."""
    _attribute_docstrings['constraint'] = """Condition that must evaluate to true."""
    _attribute_docstrings['mustSupport'] = """If the element must be supported."""
    _attribute_docstrings['isModifier'] = """If this modifies the meaning of other elements."""
    _attribute_docstrings['isModifierReason'] = """Reason that this element is marked as a modifier."""
    _attribute_docstrings['isSummary'] = """Include when _summary = true?."""
    _attribute_docstrings['binding'] = """ValueSet details if this is coded."""
    _attribute_docstrings['mapping'] = """Map element to another set of definitions."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['representation'] = {
        'url': 'http://hl7.org/fhir/property-representation',
        'restricted_to': ['xmlAttr', 'xmlText', 'typeAttr', 'cdaText', 'xhtml'],
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
        
        self.path = None
        """ Path of the element in the hierarchy of elements.
        Type `str`. """
        
        self.representation = None
        """ Codes that define how this element is represented in instances,
        when the deviation varies from the normal case.
        List of `str` items. """
        
        self.sliceName = None
        """ Name for this particular element (in a set of slices).
        Type `str`. """
        
        self.sliceIsConstraining = None
        """ If this slice definition constrains an inherited slice definition
        (or not).
        Type `bool`. """
        
        self.label = None
        """ Name for element to display with or prompt for element.
        Type `str`. """
        
        self.code = None
        """ Corresponding codes in terminologies.
        List of `Coding` items (represented as `dict` in JSON). """
        
        self.slicing = None
        """ This element is sliced - slices follow.
        Type `ElementDefinitionSlicing` (represented as `dict` in JSON). """
        
        self.short = None
        """ Concise definition for space-constrained presentation.
        Type `str`. """
        
        self.definition = None
        """ Full formal definition as narrative text.
        Type `str`. """
        
        self.comment = None
        """ Comments about the use of this element.
        Type `str`. """
        
        self.requirements = None
        """ Why this resource has been created.
        Type `str`. """
        
        self.alias = None
        """ Other names.
        List of `str` items. """
        
        self.min = None
        """ Minimum Cardinality.
        Type `int`. """
        
        self.max = None
        """ Maximum Cardinality (a number or *).
        Type `str`. """
        
        self.base = None
        """ Base definition information for tools.
        Type `ElementDefinitionBase` (represented as `dict` in JSON). """
        
        self.contentReference = None
        """ Reference to definition of content for the element.
        Type `str`. """
        
        self.type = None
        """ Data type and Profile for this element.
        List of `ElementDefinitionType` items (represented as `dict` in JSON). """
        
        self.defaultValueBase64Binary = None
        """ Specified value if missing from instance.
        Type `str`. """
        
        self.defaultValueBoolean = None
        """ Specified value if missing from instance.
        Type `bool`. """
        
        self.defaultValueCanonical = None
        """ Specified value if missing from instance.
        Type `str`. """
        
        self.defaultValueCode = None
        """ Specified value if missing from instance.
        Type `str`. """
        
        self.defaultValueDate = None
        """ Specified value if missing from instance.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.defaultValueDateTime = None
        """ Specified value if missing from instance.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.defaultValueDecimal = None
        """ Specified value if missing from instance.
        Type `float`. """
        
        self.defaultValueId = None
        """ Specified value if missing from instance.
        Type `str`. """
        
        self.defaultValueInstant = None
        """ Specified value if missing from instance.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.defaultValueInteger = None
        """ Specified value if missing from instance.
        Type `int`. """
        
        self.defaultValueMarkdown = None
        """ Specified value if missing from instance.
        Type `str`. """
        
        self.defaultValueOid = None
        """ Specified value if missing from instance.
        Type `str`. """
        
        self.defaultValuePositiveInt = None
        """ Specified value if missing from instance.
        Type `int`. """
        
        self.defaultValueString = None
        """ Specified value if missing from instance.
        Type `str`. """
        
        self.defaultValueTime = None
        """ Specified value if missing from instance.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.defaultValueUnsignedInt = None
        """ Specified value if missing from instance.
        Type `int`. """
        
        self.defaultValueUri = None
        """ Specified value if missing from instance.
        Type `str`. """
        
        self.defaultValueUrl = None
        """ Specified value if missing from instance.
        Type `str`. """
        
        self.defaultValueUuid = None
        """ Specified value if missing from instance.
        Type `str`. """
        
        self.defaultValueAddress = None
        """ Specified value if missing from instance.
        Type `Address` (represented as `dict` in JSON). """
        
        self.defaultValueAge = None
        """ Specified value if missing from instance.
        Type `Age` (represented as `dict` in JSON). """
        
        self.defaultValueAnnotation = None
        """ Specified value if missing from instance.
        Type `Annotation` (represented as `dict` in JSON). """
        
        self.defaultValueAttachment = None
        """ Specified value if missing from instance.
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.defaultValueCodeableConcept = None
        """ Specified value if missing from instance.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.defaultValueCoding = None
        """ Specified value if missing from instance.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.defaultValueContactPoint = None
        """ Specified value if missing from instance.
        Type `ContactPoint` (represented as `dict` in JSON). """
        
        self.defaultValueCount = None
        """ Specified value if missing from instance.
        Type `Count` (represented as `dict` in JSON). """
        
        self.defaultValueDistance = None
        """ Specified value if missing from instance.
        Type `Distance` (represented as `dict` in JSON). """
        
        self.defaultValueDuration = None
        """ Specified value if missing from instance.
        Type `Duration` (represented as `dict` in JSON). """
        
        self.defaultValueHumanName = None
        """ Specified value if missing from instance.
        Type `HumanName` (represented as `dict` in JSON). """
        
        self.defaultValueIdentifier = None
        """ Specified value if missing from instance.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.defaultValueMoney = None
        """ Specified value if missing from instance.
        Type `Money` (represented as `dict` in JSON). """
        
        self.defaultValuePeriod = None
        """ Specified value if missing from instance.
        Type `Period` (represented as `dict` in JSON). """
        
        self.defaultValueQuantity = None
        """ Specified value if missing from instance.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.defaultValueRange = None
        """ Specified value if missing from instance.
        Type `Range` (represented as `dict` in JSON). """
        
        self.defaultValueRatio = None
        """ Specified value if missing from instance.
        Type `Ratio` (represented as `dict` in JSON). """
        
        self.defaultValueReference = None
        """ Specified value if missing from instance.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.defaultValueSampledData = None
        """ Specified value if missing from instance.
        Type `SampledData` (represented as `dict` in JSON). """
        
        self.defaultValueSignature = None
        """ Specified value if missing from instance.
        Type `Signature` (represented as `dict` in JSON). """
        
        self.defaultValueTiming = None
        """ Specified value if missing from instance.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.defaultValueContactDetail = None
        """ Specified value if missing from instance.
        Type `ContactDetail` (represented as `dict` in JSON). """
        
        self.defaultValueContributor = None
        """ Specified value if missing from instance.
        Type `Contributor` (represented as `dict` in JSON). """
        
        self.defaultValueDataRequirement = None
        """ Specified value if missing from instance.
        Type `DataRequirement` (represented as `dict` in JSON). """
        
        self.defaultValueExpression = None
        """ Specified value if missing from instance.
        Type `Expression` (represented as `dict` in JSON). """
        
        self.defaultValueParameterDefinition = None
        """ Specified value if missing from instance.
        Type `ParameterDefinition` (represented as `dict` in JSON). """
        
        self.defaultValueRelatedArtifact = None
        """ Specified value if missing from instance.
        Type `RelatedArtifact` (represented as `dict` in JSON). """
        
        self.defaultValueTriggerDefinition = None
        """ Specified value if missing from instance.
        Type `TriggerDefinition` (represented as `dict` in JSON). """
        
        self.defaultValueUsageContext = None
        """ Specified value if missing from instance.
        Type `UsageContext` (represented as `dict` in JSON). """
        
        self.defaultValueDosage = None
        """ Specified value if missing from instance.
        Type `Dosage` (represented as `dict` in JSON). """
        
        self.defaultValueMeta = None
        """ Specified value if missing from instance.
        Type `Meta` (represented as `dict` in JSON). """
        
        self.meaningWhenMissing = None
        """ Implicit meaning when this element is missing.
        Type `str`. """
        
        self.orderMeaning = None
        """ What the order of the elements means.
        Type `str`. """
        
        self.fixedBase64Binary = None
        """ Value must be exactly this.
        Type `str`. """
        
        self.fixedBoolean = None
        """ Value must be exactly this.
        Type `bool`. """
        
        self.fixedCanonical = None
        """ Value must be exactly this.
        Type `str`. """
        
        self.fixedCode = None
        """ Value must be exactly this.
        Type `str`. """
        
        self.fixedDate = None
        """ Value must be exactly this.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.fixedDateTime = None
        """ Value must be exactly this.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.fixedDecimal = None
        """ Value must be exactly this.
        Type `float`. """
        
        self.fixedId = None
        """ Value must be exactly this.
        Type `str`. """
        
        self.fixedInstant = None
        """ Value must be exactly this.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.fixedInteger = None
        """ Value must be exactly this.
        Type `int`. """
        
        self.fixedMarkdown = None
        """ Value must be exactly this.
        Type `str`. """
        
        self.fixedOid = None
        """ Value must be exactly this.
        Type `str`. """
        
        self.fixedPositiveInt = None
        """ Value must be exactly this.
        Type `int`. """
        
        self.fixedString = None
        """ Value must be exactly this.
        Type `str`. """
        
        self.fixedTime = None
        """ Value must be exactly this.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.fixedUnsignedInt = None
        """ Value must be exactly this.
        Type `int`. """
        
        self.fixedUri = None
        """ Value must be exactly this.
        Type `str`. """
        
        self.fixedUrl = None
        """ Value must be exactly this.
        Type `str`. """
        
        self.fixedUuid = None
        """ Value must be exactly this.
        Type `str`. """
        
        self.fixedAddress = None
        """ Value must be exactly this.
        Type `Address` (represented as `dict` in JSON). """
        
        self.fixedAge = None
        """ Value must be exactly this.
        Type `Age` (represented as `dict` in JSON). """
        
        self.fixedAnnotation = None
        """ Value must be exactly this.
        Type `Annotation` (represented as `dict` in JSON). """
        
        self.fixedAttachment = None
        """ Value must be exactly this.
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.fixedCodeableConcept = None
        """ Value must be exactly this.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.fixedCoding = None
        """ Value must be exactly this.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.fixedContactPoint = None
        """ Value must be exactly this.
        Type `ContactPoint` (represented as `dict` in JSON). """
        
        self.fixedCount = None
        """ Value must be exactly this.
        Type `Count` (represented as `dict` in JSON). """
        
        self.fixedDistance = None
        """ Value must be exactly this.
        Type `Distance` (represented as `dict` in JSON). """
        
        self.fixedDuration = None
        """ Value must be exactly this.
        Type `Duration` (represented as `dict` in JSON). """
        
        self.fixedHumanName = None
        """ Value must be exactly this.
        Type `HumanName` (represented as `dict` in JSON). """
        
        self.fixedIdentifier = None
        """ Value must be exactly this.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.fixedMoney = None
        """ Value must be exactly this.
        Type `Money` (represented as `dict` in JSON). """
        
        self.fixedPeriod = None
        """ Value must be exactly this.
        Type `Period` (represented as `dict` in JSON). """
        
        self.fixedQuantity = None
        """ Value must be exactly this.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.fixedRange = None
        """ Value must be exactly this.
        Type `Range` (represented as `dict` in JSON). """
        
        self.fixedRatio = None
        """ Value must be exactly this.
        Type `Ratio` (represented as `dict` in JSON). """
        
        self.fixedReference = None
        """ Value must be exactly this.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.fixedSampledData = None
        """ Value must be exactly this.
        Type `SampledData` (represented as `dict` in JSON). """
        
        self.fixedSignature = None
        """ Value must be exactly this.
        Type `Signature` (represented as `dict` in JSON). """
        
        self.fixedTiming = None
        """ Value must be exactly this.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.fixedContactDetail = None
        """ Value must be exactly this.
        Type `ContactDetail` (represented as `dict` in JSON). """
        
        self.fixedContributor = None
        """ Value must be exactly this.
        Type `Contributor` (represented as `dict` in JSON). """
        
        self.fixedDataRequirement = None
        """ Value must be exactly this.
        Type `DataRequirement` (represented as `dict` in JSON). """
        
        self.fixedExpression = None
        """ Value must be exactly this.
        Type `Expression` (represented as `dict` in JSON). """
        
        self.fixedParameterDefinition = None
        """ Value must be exactly this.
        Type `ParameterDefinition` (represented as `dict` in JSON). """
        
        self.fixedRelatedArtifact = None
        """ Value must be exactly this.
        Type `RelatedArtifact` (represented as `dict` in JSON). """
        
        self.fixedTriggerDefinition = None
        """ Value must be exactly this.
        Type `TriggerDefinition` (represented as `dict` in JSON). """
        
        self.fixedUsageContext = None
        """ Value must be exactly this.
        Type `UsageContext` (represented as `dict` in JSON). """
        
        self.fixedDosage = None
        """ Value must be exactly this.
        Type `Dosage` (represented as `dict` in JSON). """
        
        self.fixedMeta = None
        """ Value must be exactly this.
        Type `Meta` (represented as `dict` in JSON). """
        
        self.patternBase64Binary = None
        """ Value must have at least these property values.
        Type `str`. """
        
        self.patternBoolean = None
        """ Value must have at least these property values.
        Type `bool`. """
        
        self.patternCanonical = None
        """ Value must have at least these property values.
        Type `str`. """
        
        self.patternCode = None
        """ Value must have at least these property values.
        Type `str`. """
        
        self.patternDate = None
        """ Value must have at least these property values.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.patternDateTime = None
        """ Value must have at least these property values.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.patternDecimal = None
        """ Value must have at least these property values.
        Type `float`. """
        
        self.patternId = None
        """ Value must have at least these property values.
        Type `str`. """
        
        self.patternInstant = None
        """ Value must have at least these property values.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.patternInteger = None
        """ Value must have at least these property values.
        Type `int`. """
        
        self.patternMarkdown = None
        """ Value must have at least these property values.
        Type `str`. """
        
        self.patternOid = None
        """ Value must have at least these property values.
        Type `str`. """
        
        self.patternPositiveInt = None
        """ Value must have at least these property values.
        Type `int`. """
        
        self.patternString = None
        """ Value must have at least these property values.
        Type `str`. """
        
        self.patternTime = None
        """ Value must have at least these property values.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.patternUnsignedInt = None
        """ Value must have at least these property values.
        Type `int`. """
        
        self.patternUri = None
        """ Value must have at least these property values.
        Type `str`. """
        
        self.patternUrl = None
        """ Value must have at least these property values.
        Type `str`. """
        
        self.patternUuid = None
        """ Value must have at least these property values.
        Type `str`. """
        
        self.patternAddress = None
        """ Value must have at least these property values.
        Type `Address` (represented as `dict` in JSON). """
        
        self.patternAge = None
        """ Value must have at least these property values.
        Type `Age` (represented as `dict` in JSON). """
        
        self.patternAnnotation = None
        """ Value must have at least these property values.
        Type `Annotation` (represented as `dict` in JSON). """
        
        self.patternAttachment = None
        """ Value must have at least these property values.
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.patternCodeableConcept = None
        """ Value must have at least these property values.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.patternCoding = None
        """ Value must have at least these property values.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.patternContactPoint = None
        """ Value must have at least these property values.
        Type `ContactPoint` (represented as `dict` in JSON). """
        
        self.patternCount = None
        """ Value must have at least these property values.
        Type `Count` (represented as `dict` in JSON). """
        
        self.patternDistance = None
        """ Value must have at least these property values.
        Type `Distance` (represented as `dict` in JSON). """
        
        self.patternDuration = None
        """ Value must have at least these property values.
        Type `Duration` (represented as `dict` in JSON). """
        
        self.patternHumanName = None
        """ Value must have at least these property values.
        Type `HumanName` (represented as `dict` in JSON). """
        
        self.patternIdentifier = None
        """ Value must have at least these property values.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.patternMoney = None
        """ Value must have at least these property values.
        Type `Money` (represented as `dict` in JSON). """
        
        self.patternPeriod = None
        """ Value must have at least these property values.
        Type `Period` (represented as `dict` in JSON). """
        
        self.patternQuantity = None
        """ Value must have at least these property values.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.patternRange = None
        """ Value must have at least these property values.
        Type `Range` (represented as `dict` in JSON). """
        
        self.patternRatio = None
        """ Value must have at least these property values.
        Type `Ratio` (represented as `dict` in JSON). """
        
        self.patternReference = None
        """ Value must have at least these property values.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.patternSampledData = None
        """ Value must have at least these property values.
        Type `SampledData` (represented as `dict` in JSON). """
        
        self.patternSignature = None
        """ Value must have at least these property values.
        Type `Signature` (represented as `dict` in JSON). """
        
        self.patternTiming = None
        """ Value must have at least these property values.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.patternContactDetail = None
        """ Value must have at least these property values.
        Type `ContactDetail` (represented as `dict` in JSON). """
        
        self.patternContributor = None
        """ Value must have at least these property values.
        Type `Contributor` (represented as `dict` in JSON). """
        
        self.patternDataRequirement = None
        """ Value must have at least these property values.
        Type `DataRequirement` (represented as `dict` in JSON). """
        
        self.patternExpression = None
        """ Value must have at least these property values.
        Type `Expression` (represented as `dict` in JSON). """
        
        self.patternParameterDefinition = None
        """ Value must have at least these property values.
        Type `ParameterDefinition` (represented as `dict` in JSON). """
        
        self.patternRelatedArtifact = None
        """ Value must have at least these property values.
        Type `RelatedArtifact` (represented as `dict` in JSON). """
        
        self.patternTriggerDefinition = None
        """ Value must have at least these property values.
        Type `TriggerDefinition` (represented as `dict` in JSON). """
        
        self.patternUsageContext = None
        """ Value must have at least these property values.
        Type `UsageContext` (represented as `dict` in JSON). """
        
        self.patternDosage = None
        """ Value must have at least these property values.
        Type `Dosage` (represented as `dict` in JSON). """
        
        self.patternMeta = None
        """ Value must have at least these property values.
        Type `Meta` (represented as `dict` in JSON). """
        
        self.example = None
        """ Example value (as defined for type).
        List of `ElementDefinitionExample` items (represented as `dict` in JSON). """
        
        self.minValueDate = None
        """ Minimum Allowed Value (for some types).
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.minValueDateTime = None
        """ Minimum Allowed Value (for some types).
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.minValueInstant = None
        """ Minimum Allowed Value (for some types).
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.minValueTime = None
        """ Minimum Allowed Value (for some types).
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.minValueDecimal = None
        """ Minimum Allowed Value (for some types).
        Type `float`. """
        
        self.minValueInteger = None
        """ Minimum Allowed Value (for some types).
        Type `int`. """
        
        self.minValuePositiveInt = None
        """ Minimum Allowed Value (for some types).
        Type `int`. """
        
        self.minValueUnsignedInt = None
        """ Minimum Allowed Value (for some types).
        Type `int`. """
        
        self.minValueQuantity = None
        """ Minimum Allowed Value (for some types).
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.maxValueDate = None
        """ Maximum Allowed Value (for some types).
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.maxValueDateTime = None
        """ Maximum Allowed Value (for some types).
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.maxValueInstant = None
        """ Maximum Allowed Value (for some types).
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.maxValueTime = None
        """ Maximum Allowed Value (for some types).
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.maxValueDecimal = None
        """ Maximum Allowed Value (for some types).
        Type `float`. """
        
        self.maxValueInteger = None
        """ Maximum Allowed Value (for some types).
        Type `int`. """
        
        self.maxValuePositiveInt = None
        """ Maximum Allowed Value (for some types).
        Type `int`. """
        
        self.maxValueUnsignedInt = None
        """ Maximum Allowed Value (for some types).
        Type `int`. """
        
        self.maxValueQuantity = None
        """ Maximum Allowed Value (for some types).
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.maxLength = None
        """ Max length for strings.
        Type `int`. """
        
        self.condition = None
        """ Reference to invariant about presence.
        List of `str` items. """
        
        self.constraint = None
        """ Condition that must evaluate to true.
        List of `ElementDefinitionConstraint` items (represented as `dict` in JSON). """
        
        self.mustSupport = None
        """ If the element must be supported.
        Type `bool`. """
        
        self.isModifier = None
        """ If this modifies the meaning of other elements.
        Type `bool`. """
        
        self.isModifierReason = None
        """ Reason that this element is marked as a modifier.
        Type `str`. """
        
        self.isSummary = None
        """ Include when _summary = true?.
        Type `bool`. """
        
        self.binding = None
        """ ValueSet details if this is coded.
        Type `ElementDefinitionBinding` (represented as `dict` in JSON). """
        
        self.mapping = None
        """ Map element to another set of definitions.
        List of `ElementDefinitionMapping` items (represented as `dict` in JSON). """
        
        super(ElementDefinition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ElementDefinition, self).elementProperties()
        js.extend([
            ("path", "path", str, False, None, True),
            ("representation", "representation", str, True, None, False),
            ("sliceName", "sliceName", str, False, None, False),
            ("sliceIsConstraining", "sliceIsConstraining", bool, False, None, False),
            ("label", "label", str, False, None, False),
            ("code", "code", coding.Coding, True, None, False),
            ("slicing", "slicing", ElementDefinitionSlicing, False, None, False),
            ("short", "short", str, False, None, False),
            ("definition", "definition", str, False, None, False),
            ("comment", "comment", str, False, None, False),
            ("requirements", "requirements", str, False, None, False),
            ("alias", "alias", str, True, None, False),
            ("min", "min", int, False, None, False),
            ("max", "max", str, False, None, False),
            ("base", "base", ElementDefinitionBase, False, None, False),
            ("contentReference", "contentReference", str, False, None, False),
            ("type", "type", ElementDefinitionType, True, None, False),
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
            ("meaningWhenMissing", "meaningWhenMissing", str, False, None, False),
            ("orderMeaning", "orderMeaning", str, False, None, False),
            ("fixedBase64Binary", "fixedBase64Binary", str, False, "fixed", False),
            ("fixedBoolean", "fixedBoolean", bool, False, "fixed", False),
            ("fixedCanonical", "fixedCanonical", str, False, "fixed", False),
            ("fixedCode", "fixedCode", str, False, "fixed", False),
            ("fixedDate", "fixedDate", fhirdate.FHIRDate, False, "fixed", False),
            ("fixedDateTime", "fixedDateTime", fhirdate.FHIRDate, False, "fixed", False),
            ("fixedDecimal", "fixedDecimal", float, False, "fixed", False),
            ("fixedId", "fixedId", str, False, "fixed", False),
            ("fixedInstant", "fixedInstant", fhirdate.FHIRDate, False, "fixed", False),
            ("fixedInteger", "fixedInteger", int, False, "fixed", False),
            ("fixedMarkdown", "fixedMarkdown", str, False, "fixed", False),
            ("fixedOid", "fixedOid", str, False, "fixed", False),
            ("fixedPositiveInt", "fixedPositiveInt", int, False, "fixed", False),
            ("fixedString", "fixedString", str, False, "fixed", False),
            ("fixedTime", "fixedTime", fhirdate.FHIRDate, False, "fixed", False),
            ("fixedUnsignedInt", "fixedUnsignedInt", int, False, "fixed", False),
            ("fixedUri", "fixedUri", str, False, "fixed", False),
            ("fixedUrl", "fixedUrl", str, False, "fixed", False),
            ("fixedUuid", "fixedUuid", str, False, "fixed", False),
            ("fixedAddress", "fixedAddress", address.Address, False, "fixed", False),
            ("fixedAge", "fixedAge", age.Age, False, "fixed", False),
            ("fixedAnnotation", "fixedAnnotation", annotation.Annotation, False, "fixed", False),
            ("fixedAttachment", "fixedAttachment", attachment.Attachment, False, "fixed", False),
            ("fixedCodeableConcept", "fixedCodeableConcept", codeableconcept.CodeableConcept, False, "fixed", False),
            ("fixedCoding", "fixedCoding", coding.Coding, False, "fixed", False),
            ("fixedContactPoint", "fixedContactPoint", contactpoint.ContactPoint, False, "fixed", False),
            ("fixedCount", "fixedCount", count.Count, False, "fixed", False),
            ("fixedDistance", "fixedDistance", distance.Distance, False, "fixed", False),
            ("fixedDuration", "fixedDuration", duration.Duration, False, "fixed", False),
            ("fixedHumanName", "fixedHumanName", humanname.HumanName, False, "fixed", False),
            ("fixedIdentifier", "fixedIdentifier", identifier.Identifier, False, "fixed", False),
            ("fixedMoney", "fixedMoney", money.Money, False, "fixed", False),
            ("fixedPeriod", "fixedPeriod", period.Period, False, "fixed", False),
            ("fixedQuantity", "fixedQuantity", quantity.Quantity, False, "fixed", False),
            ("fixedRange", "fixedRange", range.Range, False, "fixed", False),
            ("fixedRatio", "fixedRatio", ratio.Ratio, False, "fixed", False),
            ("fixedReference", "fixedReference", fhirreference.FHIRReference, False, "fixed", False),
            ("fixedSampledData", "fixedSampledData", sampleddata.SampledData, False, "fixed", False),
            ("fixedSignature", "fixedSignature", signature.Signature, False, "fixed", False),
            ("fixedTiming", "fixedTiming", timing.Timing, False, "fixed", False),
            ("fixedContactDetail", "fixedContactDetail", contactdetail.ContactDetail, False, "fixed", False),
            ("fixedContributor", "fixedContributor", contributor.Contributor, False, "fixed", False),
            ("fixedDataRequirement", "fixedDataRequirement", datarequirement.DataRequirement, False, "fixed", False),
            ("fixedExpression", "fixedExpression", expression.Expression, False, "fixed", False),
            ("fixedParameterDefinition", "fixedParameterDefinition", parameterdefinition.ParameterDefinition, False, "fixed", False),
            ("fixedRelatedArtifact", "fixedRelatedArtifact", relatedartifact.RelatedArtifact, False, "fixed", False),
            ("fixedTriggerDefinition", "fixedTriggerDefinition", triggerdefinition.TriggerDefinition, False, "fixed", False),
            ("fixedUsageContext", "fixedUsageContext", usagecontext.UsageContext, False, "fixed", False),
            ("fixedDosage", "fixedDosage", dosage.Dosage, False, "fixed", False),
            ("fixedMeta", "fixedMeta", meta.Meta, False, "fixed", False),
            ("patternBase64Binary", "patternBase64Binary", str, False, "pattern", False),
            ("patternBoolean", "patternBoolean", bool, False, "pattern", False),
            ("patternCanonical", "patternCanonical", str, False, "pattern", False),
            ("patternCode", "patternCode", str, False, "pattern", False),
            ("patternDate", "patternDate", fhirdate.FHIRDate, False, "pattern", False),
            ("patternDateTime", "patternDateTime", fhirdate.FHIRDate, False, "pattern", False),
            ("patternDecimal", "patternDecimal", float, False, "pattern", False),
            ("patternId", "patternId", str, False, "pattern", False),
            ("patternInstant", "patternInstant", fhirdate.FHIRDate, False, "pattern", False),
            ("patternInteger", "patternInteger", int, False, "pattern", False),
            ("patternMarkdown", "patternMarkdown", str, False, "pattern", False),
            ("patternOid", "patternOid", str, False, "pattern", False),
            ("patternPositiveInt", "patternPositiveInt", int, False, "pattern", False),
            ("patternString", "patternString", str, False, "pattern", False),
            ("patternTime", "patternTime", fhirdate.FHIRDate, False, "pattern", False),
            ("patternUnsignedInt", "patternUnsignedInt", int, False, "pattern", False),
            ("patternUri", "patternUri", str, False, "pattern", False),
            ("patternUrl", "patternUrl", str, False, "pattern", False),
            ("patternUuid", "patternUuid", str, False, "pattern", False),
            ("patternAddress", "patternAddress", address.Address, False, "pattern", False),
            ("patternAge", "patternAge", age.Age, False, "pattern", False),
            ("patternAnnotation", "patternAnnotation", annotation.Annotation, False, "pattern", False),
            ("patternAttachment", "patternAttachment", attachment.Attachment, False, "pattern", False),
            ("patternCodeableConcept", "patternCodeableConcept", codeableconcept.CodeableConcept, False, "pattern", False),
            ("patternCoding", "patternCoding", coding.Coding, False, "pattern", False),
            ("patternContactPoint", "patternContactPoint", contactpoint.ContactPoint, False, "pattern", False),
            ("patternCount", "patternCount", count.Count, False, "pattern", False),
            ("patternDistance", "patternDistance", distance.Distance, False, "pattern", False),
            ("patternDuration", "patternDuration", duration.Duration, False, "pattern", False),
            ("patternHumanName", "patternHumanName", humanname.HumanName, False, "pattern", False),
            ("patternIdentifier", "patternIdentifier", identifier.Identifier, False, "pattern", False),
            ("patternMoney", "patternMoney", money.Money, False, "pattern", False),
            ("patternPeriod", "patternPeriod", period.Period, False, "pattern", False),
            ("patternQuantity", "patternQuantity", quantity.Quantity, False, "pattern", False),
            ("patternRange", "patternRange", range.Range, False, "pattern", False),
            ("patternRatio", "patternRatio", ratio.Ratio, False, "pattern", False),
            ("patternReference", "patternReference", fhirreference.FHIRReference, False, "pattern", False),
            ("patternSampledData", "patternSampledData", sampleddata.SampledData, False, "pattern", False),
            ("patternSignature", "patternSignature", signature.Signature, False, "pattern", False),
            ("patternTiming", "patternTiming", timing.Timing, False, "pattern", False),
            ("patternContactDetail", "patternContactDetail", contactdetail.ContactDetail, False, "pattern", False),
            ("patternContributor", "patternContributor", contributor.Contributor, False, "pattern", False),
            ("patternDataRequirement", "patternDataRequirement", datarequirement.DataRequirement, False, "pattern", False),
            ("patternExpression", "patternExpression", expression.Expression, False, "pattern", False),
            ("patternParameterDefinition", "patternParameterDefinition", parameterdefinition.ParameterDefinition, False, "pattern", False),
            ("patternRelatedArtifact", "patternRelatedArtifact", relatedartifact.RelatedArtifact, False, "pattern", False),
            ("patternTriggerDefinition", "patternTriggerDefinition", triggerdefinition.TriggerDefinition, False, "pattern", False),
            ("patternUsageContext", "patternUsageContext", usagecontext.UsageContext, False, "pattern", False),
            ("patternDosage", "patternDosage", dosage.Dosage, False, "pattern", False),
            ("patternMeta", "patternMeta", meta.Meta, False, "pattern", False),
            ("example", "example", ElementDefinitionExample, True, None, False),
            ("minValueDate", "minValueDate", fhirdate.FHIRDate, False, "minValue", False),
            ("minValueDateTime", "minValueDateTime", fhirdate.FHIRDate, False, "minValue", False),
            ("minValueInstant", "minValueInstant", fhirdate.FHIRDate, False, "minValue", False),
            ("minValueTime", "minValueTime", fhirdate.FHIRDate, False, "minValue", False),
            ("minValueDecimal", "minValueDecimal", float, False, "minValue", False),
            ("minValueInteger", "minValueInteger", int, False, "minValue", False),
            ("minValuePositiveInt", "minValuePositiveInt", int, False, "minValue", False),
            ("minValueUnsignedInt", "minValueUnsignedInt", int, False, "minValue", False),
            ("minValueQuantity", "minValueQuantity", quantity.Quantity, False, "minValue", False),
            ("maxValueDate", "maxValueDate", fhirdate.FHIRDate, False, "maxValue", False),
            ("maxValueDateTime", "maxValueDateTime", fhirdate.FHIRDate, False, "maxValue", False),
            ("maxValueInstant", "maxValueInstant", fhirdate.FHIRDate, False, "maxValue", False),
            ("maxValueTime", "maxValueTime", fhirdate.FHIRDate, False, "maxValue", False),
            ("maxValueDecimal", "maxValueDecimal", float, False, "maxValue", False),
            ("maxValueInteger", "maxValueInteger", int, False, "maxValue", False),
            ("maxValuePositiveInt", "maxValuePositiveInt", int, False, "maxValue", False),
            ("maxValueUnsignedInt", "maxValueUnsignedInt", int, False, "maxValue", False),
            ("maxValueQuantity", "maxValueQuantity", quantity.Quantity, False, "maxValue", False),
            ("maxLength", "maxLength", int, False, None, False),
            ("condition", "condition", str, True, None, False),
            ("constraint", "constraint", ElementDefinitionConstraint, True, None, False),
            ("mustSupport", "mustSupport", bool, False, None, False),
            ("isModifier", "isModifier", bool, False, None, False),
            ("isModifierReason", "isModifierReason", str, False, None, False),
            ("isSummary", "isSummary", bool, False, None, False),
            ("binding", "binding", ElementDefinitionBinding, False, None, False),
            ("mapping", "mapping", ElementDefinitionMapping, True, None, False),
        ])
        return js


from . import element

class ElementDefinitionBase(element.Element):
    """ Base definition information for tools.
    
    Information about the base definition of the element, provided to make it
    unnecessary for tools to trace the deviation of the element through the
    derived and related profiles. When the element definition is not the
    original definition of an element - i.g. either in a constraint on another
    type, or for elements from a super type in a snap shot - then the
    information in provided in the element definition may be different to the
    base definition. On the original definition of the element, it will be
    same.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['path'] = """Path that identifies the base element."""
    _attribute_docstrings['min'] = """Min cardinality of the base element."""
    _attribute_docstrings['max'] = """Max cardinality of the base element."""

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
        
        self.path = None
        """ Path that identifies the base element.
        Type `str`. """
        
        self.min = None
        """ Min cardinality of the base element.
        Type `int`. """
        
        self.max = None
        """ Max cardinality of the base element.
        Type `str`. """
        
        super(ElementDefinitionBase, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ElementDefinitionBase, self).elementProperties()
        js.extend([
            ("path", "path", str, False, None, True),
            ("min", "min", int, False, None, True),
            ("max", "max", str, False, None, True),
        ])
        return js


class ElementDefinitionBinding(element.Element):
    """ ValueSet details if this is coded.
    
    Binds to a value set if this element is coded (code, Coding,
    CodeableConcept, Quantity), or the data types (string, uri).
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['strength'] = """Indicates the degree of conformance expectations associated with this binding - that is, the degree to which the provided value set must be adhered to in the instances."""
    _attribute_docstrings['description'] = """Human explanation of the value set."""
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
        
        self.description = None
        """ Human explanation of the value set.
        Type `str`. """
        
        self.valueSet = None
        """ Source of value set.
        Type `str`. """
        
        super(ElementDefinitionBinding, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ElementDefinitionBinding, self).elementProperties()
        js.extend([
            ("strength", "strength", str, False, None, True),
            ("description", "description", str, False, None, False),
            ("valueSet", "valueSet", str, False, None, False),
        ])
        return js


class ElementDefinitionConstraint(element.Element):
    """ Condition that must evaluate to true.
    
    Formal constraints such as co-occurrence and other constraints that can be
    computationally evaluated within the context of the instance.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['key'] = """Target of 'condition' reference above."""
    _attribute_docstrings['requirements'] = """Why this constraint is necessary or appropriate."""
    _attribute_docstrings['severity'] = """Identifies the impact constraint violation has on the conformance of the instance."""
    _attribute_docstrings['human'] = """Human description of constraint."""
    _attribute_docstrings['expression'] = """FHIRPath expression of constraint."""
    _attribute_docstrings['xpath'] = """XPath expression of constraint."""
    _attribute_docstrings['source'] = """Reference to original source of constraint."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['severity'] = {
        'url': 'http://hl7.org/fhir/constraint-severity',
        'restricted_to': ['error', 'warning'],
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
        
        self.key = None
        """ Target of 'condition' reference above.
        Type `str`. """
        
        self.requirements = None
        """ Why this constraint is necessary or appropriate.
        Type `str`. """
        
        self.severity = None
        """ Identifies the impact constraint violation has on the conformance
        of the instance.
        Type `str`. """
        
        self.human = None
        """ Human description of constraint.
        Type `str`. """
        
        self.expression = None
        """ FHIRPath expression of constraint.
        Type `str`. """
        
        self.xpath = None
        """ XPath expression of constraint.
        Type `str`. """
        
        self.source = None
        """ Reference to original source of constraint.
        Type `str`. """
        
        super(ElementDefinitionConstraint, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ElementDefinitionConstraint, self).elementProperties()
        js.extend([
            ("key", "key", str, False, None, True),
            ("requirements", "requirements", str, False, None, False),
            ("severity", "severity", str, False, None, True),
            ("human", "human", str, False, None, True),
            ("expression", "expression", str, False, None, False),
            ("xpath", "xpath", str, False, None, False),
            ("source", "source", str, False, None, False),
        ])
        return js


class ElementDefinitionExample(element.Element):
    """ Example value (as defined for type).
    
    A sample value for this element demonstrating the type of information that
    would typically be found in the element.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['label'] = """Describes the purpose of this example."""
    _attribute_docstrings['valueBase64Binary'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueBoolean'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueCanonical'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueCode'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueDate'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueDateTime'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueDecimal'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueId'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueInstant'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueInteger'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueMarkdown'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueOid'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valuePositiveInt'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueString'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueTime'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueUnsignedInt'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueUri'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueUrl'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueUuid'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueAddress'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueAge'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueAnnotation'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueAttachment'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueCodeableConcept'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueCoding'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueContactPoint'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueCount'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueDistance'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueDuration'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueHumanName'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueIdentifier'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueMoney'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valuePeriod'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueQuantity'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueRange'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueRatio'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueReference'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueSampledData'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueSignature'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueTiming'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueContactDetail'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueContributor'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueDataRequirement'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueExpression'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueParameterDefinition'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueRelatedArtifact'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueTriggerDefinition'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueUsageContext'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueDosage'] = """Value of Example (one of allowed types)."""
    _attribute_docstrings['valueMeta'] = """Value of Example (one of allowed types)."""

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
        
        self.label = None
        """ Describes the purpose of this example.
        Type `str`. """
        
        self.valueBase64Binary = None
        """ Value of Example (one of allowed types).
        Type `str`. """
        
        self.valueBoolean = None
        """ Value of Example (one of allowed types).
        Type `bool`. """
        
        self.valueCanonical = None
        """ Value of Example (one of allowed types).
        Type `str`. """
        
        self.valueCode = None
        """ Value of Example (one of allowed types).
        Type `str`. """
        
        self.valueDate = None
        """ Value of Example (one of allowed types).
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valueDateTime = None
        """ Value of Example (one of allowed types).
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valueDecimal = None
        """ Value of Example (one of allowed types).
        Type `float`. """
        
        self.valueId = None
        """ Value of Example (one of allowed types).
        Type `str`. """
        
        self.valueInstant = None
        """ Value of Example (one of allowed types).
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valueInteger = None
        """ Value of Example (one of allowed types).
        Type `int`. """
        
        self.valueMarkdown = None
        """ Value of Example (one of allowed types).
        Type `str`. """
        
        self.valueOid = None
        """ Value of Example (one of allowed types).
        Type `str`. """
        
        self.valuePositiveInt = None
        """ Value of Example (one of allowed types).
        Type `int`. """
        
        self.valueString = None
        """ Value of Example (one of allowed types).
        Type `str`. """
        
        self.valueTime = None
        """ Value of Example (one of allowed types).
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valueUnsignedInt = None
        """ Value of Example (one of allowed types).
        Type `int`. """
        
        self.valueUri = None
        """ Value of Example (one of allowed types).
        Type `str`. """
        
        self.valueUrl = None
        """ Value of Example (one of allowed types).
        Type `str`. """
        
        self.valueUuid = None
        """ Value of Example (one of allowed types).
        Type `str`. """
        
        self.valueAddress = None
        """ Value of Example (one of allowed types).
        Type `Address` (represented as `dict` in JSON). """
        
        self.valueAge = None
        """ Value of Example (one of allowed types).
        Type `Age` (represented as `dict` in JSON). """
        
        self.valueAnnotation = None
        """ Value of Example (one of allowed types).
        Type `Annotation` (represented as `dict` in JSON). """
        
        self.valueAttachment = None
        """ Value of Example (one of allowed types).
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.valueCodeableConcept = None
        """ Value of Example (one of allowed types).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.valueCoding = None
        """ Value of Example (one of allowed types).
        Type `Coding` (represented as `dict` in JSON). """
        
        self.valueContactPoint = None
        """ Value of Example (one of allowed types).
        Type `ContactPoint` (represented as `dict` in JSON). """
        
        self.valueCount = None
        """ Value of Example (one of allowed types).
        Type `Count` (represented as `dict` in JSON). """
        
        self.valueDistance = None
        """ Value of Example (one of allowed types).
        Type `Distance` (represented as `dict` in JSON). """
        
        self.valueDuration = None
        """ Value of Example (one of allowed types).
        Type `Duration` (represented as `dict` in JSON). """
        
        self.valueHumanName = None
        """ Value of Example (one of allowed types).
        Type `HumanName` (represented as `dict` in JSON). """
        
        self.valueIdentifier = None
        """ Value of Example (one of allowed types).
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.valueMoney = None
        """ Value of Example (one of allowed types).
        Type `Money` (represented as `dict` in JSON). """
        
        self.valuePeriod = None
        """ Value of Example (one of allowed types).
        Type `Period` (represented as `dict` in JSON). """
        
        self.valueQuantity = None
        """ Value of Example (one of allowed types).
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.valueRange = None
        """ Value of Example (one of allowed types).
        Type `Range` (represented as `dict` in JSON). """
        
        self.valueRatio = None
        """ Value of Example (one of allowed types).
        Type `Ratio` (represented as `dict` in JSON). """
        
        self.valueReference = None
        """ Value of Example (one of allowed types).
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.valueSampledData = None
        """ Value of Example (one of allowed types).
        Type `SampledData` (represented as `dict` in JSON). """
        
        self.valueSignature = None
        """ Value of Example (one of allowed types).
        Type `Signature` (represented as `dict` in JSON). """
        
        self.valueTiming = None
        """ Value of Example (one of allowed types).
        Type `Timing` (represented as `dict` in JSON). """
        
        self.valueContactDetail = None
        """ Value of Example (one of allowed types).
        Type `ContactDetail` (represented as `dict` in JSON). """
        
        self.valueContributor = None
        """ Value of Example (one of allowed types).
        Type `Contributor` (represented as `dict` in JSON). """
        
        self.valueDataRequirement = None
        """ Value of Example (one of allowed types).
        Type `DataRequirement` (represented as `dict` in JSON). """
        
        self.valueExpression = None
        """ Value of Example (one of allowed types).
        Type `Expression` (represented as `dict` in JSON). """
        
        self.valueParameterDefinition = None
        """ Value of Example (one of allowed types).
        Type `ParameterDefinition` (represented as `dict` in JSON). """
        
        self.valueRelatedArtifact = None
        """ Value of Example (one of allowed types).
        Type `RelatedArtifact` (represented as `dict` in JSON). """
        
        self.valueTriggerDefinition = None
        """ Value of Example (one of allowed types).
        Type `TriggerDefinition` (represented as `dict` in JSON). """
        
        self.valueUsageContext = None
        """ Value of Example (one of allowed types).
        Type `UsageContext` (represented as `dict` in JSON). """
        
        self.valueDosage = None
        """ Value of Example (one of allowed types).
        Type `Dosage` (represented as `dict` in JSON). """
        
        self.valueMeta = None
        """ Value of Example (one of allowed types).
        Type `Meta` (represented as `dict` in JSON). """
        
        super(ElementDefinitionExample, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ElementDefinitionExample, self).elementProperties()
        js.extend([
            ("label", "label", str, False, None, True),
            ("valueBase64Binary", "valueBase64Binary", str, False, "value", True),
            ("valueBoolean", "valueBoolean", bool, False, "value", True),
            ("valueCanonical", "valueCanonical", str, False, "value", True),
            ("valueCode", "valueCode", str, False, "value", True),
            ("valueDate", "valueDate", fhirdate.FHIRDate, False, "value", True),
            ("valueDateTime", "valueDateTime", fhirdate.FHIRDate, False, "value", True),
            ("valueDecimal", "valueDecimal", float, False, "value", True),
            ("valueId", "valueId", str, False, "value", True),
            ("valueInstant", "valueInstant", fhirdate.FHIRDate, False, "value", True),
            ("valueInteger", "valueInteger", int, False, "value", True),
            ("valueMarkdown", "valueMarkdown", str, False, "value", True),
            ("valueOid", "valueOid", str, False, "value", True),
            ("valuePositiveInt", "valuePositiveInt", int, False, "value", True),
            ("valueString", "valueString", str, False, "value", True),
            ("valueTime", "valueTime", fhirdate.FHIRDate, False, "value", True),
            ("valueUnsignedInt", "valueUnsignedInt", int, False, "value", True),
            ("valueUri", "valueUri", str, False, "value", True),
            ("valueUrl", "valueUrl", str, False, "value", True),
            ("valueUuid", "valueUuid", str, False, "value", True),
            ("valueAddress", "valueAddress", address.Address, False, "value", True),
            ("valueAge", "valueAge", age.Age, False, "value", True),
            ("valueAnnotation", "valueAnnotation", annotation.Annotation, False, "value", True),
            ("valueAttachment", "valueAttachment", attachment.Attachment, False, "value", True),
            ("valueCodeableConcept", "valueCodeableConcept", codeableconcept.CodeableConcept, False, "value", True),
            ("valueCoding", "valueCoding", coding.Coding, False, "value", True),
            ("valueContactPoint", "valueContactPoint", contactpoint.ContactPoint, False, "value", True),
            ("valueCount", "valueCount", count.Count, False, "value", True),
            ("valueDistance", "valueDistance", distance.Distance, False, "value", True),
            ("valueDuration", "valueDuration", duration.Duration, False, "value", True),
            ("valueHumanName", "valueHumanName", humanname.HumanName, False, "value", True),
            ("valueIdentifier", "valueIdentifier", identifier.Identifier, False, "value", True),
            ("valueMoney", "valueMoney", money.Money, False, "value", True),
            ("valuePeriod", "valuePeriod", period.Period, False, "value", True),
            ("valueQuantity", "valueQuantity", quantity.Quantity, False, "value", True),
            ("valueRange", "valueRange", range.Range, False, "value", True),
            ("valueRatio", "valueRatio", ratio.Ratio, False, "value", True),
            ("valueReference", "valueReference", fhirreference.FHIRReference, False, "value", True),
            ("valueSampledData", "valueSampledData", sampleddata.SampledData, False, "value", True),
            ("valueSignature", "valueSignature", signature.Signature, False, "value", True),
            ("valueTiming", "valueTiming", timing.Timing, False, "value", True),
            ("valueContactDetail", "valueContactDetail", contactdetail.ContactDetail, False, "value", True),
            ("valueContributor", "valueContributor", contributor.Contributor, False, "value", True),
            ("valueDataRequirement", "valueDataRequirement", datarequirement.DataRequirement, False, "value", True),
            ("valueExpression", "valueExpression", expression.Expression, False, "value", True),
            ("valueParameterDefinition", "valueParameterDefinition", parameterdefinition.ParameterDefinition, False, "value", True),
            ("valueRelatedArtifact", "valueRelatedArtifact", relatedartifact.RelatedArtifact, False, "value", True),
            ("valueTriggerDefinition", "valueTriggerDefinition", triggerdefinition.TriggerDefinition, False, "value", True),
            ("valueUsageContext", "valueUsageContext", usagecontext.UsageContext, False, "value", True),
            ("valueDosage", "valueDosage", dosage.Dosage, False, "value", True),
            ("valueMeta", "valueMeta", meta.Meta, False, "value", True),
        ])
        return js


class ElementDefinitionMapping(element.Element):
    """ Map element to another set of definitions.
    
    Identifies a concept from an external specification that roughly
    corresponds to this element.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identity'] = """Reference to mapping declaration."""
    _attribute_docstrings['language'] = """Computable language of mapping."""
    _attribute_docstrings['map'] = """Details of the mapping."""
    _attribute_docstrings['comment'] = """Comments about the mapping or its use."""

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
        """ Reference to mapping declaration.
        Type `str`. """
        
        self.language = None
        """ Computable language of mapping.
        Type `str`. """
        
        self.map = None
        """ Details of the mapping.
        Type `str`. """
        
        self.comment = None
        """ Comments about the mapping or its use.
        Type `str`. """
        
        super(ElementDefinitionMapping, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ElementDefinitionMapping, self).elementProperties()
        js.extend([
            ("identity", "identity", str, False, None, True),
            ("language", "language", str, False, None, False),
            ("map", "map", str, False, None, True),
            ("comment", "comment", str, False, None, False),
        ])
        return js


class ElementDefinitionSlicing(element.Element):
    """ This element is sliced - slices follow.
    
    Indicates that the element is sliced into a set of alternative definitions
    (i.e. in a structure definition, there are multiple different constraints
    on a single element in the base resource). Slicing can be used in any
    resource that has cardinality ..* on the base resource, or any resource
    with a choice of types. The set of slices is any elements that come after
    this in the element sequence that have the same path, until a shorter path
    occurs (the shorter path terminates the set).
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['discriminator'] = """Element values that are used to distinguish the slices."""
    _attribute_docstrings['description'] = """Text description of how slicing works (or not)."""
    _attribute_docstrings['ordered'] = """If elements must be in same order as slices."""
    _attribute_docstrings['rules'] = """Whether additional slices are allowed or not. When the slices are ordered, profile authors can also say that additional slices are only allowed at the end."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['rules'] = {
        'url': 'http://hl7.org/fhir/resource-slicing-rules',
        'restricted_to': ['closed', 'open', 'openAtEnd'],
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
        
        self.discriminator = None
        """ Element values that are used to distinguish the slices.
        List of `ElementDefinitionSlicingDiscriminator` items (represented as `dict` in JSON). """
        
        self.description = None
        """ Text description of how slicing works (or not).
        Type `str`. """
        
        self.ordered = None
        """ If elements must be in same order as slices.
        Type `bool`. """
        
        self.rules = None
        """ Whether additional slices are allowed or not. When the slices are
        ordered, profile authors can also say that additional slices are
        only allowed at the end.
        Type `str`. """
        
        super(ElementDefinitionSlicing, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ElementDefinitionSlicing, self).elementProperties()
        js.extend([
            ("discriminator", "discriminator", ElementDefinitionSlicingDiscriminator, True, None, False),
            ("description", "description", str, False, None, False),
            ("ordered", "ordered", bool, False, None, False),
            ("rules", "rules", str, False, None, True),
        ])
        return js


class ElementDefinitionSlicingDiscriminator(element.Element):
    """ Element values that are used to distinguish the slices.
    
    Designates which child elements are used to discriminate between the slices
    when processing an instance. If one or more discriminators are provided,
    the value of the child elements in the instance data SHALL completely
    distinguish which slice the element in the resource matches based on the
    allowed values for those elements in each of the slices.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """How the element value is interpreted when discrimination is evaluated."""
    _attribute_docstrings['path'] = """Path to element value."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://hl7.org/fhir/discriminator-type',
        'restricted_to': ['value', 'exists', 'pattern', 'type', 'profile'],
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
        """ How the element value is interpreted when discrimination is
        evaluated.
        Type `str`. """
        
        self.path = None
        """ Path to element value.
        Type `str`. """
        
        super(ElementDefinitionSlicingDiscriminator, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ElementDefinitionSlicingDiscriminator, self).elementProperties()
        js.extend([
            ("type", "type", str, False, None, True),
            ("path", "path", str, False, None, True),
        ])
        return js


class ElementDefinitionType(element.Element):
    """ Data type and Profile for this element.
    
    The data type or resource that the value of this element is permitted to
    be.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Data type or Resource (reference to definition)."""
    _attribute_docstrings['profile'] = """Profiles (StructureDefinition or IG) - one must apply."""
    _attribute_docstrings['targetProfile'] = """Profile (StructureDefinition or IG) on the Reference/canonical target - one must apply."""
    _attribute_docstrings['aggregation'] = """If the type is a reference to another resource, how the resource is or can be aggregated - is it a contained resource, or a reference, and if the context is a bundle, is it included in the bundle."""
    _attribute_docstrings['versioning'] = """Whether this reference needs to be version specific or version independent, or whether either can be used."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['aggregation'] = {
        'url': 'http://hl7.org/fhir/resource-aggregation-mode',
        'restricted_to': ['contained', 'referenced', 'bundled'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['versioning'] = {
        'url': 'http://hl7.org/fhir/reference-version-rules',
        'restricted_to': ['either', 'independent', 'specific'],
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
        """ Data type or Resource (reference to definition).
        Type `str`. """
        
        self.profile = None
        """ Profiles (StructureDefinition or IG) - one must apply.
        List of `str` items. """
        
        self.targetProfile = None
        """ Profile (StructureDefinition or IG) on the Reference/canonical
        target - one must apply.
        List of `str` items. """
        
        self.aggregation = None
        """ If the type is a reference to another resource, how the resource is
        or can be aggregated - is it a contained resource, or a reference,
        and if the context is a bundle, is it included in the bundle.
        List of `str` items. """
        
        self.versioning = None
        """ Whether this reference needs to be version specific or version
        independent, or whether either can be used.
        Type `str`. """
        
        super(ElementDefinitionType, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ElementDefinitionType, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, True),
            ("profile", "profile", str, True, None, False),
            ("targetProfile", "targetProfile", str, True, None, False),
            ("aggregation", "aggregation", str, True, None, False),
            ("versioning", "versioning", str, False, None, False),
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
