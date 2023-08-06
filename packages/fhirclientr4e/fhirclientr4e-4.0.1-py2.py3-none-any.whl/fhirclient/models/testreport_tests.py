#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 on 2022-06-20.
#  2022, SMART Health IT.

import io
import json
import logging
import os
import typing
import unittest

from . import testreport

from .fhirdate import FHIRDate
import logging


class TestReportTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("TestReport", js["resourceType"])
        return testreport.TestReport(js)
    
    def testTestReport1(self):
        inst = self.instantiate_from("testreport-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a TestReport instance")
        self.implTestReport1(inst)
        
        js = inst.as_json()
        self.assertEqual("TestReport", js["resourceType"])
        inst2 = testreport.TestReport(js)
        self.implTestReport1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implTestReport1(self, inst):
        self.assertEqual(inst.id, "testreport-example")
        self.assertEqual(inst.identifier.system, "urn:ietf:rfc:3986")
        self.assertEqual(inst.identifier.value, "urn:oid:1.3.6.1.4.1.21367.2005.3.7.9878")
        self.assertEqual(inst.issued.date, FHIRDate("2016-10-07T08:25:34-05:00").date)
        self.assertEqual(inst.issued.as_json(), "2016-10-07T08:25:34-05:00")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.name, "TestReport Example for TestScript Example")
        self.assertEqual(inst.participant[0].display, "Crucible")
        self.assertEqual(inst.participant[0].type, "test-engine")
        self.assertEqual(inst.participant[0].uri, "http://projectcrucible.org")
        self.assertEqual(inst.participant[1].display, "HealthIntersections STU3")
        self.assertEqual(inst.participant[1].type, "server")
        self.assertEqual(inst.participant[1].uri, "http://fhir3.healthintersections.com.au/open")
        self.assertEqual(inst.result, "pass")
        self.assertEqual(inst.score, 100.0)
        self.assertEqual(inst.setup.action[0].operation.detail, "http://projectcrucible.org/permalink/1")
        self.assertEqual(inst.setup.action[0].operation.message, "DELETE Patient")
        self.assertEqual(inst.setup.action[0].operation.result, "pass")
        self.assertEqual(inst.setup.action[1].assert_fhir.detail, "http://projectcrucible.org/permalink/1")
        self.assertEqual(inst.setup.action[1].assert_fhir.message, "HTTP 204")
        self.assertEqual(inst.setup.action[1].assert_fhir.result, "pass")
        self.assertEqual(inst.setup.action[2].operation.detail, "http://projectcrucible.org/permalink/1")
        self.assertEqual(inst.setup.action[2].operation.message, "POST Patient/fixture-patient-create")
        self.assertEqual(inst.setup.action[2].operation.result, "pass")
        self.assertEqual(inst.setup.action[3].assert_fhir.detail, "http://projectcrucible.org/permalink/1")
        self.assertEqual(inst.setup.action[3].assert_fhir.message, "HTTP 201")
        self.assertEqual(inst.setup.action[3].assert_fhir.result, "pass")
        self.assertEqual(inst.status, "completed")
        self.assertEqual(inst.teardown.action[0].operation.detail, "http://projectcrucible.org/permalink/3")
        self.assertEqual(inst.teardown.action[0].operation.message, "DELETE Patient/fixture-patient-create.")
        self.assertEqual(inst.teardown.action[0].operation.result, "pass")
        self.assertEqual(inst.test[0].action[0].operation.detail, "http://projectcrucible.org/permalink/2")
        self.assertEqual(inst.test[0].action[0].operation.message, "GET Patient/fixture-patient-create")
        self.assertEqual(inst.test[0].action[0].operation.result, "pass")
        self.assertEqual(inst.test[0].action[1].assert_fhir.detail, "http://projectcrucible.org/permalink/2")
        self.assertEqual(inst.test[0].action[1].assert_fhir.message, "HTTP 200")
        self.assertEqual(inst.test[0].action[1].assert_fhir.result, "pass")
        self.assertEqual(inst.test[0].action[2].assert_fhir.detail, "http://projectcrucible.org/permalink/2")
        self.assertEqual(inst.test[0].action[2].assert_fhir.message, "Last-Modified Present")
        self.assertEqual(inst.test[0].action[2].assert_fhir.result, "pass")
        self.assertEqual(inst.test[0].action[3].assert_fhir.detail, "http://projectcrucible.org/permalink/2")
        self.assertEqual(inst.test[0].action[3].assert_fhir.message, "Response is Patient")
        self.assertEqual(inst.test[0].action[3].assert_fhir.result, "pass")
        self.assertEqual(inst.test[0].action[4].assert_fhir.detail, "http://projectcrucible.org/permalink/2")
        self.assertEqual(inst.test[0].action[4].assert_fhir.message, "Response validates")
        self.assertEqual(inst.test[0].action[4].assert_fhir.result, "pass")
        self.assertEqual(inst.test[0].action[5].assert_fhir.detail, "http://projectcrucible.org/permalink/2")
        self.assertEqual(inst.test[0].action[5].assert_fhir.message, "Patient.name.family 'Chalmers'")
        self.assertEqual(inst.test[0].action[5].assert_fhir.result, "pass")
        self.assertEqual(inst.test[0].action[6].assert_fhir.detail, "http://projectcrucible.org/permalink/2")
        self.assertEqual(inst.test[0].action[6].assert_fhir.message, "Patient.name.given 'Peter'")
        self.assertEqual(inst.test[0].action[6].assert_fhir.result, "pass")
        self.assertEqual(inst.test[0].action[7].assert_fhir.detail, "http://projectcrucible.org/permalink/2")
        self.assertEqual(inst.test[0].action[7].assert_fhir.message, "Patient.name.family 'Chalmers'")
        self.assertEqual(inst.test[0].action[7].assert_fhir.result, "pass")
        self.assertEqual(inst.test[0].action[8].assert_fhir.detail, "http://projectcrucible.org/permalink/2")
        self.assertEqual(inst.test[0].action[8].assert_fhir.message, "Patient.name.family 'Chalmers'")
        self.assertEqual(inst.test[0].action[8].assert_fhir.result, "pass")
        self.assertEqual(inst.test[0].action[9].assert_fhir.detail, "http://projectcrucible.org/permalink/2")
        self.assertEqual(inst.test[0].action[9].assert_fhir.message, "Patient expected values.")
        self.assertEqual(inst.test[0].action[9].assert_fhir.result, "pass")
        self.assertEqual(inst.test[0].description, "Read a Patient and validate response.")
        self.assertEqual(inst.test[0].id, "01-ReadPatient")
        self.assertEqual(inst.test[0].name, "Read Patient")
        self.assertEqual(inst.tester, "HL7 Execution Engine")
        self.assertEqual(inst.text.status, "generated")

    def evaluate_simplified_json(self, inst):
        """Ensure simplified json."""
        simplified_js, simplified_schema = inst.as_simplified_json()
        self.assertIsNotNone(simplified_js, "Must create simplified json")

        # test simplify identifiers
        if hasattr(inst, 'identifier'):
            assert 'identifier' not in simplified_js
            if inst.identifier:
                simplified_identifiers = [k for k in simplified_js.keys() if k.startswith('identifier_')]
                if isinstance(inst.identifier, typing.List):
                    identifiers_with_values = [i for i in inst.identifier if i.value]
                else:
                    identifiers_with_values = [inst.identifier]
                self.assertEqual(len(identifiers_with_values), len(simplified_identifiers), "Should simplify identifiers.")

        # test simplify lists
        for name in vars(inst):

            if name == 'identifier':
                continue

            if name == 'extension':
                continue

            value = getattr(inst, name)
            is_coding = value.__class__.__name__ == 'Coding' or (isinstance(value, typing.List) and len(value) == 1 and value[0].__class__.__name__ == 'Coding')
            if is_coding:
                continue

            if isinstance(getattr(inst, name), typing.List) and len(getattr(inst, name)) == 1:
                # Properties that need to be renamed because of language keyword conflicts
                # see mapping
                if name not in simplified_js:
                    name = name.replace("_fhir", "")
                self.assertFalse(isinstance(simplified_js[name], typing.List), "Should simplify lists {}".format(name))

        # test simplify coding
        # meta has known coding attribute 'tags'
        if hasattr(inst, 'meta'):
            if inst.meta and inst.meta.tag and len(inst.meta.tag) > 0:
                simplified_tags = [k for k in simplified_js['meta'].keys() if k.startswith('tag_')]
                self.assertEqual(len(inst.meta.tag), len(simplified_tags), "Should simplify meta tags.")
                self.assertTrue('tag' not in simplified_js['meta'], "Should not have meta.tag")

        # test simplify extensions
        if hasattr(inst, 'extension'):
            if inst.extension and len(inst.extension) > 0:
                assert 'extension' not in simplified_js
                simplified_extensions = [k for k in simplified_js.keys() if k.startswith('extension_')]
                self.assertEqual(len(inst.extension), len(simplified_extensions), "Should simplify extensions.")

        # test simplify schema
        for k in simplified_js:
            assert k in simplified_schema, "Should have a schema definition for {}".format(k)

        # test simplified, flattened
        from flatten_json import flatten
        flattened = flatten(simplified_js, separator='|')
        for flattened_key in flattened:
            dict_ = simplified_schema
            for flattened_key_part in flattened_key.split('|'):
                if flattened_key_part not in dict_ and flattened_key_part.isnumeric():
                    # traverse over list index
                    continue
                dict_ = dict_[flattened_key_part]
                self.assertIsNotNone(dict_, "Should have a schema entry for {}".format(flattened_key_part))
                if 'docstring' not in dict_:
                    logging.getLogger(__name__).warning(
                        "Missing docstring for resource_type:{} flattened_key:{} flattened_key_part:{} dict:{}".format(
                            inst.resource_type, flattened_key, flattened_key_part, dict_))
                    break