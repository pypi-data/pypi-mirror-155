#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/DeviceMetric) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class DeviceMetric(domainresource.DomainResource):
    """ Measurement, calculation or setting capability of a medical device.
    
    Describes a measurement, calculation or setting capability of a medical
    device.
    """
    
    resource_type = "DeviceMetric"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Instance identifier."""
    _attribute_docstrings['type'] = """Identity of metric, for example Heart Rate or PEEP Setting."""
    _attribute_docstrings['unit'] = """Unit of Measure for the Metric."""
    _attribute_docstrings['source'] = """Describes the link to the source Device."""
    _attribute_docstrings['parent'] = """Describes the link to the parent Device."""
    _attribute_docstrings['operationalStatus'] = """Indicates current operational state of the device. For example: On, Off, Standby, etc."""
    _attribute_docstrings['color'] = """Describes the color representation for the metric. This is often used to aid clinicians to track and identify parameter types by color. In practice, consider a Patient Monitor that has ECG/HR and Pleth for example; the parameters are displayed in different characteristic colors, such as HR-blue, BP-green, and PR and SpO2- magenta."""
    _attribute_docstrings['category'] = """Indicates the category of the observation generation process. A DeviceMetric can be for example a setting, measurement, or calculation."""
    _attribute_docstrings['measurementPeriod'] = """Describes the measurement repetition time."""
    _attribute_docstrings['calibration'] = """Describes the calibrations that have been performed or that are required to be performed."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['operationalStatus'] = {
        'url': 'http://hl7.org/fhir/metric-operational-status',
        'restricted_to': ['on', 'off', 'standby', 'entered-in-error'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['color'] = {
        'url': 'http://hl7.org/fhir/metric-color',
        'restricted_to': ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['category'] = {
        'url': 'http://hl7.org/fhir/metric-category',
        'restricted_to': ['measurement', 'setting', 'calculation', 'unspecified'],
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
        """ Instance identifier.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.type = None
        """ Identity of metric, for example Heart Rate or PEEP Setting.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.unit = None
        """ Unit of Measure for the Metric.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.source = None
        """ Describes the link to the source Device.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.parent = None
        """ Describes the link to the parent Device.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.operationalStatus = None
        """ Indicates current operational state of the device. For example: On,
        Off, Standby, etc.
        Type `str`. """
        
        self.color = None
        """ Describes the color representation for the metric. This is often
        used to aid clinicians to track and identify parameter types by
        color. In practice, consider a Patient Monitor that has ECG/HR and
        Pleth for example; the parameters are displayed in different
        characteristic colors, such as HR-blue, BP-green, and PR and SpO2-
        magenta.
        Type `str`. """
        
        self.category = None
        """ Indicates the category of the observation generation process. A
        DeviceMetric can be for example a setting, measurement, or
        calculation.
        Type `str`. """
        
        self.measurementPeriod = None
        """ Describes the measurement repetition time.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.calibration = None
        """ Describes the calibrations that have been performed or that are
        required to be performed.
        List of `DeviceMetricCalibration` items (represented as `dict` in JSON). """
        
        super(DeviceMetric, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DeviceMetric, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("unit", "unit", codeableconcept.CodeableConcept, False, None, False),
            ("source", "source", fhirreference.FHIRReference, False, None, False),
            ("parent", "parent", fhirreference.FHIRReference, False, None, False),
            ("operationalStatus", "operationalStatus", str, False, None, False),
            ("color", "color", str, False, None, False),
            ("category", "category", str, False, None, True),
            ("measurementPeriod", "measurementPeriod", timing.Timing, False, None, False),
            ("calibration", "calibration", DeviceMetricCalibration, True, None, False),
        ])
        return js


from . import backboneelement

class DeviceMetricCalibration(backboneelement.BackboneElement):
    """ Describes the calibrations that have been performed or that are required to
    be performed.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Describes the type of the calibration method."""
    _attribute_docstrings['state'] = """Describes the state of the calibration."""
    _attribute_docstrings['time'] = """Describes the time last calibration has been performed."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://hl7.org/fhir/metric-calibration-type',
        'restricted_to': ['unspecified', 'offset', 'gain', 'two-point'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['state'] = {
        'url': 'http://hl7.org/fhir/metric-calibration-state',
        'restricted_to': ['not-calibrated', 'calibration-required', 'calibrated', 'unspecified'],
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
        """ Describes the type of the calibration method.
        Type `str`. """
        
        self.state = None
        """ Describes the state of the calibration.
        Type `str`. """
        
        self.time = None
        """ Describes the time last calibration has been performed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        super(DeviceMetricCalibration, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DeviceMetricCalibration, self).elementProperties()
        js.extend([
            ("type", "type", str, False, None, False),
            ("state", "state", str, False, None, False),
            ("time", "time", fhirdate.FHIRDate, False, None, False),
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
    from . import timing
except ImportError:
    timing = sys.modules[__package__ + '.timing']
