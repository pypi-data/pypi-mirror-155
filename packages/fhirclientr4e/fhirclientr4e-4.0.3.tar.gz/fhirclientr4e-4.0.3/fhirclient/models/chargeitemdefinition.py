#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/ChargeItemDefinition) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class ChargeItemDefinition(domainresource.DomainResource):
    """ Definition of properties and rules about how the price and the
    applicability of a ChargeItem can be determined.
    
    The ChargeItemDefinition resource provides the properties that apply to the
    (billing) codes necessary to calculate costs and prices. The properties may
    differ largely depending on type and realm, therefore this resource gives
    only a rough structure and requires profiling for each type of billing code
    system.
    """
    
    resource_type = "ChargeItemDefinition"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['url'] = """Canonical identifier for this charge item definition, represented as a URI (globally unique)."""
    _attribute_docstrings['identifier'] = """Additional identifier for the charge item definition."""
    _attribute_docstrings['version'] = """Business version of the charge item definition."""
    _attribute_docstrings['title'] = """Name for this charge item definition (human friendly)."""
    _attribute_docstrings['derivedFromUri'] = """Underlying externally-defined charge item definition."""
    _attribute_docstrings['partOf'] = """A larger definition of which this particular definition is a component or step."""
    _attribute_docstrings['replaces'] = """Completed or terminated request(s) whose function is taken by this new request."""
    _attribute_docstrings['status'] = """The current state of the ChargeItemDefinition."""
    _attribute_docstrings['experimental'] = """For testing purposes, not real usage."""
    _attribute_docstrings['date'] = """Date last changed."""
    _attribute_docstrings['publisher'] = """Name of the publisher (organization or individual)."""
    _attribute_docstrings['contact'] = """Contact details for the publisher."""
    _attribute_docstrings['description'] = """Natural language description of the charge item definition."""
    _attribute_docstrings['useContext'] = """The context that the content is intended to support."""
    _attribute_docstrings['jurisdiction'] = """Intended jurisdiction for charge item definition (if applicable)."""
    _attribute_docstrings['copyright'] = """Use and/or publishing restrictions."""
    _attribute_docstrings['approvalDate'] = """When the charge item definition was approved by publisher."""
    _attribute_docstrings['lastReviewDate'] = """When the charge item definition was last reviewed."""
    _attribute_docstrings['effectivePeriod'] = """When the charge item definition is expected to be used."""
    _attribute_docstrings['code'] = """Billing codes or product types this definition applies to."""
    _attribute_docstrings['instance'] = """Instances this definition applies to."""
    _attribute_docstrings['applicability'] = """Whether or not the billing code is applicable."""
    _attribute_docstrings['propertyGroup'] = """Group of properties which are applicable under the same conditions."""

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
        
        self.url = None
        """ Canonical identifier for this charge item definition, represented
        as a URI (globally unique).
        Type `str`. """
        
        self.identifier = None
        """ Additional identifier for the charge item definition.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.version = None
        """ Business version of the charge item definition.
        Type `str`. """
        
        self.title = None
        """ Name for this charge item definition (human friendly).
        Type `str`. """
        
        self.derivedFromUri = None
        """ Underlying externally-defined charge item definition.
        List of `str` items. """
        
        self.partOf = None
        """ A larger definition of which this particular definition is a
        component or step.
        List of `str` items. """
        
        self.replaces = None
        """ Completed or terminated request(s) whose function is taken by this
        new request.
        List of `str` items. """
        
        self.status = None
        """ The current state of the ChargeItemDefinition.
        Type `str`. """
        
        self.experimental = None
        """ For testing purposes, not real usage.
        Type `bool`. """
        
        self.date = None
        """ Date last changed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.publisher = None
        """ Name of the publisher (organization or individual).
        Type `str`. """
        
        self.contact = None
        """ Contact details for the publisher.
        List of `ContactDetail` items (represented as `dict` in JSON). """
        
        self.description = None
        """ Natural language description of the charge item definition.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for charge item definition (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.copyright = None
        """ Use and/or publishing restrictions.
        Type `str`. """
        
        self.approvalDate = None
        """ When the charge item definition was approved by publisher.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.lastReviewDate = None
        """ When the charge item definition was last reviewed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.effectivePeriod = None
        """ When the charge item definition is expected to be used.
        Type `Period` (represented as `dict` in JSON). """
        
        self.code = None
        """ Billing codes or product types this definition applies to.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.instance = None
        """ Instances this definition applies to.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.applicability = None
        """ Whether or not the billing code is applicable.
        List of `ChargeItemDefinitionApplicability` items (represented as `dict` in JSON). """
        
        self.propertyGroup = None
        """ Group of properties which are applicable under the same conditions.
        List of `ChargeItemDefinitionPropertyGroup` items (represented as `dict` in JSON). """
        
        super(ChargeItemDefinition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ChargeItemDefinition, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, True),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("version", "version", str, False, None, False),
            ("title", "title", str, False, None, False),
            ("derivedFromUri", "derivedFromUri", str, True, None, False),
            ("partOf", "partOf", str, True, None, False),
            ("replaces", "replaces", str, True, None, False),
            ("status", "status", str, False, None, True),
            ("experimental", "experimental", bool, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("publisher", "publisher", str, False, None, False),
            ("contact", "contact", contactdetail.ContactDetail, True, None, False),
            ("description", "description", str, False, None, False),
            ("useContext", "useContext", usagecontext.UsageContext, True, None, False),
            ("jurisdiction", "jurisdiction", codeableconcept.CodeableConcept, True, None, False),
            ("copyright", "copyright", str, False, None, False),
            ("approvalDate", "approvalDate", fhirdate.FHIRDate, False, None, False),
            ("lastReviewDate", "lastReviewDate", fhirdate.FHIRDate, False, None, False),
            ("effectivePeriod", "effectivePeriod", period.Period, False, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("instance", "instance", fhirreference.FHIRReference, True, None, False),
            ("applicability", "applicability", ChargeItemDefinitionApplicability, True, None, False),
            ("propertyGroup", "propertyGroup", ChargeItemDefinitionPropertyGroup, True, None, False),
        ])
        return js


from . import backboneelement

class ChargeItemDefinitionApplicability(backboneelement.BackboneElement):
    """ Whether or not the billing code is applicable.
    
    Expressions that describe applicability criteria for the billing code.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['description'] = """Natural language description of the condition."""
    _attribute_docstrings['language'] = """Language of the expression."""
    _attribute_docstrings['expression'] = """Boolean-valued expression."""

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
        """ Natural language description of the condition.
        Type `str`. """
        
        self.language = None
        """ Language of the expression.
        Type `str`. """
        
        self.expression = None
        """ Boolean-valued expression.
        Type `str`. """
        
        super(ChargeItemDefinitionApplicability, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ChargeItemDefinitionApplicability, self).elementProperties()
        js.extend([
            ("description", "description", str, False, None, False),
            ("language", "language", str, False, None, False),
            ("expression", "expression", str, False, None, False),
        ])
        return js


class ChargeItemDefinitionPropertyGroup(backboneelement.BackboneElement):
    """ Group of properties which are applicable under the same conditions.
    
    Group of properties which are applicable under the same conditions. If no
    applicability rules are established for the group, then all properties
    always apply.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['applicability'] = """Conditions under which the priceComponent is applicable."""
    _attribute_docstrings['priceComponent'] = """Components of total line item price."""

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
        
        self.applicability = None
        """ Conditions under which the priceComponent is applicable.
        List of `ChargeItemDefinitionApplicability` items (represented as `dict` in JSON). """
        
        self.priceComponent = None
        """ Components of total line item price.
        List of `ChargeItemDefinitionPropertyGroupPriceComponent` items (represented as `dict` in JSON). """
        
        super(ChargeItemDefinitionPropertyGroup, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ChargeItemDefinitionPropertyGroup, self).elementProperties()
        js.extend([
            ("applicability", "applicability", ChargeItemDefinitionApplicability, True, None, False),
            ("priceComponent", "priceComponent", ChargeItemDefinitionPropertyGroupPriceComponent, True, None, False),
        ])
        return js


class ChargeItemDefinitionPropertyGroupPriceComponent(backboneelement.BackboneElement):
    """ Components of total line item price.
    
    The price for a ChargeItem may be calculated as a base price with
    surcharges/deductions that apply in certain conditions. A
    ChargeItemDefinition resource that defines the prices, factors and
    conditions that apply to a billing code is currently under development. The
    priceComponent element can be used to offer transparency to the recipient
    of the Invoice of how the prices have been calculated.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """This code identifies the type of the component."""
    _attribute_docstrings['code'] = """Code identifying the specific component."""
    _attribute_docstrings['factor'] = """Factor used for calculating this component."""
    _attribute_docstrings['amount'] = """Monetary amount associated with this component."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://hl7.org/fhir/invoice-priceComponentType',
        'restricted_to': ['base', 'surcharge', 'deduction', 'discount', 'tax', 'informational'],
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
        
        self.type = None
        """ This code identifies the type of the component.
        Type `str`. """
        
        self.code = None
        """ Code identifying the specific component.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.factor = None
        """ Factor used for calculating this component.
        Type `float`. """
        
        self.amount = None
        """ Monetary amount associated with this component.
        Type `Money` (represented as `dict` in JSON). """
        
        super(ChargeItemDefinitionPropertyGroupPriceComponent, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ChargeItemDefinitionPropertyGroupPriceComponent, self).elementProperties()
        js.extend([
            ("type", "type", str, False, None, True),
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("factor", "factor", float, False, None, False),
            ("amount", "amount", money.Money, False, None, False),
        ])
        return js


import sys
try:
    from . import codeableconcept
except ImportError:
    codeableconcept = sys.modules[__package__ + '.codeableconcept']
try:
    from . import contactdetail
except ImportError:
    contactdetail = sys.modules[__package__ + '.contactdetail']
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
    from . import usagecontext
except ImportError:
    usagecontext = sys.modules[__package__ + '.usagecontext']
