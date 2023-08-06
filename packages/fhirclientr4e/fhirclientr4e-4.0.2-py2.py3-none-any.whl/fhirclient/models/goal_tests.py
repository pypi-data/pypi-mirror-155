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

from . import goal

from .fhirdate import FHIRDate
import logging


class GoalTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("Goal", js["resourceType"])
        return goal.Goal(js)
    
    def testGoal1(self):
        inst = self.instantiate_from("goal-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a Goal instance")
        self.implGoal1(inst)
        
        js = inst.as_json()
        self.assertEqual("Goal", js["resourceType"])
        inst2 = goal.Goal(js)
        self.implGoal1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implGoal1(self, inst):
        self.assertEqual(inst.category[0].coding[0].code, "dietary")
        self.assertEqual(inst.category[0].coding[0].system, "http://terminology.hl7.org/CodeSystem/goal-category")
        self.assertEqual(inst.description.text, "Target weight is 160 to 180 lbs.")
        self.assertEqual(inst.id, "example")
        self.assertEqual(inst.identifier[0].value, "123")
        self.assertEqual(inst.lifecycleStatus, "on-hold")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.priority.coding[0].code, "high-priority")
        self.assertEqual(inst.priority.coding[0].display, "High Priority")
        self.assertEqual(inst.priority.coding[0].system, "http://terminology.hl7.org/CodeSystem/goal-priority")
        self.assertEqual(inst.priority.text, "high")
        self.assertEqual(inst.startDate.date, FHIRDate("2015-04-05").date)
        self.assertEqual(inst.startDate.as_json(), "2015-04-05")
        self.assertEqual(inst.statusDate.date, FHIRDate("2016-02-14").date)
        self.assertEqual(inst.statusDate.as_json(), "2016-02-14")
        self.assertEqual(inst.statusReason, "Patient wants to defer weight loss until after honeymoon.")
        self.assertEqual(inst.target[0].detailRange.high.code, "[lb_av]")
        self.assertEqual(inst.target[0].detailRange.high.system, "http://unitsofmeasure.org")
        self.assertEqual(inst.target[0].detailRange.high.unit, "lbs")
        self.assertEqual(inst.target[0].detailRange.high.value, 180)
        self.assertEqual(inst.target[0].detailRange.low.code, "[lb_av]")
        self.assertEqual(inst.target[0].detailRange.low.system, "http://unitsofmeasure.org")
        self.assertEqual(inst.target[0].detailRange.low.unit, "lbs")
        self.assertEqual(inst.target[0].detailRange.low.value, 160)
        self.assertEqual(inst.target[0].dueDate.date, FHIRDate("2016-04-05").date)
        self.assertEqual(inst.target[0].dueDate.as_json(), "2016-04-05")
        self.assertEqual(inst.target[0].measure.coding[0].code, "3141-9")
        self.assertEqual(inst.target[0].measure.coding[0].display, "Weight Measured")
        self.assertEqual(inst.target[0].measure.coding[0].system, "http://loinc.org")
        self.assertEqual(inst.text.status, "additional")
    
    def testGoal2(self):
        inst = self.instantiate_from("goal-example-stop-smoking.json")
        self.assertIsNotNone(inst, "Must have instantiated a Goal instance")
        self.implGoal2(inst)
        
        js = inst.as_json()
        self.assertEqual("Goal", js["resourceType"])
        inst2 = goal.Goal(js)
        self.implGoal2(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implGoal2(self, inst):
        self.assertEqual(inst.achievementStatus.coding[0].code, "achieved")
        self.assertEqual(inst.achievementStatus.coding[0].display, "Achieved")
        self.assertEqual(inst.achievementStatus.coding[0].system, "http://terminology.hl7.org/CodeSystem/goal-achievement")
        self.assertEqual(inst.achievementStatus.text, "Achieved")
        self.assertEqual(inst.description.text, "Stop smoking")
        self.assertEqual(inst.id, "stop-smoking")
        self.assertEqual(inst.identifier[0].value, "123")
        self.assertEqual(inst.lifecycleStatus, "completed")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.outcomeCode[0].coding[0].code, "8517006")
        self.assertEqual(inst.outcomeCode[0].coding[0].display, "Ex-smoker (finding)")
        self.assertEqual(inst.outcomeCode[0].coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.outcomeCode[0].text, "Former smoker")
        self.assertEqual(inst.startDate.date, FHIRDate("2015-04-05").date)
        self.assertEqual(inst.startDate.as_json(), "2015-04-05")
        self.assertEqual(inst.text.status, "additional")

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