#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/ExplanationOfBenefit) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class ExplanationOfBenefit(domainresource.DomainResource):
    """ Explanation of Benefit resource.
    
    This resource provides: the claim details; adjudication details from the
    processing of a Claim; and optionally account balance information, for
    informing the subscriber of the benefits provided.
    """
    
    resource_type = "ExplanationOfBenefit"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business Identifier for the resource."""
    _attribute_docstrings['status'] = """The status of the resource instance."""
    _attribute_docstrings['type'] = """The category of claim, e.g. oral, pharmacy, vision, institutional, professional."""
    _attribute_docstrings['subType'] = """A finer grained suite of claim type codes which may convey additional information such as Inpatient vs Outpatient and/or a specialty service."""
    _attribute_docstrings['use'] = """A code to indicate whether the nature of the request is: to request adjudication of products and services previously rendered; or requesting authorization and adjudication for provision in the future; or requesting the non-binding adjudication of the listed products and services which could be provided in the future."""
    _attribute_docstrings['patient'] = """The recipient of the products and services."""
    _attribute_docstrings['billablePeriod'] = """Relevant time frame for the claim."""
    _attribute_docstrings['created'] = """Response creation date."""
    _attribute_docstrings['enterer'] = """Author of the claim."""
    _attribute_docstrings['insurer'] = """Party responsible for reimbursement."""
    _attribute_docstrings['provider'] = """Party responsible for the claim."""
    _attribute_docstrings['priority'] = """Desired processing urgency."""
    _attribute_docstrings['fundsReserveRequested'] = """For whom to reserve funds."""
    _attribute_docstrings['fundsReserve'] = """Funds reserved status."""
    _attribute_docstrings['related'] = """Prior or corollary claims."""
    _attribute_docstrings['prescription'] = """Prescription authorizing services or products."""
    _attribute_docstrings['originalPrescription'] = """Original prescription if superceded by fulfiller."""
    _attribute_docstrings['payee'] = """Recipient of benefits payable."""
    _attribute_docstrings['referral'] = """Treatment Referral."""
    _attribute_docstrings['facility'] = """Servicing Facility."""
    _attribute_docstrings['claim'] = """Claim reference."""
    _attribute_docstrings['claimResponse'] = """Claim response reference."""
    _attribute_docstrings['outcome'] = """The outcome of the claim, predetermination, or preauthorization processing."""
    _attribute_docstrings['disposition'] = """Disposition Message."""
    _attribute_docstrings['preAuthRef'] = """Preauthorization reference."""
    _attribute_docstrings['preAuthRefPeriod'] = """Preauthorization in-effect period."""
    _attribute_docstrings['careTeam'] = """Care Team members."""
    _attribute_docstrings['supportingInfo'] = """Supporting information."""
    _attribute_docstrings['diagnosis'] = """Pertinent diagnosis information."""
    _attribute_docstrings['procedure'] = """Clinical procedures performed."""
    _attribute_docstrings['precedence'] = """Precedence (primary, secondary, etc.)."""
    _attribute_docstrings['insurance'] = """Patient insurance information."""
    _attribute_docstrings['accident'] = """Details of the event."""
    _attribute_docstrings['item'] = """Product or service provided."""
    _attribute_docstrings['addItem'] = """Insurer added line items."""
    _attribute_docstrings['adjudication'] = """Header-level adjudication."""
    _attribute_docstrings['total'] = """Adjudication totals."""
    _attribute_docstrings['payment'] = """Payment Details."""
    _attribute_docstrings['formCode'] = """Printed form identifier."""
    _attribute_docstrings['form'] = """Printed reference or actual form."""
    _attribute_docstrings['processNote'] = """Note concerning adjudication."""
    _attribute_docstrings['benefitPeriod'] = """When the benefits are applicable."""
    _attribute_docstrings['benefitBalance'] = """Balance by Benefit Category."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/explanationofbenefit-status',
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
        """ Business Identifier for the resource.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ The status of the resource instance.
        Type `str`. """
        
        self.type = None
        """ The category of claim, e.g. oral, pharmacy, vision, institutional,
        professional.
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
        
        self.billablePeriod = None
        """ Relevant time frame for the claim.
        Type `Period` (represented as `dict` in JSON). """
        
        self.created = None
        """ Response creation date.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.enterer = None
        """ Author of the claim.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.insurer = None
        """ Party responsible for reimbursement.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.provider = None
        """ Party responsible for the claim.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.priority = None
        """ Desired processing urgency.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.fundsReserveRequested = None
        """ For whom to reserve funds.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.fundsReserve = None
        """ Funds reserved status.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.related = None
        """ Prior or corollary claims.
        List of `ExplanationOfBenefitRelated` items (represented as `dict` in JSON). """
        
        self.prescription = None
        """ Prescription authorizing services or products.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.originalPrescription = None
        """ Original prescription if superceded by fulfiller.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.payee = None
        """ Recipient of benefits payable.
        Type `ExplanationOfBenefitPayee` (represented as `dict` in JSON). """
        
        self.referral = None
        """ Treatment Referral.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.facility = None
        """ Servicing Facility.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.claim = None
        """ Claim reference.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.claimResponse = None
        """ Claim response reference.
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
        List of `str` items. """
        
        self.preAuthRefPeriod = None
        """ Preauthorization in-effect period.
        List of `Period` items (represented as `dict` in JSON). """
        
        self.careTeam = None
        """ Care Team members.
        List of `ExplanationOfBenefitCareTeam` items (represented as `dict` in JSON). """
        
        self.supportingInfo = None
        """ Supporting information.
        List of `ExplanationOfBenefitSupportingInfo` items (represented as `dict` in JSON). """
        
        self.diagnosis = None
        """ Pertinent diagnosis information.
        List of `ExplanationOfBenefitDiagnosis` items (represented as `dict` in JSON). """
        
        self.procedure = None
        """ Clinical procedures performed.
        List of `ExplanationOfBenefitProcedure` items (represented as `dict` in JSON). """
        
        self.precedence = None
        """ Precedence (primary, secondary, etc.).
        Type `int`. """
        
        self.insurance = None
        """ Patient insurance information.
        List of `ExplanationOfBenefitInsurance` items (represented as `dict` in JSON). """
        
        self.accident = None
        """ Details of the event.
        Type `ExplanationOfBenefitAccident` (represented as `dict` in JSON). """
        
        self.item = None
        """ Product or service provided.
        List of `ExplanationOfBenefitItem` items (represented as `dict` in JSON). """
        
        self.addItem = None
        """ Insurer added line items.
        List of `ExplanationOfBenefitAddItem` items (represented as `dict` in JSON). """
        
        self.adjudication = None
        """ Header-level adjudication.
        List of `ExplanationOfBenefitItemAdjudication` items (represented as `dict` in JSON). """
        
        self.total = None
        """ Adjudication totals.
        List of `ExplanationOfBenefitTotal` items (represented as `dict` in JSON). """
        
        self.payment = None
        """ Payment Details.
        Type `ExplanationOfBenefitPayment` (represented as `dict` in JSON). """
        
        self.formCode = None
        """ Printed form identifier.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.form = None
        """ Printed reference or actual form.
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.processNote = None
        """ Note concerning adjudication.
        List of `ExplanationOfBenefitProcessNote` items (represented as `dict` in JSON). """
        
        self.benefitPeriod = None
        """ When the benefits are applicable.
        Type `Period` (represented as `dict` in JSON). """
        
        self.benefitBalance = None
        """ Balance by Benefit Category.
        List of `ExplanationOfBenefitBenefitBalance` items (represented as `dict` in JSON). """
        
        super(ExplanationOfBenefit, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExplanationOfBenefit, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("subType", "subType", codeableconcept.CodeableConcept, False, None, False),
            ("use", "use", str, False, None, True),
            ("patient", "patient", fhirreference.FHIRReference, False, None, True),
            ("billablePeriod", "billablePeriod", period.Period, False, None, False),
            ("created", "created", fhirdate.FHIRDate, False, None, True),
            ("enterer", "enterer", fhirreference.FHIRReference, False, None, False),
            ("insurer", "insurer", fhirreference.FHIRReference, False, None, True),
            ("provider", "provider", fhirreference.FHIRReference, False, None, True),
            ("priority", "priority", codeableconcept.CodeableConcept, False, None, False),
            ("fundsReserveRequested", "fundsReserveRequested", codeableconcept.CodeableConcept, False, None, False),
            ("fundsReserve", "fundsReserve", codeableconcept.CodeableConcept, False, None, False),
            ("related", "related", ExplanationOfBenefitRelated, True, None, False),
            ("prescription", "prescription", fhirreference.FHIRReference, False, None, False),
            ("originalPrescription", "originalPrescription", fhirreference.FHIRReference, False, None, False),
            ("payee", "payee", ExplanationOfBenefitPayee, False, None, False),
            ("referral", "referral", fhirreference.FHIRReference, False, None, False),
            ("facility", "facility", fhirreference.FHIRReference, False, None, False),
            ("claim", "claim", fhirreference.FHIRReference, False, None, False),
            ("claimResponse", "claimResponse", fhirreference.FHIRReference, False, None, False),
            ("outcome", "outcome", str, False, None, True),
            ("disposition", "disposition", str, False, None, False),
            ("preAuthRef", "preAuthRef", str, True, None, False),
            ("preAuthRefPeriod", "preAuthRefPeriod", period.Period, True, None, False),
            ("careTeam", "careTeam", ExplanationOfBenefitCareTeam, True, None, False),
            ("supportingInfo", "supportingInfo", ExplanationOfBenefitSupportingInfo, True, None, False),
            ("diagnosis", "diagnosis", ExplanationOfBenefitDiagnosis, True, None, False),
            ("procedure", "procedure", ExplanationOfBenefitProcedure, True, None, False),
            ("precedence", "precedence", int, False, None, False),
            ("insurance", "insurance", ExplanationOfBenefitInsurance, True, None, True),
            ("accident", "accident", ExplanationOfBenefitAccident, False, None, False),
            ("item", "item", ExplanationOfBenefitItem, True, None, False),
            ("addItem", "addItem", ExplanationOfBenefitAddItem, True, None, False),
            ("adjudication", "adjudication", ExplanationOfBenefitItemAdjudication, True, None, False),
            ("total", "total", ExplanationOfBenefitTotal, True, None, False),
            ("payment", "payment", ExplanationOfBenefitPayment, False, None, False),
            ("formCode", "formCode", codeableconcept.CodeableConcept, False, None, False),
            ("form", "form", attachment.Attachment, False, None, False),
            ("processNote", "processNote", ExplanationOfBenefitProcessNote, True, None, False),
            ("benefitPeriod", "benefitPeriod", period.Period, False, None, False),
            ("benefitBalance", "benefitBalance", ExplanationOfBenefitBenefitBalance, True, None, False),
        ])
        return js


from . import backboneelement

class ExplanationOfBenefitAccident(backboneelement.BackboneElement):
    """ Details of the event.
    
    Details of a accident which resulted in injuries which required the
    products and services listed in the claim.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['date'] = """When the incident occurred."""
    _attribute_docstrings['type'] = """The nature of the accident."""
    _attribute_docstrings['locationAddress'] = """Where the event occurred."""
    _attribute_docstrings['locationReference'] = """Where the event occurred."""

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
        
        self.date = None
        """ When the incident occurred.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.type = None
        """ The nature of the accident.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.locationAddress = None
        """ Where the event occurred.
        Type `Address` (represented as `dict` in JSON). """
        
        self.locationReference = None
        """ Where the event occurred.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(ExplanationOfBenefitAccident, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExplanationOfBenefitAccident, self).elementProperties()
        js.extend([
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("locationAddress", "locationAddress", address.Address, False, "location", False),
            ("locationReference", "locationReference", fhirreference.FHIRReference, False, "location", False),
        ])
        return js


class ExplanationOfBenefitAddItem(backboneelement.BackboneElement):
    """ Insurer added line items.
    
    The first-tier service adjudications for payor added product or service
    lines.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['itemSequence'] = """Item sequence number."""
    _attribute_docstrings['detailSequence'] = """Detail sequence number."""
    _attribute_docstrings['subDetailSequence'] = """Subdetail sequence number."""
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
    _attribute_docstrings['detail'] = """Insurer added line items."""

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
        
        self.subDetailSequence = None
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
        List of `ExplanationOfBenefitItemAdjudication` items (represented as `dict` in JSON). """
        
        self.detail = None
        """ Insurer added line items.
        List of `ExplanationOfBenefitAddItemDetail` items (represented as `dict` in JSON). """
        
        super(ExplanationOfBenefitAddItem, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExplanationOfBenefitAddItem, self).elementProperties()
        js.extend([
            ("itemSequence", "itemSequence", int, True, None, False),
            ("detailSequence", "detailSequence", int, True, None, False),
            ("subDetailSequence", "subDetailSequence", int, True, None, False),
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
            ("adjudication", "adjudication", ExplanationOfBenefitItemAdjudication, True, None, False),
            ("detail", "detail", ExplanationOfBenefitAddItemDetail, True, None, False),
        ])
        return js


class ExplanationOfBenefitAddItemDetail(backboneelement.BackboneElement):
    """ Insurer added line items.
    
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
    _attribute_docstrings['adjudication'] = """Added items adjudication."""
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
        """ Added items adjudication.
        List of `ExplanationOfBenefitItemAdjudication` items (represented as `dict` in JSON). """
        
        self.subDetail = None
        """ Insurer added line items.
        List of `ExplanationOfBenefitAddItemDetailSubDetail` items (represented as `dict` in JSON). """
        
        super(ExplanationOfBenefitAddItemDetail, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExplanationOfBenefitAddItemDetail, self).elementProperties()
        js.extend([
            ("productOrService", "productOrService", codeableconcept.CodeableConcept, False, None, True),
            ("modifier", "modifier", codeableconcept.CodeableConcept, True, None, False),
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("unitPrice", "unitPrice", money.Money, False, None, False),
            ("factor", "factor", float, False, None, False),
            ("net", "net", money.Money, False, None, False),
            ("noteNumber", "noteNumber", int, True, None, False),
            ("adjudication", "adjudication", ExplanationOfBenefitItemAdjudication, True, None, False),
            ("subDetail", "subDetail", ExplanationOfBenefitAddItemDetailSubDetail, True, None, False),
        ])
        return js


class ExplanationOfBenefitAddItemDetailSubDetail(backboneelement.BackboneElement):
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
    _attribute_docstrings['adjudication'] = """Added items adjudication."""

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
        """ Added items adjudication.
        List of `ExplanationOfBenefitItemAdjudication` items (represented as `dict` in JSON). """
        
        super(ExplanationOfBenefitAddItemDetailSubDetail, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExplanationOfBenefitAddItemDetailSubDetail, self).elementProperties()
        js.extend([
            ("productOrService", "productOrService", codeableconcept.CodeableConcept, False, None, True),
            ("modifier", "modifier", codeableconcept.CodeableConcept, True, None, False),
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("unitPrice", "unitPrice", money.Money, False, None, False),
            ("factor", "factor", float, False, None, False),
            ("net", "net", money.Money, False, None, False),
            ("noteNumber", "noteNumber", int, True, None, False),
            ("adjudication", "adjudication", ExplanationOfBenefitItemAdjudication, True, None, False),
        ])
        return js


class ExplanationOfBenefitBenefitBalance(backboneelement.BackboneElement):
    """ Balance by Benefit Category.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['category'] = """Benefit classification."""
    _attribute_docstrings['excluded'] = """Excluded from the plan."""
    _attribute_docstrings['name'] = """Short name for the benefit."""
    _attribute_docstrings['description'] = """Description of the benefit or services covered."""
    _attribute_docstrings['network'] = """Is a flag to indicate whether the benefits refer to in-network providers or out-of-network providers."""
    _attribute_docstrings['unit'] = """Indicates if the benefits apply to an individual or to the family."""
    _attribute_docstrings['term'] = """The term or period of the values such as 'maximum lifetime benefit' or 'maximum annual visits'."""
    _attribute_docstrings['financial'] = """Benefit Summary."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
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
        
        self.financial = None
        """ Benefit Summary.
        List of `ExplanationOfBenefitBenefitBalanceFinancial` items (represented as `dict` in JSON). """
        
        super(ExplanationOfBenefitBenefitBalance, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExplanationOfBenefitBenefitBalance, self).elementProperties()
        js.extend([
            ("category", "category", codeableconcept.CodeableConcept, False, None, True),
            ("excluded", "excluded", bool, False, None, False),
            ("name", "name", str, False, None, False),
            ("description", "description", str, False, None, False),
            ("network", "network", codeableconcept.CodeableConcept, False, None, False),
            ("unit", "unit", codeableconcept.CodeableConcept, False, None, False),
            ("term", "term", codeableconcept.CodeableConcept, False, None, False),
            ("financial", "financial", ExplanationOfBenefitBenefitBalanceFinancial, True, None, False),
        ])
        return js


class ExplanationOfBenefitBenefitBalanceFinancial(backboneelement.BackboneElement):
    """ Benefit Summary.
    
    Benefits Used to date.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Classification of benefit being provided."""
    _attribute_docstrings['allowedUnsignedInt'] = """Benefits allowed."""
    _attribute_docstrings['allowedString'] = """Benefits allowed."""
    _attribute_docstrings['allowedMoney'] = """Benefits allowed."""
    _attribute_docstrings['usedUnsignedInt'] = """Benefits used."""
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
        
        self.usedMoney = None
        """ Benefits used.
        Type `Money` (represented as `dict` in JSON). """
        
        super(ExplanationOfBenefitBenefitBalanceFinancial, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExplanationOfBenefitBenefitBalanceFinancial, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("allowedUnsignedInt", "allowedUnsignedInt", int, False, "allowed", False),
            ("allowedString", "allowedString", str, False, "allowed", False),
            ("allowedMoney", "allowedMoney", money.Money, False, "allowed", False),
            ("usedUnsignedInt", "usedUnsignedInt", int, False, "used", False),
            ("usedMoney", "usedMoney", money.Money, False, "used", False),
        ])
        return js


class ExplanationOfBenefitCareTeam(backboneelement.BackboneElement):
    """ Care Team members.
    
    The members of the team who provided the products and services.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['sequence'] = """Order of care team."""
    _attribute_docstrings['provider'] = """Practitioner or organization."""
    _attribute_docstrings['responsible'] = """Indicator of the lead practitioner."""
    _attribute_docstrings['role'] = """The lead, assisting or supervising practitioner and their discipline if a multidisciplinary team."""
    _attribute_docstrings['qualification'] = """Practitioner credential or specialization."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['role'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/claimcareteamrole',
        'restricted_to': ['primary', 'assist', 'supervisor', 'other'],
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
        
        self.sequence = None
        """ Order of care team.
        Type `int`. """
        
        self.provider = None
        """ Practitioner or organization.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.responsible = None
        """ Indicator of the lead practitioner.
        Type `bool`. """
        
        self.role = None
        """ The lead, assisting or supervising practitioner and their
        discipline if a multidisciplinary team.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.qualification = None
        """ Practitioner credential or specialization.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(ExplanationOfBenefitCareTeam, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExplanationOfBenefitCareTeam, self).elementProperties()
        js.extend([
            ("sequence", "sequence", int, False, None, True),
            ("provider", "provider", fhirreference.FHIRReference, False, None, True),
            ("responsible", "responsible", bool, False, None, False),
            ("role", "role", codeableconcept.CodeableConcept, False, None, False),
            ("qualification", "qualification", codeableconcept.CodeableConcept, False, None, False),
        ])
        return js


class ExplanationOfBenefitDiagnosis(backboneelement.BackboneElement):
    """ Pertinent diagnosis information.
    
    Information about diagnoses relevant to the claim items.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['sequence'] = """Diagnosis instance identifier."""
    _attribute_docstrings['diagnosisCodeableConcept'] = """Nature of illness or problem."""
    _attribute_docstrings['diagnosisReference'] = """Nature of illness or problem."""
    _attribute_docstrings['type'] = """When the condition was observed or the relative ranking."""
    _attribute_docstrings['onAdmission'] = """Indication of whether the diagnosis was present on admission to a facility."""
    _attribute_docstrings['packageCode'] = """Package billing code."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/ex-diagnosistype',
        'restricted_to': ['admitting', 'clinical', 'differential', 'discharge', 'laboratory', 'nursing', 'prenatal', 'principal', 'radiology', 'remote', 'retrospective', 'self'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['onAdmission'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/ex-diagnosis-on-admission',
        'restricted_to': ['y', 'n', 'u', 'w'],
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
        
        self.sequence = None
        """ Diagnosis instance identifier.
        Type `int`. """
        
        self.diagnosisCodeableConcept = None
        """ Nature of illness or problem.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.diagnosisReference = None
        """ Nature of illness or problem.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.type = None
        """ When the condition was observed or the relative ranking.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.onAdmission = None
        """ Indication of whether the diagnosis was present on admission to a
        facility.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.packageCode = None
        """ Package billing code.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(ExplanationOfBenefitDiagnosis, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExplanationOfBenefitDiagnosis, self).elementProperties()
        js.extend([
            ("sequence", "sequence", int, False, None, True),
            ("diagnosisCodeableConcept", "diagnosisCodeableConcept", codeableconcept.CodeableConcept, False, "diagnosis", True),
            ("diagnosisReference", "diagnosisReference", fhirreference.FHIRReference, False, "diagnosis", True),
            ("type", "type", codeableconcept.CodeableConcept, True, None, False),
            ("onAdmission", "onAdmission", codeableconcept.CodeableConcept, False, None, False),
            ("packageCode", "packageCode", codeableconcept.CodeableConcept, False, None, False),
        ])
        return js


class ExplanationOfBenefitInsurance(backboneelement.BackboneElement):
    """ Patient insurance information.
    
    Financial instruments for reimbursement for the health care products and
    services specified on the claim.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['focal'] = """Coverage to be used for adjudication."""
    _attribute_docstrings['coverage'] = """Insurance information."""
    _attribute_docstrings['preAuthRef'] = """Prior authorization reference number."""

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
        """ Coverage to be used for adjudication.
        Type `bool`. """
        
        self.coverage = None
        """ Insurance information.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.preAuthRef = None
        """ Prior authorization reference number.
        List of `str` items. """
        
        super(ExplanationOfBenefitInsurance, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExplanationOfBenefitInsurance, self).elementProperties()
        js.extend([
            ("focal", "focal", bool, False, None, True),
            ("coverage", "coverage", fhirreference.FHIRReference, False, None, True),
            ("preAuthRef", "preAuthRef", str, True, None, False),
        ])
        return js


class ExplanationOfBenefitItem(backboneelement.BackboneElement):
    """ Product or service provided.
    
    A claim line. Either a simple (a product or service) or a 'group' of
    details which can also be a simple items or groups of sub-details.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['sequence'] = """Item instance identifier."""
    _attribute_docstrings['careTeamSequence'] = """Applicable care team members."""
    _attribute_docstrings['diagnosisSequence'] = """Applicable diagnoses."""
    _attribute_docstrings['procedureSequence'] = """Applicable procedures."""
    _attribute_docstrings['informationSequence'] = """Applicable exception and supporting information."""
    _attribute_docstrings['revenue'] = """Revenue or cost center code."""
    _attribute_docstrings['category'] = """Benefit classification."""
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
    _attribute_docstrings['udi'] = """Unique device identifier."""
    _attribute_docstrings['bodySite'] = """Anatomical location."""
    _attribute_docstrings['subSite'] = """A region or surface of the bodySite, e.g. limb region or tooth surface(s)."""
    _attribute_docstrings['encounter'] = """Encounters related to this billed item."""
    _attribute_docstrings['noteNumber'] = """Applicable note numbers."""
    _attribute_docstrings['adjudication'] = """Adjudication details."""
    _attribute_docstrings['detail'] = """Additional items."""

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
        
        self.sequence = None
        """ Item instance identifier.
        Type `int`. """
        
        self.careTeamSequence = None
        """ Applicable care team members.
        List of `int` items. """
        
        self.diagnosisSequence = None
        """ Applicable diagnoses.
        List of `int` items. """
        
        self.procedureSequence = None
        """ Applicable procedures.
        List of `int` items. """
        
        self.informationSequence = None
        """ Applicable exception and supporting information.
        List of `int` items. """
        
        self.revenue = None
        """ Revenue or cost center code.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
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
        
        self.udi = None
        """ Unique device identifier.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.bodySite = None
        """ Anatomical location.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subSite = None
        """ A region or surface of the bodySite, e.g. limb region or tooth
        surface(s).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Encounters related to this billed item.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.noteNumber = None
        """ Applicable note numbers.
        List of `int` items. """
        
        self.adjudication = None
        """ Adjudication details.
        List of `ExplanationOfBenefitItemAdjudication` items (represented as `dict` in JSON). """
        
        self.detail = None
        """ Additional items.
        List of `ExplanationOfBenefitItemDetail` items (represented as `dict` in JSON). """
        
        super(ExplanationOfBenefitItem, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExplanationOfBenefitItem, self).elementProperties()
        js.extend([
            ("sequence", "sequence", int, False, None, True),
            ("careTeamSequence", "careTeamSequence", int, True, None, False),
            ("diagnosisSequence", "diagnosisSequence", int, True, None, False),
            ("procedureSequence", "procedureSequence", int, True, None, False),
            ("informationSequence", "informationSequence", int, True, None, False),
            ("revenue", "revenue", codeableconcept.CodeableConcept, False, None, False),
            ("category", "category", codeableconcept.CodeableConcept, False, None, False),
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
            ("udi", "udi", fhirreference.FHIRReference, True, None, False),
            ("bodySite", "bodySite", codeableconcept.CodeableConcept, False, None, False),
            ("subSite", "subSite", codeableconcept.CodeableConcept, True, None, False),
            ("encounter", "encounter", fhirreference.FHIRReference, True, None, False),
            ("noteNumber", "noteNumber", int, True, None, False),
            ("adjudication", "adjudication", ExplanationOfBenefitItemAdjudication, True, None, False),
            ("detail", "detail", ExplanationOfBenefitItemDetail, True, None, False),
        ])
        return js


class ExplanationOfBenefitItemAdjudication(backboneelement.BackboneElement):
    """ Adjudication details.
    
    If this item is a group then the values here are a summary of the
    adjudication of the detail items. If this item is a simple product or
    service then this is the result of the adjudication of this item.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['category'] = """A code to indicate the information type of this adjudication record. Information types may include: the value submitted, maximum values or percentages allowed or payable under the plan, amounts that the patient is responsible for in-aggregate or pertaining to this item, amounts paid by other coverages, and the benefit payable for this item."""
    _attribute_docstrings['reason'] = """A code supporting the understanding of the adjudication result and explaining variance from expected amount."""
    _attribute_docstrings['amount'] = """Monetary amount."""
    _attribute_docstrings['value'] = """Non-monitary value."""

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
        record. Information types may include: the value submitted, maximum
        values or percentages allowed or payable under the plan, amounts
        that the patient is responsible for in-aggregate or pertaining to
        this item, amounts paid by other coverages, and the benefit payable
        for this item.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.reason = None
        """ A code supporting the understanding of the adjudication result and
        explaining variance from expected amount.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.amount = None
        """ Monetary amount.
        Type `Money` (represented as `dict` in JSON). """
        
        self.value = None
        """ Non-monitary value.
        Type `float`. """
        
        super(ExplanationOfBenefitItemAdjudication, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExplanationOfBenefitItemAdjudication, self).elementProperties()
        js.extend([
            ("category", "category", codeableconcept.CodeableConcept, False, None, True),
            ("reason", "reason", codeableconcept.CodeableConcept, False, None, False),
            ("amount", "amount", money.Money, False, None, False),
            ("value", "value", float, False, None, False),
        ])
        return js


class ExplanationOfBenefitItemDetail(backboneelement.BackboneElement):
    """ Additional items.
    
    Second-tier of goods and services.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['sequence'] = """Product or service provided."""
    _attribute_docstrings['revenue'] = """Revenue or cost center code."""
    _attribute_docstrings['category'] = """Benefit classification."""
    _attribute_docstrings['productOrService'] = """Billing, service, product, or drug code."""
    _attribute_docstrings['modifier'] = """Item typification or modifiers codes to convey additional context for the product or service."""
    _attribute_docstrings['programCode'] = """Identifies the program under which this may be recovered."""
    _attribute_docstrings['quantity'] = """Count of products or services."""
    _attribute_docstrings['unitPrice'] = """Fee, charge or cost per item."""
    _attribute_docstrings['factor'] = """Price scaling factor."""
    _attribute_docstrings['net'] = """Total item cost."""
    _attribute_docstrings['udi'] = """Unique device identifier."""
    _attribute_docstrings['noteNumber'] = """Applicable note numbers."""
    _attribute_docstrings['adjudication'] = """Detail level adjudication details."""
    _attribute_docstrings['subDetail'] = """Additional items."""

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
        """ Product or service provided.
        Type `int`. """
        
        self.revenue = None
        """ Revenue or cost center code.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
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
        
        self.programCode = None
        """ Identifies the program under which this may be recovered.
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
        
        self.udi = None
        """ Unique device identifier.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.noteNumber = None
        """ Applicable note numbers.
        List of `int` items. """
        
        self.adjudication = None
        """ Detail level adjudication details.
        List of `ExplanationOfBenefitItemAdjudication` items (represented as `dict` in JSON). """
        
        self.subDetail = None
        """ Additional items.
        List of `ExplanationOfBenefitItemDetailSubDetail` items (represented as `dict` in JSON). """
        
        super(ExplanationOfBenefitItemDetail, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExplanationOfBenefitItemDetail, self).elementProperties()
        js.extend([
            ("sequence", "sequence", int, False, None, True),
            ("revenue", "revenue", codeableconcept.CodeableConcept, False, None, False),
            ("category", "category", codeableconcept.CodeableConcept, False, None, False),
            ("productOrService", "productOrService", codeableconcept.CodeableConcept, False, None, True),
            ("modifier", "modifier", codeableconcept.CodeableConcept, True, None, False),
            ("programCode", "programCode", codeableconcept.CodeableConcept, True, None, False),
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("unitPrice", "unitPrice", money.Money, False, None, False),
            ("factor", "factor", float, False, None, False),
            ("net", "net", money.Money, False, None, False),
            ("udi", "udi", fhirreference.FHIRReference, True, None, False),
            ("noteNumber", "noteNumber", int, True, None, False),
            ("adjudication", "adjudication", ExplanationOfBenefitItemAdjudication, True, None, False),
            ("subDetail", "subDetail", ExplanationOfBenefitItemDetailSubDetail, True, None, False),
        ])
        return js


class ExplanationOfBenefitItemDetailSubDetail(backboneelement.BackboneElement):
    """ Additional items.
    
    Third-tier of goods and services.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['sequence'] = """Product or service provided."""
    _attribute_docstrings['revenue'] = """Revenue or cost center code."""
    _attribute_docstrings['category'] = """Benefit classification."""
    _attribute_docstrings['productOrService'] = """Billing, service, product, or drug code."""
    _attribute_docstrings['modifier'] = """Item typification or modifiers codes to convey additional context for the product or service."""
    _attribute_docstrings['programCode'] = """Identifies the program under which this may be recovered."""
    _attribute_docstrings['quantity'] = """Count of products or services."""
    _attribute_docstrings['unitPrice'] = """Fee, charge or cost per item."""
    _attribute_docstrings['factor'] = """Price scaling factor."""
    _attribute_docstrings['net'] = """Total item cost."""
    _attribute_docstrings['udi'] = """Unique device identifier."""
    _attribute_docstrings['noteNumber'] = """Applicable note numbers."""
    _attribute_docstrings['adjudication'] = """Subdetail level adjudication details."""

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
        """ Product or service provided.
        Type `int`. """
        
        self.revenue = None
        """ Revenue or cost center code.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
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
        
        self.programCode = None
        """ Identifies the program under which this may be recovered.
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
        
        self.udi = None
        """ Unique device identifier.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.noteNumber = None
        """ Applicable note numbers.
        List of `int` items. """
        
        self.adjudication = None
        """ Subdetail level adjudication details.
        List of `ExplanationOfBenefitItemAdjudication` items (represented as `dict` in JSON). """
        
        super(ExplanationOfBenefitItemDetailSubDetail, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExplanationOfBenefitItemDetailSubDetail, self).elementProperties()
        js.extend([
            ("sequence", "sequence", int, False, None, True),
            ("revenue", "revenue", codeableconcept.CodeableConcept, False, None, False),
            ("category", "category", codeableconcept.CodeableConcept, False, None, False),
            ("productOrService", "productOrService", codeableconcept.CodeableConcept, False, None, True),
            ("modifier", "modifier", codeableconcept.CodeableConcept, True, None, False),
            ("programCode", "programCode", codeableconcept.CodeableConcept, True, None, False),
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("unitPrice", "unitPrice", money.Money, False, None, False),
            ("factor", "factor", float, False, None, False),
            ("net", "net", money.Money, False, None, False),
            ("udi", "udi", fhirreference.FHIRReference, True, None, False),
            ("noteNumber", "noteNumber", int, True, None, False),
            ("adjudication", "adjudication", ExplanationOfBenefitItemAdjudication, True, None, False),
        ])
        return js


class ExplanationOfBenefitPayee(backboneelement.BackboneElement):
    """ Recipient of benefits payable.
    
    The party to be reimbursed for cost of the products and services according
    to the terms of the policy.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Category of recipient."""
    _attribute_docstrings['party'] = """Recipient reference."""

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
        """ Category of recipient.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.party = None
        """ Recipient reference.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(ExplanationOfBenefitPayee, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExplanationOfBenefitPayee, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("party", "party", fhirreference.FHIRReference, False, None, False),
        ])
        return js


class ExplanationOfBenefitPayment(backboneelement.BackboneElement):
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
        
        super(ExplanationOfBenefitPayment, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExplanationOfBenefitPayment, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("adjustment", "adjustment", money.Money, False, None, False),
            ("adjustmentReason", "adjustmentReason", codeableconcept.CodeableConcept, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("amount", "amount", money.Money, False, None, False),
            ("identifier", "identifier", identifier.Identifier, False, None, False),
        ])
        return js


class ExplanationOfBenefitProcedure(backboneelement.BackboneElement):
    """ Clinical procedures performed.
    
    Procedures performed on the patient relevant to the billing items with the
    claim.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['sequence'] = """Procedure instance identifier."""
    _attribute_docstrings['type'] = """When the condition was observed or the relative ranking."""
    _attribute_docstrings['date'] = """When the procedure was performed."""
    _attribute_docstrings['procedureCodeableConcept'] = """Specific clinical procedure."""
    _attribute_docstrings['procedureReference'] = """Specific clinical procedure."""
    _attribute_docstrings['udi'] = """Unique device identifier."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/ex-procedure-type',
        'restricted_to': ['primary', 'secondary'],
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
        
        self.sequence = None
        """ Procedure instance identifier.
        Type `int`. """
        
        self.type = None
        """ When the condition was observed or the relative ranking.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.date = None
        """ When the procedure was performed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.procedureCodeableConcept = None
        """ Specific clinical procedure.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.procedureReference = None
        """ Specific clinical procedure.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.udi = None
        """ Unique device identifier.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(ExplanationOfBenefitProcedure, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExplanationOfBenefitProcedure, self).elementProperties()
        js.extend([
            ("sequence", "sequence", int, False, None, True),
            ("type", "type", codeableconcept.CodeableConcept, True, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("procedureCodeableConcept", "procedureCodeableConcept", codeableconcept.CodeableConcept, False, "procedure", True),
            ("procedureReference", "procedureReference", fhirreference.FHIRReference, False, "procedure", True),
            ("udi", "udi", fhirreference.FHIRReference, True, None, False),
        ])
        return js


class ExplanationOfBenefitProcessNote(backboneelement.BackboneElement):
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
        
        super(ExplanationOfBenefitProcessNote, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExplanationOfBenefitProcessNote, self).elementProperties()
        js.extend([
            ("number", "number", int, False, None, False),
            ("type", "type", str, False, None, False),
            ("text", "text", str, False, None, False),
            ("language", "language", codeableconcept.CodeableConcept, False, None, False),
        ])
        return js


class ExplanationOfBenefitRelated(backboneelement.BackboneElement):
    """ Prior or corollary claims.
    
    Other claims which are related to this claim such as prior submissions or
    claims for related services or for the same event.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['claim'] = """Reference to the related claim."""
    _attribute_docstrings['relationship'] = """A code to convey how the claims are related."""
    _attribute_docstrings['reference'] = """File or case reference."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['relationship'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/ex-relatedclaimrelationship',
        'restricted_to': ['prior', 'associated'],
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
        
        self.claim = None
        """ Reference to the related claim.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.relationship = None
        """ A code to convey how the claims are related.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.reference = None
        """ File or case reference.
        Type `Identifier` (represented as `dict` in JSON). """
        
        super(ExplanationOfBenefitRelated, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExplanationOfBenefitRelated, self).elementProperties()
        js.extend([
            ("claim", "claim", fhirreference.FHIRReference, False, None, False),
            ("relationship", "relationship", codeableconcept.CodeableConcept, False, None, False),
            ("reference", "reference", identifier.Identifier, False, None, False),
        ])
        return js


class ExplanationOfBenefitSupportingInfo(backboneelement.BackboneElement):
    """ Supporting information.
    
    Additional information codes regarding exceptions, special considerations,
    the condition, situation, prior or concurrent issues.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['sequence'] = """Information instance identifier."""
    _attribute_docstrings['category'] = """The general class of the information supplied: information; exception; accident, employment; onset, etc."""
    _attribute_docstrings['code'] = """System and code pertaining to the specific information regarding special conditions relating to the setting, treatment or patient  for which care is sought."""
    _attribute_docstrings['timingDate'] = """When it occurred."""
    _attribute_docstrings['timingPeriod'] = """When it occurred."""
    _attribute_docstrings['valueBoolean'] = """Data to be provided."""
    _attribute_docstrings['valueString'] = """Data to be provided."""
    _attribute_docstrings['valueQuantity'] = """Data to be provided."""
    _attribute_docstrings['valueAttachment'] = """Data to be provided."""
    _attribute_docstrings['valueReference'] = """Data to be provided."""
    _attribute_docstrings['reason'] = """Explanation for the information."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['category'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/claiminformationcategory',
        'restricted_to': ['info', 'discharge', 'onset', 'related', 'exception', 'material', 'attachment', 'missingtooth', 'prosthesis', 'other', 'hospitalized', 'employmentimpacted', 'externalcause', 'patientreasonforvisit'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['code'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/claim-exception',
        'restricted_to': ['student', 'disabled'],
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
        
        self.sequence = None
        """ Information instance identifier.
        Type `int`. """
        
        self.category = None
        """ The general class of the information supplied: information;
        exception; accident, employment; onset, etc.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.code = None
        """ System and code pertaining to the specific information regarding
        special conditions relating to the setting, treatment or patient
        for which care is sought.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.timingDate = None
        """ When it occurred.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.timingPeriod = None
        """ When it occurred.
        Type `Period` (represented as `dict` in JSON). """
        
        self.valueBoolean = None
        """ Data to be provided.
        Type `bool`. """
        
        self.valueString = None
        """ Data to be provided.
        Type `str`. """
        
        self.valueQuantity = None
        """ Data to be provided.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.valueAttachment = None
        """ Data to be provided.
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.valueReference = None
        """ Data to be provided.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.reason = None
        """ Explanation for the information.
        Type `Coding` (represented as `dict` in JSON). """
        
        super(ExplanationOfBenefitSupportingInfo, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExplanationOfBenefitSupportingInfo, self).elementProperties()
        js.extend([
            ("sequence", "sequence", int, False, None, True),
            ("category", "category", codeableconcept.CodeableConcept, False, None, True),
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("timingDate", "timingDate", fhirdate.FHIRDate, False, "timing", False),
            ("timingPeriod", "timingPeriod", period.Period, False, "timing", False),
            ("valueBoolean", "valueBoolean", bool, False, "value", False),
            ("valueString", "valueString", str, False, "value", False),
            ("valueQuantity", "valueQuantity", quantity.Quantity, False, "value", False),
            ("valueAttachment", "valueAttachment", attachment.Attachment, False, "value", False),
            ("valueReference", "valueReference", fhirreference.FHIRReference, False, "value", False),
            ("reason", "reason", coding.Coding, False, None, False),
        ])
        return js


class ExplanationOfBenefitTotal(backboneelement.BackboneElement):
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
        
        super(ExplanationOfBenefitTotal, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ExplanationOfBenefitTotal, self).elementProperties()
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
    from . import coding
except ImportError:
    coding = sys.modules[__package__ + '.coding']
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
