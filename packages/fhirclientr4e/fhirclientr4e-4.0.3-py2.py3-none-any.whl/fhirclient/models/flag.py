#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Flag) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Flag(domainresource.DomainResource):
    """ Key information to flag to healthcare providers.
    
    Prospective warnings of potential issues when providing care to the
    patient.
    """
    
    resource_type = "Flag"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business identifier."""
    _attribute_docstrings['status'] = """Supports basic workflow."""
    _attribute_docstrings['category'] = """Allows a flag to be divided into different categories like clinical, administrative etc. Intended to be used as a means of filtering which flags are displayed to particular user or in a given context."""
    _attribute_docstrings['code'] = """Coded or textual message to display to user."""
    _attribute_docstrings['subject'] = """Who/What is flag about?."""
    _attribute_docstrings['period'] = """Time period when flag is active."""
    _attribute_docstrings['encounter'] = """Alert relevant during encounter."""
    _attribute_docstrings['author'] = """Flag creator."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/flag-status',
        'restricted_to': ['active', 'inactive', 'entered-in-error'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['category'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/flag-category',
        'restricted_to': ['diet', 'drug', 'lab', 'admin', 'contact', 'clinical', 'behavioral', 'research', 'advance-directive', 'safety'],
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
        
        self.status = None
        """ Supports basic workflow.
        Type `str`. """
        
        self.category = None
        """ Allows a flag to be divided into different categories like
        clinical, administrative etc. Intended to be used as a means of
        filtering which flags are displayed to particular user or in a
        given context.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.code = None
        """ Coded or textual message to display to user.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subject = None
        """ Who/What is flag about?.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.period = None
        """ Time period when flag is active.
        Type `Period` (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Alert relevant during encounter.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.author = None
        """ Flag creator.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(Flag, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Flag, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("category", "category", codeableconcept.CodeableConcept, True, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, True),
            ("subject", "subject", fhirreference.FHIRReference, False, None, True),
            ("period", "period", period.Period, False, None, False),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("author", "author", fhirreference.FHIRReference, False, None, False),
        ])
        return js


import sys
try:
    from . import codeableconcept
except ImportError:
    codeableconcept = sys.modules[__package__ + '.codeableconcept']
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
