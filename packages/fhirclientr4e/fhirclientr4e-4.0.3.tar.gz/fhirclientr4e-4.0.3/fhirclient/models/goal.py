#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Goal) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Goal(domainresource.DomainResource):
    """ Describes the intended objective(s) for a patient, group or organization.
    
    Describes the intended objective(s) for a patient, group or organization
    care, for example, weight loss, restoring an activity of daily living,
    obtaining herd immunity via immunization, meeting a process improvement
    objective, etc.
    """
    
    resource_type = "Goal"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """External Ids for this goal."""
    _attribute_docstrings['lifecycleStatus'] = """The state of the goal throughout its lifecycle."""
    _attribute_docstrings['achievementStatus'] = """Describes the progression, or lack thereof, towards the goal against the target."""
    _attribute_docstrings['category'] = """Indicates a category the goal falls within."""
    _attribute_docstrings['priority'] = """Identifies the mutually agreed level of importance associated with reaching/sustaining the goal."""
    _attribute_docstrings['description'] = """Code or text describing goal."""
    _attribute_docstrings['subject'] = """Who this goal is intended for."""
    _attribute_docstrings['startDate'] = """When goal pursuit begins."""
    _attribute_docstrings['startCodeableConcept'] = """When goal pursuit begins."""
    _attribute_docstrings['target'] = """Target outcome for the goal."""
    _attribute_docstrings['statusDate'] = """When goal status took effect."""
    _attribute_docstrings['statusReason'] = """Reason for current status."""
    _attribute_docstrings['expressedBy'] = """Who's responsible for creating Goal?."""
    _attribute_docstrings['addresses'] = """Issues addressed by this goal."""
    _attribute_docstrings['note'] = """Comments about the goal."""
    _attribute_docstrings['outcomeCode'] = """What result was achieved regarding the goal?."""
    _attribute_docstrings['outcomeReference'] = """Observation that resulted from goal."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['lifecycleStatus'] = {
        'url': 'http://hl7.org/fhir/goal-status',
        'restricted_to': ['proposed', 'planned', 'accepted', 'active', 'on-hold', 'completed', 'cancelled', 'entered-in-error', 'rejected'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['achievementStatus'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/goal-achievement',
        'restricted_to': ['in-progress', 'improving', 'worsening', 'no-change', 'achieved', 'sustaining', 'not-achieved', 'no-progress', 'not-attainable'],
        'binding_strength': 'preferred',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['category'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/goal-category',
        'restricted_to': ['dietary', 'safety', 'behavioral', 'nursing', 'physiotherapy'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['priority'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/goal-priority',
        'restricted_to': ['high-priority', 'medium-priority', 'low-priority'],
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
        
        self.identifier = None
        """ External Ids for this goal.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.lifecycleStatus = None
        """ The state of the goal throughout its lifecycle.
        Type `str`. """
        
        self.achievementStatus = None
        """ Describes the progression, or lack thereof, towards the goal
        against the target.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.category = None
        """ Indicates a category the goal falls within.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.priority = None
        """ Identifies the mutually agreed level of importance associated with
        reaching/sustaining the goal.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.description = None
        """ Code or text describing goal.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subject = None
        """ Who this goal is intended for.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.startDate = None
        """ When goal pursuit begins.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.startCodeableConcept = None
        """ When goal pursuit begins.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.target = None
        """ Target outcome for the goal.
        List of `GoalTarget` items (represented as `dict` in JSON). """
        
        self.statusDate = None
        """ When goal status took effect.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.statusReason = None
        """ Reason for current status.
        Type `str`. """
        
        self.expressedBy = None
        """ Who's responsible for creating Goal?.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.addresses = None
        """ Issues addressed by this goal.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.note = None
        """ Comments about the goal.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        self.outcomeCode = None
        """ What result was achieved regarding the goal?.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.outcomeReference = None
        """ Observation that resulted from goal.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(Goal, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Goal, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("lifecycleStatus", "lifecycleStatus", str, False, None, True),
            ("achievementStatus", "achievementStatus", codeableconcept.CodeableConcept, False, None, False),
            ("category", "category", codeableconcept.CodeableConcept, True, None, False),
            ("priority", "priority", codeableconcept.CodeableConcept, False, None, False),
            ("description", "description", codeableconcept.CodeableConcept, False, None, True),
            ("subject", "subject", fhirreference.FHIRReference, False, None, True),
            ("startDate", "startDate", fhirdate.FHIRDate, False, "start", False),
            ("startCodeableConcept", "startCodeableConcept", codeableconcept.CodeableConcept, False, "start", False),
            ("target", "target", GoalTarget, True, None, False),
            ("statusDate", "statusDate", fhirdate.FHIRDate, False, None, False),
            ("statusReason", "statusReason", str, False, None, False),
            ("expressedBy", "expressedBy", fhirreference.FHIRReference, False, None, False),
            ("addresses", "addresses", fhirreference.FHIRReference, True, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
            ("outcomeCode", "outcomeCode", codeableconcept.CodeableConcept, True, None, False),
            ("outcomeReference", "outcomeReference", fhirreference.FHIRReference, True, None, False),
        ])
        return js


from . import backboneelement

class GoalTarget(backboneelement.BackboneElement):
    """ Target outcome for the goal.
    
    Indicates what should be done by when.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['measure'] = """The parameter whose value is being tracked."""
    _attribute_docstrings['detailQuantity'] = """The target value to be achieved."""
    _attribute_docstrings['detailRange'] = """The target value to be achieved."""
    _attribute_docstrings['detailCodeableConcept'] = """The target value to be achieved."""
    _attribute_docstrings['detailString'] = """The target value to be achieved."""
    _attribute_docstrings['detailBoolean'] = """The target value to be achieved."""
    _attribute_docstrings['detailInteger'] = """The target value to be achieved."""
    _attribute_docstrings['detailRatio'] = """The target value to be achieved."""
    _attribute_docstrings['dueDate'] = """Reach goal on or before."""
    _attribute_docstrings['dueDuration'] = """Reach goal on or before."""

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
        
        self.measure = None
        """ The parameter whose value is being tracked.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.detailQuantity = None
        """ The target value to be achieved.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.detailRange = None
        """ The target value to be achieved.
        Type `Range` (represented as `dict` in JSON). """
        
        self.detailCodeableConcept = None
        """ The target value to be achieved.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.detailString = None
        """ The target value to be achieved.
        Type `str`. """
        
        self.detailBoolean = None
        """ The target value to be achieved.
        Type `bool`. """
        
        self.detailInteger = None
        """ The target value to be achieved.
        Type `int`. """
        
        self.detailRatio = None
        """ The target value to be achieved.
        Type `Ratio` (represented as `dict` in JSON). """
        
        self.dueDate = None
        """ Reach goal on or before.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.dueDuration = None
        """ Reach goal on or before.
        Type `Duration` (represented as `dict` in JSON). """
        
        super(GoalTarget, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(GoalTarget, self).elementProperties()
        js.extend([
            ("measure", "measure", codeableconcept.CodeableConcept, False, None, False),
            ("detailQuantity", "detailQuantity", quantity.Quantity, False, "detail", False),
            ("detailRange", "detailRange", range.Range, False, "detail", False),
            ("detailCodeableConcept", "detailCodeableConcept", codeableconcept.CodeableConcept, False, "detail", False),
            ("detailString", "detailString", str, False, "detail", False),
            ("detailBoolean", "detailBoolean", bool, False, "detail", False),
            ("detailInteger", "detailInteger", int, False, "detail", False),
            ("detailRatio", "detailRatio", ratio.Ratio, False, "detail", False),
            ("dueDate", "dueDate", fhirdate.FHIRDate, False, "due", False),
            ("dueDuration", "dueDuration", duration.Duration, False, "due", False),
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
    from . import quantity
except ImportError:
    quantity = sys.modules[__package__ + '.quantity']
try:
    from . import range
except ImportError:
    range = sys.modules[__package__ + '.range']
try:
    from . import ratio
except ImportError:
    ratio = sys.modules[__package__ + '.ratio']
