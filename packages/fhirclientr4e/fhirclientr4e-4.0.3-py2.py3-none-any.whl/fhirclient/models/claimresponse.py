#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/ClaimResponse) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class ClaimResponse(domainresource.DomainResource):
    """ Response to a claim predetermination or preauthorization.
    
    This resource provides the adjudication details from the processing of a
    Claim resource.
    """
    
    resource_type = "ClaimResponse"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business Identifier for a claim response."""
    _attribute_docstrings['status'] = """The status of the resource instance."""
    _attribute_docstrings['type'] = """A finer grained suite of claim type codes which may convey additional information such as Inpatient vs Outpatient and/or a specialty service."""
    _attribute_docstrings['subType'] = """A finer grained suite of claim type codes which may convey additional information such as Inpatient vs Outpatient and/or a specialty service."""
    _attribute_docstrings['use'] = """A code to indicate whether the nature of the request is: to request adjudication of products and services previously rendered; or requesting authorization and adjudication for provision in the future; or requesting the non-binding adjudication of the listed products and services which could be provided in the future."""
    _attribute_docstrings['patient'] = """The recipient of the products and services."""
    _attribute_docstrings['created'] = """Response creation date."""
    _attribute_docstrings['insurer'] = """Party responsible for reimbursement."""
    _attribute_docstrings['requestor'] = """Party responsible for the claim."""
    _attribute_docstrings['request'] = """Id of resource triggering adjudication."""
    _attribute_docstrings['outcome'] = """The outcome of the claim, predetermination, or preauthorization processing."""
    _attribute_docstrings['disposition'] = """Disposition Message."""
    _attribute_docstrings['preAuthRef'] = """Preauthorization reference."""
    _attribute_docstrings['preAuthPeriod'] = """Preauthorization reference effective period."""
    _attribute_docstrings['payeeType'] = """Party to be paid any benefits payable."""
    _attribute_docstrings['item'] = """Adjudication for claim line items."""
    _attribute_docstrings['addItem'] = """Insurer added line items."""
    _attribute_docstrings['adjudication'] = """Header-level adjudication."""
    _attribute_docstrings['total'] = """Adjudication totals."""
    _attribute_docstrings['payment'] = """Payment Details."""
    _attribute_docstrings['fundsReserve'] = """Funds reserved status."""
    _attribute_docstrings['formCode'] = """Printed form identifier."""
    _attribute_docstrings['form'] = """Printed reference or actual form."""
    _attribute_docstrings['processNote'] = """Note concerning adjudication."""
    _attribute_docstrings['communicationRequest'] = """Request for additional information."""
    _attribute_docstrings['insurance'] = """Patient insurance information."""
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
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/claim-type',
        'restricted_to': ['institutional', 'oral', 'pharmacy', 'professional', 'vision'],
        'binding_strength': 'extensible',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['subType'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/ex-claimsubtype',
        'restricted_to': ['ortho', 'emergency'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['use'] = {
        'url': 'http://hl7.org/fhir/claim-use',
        'restricted_to': ['claim', 'preauthorization', 'predetermination'],
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
        """ Business Identifier for a claim response.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ The status of the resource instance.
        Type `str`. """
        
        self.type = None
        """ A finer grained suite of claim type codes which may convey
        additional information such as Inpatient vs Outpatient and/or a
        specialty service.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subType = None
        """ A finer grained suite of claim type codes which may convey
        additional information such as Inpatient vs Outpatient and/or a
        specialty service.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.use = None
        """ A code to indicate whether the nature of the request is: to request
        adjudication of products and services previously rendered; or
        requesting authorization and adjudication for provision in the
        future; or requesting the non-binding adjudication of the listed
        products and services which could be provided in the future.
        Type `str`. """
        
        self.patient = None
        """ The recipient of the products and services.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.created = None
        """ Response creation date.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.insurer = None
        """ Party responsible for reimbursement.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.requestor = None
        """ Party responsible for the claim.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.request = None
        """ Id of resource triggering adjudication.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.outcome = None
        """ The outcome of the claim, predetermination, or preauthorization
        processing.
        Type `str`. """
        
        self.disposition = None
        """ Disposition Message.
        Type `str`. """
        
        self.preAuthRef = None
        """ Preauthorization reference.
        Type `str`. """
        
        self.preAuthPeriod = None
        """ Preauthorization reference effective period.
        Type `Period` (represented as `dict` in JSON). """
        
        self.payeeType = None
        """ Party to be paid any benefits payable.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.item = None
        """ Adjudication for claim line items.
        List of `ClaimResponseItem` items (represented as `dict` in JSON). """
        
        self.addItem = None
        """ Insurer added line items.
        List of `ClaimResponseAddItem` items (represented as `dict` in JSON). """
        
        self.adjudication = None
        """ Header-level adjudication.
        List of `ClaimResponseItemAdjudication` items (represented as `dict` in JSON). """
        
        self.total = None
        """ Adjudication totals.
        List of `ClaimResponseTotal` items (represented as `dict` in JSON). """
        
        self.payment = None
        """ Payment Details.
        Type `ClaimResponsePayment` (represented as `dict` in JSON). """
        
        self.fundsReserve = None
        """ Funds reserved status.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.formCode = None
        """ Printed form identifier.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.form = None
        """ Printed reference or actual form.
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.processNote = None
        """ Note concerning adjudication.
        List of `ClaimResponseProcessNote` items (represented as `dict` in JSON). """
        
        self.communicationRequest = None
        """ Request for additional information.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.insurance = None
        """ Patient insurance information.
        List of `ClaimResponseInsurance` items (represented as `dict` in JSON). """
        
        self.error = None
        """ Processing errors.
        List of `ClaimResponseError` items (represented as `dict` in JSON). """
        
        super(ClaimResponse, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponse, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("subType", "subType", codeableconcept.CodeableConcept, False, None, False),
            ("use", "use", str, False, None, True),
            ("patient", "patient", fhirreference.FHIRReference, False, None, True),
            ("created", "created", fhirdate.FHIRDate, False, None, True),
            ("insurer", "insurer", fhirreference.FHIRReference, False, None, True),
            ("requestor", "requestor", fhirreference.FHIRReference, False, None, False),
            ("request", "request", fhirreference.FHIRReference, False, None, False),
            ("outcome", "outcome", str, False, None, True),
            ("disposition", "disposition", str, False, None, False),
            ("preAuthRef", "preAuthRef", str, False, None, False),
            ("preAuthPeriod", "preAuthPeriod", period.Period, False, None, False),
            ("payeeType", "payeeType", codeableconcept.CodeableConcept, False, None, False),
            ("item", "item", ClaimResponseItem, True, None, False),
            ("addItem", "addItem", ClaimResponseAddItem, True, None, False),
            ("adjudication", "adjudication", ClaimResponseItemAdjudication, True, None, False),
            ("total", "total", ClaimResponseTotal, True, None, False),
            ("payment", "payment", ClaimResponsePayment, False, None, False),
            ("fundsReserve", "fundsReserve", codeableconcept.CodeableConcept, False, None, False),
            ("formCode", "formCode", codeableconcept.CodeableConcept, False, None, False),
            ("form", "form", attachment.Attachment, False, None, False),
            ("processNote", "processNote", ClaimResponseProcessNote, True, None, False),
            ("communicationRequest", "communicationRequest", fhirreference.FHIRReference, True, None, False),
            ("insurance", "insurance", ClaimResponseInsurance, True, None, False),
            ("error", "error", ClaimResponseError, True, None, False),
        ])
        return js


from . import backboneelement

class ClaimResponseAddItem(backboneelement.BackboneElement):
    """ Insurer added line items.
    
    The first-tier service adjudications for payor added product or service
    lines.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['itemSequence'] = """Item sequence number."""
    _attribute_docstrings['detailSequence'] = """Detail sequence number."""
    _attribute_docstrings['subdetailSequence'] = """Subdetail sequence number."""
    _attribute_docstrings['provider'] = """Authorized providers."""
    _attribute_docstrings['productOrService'] = """Billing, service, product, or drug code."""
    _attribute_docstrings['modifier'] = """Item typification or modifiers codes to convey additional context for the product or service."""
    _attribute_docstrings['programCode'] = """Identifies the program under which this may be recovered."""
    _attribute_docstrings['servicedDate'] = """Date or dates of service or product delivery."""
    _attribute_docstrings['servicedPeriod'] = """Date or dates of service or product delivery."""
    _attribute_docstrings['locationCodeableConcept'] = """Place of service or where product was supplied."""
    _attribute_docstrings['locationAddress'] = """Place of service or where product was supplied."""
    _attribute_docstrings['locationReference'] = """Place of service or where product was supplied."""
    _attribute_docstrings['quantity'] = """Count of products or services."""
    _attribute_docstrings['unitPrice'] = """Fee, charge or cost per item."""
    _attribute_docstrings['factor'] = """Price scaling factor."""
    _attribute_docstrings['net'] = """Total item cost."""
    _attribute_docstrings['bodySite'] = """Anatomical location."""
    _attribute_docstrings['subSite'] = """A region or surface of the bodySite, e.g. limb region or tooth surface(s)."""
    _attribute_docstrings['noteNumber'] = """Applicable note numbers."""
    _attribute_docstrings['adjudication'] = """Added items adjudication."""
    _attribute_docstrings['detail'] = """Insurer added line details."""

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
    _attribute_enums['programCode'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/ex-programcode',
        'restricted_to': ['as', 'hd', 'auscr', 'none'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['subSite'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/FDI-surface',
        'restricted_to': ['M', 'O', 'I', 'D', 'B', 'V', 'L', 'MO', 'DO', 'DI', 'MOD'],
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
        
        self.itemSequence = None
        """ Item sequence number.
        List of `int` items. """
        
        self.detailSequence = None
        """ Detail sequence number.
        List of `int` items. """
        
        self.subdetailSequence = None
        """ Subdetail sequence number.
        List of `int` items. """
        
        self.provider = None
        """ Authorized providers.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.productOrService = None
        """ Billing, service, product, or drug code.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.modifier = None
        """ Item typification or modifiers codes to convey additional context
        for the product or service.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.programCode = None
        """ Identifies the program under which this may be recovered.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.servicedDate = None
        """ Date or dates of service or product delivery.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.servicedPeriod = None
        """ Date or dates of service or product delivery.
        Type `Period` (represented as `dict` in JSON). """
        
        self.locationCodeableConcept = None
        """ Place of service or where product was supplied.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.locationAddress = None
        """ Place of service or where product was supplied.
        Type `Address` (represented as `dict` in JSON). """
        
        self.locationReference = None
        """ Place of service or where product was supplied.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.quantity = None
        """ Count of products or services.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.unitPrice = None
        """ Fee, charge or cost per item.
        Type `Money` (represented as `dict` in JSON). """
        
        self.factor = None
        """ Price scaling factor.
        Type `float`. """
        
        self.net = None
        """ Total item cost.
        Type `Money` (represented as `dict` in JSON). """
        
        self.bodySite = None
        """ Anatomical location.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subSite = None
        """ A region or surface of the bodySite, e.g. limb region or tooth
        surface(s).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.noteNumber = None
        """ Applicable note numbers.
        List of `int` items. """
        
        self.adjudication = None
        """ Added items adjudication.
        List of `ClaimResponseItemAdjudication` items (represented as `dict` in JSON). """
        
        self.detail = None
        """ Insurer added line details.
        List of `ClaimResponseAddItemDetail` items (represented as `dict` in JSON). """
        
        super(ClaimResponseAddItem, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponseAddItem, self).elementProperties()
        js.extend([
            ("itemSequence", "itemSequence", int, True, None, False),
            ("detailSequence", "detailSequence", int, True, None, False),
            ("subdetailSequence", "subdetailSequence", int, True, None, False),
            ("provider", "provider", fhirreference.FHIRReference, True, None, False),
            ("productOrService", "productOrService", codeableconcept.CodeableConcept, False, None, True),
            ("modifier", "modifier", codeableconcept.CodeableConcept, True, None, False),
            ("programCode", "programCode", codeableconcept.CodeableConcept, True, None, False),
            ("servicedDate", "servicedDate", fhirdate.FHIRDate, False, "serviced", False),
            ("servicedPeriod", "servicedPeriod", period.Period, False, "serviced", False),
            ("locationCodeableConcept", "locationCodeableConcept", codeableconcept.CodeableConcept, False, "location", False),
            ("locationAddress", "locationAddress", address.Address, False, "location", False),
            ("locationReference", "locationReference", fhirreference.FHIRReference, False, "location", False),
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("unitPrice", "unitPrice", money.Money, False, None, False),
            ("factor", "factor", float, False, None, False),
            ("net", "net", money.Money, False, None, False),
            ("bodySite", "bodySite", codeableconcept.CodeableConcept, False, None, False),
            ("subSite", "subSite", codeableconcept.CodeableConcept, True, None, False),
            ("noteNumber", "noteNumber", int, True, None, False),
            ("adjudication", "adjudication", ClaimResponseItemAdjudication, True, None, True),
            ("detail", "detail", ClaimResponseAddItemDetail, True, None, False),
        ])
        return js


class ClaimResponseAddItemDetail(backboneelement.BackboneElement):
    """ Insurer added line details.
    
    The second-tier service adjudications for payor added services.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['productOrService'] = """Billing, service, product, or drug code."""
    _attribute_docstrings['modifier'] = """Item typification or modifiers codes to convey additional context for the product or service."""
    _attribute_docstrings['quantity'] = """Count of products or services."""
    _attribute_docstrings['unitPrice'] = """Fee, charge or cost per item."""
    _attribute_docstrings['factor'] = """Price scaling factor."""
    _attribute_docstrings['net'] = """Total item cost."""
    _attribute_docstrings['noteNumber'] = """Applicable note numbers."""
    _attribute_docstrings['adjudication'] = """Added items detail adjudication."""
    _attribute_docstrings['subDetail'] = """Insurer added line items."""

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
        
        self.productOrService = None
        """ Billing, service, product, or drug code.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.modifier = None
        """ Item typification or modifiers codes to convey additional context
        for the product or service.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.quantity = None
        """ Count of products or services.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.unitPrice = None
        """ Fee, charge or cost per item.
        Type `Money` (represented as `dict` in JSON). """
        
        self.factor = None
        """ Price scaling factor.
        Type `float`. """
        
        self.net = None
        """ Total item cost.
        Type `Money` (represented as `dict` in JSON). """
        
        self.noteNumber = None
        """ Applicable note numbers.
        List of `int` items. """
        
        self.adjudication = None
        """ Added items detail adjudication.
        List of `ClaimResponseItemAdjudication` items (represented as `dict` in JSON). """
        
        self.subDetail = None
        """ Insurer added line items.
        List of `ClaimResponseAddItemDetailSubDetail` items (represented as `dict` in JSON). """
        
        super(ClaimResponseAddItemDetail, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponseAddItemDetail, self).elementProperties()
        js.extend([
            ("productOrService", "productOrService", codeableconcept.CodeableConcept, False, None, True),
            ("modifier", "modifier", codeableconcept.CodeableConcept, True, None, False),
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("unitPrice", "unitPrice", money.Money, False, None, False),
            ("factor", "factor", float, False, None, False),
            ("net", "net", money.Money, False, None, False),
            ("noteNumber", "noteNumber", int, True, None, False),
            ("adjudication", "adjudication", ClaimResponseItemAdjudication, True, None, True),
            ("subDetail", "subDetail", ClaimResponseAddItemDetailSubDetail, True, None, False),
        ])
        return js


class ClaimResponseAddItemDetailSubDetail(backboneelement.BackboneElement):
    """ Insurer added line items.
    
    The third-tier service adjudications for payor added services.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['productOrService'] = """Billing, service, product, or drug code."""
    _attribute_docstrings['modifier'] = """Item typification or modifiers codes to convey additional context for the product or service."""
    _attribute_docstrings['quantity'] = """Count of products or services."""
    _attribute_docstrings['unitPrice'] = """Fee, charge or cost per item."""
    _attribute_docstrings['factor'] = """Price scaling factor."""
    _attribute_docstrings['net'] = """Total item cost."""
    _attribute_docstrings['noteNumber'] = """Applicable note numbers."""
    _attribute_docstrings['adjudication'] = """Added items detail adjudication."""

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
        
        self.productOrService = None
        """ Billing, service, product, or drug code.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.modifier = None
        """ Item typification or modifiers codes to convey additional context
        for the product or service.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.quantity = None
        """ Count of products or services.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.unitPrice = None
        """ Fee, charge or cost per item.
        Type `Money` (represented as `dict` in JSON). """
        
        self.factor = None
        """ Price scaling factor.
        Type `float`. """
        
        self.net = None
        """ Total item cost.
        Type `Money` (represented as `dict` in JSON). """
        
        self.noteNumber = None
        """ Applicable note numbers.
        List of `int` items. """
        
        self.adjudication = None
        """ Added items detail adjudication.
        List of `ClaimResponseItemAdjudication` items (represented as `dict` in JSON). """
        
        super(ClaimResponseAddItemDetailSubDetail, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponseAddItemDetailSubDetail, self).elementProperties()
        js.extend([
            ("productOrService", "productOrService", codeableconcept.CodeableConcept, False, None, True),
            ("modifier", "modifier", codeableconcept.CodeableConcept, True, None, False),
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("unitPrice", "unitPrice", money.Money, False, None, False),
            ("factor", "factor", float, False, None, False),
            ("net", "net", money.Money, False, None, False),
            ("noteNumber", "noteNumber", int, True, None, False),
            ("adjudication", "adjudication", ClaimResponseItemAdjudication, True, None, True),
        ])
        return js


class ClaimResponseError(backboneelement.BackboneElement):
    """ Processing errors.
    
    Errors encountered during the processing of the adjudication.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['itemSequence'] = """Item sequence number."""
    _attribute_docstrings['detailSequence'] = """Detail sequence number."""
    _attribute_docstrings['subDetailSequence'] = """Subdetail sequence number."""
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
        
        self.itemSequence = None
        """ Item sequence number.
        Type `int`. """
        
        self.detailSequence = None
        """ Detail sequence number.
        Type `int`. """
        
        self.subDetailSequence = None
        """ Subdetail sequence number.
        Type `int`. """
        
        self.code = None
        """ Error code detailing processing issues.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(ClaimResponseError, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponseError, self).elementProperties()
        js.extend([
            ("itemSequence", "itemSequence", int, False, None, False),
            ("detailSequence", "detailSequence", int, False, None, False),
            ("subDetailSequence", "subDetailSequence", int, False, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, True),
        ])
        return js


class ClaimResponseInsurance(backboneelement.BackboneElement):
    """ Patient insurance information.
    
    Financial instruments for reimbursement for the health care products and
    services specified on the claim.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['sequence'] = """Insurance instance identifier."""
    _attribute_docstrings['focal'] = """Coverage to be used for adjudication."""
    _attribute_docstrings['coverage'] = """Insurance information."""
    _attribute_docstrings['businessArrangement'] = """Additional provider contract number."""
    _attribute_docstrings['claimResponse'] = """Adjudication results."""

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
        """ Insurance instance identifier.
        Type `int`. """
        
        self.focal = None
        """ Coverage to be used for adjudication.
        Type `bool`. """
        
        self.coverage = None
        """ Insurance information.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.businessArrangement = None
        """ Additional provider contract number.
        Type `str`. """
        
        self.claimResponse = None
        """ Adjudication results.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(ClaimResponseInsurance, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponseInsurance, self).elementProperties()
        js.extend([
            ("sequence", "sequence", int, False, None, True),
            ("focal", "focal", bool, False, None, True),
            ("coverage", "coverage", fhirreference.FHIRReference, False, None, True),
            ("businessArrangement", "businessArrangement", str, False, None, False),
            ("claimResponse", "claimResponse", fhirreference.FHIRReference, False, None, False),
        ])
        return js


class ClaimResponseItem(backboneelement.BackboneElement):
    """ Adjudication for claim line items.
    
    A claim line. Either a simple (a product or service) or a 'group' of
    details which can also be a simple items or groups of sub-details.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['itemSequence'] = """Claim item instance identifier."""
    _attribute_docstrings['noteNumber'] = """Applicable note numbers."""
    _attribute_docstrings['adjudication'] = """Adjudication details."""
    _attribute_docstrings['detail'] = """Adjudication for claim details."""

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
        
        self.itemSequence = None
        """ Claim item instance identifier.
        Type `int`. """
        
        self.noteNumber = None
        """ Applicable note numbers.
        List of `int` items. """
        
        self.adjudication = None
        """ Adjudication details.
        List of `ClaimResponseItemAdjudication` items (represented as `dict` in JSON). """
        
        self.detail = None
        """ Adjudication for claim details.
        List of `ClaimResponseItemDetail` items (represented as `dict` in JSON). """
        
        super(ClaimResponseItem, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponseItem, self).elementProperties()
        js.extend([
            ("itemSequence", "itemSequence", int, False, None, True),
            ("noteNumber", "noteNumber", int, True, None, False),
            ("adjudication", "adjudication", ClaimResponseItemAdjudication, True, None, True),
            ("detail", "detail", ClaimResponseItemDetail, True, None, False),
        ])
        return js


class ClaimResponseItemAdjudication(backboneelement.BackboneElement):
    """ Adjudication details.
    
    If this item is a group then the values here are a summary of the
    adjudication of the detail items. If this item is a simple product or
    service then this is the result of the adjudication of this item.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['category'] = """A code to indicate the information type of this adjudication record. Information types may include the value submitted, maximum values or percentages allowed or payable under the plan, amounts that: the patient is responsible for in aggregate or pertaining to this item; amounts paid by other coverages; and, the benefit payable for this item."""
    _attribute_docstrings['reason'] = """A code supporting the understanding of the adjudication result and explaining variance from expected amount."""
    _attribute_docstrings['amount'] = """Monetary amount."""
    _attribute_docstrings['value'] = """Non-monetary value."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['category'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/adjudication',
        'restricted_to': ['submitted', 'copay', 'eligible', 'deductible', 'unallocdeduct', 'eligpercent', 'tax', 'benefit'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['reason'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/adjudication-reason',
        'restricted_to': ['ar001', 'ar002'],
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
        """ A code to indicate the information type of this adjudication
        record. Information types may include the value submitted, maximum
        values or percentages allowed or payable under the plan, amounts
        that: the patient is responsible for in aggregate or pertaining to
        this item; amounts paid by other coverages; and, the benefit
        payable for this item.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.reason = None
        """ A code supporting the understanding of the adjudication result and
        explaining variance from expected amount.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.amount = None
        """ Monetary amount.
        Type `Money` (represented as `dict` in JSON). """
        
        self.value = None
        """ Non-monetary value.
        Type `float`. """
        
        super(ClaimResponseItemAdjudication, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponseItemAdjudication, self).elementProperties()
        js.extend([
            ("category", "category", codeableconcept.CodeableConcept, False, None, True),
            ("reason", "reason", codeableconcept.CodeableConcept, False, None, False),
            ("amount", "amount", money.Money, False, None, False),
            ("value", "value", float, False, None, False),
        ])
        return js


class ClaimResponseItemDetail(backboneelement.BackboneElement):
    """ Adjudication for claim details.
    
    A claim detail. Either a simple (a product or service) or a 'group' of sub-
    details which are simple items.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['detailSequence'] = """Claim detail instance identifier."""
    _attribute_docstrings['noteNumber'] = """Applicable note numbers."""
    _attribute_docstrings['adjudication'] = """Detail level adjudication details."""
    _attribute_docstrings['subDetail'] = """Adjudication for claim sub-details."""

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
        
        self.detailSequence = None
        """ Claim detail instance identifier.
        Type `int`. """
        
        self.noteNumber = None
        """ Applicable note numbers.
        List of `int` items. """
        
        self.adjudication = None
        """ Detail level adjudication details.
        List of `ClaimResponseItemAdjudication` items (represented as `dict` in JSON). """
        
        self.subDetail = None
        """ Adjudication for claim sub-details.
        List of `ClaimResponseItemDetailSubDetail` items (represented as `dict` in JSON). """
        
        super(ClaimResponseItemDetail, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponseItemDetail, self).elementProperties()
        js.extend([
            ("detailSequence", "detailSequence", int, False, None, True),
            ("noteNumber", "noteNumber", int, True, None, False),
            ("adjudication", "adjudication", ClaimResponseItemAdjudication, True, None, True),
            ("subDetail", "subDetail", ClaimResponseItemDetailSubDetail, True, None, False),
        ])
        return js


class ClaimResponseItemDetailSubDetail(backboneelement.BackboneElement):
    """ Adjudication for claim sub-details.
    
    A sub-detail adjudication of a simple product or service.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['subDetailSequence'] = """Claim sub-detail instance identifier."""
    _attribute_docstrings['noteNumber'] = """Applicable note numbers."""
    _attribute_docstrings['adjudication'] = """Subdetail level adjudication details."""

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
        
        self.subDetailSequence = None
        """ Claim sub-detail instance identifier.
        Type `int`. """
        
        self.noteNumber = None
        """ Applicable note numbers.
        List of `int` items. """
        
        self.adjudication = None
        """ Subdetail level adjudication details.
        List of `ClaimResponseItemAdjudication` items (represented as `dict` in JSON). """
        
        super(ClaimResponseItemDetailSubDetail, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponseItemDetailSubDetail, self).elementProperties()
        js.extend([
            ("subDetailSequence", "subDetailSequence", int, False, None, True),
            ("noteNumber", "noteNumber", int, True, None, False),
            ("adjudication", "adjudication", ClaimResponseItemAdjudication, True, None, False),
        ])
        return js


class ClaimResponsePayment(backboneelement.BackboneElement):
    """ Payment Details.
    
    Payment details for the adjudication of the claim.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Whether this represents partial or complete payment of the benefits payable."""
    _attribute_docstrings['adjustment'] = """Payment adjustment for non-claim issues."""
    _attribute_docstrings['adjustmentReason'] = """Reason for the payment adjustment."""
    _attribute_docstrings['date'] = """Expected date of payment."""
    _attribute_docstrings['amount'] = """Payable amount after adjustment."""
    _attribute_docstrings['identifier'] = """Business identifier for the payment."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/ex-paymenttype',
        'restricted_to': ['complete', 'partial'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['adjustmentReason'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/payment-adjustment-reason',
        'restricted_to': ['a001', 'a002'],
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
        """ Whether this represents partial or complete payment of the benefits
        payable.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.adjustment = None
        """ Payment adjustment for non-claim issues.
        Type `Money` (represented as `dict` in JSON). """
        
        self.adjustmentReason = None
        """ Reason for the payment adjustment.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.date = None
        """ Expected date of payment.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.amount = None
        """ Payable amount after adjustment.
        Type `Money` (represented as `dict` in JSON). """
        
        self.identifier = None
        """ Business identifier for the payment.
        Type `Identifier` (represented as `dict` in JSON). """
        
        super(ClaimResponsePayment, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponsePayment, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("adjustment", "adjustment", money.Money, False, None, False),
            ("adjustmentReason", "adjustmentReason", codeableconcept.CodeableConcept, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("amount", "amount", money.Money, False, None, True),
            ("identifier", "identifier", identifier.Identifier, False, None, False),
        ])
        return js


class ClaimResponseProcessNote(backboneelement.BackboneElement):
    """ Note concerning adjudication.
    
    A note that describes or explains adjudication results in a human readable
    form.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['number'] = """Note instance identifier."""
    _attribute_docstrings['type'] = """The business purpose of the note text."""
    _attribute_docstrings['text'] = """Note explanatory text."""
    _attribute_docstrings['language'] = """Language of the text."""

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
        
        self.number = None
        """ Note instance identifier.
        Type `int`. """
        
        self.type = None
        """ The business purpose of the note text.
        Type `str`. """
        
        self.text = None
        """ Note explanatory text.
        Type `str`. """
        
        self.language = None
        """ Language of the text.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(ClaimResponseProcessNote, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponseProcessNote, self).elementProperties()
        js.extend([
            ("number", "number", int, False, None, False),
            ("type", "type", str, False, None, False),
            ("text", "text", str, False, None, True),
            ("language", "language", codeableconcept.CodeableConcept, False, None, False),
        ])
        return js


class ClaimResponseTotal(backboneelement.BackboneElement):
    """ Adjudication totals.
    
    Categorized monetary totals for the adjudication.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['category'] = """A code to indicate the information type of this adjudication record. Information types may include: the value submitted, maximum values or percentages allowed or payable under the plan, amounts that the patient is responsible for in aggregate or pertaining to this item, amounts paid by other coverages, and the benefit payable for this item."""
    _attribute_docstrings['amount'] = """Financial total for the category."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['category'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/adjudication',
        'restricted_to': ['submitted', 'copay', 'eligible', 'deductible', 'unallocdeduct', 'eligpercent', 'tax', 'benefit'],
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
        """ A code to indicate the information type of this adjudication
        record. Information types may include: the value submitted, maximum
        values or percentages allowed or payable under the plan, amounts
        that the patient is responsible for in aggregate or pertaining to
        this item, amounts paid by other coverages, and the benefit payable
        for this item.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.amount = None
        """ Financial total for the category.
        Type `Money` (represented as `dict` in JSON). """
        
        super(ClaimResponseTotal, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimResponseTotal, self).elementProperties()
        js.extend([
            ("category", "category", codeableconcept.CodeableConcept, False, None, True),
            ("amount", "amount", money.Money, False, None, True),
        ])
        return js


import sys
try:
    from . import address
except ImportError:
    address = sys.modules[__package__ + '.address']
try:
    from . import attachment
except ImportError:
    attachment = sys.modules[__package__ + '.attachment']
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
