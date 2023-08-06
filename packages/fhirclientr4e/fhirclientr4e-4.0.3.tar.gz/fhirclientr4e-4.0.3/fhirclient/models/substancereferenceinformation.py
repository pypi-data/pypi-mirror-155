#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/SubstanceReferenceInformation) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class SubstanceReferenceInformation(domainresource.DomainResource):
    """ Todo.
    """
    
    resource_type = "SubstanceReferenceInformation"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['comment'] = """Todo."""
    _attribute_docstrings['gene'] = """Todo."""
    _attribute_docstrings['geneElement'] = """Todo."""
    _attribute_docstrings['classification'] = """Todo."""
    _attribute_docstrings['target'] = """Todo."""

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
        
        self.comment = None
        """ Todo.
        Type `str`. """
        
        self.gene = None
        """ Todo.
        List of `SubstanceReferenceInformationGene` items (represented as `dict` in JSON). """
        
        self.geneElement = None
        """ Todo.
        List of `SubstanceReferenceInformationGeneElement` items (represented as `dict` in JSON). """
        
        self.classification = None
        """ Todo.
        List of `SubstanceReferenceInformationClassification` items (represented as `dict` in JSON). """
        
        self.target = None
        """ Todo.
        List of `SubstanceReferenceInformationTarget` items (represented as `dict` in JSON). """
        
        super(SubstanceReferenceInformation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SubstanceReferenceInformation, self).elementProperties()
        js.extend([
            ("comment", "comment", str, False, None, False),
            ("gene", "gene", SubstanceReferenceInformationGene, True, None, False),
            ("geneElement", "geneElement", SubstanceReferenceInformationGeneElement, True, None, False),
            ("classification", "classification", SubstanceReferenceInformationClassification, True, None, False),
            ("target", "target", SubstanceReferenceInformationTarget, True, None, False),
        ])
        return js


from . import backboneelement

class SubstanceReferenceInformationClassification(backboneelement.BackboneElement):
    """ Todo.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['domain'] = """Todo."""
    _attribute_docstrings['classification'] = """Todo."""
    _attribute_docstrings['subtype'] = """Todo."""
    _attribute_docstrings['source'] = """Todo."""

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
        
        self.domain = None
        """ Todo.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.classification = None
        """ Todo.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subtype = None
        """ Todo.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.source = None
        """ Todo.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(SubstanceReferenceInformationClassification, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SubstanceReferenceInformationClassification, self).elementProperties()
        js.extend([
            ("domain", "domain", codeableconcept.CodeableConcept, False, None, False),
            ("classification", "classification", codeableconcept.CodeableConcept, False, None, False),
            ("subtype", "subtype", codeableconcept.CodeableConcept, True, None, False),
            ("source", "source", fhirreference.FHIRReference, True, None, False),
        ])
        return js


class SubstanceReferenceInformationGene(backboneelement.BackboneElement):
    """ Todo.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['geneSequenceOrigin'] = """Todo."""
    _attribute_docstrings['gene'] = """Todo."""
    _attribute_docstrings['source'] = """Todo."""

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
        
        self.geneSequenceOrigin = None
        """ Todo.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.gene = None
        """ Todo.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.source = None
        """ Todo.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(SubstanceReferenceInformationGene, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SubstanceReferenceInformationGene, self).elementProperties()
        js.extend([
            ("geneSequenceOrigin", "geneSequenceOrigin", codeableconcept.CodeableConcept, False, None, False),
            ("gene", "gene", codeableconcept.CodeableConcept, False, None, False),
            ("source", "source", fhirreference.FHIRReference, True, None, False),
        ])
        return js


class SubstanceReferenceInformationGeneElement(backboneelement.BackboneElement):
    """ Todo.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Todo."""
    _attribute_docstrings['element'] = """Todo."""
    _attribute_docstrings['source'] = """Todo."""

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
        
        self.type = None
        """ Todo.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.element = None
        """ Todo.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.source = None
        """ Todo.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(SubstanceReferenceInformationGeneElement, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SubstanceReferenceInformationGeneElement, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("element", "element", identifier.Identifier, False, None, False),
            ("source", "source", fhirreference.FHIRReference, True, None, False),
        ])
        return js


class SubstanceReferenceInformationTarget(backboneelement.BackboneElement):
    """ Todo.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['target'] = """Todo."""
    _attribute_docstrings['type'] = """Todo."""
    _attribute_docstrings['interaction'] = """Todo."""
    _attribute_docstrings['organism'] = """Todo."""
    _attribute_docstrings['organismType'] = """Todo."""
    _attribute_docstrings['amountQuantity'] = """Todo."""
    _attribute_docstrings['amountRange'] = """Todo."""
    _attribute_docstrings['amountString'] = """Todo."""
    _attribute_docstrings['amountType'] = """Todo."""
    _attribute_docstrings['source'] = """Todo."""

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
        
        self.target = None
        """ Todo.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.type = None
        """ Todo.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.interaction = None
        """ Todo.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.organism = None
        """ Todo.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.organismType = None
        """ Todo.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.amountQuantity = None
        """ Todo.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.amountRange = None
        """ Todo.
        Type `Range` (represented as `dict` in JSON). """
        
        self.amountString = None
        """ Todo.
        Type `str`. """
        
        self.amountType = None
        """ Todo.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.source = None
        """ Todo.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(SubstanceReferenceInformationTarget, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SubstanceReferenceInformationTarget, self).elementProperties()
        js.extend([
            ("target", "target", identifier.Identifier, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("interaction", "interaction", codeableconcept.CodeableConcept, False, None, False),
            ("organism", "organism", codeableconcept.CodeableConcept, False, None, False),
            ("organismType", "organismType", codeableconcept.CodeableConcept, False, None, False),
            ("amountQuantity", "amountQuantity", quantity.Quantity, False, "amount", False),
            ("amountRange", "amountRange", range.Range, False, "amount", False),
            ("amountString", "amountString", str, False, "amount", False),
            ("amountType", "amountType", codeableconcept.CodeableConcept, False, None, False),
            ("source", "source", fhirreference.FHIRReference, True, None, False),
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
    from . import quantity
except ImportError:
    quantity = sys.modules[__package__ + '.quantity']
try:
    from . import range
except ImportError:
    range = sys.modules[__package__ + '.range']
