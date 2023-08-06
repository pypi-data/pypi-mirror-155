#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Encounter) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Encounter(domainresource.DomainResource):
    """ An interaction during which services are provided to the patient.
    
    An interaction between a patient and healthcare provider(s) for the purpose
    of providing healthcare service(s) or assessing the health status of a
    patient.
    """
    
    resource_type = "Encounter"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Identifier(s) by which this encounter is known."""
    _attribute_docstrings['status'] = """None"""
    _attribute_docstrings['statusHistory'] = """List of past encounter statuses."""
    _attribute_docstrings['class_fhir'] = """Classification of patient encounter."""
    _attribute_docstrings['classHistory'] = """List of past encounter classes."""
    _attribute_docstrings['type'] = """Specific type of encounter (e.g. e-mail consultation, surgical day-care, skilled nursing, rehabilitation)."""
    _attribute_docstrings['serviceType'] = """Specific type of service."""
    _attribute_docstrings['priority'] = """Indicates the urgency of the encounter."""
    _attribute_docstrings['subject'] = """The patient or group present at the encounter."""
    _attribute_docstrings['episodeOfCare'] = """Episode(s) of care that this encounter should be recorded against."""
    _attribute_docstrings['basedOn'] = """The ServiceRequest that initiated this encounter."""
    _attribute_docstrings['participant'] = """List of participants involved in the encounter."""
    _attribute_docstrings['appointment'] = """The appointment that scheduled this encounter."""
    _attribute_docstrings['period'] = """The start and end time of the encounter."""
    _attribute_docstrings['length'] = """Quantity of time the encounter lasted (less time absent)."""
    _attribute_docstrings['reasonCode'] = """Coded reason the encounter takes place."""
    _attribute_docstrings['reasonReference'] = """Reason the encounter takes place (reference)."""
    _attribute_docstrings['diagnosis'] = """The list of diagnosis relevant to this encounter."""
    _attribute_docstrings['account'] = """The set of accounts that may be used for billing for this Encounter."""
    _attribute_docstrings['hospitalization'] = """Details about the admission to a healthcare service."""
    _attribute_docstrings['location'] = """List of locations where the patient has been."""
    _attribute_docstrings['serviceProvider'] = """The organization (facility) responsible for this encounter."""
    _attribute_docstrings['partOf'] = """Another Encounter this encounter is part of."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/encounter-status',
        'restricted_to': ['planned', 'arrived', 'triaged', 'in-progress', 'onleave', 'finished', 'cancelled', 'entered-in-error', 'unknown'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/encounter-type',
        'restricted_to': ['ADMS', 'BD/BM-clin', 'CCS60', 'OKI'],
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
        """ Identifier(s) by which this encounter is known.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ None.
        Type `str`. """
        
        self.statusHistory = None
        """ List of past encounter statuses.
        List of `EncounterStatusHistory` items (represented as `dict` in JSON). """
        
        self.class_fhir = None
        """ Classification of patient encounter.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.classHistory = None
        """ List of past encounter classes.
        List of `EncounterClassHistory` items (represented as `dict` in JSON). """
        
        self.type = None
        """ Specific type of encounter (e.g. e-mail consultation, surgical day-
        care, skilled nursing, rehabilitation).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.serviceType = None
        """ Specific type of service.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.priority = None
        """ Indicates the urgency of the encounter.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subject = None
        """ The patient or group present at the encounter.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.episodeOfCare = None
        """ Episode(s) of care that this encounter should be recorded against.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.basedOn = None
        """ The ServiceRequest that initiated this encounter.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.participant = None
        """ List of participants involved in the encounter.
        List of `EncounterParticipant` items (represented as `dict` in JSON). """
        
        self.appointment = None
        """ The appointment that scheduled this encounter.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.period = None
        """ The start and end time of the encounter.
        Type `Period` (represented as `dict` in JSON). """
        
        self.length = None
        """ Quantity of time the encounter lasted (less time absent).
        Type `Duration` (represented as `dict` in JSON). """
        
        self.reasonCode = None
        """ Coded reason the encounter takes place.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.reasonReference = None
        """ Reason the encounter takes place (reference).
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.diagnosis = None
        """ The list of diagnosis relevant to this encounter.
        List of `EncounterDiagnosis` items (represented as `dict` in JSON). """
        
        self.account = None
        """ The set of accounts that may be used for billing for this Encounter.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.hospitalization = None
        """ Details about the admission to a healthcare service.
        Type `EncounterHospitalization` (represented as `dict` in JSON). """
        
        self.location = None
        """ List of locations where the patient has been.
        List of `EncounterLocation` items (represented as `dict` in JSON). """
        
        self.serviceProvider = None
        """ The organization (facility) responsible for this encounter.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.partOf = None
        """ Another Encounter this encounter is part of.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(Encounter, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Encounter, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("statusHistory", "statusHistory", EncounterStatusHistory, True, None, False),
            ("class_fhir", "class", coding.Coding, False, None, True),
            ("classHistory", "classHistory", EncounterClassHistory, True, None, False),
            ("type", "type", codeableconcept.CodeableConcept, True, None, False),
            ("serviceType", "serviceType", codeableconcept.CodeableConcept, False, None, False),
            ("priority", "priority", codeableconcept.CodeableConcept, False, None, False),
            ("subject", "subject", fhirreference.FHIRReference, False, None, False),
            ("episodeOfCare", "episodeOfCare", fhirreference.FHIRReference, True, None, False),
            ("basedOn", "basedOn", fhirreference.FHIRReference, True, None, False),
            ("participant", "participant", EncounterParticipant, True, None, False),
            ("appointment", "appointment", fhirreference.FHIRReference, True, None, False),
            ("period", "period", period.Period, False, None, False),
            ("length", "length", duration.Duration, False, None, False),
            ("reasonCode", "reasonCode", codeableconcept.CodeableConcept, True, None, False),
            ("reasonReference", "reasonReference", fhirreference.FHIRReference, True, None, False),
            ("diagnosis", "diagnosis", EncounterDiagnosis, True, None, False),
            ("account", "account", fhirreference.FHIRReference, True, None, False),
            ("hospitalization", "hospitalization", EncounterHospitalization, False, None, False),
            ("location", "location", EncounterLocation, True, None, False),
            ("serviceProvider", "serviceProvider", fhirreference.FHIRReference, False, None, False),
            ("partOf", "partOf", fhirreference.FHIRReference, False, None, False),
        ])
        return js


from . import backboneelement

class EncounterClassHistory(backboneelement.BackboneElement):
    """ List of past encounter classes.
    
    The class history permits the tracking of the encounters transitions
    without needing to go  through the resource history.  This would be used
    for a case where an admission starts of as an emergency encounter, then
    transitions into an inpatient scenario. Doing this and not restarting a new
    encounter ensures that any lab/diagnostic results can more easily follow
    the patient and not require re-processing and not get lost or cancelled
    during a kind of discharge from emergency to inpatient.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['class_fhir'] = """inpatient | outpatient | ambulatory | emergency +."""
    _attribute_docstrings['period'] = """The time that the episode was in the specified class."""

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
        
        self.class_fhir = None
        """ inpatient | outpatient | ambulatory | emergency +.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.period = None
        """ The time that the episode was in the specified class.
        Type `Period` (represented as `dict` in JSON). """
        
        super(EncounterClassHistory, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(EncounterClassHistory, self).elementProperties()
        js.extend([
            ("class_fhir", "class", coding.Coding, False, None, True),
            ("period", "period", period.Period, False, None, True),
        ])
        return js


class EncounterDiagnosis(backboneelement.BackboneElement):
    """ The list of diagnosis relevant to this encounter.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['condition'] = """The diagnosis or procedure relevant to the encounter."""
    _attribute_docstrings['use'] = """None"""
    _attribute_docstrings['rank'] = """Ranking of the diagnosis (for each role type)."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['use'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/diagnosis-role',
        'restricted_to': ['AD', 'DD', 'CC', 'CM', 'pre-op', 'post-op', 'billing'],
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
        
        self.condition = None
        """ The diagnosis or procedure relevant to the encounter.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.use = None
        """ None.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.rank = None
        """ Ranking of the diagnosis (for each role type).
        Type `int`. """
        
        super(EncounterDiagnosis, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(EncounterDiagnosis, self).elementProperties()
        js.extend([
            ("condition", "condition", fhirreference.FHIRReference, False, None, True),
            ("use", "use", codeableconcept.CodeableConcept, False, None, False),
            ("rank", "rank", int, False, None, False),
        ])
        return js


class EncounterHospitalization(backboneelement.BackboneElement):
    """ Details about the admission to a healthcare service.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['preAdmissionIdentifier'] = """Pre-admission identifier."""
    _attribute_docstrings['origin'] = """The location/organization from which the patient came before admission."""
    _attribute_docstrings['admitSource'] = """None"""
    _attribute_docstrings['reAdmission'] = """The type of hospital re-admission that has occurred (if any). If the value is absent, then this is not identified as a readmission."""
    _attribute_docstrings['dietPreference'] = """None"""
    _attribute_docstrings['specialCourtesy'] = """Special courtesies (VIP, board member)."""
    _attribute_docstrings['specialArrangement'] = """Any special requests that have been made for this hospitalization encounter, such as the provision of specific equipment or other things."""
    _attribute_docstrings['destination'] = """Location/organization to which the patient is discharged."""
    _attribute_docstrings['dischargeDisposition'] = """None"""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['admitSource'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/admit-source',
        'restricted_to': ['hosp-trans', 'emd', 'outp', 'born', 'gp', 'mp', 'nursing', 'psych', 'rehab', 'other'],
        'binding_strength': 'preferred',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['dietPreference'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/diet',
        'restricted_to': ['vegetarian', 'dairy-free', 'nut-free', 'gluten-free', 'vegan', 'halal', 'kosher'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['specialArrangement'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/encounter-special-arrangements',
        'restricted_to': ['wheel', 'add-bed', 'int', 'att', 'dog'],
        'binding_strength': 'preferred',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['dischargeDisposition'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/discharge-disposition',
        'restricted_to': ['home', 'alt-home', 'other-hcf', 'hosp', 'long', 'aadvice', 'exp', 'psy', 'rehab', 'snf', 'oth'],
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
        
        self.preAdmissionIdentifier = None
        """ Pre-admission identifier.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.origin = None
        """ The location/organization from which the patient came before
        admission.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.admitSource = None
        """ None.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.reAdmission = None
        """ The type of hospital re-admission that has occurred (if any). If
        the value is absent, then this is not identified as a readmission.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.dietPreference = None
        """ None.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.specialCourtesy = None
        """ Special courtesies (VIP, board member).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.specialArrangement = None
        """ Any special requests that have been made for this hospitalization
        encounter, such as the provision of specific equipment or other
        things.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.destination = None
        """ Location/organization to which the patient is discharged.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.dischargeDisposition = None
        """ None.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(EncounterHospitalization, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(EncounterHospitalization, self).elementProperties()
        js.extend([
            ("preAdmissionIdentifier", "preAdmissionIdentifier", identifier.Identifier, False, None, False),
            ("origin", "origin", fhirreference.FHIRReference, False, None, False),
            ("admitSource", "admitSource", codeableconcept.CodeableConcept, False, None, False),
            ("reAdmission", "reAdmission", codeableconcept.CodeableConcept, False, None, False),
            ("dietPreference", "dietPreference", codeableconcept.CodeableConcept, True, None, False),
            ("specialCourtesy", "specialCourtesy", codeableconcept.CodeableConcept, True, None, False),
            ("specialArrangement", "specialArrangement", codeableconcept.CodeableConcept, True, None, False),
            ("destination", "destination", fhirreference.FHIRReference, False, None, False),
            ("dischargeDisposition", "dischargeDisposition", codeableconcept.CodeableConcept, False, None, False),
        ])
        return js


class EncounterLocation(backboneelement.BackboneElement):
    """ List of locations where the patient has been.
    
    List of locations where  the patient has been during this encounter.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['location'] = """Location the encounter takes place."""
    _attribute_docstrings['status'] = """The status of the participants' presence at the specified location during the period specified. If the participant is no longer at the location, then the period will have an end date/time."""
    _attribute_docstrings['physicalType'] = """This will be used to specify the required levels (bed/ward/room/etc.) desired to be recorded to simplify either messaging or query."""
    _attribute_docstrings['period'] = """Time period during which the patient was present at the location."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/encounter-location-status',
        'restricted_to': ['planned', 'active', 'reserved', 'completed'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['physicalType'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/location-physical-type',
        'restricted_to': ['si', 'bu', 'wi', 'wa', 'lvl', 'co', 'ro', 'bd', 've', 'ho', 'ca', 'rd', 'area', 'jdn'],
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
        
        self.location = None
        """ Location the encounter takes place.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.status = None
        """ The status of the participants' presence at the specified location
        during the period specified. If the participant is no longer at the
        location, then the period will have an end date/time.
        Type `str`. """
        
        self.physicalType = None
        """ This will be used to specify the required levels
        (bed/ward/room/etc.) desired to be recorded to simplify either
        messaging or query.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.period = None
        """ Time period during which the patient was present at the location.
        Type `Period` (represented as `dict` in JSON). """
        
        super(EncounterLocation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(EncounterLocation, self).elementProperties()
        js.extend([
            ("location", "location", fhirreference.FHIRReference, False, None, True),
            ("status", "status", str, False, None, False),
            ("physicalType", "physicalType", codeableconcept.CodeableConcept, False, None, False),
            ("period", "period", period.Period, False, None, False),
        ])
        return js


class EncounterParticipant(backboneelement.BackboneElement):
    """ List of participants involved in the encounter.
    
    The list of people responsible for providing the service.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Role of participant in encounter."""
    _attribute_docstrings['period'] = """Period of time during the encounter that the participant participated."""
    _attribute_docstrings['individual'] = """Persons involved in the encounter other than the patient."""

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
        
        self.type = None
        """ Role of participant in encounter.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.period = None
        """ Period of time during the encounter that the participant
        participated.
        Type `Period` (represented as `dict` in JSON). """
        
        self.individual = None
        """ Persons involved in the encounter other than the patient.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(EncounterParticipant, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(EncounterParticipant, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, True, None, False),
            ("period", "period", period.Period, False, None, False),
            ("individual", "individual", fhirreference.FHIRReference, False, None, False),
        ])
        return js


class EncounterStatusHistory(backboneelement.BackboneElement):
    """ List of past encounter statuses.
    
    The status history permits the encounter resource to contain the status
    history without needing to read through the historical versions of the
    resource, or even have the server store them.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['status'] = """None"""
    _attribute_docstrings['period'] = """The time that the episode was in the specified status."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/encounter-status',
        'restricted_to': ['planned', 'arrived', 'triaged', 'in-progress', 'onleave', 'finished', 'cancelled', 'entered-in-error', 'unknown'],
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
        
        self.status = None
        """ None.
        Type `str`. """
        
        self.period = None
        """ The time that the episode was in the specified status.
        Type `Period` (represented as `dict` in JSON). """
        
        super(EncounterStatusHistory, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(EncounterStatusHistory, self).elementProperties()
        js.extend([
            ("status", "status", str, False, None, True),
            ("period", "period", period.Period, False, None, True),
        ])
        return js


import sys
try:
    from . import codeableconcept
except ImportError:
    codeableconcept = sys.modules[__package__ + '.codeableconcept']
try:
    from . import coding
except ImportError:
    coding = sys.modules[__package__ + '.coding']
try:
    from . import duration
except ImportError:
    duration = sys.modules[__package__ + '.duration']
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
