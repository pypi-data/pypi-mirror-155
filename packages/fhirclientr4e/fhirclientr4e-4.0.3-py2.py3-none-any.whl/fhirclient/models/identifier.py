#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Identifier) on 2022-06-21.
#  2022, SMART Health IT.


from . import element

class Identifier(element.Element):
    """ An identifier intended for computation.
    
    An identifier - identifies some entity uniquely and unambiguously.
    Typically this is used for business identifiers.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['use'] = """The purpose of this identifier."""
    _attribute_docstrings['type'] = """Description of identifier."""
    _attribute_docstrings['system'] = """The namespace for the identifier value."""
    _attribute_docstrings['value'] = """The value that is unique."""
    _attribute_docstrings['period'] = """Time period when id is/was valid for use."""
    _attribute_docstrings['assigner'] = """Organization that issued id (may be just text)."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['use'] = {
        'url': 'http://hl7.org/fhir/identifier-use',
        'restricted_to': ['usual', 'official', 'temp', 'secondary', 'old'],
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
        
        self.use = None
        """ The purpose of this identifier.
        Type `str`. """
        
        self.type = None
        """ Description of identifier.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.system = None
        """ The namespace for the identifier value.
        Type `str`. """
        
        self.value = None
        """ The value that is unique.
        Type `str`. """
        
        self.period = None
        """ Time period when id is/was valid for use.
        Type `Period` (represented as `dict` in JSON). """
        
        self.assigner = None
        """ Organization that issued id (may be just text).
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(Identifier, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Identifier, self).elementProperties()
        js.extend([
            ("use", "use", str, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("system", "system", str, False, None, False),
            ("value", "value", str, False, None, False),
            ("period", "period", period.Period, False, None, False),
            ("assigner", "assigner", fhirreference.FHIRReference, False, None, False),
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
    from . import period
except ImportError:
    period = sys.modules[__package__ + '.period']
