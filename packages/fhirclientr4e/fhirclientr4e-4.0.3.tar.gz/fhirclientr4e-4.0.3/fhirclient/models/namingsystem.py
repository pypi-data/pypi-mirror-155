#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/NamingSystem) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class NamingSystem(domainresource.DomainResource):
    """ System of unique identification.
    
    A curated namespace that issues unique symbols within that namespace for
    the identification of concepts, people, devices, etc.  Represents a
    "System" used within the Identifier and Coding data types.
    """
    
    resource_type = "NamingSystem"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['name'] = """Name for this naming system (computer friendly)."""
    _attribute_docstrings['status'] = """The status of this naming system. Enables tracking the life-cycle of the content."""
    _attribute_docstrings['kind'] = """Indicates the purpose for the naming system - what kinds of things does it make unique?"""
    _attribute_docstrings['date'] = """Date last changed."""
    _attribute_docstrings['publisher'] = """Name of the publisher (organization or individual)."""
    _attribute_docstrings['contact'] = """Contact details for the publisher."""
    _attribute_docstrings['responsible'] = """Who maintains system namespace?."""
    _attribute_docstrings['type'] = """e.g. driver,  provider,  patient, bank etc.."""
    _attribute_docstrings['description'] = """Natural language description of the naming system."""
    _attribute_docstrings['useContext'] = """The context that the content is intended to support."""
    _attribute_docstrings['jurisdiction'] = """Intended jurisdiction for naming system (if applicable)."""
    _attribute_docstrings['usage'] = """How/where is it used."""
    _attribute_docstrings['uniqueId'] = """Unique identifiers used for system."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/publication-status',
        'restricted_to': ['draft', 'active', 'retired', 'unknown'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['kind'] = {
        'url': 'http://hl7.org/fhir/namingsystem-type',
        'restricted_to': ['codesystem', 'identifier', 'root'],
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
        """ Name for this naming system (computer friendly).
        Type `str`. """
        
        self.status = None
        """ The status of this naming system. Enables tracking the life-cycle
        of the content.
        Type `str`. """
        
        self.kind = None
        """ Indicates the purpose for the naming system - what kinds of things
        does it make unique?.
        Type `str`. """
        
        self.date = None
        """ Date last changed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.publisher = None
        """ Name of the publisher (organization or individual).
        Type `str`. """
        
        self.contact = None
        """ Contact details for the publisher.
        List of `ContactDetail` items (represented as `dict` in JSON). """
        
        self.responsible = None
        """ Who maintains system namespace?.
        Type `str`. """
        
        self.type = None
        """ e.g. driver,  provider,  patient, bank etc.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.description = None
        """ Natural language description of the naming system.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for naming system (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.usage = None
        """ How/where is it used.
        Type `str`. """
        
        self.uniqueId = None
        """ Unique identifiers used for system.
        List of `NamingSystemUniqueId` items (represented as `dict` in JSON). """
        
        super(NamingSystem, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(NamingSystem, self).elementProperties()
        js.extend([
            ("name", "name", str, False, None, True),
            ("status", "status", str, False, None, True),
            ("kind", "kind", str, False, None, True),
            ("date", "date", fhirdate.FHIRDate, False, None, True),
            ("publisher", "publisher", str, False, None, False),
            ("contact", "contact", contactdetail.ContactDetail, True, None, False),
            ("responsible", "responsible", str, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("description", "description", str, False, None, False),
            ("useContext", "useContext", usagecontext.UsageContext, True, None, False),
            ("jurisdiction", "jurisdiction", codeableconcept.CodeableConcept, True, None, False),
            ("usage", "usage", str, False, None, False),
            ("uniqueId", "uniqueId", NamingSystemUniqueId, True, None, True),
        ])
        return js


from . import backboneelement

class NamingSystemUniqueId(backboneelement.BackboneElement):
    """ Unique identifiers used for system.
    
    Indicates how the system may be identified when referenced in electronic
    exchange.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Identifies the unique identifier scheme used for this particular identifier."""
    _attribute_docstrings['value'] = """The unique identifier."""
    _attribute_docstrings['preferred'] = """Is this the id that should be used for this type."""
    _attribute_docstrings['comment'] = """Notes about identifier usage."""
    _attribute_docstrings['period'] = """When is identifier valid?."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://hl7.org/fhir/namingsystem-identifier-type',
        'restricted_to': ['oid', 'uuid', 'uri', 'other'],
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
        """ Identifies the unique identifier scheme used for this particular
        identifier.
        Type `str`. """
        
        self.value = None
        """ The unique identifier.
        Type `str`. """
        
        self.preferred = None
        """ Is this the id that should be used for this type.
        Type `bool`. """
        
        self.comment = None
        """ Notes about identifier usage.
        Type `str`. """
        
        self.period = None
        """ When is identifier valid?.
        Type `Period` (represented as `dict` in JSON). """
        
        super(NamingSystemUniqueId, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(NamingSystemUniqueId, self).elementProperties()
        js.extend([
            ("type", "type", str, False, None, True),
            ("value", "value", str, False, None, True),
            ("preferred", "preferred", bool, False, None, False),
            ("comment", "comment", str, False, None, False),
            ("period", "period", period.Period, False, None, False),
        ])
        return js


import sys
try:
    from . import codeableconcept
except ImportError:
    codeableconcept = sys.modules[__package__ + '.codeableconcept']
try:
    from . import contactdetail
except ImportError:
    contactdetail = sys.modules[__package__ + '.contactdetail']
try:
    from . import fhirdate
except ImportError:
    fhirdate = sys.modules[__package__ + '.fhirdate']
try:
    from . import period
except ImportError:
    period = sys.modules[__package__ + '.period']
try:
    from . import usagecontext
except ImportError:
    usagecontext = sys.modules[__package__ + '.usagecontext']
