#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Specimen) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Specimen(domainresource.DomainResource):
    """ Sample for analysis.
    
    A sample to be used for analysis.
    """
    
    resource_type = "Specimen"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """External Identifier."""
    _attribute_docstrings['accessionIdentifier'] = """Identifier assigned by the lab."""
    _attribute_docstrings['status'] = """The availability of the specimen."""
    _attribute_docstrings['type'] = """Kind of material that forms the specimen."""
    _attribute_docstrings['subject'] = """Where the specimen came from. This may be from patient(s), from a location (e.g., the source of an environmental sample), or a sampling of a substance or a device."""
    _attribute_docstrings['receivedTime'] = """The time when specimen was received for processing."""
    _attribute_docstrings['parent'] = """Specimen from which this specimen originated."""
    _attribute_docstrings['request'] = """Why the specimen was collected."""
    _attribute_docstrings['collection'] = """Collection details."""
    _attribute_docstrings['processing'] = """Processing and processing step details."""
    _attribute_docstrings['container'] = """Direct container of specimen (tube/slide, etc.)."""
    _attribute_docstrings['condition'] = """State of the specimen."""
    _attribute_docstrings['note'] = """Comments."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/specimen-status',
        'restricted_to': ['available', 'unavailable', 'unsatisfactory', 'entered-in-error'],
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
        """ External Identifier.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.accessionIdentifier = None
        """ Identifier assigned by the lab.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.status = None
        """ The availability of the specimen.
        Type `str`. """
        
        self.type = None
        """ Kind of material that forms the specimen.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subject = None
        """ Where the specimen came from. This may be from patient(s), from a
        location (e.g., the source of an environmental sample), or a
        sampling of a substance or a device.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.receivedTime = None
        """ The time when specimen was received for processing.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.parent = None
        """ Specimen from which this specimen originated.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.request = None
        """ Why the specimen was collected.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.collection = None
        """ Collection details.
        Type `SpecimenCollection` (represented as `dict` in JSON). """
        
        self.processing = None
        """ Processing and processing step details.
        List of `SpecimenProcessing` items (represented as `dict` in JSON). """
        
        self.container = None
        """ Direct container of specimen (tube/slide, etc.).
        List of `SpecimenContainer` items (represented as `dict` in JSON). """
        
        self.condition = None
        """ State of the specimen.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.note = None
        """ Comments.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        super(Specimen, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Specimen, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("accessionIdentifier", "accessionIdentifier", identifier.Identifier, False, None, False),
            ("status", "status", str, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("subject", "subject", fhirreference.FHIRReference, False, None, False),
            ("receivedTime", "receivedTime", fhirdate.FHIRDate, False, None, False),
            ("parent", "parent", fhirreference.FHIRReference, True, None, False),
            ("request", "request", fhirreference.FHIRReference, True, None, False),
            ("collection", "collection", SpecimenCollection, False, None, False),
            ("processing", "processing", SpecimenProcessing, True, None, False),
            ("container", "container", SpecimenContainer, True, None, False),
            ("condition", "condition", codeableconcept.CodeableConcept, True, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
        ])
        return js


from . import backboneelement

class SpecimenCollection(backboneelement.BackboneElement):
    """ Collection details.
    
    Details concerning the specimen collection.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['collector'] = """Who collected the specimen."""
    _attribute_docstrings['collectedDateTime'] = """Collection time."""
    _attribute_docstrings['collectedPeriod'] = """Collection time."""
    _attribute_docstrings['duration'] = """How long it took to collect specimen."""
    _attribute_docstrings['quantity'] = """The quantity of specimen collected."""
    _attribute_docstrings['method'] = """Technique used to perform collection."""
    _attribute_docstrings['bodySite'] = """Anatomical collection site."""
    _attribute_docstrings['fastingStatusCodeableConcept'] = """Whether or how long patient abstained from food and/or drink."""
    _attribute_docstrings['fastingStatusDuration'] = """Whether or how long patient abstained from food and/or drink."""

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
        
        self.collector = None
        """ Who collected the specimen.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.collectedDateTime = None
        """ Collection time.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.collectedPeriod = None
        """ Collection time.
        Type `Period` (represented as `dict` in JSON). """
        
        self.duration = None
        """ How long it took to collect specimen.
        Type `Duration` (represented as `dict` in JSON). """
        
        self.quantity = None
        """ The quantity of specimen collected.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.method = None
        """ Technique used to perform collection.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.bodySite = None
        """ Anatomical collection site.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.fastingStatusCodeableConcept = None
        """ Whether or how long patient abstained from food and/or drink.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.fastingStatusDuration = None
        """ Whether or how long patient abstained from food and/or drink.
        Type `Duration` (represented as `dict` in JSON). """
        
        super(SpecimenCollection, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SpecimenCollection, self).elementProperties()
        js.extend([
            ("collector", "collector", fhirreference.FHIRReference, False, None, False),
            ("collectedDateTime", "collectedDateTime", fhirdate.FHIRDate, False, "collected", False),
            ("collectedPeriod", "collectedPeriod", period.Period, False, "collected", False),
            ("duration", "duration", duration.Duration, False, None, False),
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("method", "method", codeableconcept.CodeableConcept, False, None, False),
            ("bodySite", "bodySite", codeableconcept.CodeableConcept, False, None, False),
            ("fastingStatusCodeableConcept", "fastingStatusCodeableConcept", codeableconcept.CodeableConcept, False, "fastingStatus", False),
            ("fastingStatusDuration", "fastingStatusDuration", duration.Duration, False, "fastingStatus", False),
        ])
        return js


class SpecimenContainer(backboneelement.BackboneElement):
    """ Direct container of specimen (tube/slide, etc.).
    
    The container holding the specimen.  The recursive nature of containers;
    i.e. blood in tube in tray in rack is not addressed here.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Id for the container."""
    _attribute_docstrings['description'] = """Textual description of the container."""
    _attribute_docstrings['type'] = """Kind of container directly associated with specimen."""
    _attribute_docstrings['capacity'] = """Container volume or size."""
    _attribute_docstrings['specimenQuantity'] = """Quantity of specimen within container."""
    _attribute_docstrings['additiveCodeableConcept'] = """Additive associated with container."""
    _attribute_docstrings['additiveReference'] = """Additive associated with container."""

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
        """ Id for the container.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.description = None
        """ Textual description of the container.
        Type `str`. """
        
        self.type = None
        """ Kind of container directly associated with specimen.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.capacity = None
        """ Container volume or size.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.specimenQuantity = None
        """ Quantity of specimen within container.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.additiveCodeableConcept = None
        """ Additive associated with container.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.additiveReference = None
        """ Additive associated with container.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(SpecimenContainer, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SpecimenContainer, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("description", "description", str, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("capacity", "capacity", quantity.Quantity, False, None, False),
            ("specimenQuantity", "specimenQuantity", quantity.Quantity, False, None, False),
            ("additiveCodeableConcept", "additiveCodeableConcept", codeableconcept.CodeableConcept, False, "additive", False),
            ("additiveReference", "additiveReference", fhirreference.FHIRReference, False, "additive", False),
        ])
        return js


class SpecimenProcessing(backboneelement.BackboneElement):
    """ Processing and processing step details.
    
    Details concerning processing and processing steps for the specimen.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['description'] = """Textual description of procedure."""
    _attribute_docstrings['procedure'] = """Indicates the treatment step  applied to the specimen."""
    _attribute_docstrings['additive'] = """Material used in the processing step."""
    _attribute_docstrings['timeDateTime'] = """Date and time of specimen processing."""
    _attribute_docstrings['timePeriod'] = """Date and time of specimen processing."""

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
        """ Textual description of procedure.
        Type `str`. """
        
        self.procedure = None
        """ Indicates the treatment step  applied to the specimen.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.additive = None
        """ Material used in the processing step.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.timeDateTime = None
        """ Date and time of specimen processing.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.timePeriod = None
        """ Date and time of specimen processing.
        Type `Period` (represented as `dict` in JSON). """
        
        super(SpecimenProcessing, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SpecimenProcessing, self).elementProperties()
        js.extend([
            ("description", "description", str, False, None, False),
            ("procedure", "procedure", codeableconcept.CodeableConcept, False, None, False),
            ("additive", "additive", fhirreference.FHIRReference, True, None, False),
            ("timeDateTime", "timeDateTime", fhirdate.FHIRDate, False, "time", False),
            ("timePeriod", "timePeriod", period.Period, False, "time", False),
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
    from . import duration
except ImportError:
    duration = sys.modules[__package__ + '.duration']
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
    from . import quantity
except ImportError:
    quantity = sys.modules[__package__ + '.quantity']
