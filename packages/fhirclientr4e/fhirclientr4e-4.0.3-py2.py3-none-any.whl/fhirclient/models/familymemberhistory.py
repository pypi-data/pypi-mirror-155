#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/FamilyMemberHistory) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class FamilyMemberHistory(domainresource.DomainResource):
    """ Information about patient's relatives, relevant for patient.
    
    Significant health conditions for a person related to the patient relevant
    in the context of care for the patient.
    """
    
    resource_type = "FamilyMemberHistory"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """External Id(s) for this record."""
    _attribute_docstrings['instantiatesCanonical'] = """Instantiates FHIR protocol or definition."""
    _attribute_docstrings['instantiatesUri'] = """Instantiates external protocol or definition."""
    _attribute_docstrings['status'] = """A code specifying the status of the record of the family history of a specific family member."""
    _attribute_docstrings['dataAbsentReason'] = """Describes why the family member's history is not available."""
    _attribute_docstrings['patient'] = """Patient history is about."""
    _attribute_docstrings['date'] = """When history was recorded or last updated."""
    _attribute_docstrings['name'] = """The family member described."""
    _attribute_docstrings['relationship'] = """Relationship to the subject."""
    _attribute_docstrings['sex'] = """The birth sex of the family member."""
    _attribute_docstrings['bornPeriod'] = """(approximate) date of birth."""
    _attribute_docstrings['bornDate'] = """(approximate) date of birth."""
    _attribute_docstrings['bornString'] = """(approximate) date of birth."""
    _attribute_docstrings['ageAge'] = """(approximate) age."""
    _attribute_docstrings['ageRange'] = """(approximate) age."""
    _attribute_docstrings['ageString'] = """(approximate) age."""
    _attribute_docstrings['estimatedAge'] = """Age is estimated?."""
    _attribute_docstrings['deceasedBoolean'] = """Dead? How old/when?."""
    _attribute_docstrings['deceasedAge'] = """Dead? How old/when?."""
    _attribute_docstrings['deceasedRange'] = """Dead? How old/when?."""
    _attribute_docstrings['deceasedDate'] = """Dead? How old/when?."""
    _attribute_docstrings['deceasedString'] = """Dead? How old/when?."""
    _attribute_docstrings['reasonCode'] = """Why was family member history performed?."""
    _attribute_docstrings['reasonReference'] = """Why was family member history performed?."""
    _attribute_docstrings['note'] = """General note about related person."""
    _attribute_docstrings['condition'] = """Condition that the related person had."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/history-status',
        'restricted_to': ['partial', 'completed', 'entered-in-error', 'health-unknown'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['dataAbsentReason'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/history-absent-reason',
        'restricted_to': ['subject-unknown', 'withheld', 'unable-to-obtain', 'deferred'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['sex'] = {
        'url': 'http://hl7.org/fhir/administrative-gender',
        'restricted_to': ['male', 'female', 'other', 'unknown'],
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
        """ External Id(s) for this record.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.instantiatesCanonical = None
        """ Instantiates FHIR protocol or definition.
        List of `str` items. """
        
        self.instantiatesUri = None
        """ Instantiates external protocol or definition.
        List of `str` items. """
        
        self.status = None
        """ A code specifying the status of the record of the family history of
        a specific family member.
        Type `str`. """
        
        self.dataAbsentReason = None
        """ Describes why the family member's history is not available.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.patient = None
        """ Patient history is about.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.date = None
        """ When history was recorded or last updated.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.name = None
        """ The family member described.
        Type `str`. """
        
        self.relationship = None
        """ Relationship to the subject.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.sex = None
        """ The birth sex of the family member.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.bornPeriod = None
        """ (approximate) date of birth.
        Type `Period` (represented as `dict` in JSON). """
        
        self.bornDate = None
        """ (approximate) date of birth.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.bornString = None
        """ (approximate) date of birth.
        Type `str`. """
        
        self.ageAge = None
        """ (approximate) age.
        Type `Age` (represented as `dict` in JSON). """
        
        self.ageRange = None
        """ (approximate) age.
        Type `Range` (represented as `dict` in JSON). """
        
        self.ageString = None
        """ (approximate) age.
        Type `str`. """
        
        self.estimatedAge = None
        """ Age is estimated?.
        Type `bool`. """
        
        self.deceasedBoolean = None
        """ Dead? How old/when?.
        Type `bool`. """
        
        self.deceasedAge = None
        """ Dead? How old/when?.
        Type `Age` (represented as `dict` in JSON). """
        
        self.deceasedRange = None
        """ Dead? How old/when?.
        Type `Range` (represented as `dict` in JSON). """
        
        self.deceasedDate = None
        """ Dead? How old/when?.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.deceasedString = None
        """ Dead? How old/when?.
        Type `str`. """
        
        self.reasonCode = None
        """ Why was family member history performed?.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.reasonReference = None
        """ Why was family member history performed?.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.note = None
        """ General note about related person.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        self.condition = None
        """ Condition that the related person had.
        List of `FamilyMemberHistoryCondition` items (represented as `dict` in JSON). """
        
        super(FamilyMemberHistory, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(FamilyMemberHistory, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("instantiatesCanonical", "instantiatesCanonical", str, True, None, False),
            ("instantiatesUri", "instantiatesUri", str, True, None, False),
            ("status", "status", str, False, None, True),
            ("dataAbsentReason", "dataAbsentReason", codeableconcept.CodeableConcept, False, None, False),
            ("patient", "patient", fhirreference.FHIRReference, False, None, True),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("name", "name", str, False, None, False),
            ("relationship", "relationship", codeableconcept.CodeableConcept, False, None, True),
            ("sex", "sex", codeableconcept.CodeableConcept, False, None, False),
            ("bornPeriod", "bornPeriod", period.Period, False, "born", False),
            ("bornDate", "bornDate", fhirdate.FHIRDate, False, "born", False),
            ("bornString", "bornString", str, False, "born", False),
            ("ageAge", "ageAge", age.Age, False, "age", False),
            ("ageRange", "ageRange", range.Range, False, "age", False),
            ("ageString", "ageString", str, False, "age", False),
            ("estimatedAge", "estimatedAge", bool, False, None, False),
            ("deceasedBoolean", "deceasedBoolean", bool, False, "deceased", False),
            ("deceasedAge", "deceasedAge", age.Age, False, "deceased", False),
            ("deceasedRange", "deceasedRange", range.Range, False, "deceased", False),
            ("deceasedDate", "deceasedDate", fhirdate.FHIRDate, False, "deceased", False),
            ("deceasedString", "deceasedString", str, False, "deceased", False),
            ("reasonCode", "reasonCode", codeableconcept.CodeableConcept, True, None, False),
            ("reasonReference", "reasonReference", fhirreference.FHIRReference, True, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
            ("condition", "condition", FamilyMemberHistoryCondition, True, None, False),
        ])
        return js


from . import backboneelement

class FamilyMemberHistoryCondition(backboneelement.BackboneElement):
    """ Condition that the related person had.
    
    The significant Conditions (or condition) that the family member had. This
    is a repeating section to allow a system to represent more than one
    condition per resource, though there is nothing stopping multiple resources
    - one per condition.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Condition suffered by relation."""
    _attribute_docstrings['outcome'] = """deceased | permanent disability | etc.."""
    _attribute_docstrings['contributedToDeath'] = """Whether the condition contributed to the cause of death."""
    _attribute_docstrings['onsetAge'] = """When condition first manifested."""
    _attribute_docstrings['onsetRange'] = """When condition first manifested."""
    _attribute_docstrings['onsetPeriod'] = """When condition first manifested."""
    _attribute_docstrings['onsetString'] = """When condition first manifested."""
    _attribute_docstrings['note'] = """Extra information about condition."""

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
        """ Condition suffered by relation.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.outcome = None
        """ deceased | permanent disability | etc.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.contributedToDeath = None
        """ Whether the condition contributed to the cause of death.
        Type `bool`. """
        
        self.onsetAge = None
        """ When condition first manifested.
        Type `Age` (represented as `dict` in JSON). """
        
        self.onsetRange = None
        """ When condition first manifested.
        Type `Range` (represented as `dict` in JSON). """
        
        self.onsetPeriod = None
        """ When condition first manifested.
        Type `Period` (represented as `dict` in JSON). """
        
        self.onsetString = None
        """ When condition first manifested.
        Type `str`. """
        
        self.note = None
        """ Extra information about condition.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        super(FamilyMemberHistoryCondition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(FamilyMemberHistoryCondition, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, False, None, True),
            ("outcome", "outcome", codeableconcept.CodeableConcept, False, None, False),
            ("contributedToDeath", "contributedToDeath", bool, False, None, False),
            ("onsetAge", "onsetAge", age.Age, False, "onset", False),
            ("onsetRange", "onsetRange", range.Range, False, "onset", False),
            ("onsetPeriod", "onsetPeriod", period.Period, False, "onset", False),
            ("onsetString", "onsetString", str, False, "onset", False),
            ("note", "note", annotation.Annotation, True, None, False),
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
