#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/MedicinalProductPackaged) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class MedicinalProductPackaged(domainresource.DomainResource):
    """ A medicinal product in a container or package.
    """
    
    resource_type = "MedicinalProductPackaged"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Unique identifier."""
    _attribute_docstrings['subject'] = """The product with this is a pack for."""
    _attribute_docstrings['description'] = """Textual description."""
    _attribute_docstrings['legalStatusOfSupply'] = """The legal status of supply of the medicinal product as classified by the regulator."""
    _attribute_docstrings['marketingStatus'] = """Marketing information."""
    _attribute_docstrings['marketingAuthorization'] = """Manufacturer of this Package Item."""
    _attribute_docstrings['manufacturer'] = """Manufacturer of this Package Item."""
    _attribute_docstrings['batchIdentifier'] = """Batch numbering."""
    _attribute_docstrings['packageItem'] = """A packaging item, as a contained for medicine, possibly with other packaging items within."""

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
        """ Unique identifier.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.subject = None
        """ The product with this is a pack for.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.description = None
        """ Textual description.
        Type `str`. """
        
        self.legalStatusOfSupply = None
        """ The legal status of supply of the medicinal product as classified
        by the regulator.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.marketingStatus = None
        """ Marketing information.
        List of `MarketingStatus` items (represented as `dict` in JSON). """
        
        self.marketingAuthorization = None
        """ Manufacturer of this Package Item.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.manufacturer = None
        """ Manufacturer of this Package Item.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.batchIdentifier = None
        """ Batch numbering.
        List of `MedicinalProductPackagedBatchIdentifier` items (represented as `dict` in JSON). """
        
        self.packageItem = None
        """ A packaging item, as a contained for medicine, possibly with other
        packaging items within.
        List of `MedicinalProductPackagedPackageItem` items (represented as `dict` in JSON). """
        
        super(MedicinalProductPackaged, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicinalProductPackaged, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("subject", "subject", fhirreference.FHIRReference, True, None, False),
            ("description", "description", str, False, None, False),
            ("legalStatusOfSupply", "legalStatusOfSupply", codeableconcept.CodeableConcept, False, None, False),
            ("marketingStatus", "marketingStatus", marketingstatus.MarketingStatus, True, None, False),
            ("marketingAuthorization", "marketingAuthorization", fhirreference.FHIRReference, False, None, False),
            ("manufacturer", "manufacturer", fhirreference.FHIRReference, True, None, False),
            ("batchIdentifier", "batchIdentifier", MedicinalProductPackagedBatchIdentifier, True, None, False),
            ("packageItem", "packageItem", MedicinalProductPackagedPackageItem, True, None, True),
        ])
        return js


from . import backboneelement

class MedicinalProductPackagedBatchIdentifier(backboneelement.BackboneElement):
    """ Batch numbering.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['outerPackaging'] = """A number appearing on the outer packaging of a specific batch."""
    _attribute_docstrings['immediatePackaging'] = """A number appearing on the immediate packaging (and not the outer packaging)."""

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
        
        self.outerPackaging = None
        """ A number appearing on the outer packaging of a specific batch.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.immediatePackaging = None
        """ A number appearing on the immediate packaging (and not the outer
        packaging).
        Type `Identifier` (represented as `dict` in JSON). """
        
        super(MedicinalProductPackagedBatchIdentifier, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicinalProductPackagedBatchIdentifier, self).elementProperties()
        js.extend([
            ("outerPackaging", "outerPackaging", identifier.Identifier, False, None, True),
            ("immediatePackaging", "immediatePackaging", identifier.Identifier, False, None, False),
        ])
        return js


class MedicinalProductPackagedPackageItem(backboneelement.BackboneElement):
    """ A packaging item, as a contained for medicine, possibly with other
    packaging items within.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Including possibly Data Carrier Identifier."""
    _attribute_docstrings['type'] = """The physical type of the container of the medicine."""
    _attribute_docstrings['quantity'] = """The quantity of this package in the medicinal product, at the current level of packaging. The outermost is always 1."""
    _attribute_docstrings['material'] = """Material type of the package item."""
    _attribute_docstrings['alternateMaterial'] = """A possible alternate material for the packaging."""
    _attribute_docstrings['device'] = """A device accompanying a medicinal product."""
    _attribute_docstrings['manufacturedItem'] = """The manufactured item as contained in the packaged medicinal product."""
    _attribute_docstrings['packageItem'] = """Allows containers within containers."""
    _attribute_docstrings['physicalCharacteristics'] = """Dimensions, color etc.."""
    _attribute_docstrings['otherCharacteristics'] = """Other codeable characteristics."""
    _attribute_docstrings['shelfLifeStorage'] = """Shelf Life and storage information."""
    _attribute_docstrings['manufacturer'] = """Manufacturer of this Package Item."""

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
        """ Including possibly Data Carrier Identifier.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.type = None
        """ The physical type of the container of the medicine.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.quantity = None
        """ The quantity of this package in the medicinal product, at the
        current level of packaging. The outermost is always 1.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.material = None
        """ Material type of the package item.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.alternateMaterial = None
        """ A possible alternate material for the packaging.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.device = None
        """ A device accompanying a medicinal product.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.manufacturedItem = None
        """ The manufactured item as contained in the packaged medicinal
        product.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.packageItem = None
        """ Allows containers within containers.
        List of `MedicinalProductPackagedPackageItem` items (represented as `dict` in JSON). """
        
        self.physicalCharacteristics = None
        """ Dimensions, color etc.
        Type `ProdCharacteristic` (represented as `dict` in JSON). """
        
        self.otherCharacteristics = None
        """ Other codeable characteristics.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.shelfLifeStorage = None
        """ Shelf Life and storage information.
        List of `ProductShelfLife` items (represented as `dict` in JSON). """
        
        self.manufacturer = None
        """ Manufacturer of this Package Item.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(MedicinalProductPackagedPackageItem, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MedicinalProductPackagedPackageItem, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("quantity", "quantity", quantity.Quantity, False, None, True),
            ("material", "material", codeableconcept.CodeableConcept, True, None, False),
            ("alternateMaterial", "alternateMaterial", codeableconcept.CodeableConcept, True, None, False),
            ("device", "device", fhirreference.FHIRReference, True, None, False),
            ("manufacturedItem", "manufacturedItem", fhirreference.FHIRReference, True, None, False),
            ("packageItem", "packageItem", MedicinalProductPackagedPackageItem, True, None, False),
            ("physicalCharacteristics", "physicalCharacteristics", prodcharacteristic.ProdCharacteristic, False, None, False),
            ("otherCharacteristics", "otherCharacteristics", codeableconcept.CodeableConcept, True, None, False),
            ("shelfLifeStorage", "shelfLifeStorage", productshelflife.ProductShelfLife, True, None, False),
            ("manufacturer", "manufacturer", fhirreference.FHIRReference, True, None, False),
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
    from . import marketingstatus
except ImportError:
    marketingstatus = sys.modules[__package__ + '.marketingstatus']
try:
    from . import prodcharacteristic
except ImportError:
    prodcharacteristic = sys.modules[__package__ + '.prodcharacteristic']
try:
    from . import productshelflife
except ImportError:
    productshelflife = sys.modules[__package__ + '.productshelflife']
try:
    from . import quantity
except ImportError:
    quantity = sys.modules[__package__ + '.quantity']
