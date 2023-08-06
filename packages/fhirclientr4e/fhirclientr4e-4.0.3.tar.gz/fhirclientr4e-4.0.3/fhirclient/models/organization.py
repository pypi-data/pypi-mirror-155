#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Organization) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Organization(domainresource.DomainResource):
    """ A grouping of people or organizations with a common purpose.
    
    A formally or informally recognized grouping of people or organizations
    formed for the purpose of achieving some form of collective action.
    Includes companies, institutions, corporations, departments, community
    groups, healthcare practice groups, payer/insurer, etc.
    """
    
    resource_type = "Organization"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Identifies this organization  across multiple systems."""
    _attribute_docstrings['active'] = """Whether the organization's record is still in active use."""
    _attribute_docstrings['type'] = """The kind(s) of organization that this is."""
    _attribute_docstrings['name'] = """Name used for the organization."""
    _attribute_docstrings['alias'] = """A list of alternate names that the organization is known as, or was known as in the past."""
    _attribute_docstrings['telecom'] = """A contact detail for the organization."""
    _attribute_docstrings['address'] = """An address for the organization."""
    _attribute_docstrings['partOf'] = """The organization of which this organization forms a part."""
    _attribute_docstrings['contact'] = """Contact for the organization for a certain purpose."""
    _attribute_docstrings['endpoint'] = """Technical endpoints providing access to services operated for the organization."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/organization-type',
        'restricted_to': ['prov', 'dept', 'team', 'govt', 'ins', 'pay', 'edu', 'reli', 'crs', 'cg', 'bus', 'other'],
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
        """ Identifies this organization  across multiple systems.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.active = None
        """ Whether the organization's record is still in active use.
        Type `bool`. """
        
        self.type = None
        """ The kind(s) of organization that this is.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.name = None
        """ Name used for the organization.
        Type `str`. """
        
        self.alias = None
        """ A list of alternate names that the organization is known as, or was
        known as in the past.
        List of `str` items. """
        
        self.telecom = None
        """ A contact detail for the organization.
        List of `ContactPoint` items (represented as `dict` in JSON). """
        
        self.address = None
        """ An address for the organization.
        List of `Address` items (represented as `dict` in JSON). """
        
        self.partOf = None
        """ The organization of which this organization forms a part.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.contact = None
        """ Contact for the organization for a certain purpose.
        List of `OrganizationContact` items (represented as `dict` in JSON). """
        
        self.endpoint = None
        """ Technical endpoints providing access to services operated for the
        organization.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(Organization, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Organization, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("active", "active", bool, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, True, None, False),
            ("name", "name", str, False, None, False),
            ("alias", "alias", str, True, None, False),
            ("telecom", "telecom", contactpoint.ContactPoint, True, None, False),
            ("address", "address", address.Address, True, None, False),
            ("partOf", "partOf", fhirreference.FHIRReference, False, None, False),
            ("contact", "contact", OrganizationContact, True, None, False),
            ("endpoint", "endpoint", fhirreference.FHIRReference, True, None, False),
        ])
        return js


from . import backboneelement

class OrganizationContact(backboneelement.BackboneElement):
    """ Contact for the organization for a certain purpose.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['purpose'] = """Indicates a purpose for which the contact can be reached."""
    _attribute_docstrings['name'] = """A name associated with the contact."""
    _attribute_docstrings['telecom'] = """Contact details (telephone, email, etc.)  for a contact."""
    _attribute_docstrings['address'] = """Visiting or postal addresses for the contact."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['purpose'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/contactentity-type',
        'restricted_to': ['BILL', 'ADMIN', 'HR', 'PAYOR', 'PATINF', 'PRESS'],
        'binding_strength': 'extensible',
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
        
        self.purpose = None
        """ Indicates a purpose for which the contact can be reached.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.name = None
        """ A name associated with the contact.
        Type `HumanName` (represented as `dict` in JSON). """
        
        self.telecom = None
        """ Contact details (telephone, email, etc.)  for a contact.
        List of `ContactPoint` items (represented as `dict` in JSON). """
        
        self.address = None
        """ Visiting or postal addresses for the contact.
        Type `Address` (represented as `dict` in JSON). """
        
        super(OrganizationContact, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(OrganizationContact, self).elementProperties()
        js.extend([
            ("purpose", "purpose", codeableconcept.CodeableConcept, False, None, False),
            ("name", "name", humanname.HumanName, False, None, False),
            ("telecom", "telecom", contactpoint.ContactPoint, True, None, False),
            ("address", "address", address.Address, False, None, False),
        ])
        return js


import sys
try:
    from . import address
except ImportError:
    address = sys.modules[__package__ + '.address']
try:
    from . import codeableconcept
except ImportError:
    codeableconcept = sys.modules[__package__ + '.codeableconcept']
try:
    from . import contactpoint
except ImportError:
    contactpoint = sys.modules[__package__ + '.contactpoint']
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
