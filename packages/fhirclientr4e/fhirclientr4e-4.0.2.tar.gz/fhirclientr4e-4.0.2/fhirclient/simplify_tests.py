# -*- coding: utf-8 -*-

import unittest
from pprint import pprint

from fhirclient.models.patient_tests import PatientTests
from fhirclient.models.researchstudy_tests import ResearchStudyTests


class TestSimplify(unittest.TestCase):
    """Ensure customizations we've added work."""

    def testResearchStudy1(self):
        inst = ResearchStudyTests().instantiate_from("researchstudy-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a ResearchStudy instance")
        # pprint(inst.as_simplified_json())

    def testPatient10(self):
        inst = PatientTests().instantiate_from("patient-example-xds.json")
        self.assertIsNotNone(inst, "Must have instantiated a Patient instance")
        pprint(inst.as_simplified_json())
