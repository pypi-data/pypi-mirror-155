#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Observation) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Observation(domainresource.DomainResource):
    """ Measurements and simple assertions.
    
    Measurements and simple assertions made about a patient, device or other
    subject.
    """
    
    resource_type = "Observation"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business Identifier for observation."""
    _attribute_docstrings['basedOn'] = """Fulfills plan, proposal or order."""
    _attribute_docstrings['partOf'] = """Part of referenced event."""
    _attribute_docstrings['status'] = """The status of the result value."""
    _attribute_docstrings['category'] = """A code that classifies the general type of observation being made."""
    _attribute_docstrings['code'] = """Type of observation (code / type)."""
    _attribute_docstrings['subject'] = """Who and/or what the observation is about."""
    _attribute_docstrings['focus'] = """What the observation is about, when it is not about the subject of record."""
    _attribute_docstrings['encounter'] = """Healthcare event during which this observation is made."""
    _attribute_docstrings['effectiveDateTime'] = """Clinically relevant time/time-period for observation."""
    _attribute_docstrings['effectivePeriod'] = """Clinically relevant time/time-period for observation."""
    _attribute_docstrings['effectiveTiming'] = """Clinically relevant time/time-period for observation."""
    _attribute_docstrings['effectiveInstant'] = """Clinically relevant time/time-period for observation."""
    _attribute_docstrings['issued'] = """Date/Time this version was made available."""
    _attribute_docstrings['performer'] = """Who is responsible for the observation."""
    _attribute_docstrings['valueQuantity'] = """Actual result."""
    _attribute_docstrings['valueCodeableConcept'] = """Actual result."""
    _attribute_docstrings['valueString'] = """Actual result."""
    _attribute_docstrings['valueBoolean'] = """Actual result."""
    _attribute_docstrings['valueInteger'] = """Actual result."""
    _attribute_docstrings['valueRange'] = """Actual result."""
    _attribute_docstrings['valueRatio'] = """Actual result."""
    _attribute_docstrings['valueSampledData'] = """Actual result."""
    _attribute_docstrings['valueTime'] = """Actual result."""
    _attribute_docstrings['valueDateTime'] = """Actual result."""
    _attribute_docstrings['valuePeriod'] = """Actual result."""
    _attribute_docstrings['dataAbsentReason'] = """Provides a reason why the expected value in the element Observation.value[x] is missing."""
    _attribute_docstrings['interpretation'] = """High, low, normal, etc.."""
    _attribute_docstrings['note'] = """Comments about the observation."""
    _attribute_docstrings['bodySite'] = """Observed body part."""
    _attribute_docstrings['method'] = """How it was done."""
    _attribute_docstrings['specimen'] = """Specimen used for this observation."""
    _attribute_docstrings['device'] = """(Measurement) Device."""
    _attribute_docstrings['referenceRange'] = """Provides guide for interpretation."""
    _attribute_docstrings['hasMember'] = """Related resource that belongs to the Observation group."""
    _attribute_docstrings['derivedFrom'] = """Related measurements the observation is made from."""
    _attribute_docstrings['component'] = """Component results."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/observation-status',
        'restricted_to': ['registered', 'preliminary', 'final', 'amended', 'corrected', 'cancelled', 'entered-in-error', 'unknown'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['category'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/observation-category',
        'restricted_to': ['social-history', 'vital-signs', 'imaging', 'laboratory', 'procedure', 'survey', 'exam', 'therapy', 'activity'],
        'binding_strength': 'preferred',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['dataAbsentReason'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/data-absent-reason',
        'restricted_to': ['unknown', 'asked-unknown', 'temp-unknown', 'not-asked', 'asked-declined', 'masked', 'not-applicable', 'unsupported', 'as-text', 'error', 'not-a-number', 'negative-infinity', 'positive-infinity', 'not-performed', 'not-permitted'],
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
        
        self.identifier = None
        """ Business Identifier for observation.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.basedOn = None
        """ Fulfills plan, proposal or order.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.partOf = None
        """ Part of referenced event.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.status = None
        """ The status of the result value.
        Type `str`. """
        
        self.category = None
        """ A code that classifies the general type of observation being made.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.code = None
        """ Type of observation (code / type).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subject = None
        """ Who and/or what the observation is about.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.focus = None
        """ What the observation is about, when it is not about the subject of
        record.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Healthcare event during which this observation is made.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.effectiveDateTime = None
        """ Clinically relevant time/time-period for observation.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.effectivePeriod = None
        """ Clinically relevant time/time-period for observation.
        Type `Period` (represented as `dict` in JSON). """
        
        self.effectiveTiming = None
        """ Clinically relevant time/time-period for observation.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.effectiveInstant = None
        """ Clinically relevant time/time-period for observation.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.issued = None
        """ Date/Time this version was made available.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.performer = None
        """ Who is responsible for the observation.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.valueQuantity = None
        """ Actual result.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.valueCodeableConcept = None
        """ Actual result.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.valueString = None
        """ Actual result.
        Type `str`. """
        
        self.valueBoolean = None
        """ Actual result.
        Type `bool`. """
        
        self.valueInteger = None
        """ Actual result.
        Type `int`. """
        
        self.valueRange = None
        """ Actual result.
        Type `Range` (represented as `dict` in JSON). """
        
        self.valueRatio = None
        """ Actual result.
        Type `Ratio` (represented as `dict` in JSON). """
        
        self.valueSampledData = None
        """ Actual result.
        Type `SampledData` (represented as `dict` in JSON). """
        
        self.valueTime = None
        """ Actual result.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valueDateTime = None
        """ Actual result.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valuePeriod = None
        """ Actual result.
        Type `Period` (represented as `dict` in JSON). """
        
        self.dataAbsentReason = None
        """ Provides a reason why the expected value in the element
        Observation.value[x] is missing.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.interpretation = None
        """ High, low, normal, etc.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.note = None
        """ Comments about the observation.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        self.bodySite = None
        """ Observed body part.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.method = None
        """ How it was done.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.specimen = None
        """ Specimen used for this observation.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.device = None
        """ (Measurement) Device.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.referenceRange = None
        """ Provides guide for interpretation.
        List of `ObservationReferenceRange` items (represented as `dict` in JSON). """
        
        self.hasMember = None
        """ Related resource that belongs to the Observation group.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.derivedFrom = None
        """ Related measurements the observation is made from.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.component = None
        """ Component results.
        List of `ObservationComponent` items (represented as `dict` in JSON). """
        
        super(Observation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Observation, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("basedOn", "basedOn", fhirreference.FHIRReference, True, None, False),
            ("partOf", "partOf", fhirreference.FHIRReference, True, None, False),
            ("status", "status", str, False, None, True),
            ("category", "category", codeableconcept.CodeableConcept, True, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, True),
            ("subject", "subject", fhirreference.FHIRReference, False, None, False),
            ("focus", "focus", fhirreference.FHIRReference, True, None, False),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("effectiveDateTime", "effectiveDateTime", fhirdate.FHIRDate, False, "effective", False),
            ("effectivePeriod", "effectivePeriod", period.Period, False, "effective", False),
            ("effectiveTiming", "effectiveTiming", timing.Timing, False, "effective", False),
            ("effectiveInstant", "effectiveInstant", fhirdate.FHIRDate, False, "effective", False),
            ("issued", "issued", fhirdate.FHIRDate, False, None, False),
            ("performer", "performer", fhirreference.FHIRReference, True, None, False),
            ("valueQuantity", "valueQuantity", quantity.Quantity, False, "value", False),
            ("valueCodeableConcept", "valueCodeableConcept", codeableconcept.CodeableConcept, False, "value", False),
            ("valueString", "valueString", str, False, "value", False),
            ("valueBoolean", "valueBoolean", bool, False, "value", False),
            ("valueInteger", "valueInteger", int, False, "value", False),
            ("valueRange", "valueRange", range.Range, False, "value", False),
            ("valueRatio", "valueRatio", ratio.Ratio, False, "value", False),
            ("valueSampledData", "valueSampledData", sampleddata.SampledData, False, "value", False),
            ("valueTime", "valueTime", fhirdate.FHIRDate, False, "value", False),
            ("valueDateTime", "valueDateTime", fhirdate.FHIRDate, False, "value", False),
            ("valuePeriod", "valuePeriod", period.Period, False, "value", False),
            ("dataAbsentReason", "dataAbsentReason", codeableconcept.CodeableConcept, False, None, False),
            ("interpretation", "interpretation", codeableconcept.CodeableConcept, True, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
            ("bodySite", "bodySite", codeableconcept.CodeableConcept, False, None, False),
            ("method", "method", codeableconcept.CodeableConcept, False, None, False),
            ("specimen", "specimen", fhirreference.FHIRReference, False, None, False),
            ("device", "device", fhirreference.FHIRReference, False, None, False),
            ("referenceRange", "referenceRange", ObservationReferenceRange, True, None, False),
            ("hasMember", "hasMember", fhirreference.FHIRReference, True, None, False),
            ("derivedFrom", "derivedFrom", fhirreference.FHIRReference, True, None, False),
            ("component", "component", ObservationComponent, True, None, False),
        ])
        return js


from . import backboneelement

class ObservationComponent(backboneelement.BackboneElement):
    """ Component results.
    
    Some observations have multiple component observations.  These component
    observations are expressed as separate code value pairs that share the same
    attributes.  Examples include systolic and diastolic component observations
    for blood pressure measurement and multiple component observations for
    genetics observations.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Type of component observation (code / type)."""
    _attribute_docstrings['valueQuantity'] = """Actual component result."""
    _attribute_docstrings['valueCodeableConcept'] = """Actual component result."""
    _attribute_docstrings['valueString'] = """Actual component result."""
    _attribute_docstrings['valueBoolean'] = """Actual component result."""
    _attribute_docstrings['valueInteger'] = """Actual component result."""
    _attribute_docstrings['valueRange'] = """Actual component result."""
    _attribute_docstrings['valueRatio'] = """Actual component result."""
    _attribute_docstrings['valueSampledData'] = """Actual component result."""
    _attribute_docstrings['valueTime'] = """Actual component result."""
    _attribute_docstrings['valueDateTime'] = """Actual component result."""
    _attribute_docstrings['valuePeriod'] = """Actual component result."""
    _attribute_docstrings['dataAbsentReason'] = """Provides a reason why the expected value in the element Observation.component.value[x] is missing."""
    _attribute_docstrings['interpretation'] = """High, low, normal, etc.."""
    _attribute_docstrings['referenceRange'] = """Provides guide for interpretation of component result."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['dataAbsentReason'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/data-absent-reason',
        'restricted_to': ['unknown', 'asked-unknown', 'temp-unknown', 'not-asked', 'asked-declined', 'masked', 'not-applicable', 'unsupported', 'as-text', 'error', 'not-a-number', 'negative-infinity', 'positive-infinity', 'not-performed', 'not-permitted'],
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
        
        self.code = None
        """ Type of component observation (code / type).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.valueQuantity = None
        """ Actual component result.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.valueCodeableConcept = None
        """ Actual component result.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.valueString = None
        """ Actual component result.
        Type `str`. """
        
        self.valueBoolean = None
        """ Actual component result.
        Type `bool`. """
        
        self.valueInteger = None
        """ Actual component result.
        Type `int`. """
        
        self.valueRange = None
        """ Actual component result.
        Type `Range` (represented as `dict` in JSON). """
        
        self.valueRatio = None
        """ Actual component result.
        Type `Ratio` (represented as `dict` in JSON). """
        
        self.valueSampledData = None
        """ Actual component result.
        Type `SampledData` (represented as `dict` in JSON). """
        
        self.valueTime = None
        """ Actual component result.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valueDateTime = None
        """ Actual component result.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valuePeriod = None
        """ Actual component result.
        Type `Period` (represented as `dict` in JSON). """
        
        self.dataAbsentReason = None
        """ Provides a reason why the expected value in the element
        Observation.component.value[x] is missing.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.interpretation = None
        """ High, low, normal, etc.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.referenceRange = None
        """ Provides guide for interpretation of component result.
        List of `ObservationReferenceRange` items (represented as `dict` in JSON). """
        
        super(ObservationComponent, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ObservationComponent, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, False, None, True),
            ("valueQuantity", "valueQuantity", quantity.Quantity, False, "value", False),
            ("valueCodeableConcept", "valueCodeableConcept", codeableconcept.CodeableConcept, False, "value", False),
            ("valueString", "valueString", str, False, "value", False),
            ("valueBoolean", "valueBoolean", bool, False, "value", False),
            ("valueInteger", "valueInteger", int, False, "value", False),
            ("valueRange", "valueRange", range.Range, False, "value", False),
            ("valueRatio", "valueRatio", ratio.Ratio, False, "value", False),
            ("valueSampledData", "valueSampledData", sampleddata.SampledData, False, "value", False),
            ("valueTime", "valueTime", fhirdate.FHIRDate, False, "value", False),
            ("valueDateTime", "valueDateTime", fhirdate.FHIRDate, False, "value", False),
            ("valuePeriod", "valuePeriod", period.Period, False, "value", False),
            ("dataAbsentReason", "dataAbsentReason", codeableconcept.CodeableConcept, False, None, False),
            ("interpretation", "interpretation", codeableconcept.CodeableConcept, True, None, False),
            ("referenceRange", "referenceRange", ObservationReferenceRange, True, None, False),
        ])
        return js


class ObservationReferenceRange(backboneelement.BackboneElement):
    """ Provides guide for interpretation.
    
    Guidance on how to interpret the value by comparison to a normal or
    recommended range.  Multiple reference ranges are interpreted as an "OR".
    In other words, to represent two distinct target populations, two
    `referenceRange` elements would be used.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['low'] = """Low Range, if relevant."""
    _attribute_docstrings['high'] = """High Range, if relevant."""
    _attribute_docstrings['type'] = """Codes to indicate the what part of the targeted reference population it applies to. For example, the normal or therapeutic range."""
    _attribute_docstrings['appliesTo'] = """Reference range population."""
    _attribute_docstrings['age'] = """Applicable age range, if relevant."""
    _attribute_docstrings['text'] = """Text based reference range in an observation."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/referencerange-meaning',
        'restricted_to': ['type', 'normal', 'recommended', 'treatment', 'therapeutic', 'pre', 'post', 'endocrine', 'pre-puberty', 'follicular', 'midcycle', 'luteal', 'postmenopausal'],
        'binding_strength': 'preferred',
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
        
        self.low = None
        """ Low Range, if relevant.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.high = None
        """ High Range, if relevant.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.type = None
        """ Codes to indicate the what part of the targeted reference
        population it applies to. For example, the normal or therapeutic
        range.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.appliesTo = None
        """ Reference range population.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.age = None
        """ Applicable age range, if relevant.
        Type `Range` (represented as `dict` in JSON). """
        
        self.text = None
        """ Text based reference range in an observation.
        Type `str`. """
        
        super(ObservationReferenceRange, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ObservationReferenceRange, self).elementProperties()
        js.extend([
            ("low", "low", quantity.Quantity, False, None, False),
            ("high", "high", quantity.Quantity, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("appliesTo", "appliesTo", codeableconcept.CodeableConcept, True, None, False),
            ("age", "age", range.Range, False, None, False),
            ("text", "text", str, False, None, False),
        ])
        return js


import sys
try:
    from . import annotation
except ImportError:
    annotation = sys.modules[__package__ + '.annotation']
try:
    from . import codeableconcept
except ImportError:
    codeableconcept = sys.modules[__package__ + '.codeableconcept']
try:
    from . import fhirdate
except ImportError:
    fhirdate = sys.modules[__package__ + '.fhirdate']
try:
    from . import fhirreference
except ImportError:
    fhirreference = sys.modules[__package__ + '.fhirreference']
try:
    from . import identifier
except ImportError:
    identifier = sys.modules[__package__ + '.identifier']
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
    from . import sampleddata
except ImportError:
    sampleddata = sys.modules[__package__ + '.sampleddata']
try:
    from . import timing
except ImportError:
    timing = sys.modules[__package__ + '.timing']
