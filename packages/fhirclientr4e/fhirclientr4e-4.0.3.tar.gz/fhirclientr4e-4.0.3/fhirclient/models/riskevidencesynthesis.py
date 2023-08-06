#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/RiskEvidenceSynthesis) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class RiskEvidenceSynthesis(domainresource.DomainResource):
    """ A quantified estimate of risk based on a body of evidence.
    
    The RiskEvidenceSynthesis resource describes the likelihood of an outcome
    in a population plus exposure state where the risk estimate is derived from
    a combination of research studies.
    """
    
    resource_type = "RiskEvidenceSynthesis"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['url'] = """Canonical identifier for this risk evidence synthesis, represented as a URI (globally unique)."""
    _attribute_docstrings['identifier'] = """Additional identifier for the risk evidence synthesis."""
    _attribute_docstrings['version'] = """Business version of the risk evidence synthesis."""
    _attribute_docstrings['name'] = """Name for this risk evidence synthesis (computer friendly)."""
    _attribute_docstrings['title'] = """Name for this risk evidence synthesis (human friendly)."""
    _attribute_docstrings['status'] = """The status of this risk evidence synthesis. Enables tracking the life-cycle of the content."""
    _attribute_docstrings['date'] = """Date last changed."""
    _attribute_docstrings['publisher'] = """Name of the publisher (organization or individual)."""
    _attribute_docstrings['contact'] = """Contact details for the publisher."""
    _attribute_docstrings['description'] = """Natural language description of the risk evidence synthesis."""
    _attribute_docstrings['note'] = """Used for footnotes or explanatory notes."""
    _attribute_docstrings['useContext'] = """The context that the content is intended to support."""
    _attribute_docstrings['jurisdiction'] = """Intended jurisdiction for risk evidence synthesis (if applicable)."""
    _attribute_docstrings['copyright'] = """Use and/or publishing restrictions."""
    _attribute_docstrings['approvalDate'] = """When the risk evidence synthesis was approved by publisher."""
    _attribute_docstrings['lastReviewDate'] = """When the risk evidence synthesis was last reviewed."""
    _attribute_docstrings['effectivePeriod'] = """When the risk evidence synthesis is expected to be used."""
    _attribute_docstrings['topic'] = """Descriptive topics related to the content of the RiskEvidenceSynthesis. Topics provide a high-level categorization grouping types of EffectEvidenceSynthesiss that can be useful for filtering and searching."""
    _attribute_docstrings['author'] = """Who authored the content."""
    _attribute_docstrings['editor'] = """Who edited the content."""
    _attribute_docstrings['reviewer'] = """Who reviewed the content."""
    _attribute_docstrings['endorser'] = """Who endorsed the content."""
    _attribute_docstrings['relatedArtifact'] = """Additional documentation, citations, etc.."""
    _attribute_docstrings['synthesisType'] = """Type of synthesis eg meta-analysis."""
    _attribute_docstrings['studyType'] = """Type of study eg randomized trial."""
    _attribute_docstrings['population'] = """What population?."""
    _attribute_docstrings['exposure'] = """What exposure?."""
    _attribute_docstrings['outcome'] = """What outcome?."""
    _attribute_docstrings['sampleSize'] = """What sample size was involved?."""
    _attribute_docstrings['riskEstimate'] = """What was the estimated risk."""
    _attribute_docstrings['certainty'] = """How certain is the risk."""

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
    _attribute_enums['topic'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/definition-topic',
        'restricted_to': ['treatment', 'education', 'assessment'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['synthesisType'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/synthesis-type',
        'restricted_to': ['std-MA', 'IPD-MA', 'indirect-NMA', 'combined-NMA', 'range', 'classification'],
        'binding_strength': 'extensible',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['studyType'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/study-type',
        'restricted_to': ['RCT', 'CCT', 'cohort', 'case-control', 'series', 'case-report', 'mixed'],
        'binding_strength': 'extensible',
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
        
        self.url = None
        """ Canonical identifier for this risk evidence synthesis, represented
        as a URI (globally unique).
        Type `str`. """
        
        self.identifier = None
        """ Additional identifier for the risk evidence synthesis.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.version = None
        """ Business version of the risk evidence synthesis.
        Type `str`. """
        
        self.name = None
        """ Name for this risk evidence synthesis (computer friendly).
        Type `str`. """
        
        self.title = None
        """ Name for this risk evidence synthesis (human friendly).
        Type `str`. """
        
        self.status = None
        """ The status of this risk evidence synthesis. Enables tracking the
        life-cycle of the content.
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
        
        self.description = None
        """ Natural language description of the risk evidence synthesis.
        Type `str`. """
        
        self.note = None
        """ Used for footnotes or explanatory notes.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for risk evidence synthesis (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.copyright = None
        """ Use and/or publishing restrictions.
        Type `str`. """
        
        self.approvalDate = None
        """ When the risk evidence synthesis was approved by publisher.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.lastReviewDate = None
        """ When the risk evidence synthesis was last reviewed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.effectivePeriod = None
        """ When the risk evidence synthesis is expected to be used.
        Type `Period` (represented as `dict` in JSON). """
        
        self.topic = None
        """ Descriptive topics related to the content of the
        RiskEvidenceSynthesis. Topics provide a high-level categorization
        grouping types of EffectEvidenceSynthesiss that can be useful for
        filtering and searching.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.author = None
        """ Who authored the content.
        List of `ContactDetail` items (represented as `dict` in JSON). """
        
        self.editor = None
        """ Who edited the content.
        List of `ContactDetail` items (represented as `dict` in JSON). """
        
        self.reviewer = None
        """ Who reviewed the content.
        List of `ContactDetail` items (represented as `dict` in JSON). """
        
        self.endorser = None
        """ Who endorsed the content.
        List of `ContactDetail` items (represented as `dict` in JSON). """
        
        self.relatedArtifact = None
        """ Additional documentation, citations, etc.
        List of `RelatedArtifact` items (represented as `dict` in JSON). """
        
        self.synthesisType = None
        """ Type of synthesis eg meta-analysis.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.studyType = None
        """ Type of study eg randomized trial.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.population = None
        """ What population?.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.exposure = None
        """ What exposure?.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.outcome = None
        """ What outcome?.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.sampleSize = None
        """ What sample size was involved?.
        Type `RiskEvidenceSynthesisSampleSize` (represented as `dict` in JSON). """
        
        self.riskEstimate = None
        """ What was the estimated risk.
        Type `RiskEvidenceSynthesisRiskEstimate` (represented as `dict` in JSON). """
        
        self.certainty = None
        """ How certain is the risk.
        List of `RiskEvidenceSynthesisCertainty` items (represented as `dict` in JSON). """
        
        super(RiskEvidenceSynthesis, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(RiskEvidenceSynthesis, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("version", "version", str, False, None, False),
            ("name", "name", str, False, None, False),
            ("title", "title", str, False, None, False),
            ("status", "status", str, False, None, True),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("publisher", "publisher", str, False, None, False),
            ("contact", "contact", contactdetail.ContactDetail, True, None, False),
            ("description", "description", str, False, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
            ("useContext", "useContext", usagecontext.UsageContext, True, None, False),
            ("jurisdiction", "jurisdiction", codeableconcept.CodeableConcept, True, None, False),
            ("copyright", "copyright", str, False, None, False),
            ("approvalDate", "approvalDate", fhirdate.FHIRDate, False, None, False),
            ("lastReviewDate", "lastReviewDate", fhirdate.FHIRDate, False, None, False),
            ("effectivePeriod", "effectivePeriod", period.Period, False, None, False),
            ("topic", "topic", codeableconcept.CodeableConcept, True, None, False),
            ("author", "author", contactdetail.ContactDetail, True, None, False),
            ("editor", "editor", contactdetail.ContactDetail, True, None, False),
            ("reviewer", "reviewer", contactdetail.ContactDetail, True, None, False),
            ("endorser", "endorser", contactdetail.ContactDetail, True, None, False),
            ("relatedArtifact", "relatedArtifact", relatedartifact.RelatedArtifact, True, None, False),
            ("synthesisType", "synthesisType", codeableconcept.CodeableConcept, False, None, False),
            ("studyType", "studyType", codeableconcept.CodeableConcept, False, None, False),
            ("population", "population", fhirreference.FHIRReference, False, None, True),
            ("exposure", "exposure", fhirreference.FHIRReference, False, None, False),
            ("outcome", "outcome", fhirreference.FHIRReference, False, None, True),
            ("sampleSize", "sampleSize", RiskEvidenceSynthesisSampleSize, False, None, False),
            ("riskEstimate", "riskEstimate", RiskEvidenceSynthesisRiskEstimate, False, None, False),
            ("certainty", "certainty", RiskEvidenceSynthesisCertainty, True, None, False),
        ])
        return js


from . import backboneelement

class RiskEvidenceSynthesisCertainty(backboneelement.BackboneElement):
    """ How certain is the risk.
    
    A description of the certainty of the risk estimate.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['rating'] = """A rating of the certainty of the effect estimate."""
    _attribute_docstrings['note'] = """Used for footnotes or explanatory notes."""
    _attribute_docstrings['certaintySubcomponent'] = """A component that contributes to the overall certainty."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['rating'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/evidence-quality',
        'restricted_to': ['high', 'moderate', 'low', 'very-low'],
        'binding_strength': 'extensible',
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
        
        self.rating = None
        """ A rating of the certainty of the effect estimate.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.note = None
        """ Used for footnotes or explanatory notes.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        self.certaintySubcomponent = None
        """ A component that contributes to the overall certainty.
        List of `RiskEvidenceSynthesisCertaintyCertaintySubcomponent` items (represented as `dict` in JSON). """
        
        super(RiskEvidenceSynthesisCertainty, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(RiskEvidenceSynthesisCertainty, self).elementProperties()
        js.extend([
            ("rating", "rating", codeableconcept.CodeableConcept, True, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
            ("certaintySubcomponent", "certaintySubcomponent", RiskEvidenceSynthesisCertaintyCertaintySubcomponent, True, None, False),
        ])
        return js


class RiskEvidenceSynthesisCertaintyCertaintySubcomponent(backboneelement.BackboneElement):
    """ A component that contributes to the overall certainty.
    
    A description of a component of the overall certainty.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """None"""
    _attribute_docstrings['rating'] = """A rating of a subcomponent of rating certainty."""
    _attribute_docstrings['note'] = """Used for footnotes or explanatory notes."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/certainty-subcomponent-type',
        'restricted_to': ['RiskOfBias', 'Inconsistency', 'Indirectness', 'Imprecision', 'PublicationBias', 'DoseResponseGradient', 'PlausibleConfounding', 'LargeEffect'],
        'binding_strength': 'extensible',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['rating'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/certainty-subcomponent-rating',
        'restricted_to': ['no-change', 'downcode1', 'downcode2', 'downcode3', 'upcode1', 'upcode2', 'no-concern', 'serious-concern', 'critical-concern', 'present', 'absent'],
        'binding_strength': 'extensible',
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
        
        self.type = None
        """ None.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.rating = None
        """ A rating of a subcomponent of rating certainty.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.note = None
        """ Used for footnotes or explanatory notes.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        super(RiskEvidenceSynthesisCertaintyCertaintySubcomponent, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(RiskEvidenceSynthesisCertaintyCertaintySubcomponent, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("rating", "rating", codeableconcept.CodeableConcept, True, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
        ])
        return js


class RiskEvidenceSynthesisRiskEstimate(backboneelement.BackboneElement):
    """ What was the estimated risk.
    
    The estimated risk of the outcome.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['description'] = """Description of risk estimate."""
    _attribute_docstrings['type'] = """Examples include proportion and mean."""
    _attribute_docstrings['value'] = """Point estimate."""
    _attribute_docstrings['unitOfMeasure'] = """What unit is the outcome described in?."""
    _attribute_docstrings['denominatorCount'] = """Sample size for group measured."""
    _attribute_docstrings['numeratorCount'] = """Number with the outcome."""
    _attribute_docstrings['precisionEstimate'] = """How precise the estimate is."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/risk-estimate-type',
        'restricted_to': ['proportion', 'derivedProportion', 'mean', 'median', 'count', 'descriptive'],
        'binding_strength': 'extensible',
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
        
        self.description = None
        """ Description of risk estimate.
        Type `str`. """
        
        self.type = None
        """ Examples include proportion and mean.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.value = None
        """ Point estimate.
        Type `float`. """
        
        self.unitOfMeasure = None
        """ What unit is the outcome described in?.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.denominatorCount = None
        """ Sample size for group measured.
        Type `int`. """
        
        self.numeratorCount = None
        """ Number with the outcome.
        Type `int`. """
        
        self.precisionEstimate = None
        """ How precise the estimate is.
        List of `RiskEvidenceSynthesisRiskEstimatePrecisionEstimate` items (represented as `dict` in JSON). """
        
        super(RiskEvidenceSynthesisRiskEstimate, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(RiskEvidenceSynthesisRiskEstimate, self).elementProperties()
        js.extend([
            ("description", "description", str, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("value", "value", float, False, None, False),
            ("unitOfMeasure", "unitOfMeasure", codeableconcept.CodeableConcept, False, None, False),
            ("denominatorCount", "denominatorCount", int, False, None, False),
            ("numeratorCount", "numeratorCount", int, False, None, False),
            ("precisionEstimate", "precisionEstimate", RiskEvidenceSynthesisRiskEstimatePrecisionEstimate, True, None, False),
        ])
        return js


class RiskEvidenceSynthesisRiskEstimatePrecisionEstimate(backboneelement.BackboneElement):
    """ How precise the estimate is.
    
    A description of the precision of the estimate for the effect.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['type'] = """Examples include confidence interval and interquartile range."""
    _attribute_docstrings['level'] = """Level of confidence interval."""
    _attribute_docstrings['from_fhir'] = """Lower bound."""
    _attribute_docstrings['to'] = """Upper bound."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/precision-estimate-type',
        'restricted_to': ['CI', 'IQR', 'SD', 'SE'],
        'binding_strength': 'extensible',
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
        
        self.type = None
        """ Examples include confidence interval and interquartile range.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.level = None
        """ Level of confidence interval.
        Type `float`. """
        
        self.from_fhir = None
        """ Lower bound.
        Type `float`. """
        
        self.to = None
        """ Upper bound.
        Type `float`. """
        
        super(RiskEvidenceSynthesisRiskEstimatePrecisionEstimate, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(RiskEvidenceSynthesisRiskEstimatePrecisionEstimate, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("level", "level", float, False, None, False),
            ("from_fhir", "from", float, False, None, False),
            ("to", "to", float, False, None, False),
        ])
        return js


class RiskEvidenceSynthesisSampleSize(backboneelement.BackboneElement):
    """ What sample size was involved?.
    
    A description of the size of the sample involved in the synthesis.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['description'] = """Description of sample size."""
    _attribute_docstrings['numberOfStudies'] = """How many studies?."""
    _attribute_docstrings['numberOfParticipants'] = """How many participants?."""

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
        
        self.description = None
        """ Description of sample size.
        Type `str`. """
        
        self.numberOfStudies = None
        """ How many studies?.
        Type `int`. """
        
        self.numberOfParticipants = None
        """ How many participants?.
        Type `int`. """
        
        super(RiskEvidenceSynthesisSampleSize, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(RiskEvidenceSynthesisSampleSize, self).elementProperties()
        js.extend([
            ("description", "description", str, False, None, False),
            ("numberOfStudies", "numberOfStudies", int, False, None, False),
            ("numberOfParticipants", "numberOfParticipants", int, False, None, False),
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
    from . import contactdetail
except ImportError:
    contactdetail = sys.modules[__package__ + '.contactdetail']
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
    from . import period
except ImportError:
    period = sys.modules[__package__ + '.period']
try:
    from . import relatedartifact
except ImportError:
    relatedartifact = sys.modules[__package__ + '.relatedartifact']
try:
    from . import usagecontext
except ImportError:
    usagecontext = sys.modules[__package__ + '.usagecontext']
