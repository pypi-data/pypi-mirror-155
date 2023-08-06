#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/EffectEvidenceSynthesis) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class EffectEvidenceSynthesis(domainresource.DomainResource):
    """ A quantified estimate of effect based on a body of evidence.
    
    The EffectEvidenceSynthesis resource describes the difference in an outcome
    between exposures states in a population where the effect estimate is
    derived from a combination of research studies.
    """
    
    resource_type = "EffectEvidenceSynthesis"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['url'] = """Canonical identifier for this effect evidence synthesis, represented as a URI (globally unique)."""
    _attribute_docstrings['identifier'] = """Additional identifier for the effect evidence synthesis."""
    _attribute_docstrings['version'] = """Business version of the effect evidence synthesis."""
    _attribute_docstrings['name'] = """Name for this effect evidence synthesis (computer friendly)."""
    _attribute_docstrings['title'] = """Name for this effect evidence synthesis (human friendly)."""
    _attribute_docstrings['status'] = """The status of this effect evidence synthesis. Enables tracking the life-cycle of the content."""
    _attribute_docstrings['date'] = """Date last changed."""
    _attribute_docstrings['publisher'] = """Name of the publisher (organization or individual)."""
    _attribute_docstrings['contact'] = """Contact details for the publisher."""
    _attribute_docstrings['description'] = """Natural language description of the effect evidence synthesis."""
    _attribute_docstrings['note'] = """Used for footnotes or explanatory notes."""
    _attribute_docstrings['useContext'] = """The context that the content is intended to support."""
    _attribute_docstrings['jurisdiction'] = """Intended jurisdiction for effect evidence synthesis (if applicable)."""
    _attribute_docstrings['copyright'] = """Use and/or publishing restrictions."""
    _attribute_docstrings['approvalDate'] = """When the effect evidence synthesis was approved by publisher."""
    _attribute_docstrings['lastReviewDate'] = """When the effect evidence synthesis was last reviewed."""
    _attribute_docstrings['effectivePeriod'] = """When the effect evidence synthesis is expected to be used."""
    _attribute_docstrings['topic'] = """Descriptive topics related to the content of the EffectEvidenceSynthesis. Topics provide a high-level categorization grouping types of EffectEvidenceSynthesiss that can be useful for filtering and searching."""
    _attribute_docstrings['author'] = """Who authored the content."""
    _attribute_docstrings['editor'] = """Who edited the content."""
    _attribute_docstrings['reviewer'] = """Who reviewed the content."""
    _attribute_docstrings['endorser'] = """Who endorsed the content."""
    _attribute_docstrings['relatedArtifact'] = """Additional documentation, citations, etc.."""
    _attribute_docstrings['synthesisType'] = """Type of synthesis eg meta-analysis."""
    _attribute_docstrings['studyType'] = """Type of study eg randomized trial."""
    _attribute_docstrings['population'] = """What population?."""
    _attribute_docstrings['exposure'] = """What exposure?."""
    _attribute_docstrings['exposureAlternative'] = """What comparison exposure?."""
    _attribute_docstrings['outcome'] = """What outcome?."""
    _attribute_docstrings['sampleSize'] = """What sample size was involved?."""
    _attribute_docstrings['resultsByExposure'] = """What was the result per exposure?."""
    _attribute_docstrings['effectEstimate'] = """What was the estimated effect."""
    _attribute_docstrings['certainty'] = """How certain is the effect."""

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
        """ Canonical identifier for this effect evidence synthesis,
        represented as a URI (globally unique).
        Type `str`. """
        
        self.identifier = None
        """ Additional identifier for the effect evidence synthesis.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.version = None
        """ Business version of the effect evidence synthesis.
        Type `str`. """
        
        self.name = None
        """ Name for this effect evidence synthesis (computer friendly).
        Type `str`. """
        
        self.title = None
        """ Name for this effect evidence synthesis (human friendly).
        Type `str`. """
        
        self.status = None
        """ The status of this effect evidence synthesis. Enables tracking the
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
        """ Natural language description of the effect evidence synthesis.
        Type `str`. """
        
        self.note = None
        """ Used for footnotes or explanatory notes.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for effect evidence synthesis (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.copyright = None
        """ Use and/or publishing restrictions.
        Type `str`. """
        
        self.approvalDate = None
        """ When the effect evidence synthesis was approved by publisher.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.lastReviewDate = None
        """ When the effect evidence synthesis was last reviewed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.effectivePeriod = None
        """ When the effect evidence synthesis is expected to be used.
        Type `Period` (represented as `dict` in JSON). """
        
        self.topic = None
        """ Descriptive topics related to the content of the
        EffectEvidenceSynthesis. Topics provide a high-level categorization
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
        
        self.exposureAlternative = None
        """ What comparison exposure?.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.outcome = None
        """ What outcome?.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.sampleSize = None
        """ What sample size was involved?.
        Type `EffectEvidenceSynthesisSampleSize` (represented as `dict` in JSON). """
        
        self.resultsByExposure = None
        """ What was the result per exposure?.
        List of `EffectEvidenceSynthesisResultsByExposure` items (represented as `dict` in JSON). """
        
        self.effectEstimate = None
        """ What was the estimated effect.
        List of `EffectEvidenceSynthesisEffectEstimate` items (represented as `dict` in JSON). """
        
        self.certainty = None
        """ How certain is the effect.
        List of `EffectEvidenceSynthesisCertainty` items (represented as `dict` in JSON). """
        
        super(EffectEvidenceSynthesis, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(EffectEvidenceSynthesis, self).elementProperties()
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
            ("exposure", "exposure", fhirreference.FHIRReference, False, None, True),
            ("exposureAlternative", "exposureAlternative", fhirreference.FHIRReference, False, None, True),
            ("outcome", "outcome", fhirreference.FHIRReference, False, None, True),
            ("sampleSize", "sampleSize", EffectEvidenceSynthesisSampleSize, False, None, False),
            ("resultsByExposure", "resultsByExposure", EffectEvidenceSynthesisResultsByExposure, True, None, False),
            ("effectEstimate", "effectEstimate", EffectEvidenceSynthesisEffectEstimate, True, None, False),
            ("certainty", "certainty", EffectEvidenceSynthesisCertainty, True, None, False),
        ])
        return js


from . import backboneelement

class EffectEvidenceSynthesisCertainty(backboneelement.BackboneElement):
    """ How certain is the effect.
    
    A description of the certainty of the effect estimate.
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
        List of `EffectEvidenceSynthesisCertaintyCertaintySubcomponent` items (represented as `dict` in JSON). """
        
        super(EffectEvidenceSynthesisCertainty, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(EffectEvidenceSynthesisCertainty, self).elementProperties()
        js.extend([
            ("rating", "rating", codeableconcept.CodeableConcept, True, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
            ("certaintySubcomponent", "certaintySubcomponent", EffectEvidenceSynthesisCertaintyCertaintySubcomponent, True, None, False),
        ])
        return js


class EffectEvidenceSynthesisCertaintyCertaintySubcomponent(backboneelement.BackboneElement):
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
        
        super(EffectEvidenceSynthesisCertaintyCertaintySubcomponent, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(EffectEvidenceSynthesisCertaintyCertaintySubcomponent, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("rating", "rating", codeableconcept.CodeableConcept, True, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
        ])
        return js


class EffectEvidenceSynthesisEffectEstimate(backboneelement.BackboneElement):
    """ What was the estimated effect.
    
    The estimated effect of the exposure variant.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['description'] = """Description of effect estimate."""
    _attribute_docstrings['type'] = """Examples include relative risk and mean difference."""
    _attribute_docstrings['variantState'] = """Used to define variant exposure states such as low-risk state."""
    _attribute_docstrings['value'] = """Point estimate."""
    _attribute_docstrings['unitOfMeasure'] = """What unit is the outcome described in?."""
    _attribute_docstrings['precisionEstimate'] = """How precise the estimate is."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/effect-estimate-type',
        'restricted_to': ['relative-RR', 'relative-OR', 'relative-HR', 'absolute-ARD', 'absolute-MeanDiff', 'absolute-SMD', 'absolute-MedianDiff'],
        'binding_strength': 'extensible',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['variantState'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/evidence-variant-state',
        'restricted_to': ['low-risk', 'medium-risk', 'high-risk'],
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
        """ Description of effect estimate.
        Type `str`. """
        
        self.type = None
        """ Examples include relative risk and mean difference.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.variantState = None
        """ Used to define variant exposure states such as low-risk state.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.value = None
        """ Point estimate.
        Type `float`. """
        
        self.unitOfMeasure = None
        """ What unit is the outcome described in?.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.precisionEstimate = None
        """ How precise the estimate is.
        List of `EffectEvidenceSynthesisEffectEstimatePrecisionEstimate` items (represented as `dict` in JSON). """
        
        super(EffectEvidenceSynthesisEffectEstimate, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(EffectEvidenceSynthesisEffectEstimate, self).elementProperties()
        js.extend([
            ("description", "description", str, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("variantState", "variantState", codeableconcept.CodeableConcept, False, None, False),
            ("value", "value", float, False, None, False),
            ("unitOfMeasure", "unitOfMeasure", codeableconcept.CodeableConcept, False, None, False),
            ("precisionEstimate", "precisionEstimate", EffectEvidenceSynthesisEffectEstimatePrecisionEstimate, True, None, False),
        ])
        return js


class EffectEvidenceSynthesisEffectEstimatePrecisionEstimate(backboneelement.BackboneElement):
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
        
        super(EffectEvidenceSynthesisEffectEstimatePrecisionEstimate, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(EffectEvidenceSynthesisEffectEstimatePrecisionEstimate, self).elementProperties()
        js.extend([
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("level", "level", float, False, None, False),
            ("from_fhir", "from", float, False, None, False),
            ("to", "to", float, False, None, False),
        ])
        return js


class EffectEvidenceSynthesisResultsByExposure(backboneelement.BackboneElement):
    """ What was the result per exposure?.
    
    A description of the results for each exposure considered in the effect
    estimate.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['description'] = """Description of results by exposure."""
    _attribute_docstrings['exposureState'] = """Whether these results are for the exposure state or alternative exposure state."""
    _attribute_docstrings['variantState'] = """Used to define variant exposure states such as low-risk state."""
    _attribute_docstrings['riskEvidenceSynthesis'] = """Risk evidence synthesis."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['exposureState'] = {
        'url': 'http://hl7.org/fhir/exposure-state',
        'restricted_to': ['exposure', 'exposure-alternative'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['variantState'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/evidence-variant-state',
        'restricted_to': ['low-risk', 'medium-risk', 'high-risk'],
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
        """ Description of results by exposure.
        Type `str`. """
        
        self.exposureState = None
        """ Whether these results are for the exposure state or alternative
        exposure state.
        Type `str`. """
        
        self.variantState = None
        """ Used to define variant exposure states such as low-risk state.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.riskEvidenceSynthesis = None
        """ Risk evidence synthesis.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(EffectEvidenceSynthesisResultsByExposure, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(EffectEvidenceSynthesisResultsByExposure, self).elementProperties()
        js.extend([
            ("description", "description", str, False, None, False),
            ("exposureState", "exposureState", str, False, None, False),
            ("variantState", "variantState", codeableconcept.CodeableConcept, False, None, False),
            ("riskEvidenceSynthesis", "riskEvidenceSynthesis", fhirreference.FHIRReference, False, None, True),
        ])
        return js


class EffectEvidenceSynthesisSampleSize(backboneelement.BackboneElement):
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
        
        super(EffectEvidenceSynthesisSampleSize, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(EffectEvidenceSynthesisSampleSize, self).elementProperties()
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
