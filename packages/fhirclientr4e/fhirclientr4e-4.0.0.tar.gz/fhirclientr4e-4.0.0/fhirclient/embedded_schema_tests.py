# -*- coding: utf-8 -*-

import unittest
from fhirclient.models.researchstudy import ResearchStudy
from fhirclient.models.fhirabstractbase import FHIRValidationError
from fhirclient.models.condition import Condition


class TestResearchStudy(unittest.TestCase):
    """Ensure customizations we've added work."""

    def testNoParameters(self):
        """Should be able to create ResearchStudy without any parameters."""
        rs = ResearchStudy()
        assert rs, self.testNoParameters.__doc__

    def testEmptyDict(self):
        """Should not be able to create ResearchStudy empty dict."""
        with self.assertRaises(FHIRValidationError):
            ResearchStudy({})
        assert True, self.testEmptyDict.__doc__

    def testDictWithBadElement(self):
        """Should not be able to create ResearchStudy dict with unknown element."""
        with self.assertRaises(FHIRValidationError) as err:
            ResearchStudy({'foo': 'bar'})
        assert 'Superfluous entry "foo" in data' in str(err.exception), str(err.exception)

    def testDictWithBadValue(self):
        """Should not be able to create ResearchStudy dict with unknown value."""
        with self.assertRaises(FHIRValidationError) as err:
            ResearchStudy({'status': 'foo-bar'})
        expected_msg = 'Expecting property with required binding_strength "status" to be member of http://hl7.org/fhir/research-study-status is "foo-bar"'
        assert expected_msg in str(err.exception), self.testDictWithBadValue.__doc__
        #     assert expected_msg in str(err), self.testDictWithBadValue.__doc__

    def testDictWithBadElementGoodValue(self):
        """Should not be able to create ResearchStudy dict with extra unknown element ."""
        with self.assertRaises(FHIRValidationError) as err:
            ResearchStudy({'foo': 'bar', 'status': 'active'})
        assert 'Superfluous entry "foo" in data' in str(err.exception), self.testDictWithBadElementGoodValue.__doc__

    def testDictWithRequiredAttributes(self):
        """Should be able to create ResearchStudy dict required values."""
        rs = ResearchStudy({'status': 'active'})
        assert rs, self.testDictWithRequiredAttributes.__doc__
        assert rs.status == 'active'

    def testDictWithRequiredAttributesAndExampleCode(self):
        """Should be able to create ResearchStudy dict required values, and arbitrary value in example value set."""
        reason_stopped = {'coding': [{'code': 'foo-bar', 'system': 'my-system'}]}
        rs = ResearchStudy({'status': 'active', 'reasonStopped': reason_stopped})
        assert rs, self.testDictWithRequiredAttributesAndExampleCode.__doc__
        assert rs.status == 'active'
        assert rs.reasonStopped
        assert rs.reasonStopped.coding[0].code == 'foo-bar', rs.reasonStopped.as_json()


class TestCondition(unittest.TestCase):
    """Ensure customizations we've added work."""

    def testDictWithRequiredAttributesAndBadCodeableConceptSystem(self):
        """Should not be able to create Condition dict without required values, or arbitrary value in required value set."""
        with self.assertRaises(FHIRValidationError) as err:
            clinical_status = {'coding': [{'code': 'foo-bar', 'system': 'my-system'}]}
            Condition({'subject': {'reference': 'Patient/foo'}, 'clinicalStatus': clinical_status})
        expected_msg = 'Expecting CodeableConcept property with required binding_strength "clinicalStatus" system to be http://terminology.hl7.org/CodeSystem/condition-clinical was my-system'
        assert expected_msg in str(err.exception), str(err.exception)  # self.testDictWithRequiredAttributesAndBadCodeableConceptSystem.__doc__

    def testDictWithRequiredAttributesAndBadCodeableConceptCode(self):
        """Should not be able to create Condition dict without required values, or arbitrary value in required value set."""
        with self.assertRaises(FHIRValidationError) as err:
            clinical_status = {'coding': [{'code': 'foo-bar', 'system': 'http://terminology.hl7.org/CodeSystem/condition-clinical'}]}
            Condition({'subject': {'reference': 'Patient/foo'}, 'clinicalStatus': clinical_status})
        expected_msg = 'Expecting CodeableConcept property with required binding_strength "clinicalStatus" code to be in http://terminology.hl7.org/CodeSystem/condition-clinical was foo-bar'
        assert expected_msg in str(err.exception)

    def testDictWithRequiredAttributesAndGoodCodeableConceptCode(self):
        """Should not be able to create Condition dict without required values, or arbitrary value in required value set."""
        clinical_status = {'coding': [{'code': 'active', 'system': 'http://terminology.hl7.org/CodeSystem/condition-clinical'}]}
        condition = Condition({'subject': {'reference': 'Patient/foo'}, 'clinicalStatus': clinical_status})
        assert condition, self.testDictWithRequiredAttributesAndGoodCodeableConceptCode.__doc__
        assert condition.clinicalStatus
        assert condition.clinicalStatus.coding[0].code == 'active'
