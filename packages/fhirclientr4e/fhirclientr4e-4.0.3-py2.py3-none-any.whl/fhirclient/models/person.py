#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Person) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Person(domainresource.DomainResource):
    """ A generic person record.
    
    Demographics and administrative information about a person independent of a
    specific health-related context.
    """
    
    resource_type = "Person"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """A human identifier for this person."""
    _attribute_docstrings['name'] = """A name associated with the person."""
    _attribute_docstrings['telecom'] = """A contact detail for the person."""
    _attribute_docstrings['gender'] = """Administrative Gender."""
    _attribute_docstrings['birthDate'] = """The date on which the person was born."""
    _attribute_docstrings['address'] = """One or more addresses for the person."""
    _attribute_docstrings['photo'] = """Image of the person."""
    _attribute_docstrings['managingOrganization'] = """The organization that is the custodian of the person record."""
    _attribute_docstrings['active'] = """This person's record is in active use."""
    _attribute_docstrings['link'] = """Link to a resource that concerns the same actual person."""

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
        
        self.name = None
        """ A name associated with the person.
        List of `HumanName` items (represented as `dict` in JSON). """
        
        self.telecom = None
        """ A contact detail for the person.
        List of `ContactPoint` items (represented as `dict` in JSON). """
        
        self.gender = None
        """ Administrative Gender.
        Type `str`. """
        
        self.birthDate = None
        """ The date on which the person was born.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.address = None
        """ One or more addresses for the person.
        List of `Address` items (represented as `dict` in JSON). """
        
        self.photo = None
        """ Image of the person.
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.managingOrganization = None
        """ The organization that is the custodian of the person record.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.active = None
        """ This person's record is in active use.
        Type `bool`. """
        
        self.link = None
        """ Link to a resource that concerns the same actual person.
        List of `PersonLink` items (represented as `dict` in JSON). """
        
        super(Person, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Person, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("name", "name", humanname.HumanName, True, None, False),
            ("telecom", "telecom", contactpoint.ContactPoint, True, None, False),
            ("gender", "gender", str, False, None, False),
            ("birthDate", "birthDate", fhirdate.FHIRDate, False, None, False),
            ("address", "address", address.Address, True, None, False),
            ("photo", "photo", attachment.Attachment, False, None, False),
            ("managingOrganization", "managingOrganization", fhirreference.FHIRReference, False, None, False),
            ("active", "active", bool, False, None, False),
            ("link", "link", PersonLink, True, None, False),
        ])
        return js


from . import backboneelement

class PersonLink(backboneelement.BackboneElement):
    """ Link to a resource that concerns the same actual person.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['target'] = """The resource to which this actual person is associated."""
    _attribute_docstrings['assurance'] = """Level of assurance that this link is associated with the target resource."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['assurance'] = {
        'url': 'http://hl7.org/fhir/identity-assuranceLevel',
        'restricted_to': ['level1', 'level2', 'level3', 'level4'],
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
        
        self.target = None
        """ The resource to which this actual person is associated.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.assurance = None
        """ Level of assurance that this link is associated with the target
        resource.
        Type `str`. """
        
        super(PersonLink, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(PersonLink, self).elementProperties()
        js.extend([
            ("target", "target", fhirreference.FHIRReference, False, None, True),
            ("assurance", "assurance", str, False, None, False),
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
