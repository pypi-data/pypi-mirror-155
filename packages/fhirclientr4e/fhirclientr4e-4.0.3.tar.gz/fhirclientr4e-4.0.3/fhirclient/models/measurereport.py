#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/MeasureReport) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class MeasureReport(domainresource.DomainResource):
    """ Results of a measure evaluation.
    
    The MeasureReport resource contains the results of the calculation of a
    measure; and optionally a reference to the resources involved in that
    calculation.
    """
    
    resource_type = "MeasureReport"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Additional identifier for the MeasureReport."""
    _attribute_docstrings['status'] = """The MeasureReport status. No data will be available until the MeasureReport status is complete."""
    _attribute_docstrings['type'] = """The type of measure report. This may be an individual report, which provides the score for the measure for an individual member of the population; a subject-listing, which returns the list of members that meet the various criteria in the measure; a summary report, which returns a population count for each of the criteria in the measure; or a data-collection, which enables the MeasureReport to be used to exchange the data-of-interest for a quality measure."""
    _attribute_docstrings['measure'] = """What measure was calculated."""
    _attribute_docstrings['subject'] = """What individual(s) the report is for."""
    _attribute_docstrings['date'] = """When the report was generated."""
    _attribute_docstrings['reporter'] = """Who is reporting the data."""
    _attribute_docstrings['period'] = """What period the report covers."""
    _attribute_docstrings['improvementNotation'] = """Whether improvement in the measure is noted by an increase or decrease in the measure score."""
    _attribute_docstrings['group'] = """Measure results for each group."""
    _attribute_docstrings['evaluatedResource'] = """What data was used to calculate the measure score."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/measure-report-status',
        'restricted_to': ['complete', 'pending', 'error'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['type'] = {
        'url': 'http://hl7.org/fhir/measure-report-type',
        'restricted_to': ['individual', 'subject-list', 'summary', 'data-collection'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['improvementNotation'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/measure-improvement-notation',
        'restricted_to': ['increase', 'decrease'],
        'binding_strength': 'required',
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
        """ Additional identifier for the MeasureReport.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.status = None
        """ The MeasureReport status. No data will be available until the
        MeasureReport status is complete.
        Type `str`. """
        
        self.type = None
        """ The type of measure report. This may be an individual report, which
        provides the score for the measure for an individual member of the
        population; a subject-listing, which returns the list of members
        that meet the various criteria in the measure; a summary report,
        which returns a population count for each of the criteria in the
        measure; or a data-collection, which enables the MeasureReport to
        be used to exchange the data-of-interest for a quality measure.
        Type `str`. """
        
        self.measure = None
        """ What measure was calculated.
        Type `str`. """
        
        self.subject = None
        """ What individual(s) the report is for.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.date = None
        """ When the report was generated.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.reporter = None
        """ Who is reporting the data.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.period = None
        """ What period the report covers.
        Type `Period` (represented as `dict` in JSON). """
        
        self.improvementNotation = None
        """ Whether improvement in the measure is noted by an increase or
        decrease in the measure score.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.group = None
        """ Measure results for each group.
        List of `MeasureReportGroup` items (represented as `dict` in JSON). """
        
        self.evaluatedResource = None
        """ What data was used to calculate the measure score.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        super(MeasureReport, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MeasureReport, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("status", "status", str, False, None, True),
            ("type", "type", str, False, None, True),
            ("measure", "measure", str, False, None, True),
            ("subject", "subject", fhirreference.FHIRReference, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("reporter", "reporter", fhirreference.FHIRReference, False, None, False),
            ("period", "period", period.Period, False, None, True),
            ("improvementNotation", "improvementNotation", codeableconcept.CodeableConcept, False, None, False),
            ("group", "group", MeasureReportGroup, True, None, False),
            ("evaluatedResource", "evaluatedResource", fhirreference.FHIRReference, True, None, False),
        ])
        return js


from . import backboneelement

class MeasureReportGroup(backboneelement.BackboneElement):
    """ Measure results for each group.
    
    The results of the calculation, one for each population group in the
    measure.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """Meaning of the group."""
    _attribute_docstrings['population'] = """The populations in the group."""
    _attribute_docstrings['measureScore'] = """What score this group achieved."""
    _attribute_docstrings['stratifier'] = """Stratification results."""

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
        """ Meaning of the group.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.population = None
        """ The populations in the group.
        List of `MeasureReportGroupPopulation` items (represented as `dict` in JSON). """
        
        self.measureScore = None
        """ What score this group achieved.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.stratifier = None
        """ Stratification results.
        List of `MeasureReportGroupStratifier` items (represented as `dict` in JSON). """
        
        super(MeasureReportGroup, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MeasureReportGroup, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("population", "population", MeasureReportGroupPopulation, True, None, False),
            ("measureScore", "measureScore", quantity.Quantity, False, None, False),
            ("stratifier", "stratifier", MeasureReportGroupStratifier, True, None, False),
        ])
        return js


class MeasureReportGroupPopulation(backboneelement.BackboneElement):
    """ The populations in the group.
    
    The populations that make up the population group, one for each type of
    population appropriate for the measure.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """The type of the population."""
    _attribute_docstrings['count'] = """Size of the population."""
    _attribute_docstrings['subjectResults'] = """For subject-list reports, the subject results in this population."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['code'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/measure-population',
        'restricted_to': ['initial-population', 'numerator', 'numerator-exclusion', 'denominator', 'denominator-exclusion', 'denominator-exception', 'measure-population', 'measure-population-exclusion', 'measure-observation'],
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
        
        self.code = None
        """ The type of the population.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.count = None
        """ Size of the population.
        Type `int`. """
        
        self.subjectResults = None
        """ For subject-list reports, the subject results in this population.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(MeasureReportGroupPopulation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MeasureReportGroupPopulation, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("count", "count", int, False, None, False),
            ("subjectResults", "subjectResults", fhirreference.FHIRReference, False, None, False),
        ])
        return js


class MeasureReportGroupStratifier(backboneelement.BackboneElement):
    """ Stratification results.
    
    When a measure includes multiple stratifiers, there will be a stratifier
    group for each stratifier defined by the measure.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """What stratifier of the group."""
    _attribute_docstrings['stratum'] = """Stratum results, one for each unique value, or set of values, in the stratifier, or stratifier components."""

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
        """ What stratifier of the group.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.stratum = None
        """ Stratum results, one for each unique value, or set of values, in
        the stratifier, or stratifier components.
        List of `MeasureReportGroupStratifierStratum` items (represented as `dict` in JSON). """
        
        super(MeasureReportGroupStratifier, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MeasureReportGroupStratifier, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, True, None, False),
            ("stratum", "stratum", MeasureReportGroupStratifierStratum, True, None, False),
        ])
        return js


class MeasureReportGroupStratifierStratum(backboneelement.BackboneElement):
    """ Stratum results, one for each unique value, or set of values, in the
    stratifier, or stratifier components.
    
    This element contains the results for a single stratum within the
    stratifier. For example, when stratifying on administrative gender, there
    will be four strata, one for each possible gender value.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['value'] = """The stratum value, e.g. male."""
    _attribute_docstrings['component'] = """Stratifier component values."""
    _attribute_docstrings['population'] = """Population results in this stratum."""
    _attribute_docstrings['measureScore'] = """What score this stratum achieved."""

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
        
        self.value = None
        """ The stratum value, e.g. male.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.component = None
        """ Stratifier component values.
        List of `MeasureReportGroupStratifierStratumComponent` items (represented as `dict` in JSON). """
        
        self.population = None
        """ Population results in this stratum.
        List of `MeasureReportGroupStratifierStratumPopulation` items (represented as `dict` in JSON). """
        
        self.measureScore = None
        """ What score this stratum achieved.
        Type `Quantity` (represented as `dict` in JSON). """
        
        super(MeasureReportGroupStratifierStratum, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MeasureReportGroupStratifierStratum, self).elementProperties()
        js.extend([
            ("value", "value", codeableconcept.CodeableConcept, False, None, False),
            ("component", "component", MeasureReportGroupStratifierStratumComponent, True, None, False),
            ("population", "population", MeasureReportGroupStratifierStratumPopulation, True, None, False),
            ("measureScore", "measureScore", quantity.Quantity, False, None, False),
        ])
        return js


class MeasureReportGroupStratifierStratumComponent(backboneelement.BackboneElement):
    """ Stratifier component values.
    
    A stratifier component value.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """What stratifier component of the group."""
    _attribute_docstrings['value'] = """The stratum component value, e.g. male."""

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
        """ What stratifier component of the group.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.value = None
        """ The stratum component value, e.g. male.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(MeasureReportGroupStratifierStratumComponent, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MeasureReportGroupStratifierStratumComponent, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, False, None, True),
            ("value", "value", codeableconcept.CodeableConcept, False, None, True),
        ])
        return js


class MeasureReportGroupStratifierStratumPopulation(backboneelement.BackboneElement):
    """ Population results in this stratum.
    
    The populations that make up the stratum, one for each type of population
    appropriate to the measure.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['code'] = """The type of the population."""
    _attribute_docstrings['count'] = """Size of the population."""
    _attribute_docstrings['subjectResults'] = """For subject-list reports, the subject results in this population."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['code'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/measure-population',
        'restricted_to': ['initial-population', 'numerator', 'numerator-exclusion', 'denominator', 'denominator-exclusion', 'denominator-exception', 'measure-population', 'measure-population-exclusion', 'measure-observation'],
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
        
        self.code = None
        """ The type of the population.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.count = None
        """ Size of the population.
        Type `int`. """
        
        self.subjectResults = None
        """ For subject-list reports, the subject results in this population.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(MeasureReportGroupStratifierStratumPopulation, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(MeasureReportGroupStratifierStratumPopulation, self).elementProperties()
        js.extend([
            ("code", "code", codeableconcept.CodeableConcept, False, None, False),
            ("count", "count", int, False, None, False),
            ("subjectResults", "subjectResults", fhirreference.FHIRReference, False, None, False),
        ])
        return js


import sys
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
    from . import period
except ImportError:
    period = sys.modules[__package__ + '.period']
try:
    from . import quantity
except ImportError:
    quantity = sys.modules[__package__ + '.quantity']
