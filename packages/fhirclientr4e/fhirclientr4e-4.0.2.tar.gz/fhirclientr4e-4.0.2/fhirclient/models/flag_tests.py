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

from . import flag

from .fhirdate import FHIRDate
import logging


class FlagTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("Flag", js["resourceType"])
        return flag.Flag(js)
    
    def testFlag1(self):
        inst = self.instantiate_from("flag-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a Flag instance")
        self.implFlag1(inst)
        
        js = inst.as_json()
        self.assertEqual("Flag", js["resourceType"])
        inst2 = flag.Flag(js)
        self.implFlag1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implFlag1(self, inst):
        self.assertEqual(inst.category[0].coding[0].code, "safety")
        self.assertEqual(inst.category[0].coding[0].display, "Safety")
        self.assertEqual(inst.category[0].coding[0].system, "http://terminology.hl7.org/CodeSystem/flag-category")
        self.assertEqual(inst.category[0].text, "Safety")
        self.assertEqual(inst.code.coding[0].code, "bigdog")
        self.assertEqual(inst.code.coding[0].display, "Big dog")
        self.assertEqual(inst.code.coding[0].system, "http://example.org/local")
        self.assertEqual(inst.code.text, "Patient has a big dog at his home. Always always wear a suit of armor or take other active counter-measures")
        self.assertEqual(inst.id, "example")
        self.assertEqual(inst.identifier[0].value, "12345")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.period.end.date, FHIRDate("2016-12-01").date)
        self.assertEqual(inst.period.end.as_json(), "2016-12-01")
        self.assertEqual(inst.period.start.date, FHIRDate("2015-01-17").date)
        self.assertEqual(inst.period.start.as_json(), "2015-01-17")
        self.assertEqual(inst.status, "inactive")
        self.assertEqual(inst.text.div, "<div xmlns=\"http://www.w3.org/1999/xhtml\">Large Dog warning for Peter Patient</div>")
        self.assertEqual(inst.text.status, "generated")
    
    def testFlag2(self):
        inst = self.instantiate_from("flag-example-encounter.json")
        self.assertIsNotNone(inst, "Must have instantiated a Flag instance")
        self.implFlag2(inst)
        
        js = inst.as_json()
        self.assertEqual("Flag", js["resourceType"])
        inst2 = flag.Flag(js)
        self.implFlag2(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implFlag2(self, inst):
        self.assertEqual(inst.category[0].coding[0].code, "infection")
        self.assertEqual(inst.category[0].coding[0].display, "Infection Control Level")
        self.assertEqual(inst.category[0].coding[0].system, "http://example.org/local")
        self.assertEqual(inst.code.coding[0].code, "l3")
        self.assertEqual(inst.code.coding[0].display, "Follow Level 3 Protocol")
        self.assertEqual(inst.code.coding[0].system, "http://example.org/local/if1")
        self.assertEqual(inst.id, "example-encounter")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.status, "active")
        self.assertEqual(inst.text.div, "<div xmlns=\"http://www.w3.org/1999/xhtml\">Follow Infection Control Level 3 Protocol</div>")
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