#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Provenance) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Provenance(domainresource.DomainResource):
    """ Who, What, When for a set of resources.
    
    Provenance of a resource is a record that describes entities and processes
    involved in producing and delivering or otherwise influencing that
    resource. Provenance provides a critical foundation for assessing
    authenticity, enabling trust, and allowing reproducibility. Provenance
    assertions are a form of contextual metadata and can themselves become
    important records with their own provenance. Provenance statement indicates
    clinical significance in terms of confidence in authenticity, reliability,
    and trustworthiness, integrity, and stage in lifecycle (e.g. Document
    Completion - has the artifact been legally authenticated), all of which may
    impact security, privacy, and trust policies.
    """
    
    resource_type = "Provenance"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['target'] = """Target Reference(s) (usually version specific)."""
    _attribute_docstrings['occurredPeriod'] = """When the activity occurred."""
    _attribute_docstrings['occurredDateTime'] = """When the activity occurred."""
    _attribute_docstrings['recorded'] = """When the activity was recorded / updated."""
    _attribute_docstrings['policy'] = """Policy or plan the activity was defined by."""
    _attribute_docstrings['location'] = """Where the activity occurred, if relevant."""
    _attribute_docstrings['reason'] = """Reason the activity is occurring."""
    _attribute_docstrings['activity'] = """Activity that occurred."""
    _attribute_docstrings['agent'] = """Actor involved."""
    _attribute_docstrings['entity'] = """An entity used in this activity."""
    _attribute_docstrings['signature'] = """Signature on target."""

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
        
        self.target = None
        """ Target Reference(s) (usually version specific).
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.occurredPeriod = None
        """ When the activity occurred.
        Type `Period` (represented as `dict` in JSON). """
        
        self.occurredDateTime = None
        """ When the activity occurred.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.recorded = None
        """ When the activity was recorded / updated.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.policy = None
        """ Policy or plan the activity was defined by.
        List of `str` items. """
        
        self.location = None
        """ Where the activity occurred, if relevant.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.reason = None
        """ Reason the activity is occurring.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.activity = None
        """ Activity that occurred.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.agent = None
        """ Actor involved.
        List of `ProvenanceAgent` items (represented as `dict` in JSON). """
        
        self.entity = None
        """ An entity used in this activity.
        List of `ProvenanceEntity` items (represented as `dict` in JSON). """
        
        self.signature = None
        """ Signature on target.
        List of `Signature` items (represented as `dict` in JSON). """
        
        super(Provenance, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Provenance, self).elementProperties()
        js.extend([
            ("target", "target", fhirreference.FHIRReference, True, None, True),
            ("occurredPeriod", "occurredPeriod", period.Period, False, "occurred", False),
            ("occurredDateTime", "occurredDateTime", fhirdate.FHIRDate, False, "occurred", False),
            ("recorded", "recorded", fhirdate.FHIRDate, False, None, True),
            ("policy", "policy", str, True, None, False),
            ("location", "location", fhirreference.FHIRReference, False, None, False),
            ("reason", "reason", codeableconcept.CodeableConcept, True, None, False),
            ("activity", "activity", codeableconcept.CodeableConcept, False, None, False),
            ("agent", "agent", ProvenanceAgent, True, None, True),
            ("entity", "entity", ProvenanceEntity, True, None, False),
            ("signature", "signature", signature.Signature, True, None, False),
        ])
        return js


from . import backboneelement

class ProvenanceAgent(backboneelement.BackboneElement):
    """ Actor involved.
    
    An actor taking a role in an activity  for which it can be assigned some
    degree of responsibility for the activity taking place.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """The participation the agent had with respect to the activity."""
    _attribute_docstrings['role'] = """What the agents role was."""
    _attribute_docstrings['who'] = """Who participated."""
    _attribute_docstrings['onBehalfOf'] = """Who the agent is representing."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/provenance-participant-type',
        'restricted_to': ['enterer', 'performer', 'author', 'verifier', 'legal', 'attester', 'informant', 'custodian', 'assembler', 'composer'],
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
        
        self.type = None
        """ The participation the agent had with respect to the activity.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.role = None
        """ What the agents role was.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.who = None
        """ Who participated.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.onBehalfOf = None
        """ Who the agent is representing.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(ProvenanceAgent, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ProvenanceAgent, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("role", "role", codeableconcept.CodeableConcept, True, None, False),
            ("who", "who", fhirreference.FHIRReference, False, None, True),
            ("onBehalfOf", "onBehalfOf", fhirreference.FHIRReference, False, None, False),
        ])
        return js


class ProvenanceEntity(backboneelement.BackboneElement):
    """ An entity used in this activity.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['role'] = """How the entity was used during the activity."""
    _attribute_docstrings['what'] = """Identity of entity."""
    _attribute_docstrings['agent'] = """Entity is attributed to this agent."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['role'] = {
        'url': 'http://hl7.org/fhir/provenance-entity-role',
        'restricted_to': ['derivation', 'revision', 'quotation', 'source', 'removal'],
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
        
        self.role = None
        """ How the entity was used during the activity.
        Type `str`. """
        
        self.what = None
        """ Identity of entity.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.agent = None
        """ Entity is attributed to this agent.
        List of `ProvenanceAgent` items (represented as `dict` in JSON). """
        
        super(ProvenanceEntity, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ProvenanceEntity, self).elementProperties()
        js.extend([
            ("role", "role", str, False, None, True),
            ("what", "what", fhirreference.FHIRReference, False, None, True),
            ("agent", "agent", ProvenanceAgent, True, None, False),
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
    from . import period
except ImportError:
    period = sys.modules[__package__ + '.period']
try:
    from . import signature
except ImportError:
    signature = sys.modules[__package__ + '.signature']
