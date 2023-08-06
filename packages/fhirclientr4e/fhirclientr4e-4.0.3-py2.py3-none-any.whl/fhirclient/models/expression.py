#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Expression) on 2022-06-21.
#  2022, SMART Health IT.


from . import element

class Expression(element.Element):
    """ An expression that can be used to generate a value.
    
    A expression that is evaluated in a specified context and returns a value.
    The context of use of the expression must specify the context in which the
    expression is evaluated, and how the result of the expression is used.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['description'] = """Natural language description of the condition."""
    _attribute_docstrings['name'] = """Short name assigned to expression for reuse."""
    _attribute_docstrings['language'] = """The media type of the language for the expression."""
    _attribute_docstrings['expression'] = """Expression in specified language."""
    _attribute_docstrings['reference'] = """Where the expression is found."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['language'] = {
        'url': 'http://hl7.org/fhir/expression-language',
        'restricted_to': ['text/cql', 'text/fhirpath', 'application/x-fhir-query'],
        'binding_strength': 'extensible',
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
        
        self.description = None
        """ Natural language description of the condition.
        Type `str`. """
        
        self.name = None
        """ Short name assigned to expression for reuse.
        Type `str`. """
        
        self.language = None
        """ The media type of the language for the expression.
        Type `str`. """
        
        self.expression = None
        """ Expression in specified language.
        Type `str`. """
        
        self.reference = None
        """ Where the expression is found.
        Type `str`. """
        
        super(Expression, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Expression, self).elementProperties()
        js.extend([
            ("description", "description", str, False, None, False),
            ("name", "name", str, False, None, False),
            ("language", "language", str, False, None, True),
            ("expression", "expression", str, False, None, False),
            ("reference", "reference", str, False, None, False),
        ])
        return js


