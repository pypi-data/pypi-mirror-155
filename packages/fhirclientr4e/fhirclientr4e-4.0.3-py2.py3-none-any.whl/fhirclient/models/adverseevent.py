#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/AdverseEvent) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class AdverseEvent(domainresource.DomainResource):
    """ Medical care, research study or other healthcare event causing physical
    injury.
    
    Actual or  potential/avoided event causing unintended physical injury
    resulting from or contributed to by medical care, a research study or other
    healthcare setting factors that requires additional monitoring, treatment,
    or hospitalization, or that results in death.
    """
    
    resource_type = "AdverseEvent"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business identifier for the event."""
    _attribute_docstrings['actuality'] = """Whether the event actually happened, or just had the potential to. Note that this is independent of whether anyone was affected or harmed or how severely."""
    _attribute_docstrings['category'] = """The overall type of event, intended for search and filtering purposes."""
    _attribute_docstrings['event'] = """Type of the event itself in relation to the subject."""
    _attribute_docstrings['subject'] = """Subject impacted by event."""
    _attribute_docstrings['encounter'] = """Encounter created as part of."""
    _attribute_docstrings['date'] = """When the event occurred."""
    _attribute_docstrings['detected'] = """When the event was detected."""
    _attribute_docstrings['recordedDate'] = """When the event was recorded."""
    _attribute_docstrings['resultingCondition'] = """Effect on the subject due to this event."""
    _attribute_docstrings['location'] = """Location where adverse event occurred."""
    _attribute_docstrings['seriousness'] = """Assessment whether this event was of real importance."""
    _attribute_docstrings['severity'] = """Describes the severity of the adverse event, in relation to the subject. Contrast to AdverseEvent.seriousness - a severe rash might not be serious, but a mild heart problem is."""
    _attribute_docstrings['outcome'] = """Describes the type of outcome from the adverse event."""
    _attribute_docstrings['recorder'] = """Who recorded the adverse event."""
    _attribute_docstrings['contributor'] = """Who  was involved in the adverse event or the potential adverse event."""
    _attribute_docstrings['suspectEntity'] = """The suspected agent causing the adverse event."""
    _attribute_docstrings['subjectMedicalHistory'] = """AdverseEvent.subjectMedicalHistory."""
    _attribute_docstrings['referenceDocument'] = """AdverseEvent.referenceDocument."""
    _attribute_docstrings['study'] = """AdverseEvent.study."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['actuality'] = {
        'url': 'http://hl7.org/fhir/adverse-event-actuality',
        'restricted_to': ['actual', 'potential'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['category'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/adverse-event-category',
        'restricted_to': ['product-problem', 'product-quality', 'product-use-error', 'wrong-dose', 'incorrect-prescribing-information', 'wrong-technique', 'wrong-route-of-administration', 'wrong-rate', 'wrong-duration', 'wrong-time', 'expired-drug', 'medical-device-use-error', 'problem-different-manufacturer', 'unsafe-physical-environment'],
        'binding_strength': 'extensible',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['seriousness'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/adverse-event-seriousness',
        'restricted_to': ['Non-serious', 'Serious', 'SeriousResultsInDeath', 'SeriousIsLifeThreatening', 'SeriousResultsInHospitalization', 'SeriousResultsInDisability', 'SeriousIsBirthDefect', 'SeriousRequiresPreventImpairment'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['severity'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/adverse-event-severity',
        'restricted_to': ['mild', 'moderate', 'severe'],
        'binding_strength': 'required',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['outcome'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/adverse-event-outcome',
        'restricted_to': ['resolved', 'recovering', 'ongoing', 'resolvedWithSequelae', 'fatal', 'unknown'],
        'binding_strength': 'required',
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
        """ Business identifier for the event.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.actuality = None
        """ Whether the event actually happened, or just had the potential to.
        Note that this is independent of whether anyone was affected or
        harmed or how severely.
        Type `str`. """
        
        self.category = None
        """ The overall type of event, intended for search and filtering
        purposes.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.event = None
        """ Type of the event itself in relation to the subject.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subject = None
        """ Subject impacted by event.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Encounter created as part of.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.date = None
        """ When the event occurred.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.detected = None
        """ When the event was detected.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.recordedDate = None
        """ When the event was recorded.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.resultingCondition = None
        """ Effect on the subject due to this event.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.location = None
        """ Location where adverse event occurred.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.seriousness = None
        """ Assessment whether this event was of real importance.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.severity = None
        """ Describes the severity of the adverse event, in relation to the
        subject. Contrast to AdverseEvent.seriousness - a severe rash might
        not be serious, but a mild heart problem is.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.outcome = None
        """ Describes the type of outcome from the adverse event.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.recorder = None
        """ Who recorded the adverse event.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.contributor = None
        """ Who  was involved in the adverse event or the potential adverse
        event.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.suspectEntity = None
        """ The suspected agent causing the adverse event.
        List of `AdverseEventSuspectEntity` items (represented as `dict` in JSON). """
        
        self.subjectMedicalHistory = None
        """ AdverseEvent.subjectMedicalHistory.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.referenceDocument = None
        """ AdverseEvent.referenceDocument.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.study = None
        """ AdverseEvent.study.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(AdverseEvent, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(AdverseEvent, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, False, None, False),
            ("actuality", "actuality", str, False, None, True),
            ("category", "category", codeableconcept.CodeableConcept, True, None, False),
            ("event", "event", codeableconcept.CodeableConcept, False, None, False),
            ("subject", "subject", fhirreference.FHIRReference, False, None, True),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("detected", "detected", fhirdate.FHIRDate, False, None, False),
            ("recordedDate", "recordedDate", fhirdate.FHIRDate, False, None, False),
            ("resultingCondition", "resultingCondition", fhirreference.FHIRReference, True, None, False),
            ("location", "location", fhirreference.FHIRReference, False, None, False),
            ("seriousness", "seriousness", codeableconcept.CodeableConcept, False, None, False),
            ("severity", "severity", codeableconcept.CodeableConcept, False, None, False),
            ("outcome", "outcome", codeableconcept.CodeableConcept, False, None, False),
            ("recorder", "recorder", fhirreference.FHIRReference, False, None, False),
            ("contributor", "contributor", fhirreference.FHIRReference, True, None, False),
            ("suspectEntity", "suspectEntity", AdverseEventSuspectEntity, True, None, False),
            ("subjectMedicalHistory", "subjectMedicalHistory", fhirreference.FHIRReference, True, None, False),
            ("referenceDocument", "referenceDocument", fhirreference.FHIRReference, True, None, False),
            ("study", "study", fhirreference.FHIRReference, True, None, False),
        ])
        return js


from . import backboneelement

class AdverseEventSuspectEntity(backboneelement.BackboneElement):
    """ The suspected agent causing the adverse event.
    
    Describes the entity that is suspected to have caused the adverse event.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['instance'] = """Refers to the specific entity that caused the adverse event."""
    _attribute_docstrings['causality'] = """Information on the possible cause of the event."""

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
        
        self.instance = None
        """ Refers to the specific entity that caused the adverse event.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.causality = None
        """ Information on the possible cause of the event.
        List of `AdverseEventSuspectEntityCausality` items (represented as `dict` in JSON). """
        
        super(AdverseEventSuspectEntity, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(AdverseEventSuspectEntity, self).elementProperties()
        js.extend([
            ("instance", "instance", fhirreference.FHIRReference, False, None, True),
            ("causality", "causality", AdverseEventSuspectEntityCausality, True, None, False),
        ])
        return js


class AdverseEventSuspectEntityCausality(backboneelement.BackboneElement):
    """ Information on the possible cause of the event.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['assessment'] = """None"""
    _attribute_docstrings['productRelatedness'] = """AdverseEvent.suspectEntity.causalityProductRelatedness."""
    _attribute_docstrings['author'] = """AdverseEvent.suspectEntity.causalityAuthor."""
    _attribute_docstrings['method'] = """None"""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['assessment'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/adverse-event-causality-assess',
        'restricted_to': ['Certain', 'Probably-Likely', 'Possible', 'Unlikely', 'Conditional-Classified', 'Unassessable-Unclassifiable'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['method'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/adverse-event-causality-method',
        'restricted_to': ['ProbabilityScale', 'Bayesian', 'Checklist'],
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
        
        self.assessment = None
        """ None.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.productRelatedness = None
        """ AdverseEvent.suspectEntity.causalityProductRelatedness.
        Type `str`. """
        
        self.author = None
        """ AdverseEvent.suspectEntity.causalityAuthor.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.method = None
        """ None.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(AdverseEventSuspectEntityCausality, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(AdverseEventSuspectEntityCausality, self).elementProperties()
        js.extend([
            ("assessment", "assessment", codeableconcept.CodeableConcept, False, None, False),
            ("productRelatedness", "productRelatedness", str, False, None, False),
            ("author", "author", fhirreference.FHIRReference, False, None, False),
            ("method", "method", codeableconcept.CodeableConcept, False, None, False),
        ])
        return js


import sys
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
