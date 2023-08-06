#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/ChargeItem) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class ChargeItem(domainresource.DomainResource):
    """ Item containing charge code(s) associated with the provision of healthcare
    provider products.
    
    The resource ChargeItem describes the provision of healthcare provider
    products for a certain patient, therefore referring not only to the
    product, but containing in addition details of the provision, like date,
    time, amounts and participating organizations and persons. Main Usage of
    the ChargeItem is to enable the billing process and internal cost
    allocation.
    """
    
    resource_type = "ChargeItem"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business Identifier for item."""
    _attribute_docstrings['definitionUri'] = """Defining information about the code of this charge item."""
    _attribute_docstrings['definitionCanonical'] = """Resource defining the code of this ChargeItem."""
    _attribute_docstrings['status'] = """The current state of the ChargeItem."""
    _attribute_docstrings['partOf'] = """Part of referenced ChargeItem."""
    _attribute_docstrings['code'] = """A code that identifies the charge, like a billing code."""
    _attribute_docstrings['subject'] = """Individual service was done for/to."""
    _attribute_docstrings['context'] = """Encounter / Episode associated with event."""
    _attribute_docstrings['occurrenceDateTime'] = """When the charged service was applied."""
    _attribute_docstrings['occurrencePeriod'] = """When the charged service was applied."""
    _attribute_docstrings['occurrenceTiming'] = """When the charged service was applied."""
    _attribute_docstrings['performer'] = """Who performed charged service."""
    _attribute_docstrings['performingOrganization'] = """Organization providing the charged service."""
    _attribute_docstrings['requestingOrganization'] = """Organization requesting the charged service."""
    _attribute_docstrings['costCenter'] = """Organization that has ownership of the (potential, future) revenue."""
    _attribute_docstrings['quantity'] = """Quantity of which the charge item has been serviced."""
    _attribute_docstrings['bodysite'] = """Anatomical location, if relevant."""
    _attribute_docstrings['factorOverride'] = """Factor overriding the associated rules."""
    _attribute_docstrings['priceOverride'] = """Price overriding the associated rules."""
    _attribute_docstrings['overrideReason'] = """Reason for overriding the list price/factor."""
    _attribute_docstrings['enterer'] = """Individual who was entering."""
    _attribute_docstrings['enteredDate'] = """Date the charge item was entered."""
    _attribute_docstrings['reason'] = """Why was the charged  service rendered?."""
    _attribute_docstrings['service'] = """Which rendered service is being charged?."""
    _attribute_docstrings['productReference'] = """Product charged."""
    _attribute_docstrings['productCodeableConcept'] = """Product charged."""
    _attribute_docstrings['account'] = """Account to place this charge."""
    _attribute_docstrings['note'] = """Comments made about the ChargeItem."""
    _attribute_docstrings['supportingInformation'] = """Further information supporting this charge."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/chargeitem-status',
        'restricted_to': ['planned', 'billable', 'not-billable', 'aborted', 'billed', 'entered-in-error', 'unknown'],
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
        
        self.definitionUri = None
        """ Defining information about the code of this charge item.
        List of `str` items. """
        
        self.definitionCanonical = None
        """ Resource defining the code of this ChargeItem.
        List of `str` items. """
        
        self.status = None
        """ The current state of the ChargeItem.
        Type `str`. """
        
        self.partOf = None
        """ Part of referenced ChargeItem.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.code = None
        """ A code that identifies the charge, like a billing code.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subject = None
        """ Individual service was done for/to.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.context = None
        """ Encounter / Episode associated with event.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.occurrenceDateTime = None
        """ When the charged service was applied.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.occurrencePeriod = None
        """ When the charged service was applied.
        Type `Period` (represented as `dict` in JSON). """
        
        self.occurrenceTiming = None
        """ When the charged service was applied.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.performer = None
        """ Who performed charged service.
        List of `ChargeItemPerformer` items (represented as `dict` in JSON). """
        
        self.performingOrganization = None
        """ Organization providing the charged service.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.requestingOrganization = None
        """ Organization requesting the charged service.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.costCenter = None
        """ Organization that has ownership of the (potential, future) revenue.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.quantity = None
        """ Quantity of which the charge item has been serviced.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.bodysite = None
        """ Anatomical location, if relevant.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.factorOverride = None
        """ Factor overriding the associated rules.
        Type `float`. """
        
        self.priceOverride = None
        """ Price overriding the associated rules.
        Type `Money` (represented as `dict` in JSON). """
        
        self.overrideReason = None
        """ Reason for overriding the list price/factor.
        Type `str`. """
        
        self.enterer = None
        """ Individual who was entering.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.enteredDate = None
        """ Date the charge item was entered.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.reason = None
        """ Why was the charged  service rendered?.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.service = None
        """ Which rendered service is being charged?.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.productReference = None
        """ Product charged.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.productCodeableConcept = None
        """ Product charged.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.account = None
        """ Account to place this charge.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.note = None
        """ Comments made about the ChargeItem.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        self.supportingInformation = None
        """ Further information supporting this charge.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(ChargeItem, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ChargeItem, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("definitionUri", "definitionUri", str, True, None, False),
            ("definitionCanonical", "definitionCanonical", str, True, None, False),
            ("status", "status", str, False, None, True),
            ("partOf", "partOf", fhirreference.FHIRReference, True, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, True),
            ("subject", "subject", fhirreference.FHIRReference, False, None, True),
            ("context", "context", fhirreference.FHIRReference, False, None, False),
            ("occurrenceDateTime", "occurrenceDateTime", fhirdate.FHIRDate, False, "occurrence", False),
            ("occurrencePeriod", "occurrencePeriod", period.Period, False, "occurrence", False),
            ("occurrenceTiming", "occurrenceTiming", timing.Timing, False, "occurrence", False),
            ("performer", "performer", ChargeItemPerformer, True, None, False),
            ("performingOrganization", "performingOrganization", fhirreference.FHIRReference, False, None, False),
            ("requestingOrganization", "requestingOrganization", fhirreference.FHIRReference, False, None, False),
            ("costCenter", "costCenter", fhirreference.FHIRReference, False, None, False),
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("bodysite", "bodysite", codeableconcept.CodeableConcept, True, None, False),
            ("factorOverride", "factorOverride", float, False, None, False),
            ("priceOverride", "priceOverride", money.Money, False, None, False),
            ("overrideReason", "overrideReason", str, False, None, False),
            ("enterer", "enterer", fhirreference.FHIRReference, False, None, False),
            ("enteredDate", "enteredDate", fhirdate.FHIRDate, False, None, False),
            ("reason", "reason", codeableconcept.CodeableConcept, True, None, False),
            ("service", "service", fhirreference.FHIRReference, True, None, False),
            ("productReference", "productReference", fhirreference.FHIRReference, False, "product", False),
            ("productCodeableConcept", "productCodeableConcept", codeableconcept.CodeableConcept, False, "product", False),
            ("account", "account", fhirreference.FHIRReference, True, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
            ("supportingInformation", "supportingInformation", fhirreference.FHIRReference, True, None, False),
        ])
        return js


from . import backboneelement

class ChargeItemPerformer(backboneelement.BackboneElement):
    """ Who performed charged service.
    
    Indicates who or what performed or participated in the charged service.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['function'] = """What type of performance was done."""
    _attribute_docstrings['actor'] = """Individual who was performing."""

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
        
        self.function = None
        """ What type of performance was done.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.actor = None
        """ Individual who was performing.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(ChargeItemPerformer, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ChargeItemPerformer, self).elementProperties()
        js.extend([
            ("function", "function", codeableconcept.CodeableConcept, False, None, False),
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
try:
    from . import period
except ImportError:
    period = sys.modules[__package__ + '.period']
try:
    from . import quantity
except ImportError:
    quantity = sys.modules[__package__ + '.quantity']
try:
    from . import timing
except ImportError:
    timing = sys.modules[__package__ + '.timing']
