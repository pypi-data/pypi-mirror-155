#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Questionnaire) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class Questionnaire(domainresource.DomainResource):
    """ A structured set of questions.
    
    A structured set of questions intended to guide the collection of answers
    from end-users. Questionnaires provide detailed control over order,
    presentation, phraseology and grouping to allow coherent, consistent data
    collection.
    """
    
    resource_type = "Questionnaire"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['url'] = """Canonical identifier for this questionnaire, represented as a URI (globally unique)."""
    _attribute_docstrings['identifier'] = """Additional identifier for the questionnaire."""
    _attribute_docstrings['version'] = """Business version of the questionnaire."""
    _attribute_docstrings['name'] = """Name for this questionnaire (computer friendly)."""
    _attribute_docstrings['title'] = """Name for this questionnaire (human friendly)."""
    _attribute_docstrings['derivedFrom'] = """Instantiates protocol or definition."""
    _attribute_docstrings['status'] = """The status of this questionnaire. Enables tracking the life-cycle of the content."""
    _attribute_docstrings['experimental'] = """For testing purposes, not real usage."""
    _attribute_docstrings['subjectType'] = """The types of subjects that can be the subject of responses created for the questionnaire."""
    _attribute_docstrings['date'] = """Date last changed."""
    _attribute_docstrings['publisher'] = """Name of the publisher (organization or individual)."""
    _attribute_docstrings['contact'] = """Contact details for the publisher."""
    _attribute_docstrings['description'] = """Natural language description of the questionnaire."""
    _attribute_docstrings['useContext'] = """The context that the content is intended to support."""
    _attribute_docstrings['jurisdiction'] = """Intended jurisdiction for questionnaire (if applicable)."""
    _attribute_docstrings['purpose'] = """Why this questionnaire is defined."""
    _attribute_docstrings['copyright'] = """Use and/or publishing restrictions."""
    _attribute_docstrings['approvalDate'] = """When the questionnaire was approved by publisher."""
    _attribute_docstrings['lastReviewDate'] = """When the questionnaire was last reviewed."""
    _attribute_docstrings['effectivePeriod'] = """When the questionnaire is expected to be used."""
    _attribute_docstrings['code'] = """Concept that represents the overall questionnaire."""
    _attribute_docstrings['item'] = """Questions and sections within the Questionnaire."""

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
    _attribute_enums['subjectType'] = {
        'url': 'http://hl7.org/fhir/resource-types',
        'restricted_to': ['Account', 'ActivityDefinition', 'AdverseEvent', 'AllergyIntolerance', 'Appointment', 'AppointmentResponse', 'AuditEvent', 'Basic', 'Binary', 'BiologicallyDerivedProduct', 'BodyStructure', 'Bundle', 'CapabilityStatement', 'CarePlan', 'CareTeam', 'CatalogEntry', 'ChargeItem', 'ChargeItemDefinition', 'Claim', 'ClaimResponse', 'ClinicalImpression', 'CodeSystem', 'Communication', 'CommunicationRequest', 'CompartmentDefinition', 'Composition', 'ConceptMap', 'Condition', 'Consent', 'Contract', 'Coverage', 'CoverageEligibilityRequest', 'CoverageEligibilityResponse', 'DetectedIssue', 'Device', 'DeviceDefinition', 'DeviceMetric', 'DeviceRequest', 'DeviceUseStatement', 'DiagnosticReport', 'DocumentManifest', 'DocumentReference', 'DomainResource', 'EffectEvidenceSynthesis', 'Encounter', 'Endpoint', 'EnrollmentRequest', 'EnrollmentResponse', 'EpisodeOfCare', 'EventDefinition', 'Evidence', 'EvidenceVariable', 'ExampleScenario', 'ExplanationOfBenefit', 'FamilyMemberHistory', 'Flag', 'Goal', 'GraphDefinition', 'Group', 'GuidanceResponse', 'HealthcareService', 'ImagingStudy', 'Immunization', 'ImmunizationEvaluation', 'ImmunizationRecommendation', 'ImplementationGuide', 'InsurancePlan', 'Invoice', 'Library', 'Linkage', 'List', 'Location', 'Measure', 'MeasureReport', 'Media', 'Medication', 'MedicationAdministration', 'MedicationDispense', 'MedicationKnowledge', 'MedicationRequest', 'MedicationStatement', 'MedicinalProduct', 'MedicinalProductAuthorization', 'MedicinalProductContraindication', 'MedicinalProductIndication', 'MedicinalProductIngredient', 'MedicinalProductInteraction', 'MedicinalProductManufactured', 'MedicinalProductPackaged', 'MedicinalProductPharmaceutical', 'MedicinalProductUndesirableEffect', 'MessageDefinition', 'MessageHeader', 'MolecularSequence', 'NamingSystem', 'NutritionOrder', 'Observation', 'ObservationDefinition', 'OperationDefinition', 'OperationOutcome', 'Organization', 'OrganizationAffiliation', 'Parameters', 'Patient', 'PaymentNotice', 'PaymentReconciliation', 'Person', 'PlanDefinition', 'Practitioner', 'PractitionerRole', 'Procedure', 'Provenance', 'Questionnaire', 'QuestionnaireResponse', 'RelatedPerson', 'RequestGroup', 'ResearchDefinition', 'ResearchElementDefinition', 'ResearchStudy', 'ResearchSubject', 'Resource', 'RiskAssessment', 'RiskEvidenceSynthesis', 'Schedule', 'SearchParameter', 'ServiceRequest', 'Slot', 'Specimen', 'SpecimenDefinition', 'StructureDefinition', 'StructureMap', 'Subscription', 'Substance', 'SubstanceNucleicAcid', 'SubstancePolymer', 'SubstanceProtein', 'SubstanceReferenceInformation', 'SubstanceSourceMaterial', 'SubstanceSpecification', 'SupplyDelivery', 'SupplyRequest', 'Task', 'TerminologyCapabilities', 'TestReport', 'TestScript', 'ValueSet', 'VerificationResult', 'VisionPrescription'],
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
        
        self.url = None
        """ Canonical identifier for this questionnaire, represented as a URI
        (globally unique).
        Type `str`. """
        
        self.identifier = None
        """ Additional identifier for the questionnaire.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.version = None
        """ Business version of the questionnaire.
        Type `str`. """
        
        self.name = None
        """ Name for this questionnaire (computer friendly).
        Type `str`. """
        
        self.title = None
        """ Name for this questionnaire (human friendly).
        Type `str`. """
        
        self.derivedFrom = None
        """ Instantiates protocol or definition.
        List of `str` items. """
        
        self.status = None
        """ The status of this questionnaire. Enables tracking the life-cycle
        of the content.
        Type `str`. """
        
        self.experimental = None
        """ For testing purposes, not real usage.
        Type `bool`. """
        
        self.subjectType = None
        """ The types of subjects that can be the subject of responses created
        for the questionnaire.
        List of `str` items. """
        
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
        """ Natural language description of the questionnaire.
        Type `str`. """
        
        self.useContext = None
        """ The context that the content is intended to support.
        List of `UsageContext` items (represented as `dict` in JSON). """
        
        self.jurisdiction = None
        """ Intended jurisdiction for questionnaire (if applicable).
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.purpose = None
        """ Why this questionnaire is defined.
        Type `str`. """
        
        self.copyright = None
        """ Use and/or publishing restrictions.
        Type `str`. """
        
        self.approvalDate = None
        """ When the questionnaire was approved by publisher.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.lastReviewDate = None
        """ When the questionnaire was last reviewed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.effectivePeriod = None
        """ When the questionnaire is expected to be used.
        Type `Period` (represented as `dict` in JSON). """
        
        self.code = None
        """ Concept that represents the overall questionnaire.
        List of `Coding` items (represented as `dict` in JSON). """
        
        self.item = None
        """ Questions and sections within the Questionnaire.
        List of `QuestionnaireItem` items (represented as `dict` in JSON). """
        
        super(Questionnaire, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Questionnaire, self).elementProperties()
        js.extend([
            ("url", "url", str, False, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("version", "version", str, False, None, False),
            ("name", "name", str, False, None, False),
            ("title", "title", str, False, None, False),
            ("derivedFrom", "derivedFrom", str, True, None, False),
            ("status", "status", str, False, None, True),
            ("experimental", "experimental", bool, False, None, False),
            ("subjectType", "subjectType", str, True, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("publisher", "publisher", str, False, None, False),
            ("contact", "contact", contactdetail.ContactDetail, True, None, False),
            ("description", "description", str, False, None, False),
            ("useContext", "useContext", usagecontext.UsageContext, True, None, False),
            ("jurisdiction", "jurisdiction", codeableconcept.CodeableConcept, True, None, False),
            ("purpose", "purpose", str, False, None, False),
            ("copyright", "copyright", str, False, None, False),
            ("approvalDate", "approvalDate", fhirdate.FHIRDate, False, None, False),
            ("lastReviewDate", "lastReviewDate", fhirdate.FHIRDate, False, None, False),
            ("effectivePeriod", "effectivePeriod", period.Period, False, None, False),
            ("code", "code", coding.Coding, True, None, False),
            ("item", "item", QuestionnaireItem, True, None, False),
        ])
        return js


from . import backboneelement

class QuestionnaireItem(backboneelement.BackboneElement):
    """ Questions and sections within the Questionnaire.
    
    A particular question, question grouping or display text that is part of
    the questionnaire.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['linkId'] = """Unique id for item in questionnaire."""
    _attribute_docstrings['definition'] = """ElementDefinition - details for the item."""
    _attribute_docstrings['code'] = """Corresponding concept for this item in a terminology."""
    _attribute_docstrings['prefix'] = """E.g. "1(a)", "2.5.3"."""
    _attribute_docstrings['text'] = """Primary text for the item."""
    _attribute_docstrings['type'] = """The type of questionnaire item this is - whether text for display, a grouping of other items or a particular type of data to be captured (string, integer, coded choice, etc.)."""
    _attribute_docstrings['enableWhen'] = """Only allow data when."""
    _attribute_docstrings['enableBehavior'] = """Controls how multiple enableWhen values are interpreted -  whether all or any must be true."""
    _attribute_docstrings['required'] = """Whether the item must be included in data results."""
    _attribute_docstrings['repeats'] = """Whether the item may repeat."""
    _attribute_docstrings['readOnly'] = """Don't allow human editing."""
    _attribute_docstrings['maxLength'] = """No more than this many characters."""
    _attribute_docstrings['answerValueSet'] = """Valueset containing permitted answers."""
    _attribute_docstrings['answerOption'] = """Permitted answer."""
    _attribute_docstrings['initial'] = """Initial value(s) when item is first rendered."""
    _attribute_docstrings['item'] = """Nested questionnaire items."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['type'] = {
        'url': 'http://hl7.org/fhir/item-type',
        'restricted_to': ['group', 'display', 'question', 'boolean', 'decimal', 'integer', 'date', 'dateTime', 'time', 'string', 'text', 'url', 'choice', 'open-choice', 'attachment', 'reference', 'quantity'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['enableBehavior'] = {
        'url': 'http://hl7.org/fhir/questionnaire-enable-behavior',
        'restricted_to': ['all', 'any'],
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
        
        self.linkId = None
        """ Unique id for item in questionnaire.
        Type `str`. """
        
        self.definition = None
        """ ElementDefinition - details for the item.
        Type `str`. """
        
        self.code = None
        """ Corresponding concept for this item in a terminology.
        List of `Coding` items (represented as `dict` in JSON). """
        
        self.prefix = None
        """ E.g. "1(a)", "2.5.3".
        Type `str`. """
        
        self.text = None
        """ Primary text for the item.
        Type `str`. """
        
        self.type = None
        """ The type of questionnaire item this is - whether text for display,
        a grouping of other items or a particular type of data to be
        captured (string, integer, coded choice, etc.).
        Type `str`. """
        
        self.enableWhen = None
        """ Only allow data when.
        List of `QuestionnaireItemEnableWhen` items (represented as `dict` in JSON). """
        
        self.enableBehavior = None
        """ Controls how multiple enableWhen values are interpreted -  whether
        all or any must be true.
        Type `str`. """
        
        self.required = None
        """ Whether the item must be included in data results.
        Type `bool`. """
        
        self.repeats = None
        """ Whether the item may repeat.
        Type `bool`. """
        
        self.readOnly = None
        """ Don't allow human editing.
        Type `bool`. """
        
        self.maxLength = None
        """ No more than this many characters.
        Type `int`. """
        
        self.answerValueSet = None
        """ Valueset containing permitted answers.
        Type `str`. """
        
        self.answerOption = None
        """ Permitted answer.
        List of `QuestionnaireItemAnswerOption` items (represented as `dict` in JSON). """
        
        self.initial = None
        """ Initial value(s) when item is first rendered.
        List of `QuestionnaireItemInitial` items (represented as `dict` in JSON). """
        
        self.item = None
        """ Nested questionnaire items.
        List of `QuestionnaireItem` items (represented as `dict` in JSON). """
        
        super(QuestionnaireItem, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(QuestionnaireItem, self).elementProperties()
        js.extend([
            ("linkId", "linkId", str, False, None, True),
            ("definition", "definition", str, False, None, False),
            ("code", "code", coding.Coding, True, None, False),
            ("prefix", "prefix", str, False, None, False),
            ("text", "text", str, False, None, False),
            ("type", "type", str, False, None, True),
            ("enableWhen", "enableWhen", QuestionnaireItemEnableWhen, True, None, False),
            ("enableBehavior", "enableBehavior", str, False, None, False),
            ("required", "required", bool, False, None, False),
            ("repeats", "repeats", bool, False, None, False),
            ("readOnly", "readOnly", bool, False, None, False),
            ("maxLength", "maxLength", int, False, None, False),
            ("answerValueSet", "answerValueSet", str, False, None, False),
            ("answerOption", "answerOption", QuestionnaireItemAnswerOption, True, None, False),
            ("initial", "initial", QuestionnaireItemInitial, True, None, False),
            ("item", "item", QuestionnaireItem, True, None, False),
        ])
        return js


class QuestionnaireItemAnswerOption(backboneelement.BackboneElement):
    """ Permitted answer.
    
    One of the permitted answers for a "choice" or "open-choice" question.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['valueInteger'] = """Answer value."""
    _attribute_docstrings['valueDate'] = """Answer value."""
    _attribute_docstrings['valueTime'] = """Answer value."""
    _attribute_docstrings['valueString'] = """Answer value."""
    _attribute_docstrings['valueCoding'] = """Answer value."""
    _attribute_docstrings['valueReference'] = """Answer value."""
    _attribute_docstrings['initialSelected'] = """Whether option is selected by default."""

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
        
        self.valueInteger = None
        """ Answer value.
        Type `int`. """
        
        self.valueDate = None
        """ Answer value.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valueTime = None
        """ Answer value.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valueString = None
        """ Answer value.
        Type `str`. """
        
        self.valueCoding = None
        """ Answer value.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.valueReference = None
        """ Answer value.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        self.initialSelected = None
        """ Whether option is selected by default.
        Type `bool`. """
        
        super(QuestionnaireItemAnswerOption, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(QuestionnaireItemAnswerOption, self).elementProperties()
        js.extend([
            ("valueInteger", "valueInteger", int, False, "value", True),
            ("valueDate", "valueDate", fhirdate.FHIRDate, False, "value", True),
            ("valueTime", "valueTime", fhirdate.FHIRDate, False, "value", True),
            ("valueString", "valueString", str, False, "value", True),
            ("valueCoding", "valueCoding", coding.Coding, False, "value", True),
            ("valueReference", "valueReference", fhirreference.FHIRReference, False, "value", True),
            ("initialSelected", "initialSelected", bool, False, None, False),
        ])
        return js


class QuestionnaireItemEnableWhen(backboneelement.BackboneElement):
    """ Only allow data when.
    
    A constraint indicating that this item should only be enabled
    (displayed/allow answers to be captured) when the specified condition is
    true.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['question'] = """Question that determines whether item is enabled."""
    _attribute_docstrings['operator'] = """Specifies the criteria by which the question is enabled."""
    _attribute_docstrings['answerBoolean'] = """Value for question comparison based on operator."""
    _attribute_docstrings['answerDecimal'] = """Value for question comparison based on operator."""
    _attribute_docstrings['answerInteger'] = """Value for question comparison based on operator."""
    _attribute_docstrings['answerDate'] = """Value for question comparison based on operator."""
    _attribute_docstrings['answerDateTime'] = """Value for question comparison based on operator."""
    _attribute_docstrings['answerTime'] = """Value for question comparison based on operator."""
    _attribute_docstrings['answerString'] = """Value for question comparison based on operator."""
    _attribute_docstrings['answerCoding'] = """Value for question comparison based on operator."""
    _attribute_docstrings['answerQuantity'] = """Value for question comparison based on operator."""
    _attribute_docstrings['answerReference'] = """Value for question comparison based on operator."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['operator'] = {
        'url': 'http://hl7.org/fhir/questionnaire-enable-operator',
        'restricted_to': ['exists', '=', '!=', '>', '<', '>=', '<='],
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
        
        self.question = None
        """ Question that determines whether item is enabled.
        Type `str`. """
        
        self.operator = None
        """ Specifies the criteria by which the question is enabled.
        Type `str`. """
        
        self.answerBoolean = None
        """ Value for question comparison based on operator.
        Type `bool`. """
        
        self.answerDecimal = None
        """ Value for question comparison based on operator.
        Type `float`. """
        
        self.answerInteger = None
        """ Value for question comparison based on operator.
        Type `int`. """
        
        self.answerDate = None
        """ Value for question comparison based on operator.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.answerDateTime = None
        """ Value for question comparison based on operator.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.answerTime = None
        """ Value for question comparison based on operator.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.answerString = None
        """ Value for question comparison based on operator.
        Type `str`. """
        
        self.answerCoding = None
        """ Value for question comparison based on operator.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.answerQuantity = None
        """ Value for question comparison based on operator.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.answerReference = None
        """ Value for question comparison based on operator.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(QuestionnaireItemEnableWhen, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(QuestionnaireItemEnableWhen, self).elementProperties()
        js.extend([
            ("question", "question", str, False, None, True),
            ("operator", "operator", str, False, None, True),
            ("answerBoolean", "answerBoolean", bool, False, "answer", True),
            ("answerDecimal", "answerDecimal", float, False, "answer", True),
            ("answerInteger", "answerInteger", int, False, "answer", True),
            ("answerDate", "answerDate", fhirdate.FHIRDate, False, "answer", True),
            ("answerDateTime", "answerDateTime", fhirdate.FHIRDate, False, "answer", True),
            ("answerTime", "answerTime", fhirdate.FHIRDate, False, "answer", True),
            ("answerString", "answerString", str, False, "answer", True),
            ("answerCoding", "answerCoding", coding.Coding, False, "answer", True),
            ("answerQuantity", "answerQuantity", quantity.Quantity, False, "answer", True),
            ("answerReference", "answerReference", fhirreference.FHIRReference, False, "answer", True),
        ])
        return js


class QuestionnaireItemInitial(backboneelement.BackboneElement):
    """ Initial value(s) when item is first rendered.
    
    One or more values that should be pre-populated in the answer when
    initially rendering the questionnaire for user input.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['valueBoolean'] = """Actual value for initializing the question."""
    _attribute_docstrings['valueDecimal'] = """Actual value for initializing the question."""
    _attribute_docstrings['valueInteger'] = """Actual value for initializing the question."""
    _attribute_docstrings['valueDate'] = """Actual value for initializing the question."""
    _attribute_docstrings['valueDateTime'] = """Actual value for initializing the question."""
    _attribute_docstrings['valueTime'] = """Actual value for initializing the question."""
    _attribute_docstrings['valueString'] = """Actual value for initializing the question."""
    _attribute_docstrings['valueUri'] = """Actual value for initializing the question."""
    _attribute_docstrings['valueAttachment'] = """Actual value for initializing the question."""
    _attribute_docstrings['valueCoding'] = """Actual value for initializing the question."""
    _attribute_docstrings['valueQuantity'] = """Actual value for initializing the question."""
    _attribute_docstrings['valueReference'] = """Actual value for initializing the question."""

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
        """ Actual value for initializing the question.
        Type `bool`. """
        
        self.valueDecimal = None
        """ Actual value for initializing the question.
        Type `float`. """
        
        self.valueInteger = None
        """ Actual value for initializing the question.
        Type `int`. """
        
        self.valueDate = None
        """ Actual value for initializing the question.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valueDateTime = None
        """ Actual value for initializing the question.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valueTime = None
        """ Actual value for initializing the question.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.valueString = None
        """ Actual value for initializing the question.
        Type `str`. """
        
        self.valueUri = None
        """ Actual value for initializing the question.
        Type `str`. """
        
        self.valueAttachment = None
        """ Actual value for initializing the question.
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.valueCoding = None
        """ Actual value for initializing the question.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.valueQuantity = None
        """ Actual value for initializing the question.
        Type `Quantity` (represented as `dict` in JSON). """
        
        self.valueReference = None
        """ Actual value for initializing the question.
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(QuestionnaireItemInitial, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(QuestionnaireItemInitial, self).elementProperties()
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
    from . import coding
except ImportError:
    coding = sys.modules[__package__ + '.coding']
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
    from . import quantity
except ImportError:
    quantity = sys.modules[__package__ + '.quantity']
try:
    from . import usagecontext
except ImportError:
    usagecontext = sys.modules[__package__ + '.usagecontext']
