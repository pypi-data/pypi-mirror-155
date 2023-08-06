#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/DeviceDefinition) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class DeviceDefinition(domainresource.DomainResource):
    """ An instance of a medical-related component of a medical device.
    
    The characteristics, operational status and capabilities of a medical-
    related component of a medical device.
    """
    
    resource_type = "DeviceDefinition"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Instance identifier."""
    _attribute_docstrings['udiDeviceIdentifier'] = """Unique Device Identifier (UDI) Barcode string."""
    _attribute_docstrings['manufacturerString'] = """Name of device manufacturer."""
    _attribute_docstrings['manufacturerReference'] = """Name of device manufacturer."""
    _attribute_docstrings['deviceName'] = """A name given to the device to identify it."""
    _attribute_docstrings['modelNumber'] = """The model number for the device."""
    _attribute_docstrings['type'] = """What kind of device or device system this is."""
    _attribute_docstrings['specialization'] = """The capabilities supported on a  device, the standards to which the device conforms for a particular purpose, and used for the communication."""
    _attribute_docstrings['version'] = """Available versions."""
    _attribute_docstrings['safety'] = """Safety characteristics of the device."""
    _attribute_docstrings['shelfLifeStorage'] = """Shelf Life and storage information."""
    _attribute_docstrings['physicalCharacteristics'] = """Dimensions, color etc.."""
    _attribute_docstrings['languageCode'] = """Language code for the human-readable text strings produced by the device (all supported)."""
    _attribute_docstrings['capability'] = """Device capabilities."""
    _attribute_docstrings['property'] = """The actual configuration settings of a device as it actually operates, e.g., regulation status, time properties."""
    _attribute_docstrings['owner'] = """Organization responsible for device."""
    _attribute_docstrings['contact'] = """Details for human/organization for support."""
    _attribute_docstrings['url'] = """Network address to contact device."""
    _attribute_docstrings['onlineInformation'] = """Access to on-line information."""
    _attribute_docstrings['note'] = """Device notes and comments."""
    _attribute_docstrings['quantity'] = """The quantity of the device present in the packaging (e.g. the number of devices present in a pack, or the number of devices in the same package of the medicinal product)."""
    _attribute_docstrings['parentDevice'] = """The parent device it can be part of."""
    _attribute_docstrings['material'] = """A substance used to create the material(s) of which the device is made."""

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
        """ Instance identifier.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.udiDeviceIdentifier = None
        """ Unique Device Identifier (UDI) Barcode string.
        List of `DeviceDefinitionUdiDeviceIdentifier` items (represented as `dict` in JSON). """
        
        self.manufacturerString = None
        """ Name of device manufacturer.
        Type `str`. """
        
        self.manufacturerReference = None
        """ Name of device manufacturer.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.deviceName = None
        """ A name given to the device to identify it.
        List of `DeviceDefinitionDeviceName` items (represented as `dict` in JSON). """
        
        self.modelNumber = None
        """ The model number for the device.
        Type `str`. """
        
        self.type = None
        """ What kind of device or device system this is.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.specialization = None
        """ The capabilities supported on a  device, the standards to which the
        device conforms for a particular purpose, and used for the
        communication.
        List of `DeviceDefinitionSpecialization` items (represented as `dict` in JSON). """
        
        self.version = None
        """ Available versions.
        List of `str` items. """
        
        self.safety = None
        """ Safety characteristics of the device.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.shelfLifeStorage = None
        """ Shelf Life and storage information.
        List of `ProductShelfLife` items (represented as `dict` in JSON). """
        
        self.physicalCharacteristics = None
        """ Dimensions, color etc.
        Type `ProdCharacteristic` (represented as `dict` in JSON). """
        
        self.languageCode = None
        """ Language code for the human-readable text strings produced by the
        device (all supported).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.capability = None
        """ Device capabilities.
        List of `DeviceDefinitionCapability` items (represented as `dict` in JSON). """
        
        self.property = None
        """ The actual configuration settings of a device as it actually
        operates, e.g., regulation status, time properties.
        List of `DeviceDefinitionProperty` items (represented as `dict` in JSON). """
        
        self.owner = None
        """ Organization responsible for device.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.contact = None
        """ Details for human/organization for support.
        List of `ContactPoint` items (represented as `dict` in JSON). """
        
        self.url = None
        """ Network address to contact device.
        Type `str`. """
        
        self.onlineInformation = None
        """ Access to on-line information.
        Type `str`. """
        
        self.note = None
        """ Device notes and comments.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        self.quantity = None
        """ The quantity of the device present in the packaging (e.g. the
        number of devices present in a pack, or the number of devices in
        the same package of the medicinal product).
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.parentDevice = None
        """ The parent device it can be part of.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.material = None
        """ A substance used to create the material(s) of which the device is
        made.
        List of `DeviceDefinitionMaterial` items (represented as `dict` in JSON). """
        
        super(DeviceDefinition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DeviceDefinition, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("udiDeviceIdentifier", "udiDeviceIdentifier", DeviceDefinitionUdiDeviceIdentifier, True, None, False),
            ("manufacturerString", "manufacturerString", str, False, "manufacturer", False),
            ("manufacturerReference", "manufacturerReference", fhirreference.FHIRReference, False, "manufacturer", False),
            ("deviceName", "deviceName", DeviceDefinitionDeviceName, True, None, False),
            ("modelNumber", "modelNumber", str, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("specialization", "specialization", DeviceDefinitionSpecialization, True, None, False),
            ("version", "version", str, True, None, False),
            ("safety", "safety", codeableconcept.CodeableConcept, True, None, False),
            ("shelfLifeStorage", "shelfLifeStorage", productshelflife.ProductShelfLife, True, None, False),
            ("physicalCharacteristics", "physicalCharacteristics", prodcharacteristic.ProdCharacteristic, False, None, False),
            ("languageCode", "languageCode", codeableconcept.CodeableConcept, True, None, False),
            ("capability", "capability", DeviceDefinitionCapability, True, None, False),
            ("property", "property", DeviceDefinitionProperty, True, None, False),
            ("owner", "owner", fhirreference.FHIRReference, False, None, False),
            ("contact", "contact", contactpoint.ContactPoint, True, None, False),
            ("url", "url", str, False, None, False),
            ("onlineInformation", "onlineInformation", str, False, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("parentDevice", "parentDevice", fhirreference.FHIRReference, False, None, False),
            ("material", "material", DeviceDefinitionMaterial, True, None, False),
        ])
        return js


from . import backboneelement

class DeviceDefinitionCapability(backboneelement.BackboneElement):
    """ Device capabilities.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Type of capability."""
    _attribute_docstrings['description'] = """Description of capability."""

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
        """ Type of capability.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.description = None
        """ Description of capability.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        super(DeviceDefinitionCapability, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DeviceDefinitionCapability, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("description", "description", codeableconcept.CodeableConcept, True, None, False),
        ])
        return js


class DeviceDefinitionDeviceName(backboneelement.BackboneElement):
    """ A name given to the device to identify it.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['name'] = """The name of the device."""
    _attribute_docstrings['type'] = """The type of deviceName.
UDILabelName | UserFriendlyName | PatientReportedName | ManufactureDeviceName | ModelName."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://hl7.org/fhir/device-nametype',
        'restricted_to': ['udi-label-name', 'user-friendly-name', 'patient-reported-name', 'manufacturer-name', 'model-name', 'other'],
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
        """ The name of the device.
        Type `str`. """
        
        self.type = None
        """ The type of deviceName.
        UDILabelName | UserFriendlyName | PatientReportedName |
        ManufactureDeviceName | ModelName.
        Type `str`. """
        
        super(DeviceDefinitionDeviceName, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DeviceDefinitionDeviceName, self).elementProperties()
        js.extend([
            ("name", "name", str, False, None, True),
            ("type", "type", str, False, None, True),
        ])
        return js


class DeviceDefinitionMaterial(backboneelement.BackboneElement):
    """ A substance used to create the material(s) of which the device is made.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['substance'] = """The substance."""
    _attribute_docstrings['alternate'] = """Indicates an alternative material of the device."""
    _attribute_docstrings['allergenicIndicator'] = """Whether the substance is a known or suspected allergen."""

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
        
        self.substance = None
        """ The substance.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.alternate = None
        """ Indicates an alternative material of the device.
        Type `bool`. """
        
        self.allergenicIndicator = None
        """ Whether the substance is a known or suspected allergen.
        Type `bool`. """
        
        super(DeviceDefinitionMaterial, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DeviceDefinitionMaterial, self).elementProperties()
        js.extend([
            ("substance", "substance", codeableconcept.CodeableConcept, False, None, True),
            ("alternate", "alternate", bool, False, None, False),
            ("allergenicIndicator", "allergenicIndicator", bool, False, None, False),
        ])
        return js


class DeviceDefinitionProperty(backboneelement.BackboneElement):
    """ The actual configuration settings of a device as it actually operates,
    e.g., regulation status, time properties.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Code that specifies the property DeviceDefinitionPropetyCode (Extensible)."""
    _attribute_docstrings['valueQuantity'] = """Property value as a quantity."""
    _attribute_docstrings['valueCode'] = """Property value as a code, e.g., NTP4 (synced to NTP)."""

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
        """ Code that specifies the property DeviceDefinitionPropetyCode
        (Extensible).
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.valueQuantity = None
        """ Property value as a quantity.
        List of `Quantity` items (represented as `dict` in JSON). """
        
        self.valueCode = None
        """ Property value as a code, e.g., NTP4 (synced to NTP).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        super(DeviceDefinitionProperty, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DeviceDefinitionProperty, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("valueQuantity", "valueQuantity", quantity.Quantity, True, None, False),
            ("valueCode", "valueCode", codeableconcept.CodeableConcept, True, None, False),
        ])
        return js


class DeviceDefinitionSpecialization(backboneelement.BackboneElement):
    """ The capabilities supported on a  device, the standards to which the device
    conforms for a particular purpose, and used for the communication.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['systemType'] = """The standard that is used to operate and communicate."""
    _attribute_docstrings['version'] = """The version of the standard that is used to operate and communicate."""

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
        
        self.systemType = None
        """ The standard that is used to operate and communicate.
        Type `str`. """
        
        self.version = None
        """ The version of the standard that is used to operate and communicate.
        Type `str`. """
        
        super(DeviceDefinitionSpecialization, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DeviceDefinitionSpecialization, self).elementProperties()
        js.extend([
            ("systemType", "systemType", str, False, None, True),
            ("version", "version", str, False, None, False),
        ])
        return js


class DeviceDefinitionUdiDeviceIdentifier(backboneelement.BackboneElement):
    """ Unique Device Identifier (UDI) Barcode string.
    
    Unique device identifier (UDI) assigned to device label or package.  Note
    that the Device may include multiple udiCarriers as it either may include
    just the udiCarrier for the jurisdiction it is sold, or for multiple
    jurisdictions it could have been sold.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['deviceIdentifier'] = """The identifier that is to be associated with every Device that references this DeviceDefintiion for the issuer and jurisdication porvided in the DeviceDefinition.udiDeviceIdentifier."""
    _attribute_docstrings['issuer'] = """The organization that assigns the identifier algorithm."""
    _attribute_docstrings['jurisdiction'] = """The jurisdiction to which the deviceIdentifier applies."""

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
        
        self.deviceIdentifier = None
        """ The identifier that is to be associated with every Device that
        references this DeviceDefintiion for the issuer and jurisdication
        porvided in the DeviceDefinition.udiDeviceIdentifier.
        Type `str`. """
        
        self.issuer = None
        """ The organization that assigns the identifier algorithm.
        Type `str`. """
        
        self.jurisdiction = None
        """ The jurisdiction to which the deviceIdentifier applies.
        Type `str`. """
        
        super(DeviceDefinitionUdiDeviceIdentifier, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DeviceDefinitionUdiDeviceIdentifier, self).elementProperties()
        js.extend([
            ("deviceIdentifier", "deviceIdentifier", str, False, None, True),
            ("issuer", "issuer", str, False, None, True),
            ("jurisdiction", "jurisdiction", str, False, None, True),
        ])
        return js


import sys
try:
    from . import annotation
except ImportError:
    annotation = sys.modules[__package__ + '.annotation']
try:
    from . import codeableconcept
except ImportError:
    codeableconcept = sys.modules[__package__ + '.codeableconcept']
try:
    from . import contactpoint
except ImportError:
    contactpoint = sys.modules[__package__ + '.contactpoint']
try:
    from . import fhirreference
except ImportError:
    fhirreference = sys.modules[__package__ + '.fhirreference']
try:
    from . import identifier
except ImportError:
    identifier = sys.modules[__package__ + '.identifier']
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
