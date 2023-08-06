#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/List) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class List(domainresource.DomainResource):
    """ A list is a curated collection of resources.
    """
    
    resource_type = "List"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business identifier."""
    _attribute_docstrings['status'] = """Indicates the current state of this list."""
    _attribute_docstrings['mode'] = """How this list was prepared - whether it is a working list that is suitable for being maintained on an ongoing basis, or if it represents a snapshot of a list of items from another source, or whether it is a prepared list where items may be marked as added, modified or deleted."""
    _attribute_docstrings['title'] = """Descriptive name for the list."""
    _attribute_docstrings['code'] = """This code defines the purpose of the list - why it was created."""
    _attribute_docstrings['subject'] = """If all resources have the same subject."""
    _attribute_docstrings['encounter'] = """Context in which list created."""
    _attribute_docstrings['date'] = """When the list was prepared."""
    _attribute_docstrings['source'] = """Who and/or what defined the list contents (aka Author)."""
    _attribute_docstrings['orderedBy'] = """What order applies to the items in the list."""
    _attribute_docstrings['note'] = """Comments about the list."""
    _attribute_docstrings['entry'] = """Entries in the list."""
    _attribute_docstrings['emptyReason'] = """If the list is empty, why the list is empty."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/list-status',
        'restricted_to': ['current', 'retired', 'entered-in-error'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['mode'] = {
        'url': 'http://hl7.org/fhir/list-mode',
        'restricted_to': ['working', 'snapshot', 'changes'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['code'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/list-example-use-codes',
        'restricted_to': ['alerts', 'adverserxns', 'allergies', 'medications', 'problems', 'worklist', 'waiting', 'protocols', 'plans'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['orderedBy'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/list-order',
        'restricted_to': ['user', 'system', 'event-date', 'entry-date', 'priority', 'alphabetic', 'category', 'patient'],
        'binding_strength': 'preferred',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['emptyReason'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/list-empty-reason',
        'restricted_to': ['nilknown', 'notasked', 'withheld', 'unavailable', 'notstarted', 'closed'],
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
        """ Business identifier.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ Indicates the current state of this list.
        Type `str`. """
        
        self.mode = None
        """ How this list was prepared - whether it is a working list that is
        suitable for being maintained on an ongoing basis, or if it
        represents a snapshot of a list of items from another source, or
        whether it is a prepared list where items may be marked as added,
        modified or deleted.
        Type `str`. """
        
        self.title = None
        """ Descriptive name for the list.
        Type `str`. """
        
        self.code = None
        """ This code defines the purpose of the list - why it was created.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subject = None
        """ If all resources have the same subject.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Context in which list created.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.date = None
        """ When the list was prepared.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.source = None
        """ Who and/or what defined the list contents (aka Author).
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.orderedBy = None
        """ What order applies to the items in the list.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.note = None
        """ Comments about the list.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        self.entry = None
        """ Entries in the list.
        List of `ListEntry` items (represented as `dict` in JSON). """
        
        self.emptyReason = None
        """ If the list is empty, why the list is empty.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(List, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(List, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("mode", "mode", str, False, None, True),
            ("title", "title", str, False, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("subject", "subject", fhirreference.FHIRReference, False, None, False),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("source", "source", fhirreference.FHIRReference, False, None, False),
            ("orderedBy", "orderedBy", codeableconcept.CodeableConcept, False, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
            ("entry", "entry", ListEntry, True, None, False),
            ("emptyReason", "emptyReason", codeableconcept.CodeableConcept, False, None, False),
        ])
        return js


from . import backboneelement

class ListEntry(backboneelement.BackboneElement):
    """ Entries in the list.
    
    Entries in this list.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['flag'] = """Status/Workflow information about this item."""
    _attribute_docstrings['deleted'] = """If this item is actually marked as deleted."""
    _attribute_docstrings['date'] = """When item added to list."""
    _attribute_docstrings['item'] = """Actual entry."""

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
        
        self.flag = None
        """ Status/Workflow information about this item.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.deleted = None
        """ If this item is actually marked as deleted.
        Type `bool`. """
        
        self.date = None
        """ When item added to list.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.item = None
        """ Actual entry.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(ListEntry, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ListEntry, self).elementProperties()
        js.extend([
            ("flag", "flag", codeableconcept.CodeableConcept, False, None, False),
            ("deleted", "deleted", bool, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("item", "item", fhirreference.FHIRReference, False, None, True),
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
