#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/CareTeam) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class CareTeam(domainresource.DomainResource):
    """ Planned participants in the coordination and delivery of care for a patient
    or group.
    
    The Care Team includes all the people and organizations who plan to
    participate in the coordination and delivery of care for a patient.
    """
    
    resource_type = "CareTeam"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """External Ids for this team."""
    _attribute_docstrings['status'] = """Indicates the current state of the care team."""
    _attribute_docstrings['category'] = """Type of team."""
    _attribute_docstrings['name'] = """Name of the team, such as crisis assessment team."""
    _attribute_docstrings['subject'] = """Who care team is for."""
    _attribute_docstrings['encounter'] = """Encounter created as part of."""
    _attribute_docstrings['period'] = """Time period team covers."""
    _attribute_docstrings['participant'] = """Members of the team."""
    _attribute_docstrings['reasonCode'] = """Why the care team exists."""
    _attribute_docstrings['reasonReference'] = """Why the care team exists."""
    _attribute_docstrings['managingOrganization'] = """Organization responsible for the care team."""
    _attribute_docstrings['telecom'] = """A contact detail for the care team (that applies to all members)."""
    _attribute_docstrings['note'] = """Comments made about the CareTeam."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/care-team-status',
        'restricted_to': ['proposed', 'active', 'suspended', 'inactive', 'entered-in-error'],
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
        """ External Ids for this team.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ Indicates the current state of the care team.
        Type `str`. """
        
        self.category = None
        """ Type of team.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.name = None
        """ Name of the team, such as crisis assessment team.
        Type `str`. """
        
        self.subject = None
        """ Who care team is for.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Encounter created as part of.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.period = None
        """ Time period team covers.
        Type `Period` (represented as `dict` in JSON). """
        
        self.participant = None
        """ Members of the team.
        List of `CareTeamParticipant` items (represented as `dict` in JSON). """
        
        self.reasonCode = None
        """ Why the care team exists.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.reasonReference = None
        """ Why the care team exists.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.managingOrganization = None
        """ Organization responsible for the care team.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.telecom = None
        """ A contact detail for the care team (that applies to all members).
        List of `ContactPoint` items (represented as `dict` in JSON). """
        
        self.note = None
        """ Comments made about the CareTeam.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        super(CareTeam, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CareTeam, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, False),
            ("category", "category", codeableconcept.CodeableConcept, True, None, False),
            ("name", "name", str, False, None, False),
            ("subject", "subject", fhirreference.FHIRReference, False, None, False),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("period", "period", period.Period, False, None, False),
            ("participant", "participant", CareTeamParticipant, True, None, False),
            ("reasonCode", "reasonCode", codeableconcept.CodeableConcept, True, None, False),
            ("reasonReference", "reasonReference", fhirreference.FHIRReference, True, None, False),
            ("managingOrganization", "managingOrganization", fhirreference.FHIRReference, True, None, False),
            ("telecom", "telecom", contactpoint.ContactPoint, True, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
        ])
        return js


from . import backboneelement

class CareTeamParticipant(backboneelement.BackboneElement):
    """ Members of the team.
    
    Identifies all people and organizations who are expected to be involved in
    the care team.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['role'] = """Type of involvement."""
    _attribute_docstrings['member'] = """Who is involved."""
    _attribute_docstrings['onBehalfOf'] = """Organization of the practitioner."""
    _attribute_docstrings['period'] = """Time period of participant."""

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
        
        self.role = None
        """ Type of involvement.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.member = None
        """ Who is involved.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.onBehalfOf = None
        """ Organization of the practitioner.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.period = None
        """ Time period of participant.
        Type `Period` (represented as `dict` in JSON). """
        
        super(CareTeamParticipant, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CareTeamParticipant, self).elementProperties()
        js.extend([
            ("role", "role", codeableconcept.CodeableConcept, True, None, False),
            ("member", "member", fhirreference.FHIRReference, False, None, False),
            ("onBehalfOf", "onBehalfOf", fhirreference.FHIRReference, False, None, False),
            ("period", "period", period.Period, False, None, False),
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
