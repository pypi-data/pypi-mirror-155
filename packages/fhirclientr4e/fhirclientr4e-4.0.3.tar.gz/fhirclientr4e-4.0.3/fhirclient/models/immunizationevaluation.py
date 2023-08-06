#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/ImmunizationEvaluation) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class ImmunizationEvaluation(domainresource.DomainResource):
    """ Immunization evaluation information.
    
    Describes a comparison of an immunization event against published
    recommendations to determine if the administration is "valid" in relation
    to those  recommendations.
    """
    
    resource_type = "ImmunizationEvaluation"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business identifier."""
    _attribute_docstrings['status'] = """Indicates the current status of the evaluation of the vaccination administration event."""
    _attribute_docstrings['patient'] = """Who this evaluation is for."""
    _attribute_docstrings['date'] = """Date evaluation was performed."""
    _attribute_docstrings['authority'] = """Who is responsible for publishing the recommendations."""
    _attribute_docstrings['targetDisease'] = """Evaluation target disease."""
    _attribute_docstrings['immunizationEvent'] = """Immunization being evaluated."""
    _attribute_docstrings['doseStatus'] = """Indicates if the dose is valid or not valid with respect to the published recommendations."""
    _attribute_docstrings['doseStatusReason'] = """Provides an explanation as to why the vaccine administration event is valid or not relative to the published recommendations."""
    _attribute_docstrings['description'] = """Evaluation notes."""
    _attribute_docstrings['series'] = """Name of vaccine series."""
    _attribute_docstrings['doseNumberPositiveInt'] = """Dose number within series."""
    _attribute_docstrings['doseNumberString'] = """Dose number within series."""
    _attribute_docstrings['seriesDosesPositiveInt'] = """Recommended number of doses for immunity."""
    _attribute_docstrings['seriesDosesString'] = """Recommended number of doses for immunity."""

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
    _attribute_enums['doseStatus'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/immunization-evaluation-dose-status',
        'restricted_to': ['valid', 'notvalid'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['doseStatusReason'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/immunization-evaluation-dose-status-reason',
        'restricted_to': ['advstorage', 'coldchbrk', 'explot', 'outsidesched', 'prodrecall'],
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
        """ Business identifier.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ Indicates the current status of the evaluation of the vaccination
        administration event.
        Type `str`. """
        
        self.patient = None
        """ Who this evaluation is for.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.date = None
        """ Date evaluation was performed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.authority = None
        """ Who is responsible for publishing the recommendations.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.targetDisease = None
        """ Evaluation target disease.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.immunizationEvent = None
        """ Immunization being evaluated.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.doseStatus = None
        """ Indicates if the dose is valid or not valid with respect to the
        published recommendations.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.doseStatusReason = None
        """ Provides an explanation as to why the vaccine administration event
        is valid or not relative to the published recommendations.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.description = None
        """ Evaluation notes.
        Type `str`. """
        
        self.series = None
        """ Name of vaccine series.
        Type `str`. """
        
        self.doseNumberPositiveInt = None
        """ Dose number within series.
        Type `int`. """
        
        self.doseNumberString = None
        """ Dose number within series.
        Type `str`. """
        
        self.seriesDosesPositiveInt = None
        """ Recommended number of doses for immunity.
        Type `int`. """
        
        self.seriesDosesString = None
        """ Recommended number of doses for immunity.
        Type `str`. """
        
        super(ImmunizationEvaluation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ImmunizationEvaluation, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("patient", "patient", fhirreference.FHIRReference, False, None, True),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("authority", "authority", fhirreference.FHIRReference, False, None, False),
            ("targetDisease", "targetDisease", codeableconcept.CodeableConcept, False, None, True),
            ("immunizationEvent", "immunizationEvent", fhirreference.FHIRReference, False, None, True),
            ("doseStatus", "doseStatus", codeableconcept.CodeableConcept, False, None, True),
            ("doseStatusReason", "doseStatusReason", codeableconcept.CodeableConcept, True, None, False),
            ("description", "description", str, False, None, False),
            ("series", "series", str, False, None, False),
            ("doseNumberPositiveInt", "doseNumberPositiveInt", int, False, "doseNumber", False),
            ("doseNumberString", "doseNumberString", str, False, "doseNumber", False),
            ("seriesDosesPositiveInt", "seriesDosesPositiveInt", int, False, "seriesDoses", False),
            ("seriesDosesString", "seriesDosesString", str, False, "seriesDoses", False),
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
