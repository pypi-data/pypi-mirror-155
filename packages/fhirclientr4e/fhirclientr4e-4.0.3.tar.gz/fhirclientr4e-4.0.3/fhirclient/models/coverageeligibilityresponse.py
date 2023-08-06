#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/CoverageEligibilityResponse) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class CoverageEligibilityResponse(domainresource.DomainResource):
    """ CoverageEligibilityResponse resource.
    
    This resource provides eligibility and plan details from the processing of
    an CoverageEligibilityRequest resource.
    """
    
    resource_type = "CoverageEligibilityResponse"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business Identifier for coverage eligiblity request."""
    _attribute_docstrings['status'] = """The status of the resource instance."""
    _attribute_docstrings['purpose'] = """Code to specify whether requesting: prior authorization requirements for some service categories or billing codes; benefits for coverages specified or discovered; discovery and return of coverages for the patient; and/or validation that the specified coverage is in-force at the date/period specified or 'now' if not specified."""
    _attribute_docstrings['patient'] = """Intended recipient of products and services."""
    _attribute_docstrings['servicedDate'] = """Estimated date or dates of service."""
    _attribute_docstrings['servicedPeriod'] = """Estimated date or dates of service."""
    _attribute_docstrings['created'] = """Response creation date."""
    _attribute_docstrings['requestor'] = """Party responsible for the request."""
    _attribute_docstrings['request'] = """Eligibility request reference."""
    _attribute_docstrings['outcome'] = """The outcome of the request processing."""
    _attribute_docstrings['disposition'] = """Disposition Message."""
    _attribute_docstrings['insurer'] = """Coverage issuer."""
    _attribute_docstrings['insurance'] = """Patient insurance information."""
    _attribute_docstrings['preAuthRef'] = """Preauthorization reference."""
    _attribute_docstrings['form'] = """Printed form identifier."""
    _attribute_docstrings['error'] = """Processing errors."""

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
    _attribute_enums['purpose'] = {
        'url': 'http://hl7.org/fhir/eligibilityresponse-purpose',
        'restricted_to': ['auth-requirements', 'benefits', 'discovery', 'validation'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['outcome'] = {
        'url': 'http://hl7.org/fhir/remittance-outcome',
        'restricted_to': ['queued', 'complete', 'error', 'partial'],
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
        """ Response creation date.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.requestor = None
        """ Party responsible for the request.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.request = None
        """ Eligibility request reference.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.outcome = None
        """ The outcome of the request processing.
        Type `str`. """
        
        self.disposition = None
        """ Disposition Message.
        Type `str`. """
        
        self.insurer = None
        """ Coverage issuer.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.insurance = None
        """ Patient insurance information.
        List of `CoverageEligibilityResponseInsurance` items (represented as `dict` in JSON). """
        
        self.preAuthRef = None
        """ Preauthorization reference.
        Type `str`. """
        
        self.form = None
        """ Printed form identifier.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.error = None
        """ Processing errors.
        List of `CoverageEligibilityResponseError` items (represented as `dict` in JSON). """
        
        super(CoverageEligibilityResponse, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CoverageEligibilityResponse, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("purpose", "purpose", str, True, None, True),
            ("patient", "patient", fhirreference.FHIRReference, False, None, True),
            ("servicedDate", "servicedDate", fhirdate.FHIRDate, False, "serviced", False),
            ("servicedPeriod", "servicedPeriod", period.Period, False, "serviced", False),
            ("created", "created", fhirdate.FHIRDate, False, None, True),
            ("requestor", "requestor", fhirreference.FHIRReference, False, None, False),
            ("request", "request", fhirreference.FHIRReference, False, None, True),
            ("outcome", "outcome", str, False, None, True),
            ("disposition", "disposition", str, False, None, False),
            ("insurer", "insurer", fhirreference.FHIRReference, False, None, True),
            ("insurance", "insurance", CoverageEligibilityResponseInsurance, True, None, False),
            ("preAuthRef", "preAuthRef", str, False, None, False),
            ("form", "form", codeableconcept.CodeableConcept, False, None, False),
            ("error", "error", CoverageEligibilityResponseError, True, None, False),
        ])
        return js


from . import backboneelement

class CoverageEligibilityResponseError(backboneelement.BackboneElement):
    """ Processing errors.
    
    Errors encountered during the processing of the request.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Error code detailing processing issues."""

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
        """ Error code detailing processing issues.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(CoverageEligibilityResponseError, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CoverageEligibilityResponseError, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, False, None, True),
        ])
        return js


class CoverageEligibilityResponseInsurance(backboneelement.BackboneElement):
    """ Patient insurance information.
    
    Financial instruments for reimbursement for the health care products and
    services.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['coverage'] = """Insurance information."""
    _attribute_docstrings['inforce'] = """Coverage inforce indicator."""
    _attribute_docstrings['benefitPeriod'] = """When the benefits are applicable."""
    _attribute_docstrings['item'] = """Benefits and authorization details."""

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
        
        self.coverage = None
        """ Insurance information.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.inforce = None
        """ Coverage inforce indicator.
        Type `bool`. """
        
        self.benefitPeriod = None
        """ When the benefits are applicable.
        Type `Period` (represented as `dict` in JSON). """
        
        self.item = None
        """ Benefits and authorization details.
        List of `CoverageEligibilityResponseInsuranceItem` items (represented as `dict` in JSON). """
        
        super(CoverageEligibilityResponseInsurance, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CoverageEligibilityResponseInsurance, self).elementProperties()
        js.extend([
            ("coverage", "coverage", fhirreference.FHIRReference, False, None, True),
            ("inforce", "inforce", bool, False, None, False),
            ("benefitPeriod", "benefitPeriod", period.Period, False, None, False),
            ("item", "item", CoverageEligibilityResponseInsuranceItem, True, None, False),
        ])
        return js


class CoverageEligibilityResponseInsuranceItem(backboneelement.BackboneElement):
    """ Benefits and authorization details.
    
    Benefits and optionally current balances, and authorization details by
    category or service.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['category'] = """Benefit classification."""
    _attribute_docstrings['productOrService'] = """Billing, service, product, or drug code."""
    _attribute_docstrings['modifier'] = """Item typification or modifiers codes to convey additional context for the product or service."""
    _attribute_docstrings['provider'] = """Performing practitioner."""
    _attribute_docstrings['excluded'] = """Excluded from the plan."""
    _attribute_docstrings['name'] = """Short name for the benefit."""
    _attribute_docstrings['description'] = """Description of the benefit or services covered."""
    _attribute_docstrings['network'] = """Is a flag to indicate whether the benefits refer to in-network providers or out-of-network providers."""
    _attribute_docstrings['unit'] = """Indicates if the benefits apply to an individual or to the family."""
    _attribute_docstrings['term'] = """The term or period of the values such as 'maximum lifetime benefit' or 'maximum annual visits'."""
    _attribute_docstrings['benefit'] = """Benefit Summary."""
    _attribute_docstrings['authorizationRequired'] = """Authorization required flag."""
    _attribute_docstrings['authorizationSupporting'] = """Codes or comments regarding information or actions associated with the preauthorization."""
    _attribute_docstrings['authorizationUrl'] = """Preauthorization requirements endpoint."""

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
    _attribute_enums['network'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/benefit-network',
        'restricted_to': ['in', 'out'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['unit'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/benefit-unit',
        'restricted_to': ['individual', 'family'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['term'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/benefit-term',
        'restricted_to': ['annual', 'day', 'lifetime'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['authorizationSupporting'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/coverageeligibilityresponse-ex-auth-support',
        'restricted_to': ['laborder', 'labreport', 'diagnosticimageorder', 'diagnosticimagereport', 'professionalreport', 'accidentreport', 'model', 'picture'],
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
        """ Performing practitioner.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.excluded = None
        """ Excluded from the plan.
        Type `bool`. """
        
        self.name = None
        """ Short name for the benefit.
        Type `str`. """
        
        self.description = None
        """ Description of the benefit or services covered.
        Type `str`. """
        
        self.network = None
        """ Is a flag to indicate whether the benefits refer to in-network
        providers or out-of-network providers.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.unit = None
        """ Indicates if the benefits apply to an individual or to the family.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.term = None
        """ The term or period of the values such as 'maximum lifetime benefit'
        or 'maximum annual visits'.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.benefit = None
        """ Benefit Summary.
        List of `CoverageEligibilityResponseInsuranceItemBenefit` items (represented as `dict` in JSON). """
        
        self.authorizationRequired = None
        """ Authorization required flag.
        Type `bool`. """
        
        self.authorizationSupporting = None
        """ Codes or comments regarding information or actions associated with
        the preauthorization.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.authorizationUrl = None
        """ Preauthorization requirements endpoint.
        Type `str`. """
        
        super(CoverageEligibilityResponseInsuranceItem, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CoverageEligibilityResponseInsuranceItem, self).elementProperties()
        js.extend([
            ("category", "category", codeableconcept.CodeableConcept, False, None, False),
            ("productOrService", "productOrService", codeableconcept.CodeableConcept, False, None, False),
            ("modifier", "modifier", codeableconcept.CodeableConcept, True, None, False),
            ("provider", "provider", fhirreference.FHIRReference, False, None, False),
            ("excluded", "excluded", bool, False, None, False),
            ("name", "name", str, False, None, False),
            ("description", "description", str, False, None, False),
            ("network", "network", codeableconcept.CodeableConcept, False, None, False),
            ("unit", "unit", codeableconcept.CodeableConcept, False, None, False),
            ("term", "term", codeableconcept.CodeableConcept, False, None, False),
            ("benefit", "benefit", CoverageEligibilityResponseInsuranceItemBenefit, True, None, False),
            ("authorizationRequired", "authorizationRequired", bool, False, None, False),
            ("authorizationSupporting", "authorizationSupporting", codeableconcept.CodeableConcept, True, None, False),
            ("authorizationUrl", "authorizationUrl", str, False, None, False),
        ])
        return js


class CoverageEligibilityResponseInsuranceItemBenefit(backboneelement.BackboneElement):
    """ Benefit Summary.
    
    Benefits used to date.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Classification of benefit being provided."""
    _attribute_docstrings['allowedUnsignedInt'] = """Benefits allowed."""
    _attribute_docstrings['allowedString'] = """Benefits allowed."""
    _attribute_docstrings['allowedMoney'] = """Benefits allowed."""
    _attribute_docstrings['usedUnsignedInt'] = """Benefits used."""
    _attribute_docstrings['usedString'] = """Benefits used."""
    _attribute_docstrings['usedMoney'] = """Benefits used."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/benefit-type',
        'restricted_to': ['benefit', 'deductible', 'visit', 'room', 'copay', 'copay-percent', 'copay-maximum', 'vision-exam', 'vision-glasses', 'vision-contacts', 'medical-primarycare', 'pharmacy-dispense'],
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
        """ Classification of benefit being provided.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.allowedUnsignedInt = None
        """ Benefits allowed.
        Type `int`. """
        
        self.allowedString = None
        """ Benefits allowed.
        Type `str`. """
        
        self.allowedMoney = None
        """ Benefits allowed.
        Type `Money` (represented as `dict` in JSON). """
        
        self.usedUnsignedInt = None
        """ Benefits used.
        Type `int`. """
        
        self.usedString = None
        """ Benefits used.
        Type `str`. """
        
        self.usedMoney = None
        """ Benefits used.
        Type `Money` (represented as `dict` in JSON). """
        
        super(CoverageEligibilityResponseInsuranceItemBenefit, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CoverageEligibilityResponseInsuranceItemBenefit, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("allowedUnsignedInt", "allowedUnsignedInt", int, False, "allowed", False),
            ("allowedString", "allowedString", str, False, "allowed", False),
            ("allowedMoney", "allowedMoney", money.Money, False, "allowed", False),
            ("usedUnsignedInt", "usedUnsignedInt", int, False, "used", False),
            ("usedString", "usedString", str, False, "used", False),
            ("usedMoney", "usedMoney", money.Money, False, "used", False),
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
