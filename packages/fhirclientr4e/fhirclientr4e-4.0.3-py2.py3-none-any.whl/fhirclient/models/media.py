#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Media) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Media(domainresource.DomainResource):
    """ A photo, video, or audio recording acquired or used in healthcare. The
    actual content may be inline or provided by direct reference.
    """
    
    resource_type = "Media"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Identifier(s) for the image."""
    _attribute_docstrings['basedOn'] = """Procedure that caused this media to be created."""
    _attribute_docstrings['partOf'] = """Part of referenced event."""
    _attribute_docstrings['status'] = """The current state of the {{title}}."""
    _attribute_docstrings['type'] = """A code that classifies whether the media is an image, video or audio recording or some other media category."""
    _attribute_docstrings['modality'] = """The type of acquisition equipment/process."""
    _attribute_docstrings['view'] = """Imaging view, e.g. Lateral or Antero-posterior."""
    _attribute_docstrings['subject'] = """Who/What this Media is a record of."""
    _attribute_docstrings['encounter'] = """Encounter associated with media."""
    _attribute_docstrings['createdDateTime'] = """When Media was collected."""
    _attribute_docstrings['createdPeriod'] = """When Media was collected."""
    _attribute_docstrings['issued'] = """Date/Time this version was made available."""
    _attribute_docstrings['operator'] = """The person who generated the image."""
    _attribute_docstrings['reasonCode'] = """Why was event performed?."""
    _attribute_docstrings['bodySite'] = """Observed body part."""
    _attribute_docstrings['deviceName'] = """Name of the device/manufacturer."""
    _attribute_docstrings['device'] = """Observing Device."""
    _attribute_docstrings['height'] = """Height of the image in pixels (photo/video)."""
    _attribute_docstrings['width'] = """Width of the image in pixels (photo/video)."""
    _attribute_docstrings['frames'] = """Number of frames if > 1 (photo)."""
    _attribute_docstrings['duration'] = """Length in seconds (audio / video)."""
    _attribute_docstrings['content'] = """Actual Media - reference or data."""
    _attribute_docstrings['note'] = """Comments made about the media."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/event-status',
        'restricted_to': ['preparation', 'in-progress', 'not-done', 'on-hold', 'stopped', 'completed', 'entered-in-error', 'unknown'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/media-type',
        'restricted_to': ['image', 'video', 'audio'],
        'binding_strength': 'extensible',
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
        """ Identifier(s) for the image.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.basedOn = None
        """ Procedure that caused this media to be created.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.partOf = None
        """ Part of referenced event.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.status = None
        """ The current state of the {{title}}.
        Type `str`. """
        
        self.type = None
        """ A code that classifies whether the media is an image, video or
        audio recording or some other media category.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.modality = None
        """ The type of acquisition equipment/process.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.view = None
        """ Imaging view, e.g. Lateral or Antero-posterior.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subject = None
        """ Who/What this Media is a record of.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Encounter associated with media.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.createdDateTime = None
        """ When Media was collected.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.createdPeriod = None
        """ When Media was collected.
        Type `Period` (represented as `dict` in JSON). """
        
        self.issued = None
        """ Date/Time this version was made available.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.operator = None
        """ The person who generated the image.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.reasonCode = None
        """ Why was event performed?.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.bodySite = None
        """ Observed body part.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.deviceName = None
        """ Name of the device/manufacturer.
        Type `str`. """
        
        self.device = None
        """ Observing Device.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.height = None
        """ Height of the image in pixels (photo/video).
        Type `int`. """
        
        self.width = None
        """ Width of the image in pixels (photo/video).
        Type `int`. """
        
        self.frames = None
        """ Number of frames if > 1 (photo).
        Type `int`. """
        
        self.duration = None
        """ Length in seconds (audio / video).
        Type `float`. """
        
        self.content = None
        """ Actual Media - reference or data.
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.note = None
        """ Comments made about the media.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        super(Media, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Media, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("basedOn", "basedOn", fhirreference.FHIRReference, True, None, False),
            ("partOf", "partOf", fhirreference.FHIRReference, True, None, False),
            ("status", "status", str, False, None, True),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("modality", "modality", codeableconcept.CodeableConcept, False, None, False),
            ("view", "view", codeableconcept.CodeableConcept, False, None, False),
            ("subject", "subject", fhirreference.FHIRReference, False, None, False),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("createdDateTime", "createdDateTime", fhirdate.FHIRDate, False, "created", False),
            ("createdPeriod", "createdPeriod", period.Period, False, "created", False),
            ("issued", "issued", fhirdate.FHIRDate, False, None, False),
            ("operator", "operator", fhirreference.FHIRReference, False, None, False),
            ("reasonCode", "reasonCode", codeableconcept.CodeableConcept, True, None, False),
            ("bodySite", "bodySite", codeableconcept.CodeableConcept, False, None, False),
            ("deviceName", "deviceName", str, False, None, False),
            ("device", "device", fhirreference.FHIRReference, False, None, False),
            ("height", "height", int, False, None, False),
            ("width", "width", int, False, None, False),
            ("frames", "frames", int, False, None, False),
            ("duration", "duration", float, False, None, False),
            ("content", "content", attachment.Attachment, False, None, True),
            ("note", "note", annotation.Annotation, True, None, False),
        ])
        return js


import sys
try:
    from . import annotation
except ImportError:
    annotation = sys.modules[__package__ + '.annotation']
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
