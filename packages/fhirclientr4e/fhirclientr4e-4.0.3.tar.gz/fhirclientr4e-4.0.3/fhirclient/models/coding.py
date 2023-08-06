#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Coding) on 2022-06-21.
#  2022, SMART Health IT.


from . import element

class Coding(element.Element):
    """ A reference to a code defined by a terminology system.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['system'] = """Identity of the terminology system."""
    _attribute_docstrings['version'] = """Version of the system - if relevant."""
    _attribute_docstrings['code'] = """Symbol in syntax defined by the system."""
    _attribute_docstrings['display'] = """Representation defined by the system."""
    _attribute_docstrings['userSelected'] = """If this coding was chosen directly by the user."""

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
        
        self.system = None
        """ Identity of the terminology system.
        Type `str`. """
        
        self.version = None
        """ Version of the system - if relevant.
        Type `str`. """
        
        self.code = None
        """ Symbol in syntax defined by the system.
        Type `str`. """
        
        self.display = None
        """ Representation defined by the system.
        Type `str`. """
        
        self.userSelected = None
        """ If this coding was chosen directly by the user.
        Type `bool`. """
        
        super(Coding, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Coding, self).elementProperties()
        js.extend([
            ("system", "system", str, False, None, False),
            ("version", "version", str, False, None, False),
            ("code", "code", str, False, None, False),
            ("display", "display", str, False, None, False),
            ("userSelected", "userSelected", bool, False, None, False),
        ])
        return js


