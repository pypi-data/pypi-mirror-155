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

from . import adverseevent

from .fhirdate import FHIRDate
import logging


class AdverseEventTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("AdverseEvent", js["resourceType"])
        return adverseevent.AdverseEvent(js)
    
    def testAdverseEvent1(self):
        inst = self.instantiate_from("adverseevent-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a AdverseEvent instance")
        self.implAdverseEvent1(inst)
        
        js = inst.as_json()
        self.assertEqual("AdverseEvent", js["resourceType"])
        inst2 = adverseevent.AdverseEvent(js)
        self.implAdverseEvent1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implAdverseEvent1(self, inst):
        self.assertEqual(inst.actuality, "actual")
        self.assertEqual(inst.category[0].coding[0].code, "product-use-error")
        self.assertEqual(inst.category[0].coding[0].display, "Product Use Error")
        self.assertEqual(inst.category[0].coding[0].system, "http://terminology.hl7.org/CodeSystem/adverse-event-category")
        self.assertEqual(inst.date.date, FHIRDate("2017-01-29T12:34:56+00:00").date)
        self.assertEqual(inst.date.as_json(), "2017-01-29T12:34:56+00:00")
        self.assertEqual(inst.event.coding[0].code, "304386008")
        self.assertEqual(inst.event.coding[0].display, "O/E - itchy rash")
        self.assertEqual(inst.event.coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.event.text, "This was a mild rash on the left forearm")
        self.assertEqual(inst.id, "example")
        self.assertEqual(inst.identifier.system, "http://acme.com/ids/patients/risks")
        self.assertEqual(inst.identifier.value, "49476534")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.seriousness.coding[0].code, "Non-serious")
        self.assertEqual(inst.seriousness.coding[0].display, "Non-serious")
        self.assertEqual(inst.seriousness.coding[0].system, "http://terminology.hl7.org/CodeSystem/adverse-event-seriousness")
        self.assertEqual(inst.severity.coding[0].code, "mild")
        self.assertEqual(inst.severity.coding[0].display, "Mild")
        self.assertEqual(inst.severity.coding[0].system, "http://terminology.hl7.org/CodeSystem/adverse-event-severity")
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