#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/RiskAssessment) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class RiskAssessment(domainresource.DomainResource):
    """ Potential outcomes for a subject with likelihood.
    
    An assessment of the likely outcome(s) for a patient or other subject as
    well as the likelihood of each outcome.
    """
    
    resource_type = "RiskAssessment"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Unique identifier for the assessment."""
    _attribute_docstrings['basedOn'] = """Request fulfilled by this assessment."""
    _attribute_docstrings['parent'] = """Part of this occurrence."""
    _attribute_docstrings['status'] = """The status of the RiskAssessment, using the same statuses as an Observation."""
    _attribute_docstrings['method'] = """Evaluation mechanism."""
    _attribute_docstrings['code'] = """Type of assessment."""
    _attribute_docstrings['subject'] = """Who/what does assessment apply to?."""
    _attribute_docstrings['encounter'] = """Where was assessment performed?."""
    _attribute_docstrings['occurrenceDateTime'] = """When was assessment made?."""
    _attribute_docstrings['occurrencePeriod'] = """When was assessment made?."""
    _attribute_docstrings['condition'] = """Condition assessed."""
    _attribute_docstrings['performer'] = """Who did assessment?."""
    _attribute_docstrings['reasonCode'] = """Why the assessment was necessary?."""
    _attribute_docstrings['reasonReference'] = """Why the assessment was necessary?."""
    _attribute_docstrings['basis'] = """Information used in assessment."""
    _attribute_docstrings['prediction'] = """Outcome predicted."""
    _attribute_docstrings['mitigation'] = """How to reduce risk."""
    _attribute_docstrings['note'] = """Comments on the risk assessment."""

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
        """ Unique identifier for the assessment.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.basedOn = None
        """ Request fulfilled by this assessment.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.parent = None
        """ Part of this occurrence.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.status = None
        """ The status of the RiskAssessment, using the same statuses as an
        Observation.
        Type `str`. """
        
        self.method = None
        """ Evaluation mechanism.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.code = None
        """ Type of assessment.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subject = None
        """ Who/what does assessment apply to?.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Where was assessment performed?.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.occurrenceDateTime = None
        """ When was assessment made?.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.occurrencePeriod = None
        """ When was assessment made?.
        Type `Period` (represented as `dict` in JSON). """
        
        self.condition = None
        """ Condition assessed.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.performer = None
        """ Who did assessment?.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.reasonCode = None
        """ Why the assessment was necessary?.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.reasonReference = None
        """ Why the assessment was necessary?.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.basis = None
        """ Information used in assessment.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.prediction = None
        """ Outcome predicted.
        List of `RiskAssessmentPrediction` items (represented as `dict` in JSON). """
        
        self.mitigation = None
        """ How to reduce risk.
        Type `str`. """
        
        self.note = None
        """ Comments on the risk assessment.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        super(RiskAssessment, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(RiskAssessment, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("basedOn", "basedOn", fhirreference.FHIRReference, False, None, False),
            ("parent", "parent", fhirreference.FHIRReference, False, None, False),
            ("status", "status", str, False, None, True),
            ("method", "method", codeableconcept.CodeableConcept, False, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("subject", "subject", fhirreference.FHIRReference, False, None, True),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("occurrenceDateTime", "occurrenceDateTime", fhirdate.FHIRDate, False, "occurrence", False),
            ("occurrencePeriod", "occurrencePeriod", period.Period, False, "occurrence", False),
            ("condition", "condition", fhirreference.FHIRReference, False, None, False),
            ("performer", "performer", fhirreference.FHIRReference, False, None, False),
            ("reasonCode", "reasonCode", codeableconcept.CodeableConcept, True, None, False),
            ("reasonReference", "reasonReference", fhirreference.FHIRReference, True, None, False),
            ("basis", "basis", fhirreference.FHIRReference, True, None, False),
            ("prediction", "prediction", RiskAssessmentPrediction, True, None, False),
            ("mitigation", "mitigation", str, False, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
        ])
        return js


from . import backboneelement

class RiskAssessmentPrediction(backboneelement.BackboneElement):
    """ Outcome predicted.
    
    Describes the expected outcome for the subject.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['outcome'] = """Possible outcome for the subject."""
    _attribute_docstrings['probabilityDecimal'] = """Likelihood of specified outcome."""
    _attribute_docstrings['probabilityRange'] = """Likelihood of specified outcome."""
    _attribute_docstrings['qualitativeRisk'] = """Indicates how likely the outcome is (in the specified timeframe), expressed as a qualitative value (e.g. low, medium, or high)."""
    _attribute_docstrings['relativeRisk'] = """Relative likelihood."""
    _attribute_docstrings['whenPeriod'] = """Timeframe or age range."""
    _attribute_docstrings['whenRange'] = """Timeframe or age range."""
    _attribute_docstrings['rationale'] = """Explanation of prediction."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['qualitativeRisk'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/risk-probability',
        'restricted_to': ['negligible', 'low', 'moderate', 'high', 'certain'],
        'binding_strength': 'example',
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
        
        self.outcome = None
        """ Possible outcome for the subject.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.probabilityDecimal = None
        """ Likelihood of specified outcome.
        Type `float`. """
        
        self.probabilityRange = None
        """ Likelihood of specified outcome.
        Type `Range` (represented as `dict` in JSON). """
        
        self.qualitativeRisk = None
        """ Indicates how likely the outcome is (in the specified timeframe),
        expressed as a qualitative value (e.g. low, medium, or high).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.relativeRisk = None
        """ Relative likelihood.
        Type `float`. """
        
        self.whenPeriod = None
        """ Timeframe or age range.
        Type `Period` (represented as `dict` in JSON). """
        
        self.whenRange = None
        """ Timeframe or age range.
        Type `Range` (represented as `dict` in JSON). """
        
        self.rationale = None
        """ Explanation of prediction.
        Type `str`. """
        
        super(RiskAssessmentPrediction, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(RiskAssessmentPrediction, self).elementProperties()
        js.extend([
            ("outcome", "outcome", codeableconcept.CodeableConcept, False, None, False),
            ("probabilityDecimal", "probabilityDecimal", float, False, "probability", False),
            ("probabilityRange", "probabilityRange", range.Range, False, "probability", False),
            ("qualitativeRisk", "qualitativeRisk", codeableconcept.CodeableConcept, False, None, False),
            ("relativeRisk", "relativeRisk", float, False, None, False),
            ("whenPeriod", "whenPeriod", period.Period, False, "when", False),
            ("whenRange", "whenRange", range.Range, False, "when", False),
            ("rationale", "rationale", str, False, None, False),
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
    from . import range
except ImportError:
    range = sys.modules[__package__ + '.range']
