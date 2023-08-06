#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/PaymentReconciliation) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class PaymentReconciliation(domainresource.DomainResource):
    """ PaymentReconciliation resource.
    
    This resource provides the details including amount of a payment and
    allocates the payment items being paid.
    """
    
    resource_type = "PaymentReconciliation"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business Identifier for a payment reconciliation."""
    _attribute_docstrings['status'] = """The status of the resource instance."""
    _attribute_docstrings['period'] = """Period covered."""
    _attribute_docstrings['created'] = """Creation date."""
    _attribute_docstrings['paymentIssuer'] = """Party generating payment."""
    _attribute_docstrings['request'] = """Reference to requesting resource."""
    _attribute_docstrings['requestor'] = """Responsible practitioner."""
    _attribute_docstrings['outcome'] = """The outcome of a request for a reconciliation."""
    _attribute_docstrings['disposition'] = """Disposition message."""
    _attribute_docstrings['paymentDate'] = """When payment issued."""
    _attribute_docstrings['paymentAmount'] = """Total amount of Payment."""
    _attribute_docstrings['paymentIdentifier'] = """Business identifier for the payment."""
    _attribute_docstrings['detail'] = """Settlement particulars."""
    _attribute_docstrings['formCode'] = """Printed form identifier."""
    _attribute_docstrings['processNote'] = """Note concerning processing."""

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
        """ Business Identifier for a payment reconciliation.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ The status of the resource instance.
        Type `str`. """
        
        self.period = None
        """ Period covered.
        Type `Period` (represented as `dict` in JSON). """
        
        self.created = None
        """ Creation date.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.paymentIssuer = None
        """ Party generating payment.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.request = None
        """ Reference to requesting resource.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.requestor = None
        """ Responsible practitioner.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.outcome = None
        """ The outcome of a request for a reconciliation.
        Type `str`. """
        
        self.disposition = None
        """ Disposition message.
        Type `str`. """
        
        self.paymentDate = None
        """ When payment issued.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.paymentAmount = None
        """ Total amount of Payment.
        Type `Money` (represented as `dict` in JSON). """
        
        self.paymentIdentifier = None
        """ Business identifier for the payment.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.detail = None
        """ Settlement particulars.
        List of `PaymentReconciliationDetail` items (represented as `dict` in JSON). """
        
        self.formCode = None
        """ Printed form identifier.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.processNote = None
        """ Note concerning processing.
        List of `PaymentReconciliationProcessNote` items (represented as `dict` in JSON). """
        
        super(PaymentReconciliation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PaymentReconciliation, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("period", "period", period.Period, False, None, False),
            ("created", "created", fhirdate.FHIRDate, False, None, True),
            ("paymentIssuer", "paymentIssuer", fhirreference.FHIRReference, False, None, False),
            ("request", "request", fhirreference.FHIRReference, False, None, False),
            ("requestor", "requestor", fhirreference.FHIRReference, False, None, False),
            ("outcome", "outcome", str, False, None, False),
            ("disposition", "disposition", str, False, None, False),
            ("paymentDate", "paymentDate", fhirdate.FHIRDate, False, None, True),
            ("paymentAmount", "paymentAmount", money.Money, False, None, True),
            ("paymentIdentifier", "paymentIdentifier", identifier.Identifier, False, None, False),
            ("detail", "detail", PaymentReconciliationDetail, True, None, False),
            ("formCode", "formCode", codeableconcept.CodeableConcept, False, None, False),
            ("processNote", "processNote", PaymentReconciliationProcessNote, True, None, False),
        ])
        return js


from . import backboneelement

class PaymentReconciliationDetail(backboneelement.BackboneElement):
    """ Settlement particulars.
    
    Distribution of the payment amount for a previously acknowledged payable.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business identifier of the payment detail."""
    _attribute_docstrings['predecessor'] = """Business identifier of the prior payment detail."""
    _attribute_docstrings['type'] = """Code to indicate the nature of the payment."""
    _attribute_docstrings['request'] = """Request giving rise to the payment."""
    _attribute_docstrings['submitter'] = """Submitter of the request."""
    _attribute_docstrings['response'] = """Response committing to a payment."""
    _attribute_docstrings['date'] = """Date of commitment to pay."""
    _attribute_docstrings['responsible'] = """Contact for the response."""
    _attribute_docstrings['payee'] = """Recipient of the payment."""
    _attribute_docstrings['amount'] = """Amount allocated to this payable."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/payment-type',
        'restricted_to': ['payment', 'adjustment', 'advance'],
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
        
        self.identifier = None
        """ Business identifier of the payment detail.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.predecessor = None
        """ Business identifier of the prior payment detail.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.type = None
        """ Code to indicate the nature of the payment.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.request = None
        """ Request giving rise to the payment.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.submitter = None
        """ Submitter of the request.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.response = None
        """ Response committing to a payment.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.date = None
        """ Date of commitment to pay.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.responsible = None
        """ Contact for the response.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.payee = None
        """ Recipient of the payment.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.amount = None
        """ Amount allocated to this payable.
        Type `Money` (represented as `dict` in JSON). """
        
        super(PaymentReconciliationDetail, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PaymentReconciliationDetail, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, False, None, False),
            ("predecessor", "predecessor", identifier.Identifier, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("request", "request", fhirreference.FHIRReference, False, None, False),
            ("submitter", "submitter", fhirreference.FHIRReference, False, None, False),
            ("response", "response", fhirreference.FHIRReference, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("responsible", "responsible", fhirreference.FHIRReference, False, None, False),
            ("payee", "payee", fhirreference.FHIRReference, False, None, False),
            ("amount", "amount", money.Money, False, None, False),
        ])
        return js


class PaymentReconciliationProcessNote(backboneelement.BackboneElement):
    """ Note concerning processing.
    
    A note that describes or explains the processing in a human readable form.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """The business purpose of the note text."""
    _attribute_docstrings['text'] = """Note explanatory text."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://hl7.org/fhir/note-type',
        'restricted_to': ['display', 'print', 'printoper'],
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
        """ The business purpose of the note text.
        Type `str`. """
        
        self.text = None
        """ Note explanatory text.
        Type `str`. """
        
        super(PaymentReconciliationProcessNote, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PaymentReconciliationProcessNote, self).elementProperties()
        js.extend([
            ("type", "type", str, False, None, False),
            ("text", "text", str, False, None, False),
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
