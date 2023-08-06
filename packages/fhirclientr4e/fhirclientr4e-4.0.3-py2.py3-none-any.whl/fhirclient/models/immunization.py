#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Immunization) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Immunization(domainresource.DomainResource):
    """ Immunization event information.
    
    Describes the event of a patient being administered a vaccine or a record
    of an immunization as reported by a patient, a clinician or another party.
    """
    
    resource_type = "Immunization"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business identifier."""
    _attribute_docstrings['status'] = """Indicates the current status of the immunization event."""
    _attribute_docstrings['statusReason'] = """Reason not done."""
    _attribute_docstrings['vaccineCode'] = """Vaccine product administered."""
    _attribute_docstrings['patient'] = """Who was immunized."""
    _attribute_docstrings['encounter'] = """Encounter immunization was part of."""
    _attribute_docstrings['occurrenceDateTime'] = """Vaccine administration date."""
    _attribute_docstrings['occurrenceString'] = """Vaccine administration date."""
    _attribute_docstrings['recorded'] = """When the immunization was first captured in the subject's record."""
    _attribute_docstrings['primarySource'] = """Indicates context the data was recorded in."""
    _attribute_docstrings['reportOrigin'] = """The source of the data when the report of the immunization event is not based on information from the person who administered the vaccine."""
    _attribute_docstrings['location'] = """Where immunization occurred."""
    _attribute_docstrings['manufacturer'] = """Vaccine manufacturer."""
    _attribute_docstrings['lotNumber'] = """Vaccine lot number."""
    _attribute_docstrings['expirationDate'] = """Vaccine expiration date."""
    _attribute_docstrings['site'] = """Body site vaccine  was administered."""
    _attribute_docstrings['route'] = """How vaccine entered body."""
    _attribute_docstrings['doseQuantity'] = """Amount of vaccine administered."""
    _attribute_docstrings['performer'] = """Who performed event."""
    _attribute_docstrings['note'] = """Additional immunization notes."""
    _attribute_docstrings['reasonCode'] = """Why immunization occurred."""
    _attribute_docstrings['reasonReference'] = """Why immunization occurred."""
    _attribute_docstrings['isSubpotent'] = """Dose potency."""
    _attribute_docstrings['subpotentReason'] = """Reason why a dose is considered to be subpotent."""
    _attribute_docstrings['education'] = """Educational material presented to patient."""
    _attribute_docstrings['programEligibility'] = """Indicates a patient's eligibility for a funding program."""
    _attribute_docstrings['fundingSource'] = """Indicates the source of the vaccine actually administered. This may be different than the patient eligibility (e.g. the patient may be eligible for a publically purchased vaccine but due to inventory issues, vaccine purchased with private funds was actually administered)."""
    _attribute_docstrings['reaction'] = """Details of a reaction that follows immunization."""
    _attribute_docstrings['protocolApplied'] = """Protocol followed by the provider."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/event-status',
        'restricted_to': ['preparation', 'in-progress', 'not-done', 'on-hold', 'stopped', 'completed', 'entered-in-error', 'unknown'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['reportOrigin'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/immunization-origin',
        'restricted_to': ['provider', 'record', 'recall', 'school', 'jurisdiction'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['subpotentReason'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/immunization-subpotent-reason',
        'restricted_to': ['partial', 'coldchainbreak', 'recall'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['programEligibility'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/immunization-program-eligibility',
        'restricted_to': ['ineligible', 'uninsured'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['fundingSource'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/immunization-funding-source',
        'restricted_to': ['private', 'public'],
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
        """ Business identifier.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ Indicates the current status of the immunization event.
        Type `str`. """
        
        self.statusReason = None
        """ Reason not done.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.vaccineCode = None
        """ Vaccine product administered.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.patient = None
        """ Who was immunized.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Encounter immunization was part of.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.occurrenceDateTime = None
        """ Vaccine administration date.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.occurrenceString = None
        """ Vaccine administration date.
        Type `str`. """
        
        self.recorded = None
        """ When the immunization was first captured in the subject's record.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.primarySource = None
        """ Indicates context the data was recorded in.
        Type `bool`. """
        
        self.reportOrigin = None
        """ The source of the data when the report of the immunization event is
        not based on information from the person who administered the
        vaccine.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.location = None
        """ Where immunization occurred.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.manufacturer = None
        """ Vaccine manufacturer.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.lotNumber = None
        """ Vaccine lot number.
        Type `str`. """
        
        self.expirationDate = None
        """ Vaccine expiration date.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.site = None
        """ Body site vaccine  was administered.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.route = None
        """ How vaccine entered body.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.doseQuantity = None
        """ Amount of vaccine administered.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.performer = None
        """ Who performed event.
        List of `ImmunizationPerformer` items (represented as `dict` in JSON). """
        
        self.note = None
        """ Additional immunization notes.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        self.reasonCode = None
        """ Why immunization occurred.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.reasonReference = None
        """ Why immunization occurred.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.isSubpotent = None
        """ Dose potency.
        Type `bool`. """
        
        self.subpotentReason = None
        """ Reason why a dose is considered to be subpotent.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.education = None
        """ Educational material presented to patient.
        List of `ImmunizationEducation` items (represented as `dict` in JSON). """
        
        self.programEligibility = None
        """ Indicates a patient's eligibility for a funding program.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.fundingSource = None
        """ Indicates the source of the vaccine actually administered. This may
        be different than the patient eligibility (e.g. the patient may be
        eligible for a publically purchased vaccine but due to inventory
        issues, vaccine purchased with private funds was actually
        administered).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.reaction = None
        """ Details of a reaction that follows immunization.
        List of `ImmunizationReaction` items (represented as `dict` in JSON). """
        
        self.protocolApplied = None
        """ Protocol followed by the provider.
        List of `ImmunizationProtocolApplied` items (represented as `dict` in JSON). """
        
        super(Immunization, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Immunization, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("statusReason", "statusReason", codeableconcept.CodeableConcept, False, None, False),
            ("vaccineCode", "vaccineCode", codeableconcept.CodeableConcept, False, None, True),
            ("patient", "patient", fhirreference.FHIRReference, False, None, True),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("occurrenceDateTime", "occurrenceDateTime", fhirdate.FHIRDate, False, "occurrence", True),
            ("occurrenceString", "occurrenceString", str, False, "occurrence", True),
            ("recorded", "recorded", fhirdate.FHIRDate, False, None, False),
            ("primarySource", "primarySource", bool, False, None, False),
            ("reportOrigin", "reportOrigin", codeableconcept.CodeableConcept, False, None, False),
            ("location", "location", fhirreference.FHIRReference, False, None, False),
            ("manufacturer", "manufacturer", fhirreference.FHIRReference, False, None, False),
            ("lotNumber", "lotNumber", str, False, None, False),
            ("expirationDate", "expirationDate", fhirdate.FHIRDate, False, None, False),
            ("site", "site", codeableconcept.CodeableConcept, False, None, False),
            ("route", "route", codeableconcept.CodeableConcept, False, None, False),
            ("doseQuantity", "doseQuantity", quantity.Quantity, False, None, False),
            ("performer", "performer", ImmunizationPerformer, True, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
            ("reasonCode", "reasonCode", codeableconcept.CodeableConcept, True, None, False),
            ("reasonReference", "reasonReference", fhirreference.FHIRReference, True, None, False),
            ("isSubpotent", "isSubpotent", bool, False, None, False),
            ("subpotentReason", "subpotentReason", codeableconcept.CodeableConcept, True, None, False),
            ("education", "education", ImmunizationEducation, True, None, False),
            ("programEligibility", "programEligibility", codeableconcept.CodeableConcept, True, None, False),
            ("fundingSource", "fundingSource", codeableconcept.CodeableConcept, False, None, False),
            ("reaction", "reaction", ImmunizationReaction, True, None, False),
            ("protocolApplied", "protocolApplied", ImmunizationProtocolApplied, True, None, False),
        ])
        return js


from . import backboneelement

class ImmunizationEducation(backboneelement.BackboneElement):
    """ Educational material presented to patient.
    
    Educational material presented to the patient (or guardian) at the time of
    vaccine administration.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['documentType'] = """Educational material document identifier."""
    _attribute_docstrings['reference'] = """Educational material reference pointer."""
    _attribute_docstrings['publicationDate'] = """Educational material publication date."""
    _attribute_docstrings['presentationDate'] = """Educational material presentation date."""

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
        
        self.documentType = None
        """ Educational material document identifier.
        Type `str`. """
        
        self.reference = None
        """ Educational material reference pointer.
        Type `str`. """
        
        self.publicationDate = None
        """ Educational material publication date.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.presentationDate = None
        """ Educational material presentation date.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        super(ImmunizationEducation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ImmunizationEducation, self).elementProperties()
        js.extend([
            ("documentType", "documentType", str, False, None, False),
            ("reference", "reference", str, False, None, False),
            ("publicationDate", "publicationDate", fhirdate.FHIRDate, False, None, False),
            ("presentationDate", "presentationDate", fhirdate.FHIRDate, False, None, False),
        ])
        return js


class ImmunizationPerformer(backboneelement.BackboneElement):
    """ Who performed event.
    
    Indicates who performed the immunization event.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['function'] = """What type of performance was done."""
    _attribute_docstrings['actor'] = """Individual or organization who was performing."""

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
        """ Individual or organization who was performing.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(ImmunizationPerformer, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ImmunizationPerformer, self).elementProperties()
        js.extend([
            ("function", "function", codeableconcept.CodeableConcept, False, None, False),
            ("actor", "actor", fhirreference.FHIRReference, False, None, True),
        ])
        return js


class ImmunizationProtocolApplied(backboneelement.BackboneElement):
    """ Protocol followed by the provider.
    
    The protocol (set of recommendations) being followed by the provider who
    administered the dose.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['series'] = """Name of vaccine series."""
    _attribute_docstrings['authority'] = """Who is responsible for publishing the recommendations."""
    _attribute_docstrings['targetDisease'] = """Vaccine preventatable disease being targetted."""
    _attribute_docstrings['doseNumberPositiveInt'] = """Dose number within series."""
    _attribute_docstrings['doseNumberString'] = """Dose number within series."""
    _attribute_docstrings['seriesDosesPositiveInt'] = """Recommended number of doses for immunity."""
    _attribute_docstrings['seriesDosesString'] = """Recommended number of doses for immunity."""

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
        
        self.series = None
        """ Name of vaccine series.
        Type `str`. """
        
        self.authority = None
        """ Who is responsible for publishing the recommendations.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.targetDisease = None
        """ Vaccine preventatable disease being targetted.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.doseNumberPositiveInt = None
        """ Dose number within series.
        Type `int`. """
        
        self.doseNumberString = None
        """ Dose number within series.
        Type `str`. """
        
        self.seriesDosesPositiveInt = None
        """ Recommended number of doses for immunity.
        Type `int`. """
        
        self.seriesDosesString = None
        """ Recommended number of doses for immunity.
        Type `str`. """
        
        super(ImmunizationProtocolApplied, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ImmunizationProtocolApplied, self).elementProperties()
        js.extend([
            ("series", "series", str, False, None, False),
            ("authority", "authority", fhirreference.FHIRReference, False, None, False),
            ("targetDisease", "targetDisease", codeableconcept.CodeableConcept, True, None, False),
            ("doseNumberPositiveInt", "doseNumberPositiveInt", int, False, "doseNumber", True),
            ("doseNumberString", "doseNumberString", str, False, "doseNumber", True),
            ("seriesDosesPositiveInt", "seriesDosesPositiveInt", int, False, "seriesDoses", False),
            ("seriesDosesString", "seriesDosesString", str, False, "seriesDoses", False),
        ])
        return js


class ImmunizationReaction(backboneelement.BackboneElement):
    """ Details of a reaction that follows immunization.
    
    Categorical data indicating that an adverse event is associated in time to
    an immunization.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['date'] = """When reaction started."""
    _attribute_docstrings['detail'] = """Additional information on reaction."""
    _attribute_docstrings['reported'] = """Indicates self-reported reaction."""

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
        """ When reaction started.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.detail = None
        """ Additional information on reaction.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.reported = None
        """ Indicates self-reported reaction.
        Type `bool`. """
        
        super(ImmunizationReaction, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ImmunizationReaction, self).elementProperties()
        js.extend([
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("detail", "detail", fhirreference.FHIRReference, False, None, False),
            ("reported", "reported", bool, False, None, False),
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
    from . import quantity
except ImportError:
    quantity = sys.modules[__package__ + '.quantity']
