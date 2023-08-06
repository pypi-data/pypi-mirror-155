#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/AppointmentResponse) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class AppointmentResponse(domainresource.DomainResource):
    """ A reply to an appointment request for a patient and/or practitioner(s),
    such as a confirmation or rejection.
    """
    
    resource_type = "AppointmentResponse"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """External Ids for this item."""
    _attribute_docstrings['appointment'] = """Appointment this response relates to."""
    _attribute_docstrings['start'] = """Time from appointment, or requested new start time."""
    _attribute_docstrings['end'] = """Time from appointment, or requested new end time."""
    _attribute_docstrings['participantType'] = """Role of participant in the appointment."""
    _attribute_docstrings['actor'] = """Person, Location, HealthcareService, or Device."""
    _attribute_docstrings['participantStatus'] = """Participation status of the participant. When the status is declined or tentative if the start/end times are different to the appointment, then these times should be interpreted as a requested time change. When the status is accepted, the times can either be the time of the appointment (as a confirmation of the time) or can be empty."""
    _attribute_docstrings['comment'] = """Additional comments."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['participantStatus'] = {
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
        
        self.identifier = None
        """ External Ids for this item.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.appointment = None
        """ Appointment this response relates to.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.start = None
        """ Time from appointment, or requested new start time.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.end = None
        """ Time from appointment, or requested new end time.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.participantType = None
        """ Role of participant in the appointment.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.actor = None
        """ Person, Location, HealthcareService, or Device.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.participantStatus = None
        """ Participation status of the participant. When the status is
        declined or tentative if the start/end times are different to the
        appointment, then these times should be interpreted as a requested
        time change. When the status is accepted, the times can either be
        the time of the appointment (as a confirmation of the time) or can
        be empty.
        Type `str`. """
        
        self.comment = None
        """ Additional comments.
        Type `str`. """
        
        super(AppointmentResponse, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(AppointmentResponse, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("appointment", "appointment", fhirreference.FHIRReference, False, None, True),
            ("start", "start", fhirdate.FHIRDate, False, None, False),
            ("end", "end", fhirdate.FHIRDate, False, None, False),
            ("participantType", "participantType", codeableconcept.CodeableConcept, True, None, False),
            ("actor", "actor", fhirreference.FHIRReference, False, None, False),
            ("participantStatus", "participantStatus", str, False, None, True),
            ("comment", "comment", str, False, None, False),
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
