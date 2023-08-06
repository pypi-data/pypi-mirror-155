#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/MedicinalProductPharmaceutical) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class MedicinalProductPharmaceutical(domainresource.DomainResource):
    """ A pharmaceutical product described in terms of its composition and dose
    form.
    """
    
    resource_type = "MedicinalProductPharmaceutical"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """An identifier for the pharmaceutical medicinal product."""
    _attribute_docstrings['administrableDoseForm'] = """The administrable dose form, after necessary reconstitution."""
    _attribute_docstrings['unitOfPresentation'] = """Todo."""
    _attribute_docstrings['ingredient'] = """Ingredient."""
    _attribute_docstrings['device'] = """Accompanying device."""
    _attribute_docstrings['characteristics'] = """Characteristics e.g. a products onset of action."""
    _attribute_docstrings['routeOfAdministration'] = """The path by which the pharmaceutical product is taken into or makes contact with the body."""

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
        """ An identifier for the pharmaceutical medicinal product.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.administrableDoseForm = None
        """ The administrable dose form, after necessary reconstitution.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.unitOfPresentation = None
        """ Todo.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.ingredient = None
        """ Ingredient.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.device = None
        """ Accompanying device.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.characteristics = None
        """ Characteristics e.g. a products onset of action.
        List of `MedicinalProductPharmaceuticalCharacteristics` items (represented as `dict` in JSON). """
        
        self.routeOfAdministration = None
        """ The path by which the pharmaceutical product is taken into or makes
        contact with the body.
        List of `MedicinalProductPharmaceuticalRouteOfAdministration` items (represented as `dict` in JSON). """
        
        super(MedicinalProductPharmaceutical, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicinalProductPharmaceutical, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("administrableDoseForm", "administrableDoseForm", codeableconcept.CodeableConcept, False, None, True),
            ("unitOfPresentation", "unitOfPresentation", codeableconcept.CodeableConcept, False, None, False),
            ("ingredient", "ingredient", fhirreference.FHIRReference, True, None, False),
            ("device", "device", fhirreference.FHIRReference, True, None, False),
            ("characteristics", "characteristics", MedicinalProductPharmaceuticalCharacteristics, True, None, False),
            ("routeOfAdministration", "routeOfAdministration", MedicinalProductPharmaceuticalRouteOfAdministration, True, None, True),
        ])
        return js


from . import backboneelement

class MedicinalProductPharmaceuticalCharacteristics(backboneelement.BackboneElement):
    """ Characteristics e.g. a products onset of action.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """A coded characteristic."""
    _attribute_docstrings['status'] = """The status of characteristic e.g. assigned or pending."""

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
        """ A coded characteristic.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.status = None
        """ The status of characteristic e.g. assigned or pending.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(MedicinalProductPharmaceuticalCharacteristics, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicinalProductPharmaceuticalCharacteristics, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, False, None, True),
            ("status", "status", codeableconcept.CodeableConcept, False, None, False),
        ])
        return js


class MedicinalProductPharmaceuticalRouteOfAdministration(backboneelement.BackboneElement):
    """ The path by which the pharmaceutical product is taken into or makes contact
    with the body.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Coded expression for the route."""
    _attribute_docstrings['firstDose'] = """The first dose (dose quantity) administered in humans can be specified, for a product under investigation, using a numerical value and its unit of measurement."""
    _attribute_docstrings['maxSingleDose'] = """The maximum single dose that can be administered as per the protocol of a clinical trial can be specified using a numerical value and its unit of measurement."""
    _attribute_docstrings['maxDosePerDay'] = """The maximum dose per day (maximum dose quantity to be administered in any one 24-h period) that can be administered as per the protocol referenced in the clinical trial authorisation."""
    _attribute_docstrings['maxDosePerTreatmentPeriod'] = """The maximum dose per treatment period that can be administered as per the protocol referenced in the clinical trial authorisation."""
    _attribute_docstrings['maxTreatmentPeriod'] = """The maximum treatment period during which an Investigational Medicinal Product can be administered as per the protocol referenced in the clinical trial authorisation."""
    _attribute_docstrings['targetSpecies'] = """A species for which this route applies."""

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
        """ Coded expression for the route.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.firstDose = None
        """ The first dose (dose quantity) administered in humans can be
        specified, for a product under investigation, using a numerical
        value and its unit of measurement.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.maxSingleDose = None
        """ The maximum single dose that can be administered as per the
        protocol of a clinical trial can be specified using a numerical
        value and its unit of measurement.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.maxDosePerDay = None
        """ The maximum dose per day (maximum dose quantity to be administered
        in any one 24-h period) that can be administered as per the
        protocol referenced in the clinical trial authorisation.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.maxDosePerTreatmentPeriod = None
        """ The maximum dose per treatment period that can be administered as
        per the protocol referenced in the clinical trial authorisation.
        Type `Ratio` (represented as `dict` in JSON). """
        
        self.maxTreatmentPeriod = None
        """ The maximum treatment period during which an Investigational
        Medicinal Product can be administered as per the protocol
        referenced in the clinical trial authorisation.
        Type `Duration` (represented as `dict` in JSON). """
        
        self.targetSpecies = None
        """ A species for which this route applies.
        List of `MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies` items (represented as `dict` in JSON). """
        
        super(MedicinalProductPharmaceuticalRouteOfAdministration, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicinalProductPharmaceuticalRouteOfAdministration, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, False, None, True),
            ("firstDose", "firstDose", quantity.Quantity, False, None, False),
            ("maxSingleDose", "maxSingleDose", quantity.Quantity, False, None, False),
            ("maxDosePerDay", "maxDosePerDay", quantity.Quantity, False, None, False),
            ("maxDosePerTreatmentPeriod", "maxDosePerTreatmentPeriod", ratio.Ratio, False, None, False),
            ("maxTreatmentPeriod", "maxTreatmentPeriod", duration.Duration, False, None, False),
            ("targetSpecies", "targetSpecies", MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies, True, None, False),
        ])
        return js


class MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies(backboneelement.BackboneElement):
    """ A species for which this route applies.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Coded expression for the species."""
    _attribute_docstrings['withdrawalPeriod'] = """A species specific time during which consumption of animal product is not appropriate."""

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
        """ Coded expression for the species.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.withdrawalPeriod = None
        """ A species specific time during which consumption of animal product
        is not appropriate.
        List of `MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod` items (represented as `dict` in JSON). """
        
        super(MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, False, None, True),
            ("withdrawalPeriod", "withdrawalPeriod", MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod, True, None, False),
        ])
        return js


class MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod(backboneelement.BackboneElement):
    """ A species specific time during which consumption of animal product is not
    appropriate.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['tissue'] = """Coded expression for the type of tissue for which the withdrawal period applues, e.g. meat, milk."""
    _attribute_docstrings['value'] = """A value for the time."""
    _attribute_docstrings['supportingInformation'] = """Extra information about the withdrawal period."""

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
        
        self.tissue = None
        """ Coded expression for the type of tissue for which the withdrawal
        period applues, e.g. meat, milk.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.value = None
        """ A value for the time.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.supportingInformation = None
        """ Extra information about the withdrawal period.
        Type `str`. """
        
        super(MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod, self).elementProperties()
        js.extend([
            ("tissue", "tissue", codeableconcept.CodeableConcept, False, None, True),
            ("value", "value", quantity.Quantity, False, None, True),
            ("supportingInformation", "supportingInformation", str, False, None, False),
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
    from . import ratio
except ImportError:
    ratio = sys.modules[__package__ + '.ratio']
