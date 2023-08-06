#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Contract) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Contract(domainresource.DomainResource):
    """ Legal Agreement.
    
    Legally enforceable, formally recorded unilateral or bilateral directive
    i.e., a policy or agreement.
    """
    
    resource_type = "Contract"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Contract number."""
    _attribute_docstrings['url'] = """Basal definition."""
    _attribute_docstrings['version'] = """Business edition."""
    _attribute_docstrings['status'] = """The status of the resource instance."""
    _attribute_docstrings['legalState'] = """Legal states of the formation of a legal instrument, which is a formally executed written document that can be formally attributed to its author, records and formally expresses a legally enforceable act, process, or contractual duty, obligation, or right, and therefore evidences that act, process, or agreement."""
    _attribute_docstrings['instantiatesCanonical'] = """Source Contract Definition."""
    _attribute_docstrings['instantiatesUri'] = """External Contract Definition."""
    _attribute_docstrings['contentDerivative'] = """The minimal content derived from the basal information source at a specific stage in its lifecycle."""
    _attribute_docstrings['issued'] = """When this Contract was issued."""
    _attribute_docstrings['applies'] = """Effective time."""
    _attribute_docstrings['expirationType'] = """Event resulting in discontinuation or termination of this Contract instance by one or more parties to the contract."""
    _attribute_docstrings['subject'] = """Contract Target Entity."""
    _attribute_docstrings['authority'] = """Authority under which this Contract has standing."""
    _attribute_docstrings['domain'] = """A sphere of control governed by an authoritative jurisdiction, organization, or person."""
    _attribute_docstrings['site'] = """Specific Location."""
    _attribute_docstrings['name'] = """Computer friendly designation."""
    _attribute_docstrings['title'] = """Human Friendly name."""
    _attribute_docstrings['subtitle'] = """Subordinate Friendly name."""
    _attribute_docstrings['alias'] = """Acronym or short name."""
    _attribute_docstrings['author'] = """Source of Contract."""
    _attribute_docstrings['scope'] = """A selector of legal concerns for this Contract definition, derivative, or instance in any legal state."""
    _attribute_docstrings['topicCodeableConcept'] = """Focus of contract interest."""
    _attribute_docstrings['topicReference'] = """Focus of contract interest."""
    _attribute_docstrings['type'] = """A high-level category for the legal instrument, whether constructed as a Contract definition, derivative, or instance in any legal state.  Provides additional information about its content within the context of the Contract's scope to distinguish the kinds of systems that would be interested in the contract."""
    _attribute_docstrings['subType'] = """Sub-category for the Contract that distinguishes the kinds of systems that would be interested in the Contract within the context of the Contract's scope."""
    _attribute_docstrings['contentDefinition'] = """Contract precursor content."""
    _attribute_docstrings['term'] = """Contract Term List."""
    _attribute_docstrings['supportingInfo'] = """Extra Information."""
    _attribute_docstrings['relevantHistory'] = """Key event in Contract History."""
    _attribute_docstrings['signer'] = """Contract Signatory."""
    _attribute_docstrings['friendly'] = """Contract Friendly Language."""
    _attribute_docstrings['legal'] = """Contract Legal Language."""
    _attribute_docstrings['rule'] = """Computable Contract Language."""
    _attribute_docstrings['legallyBindingAttachment'] = """Binding Contract."""
    _attribute_docstrings['legallyBindingReference'] = """Binding Contract."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/contract-status',
        'restricted_to': ['amended', 'appended', 'cancelled', 'disputed', 'entered-in-error', 'executable', 'executed', 'negotiable', 'offered', 'policy', 'rejected', 'renewed', 'revoked', 'resolved', 'terminated'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['legalState'] = {
        'url': 'http://hl7.org/fhir/contract-legalstate',
        'restricted_to': ['amended', 'appended', 'cancelled', 'disputed', 'entered-in-error', 'executable', 'executed', 'negotiable', 'offered', 'policy', 'rejected', 'renewed', 'revoked', 'resolved', 'terminated'],
        'binding_strength': 'extensible',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['contentDerivative'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/contract-content-derivative',
        'restricted_to': ['registration', 'retrieval', 'statement', 'shareable'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['expirationType'] = {
        'url': 'http://hl7.org/fhir/contract-expiration-type',
        'restricted_to': ['breach'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['scope'] = {
        'url': 'http://hl7.org/fhir/contract-scope',
        'restricted_to': ['policy'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/contract-type',
        'restricted_to': ['privacy', 'disclosure', 'healthinsurance', 'supply', 'consent'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['subType'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/contractsubtypecodes',
        'restricted_to': ['disclosure-ca', 'disclosure-us'],
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
        """ Contract number.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.url = None
        """ Basal definition.
        Type `str`. """
        
        self.version = None
        """ Business edition.
        Type `str`. """
        
        self.status = None
        """ The status of the resource instance.
        Type `str`. """
        
        self.legalState = None
        """ Legal states of the formation of a legal instrument, which is a
        formally executed written document that can be formally attributed
        to its author, records and formally expresses a legally enforceable
        act, process, or contractual duty, obligation, or right, and
        therefore evidences that act, process, or agreement.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.instantiatesCanonical = None
        """ Source Contract Definition.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.instantiatesUri = None
        """ External Contract Definition.
        Type `str`. """
        
        self.contentDerivative = None
        """ The minimal content derived from the basal information source at a
        specific stage in its lifecycle.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.issued = None
        """ When this Contract was issued.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.applies = None
        """ Effective time.
        Type `Period` (represented as `dict` in JSON). """
        
        self.expirationType = None
        """ Event resulting in discontinuation or termination of this Contract
        instance by one or more parties to the contract.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subject = None
        """ Contract Target Entity.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.authority = None
        """ Authority under which this Contract has standing.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.domain = None
        """ A sphere of control governed by an authoritative jurisdiction,
        organization, or person.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.site = None
        """ Specific Location.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.name = None
        """ Computer friendly designation.
        Type `str`. """
        
        self.title = None
        """ Human Friendly name.
        Type `str`. """
        
        self.subtitle = None
        """ Subordinate Friendly name.
        Type `str`. """
        
        self.alias = None
        """ Acronym or short name.
        List of `str` items. """
        
        self.author = None
        """ Source of Contract.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.scope = None
        """ A selector of legal concerns for this Contract definition,
        derivative, or instance in any legal state.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.topicCodeableConcept = None
        """ Focus of contract interest.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.topicReference = None
        """ Focus of contract interest.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.type = None
        """ A high-level category for the legal instrument, whether constructed
        as a Contract definition, derivative, or instance in any legal
        state.  Provides additional information about its content within
        the context of the Contract's scope to distinguish the kinds of
        systems that would be interested in the contract.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subType = None
        """ Sub-category for the Contract that distinguishes the kinds of
        systems that would be interested in the Contract within the context
        of the Contract's scope.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.contentDefinition = None
        """ Contract precursor content.
        Type `ContractContentDefinition` (represented as `dict` in JSON). """
        
        self.term = None
        """ Contract Term List.
        List of `ContractTerm` items (represented as `dict` in JSON). """
        
        self.supportingInfo = None
        """ Extra Information.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.relevantHistory = None
        """ Key event in Contract History.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.signer = None
        """ Contract Signatory.
        List of `ContractSigner` items (represented as `dict` in JSON). """
        
        self.friendly = None
        """ Contract Friendly Language.
        List of `ContractFriendly` items (represented as `dict` in JSON). """
        
        self.legal = None
        """ Contract Legal Language.
        List of `ContractLegal` items (represented as `dict` in JSON). """
        
        self.rule = None
        """ Computable Contract Language.
        List of `ContractRule` items (represented as `dict` in JSON). """
        
        self.legallyBindingAttachment = None
        """ Binding Contract.
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.legallyBindingReference = None
        """ Binding Contract.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(Contract, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Contract, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("url", "url", str, False, None, False),
            ("version", "version", str, False, None, False),
            ("status", "status", str, False, None, False),
            ("legalState", "legalState", codeableconcept.CodeableConcept, False, None, False),
            ("instantiatesCanonical", "instantiatesCanonical", fhirreference.FHIRReference, False, None, False),
            ("instantiatesUri", "instantiatesUri", str, False, None, False),
            ("contentDerivative", "contentDerivative", codeableconcept.CodeableConcept, False, None, False),
            ("issued", "issued", fhirdate.FHIRDate, False, None, False),
            ("applies", "applies", period.Period, False, None, False),
            ("expirationType", "expirationType", codeableconcept.CodeableConcept, False, None, False),
            ("subject", "subject", fhirreference.FHIRReference, True, None, False),
            ("authority", "authority", fhirreference.FHIRReference, True, None, False),
            ("domain", "domain", fhirreference.FHIRReference, True, None, False),
            ("site", "site", fhirreference.FHIRReference, True, None, False),
            ("name", "name", str, False, None, False),
            ("title", "title", str, False, None, False),
            ("subtitle", "subtitle", str, False, None, False),
            ("alias", "alias", str, True, None, False),
            ("author", "author", fhirreference.FHIRReference, False, None, False),
            ("scope", "scope", codeableconcept.CodeableConcept, False, None, False),
            ("topicCodeableConcept", "topicCodeableConcept", codeableconcept.CodeableConcept, False, "topic", False),
            ("topicReference", "topicReference", fhirreference.FHIRReference, False, "topic", False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("subType", "subType", codeableconcept.CodeableConcept, True, None, False),
            ("contentDefinition", "contentDefinition", ContractContentDefinition, False, None, False),
            ("term", "term", ContractTerm, True, None, False),
            ("supportingInfo", "supportingInfo", fhirreference.FHIRReference, True, None, False),
            ("relevantHistory", "relevantHistory", fhirreference.FHIRReference, True, None, False),
            ("signer", "signer", ContractSigner, True, None, False),
            ("friendly", "friendly", ContractFriendly, True, None, False),
            ("legal", "legal", ContractLegal, True, None, False),
            ("rule", "rule", ContractRule, True, None, False),
            ("legallyBindingAttachment", "legallyBindingAttachment", attachment.Attachment, False, "legallyBinding", False),
            ("legallyBindingReference", "legallyBindingReference", fhirreference.FHIRReference, False, "legallyBinding", False),
        ])
        return js


from . import backboneelement

class ContractContentDefinition(backboneelement.BackboneElement):
    """ Contract precursor content.
    
    Precusory content developed with a focus and intent of supporting the
    formation a Contract instance, which may be associated with and
    transformable into a Contract.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Precusory content structure and use, i.e., a boilerplate, template, application for a contract such as an insurance policy or benefits under a program, e.g., workers compensation."""
    _attribute_docstrings['subType'] = """Detailed Precusory content type."""
    _attribute_docstrings['publisher'] = """Publisher Entity."""
    _attribute_docstrings['publicationDate'] = """When published."""
    _attribute_docstrings['publicationStatus'] = """None"""
    _attribute_docstrings['copyright'] = """Publication Ownership."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://hl7.org/fhir/contract-definition-type',
        'restricted_to': ['temp'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['subType'] = {
        'url': 'http://hl7.org/fhir/contract-definition-subtype',
        'restricted_to': ['temp'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['publicationStatus'] = {
        'url': 'http://hl7.org/fhir/contract-publicationstatus',
        'restricted_to': ['amended', 'appended', 'cancelled', 'disputed', 'entered-in-error', 'executable', 'executed', 'negotiable', 'offered', 'policy', 'rejected', 'renewed', 'revoked', 'resolved', 'terminated'],
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
        """ Precusory content structure and use, i.e., a boilerplate, template,
        application for a contract such as an insurance policy or benefits
        under a program, e.g., workers compensation.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subType = None
        """ Detailed Precusory content type.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.publisher = None
        """ Publisher Entity.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.publicationDate = None
        """ When published.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.publicationStatus = None
        """ None.
        Type `str`. """
        
        self.copyright = None
        """ Publication Ownership.
        Type `str`. """
        
        super(ContractContentDefinition, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ContractContentDefinition, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("subType", "subType", codeableconcept.CodeableConcept, False, None, False),
            ("publisher", "publisher", fhirreference.FHIRReference, False, None, False),
            ("publicationDate", "publicationDate", fhirdate.FHIRDate, False, None, False),
            ("publicationStatus", "publicationStatus", str, False, None, True),
            ("copyright", "copyright", str, False, None, False),
        ])
        return js


class ContractFriendly(backboneelement.BackboneElement):
    """ Contract Friendly Language.
    
    The "patient friendly language" versionof the Contract in whole or in
    parts. "Patient friendly language" means the representation of the Contract
    and Contract Provisions in a manner that is readily accessible and
    understandable by a layperson in accordance with best practices for
    communication styles that ensure that those agreeing to or signing the
    Contract understand the roles, actions, obligations, responsibilities, and
    implication of the agreement.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['contentAttachment'] = """Easily comprehended representation of this Contract."""
    _attribute_docstrings['contentReference'] = """Easily comprehended representation of this Contract."""

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
        
        self.contentAttachment = None
        """ Easily comprehended representation of this Contract.
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.contentReference = None
        """ Easily comprehended representation of this Contract.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(ContractFriendly, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ContractFriendly, self).elementProperties()
        js.extend([
            ("contentAttachment", "contentAttachment", attachment.Attachment, False, "content", True),
            ("contentReference", "contentReference", fhirreference.FHIRReference, False, "content", True),
        ])
        return js


class ContractLegal(backboneelement.BackboneElement):
    """ Contract Legal Language.
    
    List of Legal expressions or representations of this Contract.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['contentAttachment'] = """Contract Legal Text."""
    _attribute_docstrings['contentReference'] = """Contract Legal Text."""

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
        
        self.contentAttachment = None
        """ Contract Legal Text.
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.contentReference = None
        """ Contract Legal Text.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(ContractLegal, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ContractLegal, self).elementProperties()
        js.extend([
            ("contentAttachment", "contentAttachment", attachment.Attachment, False, "content", True),
            ("contentReference", "contentReference", fhirreference.FHIRReference, False, "content", True),
        ])
        return js


class ContractRule(backboneelement.BackboneElement):
    """ Computable Contract Language.
    
    List of Computable Policy Rule Language Representations of this Contract.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['contentAttachment'] = """Computable Contract Rules."""
    _attribute_docstrings['contentReference'] = """Computable Contract Rules."""

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
        
        self.contentAttachment = None
        """ Computable Contract Rules.
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.contentReference = None
        """ Computable Contract Rules.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(ContractRule, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ContractRule, self).elementProperties()
        js.extend([
            ("contentAttachment", "contentAttachment", attachment.Attachment, False, "content", True),
            ("contentReference", "contentReference", fhirreference.FHIRReference, False, "content", True),
        ])
        return js


class ContractSigner(backboneelement.BackboneElement):
    """ Contract Signatory.
    
    Parties with legal standing in the Contract, including the principal
    parties, the grantor(s) and grantee(s), which are any person or
    organization bound by the contract, and any ancillary parties, which
    facilitate the execution of the contract such as a notary or witness.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Contract Signatory Role."""
    _attribute_docstrings['party'] = """Contract Signatory Party."""
    _attribute_docstrings['signature'] = """Contract Documentation Signature."""

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
        """ Contract Signatory Role.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.party = None
        """ Contract Signatory Party.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.signature = None
        """ Contract Documentation Signature.
        List of `Signature` items (represented as `dict` in JSON). """
        
        super(ContractSigner, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ContractSigner, self).elementProperties()
        js.extend([
            ("type", "type", coding.Coding, False, None, True),
            ("party", "party", fhirreference.FHIRReference, False, None, True),
            ("signature", "signature", signature.Signature, True, None, True),
        ])
        return js


class ContractTerm(backboneelement.BackboneElement):
    """ Contract Term List.
    
    One or more Contract Provisions, which may be related and conveyed as a
    group, and may contain nested groups.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Contract Term Number."""
    _attribute_docstrings['issued'] = """Contract Term Issue Date Time."""
    _attribute_docstrings['applies'] = """Contract Term Effective Time."""
    _attribute_docstrings['topicCodeableConcept'] = """Term Concern."""
    _attribute_docstrings['topicReference'] = """Term Concern."""
    _attribute_docstrings['type'] = """A legal clause or condition contained within a contract that requires one or both parties to perform a particular requirement by some specified time or prevents one or both parties from performing a particular requirement by some specified time."""
    _attribute_docstrings['subType'] = """A specialized legal clause or condition based on overarching contract type."""
    _attribute_docstrings['text'] = """Term Statement."""
    _attribute_docstrings['securityLabel'] = """Protection for the Term."""
    _attribute_docstrings['offer'] = """Context of the Contract term."""
    _attribute_docstrings['asset'] = """Contract Term Asset List."""
    _attribute_docstrings['action'] = """Entity being ascribed responsibility."""
    _attribute_docstrings['group'] = """Nested Contract Term Group."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/contracttermtypecodes',
        'restricted_to': ['statutory', 'subject-to'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['subType'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/contracttermsubtypecodes',
        'restricted_to': ['condition', 'warranty', 'innominate'],
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
        """ Contract Term Number.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.issued = None
        """ Contract Term Issue Date Time.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.applies = None
        """ Contract Term Effective Time.
        Type `Period` (represented as `dict` in JSON). """
        
        self.topicCodeableConcept = None
        """ Term Concern.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.topicReference = None
        """ Term Concern.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.type = None
        """ A legal clause or condition contained within a contract that
        requires one or both parties to perform a particular requirement by
        some specified time or prevents one or both parties from performing
        a particular requirement by some specified time.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subType = None
        """ A specialized legal clause or condition based on overarching
        contract type.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.text = None
        """ Term Statement.
        Type `str`. """
        
        self.securityLabel = None
        """ Protection for the Term.
        List of `ContractTermSecurityLabel` items (represented as `dict` in JSON). """
        
        self.offer = None
        """ Context of the Contract term.
        Type `ContractTermOffer` (represented as `dict` in JSON). """
        
        self.asset = None
        """ Contract Term Asset List.
        List of `ContractTermAsset` items (represented as `dict` in JSON). """
        
        self.action = None
        """ Entity being ascribed responsibility.
        List of `ContractTermAction` items (represented as `dict` in JSON). """
        
        self.group = None
        """ Nested Contract Term Group.
        List of `ContractTerm` items (represented as `dict` in JSON). """
        
        super(ContractTerm, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ContractTerm, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, False, None, False),
            ("issued", "issued", fhirdate.FHIRDate, False, None, False),
            ("applies", "applies", period.Period, False, None, False),
            ("topicCodeableConcept", "topicCodeableConcept", codeableconcept.CodeableConcept, False, "topic", False),
            ("topicReference", "topicReference", fhirreference.FHIRReference, False, "topic", False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("subType", "subType", codeableconcept.CodeableConcept, False, None, False),
            ("text", "text", str, False, None, False),
            ("securityLabel", "securityLabel", ContractTermSecurityLabel, True, None, False),
            ("offer", "offer", ContractTermOffer, False, None, True),
            ("asset", "asset", ContractTermAsset, True, None, False),
            ("action", "action", ContractTermAction, True, None, False),
            ("group", "group", ContractTerm, True, None, False),
        ])
        return js


class ContractTermAction(backboneelement.BackboneElement):
    """ Entity being ascribed responsibility.
    
    An actor taking a role in an activity for which it can be assigned some
    degree of responsibility for the activity taking place.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['doNotPerform'] = """True if the term prohibits the  action."""
    _attribute_docstrings['type'] = """Activity or service obligation to be done or not done, performed or not performed, effectuated or not by this Contract term."""
    _attribute_docstrings['subject'] = """Entity of the action."""
    _attribute_docstrings['intent'] = """Purpose for the Contract Term Action."""
    _attribute_docstrings['linkId'] = """Pointer to specific item."""
    _attribute_docstrings['status'] = """Current state of the term action."""
    _attribute_docstrings['context'] = """Episode associated with action."""
    _attribute_docstrings['contextLinkId'] = """Pointer to specific item."""
    _attribute_docstrings['occurrenceDateTime'] = """When action happens."""
    _attribute_docstrings['occurrencePeriod'] = """When action happens."""
    _attribute_docstrings['occurrenceTiming'] = """When action happens."""
    _attribute_docstrings['requester'] = """Who asked for action."""
    _attribute_docstrings['requesterLinkId'] = """Pointer to specific item."""
    _attribute_docstrings['performerType'] = """The type of individual that is desired or required to perform or not perform the action."""
    _attribute_docstrings['performerRole'] = """The type of role or competency of an individual desired or required to perform or not perform the action."""
    _attribute_docstrings['performer'] = """Actor that wil execute (or not) the action."""
    _attribute_docstrings['performerLinkId'] = """Pointer to specific item."""
    _attribute_docstrings['reasonCode'] = """Why is action (not) needed?."""
    _attribute_docstrings['reasonReference'] = """Why is action (not) needed?."""
    _attribute_docstrings['reason'] = """Why action is to be performed."""
    _attribute_docstrings['reasonLinkId'] = """Pointer to specific item."""
    _attribute_docstrings['note'] = """Comments about the action."""
    _attribute_docstrings['securityLabelNumber'] = """Action restriction numbers."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/contractaction',
        'restricted_to': ['action-a', 'action-b'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/contract-action-status',
        'restricted_to': ['complete'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['performerType'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/provenance-participant-type',
        'restricted_to': ['enterer', 'performer', 'author', 'verifier', 'legal', 'attester', 'informant', 'custodian', 'assembler', 'composer'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['performerRole'] = {
        'url': 'http://hl7.org/fhir/provenance-participant-role',
        'restricted_to': ['enterer', 'performer', 'author', 'verifier', 'legal', 'attester', 'informant', 'custodian', 'assembler', 'composer'],
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
        
        self.doNotPerform = None
        """ True if the term prohibits the  action.
        Type `bool`. """
        
        self.type = None
        """ Activity or service obligation to be done or not done, performed or
        not performed, effectuated or not by this Contract term.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.subject = None
        """ Entity of the action.
        List of `ContractTermActionSubject` items (represented as `dict` in JSON). """
        
        self.intent = None
        """ Purpose for the Contract Term Action.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.linkId = None
        """ Pointer to specific item.
        List of `str` items. """
        
        self.status = None
        """ Current state of the term action.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.context = None
        """ Episode associated with action.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.contextLinkId = None
        """ Pointer to specific item.
        List of `str` items. """
        
        self.occurrenceDateTime = None
        """ When action happens.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.occurrencePeriod = None
        """ When action happens.
        Type `Period` (represented as `dict` in JSON). """
        
        self.occurrenceTiming = None
        """ When action happens.
        Type `Timing` (represented as `dict` in JSON). """
        
        self.requester = None
        """ Who asked for action.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.requesterLinkId = None
        """ Pointer to specific item.
        List of `str` items. """
        
        self.performerType = None
        """ The type of individual that is desired or required to perform or
        not perform the action.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.performerRole = None
        """ The type of role or competency of an individual desired or required
        to perform or not perform the action.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.performer = None
        """ Actor that wil execute (or not) the action.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.performerLinkId = None
        """ Pointer to specific item.
        List of `str` items. """
        
        self.reasonCode = None
        """ Why is action (not) needed?.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.reasonReference = None
        """ Why is action (not) needed?.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.reason = None
        """ Why action is to be performed.
        List of `str` items. """
        
        self.reasonLinkId = None
        """ Pointer to specific item.
        List of `str` items. """
        
        self.note = None
        """ Comments about the action.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        self.securityLabelNumber = None
        """ Action restriction numbers.
        List of `int` items. """
        
        super(ContractTermAction, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ContractTermAction, self).elementProperties()
        js.extend([
            ("doNotPerform", "doNotPerform", bool, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, True),
            ("subject", "subject", ContractTermActionSubject, True, None, False),
            ("intent", "intent", codeableconcept.CodeableConcept, False, None, True),
            ("linkId", "linkId", str, True, None, False),
            ("status", "status", codeableconcept.CodeableConcept, False, None, True),
            ("context", "context", fhirreference.FHIRReference, False, None, False),
            ("contextLinkId", "contextLinkId", str, True, None, False),
            ("occurrenceDateTime", "occurrenceDateTime", fhirdate.FHIRDate, False, "occurrence", False),
            ("occurrencePeriod", "occurrencePeriod", period.Period, False, "occurrence", False),
            ("occurrenceTiming", "occurrenceTiming", timing.Timing, False, "occurrence", False),
            ("requester", "requester", fhirreference.FHIRReference, True, None, False),
            ("requesterLinkId", "requesterLinkId", str, True, None, False),
            ("performerType", "performerType", codeableconcept.CodeableConcept, True, None, False),
            ("performerRole", "performerRole", codeableconcept.CodeableConcept, False, None, False),
            ("performer", "performer", fhirreference.FHIRReference, False, None, False),
            ("performerLinkId", "performerLinkId", str, True, None, False),
            ("reasonCode", "reasonCode", codeableconcept.CodeableConcept, True, None, False),
            ("reasonReference", "reasonReference", fhirreference.FHIRReference, True, None, False),
            ("reason", "reason", str, True, None, False),
            ("reasonLinkId", "reasonLinkId", str, True, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
            ("securityLabelNumber", "securityLabelNumber", int, True, None, False),
        ])
        return js


class ContractTermActionSubject(backboneelement.BackboneElement):
    """ Entity of the action.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['reference'] = """Entity of the action."""
    _attribute_docstrings['role'] = """Role type of agent assigned roles in this Contract."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['role'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/contractactorrole',
        'restricted_to': ['practitioner', 'patient'],
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
        
        self.reference = None
        """ Entity of the action.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.role = None
        """ Role type of agent assigned roles in this Contract.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(ContractTermActionSubject, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ContractTermActionSubject, self).elementProperties()
        js.extend([
            ("reference", "reference", fhirreference.FHIRReference, True, None, True),
            ("role", "role", codeableconcept.CodeableConcept, False, None, False),
        ])
        return js


class ContractTermAsset(backboneelement.BackboneElement):
    """ Contract Term Asset List.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['scope'] = """Differentiates the kind of the asset ."""
    _attribute_docstrings['type'] = """Target entity type about which the term may be concerned."""
    _attribute_docstrings['typeReference'] = """Associated entities."""
    _attribute_docstrings['subtype'] = """May be a subtype or part of an offered asset."""
    _attribute_docstrings['relationship'] = """Kinship of the asset."""
    _attribute_docstrings['context'] = """Circumstance of the asset."""
    _attribute_docstrings['condition'] = """Quality desctiption of asset."""
    _attribute_docstrings['periodType'] = """Type of Asset availability for use or ownership."""
    _attribute_docstrings['period'] = """Time period of the asset."""
    _attribute_docstrings['usePeriod'] = """Time period."""
    _attribute_docstrings['text'] = """Asset clause or question text."""
    _attribute_docstrings['linkId'] = """Pointer to asset text."""
    _attribute_docstrings['answer'] = """Response to assets."""
    _attribute_docstrings['securityLabelNumber'] = """Asset restriction numbers."""
    _attribute_docstrings['valuedItem'] = """Contract Valued Item List."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['scope'] = {
        'url': 'http://hl7.org/fhir/contract-asset-scope',
        'restricted_to': ['thing'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['type'] = {
        'url': 'http://hl7.org/fhir/contract-asset-type',
        'restricted_to': ['participation'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['subtype'] = {
        'url': 'http://hl7.org/fhir/contract-asset-subtype',
        'restricted_to': ['participation'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['periodType'] = {
        'url': 'http://hl7.org/fhir/asset-availability',
        'restricted_to': ['lease'],
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
        
        self.scope = None
        """ Differentiates the kind of the asset.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.type = None
        """ Target entity type about which the term may be concerned.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.typeReference = None
        """ Associated entities.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.subtype = None
        """ May be a subtype or part of an offered asset.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.relationship = None
        """ Kinship of the asset.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.context = None
        """ Circumstance of the asset.
        List of `ContractTermAssetContext` items (represented as `dict` in JSON). """
        
        self.condition = None
        """ Quality desctiption of asset.
        Type `str`. """
        
        self.periodType = None
        """ Type of Asset availability for use or ownership.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.period = None
        """ Time period of the asset.
        List of `Period` items (represented as `dict` in JSON). """
        
        self.usePeriod = None
        """ Time period.
        List of `Period` items (represented as `dict` in JSON). """
        
        self.text = None
        """ Asset clause or question text.
        Type `str`. """
        
        self.linkId = None
        """ Pointer to asset text.
        List of `str` items. """
        
        self.answer = None
        """ Response to assets.
        List of `ContractTermOfferAnswer` items (represented as `dict` in JSON). """
        
        self.securityLabelNumber = None
        """ Asset restriction numbers.
        List of `int` items. """
        
        self.valuedItem = None
        """ Contract Valued Item List.
        List of `ContractTermAssetValuedItem` items (represented as `dict` in JSON). """
        
        super(ContractTermAsset, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ContractTermAsset, self).elementProperties()
        js.extend([
            ("scope", "scope", codeableconcept.CodeableConcept, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, True, None, False),
            ("typeReference", "typeReference", fhirreference.FHIRReference, True, None, False),
            ("subtype", "subtype", codeableconcept.CodeableConcept, True, None, False),
            ("relationship", "relationship", coding.Coding, False, None, False),
            ("context", "context", ContractTermAssetContext, True, None, False),
            ("condition", "condition", str, False, None, False),
            ("periodType", "periodType", codeableconcept.CodeableConcept, True, None, False),
            ("period", "period", period.Period, True, None, False),
            ("usePeriod", "usePeriod", period.Period, True, None, False),
            ("text", "text", str, False, None, False),
            ("linkId", "linkId", str, True, None, False),
            ("answer", "answer", ContractTermOfferAnswer, True, None, False),
            ("securityLabelNumber", "securityLabelNumber", int, True, None, False),
            ("valuedItem", "valuedItem", ContractTermAssetValuedItem, True, None, False),
        ])
        return js


class ContractTermAssetContext(backboneelement.BackboneElement):
    """ Circumstance of the asset.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['reference'] = """Creator,custodian or owner."""
    _attribute_docstrings['code'] = """Coded representation of the context generally or of the Referenced entity, such as the asset holder type or location."""
    _attribute_docstrings['text'] = """Context description."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['code'] = {
        'url': 'http://hl7.org/fhir/contract-asset-context',
        'restricted_to': ['custodian'],
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
        
        self.reference = None
        """ Creator,custodian or owner.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.code = None
        """ Coded representation of the context generally or of the Referenced
        entity, such as the asset holder type or location.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.text = None
        """ Context description.
        Type `str`. """
        
        super(ContractTermAssetContext, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ContractTermAssetContext, self).elementProperties()
        js.extend([
            ("reference", "reference", fhirreference.FHIRReference, False, None, False),
            ("code", "code", codeableconcept.CodeableConcept, True, None, False),
            ("text", "text", str, False, None, False),
        ])
        return js


class ContractTermAssetValuedItem(backboneelement.BackboneElement):
    """ Contract Valued Item List.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['entityCodeableConcept'] = """Contract Valued Item Type."""
    _attribute_docstrings['entityReference'] = """Contract Valued Item Type."""
    _attribute_docstrings['identifier'] = """Contract Valued Item Number."""
    _attribute_docstrings['effectiveTime'] = """Contract Valued Item Effective Tiem."""
    _attribute_docstrings['quantity'] = """Count of Contract Valued Items."""
    _attribute_docstrings['unitPrice'] = """Contract Valued Item fee, charge, or cost."""
    _attribute_docstrings['factor'] = """Contract Valued Item Price Scaling Factor."""
    _attribute_docstrings['points'] = """Contract Valued Item Difficulty Scaling Factor."""
    _attribute_docstrings['net'] = """Total Contract Valued Item Value."""
    _attribute_docstrings['payment'] = """Terms of valuation."""
    _attribute_docstrings['paymentDate'] = """When payment is due."""
    _attribute_docstrings['responsible'] = """Who will make payment."""
    _attribute_docstrings['recipient'] = """Who will receive payment."""
    _attribute_docstrings['linkId'] = """Pointer to specific item."""
    _attribute_docstrings['securityLabelNumber'] = """Security Labels that define affected terms."""

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
        
        self.entityCodeableConcept = None
        """ Contract Valued Item Type.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.entityReference = None
        """ Contract Valued Item Type.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.identifier = None
        """ Contract Valued Item Number.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.effectiveTime = None
        """ Contract Valued Item Effective Tiem.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.quantity = None
        """ Count of Contract Valued Items.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.unitPrice = None
        """ Contract Valued Item fee, charge, or cost.
        Type `Money` (represented as `dict` in JSON). """
        
        self.factor = None
        """ Contract Valued Item Price Scaling Factor.
        Type `float`. """
        
        self.points = None
        """ Contract Valued Item Difficulty Scaling Factor.
        Type `float`. """
        
        self.net = None
        """ Total Contract Valued Item Value.
        Type `Money` (represented as `dict` in JSON). """
        
        self.payment = None
        """ Terms of valuation.
        Type `str`. """
        
        self.paymentDate = None
        """ When payment is due.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.responsible = None
        """ Who will make payment.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.recipient = None
        """ Who will receive payment.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.linkId = None
        """ Pointer to specific item.
        List of `str` items. """
        
        self.securityLabelNumber = None
        """ Security Labels that define affected terms.
        List of `int` items. """
        
        super(ContractTermAssetValuedItem, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ContractTermAssetValuedItem, self).elementProperties()
        js.extend([
            ("entityCodeableConcept", "entityCodeableConcept", codeableconcept.CodeableConcept, False, "entity", False),
            ("entityReference", "entityReference", fhirreference.FHIRReference, False, "entity", False),
            ("identifier", "identifier", identifier.Identifier, False, None, False),
            ("effectiveTime", "effectiveTime", fhirdate.FHIRDate, False, None, False),
            ("quantity", "quantity", quantity.Quantity, False, None, False),
            ("unitPrice", "unitPrice", money.Money, False, None, False),
            ("factor", "factor", float, False, None, False),
            ("points", "points", float, False, None, False),
            ("net", "net", money.Money, False, None, False),
            ("payment", "payment", str, False, None, False),
            ("paymentDate", "paymentDate", fhirdate.FHIRDate, False, None, False),
            ("responsible", "responsible", fhirreference.FHIRReference, False, None, False),
            ("recipient", "recipient", fhirreference.FHIRReference, False, None, False),
            ("linkId", "linkId", str, True, None, False),
            ("securityLabelNumber", "securityLabelNumber", int, True, None, False),
        ])
        return js


class ContractTermOffer(backboneelement.BackboneElement):
    """ Context of the Contract term.
    
    The matter of concern in the context of this provision of the agrement.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Offer business ID."""
    _attribute_docstrings['party'] = """Offer Recipient."""
    _attribute_docstrings['topic'] = """Negotiable offer asset."""
    _attribute_docstrings['type'] = """Type of Contract Provision such as specific requirements, purposes for actions, obligations, prohibitions, e.g. life time maximum benefit."""
    _attribute_docstrings['decision'] = """Accepting party choice."""
    _attribute_docstrings['decisionMode'] = """How the decision about a Contract was conveyed."""
    _attribute_docstrings['answer'] = """Response to offer text."""
    _attribute_docstrings['text'] = """Human readable offer text."""
    _attribute_docstrings['linkId'] = """Pointer to text."""
    _attribute_docstrings['securityLabelNumber'] = """Offer restriction numbers."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/contracttermtypecodes',
        'restricted_to': ['statutory', 'subject-to'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['decisionMode'] = {
        'url': 'http://hl7.org/fhir/contract-decision-mode',
        'restricted_to': ['policy'],
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
        """ Offer business ID.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.party = None
        """ Offer Recipient.
        List of `ContractTermOfferParty` items (represented as `dict` in JSON). """
        
        self.topic = None
        """ Negotiable offer asset.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.type = None
        """ Type of Contract Provision such as specific requirements, purposes
        for actions, obligations, prohibitions, e.g. life time maximum
        benefit.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.decision = None
        """ Accepting party choice.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.decisionMode = None
        """ How the decision about a Contract was conveyed.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.answer = None
        """ Response to offer text.
        List of `ContractTermOfferAnswer` items (represented as `dict` in JSON). """
        
        self.text = None
        """ Human readable offer text.
        Type `str`. """
        
        self.linkId = None
        """ Pointer to text.
        List of `str` items. """
        
        self.securityLabelNumber = None
        """ Offer restriction numbers.
        List of `int` items. """
        
        super(ContractTermOffer, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ContractTermOffer, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("party", "party", ContractTermOfferParty, True, None, False),
            ("topic", "topic", fhirreference.FHIRReference, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("decision", "decision", codeableconcept.CodeableConcept, False, None, False),
            ("decisionMode", "decisionMode", codeableconcept.CodeableConcept, True, None, False),
            ("answer", "answer", ContractTermOfferAnswer, True, None, False),
            ("text", "text", str, False, None, False),
            ("linkId", "linkId", str, True, None, False),
            ("securityLabelNumber", "securityLabelNumber", int, True, None, False),
        ])
        return js


class ContractTermOfferAnswer(backboneelement.BackboneElement):
    """ Response to offer text.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['valueBoolean'] = """The actual answer response."""
    _attribute_docstrings['valueDecimal'] = """The actual answer response."""
    _attribute_docstrings['valueInteger'] = """The actual answer response."""
    _attribute_docstrings['valueDate'] = """The actual answer response."""
    _attribute_docstrings['valueDateTime'] = """The actual answer response."""
    _attribute_docstrings['valueTime'] = """The actual answer response."""
    _attribute_docstrings['valueString'] = """The actual answer response."""
    _attribute_docstrings['valueUri'] = """The actual answer response."""
    _attribute_docstrings['valueAttachment'] = """The actual answer response."""
    _attribute_docstrings['valueCoding'] = """The actual answer response."""
    _attribute_docstrings['valueQuantity'] = """The actual answer response."""
    _attribute_docstrings['valueReference'] = """The actual answer response."""

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
        
        self.valueBoolean = None
        """ The actual answer response.
        Type `bool`. """
        
        self.valueDecimal = None
        """ The actual answer response.
        Type `float`. """
        
        self.valueInteger = None
        """ The actual answer response.
        Type `int`. """
        
        self.valueDate = None
        """ The actual answer response.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valueDateTime = None
        """ The actual answer response.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valueTime = None
        """ The actual answer response.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valueString = None
        """ The actual answer response.
        Type `str`. """
        
        self.valueUri = None
        """ The actual answer response.
        Type `str`. """
        
        self.valueAttachment = None
        """ The actual answer response.
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.valueCoding = None
        """ The actual answer response.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.valueQuantity = None
        """ The actual answer response.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.valueReference = None
        """ The actual answer response.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(ContractTermOfferAnswer, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ContractTermOfferAnswer, self).elementProperties()
        js.extend([
            ("valueBoolean", "valueBoolean", bool, False, "value", True),
            ("valueDecimal", "valueDecimal", float, False, "value", True),
            ("valueInteger", "valueInteger", int, False, "value", True),
            ("valueDate", "valueDate", fhirdate.FHIRDate, False, "value", True),
            ("valueDateTime", "valueDateTime", fhirdate.FHIRDate, False, "value", True),
            ("valueTime", "valueTime", fhirdate.FHIRDate, False, "value", True),
            ("valueString", "valueString", str, False, "value", True),
            ("valueUri", "valueUri", str, False, "value", True),
            ("valueAttachment", "valueAttachment", attachment.Attachment, False, "value", True),
            ("valueCoding", "valueCoding", coding.Coding, False, "value", True),
            ("valueQuantity", "valueQuantity", quantity.Quantity, False, "value", True),
            ("valueReference", "valueReference", fhirreference.FHIRReference, False, "value", True),
        ])
        return js


class ContractTermOfferParty(backboneelement.BackboneElement):
    """ Offer Recipient.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['reference'] = """Referenced entity."""
    _attribute_docstrings['role'] = """How the party participates in the offer."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['role'] = {
        'url': 'http://hl7.org/fhir/contract-party-role',
        'restricted_to': ['flunky'],
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
        
        self.reference = None
        """ Referenced entity.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.role = None
        """ How the party participates in the offer.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(ContractTermOfferParty, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ContractTermOfferParty, self).elementProperties()
        js.extend([
            ("reference", "reference", fhirreference.FHIRReference, True, None, True),
            ("role", "role", codeableconcept.CodeableConcept, False, None, True),
        ])
        return js


class ContractTermSecurityLabel(backboneelement.BackboneElement):
    """ Protection for the Term.
    
    Security labels that protect the handling of information about the term and
    its elements, which may be specifically identified..
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['number'] = """Link to Security Labels."""
    _attribute_docstrings['classification'] = """Confidentiality Protection."""
    _attribute_docstrings['category'] = """Applicable Policy."""
    _attribute_docstrings['control'] = """Handling Instructions."""

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
        
        self.number = None
        """ Link to Security Labels.
        List of `int` items. """
        
        self.classification = None
        """ Confidentiality Protection.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.category = None
        """ Applicable Policy.
        List of `Coding` items (represented as `dict` in JSON). """
        
        self.control = None
        """ Handling Instructions.
        List of `Coding` items (represented as `dict` in JSON). """
        
        super(ContractTermSecurityLabel, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ContractTermSecurityLabel, self).elementProperties()
        js.extend([
            ("number", "number", int, True, None, False),
            ("classification", "classification", coding.Coding, False, None, True),
            ("category", "category", coding.Coding, True, None, False),
            ("control", "control", coding.Coding, True, None, False),
        ])
        return js


import sys
try:
    from . import annotation
except ImportError:
    annotation = sys.modules[__package__ + '.annotation']
try:
    from . import attachment
except ImportError:
    attachment = sys.modules[__package__ + '.attachment']
try:
    from . import codeableconcept
except ImportError:
    codeableconcept = sys.modules[__package__ + '.codeableconcept']
try:
    from . import coding
except ImportError:
    coding = sys.modules[__package__ + '.coding']
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
    from . import money
except ImportError:
    money = sys.modules[__package__ + '.money']
try:
    from . import period
except ImportError:
    period = sys.modules[__package__ + '.period']
try:
    from . import quantity
except ImportError:
    quantity = sys.modules[__package__ + '.quantity']
try:
    from . import signature
except ImportError:
    signature = sys.modules[__package__ + '.signature']
try:
    from . import timing
except ImportError:
    timing = sys.modules[__package__ + '.timing']
