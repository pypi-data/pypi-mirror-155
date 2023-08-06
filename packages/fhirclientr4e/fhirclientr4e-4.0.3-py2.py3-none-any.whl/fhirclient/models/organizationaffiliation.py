#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/OrganizationAffiliation) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class OrganizationAffiliation(domainresource.DomainResource):
    """ Defines an affiliation/assotiation/relationship between 2 distinct
    oganizations, that is not a part-of relationship/sub-division relationship.
    """
    
    resource_type = "OrganizationAffiliation"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business identifiers that are specific to this role."""
    _attribute_docstrings['active'] = """Whether this organization affiliation record is in active use."""
    _attribute_docstrings['period'] = """The period during which the participatingOrganization is affiliated with the primary organization."""
    _attribute_docstrings['organization'] = """Organization where the role is available."""
    _attribute_docstrings['participatingOrganization'] = """Organization that provides/performs the role (e.g. providing services or is a member of)."""
    _attribute_docstrings['network'] = """Health insurance provider network in which the participatingOrganization provides the role's services (if defined) at the indicated locations (if defined)."""
    _attribute_docstrings['code'] = """Definition of the role the participatingOrganization plays in the association."""
    _attribute_docstrings['specialty'] = """Specific specialty of the participatingOrganization in the context of the role."""
    _attribute_docstrings['location'] = """The location(s) at which the role occurs."""
    _attribute_docstrings['healthcareService'] = """Healthcare services provided through the role."""
    _attribute_docstrings['telecom'] = """Contact details at the participatingOrganization relevant to this Affiliation."""
    _attribute_docstrings['endpoint'] = """Technical endpoints providing access to services operated for this role."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['code'] = {
        'url': 'http://hl7.org/fhir/organization-role',
        'restricted_to': ['provider', 'agency', 'research', 'payer', 'diagnostics', 'supplier', 'HIE/HIO', 'member'],
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
        """ Business identifiers that are specific to this role.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.active = None
        """ Whether this organization affiliation record is in active use.
        Type `bool`. """
        
        self.period = None
        """ The period during which the participatingOrganization is affiliated
        with the primary organization.
        Type `Period` (represented as `dict` in JSON). """
        
        self.organization = None
        """ Organization where the role is available.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.participatingOrganization = None
        """ Organization that provides/performs the role (e.g. providing
        services or is a member of).
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.network = None
        """ Health insurance provider network in which the
        participatingOrganization provides the role's services (if defined)
        at the indicated locations (if defined).
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.code = None
        """ Definition of the role the participatingOrganization plays in the
        association.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.specialty = None
        """ Specific specialty of the participatingOrganization in the context
        of the role.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.location = None
        """ The location(s) at which the role occurs.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.healthcareService = None
        """ Healthcare services provided through the role.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.telecom = None
        """ Contact details at the participatingOrganization relevant to this
        Affiliation.
        List of `ContactPoint` items (represented as `dict` in JSON). """
        
        self.endpoint = None
        """ Technical endpoints providing access to services operated for this
        role.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(OrganizationAffiliation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(OrganizationAffiliation, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("active", "active", bool, False, None, False),
            ("period", "period", period.Period, False, None, False),
            ("organization", "organization", fhirreference.FHIRReference, False, None, False),
            ("participatingOrganization", "participatingOrganization", fhirreference.FHIRReference, False, None, False),
            ("network", "network", fhirreference.FHIRReference, True, None, False),
            ("code", "code", codeableconcept.CodeableConcept, True, None, False),
            ("specialty", "specialty", codeableconcept.CodeableConcept, True, None, False),
            ("location", "location", fhirreference.FHIRReference, True, None, False),
            ("healthcareService", "healthcareService", fhirreference.FHIRReference, True, None, False),
            ("telecom", "telecom", contactpoint.ContactPoint, True, None, False),
            ("endpoint", "endpoint", fhirreference.FHIRReference, True, None, False),
        ])
        return js


import sys
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
    from . import identifier
except ImportError:
    identifier = sys.modules[__package__ + '.identifier']
try:
    from . import period
except ImportError:
    period = sys.modules[__package__ + '.period']
