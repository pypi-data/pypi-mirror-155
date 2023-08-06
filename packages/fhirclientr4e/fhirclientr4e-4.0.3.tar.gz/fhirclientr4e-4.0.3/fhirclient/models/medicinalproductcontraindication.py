#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/MedicinalProductContraindication) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class MedicinalProductContraindication(domainresource.DomainResource):
    """ MedicinalProductContraindication.
    
    The clinical particulars - indications, contraindications etc. of a
    medicinal product, including for regulatory purposes.
    """
    
    resource_type = "MedicinalProductContraindication"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['subject'] = """The medication for which this is an indication."""
    _attribute_docstrings['disease'] = """The disease, symptom or procedure for the contraindication."""
    _attribute_docstrings['diseaseStatus'] = """The status of the disease or symptom for the contraindication."""
    _attribute_docstrings['comorbidity'] = """A comorbidity (concurrent condition) or coinfection."""
    _attribute_docstrings['therapeuticIndication'] = """Information about the use of the medicinal product in relation to other therapies as part of the indication."""
    _attribute_docstrings['otherTherapy'] = """Information about the use of the medicinal product in relation to other therapies described as part of the indication."""
    _attribute_docstrings['population'] = """The population group to which this applies."""

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
        
        self.subject = None
        """ The medication for which this is an indication.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.disease = None
        """ The disease, symptom or procedure for the contraindication.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.diseaseStatus = None
        """ The status of the disease or symptom for the contraindication.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.comorbidity = None
        """ A comorbidity (concurrent condition) or coinfection.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.therapeuticIndication = None
        """ Information about the use of the medicinal product in relation to
        other therapies as part of the indication.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.otherTherapy = None
        """ Information about the use of the medicinal product in relation to
        other therapies described as part of the indication.
        List of `MedicinalProductContraindicationOtherTherapy` items (represented as `dict` in JSON). """
        
        self.population = None
        """ The population group to which this applies.
        List of `Population` items (represented as `dict` in JSON). """
        
        super(MedicinalProductContraindication, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicinalProductContraindication, self).elementProperties()
        js.extend([
            ("subject", "subject", fhirreference.FHIRReference, True, None, False),
            ("disease", "disease", codeableconcept.CodeableConcept, False, None, False),
            ("diseaseStatus", "diseaseStatus", codeableconcept.CodeableConcept, False, None, False),
            ("comorbidity", "comorbidity", codeableconcept.CodeableConcept, True, None, False),
            ("therapeuticIndication", "therapeuticIndication", fhirreference.FHIRReference, True, None, False),
            ("otherTherapy", "otherTherapy", MedicinalProductContraindicationOtherTherapy, True, None, False),
            ("population", "population", population.Population, True, None, False),
        ])
        return js


from . import backboneelement

class MedicinalProductContraindicationOtherTherapy(backboneelement.BackboneElement):
    """ Information about the use of the medicinal product in relation to other
    therapies described as part of the indication.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['therapyRelationshipType'] = """The type of relationship between the medicinal product indication or contraindication and another therapy."""
    _attribute_docstrings['medicationCodeableConcept'] = """Reference to a specific medication (active substance, medicinal product or class of products) as part of an indication or contraindication."""
    _attribute_docstrings['medicationReference'] = """Reference to a specific medication (active substance, medicinal product or class of products) as part of an indication or contraindication."""

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
        
        self.therapyRelationshipType = None
        """ The type of relationship between the medicinal product indication
        or contraindication and another therapy.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.medicationCodeableConcept = None
        """ Reference to a specific medication (active substance, medicinal
        product or class of products) as part of an indication or
        contraindication.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.medicationReference = None
        """ Reference to a specific medication (active substance, medicinal
        product or class of products) as part of an indication or
        contraindication.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(MedicinalProductContraindicationOtherTherapy, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicinalProductContraindicationOtherTherapy, self).elementProperties()
        js.extend([
            ("therapyRelationshipType", "therapyRelationshipType", codeableconcept.CodeableConcept, False, None, True),
            ("medicationCodeableConcept", "medicationCodeableConcept", codeableconcept.CodeableConcept, False, "medication", True),
            ("medicationReference", "medicationReference", fhirreference.FHIRReference, False, "medication", True),
        ])
        return js


import sys
try:
    from . import codeableconcept
except ImportError:
    codeableconcept = sys.modules[__package__ + '.codeableconcept']
try:
    from . import fhirreference
except ImportError:
    fhirreference = sys.modules[__package__ + '.fhirreference']
try:
    from . import population
except ImportError:
    population = sys.modules[__package__ + '.population']
