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

from . import requestgroup

from .fhirdate import FHIRDate
import logging


class RequestGroupTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("RequestGroup", js["resourceType"])
        return requestgroup.RequestGroup(js)
    
    def testRequestGroup1(self):
        inst = self.instantiate_from("requestgroup-kdn5-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a RequestGroup instance")
        self.implRequestGroup1(inst)
        
        js = inst.as_json()
        self.assertEqual("RequestGroup", js["resourceType"])
        inst2 = requestgroup.RequestGroup(js)
        self.implRequestGroup1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implRequestGroup1(self, inst):
        self.assertEqual(inst.action[0].action[0].action[0].action[0].action[0].extension[0].extension[0].url, "day")
        self.assertEqual(inst.action[0].action[0].action[0].action[0].action[0].extension[0].extension[0].valueInteger, 1)
        self.assertEqual(inst.action[0].action[0].action[0].action[0].action[0].extension[0].extension[1].url, "day")
        self.assertEqual(inst.action[0].action[0].action[0].action[0].action[0].extension[0].extension[1].valueInteger, 8)
        self.assertEqual(inst.action[0].action[0].action[0].action[0].action[0].extension[0].url, "http://hl7.org/fhir/StructureDefinition/timing-daysOfCycle")
        self.assertEqual(inst.action[0].action[0].action[0].action[0].action[0].id, "action-1")
        self.assertEqual(inst.action[0].action[0].action[0].action[0].action[0].textEquivalent, "Gemcitabine 1250 mg/m² IV over 30 minutes on days 1 and 8")
        self.assertEqual(inst.action[0].action[0].action[0].action[0].action[1].extension[0].extension[0].url, "day")
        self.assertEqual(inst.action[0].action[0].action[0].action[0].action[1].extension[0].extension[0].valueInteger, 1)
        self.assertEqual(inst.action[0].action[0].action[0].action[0].action[1].extension[0].url, "http://hl7.org/fhir/StructureDefinition/timing-daysOfCycle")
        self.assertEqual(inst.action[0].action[0].action[0].action[0].action[1].id, "action-2")
        self.assertEqual(inst.action[0].action[0].action[0].action[0].action[1].relatedAction[0].actionId, "action-1")
        self.assertEqual(inst.action[0].action[0].action[0].action[0].action[1].relatedAction[0].relationship, "concurrent-with-start")
        self.assertEqual(inst.action[0].action[0].action[0].action[0].action[1].textEquivalent, "CARBOplatin AUC 5 IV over 30 minutes on Day 1")
        self.assertEqual(inst.action[0].action[0].action[0].action[0].id, "cycle-definition-1")
        self.assertEqual(inst.action[0].action[0].action[0].action[0].textEquivalent, "21-day cycle for 6 cycles")
        self.assertEqual(inst.action[0].action[0].action[0].action[0].timingTiming.repeat.count, 6)
        self.assertEqual(inst.action[0].action[0].action[0].action[0].timingTiming.repeat.duration, 21)
        self.assertEqual(inst.action[0].action[0].action[0].action[0].timingTiming.repeat.durationUnit, "d")
        self.assertEqual(inst.action[0].action[0].action[0].groupingBehavior, "sentence-group")
        self.assertEqual(inst.action[0].action[0].action[0].selectionBehavior, "exactly-one")
        self.assertEqual(inst.action[0].action[0].selectionBehavior, "all")
        self.assertEqual(inst.action[0].selectionBehavior, "exactly-one")
        self.assertEqual(inst.authoredOn.date, FHIRDate("2017-03-06T17:31:00Z").date)
        self.assertEqual(inst.authoredOn.as_json(), "2017-03-06T17:31:00Z")
        self.assertEqual(inst.contained[0].id, "1111")
        self.assertEqual(inst.contained[1].id, "2222")
        self.assertEqual(inst.id, "kdn5-example")
        self.assertEqual(inst.identifier[0].value, "requestgroup-kdn5")
        self.assertEqual(inst.instantiatesCanonical[0], "PlanDefinition/KDN5")
        self.assertEqual(inst.intent, "plan")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.priority, "routine")
        self.assertEqual(inst.status, "draft")
        self.assertEqual(inst.text.div, "<div xmlns=\"http://www.w3.org/1999/xhtml\">Administer gemcitabine and carboplatin.</div>")
        self.assertEqual(inst.text.status, "generated")
    
    def testRequestGroup2(self):
        inst = self.instantiate_from("requestgroup-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a RequestGroup instance")
        self.implRequestGroup2(inst)
        
        js = inst.as_json()
        self.assertEqual("RequestGroup", js["resourceType"])
        inst2 = requestgroup.RequestGroup(js)
        self.implRequestGroup2(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implRequestGroup2(self, inst):
        self.assertEqual(inst.action[0].action[0].description, "Administer medication 1")
        self.assertEqual(inst.action[0].action[0].id, "medication-action-1")
        self.assertEqual(inst.action[0].action[0].type.coding[0].code, "create")
        self.assertEqual(inst.action[0].action[1].description, "Administer medication 2")
        self.assertEqual(inst.action[0].action[1].id, "medication-action-2")
        self.assertEqual(inst.action[0].action[1].relatedAction[0].actionId, "medication-action-1")
        self.assertEqual(inst.action[0].action[1].relatedAction[0].offsetDuration.unit, "h")
        self.assertEqual(inst.action[0].action[1].relatedAction[0].offsetDuration.value, 1)
        self.assertEqual(inst.action[0].action[1].relatedAction[0].relationship, "after-end")
        self.assertEqual(inst.action[0].action[1].type.coding[0].code, "create")
        self.assertEqual(inst.action[0].cardinalityBehavior, "single")
        self.assertEqual(inst.action[0].description, "Administer medications at the appropriate time")
        self.assertEqual(inst.action[0].groupingBehavior, "logical-group")
        self.assertEqual(inst.action[0].precheckBehavior, "yes")
        self.assertEqual(inst.action[0].prefix, "1")
        self.assertEqual(inst.action[0].requiredBehavior, "must")
        self.assertEqual(inst.action[0].selectionBehavior, "all")
        self.assertEqual(inst.action[0].textEquivalent, "Administer medication 1, followed an hour later by medication 2")
        self.assertEqual(inst.action[0].timingDateTime.date, FHIRDate("2017-03-06T19:00:00Z").date)
        self.assertEqual(inst.action[0].timingDateTime.as_json(), "2017-03-06T19:00:00Z")
        self.assertEqual(inst.action[0].title, "Administer Medications")
        self.assertEqual(inst.authoredOn.date, FHIRDate("2017-03-06T17:31:00Z").date)
        self.assertEqual(inst.authoredOn.as_json(), "2017-03-06T17:31:00Z")
        self.assertEqual(inst.contained[0].id, "medicationrequest-1")
        self.assertEqual(inst.contained[1].id, "medicationrequest-2")
        self.assertEqual(inst.groupIdentifier.system, "http://example.org/treatment-group")
        self.assertEqual(inst.groupIdentifier.value, "00001")
        self.assertEqual(inst.id, "example")
        self.assertEqual(inst.identifier[0].value, "requestgroup-1")
        self.assertEqual(inst.intent, "plan")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.note[0].text, "Additional notes about the request group")
        self.assertEqual(inst.priority, "routine")
        self.assertEqual(inst.reasonCode[0].text, "Treatment")
        self.assertEqual(inst.status, "draft")
        self.assertEqual(inst.text.div, "<div xmlns=\"http://www.w3.org/1999/xhtml\">Example RequestGroup illustrating related actions to administer medications in sequence with time delay.</div>")
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