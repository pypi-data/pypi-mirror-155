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

from . import basic

from .fhirdate import FHIRDate
import logging


class BasicTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("Basic", js["resourceType"])
        return basic.Basic(js)
    
    def testBasic1(self):
        inst = self.instantiate_from("basic-example2.json")
        self.assertIsNotNone(inst, "Must have instantiated a Basic instance")
        self.implBasic1(inst)
        
        js = inst.as_json()
        self.assertEqual("Basic", js["resourceType"])
        inst2 = basic.Basic(js)
        self.implBasic1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implBasic1(self, inst):
        self.assertEqual(inst.code.coding[0].code, "UMLCLASSMODEL")
        self.assertEqual(inst.code.coding[0].system, "http://example.org/do-not-use/fhir-codes#resourceTypes")
        self.assertEqual(inst.extension[0].extension[0].url, "name")
        self.assertEqual(inst.extension[0].extension[0].valueString, "Class1")
        self.assertEqual(inst.extension[0].extension[1].extension[0].url, "name")
        self.assertEqual(inst.extension[0].extension[1].extension[0].valueString, "attribute1")
        self.assertEqual(inst.extension[0].extension[1].extension[1].url, "minOccurs")
        self.assertEqual(inst.extension[0].extension[1].extension[1].valueInteger, 1)
        self.assertEqual(inst.extension[0].extension[1].extension[2].url, "maxOccurs")
        self.assertEqual(inst.extension[0].extension[1].extension[2].valueCode, "*")
        self.assertEqual(inst.extension[0].extension[1].url, "attribute")
        self.assertEqual(inst.extension[0].extension[2].extension[0].url, "name")
        self.assertEqual(inst.extension[0].extension[2].extension[0].valueString, "attribute2")
        self.assertEqual(inst.extension[0].extension[2].extension[1].url, "minOccurs")
        self.assertEqual(inst.extension[0].extension[2].extension[1].valueInteger, 0)
        self.assertEqual(inst.extension[0].extension[2].extension[2].url, "maxOccurs")
        self.assertEqual(inst.extension[0].extension[2].extension[2].valueInteger, 1)
        self.assertEqual(inst.extension[0].extension[2].url, "attribute")
        self.assertEqual(inst.extension[0].url, "http://example.org/do-not-use/fhir-extensions/UMLclass")
        self.assertEqual(inst.id, "classModel")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.text.status, "generated")
    
    def testBasic2(self):
        inst = self.instantiate_from("basic-example-narrative.json")
        self.assertIsNotNone(inst, "Must have instantiated a Basic instance")
        self.implBasic2(inst)
        
        js = inst.as_json()
        self.assertEqual("Basic", js["resourceType"])
        inst2 = basic.Basic(js)
        self.implBasic2(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implBasic2(self, inst):
        self.assertEqual(inst.code.text, "Example Narrative Tester")
        self.assertEqual(inst.id, "basic-example-narrative")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.text.status, "additional")
    
    def testBasic3(self):
        inst = self.instantiate_from("basic-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a Basic instance")
        self.implBasic3(inst)
        
        js = inst.as_json()
        self.assertEqual("Basic", js["resourceType"])
        inst2 = basic.Basic(js)
        self.implBasic3(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implBasic3(self, inst):
        self.assertEqual(inst.code.coding[0].code, "referral")
        self.assertEqual(inst.code.coding[0].system, "http://terminology.hl7.org/CodeSystem/basic-resource-type")
        self.assertEqual(inst.created.date, FHIRDate("2013-05-14").date)
        self.assertEqual(inst.created.as_json(), "2013-05-14")
        self.assertEqual(inst.extension[0].url, "http://example.org/do-not-use/fhir-extensions/referral#requestingPractitioner")
        self.assertEqual(inst.extension[1].url, "http://example.org/do-not-use/fhir-extensions/referral#notes")
        self.assertEqual(inst.extension[1].valueString, "The patient had fever peaks over the last couple of days. He is worried about these peaks.")
        self.assertEqual(inst.extension[2].url, "http://example.org/do-not-use/fhir-extensions/referral#fulfillingEncounter")
        self.assertEqual(inst.id, "referral")
        self.assertEqual(inst.identifier[0].system, "http://goodhealth.org/basic/identifiers")
        self.assertEqual(inst.identifier[0].value, "19283746")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.modifierExtension[0].url, "http://example.org/do-not-use/fhir-extensions/referral#referredForService")
        self.assertEqual(inst.modifierExtension[0].valueCodeableConcept.coding[0].code, "11429006")
        self.assertEqual(inst.modifierExtension[0].valueCodeableConcept.coding[0].display, "Consultation")
        self.assertEqual(inst.modifierExtension[0].valueCodeableConcept.coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.modifierExtension[1].url, "http://example.org/do-not-use/fhir-extensions/referral#targetDate")
        self.assertEqual(inst.modifierExtension[1].valuePeriod.end.date, FHIRDate("2013-04-15").date)
        self.assertEqual(inst.modifierExtension[1].valuePeriod.end.as_json(), "2013-04-15")
        self.assertEqual(inst.modifierExtension[1].valuePeriod.start.date, FHIRDate("2013-04-01").date)
        self.assertEqual(inst.modifierExtension[1].valuePeriod.start.as_json(), "2013-04-01")
        self.assertEqual(inst.modifierExtension[2].url, "http://example.org/do-not-use/fhir-extensions/referral#status")
        self.assertEqual(inst.modifierExtension[2].valueCode, "complete")
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