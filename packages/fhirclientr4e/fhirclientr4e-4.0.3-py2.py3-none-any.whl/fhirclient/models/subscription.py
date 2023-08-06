#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Subscription) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Subscription(domainresource.DomainResource):
    """ Server push subscription criteria.
    
    The subscription resource is used to define a push-based subscription from
    a server to another system. Once a subscription is registered with the
    server, the server checks every resource that is created or updated, and if
    the resource matches the given criteria, it sends a message on the defined
    "channel" so that another system can take an appropriate action.
    """
    
    resource_type = "Subscription"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['status'] = """The status of the subscription, which marks the server state for managing the subscription."""
    _attribute_docstrings['contact'] = """Contact details for source (e.g. troubleshooting)."""
    _attribute_docstrings['end'] = """When to automatically delete the subscription."""
    _attribute_docstrings['reason'] = """Description of why this subscription was created."""
    _attribute_docstrings['criteria'] = """Rule for server push."""
    _attribute_docstrings['error'] = """Latest error note."""
    _attribute_docstrings['channel'] = """The channel on which to report matches to the criteria."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/subscription-status',
        'restricted_to': ['requested', 'active', 'error', 'off'],
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
        
        self.status = None
        """ The status of the subscription, which marks the server state for
        managing the subscription.
        Type `str`. """
        
        self.contact = None
        """ Contact details for source (e.g. troubleshooting).
        List of `ContactPoint` items (represented as `dict` in JSON). """
        
        self.end = None
        """ When to automatically delete the subscription.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.reason = None
        """ Description of why this subscription was created.
        Type `str`. """
        
        self.criteria = None
        """ Rule for server push.
        Type `str`. """
        
        self.error = None
        """ Latest error note.
        Type `str`. """
        
        self.channel = None
        """ The channel on which to report matches to the criteria.
        Type `SubscriptionChannel` (represented as `dict` in JSON). """
        
        super(Subscription, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Subscription, self).elementProperties()
        js.extend([
            ("status", "status", str, False, None, True),
            ("contact", "contact", contactpoint.ContactPoint, True, None, False),
            ("end", "end", fhirdate.FHIRDate, False, None, False),
            ("reason", "reason", str, False, None, True),
            ("criteria", "criteria", str, False, None, True),
            ("error", "error", str, False, None, False),
            ("channel", "channel", SubscriptionChannel, False, None, True),
        ])
        return js


from . import backboneelement

class SubscriptionChannel(backboneelement.BackboneElement):
    """ The channel on which to report matches to the criteria.
    
    Details where to send notifications when resources are received that meet
    the criteria.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """The type of channel to send notifications on."""
    _attribute_docstrings['endpoint'] = """Where the channel points to."""
    _attribute_docstrings['payload'] = """MIME type to send, or omit for no payload."""
    _attribute_docstrings['header'] = """Usage depends on the channel type."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://hl7.org/fhir/subscription-channel-type',
        'restricted_to': ['rest-hook', 'websocket', 'email', 'sms', 'message'],
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
        
        self.type = None
        """ The type of channel to send notifications on.
        Type `str`. """
        
        self.endpoint = None
        """ Where the channel points to.
        Type `str`. """
        
        self.payload = None
        """ MIME type to send, or omit for no payload.
        Type `str`. """
        
        self.header = None
        """ Usage depends on the channel type.
        List of `str` items. """
        
        super(SubscriptionChannel, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SubscriptionChannel, self).elementProperties()
        js.extend([
            ("type", "type", str, False, None, True),
            ("endpoint", "endpoint", str, False, None, False),
            ("payload", "payload", str, False, None, False),
            ("header", "header", str, True, None, False),
        ])
        return js


import sys
try:
    from . import contactpoint
except ImportError:
    contactpoint = sys.modules[__package__ + '.contactpoint']
try:
    from . import fhirdate
except ImportError:
    fhirdate = sys.modules[__package__ + '.fhirdate']
