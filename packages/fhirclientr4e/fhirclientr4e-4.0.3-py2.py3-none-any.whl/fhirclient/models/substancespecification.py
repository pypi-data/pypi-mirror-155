#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/SubstanceSpecification) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class SubstanceSpecification(domainresource.DomainResource):
    """ The detailed description of a substance, typically at a level beyond what
    is used for prescribing.
    """
    
    resource_type = "SubstanceSpecification"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Identifier by which this substance is known."""
    _attribute_docstrings['type'] = """High level categorization, e.g. polymer or nucleic acid."""
    _attribute_docstrings['status'] = """Status of substance within the catalogue e.g. approved."""
    _attribute_docstrings['domain'] = """If the substance applies to only human or veterinary use."""
    _attribute_docstrings['description'] = """Textual description of the substance."""
    _attribute_docstrings['source'] = """Supporting literature."""
    _attribute_docstrings['comment'] = """Textual comment about this record of a substance."""
    _attribute_docstrings['moiety'] = """Moiety, for structural modifications."""
    _attribute_docstrings['property'] = """General specifications for this substance, including how it is related to other substances."""
    _attribute_docstrings['referenceInformation'] = """General information detailing this substance."""
    _attribute_docstrings['structure'] = """Structural information."""
    _attribute_docstrings['code'] = """Codes associated with the substance."""
    _attribute_docstrings['name'] = """Names applicable to this substance."""
    _attribute_docstrings['molecularWeight'] = """The molecular weight or weight range (for proteins, polymers or nucleic acids)."""
    _attribute_docstrings['relationship'] = """A link between this substance and another, with details of the relationship."""
    _attribute_docstrings['nucleicAcid'] = """Data items specific to nucleic acids."""
    _attribute_docstrings['polymer'] = """Data items specific to polymers."""
    _attribute_docstrings['protein'] = """Data items specific to proteins."""
    _attribute_docstrings['sourceMaterial'] = """Material or taxonomic/anatomical source for the substance."""

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
        
        self.identifier = None
        """ Identifier by which this substance is known.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.type = None
        """ High level categorization, e.g. polymer or nucleic acid.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.status = None
        """ Status of substance within the catalogue e.g. approved.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.domain = None
        """ If the substance applies to only human or veterinary use.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.description = None
        """ Textual description of the substance.
        Type `str`. """
        
        self.source = None
        """ Supporting literature.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.comment = None
        """ Textual comment about this record of a substance.
        Type `str`. """
        
        self.moiety = None
        """ Moiety, for structural modifications.
        List of `SubstanceSpecificationMoiety` items (represented as `dict` in JSON). """
        
        self.property = None
        """ General specifications for this substance, including how it is
        related to other substances.
        List of `SubstanceSpecificationProperty` items (represented as `dict` in JSON). """
        
        self.referenceInformation = None
        """ General information detailing this substance.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.structure = None
        """ Structural information.
        Type `SubstanceSpecificationStructure` (represented as `dict` in JSON). """
        
        self.code = None
        """ Codes associated with the substance.
        List of `SubstanceSpecificationstr` items (represented as `dict` in JSON). """
        
        self.name = None
        """ Names applicable to this substance.
        List of `SubstanceSpecificationName` items (represented as `dict` in JSON). """
        
        self.molecularWeight = None
        """ The molecular weight or weight range (for proteins, polymers or
        nucleic acids).
        List of `SubstanceSpecificationStructureIsotopeMolecularWeight` items (represented as `dict` in JSON). """
        
        self.relationship = None
        """ A link between this substance and another, with details of the
        relationship.
        List of `SubstanceSpecificationRelationship` items (represented as `dict` in JSON). """
        
        self.nucleicAcid = None
        """ Data items specific to nucleic acids.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.polymer = None
        """ Data items specific to polymers.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.protein = None
        """ Data items specific to proteins.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.sourceMaterial = None
        """ Material or taxonomic/anatomical source for the substance.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(SubstanceSpecification, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SubstanceSpecification, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("status", "status", codeableconcept.CodeableConcept, False, None, False),
            ("domain", "domain", codeableconcept.CodeableConcept, False, None, False),
            ("description", "description", str, False, None, False),
            ("source", "source", fhirreference.FHIRReference, True, None, False),
            ("comment", "comment", str, False, None, False),
            ("moiety", "moiety", SubstanceSpecificationMoiety, True, None, False),
            ("property", "property", SubstanceSpecificationProperty, True, None, False),
            ("referenceInformation", "referenceInformation", fhirreference.FHIRReference, False, None, False),
            ("structure", "structure", SubstanceSpecificationStructure, False, None, False),
            ("code", "code", SubstanceSpecificationstr, True, None, False),
            ("name", "name", SubstanceSpecificationName, True, None, False),
            ("molecularWeight", "molecularWeight", SubstanceSpecificationStructureIsotopeMolecularWeight, True, None, False),
            ("relationship", "relationship", SubstanceSpecificationRelationship, True, None, False),
            ("nucleicAcid", "nucleicAcid", fhirreference.FHIRReference, False, None, False),
            ("polymer", "polymer", fhirreference.FHIRReference, False, None, False),
            ("protein", "protein", fhirreference.FHIRReference, False, None, False),
            ("sourceMaterial", "sourceMaterial", fhirreference.FHIRReference, False, None, False),
        ])
        return js


from . import backboneelement

class SubstanceSpecificationMoiety(backboneelement.BackboneElement):
    """ Moiety, for structural modifications.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['role'] = """Role that the moiety is playing."""
    _attribute_docstrings['identifier'] = """Identifier by which this moiety substance is known."""
    _attribute_docstrings['name'] = """Textual name for this moiety substance."""
    _attribute_docstrings['stereochemistry'] = """Stereochemistry type."""
    _attribute_docstrings['opticalActivity'] = """Optical activity type."""
    _attribute_docstrings['molecularFormula'] = """Molecular formula."""
    _attribute_docstrings['amountQuantity'] = """Quantitative value for this moiety."""
    _attribute_docstrings['amountString'] = """Quantitative value for this moiety."""

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
        
        self.role = None
        """ Role that the moiety is playing.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.identifier = None
        """ Identifier by which this moiety substance is known.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.name = None
        """ Textual name for this moiety substance.
        Type `str`. """
        
        self.stereochemistry = None
        """ Stereochemistry type.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.opticalActivity = None
        """ Optical activity type.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.molecularFormula = None
        """ Molecular formula.
        Type `str`. """
        
        self.amountQuantity = None
        """ Quantitative value for this moiety.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.amountString = None
        """ Quantitative value for this moiety.
        Type `str`. """
        
        super(SubstanceSpecificationMoiety, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SubstanceSpecificationMoiety, self).elementProperties()
        js.extend([
            ("role", "role", codeableconcept.CodeableConcept, False, None, False),
            ("identifier", "identifier", identifier.Identifier, False, None, False),
            ("name", "name", str, False, None, False),
            ("stereochemistry", "stereochemistry", codeableconcept.CodeableConcept, False, None, False),
            ("opticalActivity", "opticalActivity", codeableconcept.CodeableConcept, False, None, False),
            ("molecularFormula", "molecularFormula", str, False, None, False),
            ("amountQuantity", "amountQuantity", quantity.Quantity, False, "amount", False),
            ("amountString", "amountString", str, False, "amount", False),
        ])
        return js


class SubstanceSpecificationName(backboneelement.BackboneElement):
    """ Names applicable to this substance.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['name'] = """The actual name."""
    _attribute_docstrings['type'] = """Name type."""
    _attribute_docstrings['status'] = """The status of the name."""
    _attribute_docstrings['preferred'] = """If this is the preferred name for this substance."""
    _attribute_docstrings['language'] = """Language of the name."""
    _attribute_docstrings['domain'] = """The use context of this name for example if there is a different name a drug active ingredient as opposed to a food colour additive."""
    _attribute_docstrings['jurisdiction'] = """The jurisdiction where this name applies."""
    _attribute_docstrings['synonym'] = """A synonym of this name."""
    _attribute_docstrings['translation'] = """A translation for this name."""
    _attribute_docstrings['official'] = """Details of the official nature of this name."""
    _attribute_docstrings['source'] = """Supporting literature."""

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
        
        self.name = None
        """ The actual name.
        Type `str`. """
        
        self.type = None
        """ Name type.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.status = None
        """ The status of the name.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.preferred = None
        """ If this is the preferred name for this substance.
        Type `bool`. """
        
        self.language = None
        """ Language of the name.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.domain = None
        """ The use context of this name for example if there is a different
        name a drug active ingredient as opposed to a food colour additive.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ The jurisdiction where this name applies.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.synonym = None
        """ A synonym of this name.
        List of `SubstanceSpecificationName` items (represented as `dict` in JSON). """
        
        self.translation = None
        """ A translation for this name.
        List of `SubstanceSpecificationName` items (represented as `dict` in JSON). """
        
        self.official = None
        """ Details of the official nature of this name.
        List of `SubstanceSpecificationNameOfficial` items (represented as `dict` in JSON). """
        
        self.source = None
        """ Supporting literature.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(SubstanceSpecificationName, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SubstanceSpecificationName, self).elementProperties()
        js.extend([
            ("name", "name", str, False, None, True),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("status", "status", codeableconcept.CodeableConcept, False, None, False),
            ("preferred", "preferred", bool, False, None, False),
            ("language", "language", codeableconcept.CodeableConcept, True, None, False),
            ("domain", "domain", codeableconcept.CodeableConcept, True, None, False),
            ("jurisdiction", "jurisdiction", codeableconcept.CodeableConcept, True, None, False),
            ("synonym", "synonym", SubstanceSpecificationName, True, None, False),
            ("translation", "translation", SubstanceSpecificationName, True, None, False),
            ("official", "official", SubstanceSpecificationNameOfficial, True, None, False),
            ("source", "source", fhirreference.FHIRReference, True, None, False),
        ])
        return js


class SubstanceSpecificationNameOfficial(backboneelement.BackboneElement):
    """ Details of the official nature of this name.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['authority'] = """Which authority uses this official name."""
    _attribute_docstrings['status'] = """The status of the official name."""
    _attribute_docstrings['date'] = """Date of official name change."""

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
        
        self.authority = None
        """ Which authority uses this official name.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.status = None
        """ The status of the official name.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.date = None
        """ Date of official name change.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        super(SubstanceSpecificationNameOfficial, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SubstanceSpecificationNameOfficial, self).elementProperties()
        js.extend([
            ("authority", "authority", codeableconcept.CodeableConcept, False, None, False),
            ("status", "status", codeableconcept.CodeableConcept, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
        ])
        return js


class SubstanceSpecificationProperty(backboneelement.BackboneElement):
    """ General specifications for this substance, including how it is related to
    other substances.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['category'] = """A category for this property, e.g. Physical, Chemical, Enzymatic."""
    _attribute_docstrings['code'] = """Property type e.g. viscosity, pH, isoelectric point."""
    _attribute_docstrings['parameters'] = """Parameters that were used in the measurement of a property (e.g. for viscosity: measured at 20C with a pH of 7.1)."""
    _attribute_docstrings['definingSubstanceReference'] = """A substance upon which a defining property depends (e.g. for solubility: in water, in alcohol)."""
    _attribute_docstrings['definingSubstanceCodeableConcept'] = """A substance upon which a defining property depends (e.g. for solubility: in water, in alcohol)."""
    _attribute_docstrings['amountQuantity'] = """Quantitative value for this property."""
    _attribute_docstrings['amountString'] = """Quantitative value for this property."""

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
        
        self.category = None
        """ A category for this property, e.g. Physical, Chemical, Enzymatic.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.code = None
        """ Property type e.g. viscosity, pH, isoelectric point.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.parameters = None
        """ Parameters that were used in the measurement of a property (e.g.
        for viscosity: measured at 20C with a pH of 7.1).
        Type `str`. """
        
        self.definingSubstanceReference = None
        """ A substance upon which a defining property depends (e.g. for
        solubility: in water, in alcohol).
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.definingSubstanceCodeableConcept = None
        """ A substance upon which a defining property depends (e.g. for
        solubility: in water, in alcohol).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.amountQuantity = None
        """ Quantitative value for this property.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.amountString = None
        """ Quantitative value for this property.
        Type `str`. """
        
        super(SubstanceSpecificationProperty, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SubstanceSpecificationProperty, self).elementProperties()
        js.extend([
            ("category", "category", codeableconcept.CodeableConcept, False, None, False),
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("parameters", "parameters", str, False, None, False),
            ("definingSubstanceReference", "definingSubstanceReference", fhirreference.FHIRReference, False, "definingSubstance", False),
            ("definingSubstanceCodeableConcept", "definingSubstanceCodeableConcept", codeableconcept.CodeableConcept, False, "definingSubstance", False),
            ("amountQuantity", "amountQuantity", quantity.Quantity, False, "amount", False),
            ("amountString", "amountString", str, False, "amount", False),
        ])
        return js


class SubstanceSpecificationRelationship(backboneelement.BackboneElement):
    """ A link between this substance and another, with details of the relationship.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['substanceReference'] = """A pointer to another substance, as a resource or just a representational code."""
    _attribute_docstrings['substanceCodeableConcept'] = """A pointer to another substance, as a resource or just a representational code."""
    _attribute_docstrings['relationship'] = """For example "salt to parent", "active moiety", "starting material"."""
    _attribute_docstrings['isDefining'] = """For example where an enzyme strongly bonds with a particular substance, this is a defining relationship for that enzyme, out of several possible substance relationships."""
    _attribute_docstrings['amountQuantity'] = """A numeric factor for the relationship, for instance to express that the salt of a substance has some percentage of the active substance in relation to some other."""
    _attribute_docstrings['amountRange'] = """A numeric factor for the relationship, for instance to express that the salt of a substance has some percentage of the active substance in relation to some other."""
    _attribute_docstrings['amountRatio'] = """A numeric factor for the relationship, for instance to express that the salt of a substance has some percentage of the active substance in relation to some other."""
    _attribute_docstrings['amountString'] = """A numeric factor for the relationship, for instance to express that the salt of a substance has some percentage of the active substance in relation to some other."""
    _attribute_docstrings['amountRatioLowLimit'] = """For use when the numeric."""
    _attribute_docstrings['amountType'] = """An operator for the amount, for example "average", "approximately", "less than"."""
    _attribute_docstrings['source'] = """Supporting literature."""

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
        
        self.substanceReference = None
        """ A pointer to another substance, as a resource or just a
        representational code.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.substanceCodeableConcept = None
        """ A pointer to another substance, as a resource or just a
        representational code.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.relationship = None
        """ For example "salt to parent", "active moiety", "starting material".
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.isDefining = None
        """ For example where an enzyme strongly bonds with a particular
        substance, this is a defining relationship for that enzyme, out of
        several possible substance relationships.
        Type `bool`. """
        
        self.amountQuantity = None
        """ A numeric factor for the relationship, for instance to express that
        the salt of a substance has some percentage of the active substance
        in relation to some other.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.amountRange = None
        """ A numeric factor for the relationship, for instance to express that
        the salt of a substance has some percentage of the active substance
        in relation to some other.
        Type `Range` (represented as `dict` in JSON). """
        
        self.amountRatio = None
        """ A numeric factor for the relationship, for instance to express that
        the salt of a substance has some percentage of the active substance
        in relation to some other.
        Type `Ratio` (represented as `dict` in JSON). """
        
        self.amountString = None
        """ A numeric factor for the relationship, for instance to express that
        the salt of a substance has some percentage of the active substance
        in relation to some other.
        Type `str`. """
        
        self.amountRatioLowLimit = None
        """ For use when the numeric.
        Type `Ratio` (represented as `dict` in JSON). """
        
        self.amountType = None
        """ An operator for the amount, for example "average", "approximately",
        "less than".
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.source = None
        """ Supporting literature.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(SubstanceSpecificationRelationship, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SubstanceSpecificationRelationship, self).elementProperties()
        js.extend([
            ("substanceReference", "substanceReference", fhirreference.FHIRReference, False, "substance", False),
            ("substanceCodeableConcept", "substanceCodeableConcept", codeableconcept.CodeableConcept, False, "substance", False),
            ("relationship", "relationship", codeableconcept.CodeableConcept, False, None, False),
            ("isDefining", "isDefining", bool, False, None, False),
            ("amountQuantity", "amountQuantity", quantity.Quantity, False, "amount", False),
            ("amountRange", "amountRange", range.Range, False, "amount", False),
            ("amountRatio", "amountRatio", ratio.Ratio, False, "amount", False),
            ("amountString", "amountString", str, False, "amount", False),
            ("amountRatioLowLimit", "amountRatioLowLimit", ratio.Ratio, False, None, False),
            ("amountType", "amountType", codeableconcept.CodeableConcept, False, None, False),
            ("source", "source", fhirreference.FHIRReference, True, None, False),
        ])
        return js


class SubstanceSpecificationStructure(backboneelement.BackboneElement):
    """ Structural information.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['stereochemistry'] = """Stereochemistry type."""
    _attribute_docstrings['opticalActivity'] = """Optical activity type."""
    _attribute_docstrings['molecularFormula'] = """Molecular formula."""
    _attribute_docstrings['molecularFormulaByMoiety'] = """Specified per moiety according to the Hill system, i.e. first C, then H, then alphabetical, each moiety separated by a dot."""
    _attribute_docstrings['isotope'] = """Applicable for single substances that contain a radionuclide or a non-natural isotopic ratio."""
    _attribute_docstrings['molecularWeight'] = """The molecular weight or weight range (for proteins, polymers or nucleic acids)."""
    _attribute_docstrings['source'] = """Supporting literature."""
    _attribute_docstrings['representation'] = """Molecular structural representation."""

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
        
        self.stereochemistry = None
        """ Stereochemistry type.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.opticalActivity = None
        """ Optical activity type.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.molecularFormula = None
        """ Molecular formula.
        Type `str`. """
        
        self.molecularFormulaByMoiety = None
        """ Specified per moiety according to the Hill system, i.e. first C,
        then H, then alphabetical, each moiety separated by a dot.
        Type `str`. """
        
        self.isotope = None
        """ Applicable for single substances that contain a radionuclide or a
        non-natural isotopic ratio.
        List of `SubstanceSpecificationStructureIsotope` items (represented as `dict` in JSON). """
        
        self.molecularWeight = None
        """ The molecular weight or weight range (for proteins, polymers or
        nucleic acids).
        Type `SubstanceSpecificationStructureIsotopeMolecularWeight` (represented as `dict` in JSON). """
        
        self.source = None
        """ Supporting literature.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.representation = None
        """ Molecular structural representation.
        List of `SubstanceSpecificationStructureRepresentation` items (represented as `dict` in JSON). """
        
        super(SubstanceSpecificationStructure, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SubstanceSpecificationStructure, self).elementProperties()
        js.extend([
            ("stereochemistry", "stereochemistry", codeableconcept.CodeableConcept, False, None, False),
            ("opticalActivity", "opticalActivity", codeableconcept.CodeableConcept, False, None, False),
            ("molecularFormula", "molecularFormula", str, False, None, False),
            ("molecularFormulaByMoiety", "molecularFormulaByMoiety", str, False, None, False),
            ("isotope", "isotope", SubstanceSpecificationStructureIsotope, True, None, False),
            ("molecularWeight", "molecularWeight", SubstanceSpecificationStructureIsotopeMolecularWeight, False, None, False),
            ("source", "source", fhirreference.FHIRReference, True, None, False),
            ("representation", "representation", SubstanceSpecificationStructureRepresentation, True, None, False),
        ])
        return js


class SubstanceSpecificationStructureIsotope(backboneelement.BackboneElement):
    """ Applicable for single substances that contain a radionuclide or a non-
    natural isotopic ratio.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Substance identifier for each non-natural or radioisotope."""
    _attribute_docstrings['name'] = """Substance name for each non-natural or radioisotope."""
    _attribute_docstrings['substitution'] = """The type of isotopic substitution present in a single substance."""
    _attribute_docstrings['halfLife'] = """Half life - for a non-natural nuclide."""
    _attribute_docstrings['molecularWeight'] = """The molecular weight or weight range (for proteins, polymers or nucleic acids)."""

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
        
        self.identifier = None
        """ Substance identifier for each non-natural or radioisotope.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.name = None
        """ Substance name for each non-natural or radioisotope.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.substitution = None
        """ The type of isotopic substitution present in a single substance.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.halfLife = None
        """ Half life - for a non-natural nuclide.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.molecularWeight = None
        """ The molecular weight or weight range (for proteins, polymers or
        nucleic acids).
        Type `SubstanceSpecificationStructureIsotopeMolecularWeight` (represented as `dict` in JSON). """
        
        super(SubstanceSpecificationStructureIsotope, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SubstanceSpecificationStructureIsotope, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, False, None, False),
            ("name", "name", codeableconcept.CodeableConcept, False, None, False),
            ("substitution", "substitution", codeableconcept.CodeableConcept, False, None, False),
            ("halfLife", "halfLife", quantity.Quantity, False, None, False),
            ("molecularWeight", "molecularWeight", SubstanceSpecificationStructureIsotopeMolecularWeight, False, None, False),
        ])
        return js


class SubstanceSpecificationStructureIsotopeMolecularWeight(backboneelement.BackboneElement):
    """ The molecular weight or weight range (for proteins, polymers or nucleic
    acids).
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['method'] = """The method by which the molecular weight was determined."""
    _attribute_docstrings['type'] = """Type of molecular weight such as exact, average (also known as. number average), weight average."""
    _attribute_docstrings['amount'] = """Used to capture quantitative values for a variety of elements. If only limits are given, the arithmetic mean would be the average. If only a single definite value for a given element is given, it would be captured in this field."""

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
        
        self.method = None
        """ The method by which the molecular weight was determined.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.type = None
        """ Type of molecular weight such as exact, average (also known as.
        number average), weight average.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.amount = None
        """ Used to capture quantitative values for a variety of elements. If
        only limits are given, the arithmetic mean would be the average. If
        only a single definite value for a given element is given, it would
        be captured in this field.
        Type `Quantity` (represented as `dict` in JSON). """
        
        super(SubstanceSpecificationStructureIsotopeMolecularWeight, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SubstanceSpecificationStructureIsotopeMolecularWeight, self).elementProperties()
        js.extend([
            ("method", "method", codeableconcept.CodeableConcept, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("amount", "amount", quantity.Quantity, False, None, False),
        ])
        return js


class SubstanceSpecificationStructureRepresentation(backboneelement.BackboneElement):
    """ Molecular structural representation.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """The type of structure (e.g. Full, Partial, Representative)."""
    _attribute_docstrings['representation'] = """The structural representation as text string in a format e.g. InChI, SMILES, MOLFILE, CDX."""
    _attribute_docstrings['attachment'] = """An attached file with the structural representation."""

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
        """ The type of structure (e.g. Full, Partial, Representative).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.representation = None
        """ The structural representation as text string in a format e.g.
        InChI, SMILES, MOLFILE, CDX.
        Type `str`. """
        
        self.attachment = None
        """ An attached file with the structural representation.
        Type `Attachment` (represented as `dict` in JSON). """
        
        super(SubstanceSpecificationStructureRepresentation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SubstanceSpecificationStructureRepresentation, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("representation", "representation", str, False, None, False),
            ("attachment", "attachment", attachment.Attachment, False, None, False),
        ])
        return js


class SubstanceSpecificationstr(backboneelement.BackboneElement):
    """ Codes associated with the substance.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """The specific code."""
    _attribute_docstrings['status'] = """Status of the code assignment."""
    _attribute_docstrings['statusDate'] = """The date at which the code status is changed as part of the terminology maintenance."""
    _attribute_docstrings['comment'] = """Any comment can be provided in this field, if necessary."""
    _attribute_docstrings['source'] = """Supporting literature."""

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
        
        self.code = None
        """ The specific code.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.status = None
        """ Status of the code assignment.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.statusDate = None
        """ The date at which the code status is changed as part of the
        terminology maintenance.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.comment = None
        """ Any comment can be provided in this field, if necessary.
        Type `str`. """
        
        self.source = None
        """ Supporting literature.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(SubstanceSpecificationstr, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(SubstanceSpecificationstr, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("status", "status", codeableconcept.CodeableConcept, False, None, False),
            ("statusDate", "statusDate", fhirdate.FHIRDate, False, None, False),
            ("comment", "comment", str, False, None, False),
            ("source", "source", fhirreference.FHIRReference, True, None, False),
        ])
        return js


import sys
try:
    from . import attachment
except ImportError:
    attachment = sys.modules[__package__ + '.attachment']
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
try:
    from . import quantity
except ImportError:
    quantity = sys.modules[__package__ + '.quantity']
try:
    from . import range
except ImportError:
    range = sys.modules[__package__ + '.range']
try:
    from . import ratio
except ImportError:
    ratio = sys.modules[__package__ + '.ratio']
