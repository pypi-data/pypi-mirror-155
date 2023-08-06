#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/MedicationKnowledge) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class MedicationKnowledge(domainresource.DomainResource):
    """ Definition of Medication Knowledge.
    
    Information about a medication that is used to support knowledge.
    """
    
    resource_type = "MedicationKnowledge"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Code that identifies this medication."""
    _attribute_docstrings['status'] = """A code to indicate if the medication is in active use.  The status refers to the validity about the information of the medication and not to its medicinal properties."""
    _attribute_docstrings['manufacturer'] = """Manufacturer of the item."""
    _attribute_docstrings['doseForm'] = """powder | tablets | capsule +."""
    _attribute_docstrings['amount'] = """Amount of drug in package."""
    _attribute_docstrings['synonym'] = """Additional names for a medication."""
    _attribute_docstrings['relatedMedicationKnowledge'] = """Associated or related medication information."""
    _attribute_docstrings['associatedMedication'] = """A medication resource that is associated with this medication."""
    _attribute_docstrings['productType'] = """Category of the medication or product."""
    _attribute_docstrings['monograph'] = """Associated documentation about the medication."""
    _attribute_docstrings['ingredient'] = """Active or inactive ingredient."""
    _attribute_docstrings['preparationInstruction'] = """The instructions for preparing the medication."""
    _attribute_docstrings['intendedRoute'] = """The intended or approved route of administration."""
    _attribute_docstrings['cost'] = """The pricing of the medication."""
    _attribute_docstrings['monitoringProgram'] = """Program under which a medication is reviewed."""
    _attribute_docstrings['administrationGuidelines'] = """Guidelines for administration of the medication."""
    _attribute_docstrings['medicineClassification'] = """Categorization of the medication within a formulary or classification system."""
    _attribute_docstrings['packaging'] = """Details about packaged medications."""
    _attribute_docstrings['drugCharacteristic'] = """Specifies descriptive properties of the medicine."""
    _attribute_docstrings['contraindication'] = """Potential clinical issue with or between medication(s)."""
    _attribute_docstrings['regulatory'] = """Regulatory information about a medication."""
    _attribute_docstrings['kinetics'] = """The time course of drug absorption, distribution, metabolism and excretion of a medication from the body."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/medicationknowledge-status',
        'restricted_to': ['active', 'inactive', 'entered-in-error'],
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
        
        self.code = None
        """ Code that identifies this medication.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.status = None
        """ A code to indicate if the medication is in active use.  The status
        refers to the validity about the information of the medication and
        not to its medicinal properties.
        Type `str`. """
        
        self.manufacturer = None
        """ Manufacturer of the item.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.doseForm = None
        """ powder | tablets | capsule +.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.amount = None
        """ Amount of drug in package.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.synonym = None
        """ Additional names for a medication.
        List of `str` items. """
        
        self.relatedMedicationKnowledge = None
        """ Associated or related medication information.
        List of `MedicationKnowledgeRelatedMedicationKnowledge` items (represented as `dict` in JSON). """
        
        self.associatedMedication = None
        """ A medication resource that is associated with this medication.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.productType = None
        """ Category of the medication or product.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.monograph = None
        """ Associated documentation about the medication.
        List of `MedicationKnowledgeMonograph` items (represented as `dict` in JSON). """
        
        self.ingredient = None
        """ Active or inactive ingredient.
        List of `MedicationKnowledgeIngredient` items (represented as `dict` in JSON). """
        
        self.preparationInstruction = None
        """ The instructions for preparing the medication.
        Type `str`. """
        
        self.intendedRoute = None
        """ The intended or approved route of administration.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.cost = None
        """ The pricing of the medication.
        List of `MedicationKnowledgeCost` items (represented as `dict` in JSON). """
        
        self.monitoringProgram = None
        """ Program under which a medication is reviewed.
        List of `MedicationKnowledgeMonitoringProgram` items (represented as `dict` in JSON). """
        
        self.administrationGuidelines = None
        """ Guidelines for administration of the medication.
        List of `MedicationKnowledgeAdministrationGuidelines` items (represented as `dict` in JSON). """
        
        self.medicineClassification = None
        """ Categorization of the medication within a formulary or
        classification system.
        List of `MedicationKnowledgeMedicineClassification` items (represented as `dict` in JSON). """
        
        self.packaging = None
        """ Details about packaged medications.
        Type `MedicationKnowledgePackaging` (represented as `dict` in JSON). """
        
        self.drugCharacteristic = None
        """ Specifies descriptive properties of the medicine.
        List of `MedicationKnowledgeDrugCharacteristic` items (represented as `dict` in JSON). """
        
        self.contraindication = None
        """ Potential clinical issue with or between medication(s).
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.regulatory = None
        """ Regulatory information about a medication.
        List of `MedicationKnowledgeRegulatory` items (represented as `dict` in JSON). """
        
        self.kinetics = None
        """ The time course of drug absorption, distribution, metabolism and
        excretion of a medication from the body.
        List of `MedicationKnowledgeKinetics` items (represented as `dict` in JSON). """
        
        super(MedicationKnowledge, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationKnowledge, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("status", "status", str, False, None, False),
            ("manufacturer", "manufacturer", fhirreference.FHIRReference, False, None, False),
            ("doseForm", "doseForm", codeableconcept.CodeableConcept, False, None, False),
            ("amount", "amount", quantity.Quantity, False, None, False),
            ("synonym", "synonym", str, True, None, False),
            ("relatedMedicationKnowledge", "relatedMedicationKnowledge", MedicationKnowledgeRelatedMedicationKnowledge, True, None, False),
            ("associatedMedication", "associatedMedication", fhirreference.FHIRReference, True, None, False),
            ("productType", "productType", codeableconcept.CodeableConcept, True, None, False),
            ("monograph", "monograph", MedicationKnowledgeMonograph, True, None, False),
            ("ingredient", "ingredient", MedicationKnowledgeIngredient, True, None, False),
            ("preparationInstruction", "preparationInstruction", str, False, None, False),
            ("intendedRoute", "intendedRoute", codeableconcept.CodeableConcept, True, None, False),
            ("cost", "cost", MedicationKnowledgeCost, True, None, False),
            ("monitoringProgram", "monitoringProgram", MedicationKnowledgeMonitoringProgram, True, None, False),
            ("administrationGuidelines", "administrationGuidelines", MedicationKnowledgeAdministrationGuidelines, True, None, False),
            ("medicineClassification", "medicineClassification", MedicationKnowledgeMedicineClassification, True, None, False),
            ("packaging", "packaging", MedicationKnowledgePackaging, False, None, False),
            ("drugCharacteristic", "drugCharacteristic", MedicationKnowledgeDrugCharacteristic, True, None, False),
            ("contraindication", "contraindication", fhirreference.FHIRReference, True, None, False),
            ("regulatory", "regulatory", MedicationKnowledgeRegulatory, True, None, False),
            ("kinetics", "kinetics", MedicationKnowledgeKinetics, True, None, False),
        ])
        return js


from . import backboneelement

class MedicationKnowledgeAdministrationGuidelines(backboneelement.BackboneElement):
    """ Guidelines for administration of the medication.
    
    Guidelines for the administration of the medication.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['dosage'] = """Dosage for the medication for the specific guidelines."""
    _attribute_docstrings['indicationCodeableConcept'] = """Indication for use that apply to the specific administration guidelines."""
    _attribute_docstrings['indicationReference'] = """Indication for use that apply to the specific administration guidelines."""
    _attribute_docstrings['patientCharacteristics'] = """Characteristics of the patient that are relevant to the administration guidelines."""

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
        
        self.dosage = None
        """ Dosage for the medication for the specific guidelines.
        List of `MedicationKnowledgeAdministrationGuidelinesDosage` items (represented as `dict` in JSON). """
        
        self.indicationCodeableConcept = None
        """ Indication for use that apply to the specific administration
        guidelines.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.indicationReference = None
        """ Indication for use that apply to the specific administration
        guidelines.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.patientCharacteristics = None
        """ Characteristics of the patient that are relevant to the
        administration guidelines.
        List of `MedicationKnowledgeAdministrationGuidelinesPatientCharacteristics` items (represented as `dict` in JSON). """
        
        super(MedicationKnowledgeAdministrationGuidelines, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationKnowledgeAdministrationGuidelines, self).elementProperties()
        js.extend([
            ("dosage", "dosage", MedicationKnowledgeAdministrationGuidelinesDosage, True, None, False),
            ("indicationCodeableConcept", "indicationCodeableConcept", codeableconcept.CodeableConcept, False, "indication", False),
            ("indicationReference", "indicationReference", fhirreference.FHIRReference, False, "indication", False),
            ("patientCharacteristics", "patientCharacteristics", MedicationKnowledgeAdministrationGuidelinesPatientCharacteristics, True, None, False),
        ])
        return js


class MedicationKnowledgeAdministrationGuidelinesDosage(backboneelement.BackboneElement):
    """ Dosage for the medication for the specific guidelines.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Type of dosage."""
    _attribute_docstrings['dosage'] = """Dosage for the medication for the specific guidelines."""

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
        
        self.type = None
        """ Type of dosage.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.dosage = None
        """ Dosage for the medication for the specific guidelines.
        List of `Dosage` items (represented as `dict` in JSON). """
        
        super(MedicationKnowledgeAdministrationGuidelinesDosage, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationKnowledgeAdministrationGuidelinesDosage, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("dosage", "dosage", dosage.Dosage, True, None, True),
        ])
        return js


class MedicationKnowledgeAdministrationGuidelinesPatientCharacteristics(backboneelement.BackboneElement):
    """ Characteristics of the patient that are relevant to the administration
    guidelines.
    
    Characteristics of the patient that are relevant to the administration
    guidelines (for example, height, weight, gender, etc.).
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['characteristicCodeableConcept'] = """Specific characteristic that is relevant to the administration guideline."""
    _attribute_docstrings['characteristicQuantity'] = """Specific characteristic that is relevant to the administration guideline."""
    _attribute_docstrings['value'] = """The specific characteristic."""

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
        
        self.characteristicCodeableConcept = None
        """ Specific characteristic that is relevant to the administration
        guideline.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.characteristicQuantity = None
        """ Specific characteristic that is relevant to the administration
        guideline.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.value = None
        """ The specific characteristic.
        List of `str` items. """
        
        super(MedicationKnowledgeAdministrationGuidelinesPatientCharacteristics, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationKnowledgeAdministrationGuidelinesPatientCharacteristics, self).elementProperties()
        js.extend([
            ("characteristicCodeableConcept", "characteristicCodeableConcept", codeableconcept.CodeableConcept, False, "characteristic", True),
            ("characteristicQuantity", "characteristicQuantity", quantity.Quantity, False, "characteristic", True),
            ("value", "value", str, True, None, False),
        ])
        return js


class MedicationKnowledgeCost(backboneelement.BackboneElement):
    """ The pricing of the medication.
    
    The price of the medication.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """The category of the cost information."""
    _attribute_docstrings['source'] = """The source or owner for the price information."""
    _attribute_docstrings['cost'] = """The price of the medication."""

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
        
        self.type = None
        """ The category of the cost information.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.source = None
        """ The source or owner for the price information.
        Type `str`. """
        
        self.cost = None
        """ The price of the medication.
        Type `Money` (represented as `dict` in JSON). """
        
        super(MedicationKnowledgeCost, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationKnowledgeCost, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("source", "source", str, False, None, False),
            ("cost", "cost", money.Money, False, None, True),
        ])
        return js


class MedicationKnowledgeDrugCharacteristic(backboneelement.BackboneElement):
    """ Specifies descriptive properties of the medicine.
    
    Specifies descriptive properties of the medicine, such as color, shape,
    imprints, etc.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """A code specifying which characteristic of the medicine is being described (for example, colour, shape, imprint)."""
    _attribute_docstrings['valueCodeableConcept'] = """Description of the characteristic."""
    _attribute_docstrings['valueString'] = """Description of the characteristic."""
    _attribute_docstrings['valueQuantity'] = """Description of the characteristic."""
    _attribute_docstrings['valueBase64Binary'] = """Description of the characteristic."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/medicationknowledge-characteristic',
        'restricted_to': ['imprintcd', 'size', 'shape', 'color', 'coating', 'scoring', 'logo'],
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
        
        self.type = None
        """ A code specifying which characteristic of the medicine is being
        described (for example, colour, shape, imprint).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.valueCodeableConcept = None
        """ Description of the characteristic.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.valueString = None
        """ Description of the characteristic.
        Type `str`. """
        
        self.valueQuantity = None
        """ Description of the characteristic.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.valueBase64Binary = None
        """ Description of the characteristic.
        Type `str`. """
        
        super(MedicationKnowledgeDrugCharacteristic, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationKnowledgeDrugCharacteristic, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("valueCodeableConcept", "valueCodeableConcept", codeableconcept.CodeableConcept, False, "value", False),
            ("valueString", "valueString", str, False, "value", False),
            ("valueQuantity", "valueQuantity", quantity.Quantity, False, "value", False),
            ("valueBase64Binary", "valueBase64Binary", str, False, "value", False),
        ])
        return js


class MedicationKnowledgeIngredient(backboneelement.BackboneElement):
    """ Active or inactive ingredient.
    
    Identifies a particular constituent of interest in the product.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['itemCodeableConcept'] = """Medication(s) or substance(s) contained in the medication."""
    _attribute_docstrings['itemReference'] = """Medication(s) or substance(s) contained in the medication."""
    _attribute_docstrings['isActive'] = """Active ingredient indicator."""
    _attribute_docstrings['strength'] = """Quantity of ingredient present."""

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
        
        self.itemCodeableConcept = None
        """ Medication(s) or substance(s) contained in the medication.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.itemReference = None
        """ Medication(s) or substance(s) contained in the medication.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.isActive = None
        """ Active ingredient indicator.
        Type `bool`. """
        
        self.strength = None
        """ Quantity of ingredient present.
        Type `Ratio` (represented as `dict` in JSON). """
        
        super(MedicationKnowledgeIngredient, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationKnowledgeIngredient, self).elementProperties()
        js.extend([
            ("itemCodeableConcept", "itemCodeableConcept", codeableconcept.CodeableConcept, False, "item", True),
            ("itemReference", "itemReference", fhirreference.FHIRReference, False, "item", True),
            ("isActive", "isActive", bool, False, None, False),
            ("strength", "strength", ratio.Ratio, False, None, False),
        ])
        return js


class MedicationKnowledgeKinetics(backboneelement.BackboneElement):
    """ The time course of drug absorption, distribution, metabolism and excretion
    of a medication from the body.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['areaUnderCurve'] = """The drug concentration measured at certain discrete points in time."""
    _attribute_docstrings['lethalDose50'] = """The median lethal dose of a drug."""
    _attribute_docstrings['halfLifePeriod'] = """Time required for concentration in the body to decrease by half."""

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
        
        self.areaUnderCurve = None
        """ The drug concentration measured at certain discrete points in time.
        List of `Quantity` items (represented as `dict` in JSON). """
        
        self.lethalDose50 = None
        """ The median lethal dose of a drug.
        List of `Quantity` items (represented as `dict` in JSON). """
        
        self.halfLifePeriod = None
        """ Time required for concentration in the body to decrease by half.
        Type `Duration` (represented as `dict` in JSON). """
        
        super(MedicationKnowledgeKinetics, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationKnowledgeKinetics, self).elementProperties()
        js.extend([
            ("areaUnderCurve", "areaUnderCurve", quantity.Quantity, True, None, False),
            ("lethalDose50", "lethalDose50", quantity.Quantity, True, None, False),
            ("halfLifePeriod", "halfLifePeriod", duration.Duration, False, None, False),
        ])
        return js


class MedicationKnowledgeMedicineClassification(backboneelement.BackboneElement):
    """ Categorization of the medication within a formulary or classification
    system.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """The type of category for the medication (for example, therapeutic classification, therapeutic sub-classification)."""
    _attribute_docstrings['classification'] = """Specific category assigned to the medication."""

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
        
        self.type = None
        """ The type of category for the medication (for example, therapeutic
        classification, therapeutic sub-classification).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.classification = None
        """ Specific category assigned to the medication.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        super(MedicationKnowledgeMedicineClassification, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationKnowledgeMedicineClassification, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("classification", "classification", codeableconcept.CodeableConcept, True, None, False),
        ])
        return js


class MedicationKnowledgeMonitoringProgram(backboneelement.BackboneElement):
    """ Program under which a medication is reviewed.
    
    The program under which the medication is reviewed.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Type of program under which the medication is monitored."""
    _attribute_docstrings['name'] = """Name of the reviewing program."""

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
        
        self.type = None
        """ Type of program under which the medication is monitored.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.name = None
        """ Name of the reviewing program.
        Type `str`. """
        
        super(MedicationKnowledgeMonitoringProgram, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationKnowledgeMonitoringProgram, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("name", "name", str, False, None, False),
        ])
        return js


class MedicationKnowledgeMonograph(backboneelement.BackboneElement):
    """ Associated documentation about the medication.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """The category of medication document."""
    _attribute_docstrings['source'] = """Associated documentation about the medication."""

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
        
        self.type = None
        """ The category of medication document.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.source = None
        """ Associated documentation about the medication.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(MedicationKnowledgeMonograph, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationKnowledgeMonograph, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("source", "source", fhirreference.FHIRReference, False, None, False),
        ])
        return js


class MedicationKnowledgePackaging(backboneelement.BackboneElement):
    """ Details about packaged medications.
    
    Information that only applies to packages (not products).
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """A code that defines the specific type of packaging that the medication can be found in (e.g. blister sleeve, tube, bottle)."""
    _attribute_docstrings['quantity'] = """The number of product units the package would contain if fully loaded."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/medicationknowledge-package-type',
        'restricted_to': ['amp', 'bag', 'blstrpk', 'bot', 'box', 'can', 'cart', 'disk', 'doset', 'jar', 'jug', 'minim', 'nebamp', 'ovul', 'pch', 'pkt', 'sash', 'strip', 'tin', 'tub', 'tube', 'vial'],
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
        
        self.type = None
        """ A code that defines the specific type of packaging that the
        medication can be found in (e.g. blister sleeve, tube, bottle).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.quantity = None
        """ The number of product units the package would contain if fully
        loaded.
        Type `Quantity` (represented as `dict` in JSON). """
        
        super(MedicationKnowledgePackaging, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationKnowledgePackaging, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("quantity", "quantity", quantity.Quantity, False, None, False),
        ])
        return js


class MedicationKnowledgeRegulatory(backboneelement.BackboneElement):
    """ Regulatory information about a medication.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['regulatoryAuthority'] = """Specifies the authority of the regulation."""
    _attribute_docstrings['substitution'] = """Specifies if changes are allowed when dispensing a medication from a regulatory perspective."""
    _attribute_docstrings['schedule'] = """Specifies the schedule of a medication in jurisdiction."""
    _attribute_docstrings['maxDispense'] = """The maximum number of units of the medication that can be dispensed in a period."""

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
        
        self.regulatoryAuthority = None
        """ Specifies the authority of the regulation.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.substitution = None
        """ Specifies if changes are allowed when dispensing a medication from
        a regulatory perspective.
        List of `MedicationKnowledgeRegulatorySubstitution` items (represented as `dict` in JSON). """
        
        self.schedule = None
        """ Specifies the schedule of a medication in jurisdiction.
        List of `MedicationKnowledgeRegulatorySchedule` items (represented as `dict` in JSON). """
        
        self.maxDispense = None
        """ The maximum number of units of the medication that can be dispensed
        in a period.
        Type `MedicationKnowledgeRegulatoryMaxDispense` (represented as `dict` in JSON). """
        
        super(MedicationKnowledgeRegulatory, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationKnowledgeRegulatory, self).elementProperties()
        js.extend([
            ("regulatoryAuthority", "regulatoryAuthority", fhirreference.FHIRReference, False, None, True),
            ("substitution", "substitution", MedicationKnowledgeRegulatorySubstitution, True, None, False),
            ("schedule", "schedule", MedicationKnowledgeRegulatorySchedule, True, None, False),
            ("maxDispense", "maxDispense", MedicationKnowledgeRegulatoryMaxDispense, False, None, False),
        ])
        return js


class MedicationKnowledgeRegulatoryMaxDispense(backboneelement.BackboneElement):
    """ The maximum number of units of the medication that can be dispensed in a
    period.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['quantity'] = """The maximum number of units of the medication that can be dispensed."""
    _attribute_docstrings['period'] = """The period that applies to the maximum number of units."""

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
        
        self.quantity = None
        """ The maximum number of units of the medication that can be dispensed.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.period = None
        """ The period that applies to the maximum number of units.
        Type `Duration` (represented as `dict` in JSON). """
        
        super(MedicationKnowledgeRegulatoryMaxDispense, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationKnowledgeRegulatoryMaxDispense, self).elementProperties()
        js.extend([
            ("quantity", "quantity", quantity.Quantity, False, None, True),
            ("period", "period", duration.Duration, False, None, False),
        ])
        return js


class MedicationKnowledgeRegulatorySchedule(backboneelement.BackboneElement):
    """ Specifies the schedule of a medication in jurisdiction.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['schedule'] = """Specifies the specific drug schedule."""

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
        
        self.schedule = None
        """ Specifies the specific drug schedule.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(MedicationKnowledgeRegulatorySchedule, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationKnowledgeRegulatorySchedule, self).elementProperties()
        js.extend([
            ("schedule", "schedule", codeableconcept.CodeableConcept, False, None, True),
        ])
        return js


class MedicationKnowledgeRegulatorySubstitution(backboneelement.BackboneElement):
    """ Specifies if changes are allowed when dispensing a medication from a
    regulatory perspective.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Specifies the type of substitution allowed."""
    _attribute_docstrings['allowed'] = """Specifies if regulation allows for changes in the medication when dispensing."""

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
        
        self.type = None
        """ Specifies the type of substitution allowed.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.allowed = None
        """ Specifies if regulation allows for changes in the medication when
        dispensing.
        Type `bool`. """
        
        super(MedicationKnowledgeRegulatorySubstitution, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationKnowledgeRegulatorySubstitution, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("allowed", "allowed", bool, False, None, True),
        ])
        return js


class MedicationKnowledgeRelatedMedicationKnowledge(backboneelement.BackboneElement):
    """ Associated or related medication information.
    
    Associated or related knowledge about a medication.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Category of medicationKnowledge."""
    _attribute_docstrings['reference'] = """Associated documentation about the associated medication knowledge."""

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
        
        self.type = None
        """ Category of medicationKnowledge.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.reference = None
        """ Associated documentation about the associated medication knowledge.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(MedicationKnowledgeRelatedMedicationKnowledge, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationKnowledgeRelatedMedicationKnowledge, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("reference", "reference", fhirreference.FHIRReference, True, None, True),
        ])
        return js


import sys
try:
    from . import codeableconcept
except ImportError:
    codeableconcept = sys.modules[__package__ + '.codeableconcept']
try:
    from . import dosage
except ImportError:
    dosage = sys.modules[__package__ + '.dosage']
try:
    from . import duration
except ImportError:
    duration = sys.modules[__package__ + '.duration']
try:
    from . import fhirreference
except ImportError:
    fhirreference = sys.modules[__package__ + '.fhirreference']
try:
    from . import money
except ImportError:
    money = sys.modules[__package__ + '.money']
try:
    from . import quantity
except ImportError:
    quantity = sys.modules[__package__ + '.quantity']
try:
    from . import ratio
except ImportError:
    ratio = sys.modules[__package__ + '.ratio']
