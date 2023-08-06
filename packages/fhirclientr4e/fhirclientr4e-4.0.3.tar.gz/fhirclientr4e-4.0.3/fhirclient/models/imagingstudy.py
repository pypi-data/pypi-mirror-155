#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/ImagingStudy) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class ImagingStudy(domainresource.DomainResource):
    """ A set of images produced in single study (one or more series of references
    images).
    
    Representation of the content produced in a DICOM imaging study. A study
    comprises a set of series, each of which includes a set of Service-Object
    Pair Instances (SOP Instances - images or other data) acquired or produced
    in a common context.  A series is of only one modality (e.g. X-ray, CT, MR,
    ultrasound), but a study may have multiple series of different modalities.
    """
    
    resource_type = "ImagingStudy"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Identifiers for the whole study."""
    _attribute_docstrings['status'] = """The current state of the ImagingStudy."""
    _attribute_docstrings['modality'] = """All series modality if actual acquisition modalities."""
    _attribute_docstrings['subject'] = """Who or what is the subject of the study."""
    _attribute_docstrings['encounter'] = """Encounter with which this imaging study is associated."""
    _attribute_docstrings['started'] = """When the study was started."""
    _attribute_docstrings['basedOn'] = """Request fulfilled."""
    _attribute_docstrings['referrer'] = """Referring physician."""
    _attribute_docstrings['interpreter'] = """Who interpreted images."""
    _attribute_docstrings['endpoint'] = """Study access endpoint."""
    _attribute_docstrings['numberOfSeries'] = """Number of Study Related Series."""
    _attribute_docstrings['numberOfInstances'] = """Number of Study Related Instances."""
    _attribute_docstrings['procedureReference'] = """The performed Procedure reference."""
    _attribute_docstrings['procedureCode'] = """The performed procedure code."""
    _attribute_docstrings['location'] = """Where ImagingStudy occurred."""
    _attribute_docstrings['reasonCode'] = """Why the study was requested."""
    _attribute_docstrings['reasonReference'] = """Why was study performed."""
    _attribute_docstrings['note'] = """User-defined comments."""
    _attribute_docstrings['description'] = """Institution-generated description."""
    _attribute_docstrings['series'] = """Each study has one or more series of instances."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/imagingstudy-status',
        'restricted_to': ['registered', 'available', 'cancelled', 'entered-in-error', 'unknown'],
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
        """ Identifiers for the whole study.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ The current state of the ImagingStudy.
        Type `str`. """
        
        self.modality = None
        """ All series modality if actual acquisition modalities.
        List of `Coding` items (represented as `dict` in JSON). """
        
        self.subject = None
        """ Who or what is the subject of the study.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Encounter with which this imaging study is associated.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.started = None
        """ When the study was started.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.basedOn = None
        """ Request fulfilled.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.referrer = None
        """ Referring physician.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.interpreter = None
        """ Who interpreted images.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.endpoint = None
        """ Study access endpoint.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.numberOfSeries = None
        """ Number of Study Related Series.
        Type `int`. """
        
        self.numberOfInstances = None
        """ Number of Study Related Instances.
        Type `int`. """
        
        self.procedureReference = None
        """ The performed Procedure reference.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.procedureCode = None
        """ The performed procedure code.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.location = None
        """ Where ImagingStudy occurred.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.reasonCode = None
        """ Why the study was requested.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.reasonReference = None
        """ Why was study performed.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.note = None
        """ User-defined comments.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        self.description = None
        """ Institution-generated description.
        Type `str`. """
        
        self.series = None
        """ Each study has one or more series of instances.
        List of `ImagingStudySeries` items (represented as `dict` in JSON). """
        
        super(ImagingStudy, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ImagingStudy, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("modality", "modality", coding.Coding, True, None, False),
            ("subject", "subject", fhirreference.FHIRReference, False, None, True),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("started", "started", fhirdate.FHIRDate, False, None, False),
            ("basedOn", "basedOn", fhirreference.FHIRReference, True, None, False),
            ("referrer", "referrer", fhirreference.FHIRReference, False, None, False),
            ("interpreter", "interpreter", fhirreference.FHIRReference, True, None, False),
            ("endpoint", "endpoint", fhirreference.FHIRReference, True, None, False),
            ("numberOfSeries", "numberOfSeries", int, False, None, False),
            ("numberOfInstances", "numberOfInstances", int, False, None, False),
            ("procedureReference", "procedureReference", fhirreference.FHIRReference, False, None, False),
            ("procedureCode", "procedureCode", codeableconcept.CodeableConcept, True, None, False),
            ("location", "location", fhirreference.FHIRReference, False, None, False),
            ("reasonCode", "reasonCode", codeableconcept.CodeableConcept, True, None, False),
            ("reasonReference", "reasonReference", fhirreference.FHIRReference, True, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
            ("description", "description", str, False, None, False),
            ("series", "series", ImagingStudySeries, True, None, False),
        ])
        return js


from . import backboneelement

class ImagingStudySeries(backboneelement.BackboneElement):
    """ Each study has one or more series of instances.
    
    Each study has one or more series of images or other content.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['uid'] = """DICOM Series Instance UID for the series."""
    _attribute_docstrings['number'] = """Numeric identifier of this series."""
    _attribute_docstrings['modality'] = """The modality of the instances in the series."""
    _attribute_docstrings['description'] = """A short human readable summary of the series."""
    _attribute_docstrings['numberOfInstances'] = """Number of Series Related Instances."""
    _attribute_docstrings['endpoint'] = """Series access endpoint."""
    _attribute_docstrings['bodySite'] = """Body part examined."""
    _attribute_docstrings['laterality'] = """Body part laterality."""
    _attribute_docstrings['specimen'] = """Specimen imaged."""
    _attribute_docstrings['started'] = """When the series started."""
    _attribute_docstrings['performer'] = """Who performed the series."""
    _attribute_docstrings['instance'] = """A single SOP instance from the series."""

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
        
        self.uid = None
        """ DICOM Series Instance UID for the series.
        Type `str`. """
        
        self.number = None
        """ Numeric identifier of this series.
        Type `int`. """
        
        self.modality = None
        """ The modality of the instances in the series.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.description = None
        """ A short human readable summary of the series.
        Type `str`. """
        
        self.numberOfInstances = None
        """ Number of Series Related Instances.
        Type `int`. """
        
        self.endpoint = None
        """ Series access endpoint.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.bodySite = None
        """ Body part examined.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.laterality = None
        """ Body part laterality.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.specimen = None
        """ Specimen imaged.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.started = None
        """ When the series started.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.performer = None
        """ Who performed the series.
        List of `ImagingStudySeriesPerformer` items (represented as `dict` in JSON). """
        
        self.instance = None
        """ A single SOP instance from the series.
        List of `ImagingStudySeriesInstance` items (represented as `dict` in JSON). """
        
        super(ImagingStudySeries, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ImagingStudySeries, self).elementProperties()
        js.extend([
            ("uid", "uid", str, False, None, True),
            ("number", "number", int, False, None, False),
            ("modality", "modality", coding.Coding, False, None, True),
            ("description", "description", str, False, None, False),
            ("numberOfInstances", "numberOfInstances", int, False, None, False),
            ("endpoint", "endpoint", fhirreference.FHIRReference, True, None, False),
            ("bodySite", "bodySite", coding.Coding, False, None, False),
            ("laterality", "laterality", coding.Coding, False, None, False),
            ("specimen", "specimen", fhirreference.FHIRReference, True, None, False),
            ("started", "started", fhirdate.FHIRDate, False, None, False),
            ("performer", "performer", ImagingStudySeriesPerformer, True, None, False),
            ("instance", "instance", ImagingStudySeriesInstance, True, None, False),
        ])
        return js


class ImagingStudySeriesInstance(backboneelement.BackboneElement):
    """ A single SOP instance from the series.
    
    A single SOP instance within the series, e.g. an image, or presentation
    state.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['uid'] = """DICOM SOP Instance UID."""
    _attribute_docstrings['sopClass'] = """DICOM class type."""
    _attribute_docstrings['number'] = """The number of this instance in the series."""
    _attribute_docstrings['title'] = """Description of instance."""

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
        
        self.uid = None
        """ DICOM SOP Instance UID.
        Type `str`. """
        
        self.sopClass = None
        """ DICOM class type.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.number = None
        """ The number of this instance in the series.
        Type `int`. """
        
        self.title = None
        """ Description of instance.
        Type `str`. """
        
        super(ImagingStudySeriesInstance, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ImagingStudySeriesInstance, self).elementProperties()
        js.extend([
            ("uid", "uid", str, False, None, True),
            ("sopClass", "sopClass", coding.Coding, False, None, True),
            ("number", "number", int, False, None, False),
            ("title", "title", str, False, None, False),
        ])
        return js


class ImagingStudySeriesPerformer(backboneelement.BackboneElement):
    """ Who performed the series.
    
    Indicates who or what performed the series and how they were involved.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['function'] = """Type of performance."""
    _attribute_docstrings['actor'] = """Who performed the series."""

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
        
        self.function = None
        """ Type of performance.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.actor = None
        """ Who performed the series.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(ImagingStudySeriesPerformer, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ImagingStudySeriesPerformer, self).elementProperties()
        js.extend([
            ("function", "function", codeableconcept.CodeableConcept, False, None, False),
            ("actor", "actor", fhirreference.FHIRReference, False, None, True),
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
    from . import coding
except ImportError:
    coding = sys.modules[__package__ + '.coding']
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
