#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/QuestionnaireResponse) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class QuestionnaireResponse(domainresource.DomainResource):
    """ A structured set of questions and their answers.
    
    A structured set of questions and their answers. The questions are ordered
    and grouped into coherent subsets, corresponding to the structure of the
    grouping of the questionnaire being responded to.
    """
    
    resource_type = "QuestionnaireResponse"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Unique id for this set of answers."""
    _attribute_docstrings['basedOn'] = """Request fulfilled by this QuestionnaireResponse."""
    _attribute_docstrings['partOf'] = """Part of this action."""
    _attribute_docstrings['questionnaire'] = """Form being answered."""
    _attribute_docstrings['status'] = """The position of the questionnaire response within its overall lifecycle."""
    _attribute_docstrings['subject'] = """The subject of the questions."""
    _attribute_docstrings['encounter'] = """Encounter created as part of."""
    _attribute_docstrings['authored'] = """Date the answers were gathered."""
    _attribute_docstrings['author'] = """Person who received and recorded the answers."""
    _attribute_docstrings['source'] = """The person who answered the questions."""
    _attribute_docstrings['item'] = """Groups and questions."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/questionnaire-answers-status',
        'restricted_to': ['in-progress', 'completed', 'amended', 'entered-in-error', 'stopped'],
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
        
        self.identifier = None
        """ Unique id for this set of answers.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.basedOn = None
        """ Request fulfilled by this QuestionnaireResponse.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.partOf = None
        """ Part of this action.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.questionnaire = None
        """ Form being answered.
        Type `str`. """
        
        self.status = None
        """ The position of the questionnaire response within its overall
        lifecycle.
        Type `str`. """
        
        self.subject = None
        """ The subject of the questions.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.encounter = None
        """ Encounter created as part of.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.authored = None
        """ Date the answers were gathered.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.author = None
        """ Person who received and recorded the answers.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.source = None
        """ The person who answered the questions.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.item = None
        """ Groups and questions.
        List of `QuestionnaireResponseItem` items (represented as `dict` in JSON). """
        
        super(QuestionnaireResponse, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(QuestionnaireResponse, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, False, None, False),
            ("basedOn", "basedOn", fhirreference.FHIRReference, True, None, False),
            ("partOf", "partOf", fhirreference.FHIRReference, True, None, False),
            ("questionnaire", "questionnaire", str, False, None, False),
            ("status", "status", str, False, None, True),
            ("subject", "subject", fhirreference.FHIRReference, False, None, False),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("authored", "authored", fhirdate.FHIRDate, False, None, False),
            ("author", "author", fhirreference.FHIRReference, False, None, False),
            ("source", "source", fhirreference.FHIRReference, False, None, False),
            ("item", "item", QuestionnaireResponseItem, True, None, False),
        ])
        return js


from . import backboneelement

class QuestionnaireResponseItem(backboneelement.BackboneElement):
    """ Groups and questions.
    
    A group or question item from the original questionnaire for which answers
    are provided.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['linkId'] = """Pointer to specific item from Questionnaire."""
    _attribute_docstrings['definition'] = """ElementDefinition - details for the item."""
    _attribute_docstrings['text'] = """Name for group or question text."""
    _attribute_docstrings['answer'] = """The response(s) to the question."""
    _attribute_docstrings['item'] = """Nested questionnaire response items."""

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
        
        self.linkId = None
        """ Pointer to specific item from Questionnaire.
        Type `str`. """
        
        self.definition = None
        """ ElementDefinition - details for the item.
        Type `str`. """
        
        self.text = None
        """ Name for group or question text.
        Type `str`. """
        
        self.answer = None
        """ The response(s) to the question.
        List of `QuestionnaireResponseItemAnswer` items (represented as `dict` in JSON). """
        
        self.item = None
        """ Nested questionnaire response items.
        List of `QuestionnaireResponseItem` items (represented as `dict` in JSON). """
        
        super(QuestionnaireResponseItem, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(QuestionnaireResponseItem, self).elementProperties()
        js.extend([
            ("linkId", "linkId", str, False, None, True),
            ("definition", "definition", str, False, None, False),
            ("text", "text", str, False, None, False),
            ("answer", "answer", QuestionnaireResponseItemAnswer, True, None, False),
            ("item", "item", QuestionnaireResponseItem, True, None, False),
        ])
        return js


class QuestionnaireResponseItemAnswer(backboneelement.BackboneElement):
    """ The response(s) to the question.
    
    The respondent's answer(s) to the question.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['valueBoolean'] = """Single-valued answer to the question."""
    _attribute_docstrings['valueDecimal'] = """Single-valued answer to the question."""
    _attribute_docstrings['valueInteger'] = """Single-valued answer to the question."""
    _attribute_docstrings['valueDate'] = """Single-valued answer to the question."""
    _attribute_docstrings['valueDateTime'] = """Single-valued answer to the question."""
    _attribute_docstrings['valueTime'] = """Single-valued answer to the question."""
    _attribute_docstrings['valueString'] = """Single-valued answer to the question."""
    _attribute_docstrings['valueUri'] = """Single-valued answer to the question."""
    _attribute_docstrings['valueAttachment'] = """Single-valued answer to the question."""
    _attribute_docstrings['valueCoding'] = """Single-valued answer to the question."""
    _attribute_docstrings['valueQuantity'] = """Single-valued answer to the question."""
    _attribute_docstrings['valueReference'] = """Single-valued answer to the question."""
    _attribute_docstrings['item'] = """Nested groups and questions."""

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
        """ Single-valued answer to the question.
        Type `bool`. """
        
        self.valueDecimal = None
        """ Single-valued answer to the question.
        Type `float`. """
        
        self.valueInteger = None
        """ Single-valued answer to the question.
        Type `int`. """
        
        self.valueDate = None
        """ Single-valued answer to the question.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valueDateTime = None
        """ Single-valued answer to the question.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valueTime = None
        """ Single-valued answer to the question.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valueString = None
        """ Single-valued answer to the question.
        Type `str`. """
        
        self.valueUri = None
        """ Single-valued answer to the question.
        Type `str`. """
        
        self.valueAttachment = None
        """ Single-valued answer to the question.
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.valueCoding = None
        """ Single-valued answer to the question.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.valueQuantity = None
        """ Single-valued answer to the question.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.valueReference = None
        """ Single-valued answer to the question.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.item = None
        """ Nested groups and questions.
        List of `QuestionnaireResponseItem` items (represented as `dict` in JSON). """
        
        super(QuestionnaireResponseItemAnswer, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(QuestionnaireResponseItemAnswer, self).elementProperties()
        js.extend([
            ("valueBoolean", "valueBoolean", bool, False, "value", False),
            ("valueDecimal", "valueDecimal", float, False, "value", False),
            ("valueInteger", "valueInteger", int, False, "value", False),
            ("valueDate", "valueDate", fhirdate.FHIRDate, False, "value", False),
            ("valueDateTime", "valueDateTime", fhirdate.FHIRDate, False, "value", False),
            ("valueTime", "valueTime", fhirdate.FHIRDate, False, "value", False),
            ("valueString", "valueString", str, False, "value", False),
            ("valueUri", "valueUri", str, False, "value", False),
            ("valueAttachment", "valueAttachment", attachment.Attachment, False, "value", False),
            ("valueCoding", "valueCoding", coding.Coding, False, "value", False),
            ("valueQuantity", "valueQuantity", quantity.Quantity, False, "value", False),
            ("valueReference", "valueReference", fhirreference.FHIRReference, False, "value", False),
            ("item", "item", QuestionnaireResponseItem, True, None, False),
        ])
        return js


import sys
try:
    from . import attachment
except ImportError:
    attachment = sys.modules[__package__ + '.attachment']
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
    from . import quantity
except ImportError:
    quantity = sys.modules[__package__ + '.quantity']
