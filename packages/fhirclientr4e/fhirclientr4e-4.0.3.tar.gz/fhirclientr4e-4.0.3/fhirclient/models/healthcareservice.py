#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/HealthcareService) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class HealthcareService(domainresource.DomainResource):
    """ The details of a healthcare service available at a location.
    """
    
    resource_type = "HealthcareService"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """External identifiers for this item."""
    _attribute_docstrings['active'] = """Whether this HealthcareService record is in active use."""
    _attribute_docstrings['providedBy'] = """Organization that provides this service."""
    _attribute_docstrings['category'] = """Broad category of service being performed or delivered."""
    _attribute_docstrings['type'] = """Type of service that may be delivered or performed."""
    _attribute_docstrings['specialty'] = """Specialties handled by the HealthcareService."""
    _attribute_docstrings['location'] = """Location(s) where service may be provided."""
    _attribute_docstrings['name'] = """Description of service as presented to a consumer while searching."""
    _attribute_docstrings['comment'] = """Additional description and/or any specific issues not covered elsewhere."""
    _attribute_docstrings['extraDetails'] = """Extra details about the service that can't be placed in the other fields."""
    _attribute_docstrings['photo'] = """Facilitates quick identification of the service."""
    _attribute_docstrings['telecom'] = """Contacts related to the healthcare service."""
    _attribute_docstrings['coverageArea'] = """Location(s) service is intended for/available to."""
    _attribute_docstrings['serviceProvisionCode'] = """The code(s) that detail the conditions under which the healthcare service is available/offered."""
    _attribute_docstrings['eligibility'] = """Specific eligibility requirements required to use the service."""
    _attribute_docstrings['program'] = """Programs that this service is applicable to."""
    _attribute_docstrings['characteristic'] = """Collection of characteristics (attributes)."""
    _attribute_docstrings['communication'] = """The language that this service is offered in."""
    _attribute_docstrings['referralMethod'] = """Ways that the service accepts referrals, if this is not provided then it is implied that no referral is required."""
    _attribute_docstrings['appointmentRequired'] = """If an appointment is required for access to this service."""
    _attribute_docstrings['availableTime'] = """Times the Service Site is available."""
    _attribute_docstrings['notAvailable'] = """Not available during this time due to provided reason."""
    _attribute_docstrings['availabilityExceptions'] = """Description of availability exceptions."""
    _attribute_docstrings['endpoint'] = """Technical endpoints providing access to electronic services operated for the healthcare service."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['serviceProvisionCode'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/service-provision-conditions',
        'restricted_to': ['free', 'disc', 'cost'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['referralMethod'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/service-referral-method',
        'restricted_to': ['fax', 'phone', 'elec', 'semail', 'mail'],
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
        """ External identifiers for this item.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.active = None
        """ Whether this HealthcareService record is in active use.
        Type `bool`. """
        
        self.providedBy = None
        """ Organization that provides this service.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.category = None
        """ Broad category of service being performed or delivered.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.type = None
        """ Type of service that may be delivered or performed.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.specialty = None
        """ Specialties handled by the HealthcareService.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.location = None
        """ Location(s) where service may be provided.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.name = None
        """ Description of service as presented to a consumer while searching.
        Type `str`. """
        
        self.comment = None
        """ Additional description and/or any specific issues not covered
        elsewhere.
        Type `str`. """
        
        self.extraDetails = None
        """ Extra details about the service that can't be placed in the other
        fields.
        Type `str`. """
        
        self.photo = None
        """ Facilitates quick identification of the service.
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.telecom = None
        """ Contacts related to the healthcare service.
        List of `ContactPoint` items (represented as `dict` in JSON). """
        
        self.coverageArea = None
        """ Location(s) service is intended for/available to.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.serviceProvisionCode = None
        """ The code(s) that detail the conditions under which the healthcare
        service is available/offered.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.eligibility = None
        """ Specific eligibility requirements required to use the service.
        List of `HealthcareServiceEligibility` items (represented as `dict` in JSON). """
        
        self.program = None
        """ Programs that this service is applicable to.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.characteristic = None
        """ Collection of characteristics (attributes).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.communication = None
        """ The language that this service is offered in.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.referralMethod = None
        """ Ways that the service accepts referrals, if this is not provided
        then it is implied that no referral is required.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.appointmentRequired = None
        """ If an appointment is required for access to this service.
        Type `bool`. """
        
        self.availableTime = None
        """ Times the Service Site is available.
        List of `HealthcareServiceAvailableTime` items (represented as `dict` in JSON). """
        
        self.notAvailable = None
        """ Not available during this time due to provided reason.
        List of `HealthcareServiceNotAvailable` items (represented as `dict` in JSON). """
        
        self.availabilityExceptions = None
        """ Description of availability exceptions.
        Type `str`. """
        
        self.endpoint = None
        """ Technical endpoints providing access to electronic services
        operated for the healthcare service.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(HealthcareService, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(HealthcareService, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("active", "active", bool, False, None, False),
            ("providedBy", "providedBy", fhirreference.FHIRReference, False, None, False),
            ("category", "category", codeableconcept.CodeableConcept, True, None, False),
            ("type", "type", codeableconcept.CodeableConcept, True, None, False),
            ("specialty", "specialty", codeableconcept.CodeableConcept, True, None, False),
            ("location", "location", fhirreference.FHIRReference, True, None, False),
            ("name", "name", str, False, None, False),
            ("comment", "comment", str, False, None, False),
            ("extraDetails", "extraDetails", str, False, None, False),
            ("photo", "photo", attachment.Attachment, False, None, False),
            ("telecom", "telecom", contactpoint.ContactPoint, True, None, False),
            ("coverageArea", "coverageArea", fhirreference.FHIRReference, True, None, False),
            ("serviceProvisionCode", "serviceProvisionCode", codeableconcept.CodeableConcept, True, None, False),
            ("eligibility", "eligibility", HealthcareServiceEligibility, True, None, False),
            ("program", "program", codeableconcept.CodeableConcept, True, None, False),
            ("characteristic", "characteristic", codeableconcept.CodeableConcept, True, None, False),
            ("communication", "communication", codeableconcept.CodeableConcept, True, None, False),
            ("referralMethod", "referralMethod", codeableconcept.CodeableConcept, True, None, False),
            ("appointmentRequired", "appointmentRequired", bool, False, None, False),
            ("availableTime", "availableTime", HealthcareServiceAvailableTime, True, None, False),
            ("notAvailable", "notAvailable", HealthcareServiceNotAvailable, True, None, False),
            ("availabilityExceptions", "availabilityExceptions", str, False, None, False),
            ("endpoint", "endpoint", fhirreference.FHIRReference, True, None, False),
        ])
        return js


from . import backboneelement

class HealthcareServiceAvailableTime(backboneelement.BackboneElement):
    """ Times the Service Site is available.
    
    A collection of times that the Service Site is available.
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
        
        super(HealthcareServiceAvailableTime, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(HealthcareServiceAvailableTime, self).elementProperties()
        js.extend([
            ("daysOfWeek", "daysOfWeek", str, True, None, False),
            ("allDay", "allDay", bool, False, None, False),
            ("availableStartTime", "availableStartTime", fhirdate.FHIRDate, False, None, False),
            ("availableEndTime", "availableEndTime", fhirdate.FHIRDate, False, None, False),
        ])
        return js


class HealthcareServiceEligibility(backboneelement.BackboneElement):
    """ Specific eligibility requirements required to use the service.
    
    Does this service have specific eligibility requirements that need to be
    met in order to use the service?
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Coded value for the eligibility."""
    _attribute_docstrings['comment'] = """Describes the eligibility conditions for the service."""

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
        """ Coded value for the eligibility.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.comment = None
        """ Describes the eligibility conditions for the service.
        Type `str`. """
        
        super(HealthcareServiceEligibility, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(HealthcareServiceEligibility, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("comment", "comment", str, False, None, False),
        ])
        return js


class HealthcareServiceNotAvailable(backboneelement.BackboneElement):
    """ Not available during this time due to provided reason.
    
    The HealthcareService is not available during this period of time due to
    the provided reason.
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
        
        super(HealthcareServiceNotAvailable, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(HealthcareServiceNotAvailable, self).elementProperties()
        js.extend([
            ("description", "description", str, False, None, True),
            ("during", "during", period.Period, False, None, False),
        ])
        return js


import sys
try:
    from . import attachment
except ImportError:
    attachment = sys.modules[__package__ + '.attachment']
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
