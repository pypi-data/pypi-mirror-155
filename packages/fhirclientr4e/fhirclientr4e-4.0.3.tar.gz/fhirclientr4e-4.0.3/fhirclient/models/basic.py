#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Basic) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Basic(domainresource.DomainResource):
    """ Resource for non-supported content.
    
    Basic is used for handling concepts not yet defined in FHIR, narrative-only
    resources that don't map to an existing resource, and custom resources not
    appropriate for inclusion in the FHIR specification.
    """
    
    resource_type = "Basic"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business identifier."""
    _attribute_docstrings['code'] = """Identifies the 'type' of resource - equivalent to the resource name for other resources."""
    _attribute_docstrings['subject'] = """Identifies the focus of this resource."""
    _attribute_docstrings['created'] = """When created."""
    _attribute_docstrings['author'] = """Who created."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['code'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/basic-resource-type',
        'restricted_to': ['consent', 'referral', 'advevent', 'aptmtreq', 'transfer', 'diet', 'adminact', 'exposure', 'investigation', 'account', 'invoice', 'adjudicat', 'predetreq', 'predetermine', 'study', 'protocol'],
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
        """ Business identifier.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.code = None
        """ Identifies the 'type' of resource - equivalent to the resource name
        for other resources.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subject = None
        """ Identifies the focus of this resource.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.created = None
        """ When created.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.author = None
        """ Who created.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(Basic, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Basic, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, True),
            ("subject", "subject", fhirreference.FHIRReference, False, None, False),
            ("created", "created", fhirdate.FHIRDate, False, None, False),
            ("author", "author", fhirreference.FHIRReference, False, None, False),
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
    from . import identifier
except ImportError:
    identifier = sys.modules[__package__ + '.identifier']
