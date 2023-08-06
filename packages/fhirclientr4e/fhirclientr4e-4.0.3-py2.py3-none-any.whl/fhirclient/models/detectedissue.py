#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/DetectedIssue) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class DetectedIssue(domainresource.DomainResource):
    """ Clinical issue with action.
    
    Indicates an actual or potential clinical issue with or between one or more
    active or proposed clinical actions for a patient; e.g. Drug-drug
    interaction, Ineffective treatment frequency, Procedure-condition conflict,
    etc.
    """
    
    resource_type = "DetectedIssue"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Unique id for the detected issue."""
    _attribute_docstrings['status'] = """Indicates the status of the detected issue."""
    _attribute_docstrings['code'] = """Issue Category, e.g. drug-drug, duplicate therapy, etc.."""
    _attribute_docstrings['severity'] = """Indicates the degree of importance associated with the identified issue based on the potential impact on the patient."""
    _attribute_docstrings['patient'] = """Associated patient."""
    _attribute_docstrings['identifiedDateTime'] = """When identified."""
    _attribute_docstrings['identifiedPeriod'] = """When identified."""
    _attribute_docstrings['author'] = """The provider or device that identified the issue."""
    _attribute_docstrings['implicated'] = """Problem resource."""
    _attribute_docstrings['evidence'] = """Supporting evidence."""
    _attribute_docstrings['detail'] = """Description and context."""
    _attribute_docstrings['reference'] = """Authority for issue."""
    _attribute_docstrings['mitigation'] = """Step taken to address."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/observation-status',
        'restricted_to': ['registered', 'preliminary', 'final', 'amended', 'corrected', 'cancelled', 'entered-in-error', 'unknown'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['severity'] = {
        'url': 'http://hl7.org/fhir/detectedissue-severity',
        'restricted_to': ['high', 'moderate', 'low'],
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
        """ Unique id for the detected issue.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ Indicates the status of the detected issue.
        Type `str`. """
        
        self.code = None
        """ Issue Category, e.g. drug-drug, duplicate therapy, etc.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.severity = None
        """ Indicates the degree of importance associated with the identified
        issue based on the potential impact on the patient.
        Type `str`. """
        
        self.patient = None
        """ Associated patient.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.identifiedDateTime = None
        """ When identified.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.identifiedPeriod = None
        """ When identified.
        Type `Period` (represented as `dict` in JSON). """
        
        self.author = None
        """ The provider or device that identified the issue.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.implicated = None
        """ Problem resource.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.evidence = None
        """ Supporting evidence.
        List of `DetectedIssueEvidence` items (represented as `dict` in JSON). """
        
        self.detail = None
        """ Description and context.
        Type `str`. """
        
        self.reference = None
        """ Authority for issue.
        Type `str`. """
        
        self.mitigation = None
        """ Step taken to address.
        List of `DetectedIssueMitigation` items (represented as `dict` in JSON). """
        
        super(DetectedIssue, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DetectedIssue, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("severity", "severity", str, False, None, False),
            ("patient", "patient", fhirreference.FHIRReference, False, None, False),
            ("identifiedDateTime", "identifiedDateTime", fhirdate.FHIRDate, False, "identified", False),
            ("identifiedPeriod", "identifiedPeriod", period.Period, False, "identified", False),
            ("author", "author", fhirreference.FHIRReference, False, None, False),
            ("implicated", "implicated", fhirreference.FHIRReference, True, None, False),
            ("evidence", "evidence", DetectedIssueEvidence, True, None, False),
            ("detail", "detail", str, False, None, False),
            ("reference", "reference", str, False, None, False),
            ("mitigation", "mitigation", DetectedIssueMitigation, True, None, False),
        ])
        return js


from . import backboneelement

class DetectedIssueEvidence(backboneelement.BackboneElement):
    """ Supporting evidence.
    
    Supporting evidence or manifestations that provide the basis for
    identifying the detected issue such as a GuidanceResponse or MeasureReport.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Manifestation."""
    _attribute_docstrings['detail'] = """Supporting information."""

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
        """ Manifestation.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.detail = None
        """ Supporting information.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(DetectedIssueEvidence, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DetectedIssueEvidence, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, True, None, False),
            ("detail", "detail", fhirreference.FHIRReference, True, None, False),
        ])
        return js


class DetectedIssueMitigation(backboneelement.BackboneElement):
    """ Step taken to address.
    
    Indicates an action that has been taken or is committed to reduce or
    eliminate the likelihood of the risk identified by the detected issue from
    manifesting.  Can also reflect an observation of known mitigating factors
    that may reduce/eliminate the need for any action.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['action'] = """What mitigation?."""
    _attribute_docstrings['date'] = """Date committed."""
    _attribute_docstrings['author'] = """Who is committing?."""

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
        
        self.action = None
        """ What mitigation?.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.date = None
        """ Date committed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.author = None
        """ Who is committing?.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(DetectedIssueMitigation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DetectedIssueMitigation, self).elementProperties()
        js.extend([
            ("action", "action", codeableconcept.CodeableConcept, False, None, True),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("author", "author", fhirreference.FHIRReference, False, None, False),
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
