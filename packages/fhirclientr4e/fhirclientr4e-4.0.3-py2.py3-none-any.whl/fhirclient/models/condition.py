#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Condition) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Condition(domainresource.DomainResource):
    """ Detailed information about conditions, problems or diagnoses.
    
    A clinical condition, problem, diagnosis, or other event, situation, issue,
    or clinical concept that has risen to a level of concern.
    """
    
    resource_type = "Condition"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """External Ids for this condition."""
    _attribute_docstrings['clinicalStatus'] = """The clinical status of the condition."""
    _attribute_docstrings['verificationStatus'] = """The verification status to support the clinical status of the condition."""
    _attribute_docstrings['category'] = """A category assigned to the condition."""
    _attribute_docstrings['severity'] = """Subjective severity of condition."""
    _attribute_docstrings['code'] = """Identification of the condition, problem or diagnosis."""
    _attribute_docstrings['bodySite'] = """Anatomical location, if relevant."""
    _attribute_docstrings['subject'] = """Who has the condition?."""
    _attribute_docstrings['encounter'] = """Encounter created as part of."""
    _attribute_docstrings['onsetDateTime'] = """Estimated or actual date,  date-time, or age."""
    _attribute_docstrings['onsetAge'] = """Estimated or actual date,  date-time, or age."""
    _attribute_docstrings['onsetPeriod'] = """Estimated or actual date,  date-time, or age."""
    _attribute_docstrings['onsetRange'] = """Estimated or actual date,  date-time, or age."""
    _attribute_docstrings['onsetString'] = """Estimated or actual date,  date-time, or age."""
    _attribute_docstrings['abatementDateTime'] = """When in resolution/remission."""
    _attribute_docstrings['abatementAge'] = """When in resolution/remission."""
    _attribute_docstrings['abatementPeriod'] = """When in resolution/remission."""
    _attribute_docstrings['abatementRange'] = """When in resolution/remission."""
    _attribute_docstrings['abatementString'] = """When in resolution/remission."""
    _attribute_docstrings['recordedDate'] = """Date record was first recorded."""
    _attribute_docstrings['recorder'] = """Who recorded the condition."""
    _attribute_docstrings['asserter'] = """Person who asserts this condition."""
    _attribute_docstrings['stage'] = """Stage/grade, usually assessed formally."""
    _attribute_docstrings['evidence'] = """Supporting evidence."""
    _attribute_docstrings['note'] = """Additional information about the Condition."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['clinicalStatus'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/condition-clinical',
        'restricted_to': ['active', 'recurrence', 'relapse', 'inactive', 'remission', 'resolved'],
        'binding_strength': 'required',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['verificationStatus'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/condition-ver-status',
        'restricted_to': ['unconfirmed', 'provisional', 'differential', 'confirmed', 'refuted', 'entered-in-error'],
        'binding_strength': 'required',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['category'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/condition-category',
        'restricted_to': ['problem-list-item', 'encounter-diagnosis'],
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
        """ External Ids for this condition.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.clinicalStatus = None
        """ The clinical status of the condition.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.verificationStatus = None
        """ The verification status to support the clinical status of the
        condition.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.category = None
        """ A category assigned to the condition.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.severity = None
        """ Subjective severity of condition.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.code = None
        """ Identification of the condition, problem or diagnosis.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.bodySite = None
        """ Anatomical location, if relevant.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.subject = None
        """ Who has the condition?.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Encounter created as part of.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.onsetDateTime = None
        """ Estimated or actual date,  date-time, or age.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.onsetAge = None
        """ Estimated or actual date,  date-time, or age.
        Type `Age` (represented as `dict` in JSON). """
        
        self.onsetPeriod = None
        """ Estimated or actual date,  date-time, or age.
        Type `Period` (represented as `dict` in JSON). """
        
        self.onsetRange = None
        """ Estimated or actual date,  date-time, or age.
        Type `Range` (represented as `dict` in JSON). """
        
        self.onsetString = None
        """ Estimated or actual date,  date-time, or age.
        Type `str`. """
        
        self.abatementDateTime = None
        """ When in resolution/remission.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.abatementAge = None
        """ When in resolution/remission.
        Type `Age` (represented as `dict` in JSON). """
        
        self.abatementPeriod = None
        """ When in resolution/remission.
        Type `Period` (represented as `dict` in JSON). """
        
        self.abatementRange = None
        """ When in resolution/remission.
        Type `Range` (represented as `dict` in JSON). """
        
        self.abatementString = None
        """ When in resolution/remission.
        Type `str`. """
        
        self.recordedDate = None
        """ Date record was first recorded.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.recorder = None
        """ Who recorded the condition.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.asserter = None
        """ Person who asserts this condition.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.stage = None
        """ Stage/grade, usually assessed formally.
        List of `ConditionStage` items (represented as `dict` in JSON). """
        
        self.evidence = None
        """ Supporting evidence.
        List of `ConditionEvidence` items (represented as `dict` in JSON). """
        
        self.note = None
        """ Additional information about the Condition.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        super(Condition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Condition, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("clinicalStatus", "clinicalStatus", codeableconcept.CodeableConcept, False, None, False),
            ("verificationStatus", "verificationStatus", codeableconcept.CodeableConcept, False, None, False),
            ("category", "category", codeableconcept.CodeableConcept, True, None, False),
            ("severity", "severity", codeableconcept.CodeableConcept, False, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("bodySite", "bodySite", codeableconcept.CodeableConcept, True, None, False),
            ("subject", "subject", fhirreference.FHIRReference, False, None, True),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("onsetDateTime", "onsetDateTime", fhirdate.FHIRDate, False, "onset", False),
            ("onsetAge", "onsetAge", age.Age, False, "onset", False),
            ("onsetPeriod", "onsetPeriod", period.Period, False, "onset", False),
            ("onsetRange", "onsetRange", range.Range, False, "onset", False),
            ("onsetString", "onsetString", str, False, "onset", False),
            ("abatementDateTime", "abatementDateTime", fhirdate.FHIRDate, False, "abatement", False),
            ("abatementAge", "abatementAge", age.Age, False, "abatement", False),
            ("abatementPeriod", "abatementPeriod", period.Period, False, "abatement", False),
            ("abatementRange", "abatementRange", range.Range, False, "abatement", False),
            ("abatementString", "abatementString", str, False, "abatement", False),
            ("recordedDate", "recordedDate", fhirdate.FHIRDate, False, None, False),
            ("recorder", "recorder", fhirreference.FHIRReference, False, None, False),
            ("asserter", "asserter", fhirreference.FHIRReference, False, None, False),
            ("stage", "stage", ConditionStage, True, None, False),
            ("evidence", "evidence", ConditionEvidence, True, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
        ])
        return js


from . import backboneelement

class ConditionEvidence(backboneelement.BackboneElement):
    """ Supporting evidence.
    
    Supporting evidence / manifestations that are the basis of the Condition's
    verification status, such as evidence that confirmed or refuted the
    condition.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Manifestation/symptom."""
    _attribute_docstrings['detail'] = """Supporting information found elsewhere."""

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
        """ Manifestation/symptom.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.detail = None
        """ Supporting information found elsewhere.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(ConditionEvidence, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ConditionEvidence, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, True, None, False),
            ("detail", "detail", fhirreference.FHIRReference, True, None, False),
        ])
        return js


class ConditionStage(backboneelement.BackboneElement):
    """ Stage/grade, usually assessed formally.
    
    Clinical stage or grade of a condition. May include formal severity
    assessments.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['summary'] = """Simple summary (disease specific)."""
    _attribute_docstrings['assessment'] = """Formal record of assessment."""
    _attribute_docstrings['type'] = """Kind of staging."""

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
        
        self.summary = None
        """ Simple summary (disease specific).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.assessment = None
        """ Formal record of assessment.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.type = None
        """ Kind of staging.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(ConditionStage, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ConditionStage, self).elementProperties()
        js.extend([
            ("summary", "summary", codeableconcept.CodeableConcept, False, None, False),
            ("assessment", "assessment", fhirreference.FHIRReference, True, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
        ])
        return js


import sys
try:
    from . import age
except ImportError:
    age = sys.modules[__package__ + '.age']
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
