#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/MedicationRequest) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class MedicationRequest(domainresource.DomainResource):
    """ Ordering of medication for patient or group.
    
    An order or request for both supply of the medication and the instructions
    for administration of the medication to a patient. The resource is called
    "MedicationRequest" rather than "MedicationPrescription" or
    "MedicationOrder" to generalize the use across inpatient and outpatient
    settings, including care plans, etc., and to harmonize with workflow
    patterns.
    """
    
    resource_type = "MedicationRequest"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """External ids for this request."""
    _attribute_docstrings['status'] = """A code specifying the current state of the order.  Generally, this will be active or completed state."""
    _attribute_docstrings['statusReason'] = """Captures the reason for the current state of the MedicationRequest."""
    _attribute_docstrings['intent'] = """Whether the request is a proposal, plan, or an original order."""
    _attribute_docstrings['category'] = """Indicates the type of medication request (for example, where the medication is expected to be consumed or administered (i.e. inpatient or outpatient))."""
    _attribute_docstrings['priority'] = """Indicates how quickly the Medication Request should be addressed with respect to other requests."""
    _attribute_docstrings['doNotPerform'] = """True if request is prohibiting action."""
    _attribute_docstrings['reportedBoolean'] = """Reported rather than primary record."""
    _attribute_docstrings['reportedReference'] = """Reported rather than primary record."""
    _attribute_docstrings['medicationCodeableConcept'] = """Medication to be taken."""
    _attribute_docstrings['medicationReference'] = """Medication to be taken."""
    _attribute_docstrings['subject'] = """Who or group medication request is for."""
    _attribute_docstrings['encounter'] = """Encounter created as part of encounter/admission/stay."""
    _attribute_docstrings['supportingInformation'] = """Information to support ordering of the medication."""
    _attribute_docstrings['authoredOn'] = """When request was initially authored."""
    _attribute_docstrings['requester'] = """Who/What requested the Request."""
    _attribute_docstrings['performer'] = """Intended performer of administration."""
    _attribute_docstrings['performerType'] = """Desired kind of performer of the medication administration."""
    _attribute_docstrings['recorder'] = """Person who entered the request."""
    _attribute_docstrings['reasonCode'] = """Reason or indication for ordering or not ordering the medication."""
    _attribute_docstrings['reasonReference'] = """Condition or observation that supports why the prescription is being written."""
    _attribute_docstrings['instantiatesCanonical'] = """Instantiates FHIR protocol or definition."""
    _attribute_docstrings['instantiatesUri'] = """Instantiates external protocol or definition."""
    _attribute_docstrings['basedOn'] = """What request fulfills."""
    _attribute_docstrings['groupIdentifier'] = """Composite request this is part of."""
    _attribute_docstrings['courseOfTherapyType'] = """The description of the overall patte3rn of the administration of the medication to the patient."""
    _attribute_docstrings['insurance'] = """Associated insurance coverage."""
    _attribute_docstrings['note'] = """Information about the prescription."""
    _attribute_docstrings['dosageInstruction'] = """How the medication should be taken."""
    _attribute_docstrings['dispenseRequest'] = """Medication supply authorization."""
    _attribute_docstrings['substitution'] = """Any restrictions on medication substitution."""
    _attribute_docstrings['priorPrescription'] = """An order/prescription that is being replaced."""
    _attribute_docstrings['detectedIssue'] = """Clinical Issue with action."""
    _attribute_docstrings['eventHistory'] = """A list of events of interest in the lifecycle."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/CodeSystem/medicationrequest-status',
        'restricted_to': ['active', 'on-hold', 'cancelled', 'completed', 'entered-in-error', 'stopped', 'draft', 'unknown'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['statusReason'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/medicationrequest-status-reason',
        'restricted_to': ['altchoice', 'clarif', 'drughigh', 'hospadm', 'labint', 'non-avail', 'preg', 'salg', 'sddi', 'sdupther', 'sintol', 'surg', 'washout'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['intent'] = {
        'url': 'http://hl7.org/fhir/CodeSystem/medicationrequest-intent',
        'restricted_to': ['proposal', 'plan', 'order', 'original-order', 'reflex-order', 'filler-order', 'instance-order', 'option'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['category'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/medicationrequest-category',
        'restricted_to': ['inpatient', 'outpatient', 'community', 'discharge'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['priority'] = {
        'url': 'http://hl7.org/fhir/request-priority',
        'restricted_to': ['routine', 'urgent', 'asap', 'stat'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['courseOfTherapyType'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/medicationrequest-course-of-therapy',
        'restricted_to': ['continuous', 'acute', 'seasonal'],
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
        """ External ids for this request.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ A code specifying the current state of the order.  Generally, this
        will be active or completed state.
        Type `str`. """
        
        self.statusReason = None
        """ Captures the reason for the current state of the MedicationRequest.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.intent = None
        """ Whether the request is a proposal, plan, or an original order.
        Type `str`. """
        
        self.category = None
        """ Indicates the type of medication request (for example, where the
        medication is expected to be consumed or administered (i.e.
        inpatient or outpatient)).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.priority = None
        """ Indicates how quickly the Medication Request should be addressed
        with respect to other requests.
        Type `str`. """
        
        self.doNotPerform = None
        """ True if request is prohibiting action.
        Type `bool`. """
        
        self.reportedBoolean = None
        """ Reported rather than primary record.
        Type `bool`. """
        
        self.reportedReference = None
        """ Reported rather than primary record.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.medicationCodeableConcept = None
        """ Medication to be taken.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.medicationReference = None
        """ Medication to be taken.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.subject = None
        """ Who or group medication request is for.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Encounter created as part of encounter/admission/stay.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.supportingInformation = None
        """ Information to support ordering of the medication.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.authoredOn = None
        """ When request was initially authored.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.requester = None
        """ Who/What requested the Request.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.performer = None
        """ Intended performer of administration.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.performerType = None
        """ Desired kind of performer of the medication administration.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.recorder = None
        """ Person who entered the request.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.reasonCode = None
        """ Reason or indication for ordering or not ordering the medication.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.reasonReference = None
        """ Condition or observation that supports why the prescription is
        being written.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.instantiatesCanonical = None
        """ Instantiates FHIR protocol or definition.
        List of `str` items. """
        
        self.instantiatesUri = None
        """ Instantiates external protocol or definition.
        List of `str` items. """
        
        self.basedOn = None
        """ What request fulfills.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.groupIdentifier = None
        """ Composite request this is part of.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.courseOfTherapyType = None
        """ The description of the overall patte3rn of the administration of
        the medication to the patient.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.insurance = None
        """ Associated insurance coverage.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.note = None
        """ Information about the prescription.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        self.dosageInstruction = None
        """ How the medication should be taken.
        List of `Dosage` items (represented as `dict` in JSON). """
        
        self.dispenseRequest = None
        """ Medication supply authorization.
        Type `MedicationRequestDispenseRequest` (represented as `dict` in JSON). """
        
        self.substitution = None
        """ Any restrictions on medication substitution.
        Type `MedicationRequestSubstitution` (represented as `dict` in JSON). """
        
        self.priorPrescription = None
        """ An order/prescription that is being replaced.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.detectedIssue = None
        """ Clinical Issue with action.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.eventHistory = None
        """ A list of events of interest in the lifecycle.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(MedicationRequest, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationRequest, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("statusReason", "statusReason", codeableconcept.CodeableConcept, False, None, False),
            ("intent", "intent", str, False, None, True),
            ("category", "category", codeableconcept.CodeableConcept, True, None, False),
            ("priority", "priority", str, False, None, False),
            ("doNotPerform", "doNotPerform", bool, False, None, False),
            ("reportedBoolean", "reportedBoolean", bool, False, "reported", False),
            ("reportedReference", "reportedReference", fhirreference.FHIRReference, False, "reported", False),
            ("medicationCodeableConcept", "medicationCodeableConcept", codeableconcept.CodeableConcept, False, "medication", True),
            ("medicationReference", "medicationReference", fhirreference.FHIRReference, False, "medication", True),
            ("subject", "subject", fhirreference.FHIRReference, False, None, True),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("supportingInformation", "supportingInformation", fhirreference.FHIRReference, True, None, False),
            ("authoredOn", "authoredOn", fhirdate.FHIRDate, False, None, False),
            ("requester", "requester", fhirreference.FHIRReference, False, None, False),
            ("performer", "performer", fhirreference.FHIRReference, False, None, False),
            ("performerType", "performerType", codeableconcept.CodeableConcept, False, None, False),
            ("recorder", "recorder", fhirreference.FHIRReference, False, None, False),
            ("reasonCode", "reasonCode", codeableconcept.CodeableConcept, True, None, False),
            ("reasonReference", "reasonReference", fhirreference.FHIRReference, True, None, False),
            ("instantiatesCanonical", "instantiatesCanonical", str, True, None, False),
            ("instantiatesUri", "instantiatesUri", str, True, None, False),
            ("basedOn", "basedOn", fhirreference.FHIRReference, True, None, False),
            ("groupIdentifier", "groupIdentifier", identifier.Identifier, False, None, False),
            ("courseOfTherapyType", "courseOfTherapyType", codeableconcept.CodeableConcept, False, None, False),
            ("insurance", "insurance", fhirreference.FHIRReference, True, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
            ("dosageInstruction", "dosageInstruction", dosage.Dosage, True, None, False),
            ("dispenseRequest", "dispenseRequest", MedicationRequestDispenseRequest, False, None, False),
            ("substitution", "substitution", MedicationRequestSubstitution, False, None, False),
            ("priorPrescription", "priorPrescription", fhirreference.FHIRReference, False, None, False),
            ("detectedIssue", "detectedIssue", fhirreference.FHIRReference, True, None, False),
            ("eventHistory", "eventHistory", fhirreference.FHIRReference, True, None, False),
        ])
        return js


from . import backboneelement

class MedicationRequestDispenseRequest(backboneelement.BackboneElement):
    """ Medication supply authorization.
    
    Indicates the specific details for the dispense or medication supply part
    of a medication request (also known as a Medication Prescription or
    Medication Order).  Note that this information is not always sent with the
    order.  There may be in some settings (e.g. hospitals) institutional or
    system support for completing the dispense details in the pharmacy
    department.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['initialFill'] = """First fill details."""
    _attribute_docstrings['dispenseInterval'] = """Minimum period of time between dispenses."""
    _attribute_docstrings['validityPeriod'] = """Time period supply is authorized for."""
    _attribute_docstrings['numberOfRepeatsAllowed'] = """Number of refills authorized."""
    _attribute_docstrings['quantity'] = """Amount of medication to supply per dispense."""
    _attribute_docstrings['expectedSupplyDuration'] = """Number of days supply per dispense."""
    _attribute_docstrings['performer'] = """Intended dispenser."""

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
        
        self.initialFill = None
        """ First fill details.
        Type `MedicationRequestDispenseRequestInitialFill` (represented as `dict` in JSON). """
        
        self.dispenseInterval = None
        """ Minimum period of time between dispenses.
        Type `Duration` (represented as `dict` in JSON). """
        
        self.validityPeriod = None
        """ Time period supply is authorized for.
        Type `Period` (represented as `dict` in JSON). """
        
        self.numberOfRepeatsAllowed = None
        """ Number of refills authorized.
        Type `int`. """
        
        self.quantity = None
        """ Amount of medication to supply per dispense.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.expectedSupplyDuration = None
        """ Number of days supply per dispense.
        Type `Duration` (represented as `dict` in JSON). """
        
        self.performer = None
        """ Intended dispenser.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(MedicationRequestDispenseRequest, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationRequestDispenseRequest, self).elementProperties()
        js.extend([
            ("initialFill", "initialFill", MedicationRequestDispenseRequestInitialFill, False, None, False),
            ("dispenseInterval", "dispenseInterval", duration.Duration, False, None, False),
            ("validityPeriod", "validityPeriod", period.Period, False, None, False),
            ("numberOfRepeatsAllowed", "numberOfRepeatsAllowed", int, False, None, False),
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("expectedSupplyDuration", "expectedSupplyDuration", duration.Duration, False, None, False),
            ("performer", "performer", fhirreference.FHIRReference, False, None, False),
        ])
        return js


class MedicationRequestDispenseRequestInitialFill(backboneelement.BackboneElement):
    """ First fill details.
    
    Indicates the quantity or duration for the first dispense of the
    medication.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['quantity'] = """First fill quantity."""
    _attribute_docstrings['duration'] = """First fill duration."""

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
        
        self.quantity = None
        """ First fill quantity.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.duration = None
        """ First fill duration.
        Type `Duration` (represented as `dict` in JSON). """
        
        super(MedicationRequestDispenseRequestInitialFill, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationRequestDispenseRequestInitialFill, self).elementProperties()
        js.extend([
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("duration", "duration", duration.Duration, False, None, False),
        ])
        return js


class MedicationRequestSubstitution(backboneelement.BackboneElement):
    """ Any restrictions on medication substitution.
    
    Indicates whether or not substitution can or should be part of the
    dispense. In some cases, substitution must happen, in other cases
    substitution must not happen. This block explains the prescriber's intent.
    If nothing is specified substitution may be done.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['allowedBoolean'] = """Whether substitution is allowed or not."""
    _attribute_docstrings['allowedCodeableConcept'] = """Whether substitution is allowed or not."""
    _attribute_docstrings['reason'] = """Why should (not) substitution be made."""

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
        
        self.allowedBoolean = None
        """ Whether substitution is allowed or not.
        Type `bool`. """
        
        self.allowedCodeableConcept = None
        """ Whether substitution is allowed or not.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.reason = None
        """ Why should (not) substitution be made.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(MedicationRequestSubstitution, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicationRequestSubstitution, self).elementProperties()
        js.extend([
            ("allowedBoolean", "allowedBoolean", bool, False, "allowed", True),
            ("allowedCodeableConcept", "allowedCodeableConcept", codeableconcept.CodeableConcept, False, "allowed", True),
            ("reason", "reason", codeableconcept.CodeableConcept, False, None, False),
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
    from . import dosage
except ImportError:
    dosage = sys.modules[__package__ + '.dosage']
try:
    from . import duration
except ImportError:
    duration = sys.modules[__package__ + '.duration']
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
    from . import period
except ImportError:
    period = sys.modules[__package__ + '.period']
try:
    from . import quantity
except ImportError:
    quantity = sys.modules[__package__ + '.quantity']
