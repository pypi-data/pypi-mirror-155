#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Coverage) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Coverage(domainresource.DomainResource):
    """ Insurance or medical plan or a payment agreement.
    
    Financial instrument which may be used to reimburse or pay for health care
    products and services. Includes both insurance and self-payment.
    """
    
    resource_type = "Coverage"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business Identifier for the coverage."""
    _attribute_docstrings['status'] = """The status of the resource instance."""
    _attribute_docstrings['type'] = """Coverage category such as medical or accident."""
    _attribute_docstrings['policyHolder'] = """Owner of the policy."""
    _attribute_docstrings['subscriber'] = """Subscriber to the policy."""
    _attribute_docstrings['subscriberId'] = """ID assigned to the subscriber."""
    _attribute_docstrings['beneficiary'] = """Plan beneficiary."""
    _attribute_docstrings['dependent'] = """Dependent number."""
    _attribute_docstrings['relationship'] = """The relationship of beneficiary (patient) to the subscriber."""
    _attribute_docstrings['period'] = """Coverage start and end dates."""
    _attribute_docstrings['payor'] = """Issuer of the policy."""
    _attribute_docstrings['class_fhir'] = """Additional coverage classifications."""
    _attribute_docstrings['order'] = """Relative order of the coverage."""
    _attribute_docstrings['network'] = """Insurer network."""
    _attribute_docstrings['costToBeneficiary'] = """Patient payments for services/products."""
    _attribute_docstrings['subrogation'] = """Reimbursement to insurer."""
    _attribute_docstrings['contract'] = """Contract details."""

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
    _attribute_enums['relationship'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/subscriber-relationship',
        'restricted_to': ['child', 'parent', 'spouse', 'common', 'other', 'self', 'injured'],
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
        """ Business Identifier for the coverage.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ The status of the resource instance.
        Type `str`. """
        
        self.type = None
        """ Coverage category such as medical or accident.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.policyHolder = None
        """ Owner of the policy.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.subscriber = None
        """ Subscriber to the policy.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.subscriberId = None
        """ ID assigned to the subscriber.
        Type `str`. """
        
        self.beneficiary = None
        """ Plan beneficiary.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.dependent = None
        """ Dependent number.
        Type `str`. """
        
        self.relationship = None
        """ The relationship of beneficiary (patient) to the subscriber.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.period = None
        """ Coverage start and end dates.
        Type `Period` (represented as `dict` in JSON). """
        
        self.payor = None
        """ Issuer of the policy.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.class_fhir = None
        """ Additional coverage classifications.
        List of `CoverageClass` items (represented as `dict` in JSON). """
        
        self.order = None
        """ Relative order of the coverage.
        Type `int`. """
        
        self.network = None
        """ Insurer network.
        Type `str`. """
        
        self.costToBeneficiary = None
        """ Patient payments for services/products.
        List of `CoverageCostToBeneficiary` items (represented as `dict` in JSON). """
        
        self.subrogation = None
        """ Reimbursement to insurer.
        Type `bool`. """
        
        self.contract = None
        """ Contract details.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(Coverage, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Coverage, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("policyHolder", "policyHolder", fhirreference.FHIRReference, False, None, False),
            ("subscriber", "subscriber", fhirreference.FHIRReference, False, None, False),
            ("subscriberId", "subscriberId", str, False, None, False),
            ("beneficiary", "beneficiary", fhirreference.FHIRReference, False, None, True),
            ("dependent", "dependent", str, False, None, False),
            ("relationship", "relationship", codeableconcept.CodeableConcept, False, None, False),
            ("period", "period", period.Period, False, None, False),
            ("payor", "payor", fhirreference.FHIRReference, True, None, True),
            ("class_fhir", "class", CoverageClass, True, None, False),
            ("order", "order", int, False, None, False),
            ("network", "network", str, False, None, False),
            ("costToBeneficiary", "costToBeneficiary", CoverageCostToBeneficiary, True, None, False),
            ("subrogation", "subrogation", bool, False, None, False),
            ("contract", "contract", fhirreference.FHIRReference, True, None, False),
        ])
        return js


from . import backboneelement

class CoverageClass(backboneelement.BackboneElement):
    """ Additional coverage classifications.
    
    A suite of underwriter specific classifiers.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """The type of classification for which an insurer-specific class label or number and optional name is provided, for example may be used to identify a class of coverage or employer group, Policy, Plan."""
    _attribute_docstrings['value'] = """Value associated with the type."""
    _attribute_docstrings['name'] = """Human readable description of the type and value."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/coverage-class',
        'restricted_to': ['group', 'subgroup', 'plan', 'subplan', 'class', 'subclass', 'sequence', 'rxbin', 'rxpcn', 'rxid', 'rxgroup'],
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
        
        self.type = None
        """ The type of classification for which an insurer-specific class
        label or number and optional name is provided, for example may be
        used to identify a class of coverage or employer group, Policy,
        Plan.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.value = None
        """ Value associated with the type.
        Type `str`. """
        
        self.name = None
        """ Human readable description of the type and value.
        Type `str`. """
        
        super(CoverageClass, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CoverageClass, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("value", "value", str, False, None, True),
            ("name", "name", str, False, None, False),
        ])
        return js


class CoverageCostToBeneficiary(backboneelement.BackboneElement):
    """ Patient payments for services/products.
    
    A suite of codes indicating the cost category and associated amount which
    have been detailed in the policy and may have been  included on the health
    card.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """The category of patient centric costs associated with treatment."""
    _attribute_docstrings['valueQuantity'] = """The amount or percentage due from the beneficiary."""
    _attribute_docstrings['valueMoney'] = """The amount or percentage due from the beneficiary."""
    _attribute_docstrings['exception'] = """Exceptions for patient payments."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/coverage-copay-type',
        'restricted_to': ['gpvisit', 'spvisit', 'emergency', 'inpthosp', 'televisit', 'urgentcare', 'copaypct', 'copay', 'deductible', 'maxoutofpocket'],
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
        
        self.type = None
        """ The category of patient centric costs associated with treatment.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.valueQuantity = None
        """ The amount or percentage due from the beneficiary.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.valueMoney = None
        """ The amount or percentage due from the beneficiary.
        Type `Money` (represented as `dict` in JSON). """
        
        self.exception = None
        """ Exceptions for patient payments.
        List of `CoverageCostToBeneficiaryException` items (represented as `dict` in JSON). """
        
        super(CoverageCostToBeneficiary, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CoverageCostToBeneficiary, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("valueQuantity", "valueQuantity", quantity.Quantity, False, "value", True),
            ("valueMoney", "valueMoney", money.Money, False, "value", True),
            ("exception", "exception", CoverageCostToBeneficiaryException, True, None, False),
        ])
        return js


class CoverageCostToBeneficiaryException(backboneelement.BackboneElement):
    """ Exceptions for patient payments.
    
    A suite of codes indicating exceptions or reductions to patient costs and
    their effective periods.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """The code for the specific exception."""
    _attribute_docstrings['period'] = """The effective period of the exception."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/ex-coverage-financial-exception',
        'restricted_to': ['retired', 'foster'],
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
        """ The code for the specific exception.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.period = None
        """ The effective period of the exception.
        Type `Period` (represented as `dict` in JSON). """
        
        super(CoverageCostToBeneficiaryException, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CoverageCostToBeneficiaryException, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("period", "period", period.Period, False, None, False),
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
    from . import identifier
except ImportError:
    identifier = sys.modules[__package__ + '.identifier']
try:
    from . import money
except ImportError:
    money = sys.modules[__package__ + '.money']
try:
    from . import period
except ImportError:
    period = sys.modules[__package__ + '.period']
try:
    from . import quantity
except ImportError:
    quantity = sys.modules[__package__ + '.quantity']
