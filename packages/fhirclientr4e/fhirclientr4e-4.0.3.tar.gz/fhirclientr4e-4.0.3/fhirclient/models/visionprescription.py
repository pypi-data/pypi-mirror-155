#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/VisionPrescription) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class VisionPrescription(domainresource.DomainResource):
    """ Prescription for vision correction products for a patient.
    
    An authorization for the provision of glasses and/or contact lenses to a
    patient.
    """
    
    resource_type = "VisionPrescription"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business Identifier for vision prescription."""
    _attribute_docstrings['status'] = """The status of the resource instance."""
    _attribute_docstrings['created'] = """Response creation date."""
    _attribute_docstrings['patient'] = """Who prescription is for."""
    _attribute_docstrings['encounter'] = """Created during encounter / admission / stay."""
    _attribute_docstrings['dateWritten'] = """When prescription was authorized."""
    _attribute_docstrings['prescriber'] = """Who authorized the vision prescription."""
    _attribute_docstrings['lensSpecification'] = """Vision lens authorization."""

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
        """ Business Identifier for vision prescription.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ The status of the resource instance.
        Type `str`. """
        
        self.created = None
        """ Response creation date.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.patient = None
        """ Who prescription is for.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Created during encounter / admission / stay.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.dateWritten = None
        """ When prescription was authorized.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.prescriber = None
        """ Who authorized the vision prescription.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.lensSpecification = None
        """ Vision lens authorization.
        List of `VisionPrescriptionLensSpecification` items (represented as `dict` in JSON). """
        
        super(VisionPrescription, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(VisionPrescription, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("created", "created", fhirdate.FHIRDate, False, None, True),
            ("patient", "patient", fhirreference.FHIRReference, False, None, True),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("dateWritten", "dateWritten", fhirdate.FHIRDate, False, None, True),
            ("prescriber", "prescriber", fhirreference.FHIRReference, False, None, True),
            ("lensSpecification", "lensSpecification", VisionPrescriptionLensSpecification, True, None, True),
        ])
        return js


from . import backboneelement

class VisionPrescriptionLensSpecification(backboneelement.BackboneElement):
    """ Vision lens authorization.
    
    Contain the details of  the individual lens specifications and serves as
    the authorization for the fullfillment by certified professionals.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['product'] = """Identifies the type of vision correction product which is required for the patient."""
    _attribute_docstrings['eye'] = """The eye for which the lens specification applies."""
    _attribute_docstrings['sphere'] = """Power of the lens."""
    _attribute_docstrings['cylinder'] = """Lens power for astigmatism."""
    _attribute_docstrings['axis'] = """Lens meridian which contain no power for astigmatism."""
    _attribute_docstrings['prism'] = """Eye alignment compensation."""
    _attribute_docstrings['add'] = """Added power for multifocal levels."""
    _attribute_docstrings['power'] = """Contact lens power."""
    _attribute_docstrings['backCurve'] = """Contact lens back curvature."""
    _attribute_docstrings['diameter'] = """Contact lens diameter."""
    _attribute_docstrings['duration'] = """Lens wear duration."""
    _attribute_docstrings['color'] = """Color required."""
    _attribute_docstrings['brand'] = """Brand required."""
    _attribute_docstrings['note'] = """Notes for coatings."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['product'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/ex-visionprescriptionproduct',
        'restricted_to': ['lens', 'contact'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['eye'] = {
        'url': 'http://hl7.org/fhir/vision-eye-codes',
        'restricted_to': ['right', 'left'],
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
        
        self.product = None
        """ Identifies the type of vision correction product which is required
        for the patient.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.eye = None
        """ The eye for which the lens specification applies.
        Type `str`. """
        
        self.sphere = None
        """ Power of the lens.
        Type `float`. """
        
        self.cylinder = None
        """ Lens power for astigmatism.
        Type `float`. """
        
        self.axis = None
        """ Lens meridian which contain no power for astigmatism.
        Type `int`. """
        
        self.prism = None
        """ Eye alignment compensation.
        List of `VisionPrescriptionLensSpecificationPrism` items (represented as `dict` in JSON). """
        
        self.add = None
        """ Added power for multifocal levels.
        Type `float`. """
        
        self.power = None
        """ Contact lens power.
        Type `float`. """
        
        self.backCurve = None
        """ Contact lens back curvature.
        Type `float`. """
        
        self.diameter = None
        """ Contact lens diameter.
        Type `float`. """
        
        self.duration = None
        """ Lens wear duration.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.color = None
        """ Color required.
        Type `str`. """
        
        self.brand = None
        """ Brand required.
        Type `str`. """
        
        self.note = None
        """ Notes for coatings.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        super(VisionPrescriptionLensSpecification, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(VisionPrescriptionLensSpecification, self).elementProperties()
        js.extend([
            ("product", "product", codeableconcept.CodeableConcept, False, None, True),
            ("eye", "eye", str, False, None, True),
            ("sphere", "sphere", float, False, None, False),
            ("cylinder", "cylinder", float, False, None, False),
            ("axis", "axis", int, False, None, False),
            ("prism", "prism", VisionPrescriptionLensSpecificationPrism, True, None, False),
            ("add", "add", float, False, None, False),
            ("power", "power", float, False, None, False),
            ("backCurve", "backCurve", float, False, None, False),
            ("diameter", "diameter", float, False, None, False),
            ("duration", "duration", quantity.Quantity, False, None, False),
            ("color", "color", str, False, None, False),
            ("brand", "brand", str, False, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
        ])
        return js


class VisionPrescriptionLensSpecificationPrism(backboneelement.BackboneElement):
    """ Eye alignment compensation.
    
    Allows for adjustment on two axis.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['amount'] = """Amount of adjustment."""
    _attribute_docstrings['base'] = """The relative base, or reference lens edge, for the prism."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['base'] = {
        'url': 'http://hl7.org/fhir/vision-base-codes',
        'restricted_to': ['up', 'down', 'in', 'out'],
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
        
        self.amount = None
        """ Amount of adjustment.
        Type `float`. """
        
        self.base = None
        """ The relative base, or reference lens edge, for the prism.
        Type `str`. """
        
        super(VisionPrescriptionLensSpecificationPrism, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(VisionPrescriptionLensSpecificationPrism, self).elementProperties()
        js.extend([
            ("amount", "amount", float, False, None, True),
            ("base", "base", str, False, None, True),
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
    from . import quantity
except ImportError:
    quantity = sys.modules[__package__ + '.quantity']
