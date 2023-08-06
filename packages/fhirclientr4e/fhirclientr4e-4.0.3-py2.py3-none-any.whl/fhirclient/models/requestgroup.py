#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/RequestGroup) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class RequestGroup(domainresource.DomainResource):
    """ A group of related requests.
    
    A group of related requests that can be used to capture intended activities
    that have inter-dependencies such as "give this medication after that one".
    """
    
    resource_type = "RequestGroup"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business identifier."""
    _attribute_docstrings['instantiatesCanonical'] = """Instantiates FHIR protocol or definition."""
    _attribute_docstrings['instantiatesUri'] = """Instantiates external protocol or definition."""
    _attribute_docstrings['basedOn'] = """Fulfills plan, proposal, or order."""
    _attribute_docstrings['replaces'] = """Request(s) replaced by this request."""
    _attribute_docstrings['groupIdentifier'] = """Composite request this is part of."""
    _attribute_docstrings['status'] = """The current state of the request. For request groups, the status reflects the status of all the requests in the group."""
    _attribute_docstrings['intent'] = """Indicates the level of authority/intentionality associated with the request and where the request fits into the workflow chain."""
    _attribute_docstrings['priority'] = """Indicates how quickly the request should be addressed with respect to other requests."""
    _attribute_docstrings['code'] = """What's being requested/ordered."""
    _attribute_docstrings['subject'] = """Who the request group is about."""
    _attribute_docstrings['encounter'] = """Created as part of."""
    _attribute_docstrings['authoredOn'] = """When the request group was authored."""
    _attribute_docstrings['author'] = """Device or practitioner that authored the request group."""
    _attribute_docstrings['reasonCode'] = """Why the request group is needed."""
    _attribute_docstrings['reasonReference'] = """Why the request group is needed."""
    _attribute_docstrings['note'] = """Additional notes about the response."""
    _attribute_docstrings['action'] = """Proposed actions, if any."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/request-status',
        'restricted_to': ['draft', 'active', 'on-hold', 'revoked', 'completed', 'entered-in-error', 'unknown'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['intent'] = {
        'url': 'http://hl7.org/fhir/request-intent',
        'restricted_to': ['proposal', 'plan', 'directive', 'order', 'original-order', 'reflex-order', 'filler-order', 'instance-order', 'option'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['priority'] = {
        'url': 'http://hl7.org/fhir/request-priority',
        'restricted_to': ['routine', 'urgent', 'asap', 'stat'],
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
        """ Business identifier.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.instantiatesCanonical = None
        """ Instantiates FHIR protocol or definition.
        List of `str` items. """
        
        self.instantiatesUri = None
        """ Instantiates external protocol or definition.
        List of `str` items. """
        
        self.basedOn = None
        """ Fulfills plan, proposal, or order.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.replaces = None
        """ Request(s) replaced by this request.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.groupIdentifier = None
        """ Composite request this is part of.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.status = None
        """ The current state of the request. For request groups, the status
        reflects the status of all the requests in the group.
        Type `str`. """
        
        self.intent = None
        """ Indicates the level of authority/intentionality associated with the
        request and where the request fits into the workflow chain.
        Type `str`. """
        
        self.priority = None
        """ Indicates how quickly the request should be addressed with respect
        to other requests.
        Type `str`. """
        
        self.code = None
        """ What's being requested/ordered.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subject = None
        """ Who the request group is about.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Created as part of.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.authoredOn = None
        """ When the request group was authored.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.author = None
        """ Device or practitioner that authored the request group.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.reasonCode = None
        """ Why the request group is needed.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.reasonReference = None
        """ Why the request group is needed.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.note = None
        """ Additional notes about the response.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        self.action = None
        """ Proposed actions, if any.
        List of `RequestGroupAction` items (represented as `dict` in JSON). """
        
        super(RequestGroup, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(RequestGroup, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("instantiatesCanonical", "instantiatesCanonical", str, True, None, False),
            ("instantiatesUri", "instantiatesUri", str, True, None, False),
            ("basedOn", "basedOn", fhirreference.FHIRReference, True, None, False),
            ("replaces", "replaces", fhirreference.FHIRReference, True, None, False),
            ("groupIdentifier", "groupIdentifier", identifier.Identifier, False, None, False),
            ("status", "status", str, False, None, True),
            ("intent", "intent", str, False, None, True),
            ("priority", "priority", str, False, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("subject", "subject", fhirreference.FHIRReference, False, None, False),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("authoredOn", "authoredOn", fhirdate.FHIRDate, False, None, False),
            ("author", "author", fhirreference.FHIRReference, False, None, False),
            ("reasonCode", "reasonCode", codeableconcept.CodeableConcept, True, None, False),
            ("reasonReference", "reasonReference", fhirreference.FHIRReference, True, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
            ("action", "action", RequestGroupAction, True, None, False),
        ])
        return js


from . import backboneelement

class RequestGroupAction(backboneelement.BackboneElement):
    """ Proposed actions, if any.
    
    The actions, if any, produced by the evaluation of the artifact.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['prefix'] = """User-visible prefix for the action (e.g. 1. or A.)."""
    _attribute_docstrings['title'] = """User-visible title."""
    _attribute_docstrings['description'] = """Short description of the action."""
    _attribute_docstrings['textEquivalent'] = """Static text equivalent of the action, used if the dynamic aspects cannot be interpreted by the receiving system."""
    _attribute_docstrings['priority'] = """Indicates how quickly the action should be addressed with respect to other actions."""
    _attribute_docstrings['code'] = """Code representing the meaning of the action or sub-actions."""
    _attribute_docstrings['documentation'] = """Supporting documentation for the intended performer of the action."""
    _attribute_docstrings['condition'] = """Whether or not the action is applicable."""
    _attribute_docstrings['relatedAction'] = """Relationship to another action."""
    _attribute_docstrings['timingDateTime'] = """When the action should take place."""
    _attribute_docstrings['timingAge'] = """When the action should take place."""
    _attribute_docstrings['timingPeriod'] = """When the action should take place."""
    _attribute_docstrings['timingDuration'] = """When the action should take place."""
    _attribute_docstrings['timingRange'] = """When the action should take place."""
    _attribute_docstrings['timingTiming'] = """When the action should take place."""
    _attribute_docstrings['participant'] = """Who should perform the action."""
    _attribute_docstrings['type'] = """The type of action to perform (create, update, remove)."""
    _attribute_docstrings['groupingBehavior'] = """Defines the grouping behavior for the action and its children."""
    _attribute_docstrings['selectionBehavior'] = """Defines the selection behavior for the action and its children."""
    _attribute_docstrings['requiredBehavior'] = """Defines expectations around whether an action is required."""
    _attribute_docstrings['precheckBehavior'] = """Defines whether the action should usually be preselected."""
    _attribute_docstrings['cardinalityBehavior'] = """Defines whether the action can be selected multiple times."""
    _attribute_docstrings['resource'] = """The target of the action."""
    _attribute_docstrings['action'] = """Sub action."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['priority'] = {
        'url': 'http://hl7.org/fhir/request-priority',
        'restricted_to': ['routine', 'urgent', 'asap', 'stat'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/action-type',
        'restricted_to': ['create', 'update', 'remove', 'fire-event'],
        'binding_strength': 'extensible',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['groupingBehavior'] = {
        'url': 'http://hl7.org/fhir/action-grouping-behavior',
        'restricted_to': ['visual-group', 'logical-group', 'sentence-group'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['selectionBehavior'] = {
        'url': 'http://hl7.org/fhir/action-selection-behavior',
        'restricted_to': ['any', 'all', 'all-or-none', 'exactly-one', 'at-most-one', 'one-or-more'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['requiredBehavior'] = {
        'url': 'http://hl7.org/fhir/action-required-behavior',
        'restricted_to': ['must', 'could', 'must-unless-documented'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['precheckBehavior'] = {
        'url': 'http://hl7.org/fhir/action-precheck-behavior',
        'restricted_to': ['yes', 'no'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['cardinalityBehavior'] = {
        'url': 'http://hl7.org/fhir/action-cardinality-behavior',
        'restricted_to': ['single', 'multiple'],
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
        
        self.prefix = None
        """ User-visible prefix for the action (e.g. 1. or A.).
        Type `str`. """
        
        self.title = None
        """ User-visible title.
        Type `str`. """
        
        self.description = None
        """ Short description of the action.
        Type `str`. """
        
        self.textEquivalent = None
        """ Static text equivalent of the action, used if the dynamic aspects
        cannot be interpreted by the receiving system.
        Type `str`. """
        
        self.priority = None
        """ Indicates how quickly the action should be addressed with respect
        to other actions.
        Type `str`. """
        
        self.code = None
        """ Code representing the meaning of the action or sub-actions.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.documentation = None
        """ Supporting documentation for the intended performer of the action.
        List of `RelatedArtifact` items (represented as `dict` in JSON). """
        
        self.condition = None
        """ Whether or not the action is applicable.
        List of `RequestGroupActionCondition` items (represented as `dict` in JSON). """
        
        self.relatedAction = None
        """ Relationship to another action.
        List of `RequestGroupActionRelatedAction` items (represented as `dict` in JSON). """
        
        self.timingDateTime = None
        """ When the action should take place.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.timingAge = None
        """ When the action should take place.
        Type `Age` (represented as `dict` in JSON). """
        
        self.timingPeriod = None
        """ When the action should take place.
        Type `Period` (represented as `dict` in JSON). """
        
        self.timingDuration = None
        """ When the action should take place.
        Type `Duration` (represented as `dict` in JSON). """
        
        self.timingRange = None
        """ When the action should take place.
        Type `Range` (represented as `dict` in JSON). """
        
        self.timingTiming = None
        """ When the action should take place.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.participant = None
        """ Who should perform the action.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.type = None
        """ The type of action to perform (create, update, remove).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.groupingBehavior = None
        """ Defines the grouping behavior for the action and its children.
        Type `str`. """
        
        self.selectionBehavior = None
        """ Defines the selection behavior for the action and its children.
        Type `str`. """
        
        self.requiredBehavior = None
        """ Defines expectations around whether an action is required.
        Type `str`. """
        
        self.precheckBehavior = None
        """ Defines whether the action should usually be preselected.
        Type `str`. """
        
        self.cardinalityBehavior = None
        """ Defines whether the action can be selected multiple times.
        Type `str`. """
        
        self.resource = None
        """ The target of the action.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.action = None
        """ Sub action.
        List of `RequestGroupAction` items (represented as `dict` in JSON). """
        
        super(RequestGroupAction, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(RequestGroupAction, self).elementProperties()
        js.extend([
            ("prefix", "prefix", str, False, None, False),
            ("title", "title", str, False, None, False),
            ("description", "description", str, False, None, False),
            ("textEquivalent", "textEquivalent", str, False, None, False),
            ("priority", "priority", str, False, None, False),
            ("code", "code", codeableconcept.CodeableConcept, True, None, False),
            ("documentation", "documentation", relatedartifact.RelatedArtifact, True, None, False),
            ("condition", "condition", RequestGroupActionCondition, True, None, False),
            ("relatedAction", "relatedAction", RequestGroupActionRelatedAction, True, None, False),
            ("timingDateTime", "timingDateTime", fhirdate.FHIRDate, False, "timing", False),
            ("timingAge", "timingAge", age.Age, False, "timing", False),
            ("timingPeriod", "timingPeriod", period.Period, False, "timing", False),
            ("timingDuration", "timingDuration", duration.Duration, False, "timing", False),
            ("timingRange", "timingRange", range.Range, False, "timing", False),
            ("timingTiming", "timingTiming", timing.Timing, False, "timing", False),
            ("participant", "participant", fhirreference.FHIRReference, True, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("groupingBehavior", "groupingBehavior", str, False, None, False),
            ("selectionBehavior", "selectionBehavior", str, False, None, False),
            ("requiredBehavior", "requiredBehavior", str, False, None, False),
            ("precheckBehavior", "precheckBehavior", str, False, None, False),
            ("cardinalityBehavior", "cardinalityBehavior", str, False, None, False),
            ("resource", "resource", fhirreference.FHIRReference, False, None, False),
            ("action", "action", RequestGroupAction, True, None, False),
        ])
        return js


class RequestGroupActionCondition(backboneelement.BackboneElement):
    """ Whether or not the action is applicable.
    
    An expression that describes applicability criteria, or start/stop
    conditions for the action.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['kind'] = """The kind of condition."""
    _attribute_docstrings['expression'] = """Boolean-valued expression."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['kind'] = {
        'url': 'http://hl7.org/fhir/action-condition-kind',
        'restricted_to': ['applicability', 'start', 'stop'],
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
        
        self.kind = None
        """ The kind of condition.
        Type `str`. """
        
        self.expression = None
        """ Boolean-valued expression.
        Type `Expression` (represented as `dict` in JSON). """
        
        super(RequestGroupActionCondition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(RequestGroupActionCondition, self).elementProperties()
        js.extend([
            ("kind", "kind", str, False, None, True),
            ("expression", "expression", expression.Expression, False, None, False),
        ])
        return js


class RequestGroupActionRelatedAction(backboneelement.BackboneElement):
    """ Relationship to another action.
    
    A relationship to another action such as "before" or "30-60 minutes after
    start of".
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['actionId'] = """What action this is related to."""
    _attribute_docstrings['relationship'] = """The relationship of this action to the related action."""
    _attribute_docstrings['offsetDuration'] = """Time offset for the relationship."""
    _attribute_docstrings['offsetRange'] = """Time offset for the relationship."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['relationship'] = {
        'url': 'http://hl7.org/fhir/action-relationship-type',
        'restricted_to': ['before-start', 'before', 'before-end', 'concurrent-with-start', 'concurrent', 'concurrent-with-end', 'after-start', 'after', 'after-end'],
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
        
        self.actionId = None
        """ What action this is related to.
        Type `str`. """
        
        self.relationship = None
        """ The relationship of this action to the related action.
        Type `str`. """
        
        self.offsetDuration = None
        """ Time offset for the relationship.
        Type `Duration` (represented as `dict` in JSON). """
        
        self.offsetRange = None
        """ Time offset for the relationship.
        Type `Range` (represented as `dict` in JSON). """
        
        super(RequestGroupActionRelatedAction, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(RequestGroupActionRelatedAction, self).elementProperties()
        js.extend([
            ("actionId", "actionId", str, False, None, True),
            ("relationship", "relationship", str, False, None, True),
            ("offsetDuration", "offsetDuration", duration.Duration, False, "offset", False),
            ("offsetRange", "offsetRange", range.Range, False, "offset", False),
        ])
        return js


import sys
try:
    from . import age
except ImportError:
    age = sys.modules[__package__ + '.age']
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
    from . import expression
except ImportError:
    expression = sys.modules[__package__ + '.expression']
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
    from . import range
except ImportError:
    range = sys.modules[__package__ + '.range']
try:
    from . import relatedartifact
except ImportError:
    relatedartifact = sys.modules[__package__ + '.relatedartifact']
try:
    from . import timing
except ImportError:
    timing = sys.modules[__package__ + '.timing']
