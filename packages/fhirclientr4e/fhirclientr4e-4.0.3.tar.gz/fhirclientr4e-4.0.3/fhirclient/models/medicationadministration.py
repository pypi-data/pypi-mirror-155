#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/MedicationAdministration) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class MedicationAdministration(domainresource.DomainResource):
    """ Administration of medication to a patient.
    
    Describes the event of a patient consuming or otherwise being administered
    a medication.  This may be as simple as swallowing a tablet or it may be a
    long running infusion.  Related resources tie this event to the authorizing
    prescription, and the specific encounter between patient and health care
    practitioner.
    """
    
    resource_type = "MedicationAdministration"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """External identifier."""
    _attribute_docstrings['instantiates'] = """Instantiates protocol or definition."""
    _attribute_docstrings['partOf'] = """Part of referenced event."""
    _attribute_docstrings['status'] = """Will generally be set to show that the administration has been completed.  For some long running administrations such as infusions, it is possible for an administration to be started but not completed or it may be paused while some other process is under way."""
    _attribute_docstrings['statusReason'] = """Reason administration not performed."""
    _attribute_docstrings['category'] = """Indicates where the medication is expected to be consumed or administered."""
    _attribute_docstrings['medicationCodeableConcept'] = """What was administered."""
    _attribute_docstrings['medicationReference'] = """What was administered."""
    _attribute_docstrings['subject'] = """Who received medication."""
    _attribute_docstrings['context'] = """Encounter or Episode of Care administered as part of."""
    _attribute_docstrings['supportingInformation'] = """Additional information to support administration."""
    _attribute_docstrings['effectiveDateTime'] = """Start and end time of administration."""
    _attribute_docstrings['effectivePeriod'] = """Start and end time of administration."""
    _attribute_docstrings['performer'] = """Who performed the medication administration and what they did."""
    _attribute_docstrings['reasonCode'] = """A code indicating why the medication was given."""
    _attribute_docstrings['reasonReference'] = """Condition or observation that supports why the medication was administered."""
    _attribute_docstrings['request'] = """Request administration performed against."""
    _attribute_docstrings['device'] = """Device used to administer."""
    _attribute_docstrings['note'] = """Information about the administration."""
    _attribute_docstrings['dosage'] = """Details of how medication was taken."""
    _attribute_docstrings['eventHistory'] = """A list of events of interest in the lifecycle."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/medication-admin-status',
        'restricted_to': ['in-progress', 'not-done', 'on-hold', 'completed', 'entered-in-error', 'stopped', 'unknown'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['category'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/medication-admin-category',
        'restricted_to': ['inpatient', 'outpatient', 'community'],
        'binding_strength': 'preferred',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['reasonCode'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/reason-medication-given',
        'restricted_to': ['a', 'b', 'c'],
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
        
        self.identifier = None
        """ External identifier.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.instantiates = None
        """ Instantiates protocol or definition.
        List of `str` items. """
        
        self.partOf = None
        """ Part of referenced event.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.status = None
        """ Will generally be set to show that the administration has been
        completed.  For some long running administrations such as
        infusions, it is possible for an administration to be started but
        not completed or it may be paused while some other process is under
        way.
        Type `str`. """
        
        self.statusReason = None
        """ Reason administration not performed.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.category = None
        """ Indicates where the medication is expected to be consumed or
        administered.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.medicationCodeableConcept = None
        """ What was administered.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.medicationReference = None
        """ What was administered.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.subject = None
        """ Who received medication.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.context = None
        """ Encounter or Episode of Care administered as part of.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.supportingInformation = None
        """ Additional information to support administration.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.effectiveDateTime = None
        """ Start and end time of administration.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.effectivePeriod = None
        """ Start and end time of administration.
        Type `Period` (represented as `dict` in JSON). """
        
        self.performer = None
        """ Who performed the medication administration and what they did.
        List of `MedicationAdministrationPerformer` items (represented as `dict` in JSON). """
        
        self.reasonCode = None
        """ A code indicating why the medication was given.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.reasonReference = None
        """ Condition or observation that supports why the medication was
        administered.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.request = None
        """ Request administration performed against.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.device = None
        """ Device used to administer.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.note = None
        """ Information about the administration.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        self.dosage = None
        """ Details of how medication was taken.
        Type `MedicationAdministrationDosage` (represented as `dict` in JSON). """
        
        self.eventHistory = None
        """ A list of events of interest in the lifecycle.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(MedicationAdministration, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationAdministration, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("instantiates", "instantiates", str, True, None, False),
            ("partOf", "partOf", fhirreference.FHIRReference, True, None, False),
            ("status", "status", str, False, None, True),
            ("statusReason", "statusReason", codeableconcept.CodeableConcept, True, None, False),
            ("category", "category", codeableconcept.CodeableConcept, False, None, False),
            ("medicationCodeableConcept", "medicationCodeableConcept", codeableconcept.CodeableConcept, False, "medication", True),
            ("medicationReference", "medicationReference", fhirreference.FHIRReference, False, "medication", True),
            ("subject", "subject", fhirreference.FHIRReference, False, None, True),
            ("context", "context", fhirreference.FHIRReference, False, None, False),
            ("supportingInformation", "supportingInformation", fhirreference.FHIRReference, True, None, False),
            ("effectiveDateTime", "effectiveDateTime", fhirdate.FHIRDate, False, "effective", True),
            ("effectivePeriod", "effectivePeriod", period.Period, False, "effective", True),
            ("performer", "performer", MedicationAdministrationPerformer, True, None, False),
            ("reasonCode", "reasonCode", codeableconcept.CodeableConcept, True, None, False),
            ("reasonReference", "reasonReference", fhirreference.FHIRReference, True, None, False),
            ("request", "request", fhirreference.FHIRReference, False, None, False),
            ("device", "device", fhirreference.FHIRReference, True, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
            ("dosage", "dosage", MedicationAdministrationDosage, False, None, False),
            ("eventHistory", "eventHistory", fhirreference.FHIRReference, True, None, False),
        ])
        return js


from . import backboneelement

class MedicationAdministrationDosage(backboneelement.BackboneElement):
    """ Details of how medication was taken.
    
    Describes the medication dosage information details e.g. dose, rate, site,
    route, etc.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['text'] = """Free text dosage instructions e.g. SIG."""
    _attribute_docstrings['site'] = """Body site administered to."""
    _attribute_docstrings['route'] = """Path of substance into body."""
    _attribute_docstrings['method'] = """How drug was administered."""
    _attribute_docstrings['dose'] = """Amount of medication per dose."""
    _attribute_docstrings['rateRatio'] = """Dose quantity per unit of time."""
    _attribute_docstrings['rateQuantity'] = """Dose quantity per unit of time."""

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
        
        self.text = None
        """ Free text dosage instructions e.g. SIG.
        Type `str`. """
        
        self.site = None
        """ Body site administered to.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.route = None
        """ Path of substance into body.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.method = None
        """ How drug was administered.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.dose = None
        """ Amount of medication per dose.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.rateRatio = None
        """ Dose quantity per unit of time.
        Type `Ratio` (represented as `dict` in JSON). """
        
        self.rateQuantity = None
        """ Dose quantity per unit of time.
        Type `Quantity` (represented as `dict` in JSON). """
        
        super(MedicationAdministrationDosage, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationAdministrationDosage, self).elementProperties()
        js.extend([
            ("text", "text", str, False, None, False),
            ("site", "site", codeableconcept.CodeableConcept, False, None, False),
            ("route", "route", codeableconcept.CodeableConcept, False, None, False),
            ("method", "method", codeableconcept.CodeableConcept, False, None, False),
            ("dose", "dose", quantity.Quantity, False, None, False),
            ("rateRatio", "rateRatio", ratio.Ratio, False, "rate", False),
            ("rateQuantity", "rateQuantity", quantity.Quantity, False, "rate", False),
        ])
        return js


class MedicationAdministrationPerformer(backboneelement.BackboneElement):
    """ Who performed the medication administration and what they did.
    
    Indicates who or what performed the medication administration and how they
    were involved.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['function'] = """Distinguishes the type of involvement of the performer in the medication administration."""
    _attribute_docstrings['actor'] = """Who performed the medication administration."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['function'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/med-admin-perform-function',
        'restricted_to': ['performer', 'verifier', 'witness'],
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
        
        self.function = None
        """ Distinguishes the type of involvement of the performer in the
        medication administration.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.actor = None
        """ Who performed the medication administration.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(MedicationAdministrationPerformer, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationAdministrationPerformer, self).elementProperties()
        js.extend([
            ("function", "function", codeableconcept.CodeableConcept, False, None, False),
            ("actor", "actor", fhirreference.FHIRReference, False, None, True),
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
    from . import ratio
except ImportError:
    ratio = sys.modules[__package__ + '.ratio']
