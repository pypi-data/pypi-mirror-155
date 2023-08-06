#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/InsurancePlan) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class InsurancePlan(domainresource.DomainResource):
    """ Details of a Health Insurance product/plan provided by an organization.
    """
    
    resource_type = "InsurancePlan"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business Identifier for Product."""
    _attribute_docstrings['status'] = """The current state of the health insurance product."""
    _attribute_docstrings['type'] = """Kind of product."""
    _attribute_docstrings['name'] = """Official name."""
    _attribute_docstrings['alias'] = """Alternate names."""
    _attribute_docstrings['period'] = """When the product is available."""
    _attribute_docstrings['ownedBy'] = """Plan issuer."""
    _attribute_docstrings['administeredBy'] = """Product administrator."""
    _attribute_docstrings['coverageArea'] = """Where product applies."""
    _attribute_docstrings['contact'] = """Contact for the product."""
    _attribute_docstrings['endpoint'] = """Technical endpoint."""
    _attribute_docstrings['network'] = """What networks are Included."""
    _attribute_docstrings['coverage'] = """Coverage details."""
    _attribute_docstrings['plan'] = """Plan details."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/publication-status',
        'restricted_to': ['draft', 'active', 'retired', 'unknown'],
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
        """ Business Identifier for Product.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ The current state of the health insurance product.
        Type `str`. """
        
        self.type = None
        """ Kind of product.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.name = None
        """ Official name.
        Type `str`. """
        
        self.alias = None
        """ Alternate names.
        List of `str` items. """
        
        self.period = None
        """ When the product is available.
        Type `Period` (represented as `dict` in JSON). """
        
        self.ownedBy = None
        """ Plan issuer.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.administeredBy = None
        """ Product administrator.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.coverageArea = None
        """ Where product applies.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.contact = None
        """ Contact for the product.
        List of `InsurancePlanContact` items (represented as `dict` in JSON). """
        
        self.endpoint = None
        """ Technical endpoint.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.network = None
        """ What networks are Included.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.coverage = None
        """ Coverage details.
        List of `InsurancePlanCoverage` items (represented as `dict` in JSON). """
        
        self.plan = None
        """ Plan details.
        List of `InsurancePlanPlan` items (represented as `dict` in JSON). """
        
        super(InsurancePlan, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(InsurancePlan, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, True, None, False),
            ("name", "name", str, False, None, False),
            ("alias", "alias", str, True, None, False),
            ("period", "period", period.Period, False, None, False),
            ("ownedBy", "ownedBy", fhirreference.FHIRReference, False, None, False),
            ("administeredBy", "administeredBy", fhirreference.FHIRReference, False, None, False),
            ("coverageArea", "coverageArea", fhirreference.FHIRReference, True, None, False),
            ("contact", "contact", InsurancePlanContact, True, None, False),
            ("endpoint", "endpoint", fhirreference.FHIRReference, True, None, False),
            ("network", "network", fhirreference.FHIRReference, True, None, False),
            ("coverage", "coverage", InsurancePlanCoverage, True, None, False),
            ("plan", "plan", InsurancePlanPlan, True, None, False),
        ])
        return js


from . import backboneelement

class InsurancePlanContact(backboneelement.BackboneElement):
    """ Contact for the product.
    
    The contact for the health insurance product for a certain purpose.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['purpose'] = """Indicates a purpose for which the contact can be reached."""
    _attribute_docstrings['name'] = """A name associated with the contact."""
    _attribute_docstrings['telecom'] = """Contact details (telephone, email, etc.)  for a contact."""
    _attribute_docstrings['address'] = """Visiting or postal addresses for the contact."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['purpose'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/contactentity-type',
        'restricted_to': ['BILL', 'ADMIN', 'HR', 'PAYOR', 'PATINF', 'PRESS'],
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
        
        self.purpose = None
        """ Indicates a purpose for which the contact can be reached.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.name = None
        """ A name associated with the contact.
        Type `HumanName` (represented as `dict` in JSON). """
        
        self.telecom = None
        """ Contact details (telephone, email, etc.)  for a contact.
        List of `ContactPoint` items (represented as `dict` in JSON). """
        
        self.address = None
        """ Visiting or postal addresses for the contact.
        Type `Address` (represented as `dict` in JSON). """
        
        super(InsurancePlanContact, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(InsurancePlanContact, self).elementProperties()
        js.extend([
            ("purpose", "purpose", codeableconcept.CodeableConcept, False, None, False),
            ("name", "name", humanname.HumanName, False, None, False),
            ("telecom", "telecom", contactpoint.ContactPoint, True, None, False),
            ("address", "address", address.Address, False, None, False),
        ])
        return js


class InsurancePlanCoverage(backboneelement.BackboneElement):
    """ Coverage details.
    
    Details about the coverage offered by the insurance product.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Type of coverage."""
    _attribute_docstrings['network'] = """What networks provide coverage."""
    _attribute_docstrings['benefit'] = """List of benefits."""

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
        """ Type of coverage.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.network = None
        """ What networks provide coverage.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.benefit = None
        """ List of benefits.
        List of `InsurancePlanCoverageBenefit` items (represented as `dict` in JSON). """
        
        super(InsurancePlanCoverage, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(InsurancePlanCoverage, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("network", "network", fhirreference.FHIRReference, True, None, False),
            ("benefit", "benefit", InsurancePlanCoverageBenefit, True, None, True),
        ])
        return js


class InsurancePlanCoverageBenefit(backboneelement.BackboneElement):
    """ List of benefits.
    
    Specific benefits under this type of coverage.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Type of benefit."""
    _attribute_docstrings['requirement'] = """Referral requirements."""
    _attribute_docstrings['limit'] = """Benefit limits."""

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
        """ Type of benefit.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.requirement = None
        """ Referral requirements.
        Type `str`. """
        
        self.limit = None
        """ Benefit limits.
        List of `InsurancePlanCoverageBenefitLimit` items (represented as `dict` in JSON). """
        
        super(InsurancePlanCoverageBenefit, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(InsurancePlanCoverageBenefit, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("requirement", "requirement", str, False, None, False),
            ("limit", "limit", InsurancePlanCoverageBenefitLimit, True, None, False),
        ])
        return js


class InsurancePlanCoverageBenefitLimit(backboneelement.BackboneElement):
    """ Benefit limits.
    
    The specific limits on the benefit.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['value'] = """Maximum value allowed."""
    _attribute_docstrings['code'] = """Benefit limit details."""

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
        
        self.value = None
        """ Maximum value allowed.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.code = None
        """ Benefit limit details.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(InsurancePlanCoverageBenefitLimit, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(InsurancePlanCoverageBenefitLimit, self).elementProperties()
        js.extend([
            ("value", "value", quantity.Quantity, False, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
        ])
        return js


class InsurancePlanPlan(backboneelement.BackboneElement):
    """ Plan details.
    
    Details about an insurance plan.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business Identifier for Product."""
    _attribute_docstrings['type'] = """Type of plan."""
    _attribute_docstrings['coverageArea'] = """Where product applies."""
    _attribute_docstrings['network'] = """What networks provide coverage."""
    _attribute_docstrings['generalCost'] = """Overall costs."""
    _attribute_docstrings['specificCost'] = """Specific costs."""

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
        """ Business Identifier for Product.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.type = None
        """ Type of plan.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.coverageArea = None
        """ Where product applies.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.network = None
        """ What networks provide coverage.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.generalCost = None
        """ Overall costs.
        List of `InsurancePlanPlanGeneralCost` items (represented as `dict` in JSON). """
        
        self.specificCost = None
        """ Specific costs.
        List of `InsurancePlanPlanSpecificCost` items (represented as `dict` in JSON). """
        
        super(InsurancePlanPlan, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(InsurancePlanPlan, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("coverageArea", "coverageArea", fhirreference.FHIRReference, True, None, False),
            ("network", "network", fhirreference.FHIRReference, True, None, False),
            ("generalCost", "generalCost", InsurancePlanPlanGeneralCost, True, None, False),
            ("specificCost", "specificCost", InsurancePlanPlanSpecificCost, True, None, False),
        ])
        return js


class InsurancePlanPlanGeneralCost(backboneelement.BackboneElement):
    """ Overall costs.
    
    Overall costs associated with the plan.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Type of cost."""
    _attribute_docstrings['groupSize'] = """Number of enrollees."""
    _attribute_docstrings['cost'] = """Cost value."""
    _attribute_docstrings['comment'] = """Additional cost information."""

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
        """ Type of cost.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.groupSize = None
        """ Number of enrollees.
        Type `int`. """
        
        self.cost = None
        """ Cost value.
        Type `Money` (represented as `dict` in JSON). """
        
        self.comment = None
        """ Additional cost information.
        Type `str`. """
        
        super(InsurancePlanPlanGeneralCost, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(InsurancePlanPlanGeneralCost, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("groupSize", "groupSize", int, False, None, False),
            ("cost", "cost", money.Money, False, None, False),
            ("comment", "comment", str, False, None, False),
        ])
        return js


class InsurancePlanPlanSpecificCost(backboneelement.BackboneElement):
    """ Specific costs.
    
    Costs associated with the coverage provided by the product.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['category'] = """General category of benefit."""
    _attribute_docstrings['benefit'] = """Benefits list."""

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
        
        self.category = None
        """ General category of benefit.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.benefit = None
        """ Benefits list.
        List of `InsurancePlanPlanSpecificCostBenefit` items (represented as `dict` in JSON). """
        
        super(InsurancePlanPlanSpecificCost, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(InsurancePlanPlanSpecificCost, self).elementProperties()
        js.extend([
            ("category", "category", codeableconcept.CodeableConcept, False, None, True),
            ("benefit", "benefit", InsurancePlanPlanSpecificCostBenefit, True, None, False),
        ])
        return js


class InsurancePlanPlanSpecificCostBenefit(backboneelement.BackboneElement):
    """ Benefits list.
    
    List of the specific benefits under this category of benefit.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Type of specific benefit."""
    _attribute_docstrings['cost'] = """List of the costs."""

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
        """ Type of specific benefit.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.cost = None
        """ List of the costs.
        List of `InsurancePlanPlanSpecificCostBenefitCost` items (represented as `dict` in JSON). """
        
        super(InsurancePlanPlanSpecificCostBenefit, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(InsurancePlanPlanSpecificCostBenefit, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("cost", "cost", InsurancePlanPlanSpecificCostBenefitCost, True, None, False),
        ])
        return js


class InsurancePlanPlanSpecificCostBenefitCost(backboneelement.BackboneElement):
    """ List of the costs.
    
    List of the costs associated with a specific benefit.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Type of cost."""
    _attribute_docstrings['applicability'] = """Whether the cost applies to in-network or out-of-network providers (in-network; out-of-network; other)."""
    _attribute_docstrings['qualifiers'] = """Additional information about the cost."""
    _attribute_docstrings['value'] = """The actual cost value."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['applicability'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/applicability',
        'restricted_to': ['in-network', 'out-of-network', 'other'],
        'binding_strength': 'required',
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
        """ Type of cost.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.applicability = None
        """ Whether the cost applies to in-network or out-of-network providers
        (in-network; out-of-network; other).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.qualifiers = None
        """ Additional information about the cost.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.value = None
        """ The actual cost value.
        Type `Quantity` (represented as `dict` in JSON). """
        
        super(InsurancePlanPlanSpecificCostBenefitCost, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(InsurancePlanPlanSpecificCostBenefitCost, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("applicability", "applicability", codeableconcept.CodeableConcept, False, None, False),
            ("qualifiers", "qualifiers", codeableconcept.CodeableConcept, True, None, False),
            ("value", "value", quantity.Quantity, False, None, False),
        ])
        return js


import sys
try:
    from . import address
except ImportError:
    address = sys.modules[__package__ + '.address']
try:
    from . import codeableconcept
except ImportError:
    codeableconcept = sys.modules[__package__ + '.codeableconcept']
try:
    from . import contactpoint
except ImportError:
    contactpoint = sys.modules[__package__ + '.contactpoint']
try:
    from . import fhirreference
except ImportError:
    fhirreference = sys.modules[__package__ + '.fhirreference']
try:
    from . import humanname
except ImportError:
    humanname = sys.modules[__package__ + '.humanname']
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
