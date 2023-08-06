#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/PractitionerRole) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class PractitionerRole(domainresource.DomainResource):
    """ Roles/organizations the practitioner is associated with.
    
    A specific set of Roles/Locations/specialties/services that a practitioner
    may perform at an organization for a period of time.
    """
    
    resource_type = "PractitionerRole"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business Identifiers that are specific to a role/location."""
    _attribute_docstrings['active'] = """Whether this practitioner role record is in active use."""
    _attribute_docstrings['period'] = """The period during which the practitioner is authorized to perform in these role(s)."""
    _attribute_docstrings['practitioner'] = """Practitioner that is able to provide the defined services for the organization."""
    _attribute_docstrings['organization'] = """Organization where the roles are available."""
    _attribute_docstrings['code'] = """Roles which this practitioner may perform."""
    _attribute_docstrings['specialty'] = """Specific specialty of the practitioner."""
    _attribute_docstrings['location'] = """The location(s) at which this practitioner provides care."""
    _attribute_docstrings['healthcareService'] = """The list of healthcare services that this worker provides for this role's Organization/Location(s)."""
    _attribute_docstrings['telecom'] = """Contact details that are specific to the role/location/service."""
    _attribute_docstrings['availableTime'] = """Times the Service Site is available."""
    _attribute_docstrings['notAvailable'] = """Not available during this time due to provided reason."""
    _attribute_docstrings['availabilityExceptions'] = """Description of availability exceptions."""
    _attribute_docstrings['endpoint'] = """Technical endpoints providing access to services operated for the practitioner with this role."""

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
        
        self.identifier = None
        """ Business Identifiers that are specific to a role/location.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.active = None
        """ Whether this practitioner role record is in active use.
        Type `bool`. """
        
        self.period = None
        """ The period during which the practitioner is authorized to perform
        in these role(s).
        Type `Period` (represented as `dict` in JSON). """
        
        self.practitioner = None
        """ Practitioner that is able to provide the defined services for the
        organization.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.organization = None
        """ Organization where the roles are available.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.code = None
        """ Roles which this practitioner may perform.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.specialty = None
        """ Specific specialty of the practitioner.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.location = None
        """ The location(s) at which this practitioner provides care.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.healthcareService = None
        """ The list of healthcare services that this worker provides for this
        role's Organization/Location(s).
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.telecom = None
        """ Contact details that are specific to the role/location/service.
        List of `ContactPoint` items (represented as `dict` in JSON). """
        
        self.availableTime = None
        """ Times the Service Site is available.
        List of `PractitionerRoleAvailableTime` items (represented as `dict` in JSON). """
        
        self.notAvailable = None
        """ Not available during this time due to provided reason.
        List of `PractitionerRoleNotAvailable` items (represented as `dict` in JSON). """
        
        self.availabilityExceptions = None
        """ Description of availability exceptions.
        Type `str`. """
        
        self.endpoint = None
        """ Technical endpoints providing access to services operated for the
        practitioner with this role.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(PractitionerRole, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PractitionerRole, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("active", "active", bool, False, None, False),
            ("period", "period", period.Period, False, None, False),
            ("practitioner", "practitioner", fhirreference.FHIRReference, False, None, False),
            ("organization", "organization", fhirreference.FHIRReference, False, None, False),
            ("code", "code", codeableconcept.CodeableConcept, True, None, False),
            ("specialty", "specialty", codeableconcept.CodeableConcept, True, None, False),
            ("location", "location", fhirreference.FHIRReference, True, None, False),
            ("healthcareService", "healthcareService", fhirreference.FHIRReference, True, None, False),
            ("telecom", "telecom", contactpoint.ContactPoint, True, None, False),
            ("availableTime", "availableTime", PractitionerRoleAvailableTime, True, None, False),
            ("notAvailable", "notAvailable", PractitionerRoleNotAvailable, True, None, False),
            ("availabilityExceptions", "availabilityExceptions", str, False, None, False),
            ("endpoint", "endpoint", fhirreference.FHIRReference, True, None, False),
        ])
        return js


from . import backboneelement

class PractitionerRoleAvailableTime(backboneelement.BackboneElement):
    """ Times the Service Site is available.
    
    A collection of times the practitioner is available or performing this role
    at the location and/or healthcareservice.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['daysOfWeek'] = """Indicates which days of the week are available between the start and end Times."""
    _attribute_docstrings['allDay'] = """Always available? e.g. 24 hour service."""
    _attribute_docstrings['availableStartTime'] = """Opening time of day (ignored if allDay = true)."""
    _attribute_docstrings['availableEndTime'] = """Closing time of day (ignored if allDay = true)."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['daysOfWeek'] = {
        'url': 'http://hl7.org/fhir/days-of-week',
        'restricted_to': ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'],
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
        
        self.daysOfWeek = None
        """ Indicates which days of the week are available between the start
        and end Times.
        List of `str` items. """
        
        self.allDay = None
        """ Always available? e.g. 24 hour service.
        Type `bool`. """
        
        self.availableStartTime = None
        """ Opening time of day (ignored if allDay = true).
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.availableEndTime = None
        """ Closing time of day (ignored if allDay = true).
        Type `FHIRDate` (represented as `str` in JSON). """
        
        super(PractitionerRoleAvailableTime, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PractitionerRoleAvailableTime, self).elementProperties()
        js.extend([
            ("daysOfWeek", "daysOfWeek", str, True, None, False),
            ("allDay", "allDay", bool, False, None, False),
            ("availableStartTime", "availableStartTime", fhirdate.FHIRDate, False, None, False),
            ("availableEndTime", "availableEndTime", fhirdate.FHIRDate, False, None, False),
        ])
        return js


class PractitionerRoleNotAvailable(backboneelement.BackboneElement):
    """ Not available during this time due to provided reason.
    
    The practitioner is not available or performing this role during this
    period of time due to the provided reason.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['description'] = """Reason presented to the user explaining why time not available."""
    _attribute_docstrings['during'] = """Service not available from this date."""

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
        
        self.description = None
        """ Reason presented to the user explaining why time not available.
        Type `str`. """
        
        self.during = None
        """ Service not available from this date.
        Type `Period` (represented as `dict` in JSON). """
        
        super(PractitionerRoleNotAvailable, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PractitionerRoleNotAvailable, self).elementProperties()
        js.extend([
            ("description", "description", str, False, None, True),
            ("during", "during", period.Period, False, None, False),
        ])
        return js


import sys
try:
    from . import codeableconcept
except ImportError:
    codeableconcept = sys.modules[__package__ + '.codeableconcept']
try:
    from . import contactpoint
except ImportError:
    contactpoint = sys.modules[__package__ + '.contactpoint']
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
