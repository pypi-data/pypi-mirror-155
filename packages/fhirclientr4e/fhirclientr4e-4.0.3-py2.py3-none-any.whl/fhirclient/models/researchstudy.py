#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/ResearchStudy) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class ResearchStudy(domainresource.DomainResource):
    """ Investigation to increase healthcare-related patient-independent knowledge.
    
    A process where a researcher or organization plans and then executes a
    series of steps intended to increase the field of healthcare-related
    knowledge.  This includes studies of safety, efficacy, comparative
    effectiveness and other information about medications, devices, therapies
    and other interventional and investigative techniques.  A ResearchStudy
    involves the gathering of information about human or animal subjects.
    """
    
    resource_type = "ResearchStudy"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['identifier'] = """Business Identifier for study."""
    _attribute_docstrings['title'] = """Name for this study."""
    _attribute_docstrings['protocol'] = """Steps followed in executing study."""
    _attribute_docstrings['partOf'] = """Part of larger study."""
    _attribute_docstrings['status'] = """The current state of the study."""
    _attribute_docstrings['primaryPurposeType'] = """The type of study based upon the intent of the study's activities. A classification of the intent of the study."""
    _attribute_docstrings['phase'] = """The stage in the progression of a therapy from initial experimental use in humans in clinical trials to post-market evaluation."""
    _attribute_docstrings['category'] = """Classifications for the study."""
    _attribute_docstrings['focus'] = """Drugs, devices, etc. under study."""
    _attribute_docstrings['condition'] = """Condition being studied."""
    _attribute_docstrings['contact'] = """Contact details for the study."""
    _attribute_docstrings['relatedArtifact'] = """References and dependencies."""
    _attribute_docstrings['keyword'] = """Used to search for the study."""
    _attribute_docstrings['location'] = """Geographic region(s) for study."""
    _attribute_docstrings['description'] = """What this is study doing."""
    _attribute_docstrings['enrollment'] = """Inclusion & exclusion criteria."""
    _attribute_docstrings['period'] = """When the study began and ended."""
    _attribute_docstrings['sponsor'] = """Organization that initiates and is legally responsible for the study."""
    _attribute_docstrings['principalInvestigator'] = """Researcher who oversees multiple aspects of the study."""
    _attribute_docstrings['site'] = """Facility where study activities are conducted."""
    _attribute_docstrings['reasonStopped'] = """A description and/or code explaining the premature termination of the study."""
    _attribute_docstrings['note'] = """Comments made about the study."""
    _attribute_docstrings['arm'] = """Defined path through the study for a subject."""
    _attribute_docstrings['objective'] = """A goal for the study."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['status'] = {
        'url': 'http://hl7.org/fhir/research-study-status',
        'restricted_to': ['active', 'administratively-completed', 'approved', 'closed-to-accrual', 'closed-to-accrual-and-intervention', 'completed', 'disapproved', 'in-review', 'temporarily-closed-to-accrual', 'temporarily-closed-to-accrual-and-intervention', 'withdrawn'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['primaryPurposeType'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/research-study-prim-purp-type',
        'restricted_to': ['treatment', 'prevention', 'diagnostic', 'supportive-care', 'screening', 'health-services-research', 'basic-science', 'device-feasibility'],
        'binding_strength': 'extensible',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['phase'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/research-study-phase',
        'restricted_to': ['n-a', 'early-phase-1', 'phase-1', 'phase-1-phase-2', 'phase-2', 'phase-2-phase-3', 'phase-3', 'phase-4'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }
    _attribute_enums['reasonStopped'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/research-study-reason-stopped',
        'restricted_to': ['accrual-goal-met', 'closed-due-to-toxicity', 'closed-due-to-lack-of-study-progress', 'temporarily-closed-per-study-design'],
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
        """ Business Identifier for study.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.title = None
        """ Name for this study.
        Type `str`. """
        
        self.protocol = None
        """ Steps followed in executing study.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.partOf = None
        """ Part of larger study.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.status = None
        """ The current state of the study.
        Type `str`. """
        
        self.primaryPurposeType = None
        """ The type of study based upon the intent of the study's activities.
        A classification of the intent of the study.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.phase = None
        """ The stage in the progression of a therapy from initial experimental
        use in humans in clinical trials to post-market evaluation.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.category = None
        """ Classifications for the study.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.focus = None
        """ Drugs, devices, etc. under study.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.condition = None
        """ Condition being studied.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.contact = None
        """ Contact details for the study.
        List of `ContactDetail` items (represented as `dict` in JSON). """
        
        self.relatedArtifact = None
        """ References and dependencies.
        List of `RelatedArtifact` items (represented as `dict` in JSON). """
        
        self.keyword = None
        """ Used to search for the study.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.location = None
        """ Geographic region(s) for study.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.description = None
        """ What this is study doing.
        Type `str`. """
        
        self.enrollment = None
        """ Inclusion & exclusion criteria.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.period = None
        """ When the study began and ended.
        Type `Period` (represented as `dict` in JSON). """
        
        self.sponsor = None
        """ Organization that initiates and is legally responsible for the
        study.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.principalInvestigator = None
        """ Researcher who oversees multiple aspects of the study.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.site = None
        """ Facility where study activities are conducted.
        List of `FHIRReference` items (represented as `dict` in JSON). """
        
        self.reasonStopped = None
        """ A description and/or code explaining the premature termination of
        the study.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.note = None
        """ Comments made about the study.
        List of `Annotation` items (represented as `dict` in JSON). """
        
        self.arm = None
        """ Defined path through the study for a subject.
        List of `ResearchStudyArm` items (represented as `dict` in JSON). """
        
        self.objective = None
        """ A goal for the study.
        List of `ResearchStudyObjective` items (represented as `dict` in JSON). """
        
        super(ResearchStudy, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ResearchStudy, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("title", "title", str, False, None, False),
            ("protocol", "protocol", fhirreference.FHIRReference, True, None, False),
            ("partOf", "partOf", fhirreference.FHIRReference, True, None, False),
            ("status", "status", str, False, None, True),
            ("primaryPurposeType", "primaryPurposeType", codeableconcept.CodeableConcept, False, None, False),
            ("phase", "phase", codeableconcept.CodeableConcept, False, None, False),
            ("category", "category", codeableconcept.CodeableConcept, True, None, False),
            ("focus", "focus", codeableconcept.CodeableConcept, True, None, False),
            ("condition", "condition", codeableconcept.CodeableConcept, True, None, False),
            ("contact", "contact", contactdetail.ContactDetail, True, None, False),
            ("relatedArtifact", "relatedArtifact", relatedartifact.RelatedArtifact, True, None, False),
            ("keyword", "keyword", codeableconcept.CodeableConcept, True, None, False),
            ("location", "location", codeableconcept.CodeableConcept, True, None, False),
            ("description", "description", str, False, None, False),
            ("enrollment", "enrollment", fhirreference.FHIRReference, True, None, False),
            ("period", "period", period.Period, False, None, False),
            ("sponsor", "sponsor", fhirreference.FHIRReference, False, None, False),
            ("principalInvestigator", "principalInvestigator", fhirreference.FHIRReference, False, None, False),
            ("site", "site", fhirreference.FHIRReference, True, None, False),
            ("reasonStopped", "reasonStopped", codeableconcept.CodeableConcept, False, None, False),
            ("note", "note", annotation.Annotation, True, None, False),
            ("arm", "arm", ResearchStudyArm, True, None, False),
            ("objective", "objective", ResearchStudyObjective, True, None, False),
        ])
        return js


from . import backboneelement

class ResearchStudyArm(backboneelement.BackboneElement):
    """ Defined path through the study for a subject.
    
    Describes an expected sequence of events for one of the participants of a
    study.  E.g. Exposure to drug A, wash-out, exposure to drug B, wash-out,
    follow-up.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['name'] = """Label for study arm."""
    _attribute_docstrings['type'] = """Categorization of study arm."""
    _attribute_docstrings['description'] = """Short explanation of study path."""

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
        """ Label for study arm.
        Type `str`. """
        
        self.type = None
        """ Categorization of study arm.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.description = None
        """ Short explanation of study path.
        Type `str`. """
        
        super(ResearchStudyArm, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ResearchStudyArm, self).elementProperties()
        js.extend([
            ("name", "name", str, False, None, True),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("description", "description", str, False, None, False),
        ])
        return js


class ResearchStudyObjective(backboneelement.BackboneElement):
    """ A goal for the study.
    
    A goal that the study is aiming to achieve in terms of a scientific
    question to be answered by the analysis of data collected during the study.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['name'] = """Label for the objective."""
    _attribute_docstrings['type'] = """The kind of study objective."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/research-study-objective-type',
        'restricted_to': ['primary', 'secondary', 'exploratory'],
        'binding_strength': 'preferred',
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
        
        self.name = None
        """ Label for the objective.
        Type `str`. """
        
        self.type = None
        """ The kind of study objective.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(ResearchStudyObjective, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ResearchStudyObjective, self).elementProperties()
        js.extend([
            ("name", "name", str, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
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
