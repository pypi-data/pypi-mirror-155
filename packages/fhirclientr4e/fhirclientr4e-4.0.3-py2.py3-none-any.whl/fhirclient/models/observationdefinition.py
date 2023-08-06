#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/ObservationDefinition) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class ObservationDefinition(domainresource.DomainResource):
    """ Definition of an observation.
    
    Set of definitional characteristics for a kind of observation or
    measurement produced or consumed by an orderable health care service.
    """
    
    resource_type = "ObservationDefinition"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['category'] = """A code that classifies the general type of observation."""
    _attribute_docstrings['code'] = """Type of observation (code / type)."""
    _attribute_docstrings['identifier'] = """Business identifier for this ObservationDefinition instance."""
    _attribute_docstrings['permittedDataType'] = """The data types allowed for the value element of the instance observations conforming to this ObservationDefinition."""
    _attribute_docstrings['multipleResultsAllowed'] = """Multiple results allowed."""
    _attribute_docstrings['method'] = """Method used to produce the observation."""
    _attribute_docstrings['preferredReportName'] = """Preferred report name."""
    _attribute_docstrings['quantitativeDetails'] = """Characteristics of quantitative results."""
    _attribute_docstrings['qualifiedInterval'] = """Qualified range for continuous and ordinal observation results."""
    _attribute_docstrings['validCodedValueSet'] = """Value set of valid coded values for the observations conforming to this ObservationDefinition."""
    _attribute_docstrings['normalCodedValueSet'] = """Value set of normal coded values for the observations conforming to this ObservationDefinition."""
    _attribute_docstrings['abnormalCodedValueSet'] = """Value set of abnormal coded values for the observations conforming to this ObservationDefinition."""
    _attribute_docstrings['criticalCodedValueSet'] = """Value set of critical coded values for the observations conforming to this ObservationDefinition."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['category'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/observation-category',
        'restricted_to': ['social-history', 'vital-signs', 'imaging', 'laboratory', 'procedure', 'survey', 'exam', 'therapy', 'activity'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['permittedDataType'] = {
        'url': 'http://hl7.org/fhir/permitted-data-type',
        'restricted_to': ['Quantity', 'CodeableConcept', 'string', 'boolean', 'integer', 'Range', 'Ratio', 'SampledData', 'time', 'dateTime', 'Period'],
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
        
        self.category = None
        """ A code that classifies the general type of observation.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.code = None
        """ Type of observation (code / type).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.identifier = None
        """ Business identifier for this ObservationDefinition instance.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.permittedDataType = None
        """ The data types allowed for the value element of the instance
        observations conforming to this ObservationDefinition.
        List of `str` items. """
        
        self.multipleResultsAllowed = None
        """ Multiple results allowed.
        Type `bool`. """
        
        self.method = None
        """ Method used to produce the observation.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.preferredReportName = None
        """ Preferred report name.
        Type `str`. """
        
        self.quantitativeDetails = None
        """ Characteristics of quantitative results.
        Type `ObservationDefinitionQuantitativeDetails` (represented as `dict` in JSON). """
        
        self.qualifiedInterval = None
        """ Qualified range for continuous and ordinal observation results.
        List of `ObservationDefinitionQualifiedInterval` items (represented as `dict` in JSON). """
        
        self.validCodedValueSet = None
        """ Value set of valid coded values for the observations conforming to
        this ObservationDefinition.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.normalCodedValueSet = None
        """ Value set of normal coded values for the observations conforming to
        this ObservationDefinition.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.abnormalCodedValueSet = None
        """ Value set of abnormal coded values for the observations conforming
        to this ObservationDefinition.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.criticalCodedValueSet = None
        """ Value set of critical coded values for the observations conforming
        to this ObservationDefinition.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(ObservationDefinition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ObservationDefinition, self).elementProperties()
        js.extend([
            ("category", "category", codeableconcept.CodeableConcept, True, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, True),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("permittedDataType", "permittedDataType", str, True, None, False),
            ("multipleResultsAllowed", "multipleResultsAllowed", bool, False, None, False),
            ("method", "method", codeableconcept.CodeableConcept, False, None, False),
            ("preferredReportName", "preferredReportName", str, False, None, False),
            ("quantitativeDetails", "quantitativeDetails", ObservationDefinitionQuantitativeDetails, False, None, False),
            ("qualifiedInterval", "qualifiedInterval", ObservationDefinitionQualifiedInterval, True, None, False),
            ("validCodedValueSet", "validCodedValueSet", fhirreference.FHIRReference, False, None, False),
            ("normalCodedValueSet", "normalCodedValueSet", fhirreference.FHIRReference, False, None, False),
            ("abnormalCodedValueSet", "abnormalCodedValueSet", fhirreference.FHIRReference, False, None, False),
            ("criticalCodedValueSet", "criticalCodedValueSet", fhirreference.FHIRReference, False, None, False),
        ])
        return js


from . import backboneelement

class ObservationDefinitionQualifiedInterval(backboneelement.BackboneElement):
    """ Qualified range for continuous and ordinal observation results.
    
    Multiple  ranges of results qualified by different contexts for ordinal or
    continuous observations conforming to this ObservationDefinition.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['category'] = """The category of interval of values for continuous or ordinal observations conforming to this ObservationDefinition."""
    _attribute_docstrings['range'] = """The interval itself, for continuous or ordinal observations."""
    _attribute_docstrings['context'] = """Codes to indicate the health context the range applies to. For example, the normal or therapeutic range."""
    _attribute_docstrings['appliesTo'] = """Targetted population of the range."""
    _attribute_docstrings['gender'] = """Sex of the population the range applies to."""
    _attribute_docstrings['age'] = """Applicable age range, if relevant."""
    _attribute_docstrings['gestationalAge'] = """Applicable gestational age range, if relevant."""
    _attribute_docstrings['condition'] = """Condition associated with the reference range."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['category'] = {
        'url': 'http://hl7.org/fhir/observation-range-category',
        'restricted_to': ['reference', 'critical', 'absolute'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['context'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/referencerange-meaning',
        'restricted_to': ['type', 'normal', 'recommended', 'treatment', 'therapeutic', 'pre', 'post', 'endocrine', 'pre-puberty', 'follicular', 'midcycle', 'luteal', 'postmenopausal'],
        'binding_strength': 'extensible',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['gender'] = {
        'url': 'http://hl7.org/fhir/administrative-gender',
        'restricted_to': ['male', 'female', 'other', 'unknown'],
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
        
        self.category = None
        """ The category of interval of values for continuous or ordinal
        observations conforming to this ObservationDefinition.
        Type `str`. """
        
        self.range = None
        """ The interval itself, for continuous or ordinal observations.
        Type `Range` (represented as `dict` in JSON). """
        
        self.context = None
        """ Codes to indicate the health context the range applies to. For
        example, the normal or therapeutic range.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.appliesTo = None
        """ Targetted population of the range.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.gender = None
        """ Sex of the population the range applies to.
        Type `str`. """
        
        self.age = None
        """ Applicable age range, if relevant.
        Type `Range` (represented as `dict` in JSON). """
        
        self.gestationalAge = None
        """ Applicable gestational age range, if relevant.
        Type `Range` (represented as `dict` in JSON). """
        
        self.condition = None
        """ Condition associated with the reference range.
        Type `str`. """
        
        super(ObservationDefinitionQualifiedInterval, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ObservationDefinitionQualifiedInterval, self).elementProperties()
        js.extend([
            ("category", "category", str, False, None, False),
            ("range", "range", range.Range, False, None, False),
            ("context", "context", codeableconcept.CodeableConcept, False, None, False),
            ("appliesTo", "appliesTo", codeableconcept.CodeableConcept, True, None, False),
            ("gender", "gender", str, False, None, False),
            ("age", "age", range.Range, False, None, False),
            ("gestationalAge", "gestationalAge", range.Range, False, None, False),
            ("condition", "condition", str, False, None, False),
        ])
        return js


class ObservationDefinitionQuantitativeDetails(backboneelement.BackboneElement):
    """ Characteristics of quantitative results.
    
    Characteristics for quantitative results of this observation.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['customaryUnit'] = """Customary unit for quantitative results."""
    _attribute_docstrings['unit'] = """SI unit for quantitative results."""
    _attribute_docstrings['conversionFactor'] = """SI to Customary unit conversion factor."""
    _attribute_docstrings['decimalPrecision'] = """Decimal precision of observation quantitative results."""

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
        
        self.customaryUnit = None
        """ Customary unit for quantitative results.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.unit = None
        """ SI unit for quantitative results.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.conversionFactor = None
        """ SI to Customary unit conversion factor.
        Type `float`. """
        
        self.decimalPrecision = None
        """ Decimal precision of observation quantitative results.
        Type `int`. """
        
        super(ObservationDefinitionQuantitativeDetails, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ObservationDefinitionQuantitativeDetails, self).elementProperties()
        js.extend([
            ("customaryUnit", "customaryUnit", codeableconcept.CodeableConcept, False, None, False),
            ("unit", "unit", codeableconcept.CodeableConcept, False, None, False),
            ("conversionFactor", "conversionFactor", float, False, None, False),
            ("decimalPrecision", "decimalPrecision", int, False, None, False),
        ])
        return js


import sys
try:
    from . import codeableconcept
except ImportError:
    codeableconcept = sys.modules[__package__ + '.codeableconcept']
try:
    from . import fhirreference
except ImportError:
    fhirreference = sys.modules[__package__ + '.fhirreference']
try:
    from . import identifier
except ImportError:
    identifier = sys.modules[__package__ + '.identifier']
try:
    from . import range
except ImportError:
    range = sys.modules[__package__ + '.range']
