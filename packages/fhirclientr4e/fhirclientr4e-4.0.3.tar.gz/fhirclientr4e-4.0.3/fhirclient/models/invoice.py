#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Invoice) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Invoice(domainresource.DomainResource):
    """ Invoice containing ChargeItems from an Account.
    
    Invoice containing collected ChargeItems from an Account with calculated
    individual and total price for Billing purpose.
    """
    
    resource_type = "Invoice"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business Identifier for item."""
    _attribute_docstrings['status'] = """The current state of the Invoice."""
    _attribute_docstrings['cancelledReason'] = """Reason for cancellation of this Invoice."""
    _attribute_docstrings['type'] = """Type of Invoice."""
    _attribute_docstrings['subject'] = """Recipient(s) of goods and services."""
    _attribute_docstrings['recipient'] = """Recipient of this invoice."""
    _attribute_docstrings['date'] = """Invoice date / posting date."""
    _attribute_docstrings['participant'] = """Participant in creation of this Invoice."""
    _attribute_docstrings['issuer'] = """Issuing Organization of Invoice."""
    _attribute_docstrings['account'] = """Account that is being balanced."""
    _attribute_docstrings['lineItem'] = """Line items of this Invoice."""
    _attribute_docstrings['totalPriceComponent'] = """Components of Invoice total."""
    _attribute_docstrings['totalNet'] = """Net total of this Invoice."""
    _attribute_docstrings['totalGross'] = """Gross total of this Invoice."""
    _attribute_docstrings['paymentTerms'] = """Payment details."""
    _attribute_docstrings['note'] = """Comments made about the invoice."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/invoice-status',
        'restricted_to': ['draft', 'issued', 'balanced', 'cancelled', 'entered-in-error'],
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
        """ Business Identifier for item.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ The current state of the Invoice.
        Type `str`. """
        
        self.cancelledReason = None
        """ Reason for cancellation of this Invoice.
        Type `str`. """
        
        self.type = None
        """ Type of Invoice.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subject = None
        """ Recipient(s) of goods and services.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.recipient = None
        """ Recipient of this invoice.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.date = None
        """ Invoice date / posting date.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.participant = None
        """ Participant in creation of this Invoice.
        List of `InvoiceParticipant` items (represented as `dict` in JSON). """
        
        self.issuer = None
        """ Issuing Organization of Invoice.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.account = None
        """ Account that is being balanced.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.lineItem = None
        """ Line items of this Invoice.
        List of `InvoiceLineItem` items (represented as `dict` in JSON). """
        
        self.totalPriceComponent = None
        """ Components of Invoice total.
        List of `InvoiceLineItemPriceComponent` items (represented as `dict` in JSON). """
        
        self.totalNet = None
        """ Net total of this Invoice.
        Type `Money` (represented as `dict` in JSON). """
        
        self.totalGross = None
        """ Gross total of this Invoice.
        Type `Money` (represented as `dict` in JSON). """
        
        self.paymentTerms = None
        """ Payment details.
        Type `str`. """
        
        self.note = None
        """ Comments made about the invoice.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        super(Invoice, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Invoice, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("cancelledReason", "cancelledReason", str, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("subject", "subject", fhirreference.FHIRReference, False, None, False),
            ("recipient", "recipient", fhirreference.FHIRReference, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("participant", "participant", InvoiceParticipant, True, None, False),
            ("issuer", "issuer", fhirreference.FHIRReference, False, None, False),
            ("account", "account", fhirreference.FHIRReference, False, None, False),
            ("lineItem", "lineItem", InvoiceLineItem, True, None, False),
            ("totalPriceComponent", "totalPriceComponent", InvoiceLineItemPriceComponent, True, None, False),
            ("totalNet", "totalNet", money.Money, False, None, False),
            ("totalGross", "totalGross", money.Money, False, None, False),
            ("paymentTerms", "paymentTerms", str, False, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
        ])
        return js


from . import backboneelement

class InvoiceLineItem(backboneelement.BackboneElement):
    """ Line items of this Invoice.
    
    Each line item represents one charge for goods and services rendered.
    Details such as date, code and amount are found in the referenced
    ChargeItem resource.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['sequence'] = """Sequence number of line item."""
    _attribute_docstrings['chargeItemReference'] = """Reference to ChargeItem containing details of this line item or an inline billing code."""
    _attribute_docstrings['chargeItemCodeableConcept'] = """Reference to ChargeItem containing details of this line item or an inline billing code."""
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
        
        self.sequence = None
        """ Sequence number of line item.
        Type `int`. """
        
        self.chargeItemReference = None
        """ Reference to ChargeItem containing details of this line item or an
        inline billing code.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.chargeItemCodeableConcept = None
        """ Reference to ChargeItem containing details of this line item or an
        inline billing code.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.priceComponent = None
        """ Components of total line item price.
        List of `InvoiceLineItemPriceComponent` items (represented as `dict` in JSON). """
        
        super(InvoiceLineItem, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(InvoiceLineItem, self).elementProperties()
        js.extend([
            ("sequence", "sequence", int, False, None, False),
            ("chargeItemReference", "chargeItemReference", fhirreference.FHIRReference, False, "chargeItem", True),
            ("chargeItemCodeableConcept", "chargeItemCodeableConcept", codeableconcept.CodeableConcept, False, "chargeItem", True),
            ("priceComponent", "priceComponent", InvoiceLineItemPriceComponent, True, None, False),
        ])
        return js


class InvoiceLineItemPriceComponent(backboneelement.BackboneElement):
    """ Components of total line item price.
    
    The price for a ChargeItem may be calculated as a base price with
    surcharges/deductions that apply in certain conditions. A
    ChargeItemDefinition resource that defines the prices, factors and
    conditions that apply to a billing code is currently under development. The
    priceComponent element can be used to offer transparency to the recipient
    of the Invoice as to how the prices have been calculated.
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
        
        super(InvoiceLineItemPriceComponent, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(InvoiceLineItemPriceComponent, self).elementProperties()
        js.extend([
            ("type", "type", str, False, None, True),
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("factor", "factor", float, False, None, False),
            ("amount", "amount", money.Money, False, None, False),
        ])
        return js


class InvoiceParticipant(backboneelement.BackboneElement):
    """ Participant in creation of this Invoice.
    
    Indicates who or what performed or participated in the charged service.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['role'] = """Type of involvement in creation of this Invoice."""
    _attribute_docstrings['actor'] = """Individual who was involved."""

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
        
        self.role = None
        """ Type of involvement in creation of this Invoice.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.actor = None
        """ Individual who was involved.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(InvoiceParticipant, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(InvoiceParticipant, self).elementProperties()
        js.extend([
            ("role", "role", codeableconcept.CodeableConcept, False, None, False),
            ("actor", "actor", fhirreference.FHIRReference, False, None, True),
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
    from . import money
except ImportError:
    money = sys.modules[__package__ + '.money']
