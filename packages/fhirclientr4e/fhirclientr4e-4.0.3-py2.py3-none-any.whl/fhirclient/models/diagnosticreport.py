#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/DiagnosticReport) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class DiagnosticReport(domainresource.DomainResource):
    """ A Diagnostic report - a combination of request information, atomic results,
    images, interpretation, as well as formatted reports.
    
    The findings and interpretation of diagnostic  tests performed on patients,
    groups of patients, devices, and locations, and/or specimens derived from
    these. The report includes clinical context such as requesting and provider
    information, and some mix of atomic results, images, textual and coded
    interpretations, and formatted representation of diagnostic reports.
    """
    
    resource_type = "DiagnosticReport"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business identifier for report."""
    _attribute_docstrings['basedOn'] = """What was requested."""
    _attribute_docstrings['status'] = """The status of the diagnostic report."""
    _attribute_docstrings['category'] = """Service category."""
    _attribute_docstrings['code'] = """Name/Code for this diagnostic report."""
    _attribute_docstrings['subject'] = """The subject of the report - usually, but not always, the patient."""
    _attribute_docstrings['encounter'] = """Health care event when test ordered."""
    _attribute_docstrings['effectiveDateTime'] = """Clinically relevant time/time-period for report."""
    _attribute_docstrings['effectivePeriod'] = """Clinically relevant time/time-period for report."""
    _attribute_docstrings['issued'] = """DateTime this version was made."""
    _attribute_docstrings['performer'] = """Responsible Diagnostic Service."""
    _attribute_docstrings['resultsInterpreter'] = """Primary result interpreter."""
    _attribute_docstrings['specimen'] = """Specimens this report is based on."""
    _attribute_docstrings['result'] = """Observations."""
    _attribute_docstrings['imagingStudy'] = """Reference to full details of imaging associated with the diagnostic report."""
    _attribute_docstrings['media'] = """Key images associated with this report."""
    _attribute_docstrings['conclusion'] = """Clinical conclusion (interpretation) of test results."""
    _attribute_docstrings['conclusionCode'] = """Codes for the clinical conclusion of test results."""
    _attribute_docstrings['presentedForm'] = """Entire report as issued."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/diagnostic-report-status',
        'restricted_to': ['registered', 'partial', 'preliminary', 'final', 'amended', 'corrected', 'appended', 'cancelled', 'entered-in-error', 'unknown'],
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
        """ Business identifier for report.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.basedOn = None
        """ What was requested.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.status = None
        """ The status of the diagnostic report.
        Type `str`. """
        
        self.category = None
        """ Service category.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.code = None
        """ Name/Code for this diagnostic report.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subject = None
        """ The subject of the report - usually, but not always, the patient.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Health care event when test ordered.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.effectiveDateTime = None
        """ Clinically relevant time/time-period for report.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.effectivePeriod = None
        """ Clinically relevant time/time-period for report.
        Type `Period` (represented as `dict` in JSON). """
        
        self.issued = None
        """ DateTime this version was made.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.performer = None
        """ Responsible Diagnostic Service.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.resultsInterpreter = None
        """ Primary result interpreter.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.specimen = None
        """ Specimens this report is based on.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.result = None
        """ Observations.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.imagingStudy = None
        """ Reference to full details of imaging associated with the diagnostic
        report.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.media = None
        """ Key images associated with this report.
        List of `DiagnosticReportMedia` items (represented as `dict` in JSON). """
        
        self.conclusion = None
        """ Clinical conclusion (interpretation) of test results.
        Type `str`. """
        
        self.conclusionCode = None
        """ Codes for the clinical conclusion of test results.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.presentedForm = None
        """ Entire report as issued.
        List of `Attachment` items (represented as `dict` in JSON). """
        
        super(DiagnosticReport, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DiagnosticReport, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("basedOn", "basedOn", fhirreference.FHIRReference, True, None, False),
            ("status", "status", str, False, None, True),
            ("category", "category", codeableconcept.CodeableConcept, True, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, True),
            ("subject", "subject", fhirreference.FHIRReference, False, None, False),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("effectiveDateTime", "effectiveDateTime", fhirdate.FHIRDate, False, "effective", False),
            ("effectivePeriod", "effectivePeriod", period.Period, False, "effective", False),
            ("issued", "issued", fhirdate.FHIRDate, False, None, False),
            ("performer", "performer", fhirreference.FHIRReference, True, None, False),
            ("resultsInterpreter", "resultsInterpreter", fhirreference.FHIRReference, True, None, False),
            ("specimen", "specimen", fhirreference.FHIRReference, True, None, False),
            ("result", "result", fhirreference.FHIRReference, True, None, False),
            ("imagingStudy", "imagingStudy", fhirreference.FHIRReference, True, None, False),
            ("media", "media", DiagnosticReportMedia, True, None, False),
            ("conclusion", "conclusion", str, False, None, False),
            ("conclusionCode", "conclusionCode", codeableconcept.CodeableConcept, True, None, False),
            ("presentedForm", "presentedForm", attachment.Attachment, True, None, False),
        ])
        return js


from . import backboneelement

class DiagnosticReportMedia(backboneelement.BackboneElement):
    """ Key images associated with this report.
    
    A list of key images associated with this report. The images are generally
    created during the diagnostic process, and may be directly of the patient,
    or of treated specimens (i.e. slides of interest).
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['comment'] = """Comment about the image (e.g. explanation)."""
    _attribute_docstrings['link'] = """Reference to the image source."""

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
        
        self.comment = None
        """ Comment about the image (e.g. explanation).
        Type `str`. """
        
        self.link = None
        """ Reference to the image source.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(DiagnosticReportMedia, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DiagnosticReportMedia, self).elementProperties()
        js.extend([
            ("comment", "comment", str, False, None, False),
            ("link", "link", fhirreference.FHIRReference, False, None, True),
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
