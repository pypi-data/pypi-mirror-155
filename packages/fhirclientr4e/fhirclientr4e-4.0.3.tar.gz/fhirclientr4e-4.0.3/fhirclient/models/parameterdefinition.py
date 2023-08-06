#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/ParameterDefinition) on 2022-06-21.
#  2022, SMART Health IT.


from . import element

class ParameterDefinition(element.Element):
    """ Definition of a parameter to a module.
    
    The parameters to the module. This collection specifies both the input and
    output parameters. Input parameters are provided by the caller as part of
    the $evaluate operation. Output parameters are included in the
    GuidanceResponse.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['name'] = """Name used to access the parameter value."""
    _attribute_docstrings['use'] = """Whether the parameter is input or output for the module."""
    _attribute_docstrings['min'] = """Minimum cardinality."""
    _attribute_docstrings['max'] = """Maximum cardinality (a number of *)."""
    _attribute_docstrings['documentation'] = """A brief description of the parameter."""
    _attribute_docstrings['type'] = """What type of value."""
    _attribute_docstrings['profile'] = """What profile the value is expected to be."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['use'] = {
        'url': 'http://hl7.org/fhir/operation-parameter-use',
        'restricted_to': ['in', 'out'],
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
        
        self.name = None
        """ Name used to access the parameter value.
        Type `str`. """
        
        self.use = None
        """ Whether the parameter is input or output for the module.
        Type `str`. """
        
        self.min = None
        """ Minimum cardinality.
        Type `int`. """
        
        self.max = None
        """ Maximum cardinality (a number of *).
        Type `str`. """
        
        self.documentation = None
        """ A brief description of the parameter.
        Type `str`. """
        
        self.type = None
        """ What type of value.
        Type `str`. """
        
        self.profile = None
        """ What profile the value is expected to be.
        Type `str`. """
        
        super(ParameterDefinition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ParameterDefinition, self).elementProperties()
        js.extend([
            ("name", "name", str, False, None, False),
            ("use", "use", str, False, None, True),
            ("min", "min", int, False, None, False),
            ("max", "max", str, False, None, False),
            ("documentation", "documentation", str, False, None, False),
            ("type", "type", str, False, None, True),
            ("profile", "profile", str, False, None, False),
        ])
        return js


