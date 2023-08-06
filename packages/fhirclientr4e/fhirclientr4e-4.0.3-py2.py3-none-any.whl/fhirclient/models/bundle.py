#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Bundle) on 2022-06-21.
#  2022, SMART Health IT.


from . import resource

class Bundle(resource.Resource):
    """ Contains a collection of resources.
    
    A container for a collection of resources.
    """
    
    resource_type = "Bundle"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Persistent identifier for the bundle."""
    _attribute_docstrings['type'] = """Indicates the purpose of this bundle - how it is intended to be used."""
    _attribute_docstrings['timestamp'] = """When the bundle was assembled."""
    _attribute_docstrings['total'] = """If search, the total number of matches."""
    _attribute_docstrings['link'] = """Links related to this Bundle."""
    _attribute_docstrings['entry'] = """Entry in the bundle - will have a resource or information."""
    _attribute_docstrings['signature'] = """Digital Signature."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://hl7.org/fhir/bundle-type',
        'restricted_to': ['document', 'message', 'transaction', 'transaction-response', 'batch', 'batch-response', 'history', 'searchset', 'collection'],
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
        """ Persistent identifier for the bundle.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.type = None
        """ Indicates the purpose of this bundle - how it is intended to be
        used.
        Type `str`. """
        
        self.timestamp = None
        """ When the bundle was assembled.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.total = None
        """ If search, the total number of matches.
        Type `int`. """
        
        self.link = None
        """ Links related to this Bundle.
        List of `BundleLink` items (represented as `dict` in JSON). """
        
        self.entry = None
        """ Entry in the bundle - will have a resource or information.
        List of `BundleEntry` items (represented as `dict` in JSON). """
        
        self.signature = None
        """ Digital Signature.
        Type `Signature` (represented as `dict` in JSON). """
        
        super(Bundle, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Bundle, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, False, None, False),
            ("type", "type", str, False, None, True),
            ("timestamp", "timestamp", fhirdate.FHIRDate, False, None, False),
            ("total", "total", int, False, None, False),
            ("link", "link", BundleLink, True, None, False),
            ("entry", "entry", BundleEntry, True, None, False),
            ("signature", "signature", signature.Signature, False, None, False),
        ])
        return js


from . import backboneelement

class BundleEntry(backboneelement.BackboneElement):
    """ Entry in the bundle - will have a resource or information.
    
    An entry in a bundle resource - will either contain a resource or
    information about a resource (transactions and history only).
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['link'] = """Links related to this entry."""
    _attribute_docstrings['fullUrl'] = """URI for resource (Absolute URL server address or URI for UUID/OID)."""
    _attribute_docstrings['resource'] = """A resource in the bundle."""
    _attribute_docstrings['search'] = """Search related information."""
    _attribute_docstrings['request'] = """Additional execution information (transaction/batch/history)."""
    _attribute_docstrings['response'] = """Results of execution (transaction/batch/history)."""

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
        
        self.link = None
        """ Links related to this entry.
        List of `BundleLink` items (represented as `dict` in JSON). """
        
        self.fullUrl = None
        """ URI for resource (Absolute URL server address or URI for UUID/OID).
        Type `str`. """
        
        self.resource = None
        """ A resource in the bundle.
        Type `Resource` (represented as `dict` in JSON). """
        
        self.search = None
        """ Search related information.
        Type `BundleEntrySearch` (represented as `dict` in JSON). """
        
        self.request = None
        """ Additional execution information (transaction/batch/history).
        Type `BundleEntryRequest` (represented as `dict` in JSON). """
        
        self.response = None
        """ Results of execution (transaction/batch/history).
        Type `BundleEntryResponse` (represented as `dict` in JSON). """
        
        super(BundleEntry, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(BundleEntry, self).elementProperties()
        js.extend([
            ("link", "link", BundleLink, True, None, False),
            ("fullUrl", "fullUrl", str, False, None, False),
            ("resource", "resource", resource.Resource, False, None, False),
            ("search", "search", BundleEntrySearch, False, None, False),
            ("request", "request", BundleEntryRequest, False, None, False),
            ("response", "response", BundleEntryResponse, False, None, False),
        ])
        return js


class BundleEntryRequest(backboneelement.BackboneElement):
    """ Additional execution information (transaction/batch/history).
    
    Additional information about how this entry should be processed as part of
    a transaction or batch.  For history, it shows how the entry was processed
    to create the version contained in the entry.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['method'] = """In a transaction or batch, this is the HTTP action to be executed for this entry. In a history bundle, this indicates the HTTP action that occurred."""
    _attribute_docstrings['url'] = """URL for HTTP equivalent of this entry."""
    _attribute_docstrings['ifNoneMatch'] = """For managing cache currency."""
    _attribute_docstrings['ifModifiedSince'] = """For managing cache currency."""
    _attribute_docstrings['ifMatch'] = """For managing update contention."""
    _attribute_docstrings['ifNoneExist'] = """For conditional creates."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['method'] = {
        'url': 'http://hl7.org/fhir/http-verb',
        'restricted_to': ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'PATCH'],
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
        
        self.method = None
        """ In a transaction or batch, this is the HTTP action to be executed
        for this entry. In a history bundle, this indicates the HTTP action
        that occurred.
        Type `str`. """
        
        self.url = None
        """ URL for HTTP equivalent of this entry.
        Type `str`. """
        
        self.ifNoneMatch = None
        """ For managing cache currency.
        Type `str`. """
        
        self.ifModifiedSince = None
        """ For managing cache currency.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.ifMatch = None
        """ For managing update contention.
        Type `str`. """
        
        self.ifNoneExist = None
        """ For conditional creates.
        Type `str`. """
        
        super(BundleEntryRequest, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(BundleEntryRequest, self).elementProperties()
        js.extend([
            ("method", "method", str, False, None, True),
            ("url", "url", str, False, None, True),
            ("ifNoneMatch", "ifNoneMatch", str, False, None, False),
            ("ifModifiedSince", "ifModifiedSince", fhirdate.FHIRDate, False, None, False),
            ("ifMatch", "ifMatch", str, False, None, False),
            ("ifNoneExist", "ifNoneExist", str, False, None, False),
        ])
        return js


class BundleEntryResponse(backboneelement.BackboneElement):
    """ Results of execution (transaction/batch/history).
    
    Indicates the results of processing the corresponding 'request' entry in
    the batch or transaction being responded to or what the results of an
    operation where when returning history.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['status'] = """Status response code (text optional)."""
    _attribute_docstrings['location'] = """The location (if the operation returns a location)."""
    _attribute_docstrings['etag'] = """The Etag for the resource (if relevant)."""
    _attribute_docstrings['lastModified'] = """Server's date time modified."""
    _attribute_docstrings['outcome'] = """OperationOutcome with hints and warnings (for batch/transaction)."""

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
        
        self.status = None
        """ Status response code (text optional).
        Type `str`. """
        
        self.location = None
        """ The location (if the operation returns a location).
        Type `str`. """
        
        self.etag = None
        """ The Etag for the resource (if relevant).
        Type `str`. """
        
        self.lastModified = None
        """ Server's date time modified.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.outcome = None
        """ OperationOutcome with hints and warnings (for batch/transaction).
        Type `Resource` (represented as `dict` in JSON). """
        
        super(BundleEntryResponse, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(BundleEntryResponse, self).elementProperties()
        js.extend([
            ("status", "status", str, False, None, True),
            ("location", "location", str, False, None, False),
            ("etag", "etag", str, False, None, False),
            ("lastModified", "lastModified", fhirdate.FHIRDate, False, None, False),
            ("outcome", "outcome", resource.Resource, False, None, False),
        ])
        return js


class BundleEntrySearch(backboneelement.BackboneElement):
    """ Search related information.
    
    Information about the search process that lead to the creation of this
    entry.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['mode'] = """Why this entry is in the result set - whether it's included as a match or because of an _include requirement, or to convey information or warning information about the search process."""
    _attribute_docstrings['score'] = """Search ranking (between 0 and 1)."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['mode'] = {
        'url': 'http://hl7.org/fhir/search-entry-mode',
        'restricted_to': ['match', 'include', 'outcome'],
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
        
        self.mode = None
        """ Why this entry is in the result set - whether it's included as a
        match or because of an _include requirement, or to convey
        information or warning information about the search process.
        Type `str`. """
        
        self.score = None
        """ Search ranking (between 0 and 1).
        Type `float`. """
        
        super(BundleEntrySearch, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(BundleEntrySearch, self).elementProperties()
        js.extend([
            ("mode", "mode", str, False, None, False),
            ("score", "score", float, False, None, False),
        ])
        return js


class BundleLink(backboneelement.BackboneElement):
    """ Links related to this Bundle.
    
    A series of links that provide context to this bundle.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['relation'] = """See http://www.iana.org/assignments/link-relations/link-relations.xhtml#link-relations-1."""
    _attribute_docstrings['url'] = """Reference details for the link."""

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
        
        self.relation = None
        """ See http://www.iana.org/assignments/link-relations/link-
        relations.xhtml#link-relations-1.
        Type `str`. """
        
        self.url = None
        """ Reference details for the link.
        Type `str`. """
        
        super(BundleLink, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(BundleLink, self).elementProperties()
        js.extend([
            ("relation", "relation", str, False, None, True),
            ("url", "url", str, False, None, True),
        ])
        return js


import sys
try:
    from . import fhirdate
except ImportError:
    fhirdate = sys.modules[__package__ + '.fhirdate']
try:
    from . import identifier
except ImportError:
    identifier = sys.modules[__package__ + '.identifier']
try:
    from . import signature
except ImportError:
    signature = sys.modules[__package__ + '.signature']
