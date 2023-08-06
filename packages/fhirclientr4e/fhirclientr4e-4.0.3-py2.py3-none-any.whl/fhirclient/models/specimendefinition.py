#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/SpecimenDefinition) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class SpecimenDefinition(domainresource.DomainResource):
    """ Kind of specimen.
    
    A kind of specimen with associated set of requirements.
    """
    
    resource_type = "SpecimenDefinition"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business identifier of a kind of specimen."""
    _attribute_docstrings['typeCollected'] = """Kind of material to collect."""
    _attribute_docstrings['patientPreparation'] = """Patient preparation for collection."""
    _attribute_docstrings['timeAspect'] = """Time aspect for collection."""
    _attribute_docstrings['collection'] = """Specimen collection procedure."""
    _attribute_docstrings['typeTested'] = """Specimen in container intended for testing by lab."""

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
        """ Business identifier of a kind of specimen.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.typeCollected = None
        """ Kind of material to collect.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.patientPreparation = None
        """ Patient preparation for collection.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.timeAspect = None
        """ Time aspect for collection.
        Type `str`. """
        
        self.collection = None
        """ Specimen collection procedure.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.typeTested = None
        """ Specimen in container intended for testing by lab.
        List of `SpecimenDefinitionTypeTested` items (represented as `dict` in JSON). """
        
        super(SpecimenDefinition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SpecimenDefinition, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, False, None, False),
            ("typeCollected", "typeCollected", codeableconcept.CodeableConcept, False, None, False),
            ("patientPreparation", "patientPreparation", codeableconcept.CodeableConcept, True, None, False),
            ("timeAspect", "timeAspect", str, False, None, False),
            ("collection", "collection", codeableconcept.CodeableConcept, True, None, False),
            ("typeTested", "typeTested", SpecimenDefinitionTypeTested, True, None, False),
        ])
        return js


from . import backboneelement

class SpecimenDefinitionTypeTested(backboneelement.BackboneElement):
    """ Specimen in container intended for testing by lab.
    
    Specimen conditioned in a container as expected by the testing laboratory.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['isDerived'] = """Primary or secondary specimen."""
    _attribute_docstrings['type'] = """Type of intended specimen."""
    _attribute_docstrings['preference'] = """The preference for this type of conditioned specimen."""
    _attribute_docstrings['container'] = """The specimen's container."""
    _attribute_docstrings['requirement'] = """Specimen requirements."""
    _attribute_docstrings['retentionTime'] = """Specimen retention time."""
    _attribute_docstrings['rejectionCriterion'] = """Criterion for rejection of the specimen in its container by the laboratory."""
    _attribute_docstrings['handling'] = """Specimen handling before testing."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['preference'] = {
        'url': 'http://hl7.org/fhir/specimen-contained-preference',
        'restricted_to': ['preferred', 'alternate'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['rejectionCriterion'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/rejection-criteria',
        'restricted_to': ['hemolized', 'insufficient', 'broken', 'clotted', 'wrong-temperature'],
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
        
        self.isDerived = None
        """ Primary or secondary specimen.
        Type `bool`. """
        
        self.type = None
        """ Type of intended specimen.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.preference = None
        """ The preference for this type of conditioned specimen.
        Type `str`. """
        
        self.container = None
        """ The specimen's container.
        Type `SpecimenDefinitionTypeTestedContainer` (represented as `dict` in JSON). """
        
        self.requirement = None
        """ Specimen requirements.
        Type `str`. """
        
        self.retentionTime = None
        """ Specimen retention time.
        Type `Duration` (represented as `dict` in JSON). """
        
        self.rejectionCriterion = None
        """ Criterion for rejection of the specimen in its container by the
        laboratory.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.handling = None
        """ Specimen handling before testing.
        List of `SpecimenDefinitionTypeTestedHandling` items (represented as `dict` in JSON). """
        
        super(SpecimenDefinitionTypeTested, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SpecimenDefinitionTypeTested, self).elementProperties()
        js.extend([
            ("isDerived", "isDerived", bool, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("preference", "preference", str, False, None, True),
            ("container", "container", SpecimenDefinitionTypeTestedContainer, False, None, False),
            ("requirement", "requirement", str, False, None, False),
            ("retentionTime", "retentionTime", duration.Duration, False, None, False),
            ("rejectionCriterion", "rejectionCriterion", codeableconcept.CodeableConcept, True, None, False),
            ("handling", "handling", SpecimenDefinitionTypeTestedHandling, True, None, False),
        ])
        return js


class SpecimenDefinitionTypeTestedContainer(backboneelement.BackboneElement):
    """ The specimen's container.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['material'] = """Container material."""
    _attribute_docstrings['type'] = """Kind of container associated with the kind of specimen."""
    _attribute_docstrings['cap'] = """None"""
    _attribute_docstrings['description'] = """Container description."""
    _attribute_docstrings['capacity'] = """Container capacity."""
    _attribute_docstrings['minimumVolumeQuantity'] = """Minimum volume."""
    _attribute_docstrings['minimumVolumeString'] = """Minimum volume."""
    _attribute_docstrings['additive'] = """Additive associated with container."""
    _attribute_docstrings['preparation'] = """Specimen container preparation."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['cap'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/container-cap',
        'restricted_to': ['red', 'yellow', 'dark-yellow', 'grey', 'light-blue', 'black', 'green', 'light-green', 'lavender', 'brown', 'white', 'pink'],
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
        
        self.material = None
        """ Container material.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.type = None
        """ Kind of container associated with the kind of specimen.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.cap = None
        """ None.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.description = None
        """ Container description.
        Type `str`. """
        
        self.capacity = None
        """ Container capacity.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.minimumVolumeQuantity = None
        """ Minimum volume.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.minimumVolumeString = None
        """ Minimum volume.
        Type `str`. """
        
        self.additive = None
        """ Additive associated with container.
        List of `SpecimenDefinitionTypeTestedContainerAdditive` items (represented as `dict` in JSON). """
        
        self.preparation = None
        """ Specimen container preparation.
        Type `str`. """
        
        super(SpecimenDefinitionTypeTestedContainer, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SpecimenDefinitionTypeTestedContainer, self).elementProperties()
        js.extend([
            ("material", "material", codeableconcept.CodeableConcept, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("cap", "cap", codeableconcept.CodeableConcept, False, None, False),
            ("description", "description", str, False, None, False),
            ("capacity", "capacity", quantity.Quantity, False, None, False),
            ("minimumVolumeQuantity", "minimumVolumeQuantity", quantity.Quantity, False, "minimumVolume", False),
            ("minimumVolumeString", "minimumVolumeString", str, False, "minimumVolume", False),
            ("additive", "additive", SpecimenDefinitionTypeTestedContainerAdditive, True, None, False),
            ("preparation", "preparation", str, False, None, False),
        ])
        return js


class SpecimenDefinitionTypeTestedContainerAdditive(backboneelement.BackboneElement):
    """ Additive associated with container.
    
    Substance introduced in the kind of container to preserve, maintain or
    enhance the specimen. Examples: Formalin, Citrate, EDTA.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
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
        
        self.additiveCodeableConcept = None
        """ Additive associated with container.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.additiveReference = None
        """ Additive associated with container.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(SpecimenDefinitionTypeTestedContainerAdditive, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SpecimenDefinitionTypeTestedContainerAdditive, self).elementProperties()
        js.extend([
            ("additiveCodeableConcept", "additiveCodeableConcept", codeableconcept.CodeableConcept, False, "additive", True),
            ("additiveReference", "additiveReference", fhirreference.FHIRReference, False, "additive", True),
        ])
        return js


class SpecimenDefinitionTypeTestedHandling(backboneelement.BackboneElement):
    """ Specimen handling before testing.
    
    Set of instructions for preservation/transport of the specimen at a defined
    temperature interval, prior the testing process.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['temperatureQualifier'] = """It qualifies the interval of temperature, which characterizes an occurrence of handling. Conditions that are not related to temperature may be handled in the instruction element."""
    _attribute_docstrings['temperatureRange'] = """Temperature range."""
    _attribute_docstrings['maxDuration'] = """Maximum preservation time."""
    _attribute_docstrings['instruction'] = """Preservation instruction."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['temperatureQualifier'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/handling-condition',
        'restricted_to': ['room', 'refrigerated', 'frozen'],
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
        
        self.temperatureQualifier = None
        """ It qualifies the interval of temperature, which characterizes an
        occurrence of handling. Conditions that are not related to
        temperature may be handled in the instruction element.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.temperatureRange = None
        """ Temperature range.
        Type `Range` (represented as `dict` in JSON). """
        
        self.maxDuration = None
        """ Maximum preservation time.
        Type `Duration` (represented as `dict` in JSON). """
        
        self.instruction = None
        """ Preservation instruction.
        Type `str`. """
        
        super(SpecimenDefinitionTypeTestedHandling, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SpecimenDefinitionTypeTestedHandling, self).elementProperties()
        js.extend([
            ("temperatureQualifier", "temperatureQualifier", codeableconcept.CodeableConcept, False, None, False),
            ("temperatureRange", "temperatureRange", range.Range, False, None, False),
            ("maxDuration", "maxDuration", duration.Duration, False, None, False),
            ("instruction", "instruction", str, False, None, False),
        ])
        return js


import sys
try:
    from . import codeableconcept
except ImportError:
    codeableconcept = sys.modules[__package__ + '.codeableconcept']
try:
    from . import duration
except ImportError:
    duration = sys.modules[__package__ + '.duration']
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
try:
    from . import range
except ImportError:
    range = sys.modules[__package__ + '.range']
