#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/RelatedPerson) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class RelatedPerson(domainresource.DomainResource):
    """ A person that is related to a patient, but who is not a direct target of
    care.
    
    Information about a person that is involved in the care for a patient, but
    who is not the target of healthcare, nor has a formal responsibility in the
    care process.
    """
    
    resource_type = "RelatedPerson"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """A human identifier for this person."""
    _attribute_docstrings['active'] = """Whether this related person's record is in active use."""
    _attribute_docstrings['patient'] = """The patient this person is related to."""
    _attribute_docstrings['relationship'] = """The nature of the relationship."""
    _attribute_docstrings['name'] = """A name associated with the person."""
    _attribute_docstrings['telecom'] = """A contact detail for the person."""
    _attribute_docstrings['gender'] = """Administrative Gender - the gender that the person is considered to have for administration and record keeping purposes."""
    _attribute_docstrings['birthDate'] = """The date on which the related person was born."""
    _attribute_docstrings['address'] = """Address where the related person can be contacted or visited."""
    _attribute_docstrings['photo'] = """Image of the person."""
    _attribute_docstrings['period'] = """Period of time that this relationship is considered valid."""
    _attribute_docstrings['communication'] = """A language which may be used to communicate with about the patient's health."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['gender'] = {
        'url': 'http://hl7.org/fhir/administrative-gender',
        'restricted_to': ['male', 'female', 'other', 'unknown'],
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
        """ A human identifier for this person.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.active = None
        """ Whether this related person's record is in active use.
        Type `bool`. """
        
        self.patient = None
        """ The patient this person is related to.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.relationship = None
        """ The nature of the relationship.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.name = None
        """ A name associated with the person.
        List of `HumanName` items (represented as `dict` in JSON). """
        
        self.telecom = None
        """ A contact detail for the person.
        List of `ContactPoint` items (represented as `dict` in JSON). """
        
        self.gender = None
        """ Administrative Gender - the gender that the person is considered to
        have for administration and record keeping purposes.
        Type `str`. """
        
        self.birthDate = None
        """ The date on which the related person was born.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.address = None
        """ Address where the related person can be contacted or visited.
        List of `Address` items (represented as `dict` in JSON). """
        
        self.photo = None
        """ Image of the person.
        List of `Attachment` items (represented as `dict` in JSON). """
        
        self.period = None
        """ Period of time that this relationship is considered valid.
        Type `Period` (represented as `dict` in JSON). """
        
        self.communication = None
        """ A language which may be used to communicate with about the
        patient's health.
        List of `RelatedPersonCommunication` items (represented as `dict` in JSON). """
        
        super(RelatedPerson, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(RelatedPerson, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("active", "active", bool, False, None, False),
            ("patient", "patient", fhirreference.FHIRReference, False, None, True),
            ("relationship", "relationship", codeableconcept.CodeableConcept, True, None, False),
            ("name", "name", humanname.HumanName, True, None, False),
            ("telecom", "telecom", contactpoint.ContactPoint, True, None, False),
            ("gender", "gender", str, False, None, False),
            ("birthDate", "birthDate", fhirdate.FHIRDate, False, None, False),
            ("address", "address", address.Address, True, None, False),
            ("photo", "photo", attachment.Attachment, True, None, False),
            ("period", "period", period.Period, False, None, False),
            ("communication", "communication", RelatedPersonCommunication, True, None, False),
        ])
        return js


from . import backboneelement

class RelatedPersonCommunication(backboneelement.BackboneElement):
    """ A language which may be used to communicate with about the patient's health.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['language'] = """The language which can be used to communicate with the patient about his or her health."""
    _attribute_docstrings['preferred'] = """Language preference indicator."""

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
        
        self.language = None
        """ The language which can be used to communicate with the patient
        about his or her health.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.preferred = None
        """ Language preference indicator.
        Type `bool`. """
        
        super(RelatedPersonCommunication, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(RelatedPersonCommunication, self).elementProperties()
        js.extend([
            ("language", "language", codeableconcept.CodeableConcept, False, None, True),
            ("preferred", "preferred", bool, False, None, False),
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
    from . import contactpoint
except ImportError:
    contactpoint = sys.modules[__package__ + '.contactpoint']
try:
    from . import fhirdate
except ImportError:
    fhirdate = sys.modules[__package__ + '.fhirdate']
try:
    from . import fhirreference
except ImportError:
    fhirreference = sys.modules[__package__ + '.fhirreference']
try:
    from . import humanname
except ImportError:
    humanname = sys.modules[__package__ + '.humanname']
try:
    from . import identifier
except ImportError:
    identifier = sys.modules[__package__ + '.identifier']
try:
    from . import period
except ImportError:
    period = sys.modules[__package__ + '.period']
