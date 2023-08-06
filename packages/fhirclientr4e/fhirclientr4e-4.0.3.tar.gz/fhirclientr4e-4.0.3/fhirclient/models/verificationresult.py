#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/VerificationResult) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class VerificationResult(domainresource.DomainResource):
    """ Describes validation requirements, source(s), status and dates for one or
    more elements.
    """
    
    resource_type = "VerificationResult"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['target'] = """A resource that was validated."""
    _attribute_docstrings['targetLocation'] = """The fhirpath location(s) within the resource that was validated."""
    _attribute_docstrings['need'] = """The frequency with which the target must be validated (none; initial; periodic)."""
    _attribute_docstrings['status'] = """The validation status of the target (attested; validated; in process; requires revalidation; validation failed; revalidation failed)."""
    _attribute_docstrings['statusDate'] = """When the validation status was updated."""
    _attribute_docstrings['validationType'] = """What the target is validated against (nothing; primary source; multiple sources)."""
    _attribute_docstrings['validationProcess'] = """None"""
    _attribute_docstrings['frequency'] = """Frequency of revalidation."""
    _attribute_docstrings['lastPerformed'] = """The date/time validation was last completed (including failed validations)."""
    _attribute_docstrings['nextScheduled'] = """The date when target is next validated, if appropriate."""
    _attribute_docstrings['failureAction'] = """The result if validation fails (fatal; warning; record only; none)."""
    _attribute_docstrings['primarySource'] = """Information about the primary source(s) involved in validation."""
    _attribute_docstrings['attestation'] = """Information about the entity attesting to information."""
    _attribute_docstrings['validator'] = """Information about the entity validating information."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['need'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/need',
        'restricted_to': ['none', 'initial', 'periodic'],
        'binding_strength': 'preferred',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/CodeSystem/status',
        'restricted_to': ['attested', 'validated', 'in-process', 'req-revalid', 'val-fail', 'reval-fail'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['validationType'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/validation-type',
        'restricted_to': ['nothing', 'primary', 'multiple'],
        'binding_strength': 'preferred',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['validationProcess'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/validation-process',
        'restricted_to': ['edit-check', 'valueset', 'primary', 'multi', 'standalone', 'in-context'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['failureAction'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/failure-action',
        'restricted_to': ['fatal', 'warn', 'rec-only', 'none'],
        'binding_strength': 'preferred',
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
        
        self.target = None
        """ A resource that was validated.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.targetLocation = None
        """ The fhirpath location(s) within the resource that was validated.
        List of `str` items. """
        
        self.need = None
        """ The frequency with which the target must be validated (none;
        initial; periodic).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.status = None
        """ The validation status of the target (attested; validated; in
        process; requires revalidation; validation failed; revalidation
        failed).
        Type `str`. """
        
        self.statusDate = None
        """ When the validation status was updated.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.validationType = None
        """ What the target is validated against (nothing; primary source;
        multiple sources).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.validationProcess = None
        """ None.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.frequency = None
        """ Frequency of revalidation.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.lastPerformed = None
        """ The date/time validation was last completed (including failed
        validations).
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.nextScheduled = None
        """ The date when target is next validated, if appropriate.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.failureAction = None
        """ The result if validation fails (fatal; warning; record only; none).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.primarySource = None
        """ Information about the primary source(s) involved in validation.
        List of `VerificationResultPrimarySource` items (represented as `dict` in JSON). """
        
        self.attestation = None
        """ Information about the entity attesting to information.
        Type `VerificationResultAttestation` (represented as `dict` in JSON). """
        
        self.validator = None
        """ Information about the entity validating information.
        List of `VerificationResultValidator` items (represented as `dict` in JSON). """
        
        super(VerificationResult, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(VerificationResult, self).elementProperties()
        js.extend([
            ("target", "target", fhirreference.FHIRReference, True, None, False),
            ("targetLocation", "targetLocation", str, True, None, False),
            ("need", "need", codeableconcept.CodeableConcept, False, None, False),
            ("status", "status", str, False, None, True),
            ("statusDate", "statusDate", fhirdate.FHIRDate, False, None, False),
            ("validationType", "validationType", codeableconcept.CodeableConcept, False, None, False),
            ("validationProcess", "validationProcess", codeableconcept.CodeableConcept, True, None, False),
            ("frequency", "frequency", timing.Timing, False, None, False),
            ("lastPerformed", "lastPerformed", fhirdate.FHIRDate, False, None, False),
            ("nextScheduled", "nextScheduled", fhirdate.FHIRDate, False, None, False),
            ("failureAction", "failureAction", codeableconcept.CodeableConcept, False, None, False),
            ("primarySource", "primarySource", VerificationResultPrimarySource, True, None, False),
            ("attestation", "attestation", VerificationResultAttestation, False, None, False),
            ("validator", "validator", VerificationResultValidator, True, None, False),
        ])
        return js


from . import backboneelement

class VerificationResultAttestation(backboneelement.BackboneElement):
    """ Information about the entity attesting to information.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['who'] = """The individual or organization attesting to information."""
    _attribute_docstrings['onBehalfOf'] = """When the who is asserting on behalf of another (organization or individual)."""
    _attribute_docstrings['communicationMethod'] = """The method by which attested information was submitted/retrieved (manual; API; Push)."""
    _attribute_docstrings['date'] = """The date the information was attested to."""
    _attribute_docstrings['sourceIdentityCertificate'] = """A digital identity certificate associated with the attestation source."""
    _attribute_docstrings['proxyIdentityCertificate'] = """A digital identity certificate associated with the proxy entity submitting attested information on behalf of the attestation source."""
    _attribute_docstrings['proxySignature'] = """Proxy signature."""
    _attribute_docstrings['sourceSignature'] = """Attester signature."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['communicationMethod'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/verificationresult-communication-method',
        'restricted_to': ['manual', 'portal', 'pull', 'push'],
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
        
        self.who = None
        """ The individual or organization attesting to information.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.onBehalfOf = None
        """ When the who is asserting on behalf of another (organization or
        individual).
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.communicationMethod = None
        """ The method by which attested information was submitted/retrieved
        (manual; API; Push).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.date = None
        """ The date the information was attested to.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.sourceIdentityCertificate = None
        """ A digital identity certificate associated with the attestation
        source.
        Type `str`. """
        
        self.proxyIdentityCertificate = None
        """ A digital identity certificate associated with the proxy entity
        submitting attested information on behalf of the attestation source.
        Type `str`. """
        
        self.proxySignature = None
        """ Proxy signature.
        Type `Signature` (represented as `dict` in JSON). """
        
        self.sourceSignature = None
        """ Attester signature.
        Type `Signature` (represented as `dict` in JSON). """
        
        super(VerificationResultAttestation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(VerificationResultAttestation, self).elementProperties()
        js.extend([
            ("who", "who", fhirreference.FHIRReference, False, None, False),
            ("onBehalfOf", "onBehalfOf", fhirreference.FHIRReference, False, None, False),
            ("communicationMethod", "communicationMethod", codeableconcept.CodeableConcept, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("sourceIdentityCertificate", "sourceIdentityCertificate", str, False, None, False),
            ("proxyIdentityCertificate", "proxyIdentityCertificate", str, False, None, False),
            ("proxySignature", "proxySignature", signature.Signature, False, None, False),
            ("sourceSignature", "sourceSignature", signature.Signature, False, None, False),
        ])
        return js


class VerificationResultPrimarySource(backboneelement.BackboneElement):
    """ Information about the primary source(s) involved in validation.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['who'] = """Reference to the primary source."""
    _attribute_docstrings['type'] = """None"""
    _attribute_docstrings['communicationMethod'] = """Method for communicating with the primary source (manual; API; Push)."""
    _attribute_docstrings['validationStatus'] = """Status of the validation of the target against the primary source (successful; failed; unknown)."""
    _attribute_docstrings['validationDate'] = """When the target was validated against the primary source."""
    _attribute_docstrings['canPushUpdates'] = """Ability of the primary source to push updates/alerts (yes; no; undetermined)."""
    _attribute_docstrings['pushTypeAvailable'] = """Type of alerts/updates the primary source can send (specific requested changes; any changes; as defined by source)."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/primary-source-type',
        'restricted_to': ['lic-board', 'prim', 'cont-ed', 'post-serv', 'rel-own', 'reg-auth', 'legal', 'issuer', 'auth-source'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['communicationMethod'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/verificationresult-communication-method',
        'restricted_to': ['manual', 'portal', 'pull', 'push'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['validationStatus'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/validation-status',
        'restricted_to': ['successful', 'failed', 'unknown'],
        'binding_strength': 'preferred',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['canPushUpdates'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/can-push-updates',
        'restricted_to': ['yes', 'no', 'undetermined'],
        'binding_strength': 'preferred',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['pushTypeAvailable'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/push-type-available',
        'restricted_to': ['specific', 'any', 'source'],
        'binding_strength': 'preferred',
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
        
        self.who = None
        """ Reference to the primary source.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.type = None
        """ None.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.communicationMethod = None
        """ Method for communicating with the primary source (manual; API;
        Push).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.validationStatus = None
        """ Status of the validation of the target against the primary source
        (successful; failed; unknown).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.validationDate = None
        """ When the target was validated against the primary source.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.canPushUpdates = None
        """ Ability of the primary source to push updates/alerts (yes; no;
        undetermined).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.pushTypeAvailable = None
        """ Type of alerts/updates the primary source can send (specific
        requested changes; any changes; as defined by source).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        super(VerificationResultPrimarySource, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(VerificationResultPrimarySource, self).elementProperties()
        js.extend([
            ("who", "who", fhirreference.FHIRReference, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, True, None, False),
            ("communicationMethod", "communicationMethod", codeableconcept.CodeableConcept, True, None, False),
            ("validationStatus", "validationStatus", codeableconcept.CodeableConcept, False, None, False),
            ("validationDate", "validationDate", fhirdate.FHIRDate, False, None, False),
            ("canPushUpdates", "canPushUpdates", codeableconcept.CodeableConcept, False, None, False),
            ("pushTypeAvailable", "pushTypeAvailable", codeableconcept.CodeableConcept, True, None, False),
        ])
        return js


class VerificationResultValidator(backboneelement.BackboneElement):
    """ Information about the entity validating information.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['organization'] = """Reference to the organization validating information."""
    _attribute_docstrings['identityCertificate'] = """A digital identity certificate associated with the validator."""
    _attribute_docstrings['attestationSignature'] = """Validator signature."""

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
        
        self.organization = None
        """ Reference to the organization validating information.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.identityCertificate = None
        """ A digital identity certificate associated with the validator.
        Type `str`. """
        
        self.attestationSignature = None
        """ Validator signature.
        Type `Signature` (represented as `dict` in JSON). """
        
        super(VerificationResultValidator, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(VerificationResultValidator, self).elementProperties()
        js.extend([
            ("organization", "organization", fhirreference.FHIRReference, False, None, True),
            ("identityCertificate", "identityCertificate", str, False, None, False),
            ("attestationSignature", "attestationSignature", signature.Signature, False, None, False),
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
    from . import signature
except ImportError:
    signature = sys.modules[__package__ + '.signature']
try:
    from . import timing
except ImportError:
    timing = sys.modules[__package__ + '.timing']
