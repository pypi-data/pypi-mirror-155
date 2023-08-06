#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/EnrollmentResponse) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class EnrollmentResponse(domainresource.DomainResource):
    """ EnrollmentResponse resource.
    
    This resource provides enrollment and plan details from the processing of
    an EnrollmentRequest resource.
    """
    
    resource_type = "EnrollmentResponse"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business Identifier."""
    _attribute_docstrings['status'] = """The status of the resource instance."""
    _attribute_docstrings['request'] = """Claim reference."""
    _attribute_docstrings['outcome'] = """Processing status: error, complete."""
    _attribute_docstrings['disposition'] = """Disposition Message."""
    _attribute_docstrings['created'] = """Creation date."""
    _attribute_docstrings['organization'] = """Insurer."""
    _attribute_docstrings['requestProvider'] = """Responsible practitioner."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/fm-status',
        'restricted_to': ['active', 'cancelled', 'draft', 'entered-in-error'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['outcome'] = {
        'url': 'http://hl7.org/fhir/remittance-outcome',
        'restricted_to': ['queued', 'complete', 'error', 'partial'],
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
        """ Business Identifier.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ The status of the resource instance.
        Type `str`. """
        
        self.request = None
        """ Claim reference.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.outcome = None
        """ Processing status: error, complete.
        Type `str`. """
        
        self.disposition = None
        """ Disposition Message.
        Type `str`. """
        
        self.created = None
        """ Creation date.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.organization = None
        """ Insurer.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.requestProvider = None
        """ Responsible practitioner.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(EnrollmentResponse, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(EnrollmentResponse, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, False),
            ("request", "request", fhirreference.FHIRReference, False, None, False),
            ("outcome", "outcome", str, False, None, False),
            ("disposition", "disposition", str, False, None, False),
            ("created", "created", fhirdate.FHIRDate, False, None, False),
            ("organization", "organization", fhirreference.FHIRReference, False, None, False),
            ("requestProvider", "requestProvider", fhirreference.FHIRReference, False, None, False),
        ])
        return js


import sys
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
