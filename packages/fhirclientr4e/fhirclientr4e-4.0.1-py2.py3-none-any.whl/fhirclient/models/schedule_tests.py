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

from . import schedule

from .fhirdate import FHIRDate
import logging


class ScheduleTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("Schedule", js["resourceType"])
        return schedule.Schedule(js)
    
    def testSchedule1(self):
        inst = self.instantiate_from("schedule-provider-location1-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a Schedule instance")
        self.implSchedule1(inst)
        
        js = inst.as_json()
        self.assertEqual("Schedule", js["resourceType"])
        inst2 = schedule.Schedule(js)
        self.implSchedule1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implSchedule1(self, inst):
        self.assertTrue(inst.active)
        self.assertEqual(inst.comment, "The slots attached to this schedule are for genetic counselling in the USS Enterprise-D Sickbay.")
        self.assertEqual(inst.id, "exampleloc1")
        self.assertEqual(inst.identifier[0].system, "http://example.org/scheduleid")
        self.assertEqual(inst.identifier[0].use, "usual")
        self.assertEqual(inst.identifier[0].value, "46")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.planningHorizon.end.date, FHIRDate("2017-12-25T09:30:00Z").date)
        self.assertEqual(inst.planningHorizon.end.as_json(), "2017-12-25T09:30:00Z")
        self.assertEqual(inst.planningHorizon.start.date, FHIRDate("2017-12-25T09:15:00Z").date)
        self.assertEqual(inst.planningHorizon.start.as_json(), "2017-12-25T09:15:00Z")
        self.assertEqual(inst.serviceCategory[0].coding[0].code, "17")
        self.assertEqual(inst.serviceCategory[0].coding[0].display, "General Practice")
        self.assertEqual(inst.serviceType[0].coding[0].code, "75")
        self.assertEqual(inst.serviceType[0].coding[0].display, "Genetic Counselling")
        self.assertEqual(inst.specialty[0].coding[0].code, "394580004")
        self.assertEqual(inst.specialty[0].coding[0].display, "Clinical genetics")
        self.assertEqual(inst.text.status, "generated")
    
    def testSchedule2(self):
        inst = self.instantiate_from("schedule-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a Schedule instance")
        self.implSchedule2(inst)
        
        js = inst.as_json()
        self.assertEqual("Schedule", js["resourceType"])
        inst2 = schedule.Schedule(js)
        self.implSchedule2(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implSchedule2(self, inst):
        self.assertTrue(inst.active)
        self.assertEqual(inst.comment, "The slots attached to this schedule should be specialized to cover immunizations within the clinic")
        self.assertEqual(inst.id, "example")
        self.assertEqual(inst.identifier[0].system, "http://example.org/scheduleid")
        self.assertEqual(inst.identifier[0].use, "usual")
        self.assertEqual(inst.identifier[0].value, "45")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.planningHorizon.end.date, FHIRDate("2013-12-25T09:30:00Z").date)
        self.assertEqual(inst.planningHorizon.end.as_json(), "2013-12-25T09:30:00Z")
        self.assertEqual(inst.planningHorizon.start.date, FHIRDate("2013-12-25T09:15:00Z").date)
        self.assertEqual(inst.planningHorizon.start.as_json(), "2013-12-25T09:15:00Z")
        self.assertEqual(inst.serviceCategory[0].coding[0].code, "17")
        self.assertEqual(inst.serviceCategory[0].coding[0].display, "General Practice")
        self.assertEqual(inst.serviceType[0].coding[0].code, "57")
        self.assertEqual(inst.serviceType[0].coding[0].display, "Immunization")
        self.assertEqual(inst.specialty[0].coding[0].code, "408480009")
        self.assertEqual(inst.specialty[0].coding[0].display, "Clinical immunology")
        self.assertEqual(inst.text.status, "generated")
    
    def testSchedule3(self):
        inst = self.instantiate_from("schedule-provider-location2-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a Schedule instance")
        self.implSchedule3(inst)
        
        js = inst.as_json()
        self.assertEqual("Schedule", js["resourceType"])
        inst2 = schedule.Schedule(js)
        self.implSchedule3(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implSchedule3(self, inst):
        self.assertTrue(inst.active)
        self.assertEqual(inst.comment, "The slots attached to this schedule are for neurosurgery operations at Starfleet HQ only.")
        self.assertEqual(inst.id, "exampleloc2")
        self.assertEqual(inst.identifier[0].system, "http://example.org/scheduleid")
        self.assertEqual(inst.identifier[0].use, "usual")
        self.assertEqual(inst.identifier[0].value, "47")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.planningHorizon.end.date, FHIRDate("2017-12-25T09:30:00Z").date)
        self.assertEqual(inst.planningHorizon.end.as_json(), "2017-12-25T09:30:00Z")
        self.assertEqual(inst.planningHorizon.start.date, FHIRDate("2017-12-25T09:15:00Z").date)
        self.assertEqual(inst.planningHorizon.start.as_json(), "2017-12-25T09:15:00Z")
        self.assertEqual(inst.serviceCategory[0].coding[0].code, "31")
        self.assertEqual(inst.serviceCategory[0].coding[0].display, "Specialist Surgical")
        self.assertEqual(inst.serviceType[0].coding[0].code, "221")
        self.assertEqual(inst.serviceType[0].coding[0].display, "Surgery - General")
        self.assertEqual(inst.specialty[0].coding[0].code, "394610002")
        self.assertEqual(inst.specialty[0].coding[0].display, "Surgery-Neurosurgery")
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