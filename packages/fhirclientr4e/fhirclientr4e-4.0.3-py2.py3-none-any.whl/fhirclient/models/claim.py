#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Claim) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Claim(domainresource.DomainResource):
    """ Claim, Pre-determination or Pre-authorization.
    
    A provider issued list of professional services and products which have
    been provided, or are to be provided, to a patient which is sent to an
    insurer for reimbursement.
    """
    
    resource_type = "Claim"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business Identifier for claim."""
    _attribute_docstrings['status'] = """The status of the resource instance."""
    _attribute_docstrings['type'] = """The category of claim, e.g. oral, pharmacy, vision, institutional, professional."""
    _attribute_docstrings['subType'] = """A finer grained suite of claim type codes which may convey additional information such as Inpatient vs Outpatient and/or a specialty service."""
    _attribute_docstrings['use'] = """A code to indicate whether the nature of the request is: to request adjudication of products and services previously rendered; or requesting authorization and adjudication for provision in the future; or requesting the non-binding adjudication of the listed products and services which could be provided in the future."""
    _attribute_docstrings['patient'] = """The recipient of the products and services."""
    _attribute_docstrings['billablePeriod'] = """Relevant time frame for the claim."""
    _attribute_docstrings['created'] = """Resource creation date."""
    _attribute_docstrings['enterer'] = """Author of the claim."""
    _attribute_docstrings['insurer'] = """Target."""
    _attribute_docstrings['provider'] = """Party responsible for the claim."""
    _attribute_docstrings['priority'] = """The provider-required urgency of processing the request. Typical values include: stat, routine deferred."""
    _attribute_docstrings['fundsReserve'] = """For whom to reserve funds."""
    _attribute_docstrings['related'] = """Prior or corollary claims."""
    _attribute_docstrings['prescription'] = """Prescription authorizing services and products."""
    _attribute_docstrings['originalPrescription'] = """Original prescription if superseded by fulfiller."""
    _attribute_docstrings['payee'] = """Recipient of benefits payable."""
    _attribute_docstrings['referral'] = """Treatment referral."""
    _attribute_docstrings['facility'] = """Servicing facility."""
    _attribute_docstrings['careTeam'] = """Members of the care team."""
    _attribute_docstrings['supportingInfo'] = """Supporting information."""
    _attribute_docstrings['diagnosis'] = """Pertinent diagnosis information."""
    _attribute_docstrings['procedure'] = """Clinical procedures performed."""
    _attribute_docstrings['insurance'] = """Patient insurance information."""
    _attribute_docstrings['accident'] = """Details of the event."""
    _attribute_docstrings['item'] = """Product or service provided."""
    _attribute_docstrings['total'] = """Total claim cost."""

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
    _attribute_enums['priority'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/processpriority',
        'restricted_to': ['stat', 'normal', 'deferred'],
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
        """ Business Identifier for claim.
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
        """ Resource creation date.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.enterer = None
        """ Author of the claim.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.insurer = None
        """ Target.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.provider = None
        """ Party responsible for the claim.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.priority = None
        """ The provider-required urgency of processing the request. Typical
        values include: stat, routine deferred.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.fundsReserve = None
        """ For whom to reserve funds.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.related = None
        """ Prior or corollary claims.
        List of `ClaimRelated` items (represented as `dict` in JSON). """
        
        self.prescription = None
        """ Prescription authorizing services and products.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.originalPrescription = None
        """ Original prescription if superseded by fulfiller.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.payee = None
        """ Recipient of benefits payable.
        Type `ClaimPayee` (represented as `dict` in JSON). """
        
        self.referral = None
        """ Treatment referral.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.facility = None
        """ Servicing facility.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.careTeam = None
        """ Members of the care team.
        List of `ClaimCareTeam` items (represented as `dict` in JSON). """
        
        self.supportingInfo = None
        """ Supporting information.
        List of `ClaimSupportingInfo` items (represented as `dict` in JSON). """
        
        self.diagnosis = None
        """ Pertinent diagnosis information.
        List of `ClaimDiagnosis` items (represented as `dict` in JSON). """
        
        self.procedure = None
        """ Clinical procedures performed.
        List of `ClaimProcedure` items (represented as `dict` in JSON). """
        
        self.insurance = None
        """ Patient insurance information.
        List of `ClaimInsurance` items (represented as `dict` in JSON). """
        
        self.accident = None
        """ Details of the event.
        Type `ClaimAccident` (represented as `dict` in JSON). """
        
        self.item = None
        """ Product or service provided.
        List of `ClaimItem` items (represented as `dict` in JSON). """
        
        self.total = None
        """ Total claim cost.
        Type `Money` (represented as `dict` in JSON). """
        
        super(Claim, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Claim, self).elementProperties()
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
            ("insurer", "insurer", fhirreference.FHIRReference, False, None, False),
            ("provider", "provider", fhirreference.FHIRReference, False, None, True),
            ("priority", "priority", codeableconcept.CodeableConcept, False, None, True),
            ("fundsReserve", "fundsReserve", codeableconcept.CodeableConcept, False, None, False),
            ("related", "related", ClaimRelated, True, None, False),
            ("prescription", "prescription", fhirreference.FHIRReference, False, None, False),
            ("originalPrescription", "originalPrescription", fhirreference.FHIRReference, False, None, False),
            ("payee", "payee", ClaimPayee, False, None, False),
            ("referral", "referral", fhirreference.FHIRReference, False, None, False),
            ("facility", "facility", fhirreference.FHIRReference, False, None, False),
            ("careTeam", "careTeam", ClaimCareTeam, True, None, False),
            ("supportingInfo", "supportingInfo", ClaimSupportingInfo, True, None, False),
            ("diagnosis", "diagnosis", ClaimDiagnosis, True, None, False),
            ("procedure", "procedure", ClaimProcedure, True, None, False),
            ("insurance", "insurance", ClaimInsurance, True, None, True),
            ("accident", "accident", ClaimAccident, False, None, False),
            ("item", "item", ClaimItem, True, None, False),
            ("total", "total", money.Money, False, None, False),
        ])
        return js


from . import backboneelement

class ClaimAccident(backboneelement.BackboneElement):
    """ Details of the event.
    
    Details of an accident which resulted in injuries which required the
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
        
        super(ClaimAccident, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimAccident, self).elementProperties()
        js.extend([
            ("date", "date", fhirdate.FHIRDate, False, None, True),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("locationAddress", "locationAddress", address.Address, False, "location", False),
            ("locationReference", "locationReference", fhirreference.FHIRReference, False, "location", False),
        ])
        return js


class ClaimCareTeam(backboneelement.BackboneElement):
    """ Members of the care team.
    
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
        
        super(ClaimCareTeam, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimCareTeam, self).elementProperties()
        js.extend([
            ("sequence", "sequence", int, False, None, True),
            ("provider", "provider", fhirreference.FHIRReference, False, None, True),
            ("responsible", "responsible", bool, False, None, False),
            ("role", "role", codeableconcept.CodeableConcept, False, None, False),
            ("qualification", "qualification", codeableconcept.CodeableConcept, False, None, False),
        ])
        return js


class ClaimDiagnosis(backboneelement.BackboneElement):
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
        
        super(ClaimDiagnosis, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimDiagnosis, self).elementProperties()
        js.extend([
            ("sequence", "sequence", int, False, None, True),
            ("diagnosisCodeableConcept", "diagnosisCodeableConcept", codeableconcept.CodeableConcept, False, "diagnosis", True),
            ("diagnosisReference", "diagnosisReference", fhirreference.FHIRReference, False, "diagnosis", True),
            ("type", "type", codeableconcept.CodeableConcept, True, None, False),
            ("onAdmission", "onAdmission", codeableconcept.CodeableConcept, False, None, False),
            ("packageCode", "packageCode", codeableconcept.CodeableConcept, False, None, False),
        ])
        return js


class ClaimInsurance(backboneelement.BackboneElement):
    """ Patient insurance information.
    
    Financial instruments for reimbursement for the health care products and
    services specified on the claim.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['sequence'] = """Insurance instance identifier."""
    _attribute_docstrings['focal'] = """Coverage to be used for adjudication."""
    _attribute_docstrings['identifier'] = """Pre-assigned Claim number."""
    _attribute_docstrings['coverage'] = """Insurance information."""
    _attribute_docstrings['businessArrangement'] = """Additional provider contract number."""
    _attribute_docstrings['preAuthRef'] = """Prior authorization reference number."""
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
        
        self.identifier = None
        """ Pre-assigned Claim number.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.coverage = None
        """ Insurance information.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.businessArrangement = None
        """ Additional provider contract number.
        Type `str`. """
        
        self.preAuthRef = None
        """ Prior authorization reference number.
        List of `str` items. """
        
        self.claimResponse = None
        """ Adjudication results.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(ClaimInsurance, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimInsurance, self).elementProperties()
        js.extend([
            ("sequence", "sequence", int, False, None, True),
            ("focal", "focal", bool, False, None, True),
            ("identifier", "identifier", identifier.Identifier, False, None, False),
            ("coverage", "coverage", fhirreference.FHIRReference, False, None, True),
            ("businessArrangement", "businessArrangement", str, False, None, False),
            ("preAuthRef", "preAuthRef", str, True, None, False),
            ("claimResponse", "claimResponse", fhirreference.FHIRReference, False, None, False),
        ])
        return js


class ClaimItem(backboneelement.BackboneElement):
    """ Product or service provided.
    
    A claim line. Either a simple  product or service or a 'group' of details
    which can each be a simple items or groups of sub-details.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['sequence'] = """Item instance identifier."""
    _attribute_docstrings['careTeamSequence'] = """Applicable careTeam members."""
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
    _attribute_docstrings['detail'] = """Product or service provided."""

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
        """ Applicable careTeam members.
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
        
        self.detail = None
        """ Product or service provided.
        List of `ClaimItemDetail` items (represented as `dict` in JSON). """
        
        super(ClaimItem, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimItem, self).elementProperties()
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
            ("detail", "detail", ClaimItemDetail, True, None, False),
        ])
        return js


class ClaimItemDetail(backboneelement.BackboneElement):
    """ Product or service provided.
    
    A claim detail line. Either a simple (a product or service) or a 'group' of
    sub-details which are simple items.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['sequence'] = """Item instance identifier."""
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
    _attribute_docstrings['subDetail'] = """Product or service provided."""

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
        """ Item instance identifier.
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
        
        self.subDetail = None
        """ Product or service provided.
        List of `ClaimItemDetailSubDetail` items (represented as `dict` in JSON). """
        
        super(ClaimItemDetail, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimItemDetail, self).elementProperties()
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
            ("subDetail", "subDetail", ClaimItemDetailSubDetail, True, None, False),
        ])
        return js


class ClaimItemDetailSubDetail(backboneelement.BackboneElement):
    """ Product or service provided.
    
    A claim detail line. Either a simple (a product or service) or a 'group' of
    sub-details which are simple items.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['sequence'] = """Item instance identifier."""
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
        """ Item instance identifier.
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
        
        super(ClaimItemDetailSubDetail, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimItemDetailSubDetail, self).elementProperties()
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
        ])
        return js


class ClaimPayee(backboneelement.BackboneElement):
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
        
        super(ClaimPayee, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimPayee, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("party", "party", fhirreference.FHIRReference, False, None, False),
        ])
        return js


class ClaimProcedure(backboneelement.BackboneElement):
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
        
        super(ClaimProcedure, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimProcedure, self).elementProperties()
        js.extend([
            ("sequence", "sequence", int, False, None, True),
            ("type", "type", codeableconcept.CodeableConcept, True, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("procedureCodeableConcept", "procedureCodeableConcept", codeableconcept.CodeableConcept, False, "procedure", True),
            ("procedureReference", "procedureReference", fhirreference.FHIRReference, False, "procedure", True),
            ("udi", "udi", fhirreference.FHIRReference, True, None, False),
        ])
        return js


class ClaimRelated(backboneelement.BackboneElement):
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
        
        super(ClaimRelated, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimRelated, self).elementProperties()
        js.extend([
            ("claim", "claim", fhirreference.FHIRReference, False, None, False),
            ("relationship", "relationship", codeableconcept.CodeableConcept, False, None, False),
            ("reference", "reference", identifier.Identifier, False, None, False),
        ])
        return js


class ClaimSupportingInfo(backboneelement.BackboneElement):
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
    _attribute_docstrings['reason'] = """Provides the reason in the situation where a reason code is required in addition to the content."""

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
    _attribute_enums['reason'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/missingtoothreason',
        'restricted_to': ['e', 'c', 'u', 'o'],
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
        """ Provides the reason in the situation where a reason code is
        required in addition to the content.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(ClaimSupportingInfo, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ClaimSupportingInfo, self).elementProperties()
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
            ("reason", "reason", codeableconcept.CodeableConcept, False, None, False),
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
