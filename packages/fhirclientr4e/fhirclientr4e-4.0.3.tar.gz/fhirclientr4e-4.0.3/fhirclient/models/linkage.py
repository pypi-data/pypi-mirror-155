#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Linkage) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Linkage(domainresource.DomainResource):
    """ Links records for 'same' item.
    
    Identifies two or more records (resource instances) that refer to the same
    real-world "occurrence".
    """
    
    resource_type = "Linkage"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['active'] = """Whether this linkage assertion is active or not."""
    _attribute_docstrings['author'] = """Who is responsible for linkages."""
    _attribute_docstrings['item'] = """Item to be linked."""

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
        
        self.active = None
        """ Whether this linkage assertion is active or not.
        Type `bool`. """
        
        self.author = None
        """ Who is responsible for linkages.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.item = None
        """ Item to be linked.
        List of `LinkageItem` items (represented as `dict` in JSON). """
        
        super(Linkage, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Linkage, self).elementProperties()
        js.extend([
            ("active", "active", bool, False, None, False),
            ("author", "author", fhirreference.FHIRReference, False, None, False),
            ("item", "item", LinkageItem, True, None, True),
        ])
        return js


from . import backboneelement

class LinkageItem(backboneelement.BackboneElement):
    """ Item to be linked.
    
    Identifies which record considered as the reference to the same real-world
    occurrence as well as how the items should be evaluated within the
    collection of linked items.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Distinguishes which item is "source of truth" (if any) and which items are no longer considered to be current representations."""
    _attribute_docstrings['resource'] = """Resource being linked."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://hl7.org/fhir/linkage-type',
        'restricted_to': ['source', 'alternate', 'historical'],
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
        """ Distinguishes which item is "source of truth" (if any) and which
        items are no longer considered to be current representations.
        Type `str`. """
        
        self.resource = None
        """ Resource being linked.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(LinkageItem, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(LinkageItem, self).elementProperties()
        js.extend([
            ("type", "type", str, False, None, True),
            ("resource", "resource", fhirreference.FHIRReference, False, None, True),
        ])
        return js


import sys
try:
    from . import fhirreference
except ImportError:
    fhirreference = sys.modules[__package__ + '.fhirreference']
