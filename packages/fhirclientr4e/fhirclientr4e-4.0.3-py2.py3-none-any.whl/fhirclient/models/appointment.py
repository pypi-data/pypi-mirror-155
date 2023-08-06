#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Appointment) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Appointment(domainresource.DomainResource):
    """ A booking of a healthcare event among patient(s), practitioner(s), related
    person(s) and/or device(s) for a specific date/time. This may result in one
    or more Encounter(s).
    """
    
    resource_type = "Appointment"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """External Ids for this item."""
    _attribute_docstrings['status'] = """The overall status of the Appointment. Each of the participants has their own participation status which indicates their involvement in the process, however this status indicates the shared status."""
    _attribute_docstrings['cancelationReason'] = """The coded reason for the appointment being cancelled."""
    _attribute_docstrings['serviceCategory'] = """A broad categorization of the service that is to be performed during this appointment."""
    _attribute_docstrings['serviceType'] = """The specific service that is to be performed during this appointment."""
    _attribute_docstrings['specialty'] = """The specialty of a practitioner that would be required to perform the service requested in this appointment."""
    _attribute_docstrings['appointmentType'] = """The style of appointment or patient that has been booked in the slot (not service type)."""
    _attribute_docstrings['reasonCode'] = """Coded reason this appointment is scheduled."""
    _attribute_docstrings['reasonReference'] = """Reason the appointment is to take place (resource)."""
    _attribute_docstrings['priority'] = """Used to make informed decisions if needing to re-prioritize."""
    _attribute_docstrings['description'] = """Shown on a subject line in a meeting request, or appointment list."""
    _attribute_docstrings['supportingInformation'] = """Additional information to support the appointment."""
    _attribute_docstrings['start'] = """When appointment is to take place."""
    _attribute_docstrings['end'] = """When appointment is to conclude."""
    _attribute_docstrings['minutesDuration'] = """Can be less than start/end (e.g. estimate)."""
    _attribute_docstrings['slot'] = """The slots that this appointment is filling."""
    _attribute_docstrings['created'] = """The date that this appointment was initially created."""
    _attribute_docstrings['comment'] = """Additional comments."""
    _attribute_docstrings['patientInstruction'] = """Detailed information and instructions for the patient."""
    _attribute_docstrings['basedOn'] = """The service request this appointment is allocated to assess."""
    _attribute_docstrings['participant'] = """Participants involved in appointment."""
    _attribute_docstrings['requestedPeriod'] = """Potential date/time interval(s) requested to allocate the appointment within."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/appointmentstatus',
        'restricted_to': ['proposed', 'pending', 'booked', 'arrived', 'fulfilled', 'cancelled', 'noshow', 'entered-in-error', 'checked-in', 'waitlist'],
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
        """ External Ids for this item.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ The overall status of the Appointment. Each of the participants has
        their own participation status which indicates their involvement in
        the process, however this status indicates the shared status.
        Type `str`. """
        
        self.cancelationReason = None
        """ The coded reason for the appointment being cancelled.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.serviceCategory = None
        """ A broad categorization of the service that is to be performed
        during this appointment.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.serviceType = None
        """ The specific service that is to be performed during this
        appointment.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.specialty = None
        """ The specialty of a practitioner that would be required to perform
        the service requested in this appointment.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.appointmentType = None
        """ The style of appointment or patient that has been booked in the
        slot (not service type).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.reasonCode = None
        """ Coded reason this appointment is scheduled.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.reasonReference = None
        """ Reason the appointment is to take place (resource).
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.priority = None
        """ Used to make informed decisions if needing to re-prioritize.
        Type `int`. """
        
        self.description = None
        """ Shown on a subject line in a meeting request, or appointment list.
        Type `str`. """
        
        self.supportingInformation = None
        """ Additional information to support the appointment.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.start = None
        """ When appointment is to take place.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.end = None
        """ When appointment is to conclude.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.minutesDuration = None
        """ Can be less than start/end (e.g. estimate).
        Type `int`. """
        
        self.slot = None
        """ The slots that this appointment is filling.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.created = None
        """ The date that this appointment was initially created.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.comment = None
        """ Additional comments.
        Type `str`. """
        
        self.patientInstruction = None
        """ Detailed information and instructions for the patient.
        Type `str`. """
        
        self.basedOn = None
        """ The service request this appointment is allocated to assess.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.participant = None
        """ Participants involved in appointment.
        List of `AppointmentParticipant` items (represented as `dict` in JSON). """
        
        self.requestedPeriod = None
        """ Potential date/time interval(s) requested to allocate the
        appointment within.
        List of `Period` items (represented as `dict` in JSON). """
        
        super(Appointment, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Appointment, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("cancelationReason", "cancelationReason", codeableconcept.CodeableConcept, False, None, False),
            ("serviceCategory", "serviceCategory", codeableconcept.CodeableConcept, True, None, False),
            ("serviceType", "serviceType", codeableconcept.CodeableConcept, True, None, False),
            ("specialty", "specialty", codeableconcept.CodeableConcept, True, None, False),
            ("appointmentType", "appointmentType", codeableconcept.CodeableConcept, False, None, False),
            ("reasonCode", "reasonCode", codeableconcept.CodeableConcept, True, None, False),
            ("reasonReference", "reasonReference", fhirreference.FHIRReference, True, None, False),
            ("priority", "priority", int, False, None, False),
            ("description", "description", str, False, None, False),
            ("supportingInformation", "supportingInformation", fhirreference.FHIRReference, True, None, False),
            ("start", "start", fhirdate.FHIRDate, False, None, False),
            ("end", "end", fhirdate.FHIRDate, False, None, False),
            ("minutesDuration", "minutesDuration", int, False, None, False),
            ("slot", "slot", fhirreference.FHIRReference, True, None, False),
            ("created", "created", fhirdate.FHIRDate, False, None, False),
            ("comment", "comment", str, False, None, False),
            ("patientInstruction", "patientInstruction", str, False, None, False),
            ("basedOn", "basedOn", fhirreference.FHIRReference, True, None, False),
            ("participant", "participant", AppointmentParticipant, True, None, True),
            ("requestedPeriod", "requestedPeriod", period.Period, True, None, False),
        ])
        return js


from . import backboneelement

class AppointmentParticipant(backboneelement.BackboneElement):
    """ Participants involved in appointment.
    
    List of participants involved in the appointment.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Role of participant in the appointment."""
    _attribute_docstrings['actor'] = """Person, Location/HealthcareService or Device."""
    _attribute_docstrings['required'] = """Whether this participant is required to be present at the meeting. This covers a use-case where two doctors need to meet to discuss the results for a specific patient, and the patient is not required to be present."""
    _attribute_docstrings['status'] = """Participation status of the actor."""
    _attribute_docstrings['period'] = """Participation period of the actor."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['required'] = {
        'url': 'http://hl7.org/fhir/participantrequired',
        'restricted_to': ['required', 'optional', 'information-only'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/participationstatus',
        'restricted_to': ['accepted', 'declined', 'tentative', 'needs-action'],
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
        """ Role of participant in the appointment.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.actor = None
        """ Person, Location/HealthcareService or Device.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.required = None
        """ Whether this participant is required to be present at the meeting.
        This covers a use-case where two doctors need to meet to discuss
        the results for a specific patient, and the patient is not required
        to be present.
        Type `str`. """
        
        self.status = None
        """ Participation status of the actor.
        Type `str`. """
        
        self.period = None
        """ Participation period of the actor.
        Type `Period` (represented as `dict` in JSON). """
        
        super(AppointmentParticipant, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(AppointmentParticipant, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, True, None, False),
            ("actor", "actor", fhirreference.FHIRReference, False, None, False),
            ("required", "required", str, False, None, False),
            ("status", "status", str, False, None, True),
            ("period", "period", period.Period, False, None, False),
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
try:
    from . import period
except ImportError:
    period = sys.modules[__package__ + '.period']
