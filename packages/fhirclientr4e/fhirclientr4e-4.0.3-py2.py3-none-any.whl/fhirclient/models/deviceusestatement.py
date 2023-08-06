#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/DeviceUseStatement) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class DeviceUseStatement(domainresource.DomainResource):
    """ Record of use of a device.
    
    A record of a device being used by a patient where the record is the result
    of a report from the patient or another clinician.
    """
    
    resource_type = "DeviceUseStatement"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """External identifier for this record."""
    _attribute_docstrings['basedOn'] = """Fulfills plan, proposal or order."""
    _attribute_docstrings['status'] = """A code representing the patient or other source's judgment about the state of the device used that this statement is about.  Generally this will be active or completed."""
    _attribute_docstrings['subject'] = """Patient using device."""
    _attribute_docstrings['derivedFrom'] = """Supporting information."""
    _attribute_docstrings['timingTiming'] = """How often  the device was used."""
    _attribute_docstrings['timingPeriod'] = """How often  the device was used."""
    _attribute_docstrings['timingDateTime'] = """How often  the device was used."""
    _attribute_docstrings['recordedOn'] = """When statement was recorded."""
    _attribute_docstrings['source'] = """Who made the statement."""
    _attribute_docstrings['device'] = """Reference to device used."""
    _attribute_docstrings['reasonCode'] = """Why device was used."""
    _attribute_docstrings['reasonReference'] = """Why was DeviceUseStatement performed?."""
    _attribute_docstrings['bodySite'] = """Target body site."""
    _attribute_docstrings['note'] = """Addition details (comments, instructions)."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/device-statement-status',
        'restricted_to': ['active', 'completed', 'entered-in-error', 'intended', 'stopped', 'on-hold'],
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
        """ External identifier for this record.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.basedOn = None
        """ Fulfills plan, proposal or order.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.status = None
        """ A code representing the patient or other source's judgment about
        the state of the device used that this statement is about.
        Generally this will be active or completed.
        Type `str`. """
        
        self.subject = None
        """ Patient using device.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.derivedFrom = None
        """ Supporting information.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.timingTiming = None
        """ How often  the device was used.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.timingPeriod = None
        """ How often  the device was used.
        Type `Period` (represented as `dict` in JSON). """
        
        self.timingDateTime = None
        """ How often  the device was used.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.recordedOn = None
        """ When statement was recorded.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.source = None
        """ Who made the statement.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.device = None
        """ Reference to device used.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.reasonCode = None
        """ Why device was used.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.reasonReference = None
        """ Why was DeviceUseStatement performed?.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.bodySite = None
        """ Target body site.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.note = None
        """ Addition details (comments, instructions).
        List of `Annotation` items (represented as `dict` in JSON). """
        
        super(DeviceUseStatement, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DeviceUseStatement, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("basedOn", "basedOn", fhirreference.FHIRReference, True, None, False),
            ("status", "status", str, False, None, True),
            ("subject", "subject", fhirreference.FHIRReference, False, None, True),
            ("derivedFrom", "derivedFrom", fhirreference.FHIRReference, True, None, False),
            ("timingTiming", "timingTiming", timing.Timing, False, "timing", False),
            ("timingPeriod", "timingPeriod", period.Period, False, "timing", False),
            ("timingDateTime", "timingDateTime", fhirdate.FHIRDate, False, "timing", False),
            ("recordedOn", "recordedOn", fhirdate.FHIRDate, False, None, False),
            ("source", "source", fhirreference.FHIRReference, False, None, False),
            ("device", "device", fhirreference.FHIRReference, False, None, True),
            ("reasonCode", "reasonCode", codeableconcept.CodeableConcept, True, None, False),
            ("reasonReference", "reasonReference", fhirreference.FHIRReference, True, None, False),
            ("bodySite", "bodySite", codeableconcept.CodeableConcept, False, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
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
    from . import timing
except ImportError:
    timing = sys.modules[__package__ + '.timing']
