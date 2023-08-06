#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/CoverageEligibilityRequest) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class CoverageEligibilityRequest(domainresource.DomainResource):
    """ CoverageEligibilityRequest resource.
    
    The CoverageEligibilityRequest provides patient and insurance coverage
    information to an insurer for them to respond, in the form of an
    CoverageEligibilityResponse, with information regarding whether the stated
    coverage is valid and in-force and optionally to provide the insurance
    details of the policy.
    """
    
    resource_type = "CoverageEligibilityRequest"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business Identifier for coverage eligiblity request."""
    _attribute_docstrings['status'] = """The status of the resource instance."""
    _attribute_docstrings['priority'] = """When the requestor expects the processor to complete processing."""
    _attribute_docstrings['purpose'] = """Code to specify whether requesting: prior authorization requirements for some service categories or billing codes; benefits for coverages specified or discovered; discovery and return of coverages for the patient; and/or validation that the specified coverage is in-force at the date/period specified or 'now' if not specified."""
    _attribute_docstrings['patient'] = """Intended recipient of products and services."""
    _attribute_docstrings['servicedDate'] = """Estimated date or dates of service."""
    _attribute_docstrings['servicedPeriod'] = """Estimated date or dates of service."""
    _attribute_docstrings['created'] = """Creation date."""
    _attribute_docstrings['enterer'] = """Author."""
    _attribute_docstrings['provider'] = """Party responsible for the request."""
    _attribute_docstrings['insurer'] = """Coverage issuer."""
    _attribute_docstrings['facility'] = """Servicing facility."""
    _attribute_docstrings['supportingInfo'] = """Supporting information."""
    _attribute_docstrings['insurance'] = """Patient insurance information."""
    _attribute_docstrings['item'] = """Item to be evaluated for eligibiity."""

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
    _attribute_enums['priority'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/processpriority',
        'restricted_to': ['stat', 'normal', 'deferred'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['purpose'] = {
        'url': 'http://hl7.org/fhir/eligibilityrequest-purpose',
        'restricted_to': ['auth-requirements', 'benefits', 'discovery', 'validation'],
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
        """ Business Identifier for coverage eligiblity request.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ The status of the resource instance.
        Type `str`. """
        
        self.priority = None
        """ When the requestor expects the processor to complete processing.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.purpose = None
        """ Code to specify whether requesting: prior authorization
        requirements for some service categories or billing codes; benefits
        for coverages specified or discovered; discovery and return of
        coverages for the patient; and/or validation that the specified
        coverage is in-force at the date/period specified or 'now' if not
        specified.
        List of `str` items. """
        
        self.patient = None
        """ Intended recipient of products and services.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.servicedDate = None
        """ Estimated date or dates of service.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.servicedPeriod = None
        """ Estimated date or dates of service.
        Type `Period` (represented as `dict` in JSON). """
        
        self.created = None
        """ Creation date.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.enterer = None
        """ Author.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.provider = None
        """ Party responsible for the request.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.insurer = None
        """ Coverage issuer.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.facility = None
        """ Servicing facility.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.supportingInfo = None
        """ Supporting information.
        List of `CoverageEligibilityRequestSupportingInfo` items (represented as `dict` in JSON). """
        
        self.insurance = None
        """ Patient insurance information.
        List of `CoverageEligibilityRequestInsurance` items (represented as `dict` in JSON). """
        
        self.item = None
        """ Item to be evaluated for eligibiity.
        List of `CoverageEligibilityRequestItem` items (represented as `dict` in JSON). """
        
        super(CoverageEligibilityRequest, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CoverageEligibilityRequest, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("priority", "priority", codeableconcept.CodeableConcept, False, None, False),
            ("purpose", "purpose", str, True, None, True),
            ("patient", "patient", fhirreference.FHIRReference, False, None, True),
            ("servicedDate", "servicedDate", fhirdate.FHIRDate, False, "serviced", False),
            ("servicedPeriod", "servicedPeriod", period.Period, False, "serviced", False),
            ("created", "created", fhirdate.FHIRDate, False, None, True),
            ("enterer", "enterer", fhirreference.FHIRReference, False, None, False),
            ("provider", "provider", fhirreference.FHIRReference, False, None, False),
            ("insurer", "insurer", fhirreference.FHIRReference, False, None, True),
            ("facility", "facility", fhirreference.FHIRReference, False, None, False),
            ("supportingInfo", "supportingInfo", CoverageEligibilityRequestSupportingInfo, True, None, False),
            ("insurance", "insurance", CoverageEligibilityRequestInsurance, True, None, False),
            ("item", "item", CoverageEligibilityRequestItem, True, None, False),
        ])
        return js


from . import backboneelement

class CoverageEligibilityRequestInsurance(backboneelement.BackboneElement):
    """ Patient insurance information.
    
    Financial instruments for reimbursement for the health care products and
    services.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['focal'] = """Applicable coverage."""
    _attribute_docstrings['coverage'] = """Insurance information."""
    _attribute_docstrings['businessArrangement'] = """Additional provider contract number."""

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
        
        self.focal = None
        """ Applicable coverage.
        Type `bool`. """
        
        self.coverage = None
        """ Insurance information.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.businessArrangement = None
        """ Additional provider contract number.
        Type `str`. """
        
        super(CoverageEligibilityRequestInsurance, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CoverageEligibilityRequestInsurance, self).elementProperties()
        js.extend([
            ("focal", "focal", bool, False, None, False),
            ("coverage", "coverage", fhirreference.FHIRReference, False, None, True),
            ("businessArrangement", "businessArrangement", str, False, None, False),
        ])
        return js


class CoverageEligibilityRequestItem(backboneelement.BackboneElement):
    """ Item to be evaluated for eligibiity.
    
    Service categories or billable services for which benefit details and/or an
    authorization prior to service delivery may be required by the payor.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['supportingInfoSequence'] = """Applicable exception or supporting information."""
    _attribute_docstrings['category'] = """Benefit classification."""
    _attribute_docstrings['productOrService'] = """Billing, service, product, or drug code."""
    _attribute_docstrings['modifier'] = """Item typification or modifiers codes to convey additional context for the product or service."""
    _attribute_docstrings['provider'] = """Perfoming practitioner."""
    _attribute_docstrings['quantity'] = """Count of products or services."""
    _attribute_docstrings['unitPrice'] = """Fee, charge or cost per item."""
    _attribute_docstrings['facility'] = """Servicing facility."""
    _attribute_docstrings['diagnosis'] = """Applicable diagnosis."""
    _attribute_docstrings['detail'] = """Product or service details."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['modifier'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/modifiers',
        'restricted_to': ['a', 'b', 'c', 'e', 'rooh', 'x'],
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
        
        self.supportingInfoSequence = None
        """ Applicable exception or supporting information.
        List of `int` items. """
        
        self.category = None
        """ Benefit classification.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.productOrService = None
        """ Billing, service, product, or drug code.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.modifier = None
        """ Item typification or modifiers codes to convey additional context
        for the product or service.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.provider = None
        """ Perfoming practitioner.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.quantity = None
        """ Count of products or services.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.unitPrice = None
        """ Fee, charge or cost per item.
        Type `Money` (represented as `dict` in JSON). """
        
        self.facility = None
        """ Servicing facility.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.diagnosis = None
        """ Applicable diagnosis.
        List of `CoverageEligibilityRequestItemDiagnosis` items (represented as `dict` in JSON). """
        
        self.detail = None
        """ Product or service details.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(CoverageEligibilityRequestItem, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CoverageEligibilityRequestItem, self).elementProperties()
        js.extend([
            ("supportingInfoSequence", "supportingInfoSequence", int, True, None, False),
            ("category", "category", codeableconcept.CodeableConcept, False, None, False),
            ("productOrService", "productOrService", codeableconcept.CodeableConcept, False, None, False),
            ("modifier", "modifier", codeableconcept.CodeableConcept, True, None, False),
            ("provider", "provider", fhirreference.FHIRReference, False, None, False),
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("unitPrice", "unitPrice", money.Money, False, None, False),
            ("facility", "facility", fhirreference.FHIRReference, False, None, False),
            ("diagnosis", "diagnosis", CoverageEligibilityRequestItemDiagnosis, True, None, False),
            ("detail", "detail", fhirreference.FHIRReference, True, None, False),
        ])
        return js


class CoverageEligibilityRequestItemDiagnosis(backboneelement.BackboneElement):
    """ Applicable diagnosis.
    
    Patient diagnosis for which care is sought.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['diagnosisCodeableConcept'] = """Nature of illness or problem."""
    _attribute_docstrings['diagnosisReference'] = """Nature of illness or problem."""

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
        
        self.diagnosisCodeableConcept = None
        """ Nature of illness or problem.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.diagnosisReference = None
        """ Nature of illness or problem.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(CoverageEligibilityRequestItemDiagnosis, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CoverageEligibilityRequestItemDiagnosis, self).elementProperties()
        js.extend([
            ("diagnosisCodeableConcept", "diagnosisCodeableConcept", codeableconcept.CodeableConcept, False, "diagnosis", False),
            ("diagnosisReference", "diagnosisReference", fhirreference.FHIRReference, False, "diagnosis", False),
        ])
        return js


class CoverageEligibilityRequestSupportingInfo(backboneelement.BackboneElement):
    """ Supporting information.
    
    Additional information codes regarding exceptions, special considerations,
    the condition, situation, prior or concurrent issues.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['sequence'] = """Information instance identifier."""
    _attribute_docstrings['information'] = """Data to be provided."""
    _attribute_docstrings['appliesToAll'] = """Applies to all items."""

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
        
        self.sequence = None
        """ Information instance identifier.
        Type `int`. """
        
        self.information = None
        """ Data to be provided.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.appliesToAll = None
        """ Applies to all items.
        Type `bool`. """
        
        super(CoverageEligibilityRequestSupportingInfo, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CoverageEligibilityRequestSupportingInfo, self).elementProperties()
        js.extend([
            ("sequence", "sequence", int, False, None, True),
            ("information", "information", fhirreference.FHIRReference, False, None, True),
            ("appliesToAll", "appliesToAll", bool, False, None, False),
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
