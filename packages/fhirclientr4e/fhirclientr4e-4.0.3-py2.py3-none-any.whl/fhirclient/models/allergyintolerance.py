#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/AllergyIntolerance) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class AllergyIntolerance(domainresource.DomainResource):
    """ Allergy or Intolerance (generally: Risk of adverse reaction to a substance).
    
    Risk of harmful or undesirable, physiological response which is unique to
    an individual and associated with exposure to a substance.
    """
    
    resource_type = "AllergyIntolerance"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """External ids for this item."""
    _attribute_docstrings['clinicalStatus'] = """The clinical status of the allergy or intolerance."""
    _attribute_docstrings['verificationStatus'] = """Assertion about certainty associated with the propensity, or potential risk, of a reaction to the identified substance (including pharmaceutical product)."""
    _attribute_docstrings['type'] = """Identification of the underlying physiological mechanism for the reaction risk."""
    _attribute_docstrings['category'] = """Category of the identified substance."""
    _attribute_docstrings['criticality'] = """Estimate of the potential clinical harm, or seriousness, of the reaction to the identified substance."""
    _attribute_docstrings['code'] = """Code that identifies the allergy or intolerance."""
    _attribute_docstrings['patient'] = """Who the sensitivity is for."""
    _attribute_docstrings['encounter'] = """Encounter when the allergy or intolerance was asserted."""
    _attribute_docstrings['onsetDateTime'] = """When allergy or intolerance was identified."""
    _attribute_docstrings['onsetAge'] = """When allergy or intolerance was identified."""
    _attribute_docstrings['onsetPeriod'] = """When allergy or intolerance was identified."""
    _attribute_docstrings['onsetRange'] = """When allergy or intolerance was identified."""
    _attribute_docstrings['onsetString'] = """When allergy or intolerance was identified."""
    _attribute_docstrings['recordedDate'] = """Date first version of the resource instance was recorded."""
    _attribute_docstrings['recorder'] = """Who recorded the sensitivity."""
    _attribute_docstrings['asserter'] = """Source of the information about the allergy."""
    _attribute_docstrings['lastOccurrence'] = """Date(/time) of last known occurrence of a reaction."""
    _attribute_docstrings['note'] = """Additional text not captured in other fields."""
    _attribute_docstrings['reaction'] = """Adverse Reaction Events linked to exposure to substance."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['clinicalStatus'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical',
        'restricted_to': ['active', 'inactive', 'resolved'],
        'binding_strength': 'required',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['verificationStatus'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/allergyintolerance-verification',
        'restricted_to': ['unconfirmed', 'confirmed', 'refuted', 'entered-in-error'],
        'binding_strength': 'required',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['type'] = {
        'url': 'http://hl7.org/fhir/allergy-intolerance-type',
        'restricted_to': ['allergy', 'intolerance'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['category'] = {
        'url': 'http://hl7.org/fhir/allergy-intolerance-category',
        'restricted_to': ['food', 'medication', 'environment', 'biologic'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['criticality'] = {
        'url': 'http://hl7.org/fhir/allergy-intolerance-criticality',
        'restricted_to': ['low', 'high', 'unable-to-assess'],
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
        """ External ids for this item.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.clinicalStatus = None
        """ The clinical status of the allergy or intolerance.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.verificationStatus = None
        """ Assertion about certainty associated with the propensity, or
        potential risk, of a reaction to the identified substance
        (including pharmaceutical product).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.type = None
        """ Identification of the underlying physiological mechanism for the
        reaction risk.
        Type `str`. """
        
        self.category = None
        """ Category of the identified substance.
        List of `str` items. """
        
        self.criticality = None
        """ Estimate of the potential clinical harm, or seriousness, of the
        reaction to the identified substance.
        Type `str`. """
        
        self.code = None
        """ Code that identifies the allergy or intolerance.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.patient = None
        """ Who the sensitivity is for.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Encounter when the allergy or intolerance was asserted.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.onsetDateTime = None
        """ When allergy or intolerance was identified.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.onsetAge = None
        """ When allergy or intolerance was identified.
        Type `Age` (represented as `dict` in JSON). """
        
        self.onsetPeriod = None
        """ When allergy or intolerance was identified.
        Type `Period` (represented as `dict` in JSON). """
        
        self.onsetRange = None
        """ When allergy or intolerance was identified.
        Type `Range` (represented as `dict` in JSON). """
        
        self.onsetString = None
        """ When allergy or intolerance was identified.
        Type `str`. """
        
        self.recordedDate = None
        """ Date first version of the resource instance was recorded.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.recorder = None
        """ Who recorded the sensitivity.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.asserter = None
        """ Source of the information about the allergy.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.lastOccurrence = None
        """ Date(/time) of last known occurrence of a reaction.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.note = None
        """ Additional text not captured in other fields.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        self.reaction = None
        """ Adverse Reaction Events linked to exposure to substance.
        List of `AllergyIntoleranceReaction` items (represented as `dict` in JSON). """
        
        super(AllergyIntolerance, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(AllergyIntolerance, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("clinicalStatus", "clinicalStatus", codeableconcept.CodeableConcept, False, None, False),
            ("verificationStatus", "verificationStatus", codeableconcept.CodeableConcept, False, None, False),
            ("type", "type", str, False, None, False),
            ("category", "category", str, True, None, False),
            ("criticality", "criticality", str, False, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("patient", "patient", fhirreference.FHIRReference, False, None, True),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("onsetDateTime", "onsetDateTime", fhirdate.FHIRDate, False, "onset", False),
            ("onsetAge", "onsetAge", age.Age, False, "onset", False),
            ("onsetPeriod", "onsetPeriod", period.Period, False, "onset", False),
            ("onsetRange", "onsetRange", range.Range, False, "onset", False),
            ("onsetString", "onsetString", str, False, "onset", False),
            ("recordedDate", "recordedDate", fhirdate.FHIRDate, False, None, False),
            ("recorder", "recorder", fhirreference.FHIRReference, False, None, False),
            ("asserter", "asserter", fhirreference.FHIRReference, False, None, False),
            ("lastOccurrence", "lastOccurrence", fhirdate.FHIRDate, False, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
            ("reaction", "reaction", AllergyIntoleranceReaction, True, None, False),
        ])
        return js


from . import backboneelement

class AllergyIntoleranceReaction(backboneelement.BackboneElement):
    """ Adverse Reaction Events linked to exposure to substance.
    
    Details about each adverse reaction event linked to exposure to the
    identified substance.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['substance'] = """Specific substance or pharmaceutical product considered to be responsible for event."""
    _attribute_docstrings['manifestation'] = """Clinical symptoms/signs associated with the Event."""
    _attribute_docstrings['description'] = """Description of the event as a whole."""
    _attribute_docstrings['onset'] = """Date(/time) when manifestations showed."""
    _attribute_docstrings['severity'] = """Clinical assessment of the severity of the reaction event as a whole, potentially considering multiple different manifestations."""
    _attribute_docstrings['exposureRoute'] = """How the subject was exposed to the substance."""
    _attribute_docstrings['note'] = """Text about event not captured in other fields."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['severity'] = {
        'url': 'http://hl7.org/fhir/reaction-event-severity',
        'restricted_to': ['mild', 'moderate', 'severe'],
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
        
        self.substance = None
        """ Specific substance or pharmaceutical product considered to be
        responsible for event.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.manifestation = None
        """ Clinical symptoms/signs associated with the Event.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.description = None
        """ Description of the event as a whole.
        Type `str`. """
        
        self.onset = None
        """ Date(/time) when manifestations showed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.severity = None
        """ Clinical assessment of the severity of the reaction event as a
        whole, potentially considering multiple different manifestations.
        Type `str`. """
        
        self.exposureRoute = None
        """ How the subject was exposed to the substance.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.note = None
        """ Text about event not captured in other fields.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        super(AllergyIntoleranceReaction, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(AllergyIntoleranceReaction, self).elementProperties()
        js.extend([
            ("substance", "substance", codeableconcept.CodeableConcept, False, None, False),
            ("manifestation", "manifestation", codeableconcept.CodeableConcept, True, None, True),
            ("description", "description", str, False, None, False),
            ("onset", "onset", fhirdate.FHIRDate, False, None, False),
            ("severity", "severity", str, False, None, False),
            ("exposureRoute", "exposureRoute", codeableconcept.CodeableConcept, False, None, False),
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
