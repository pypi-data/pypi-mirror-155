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

from . import group

from .fhirdate import FHIRDate
import logging


class GroupTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("Group", js["resourceType"])
        return group.Group(js)
    
    def testGroup1(self):
        inst = self.instantiate_from("group-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a Group instance")
        self.implGroup1(inst)
        
        js = inst.as_json()
        self.assertEqual("Group", js["resourceType"])
        inst2 = group.Group(js)
        self.implGroup1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implGroup1(self, inst):
        self.assertTrue(inst.actual)
        self.assertEqual(inst.characteristic[0].code.text, "gender")
        self.assertFalse(inst.characteristic[0].exclude)
        self.assertEqual(inst.characteristic[0].valueCodeableConcept.text, "mixed")
        self.assertEqual(inst.characteristic[1].code.text, "owner")
        self.assertFalse(inst.characteristic[1].exclude)
        self.assertEqual(inst.characteristic[1].valueCodeableConcept.text, "John Smith")
        self.assertEqual(inst.code.text, "Horse")
        self.assertEqual(inst.id, "101")
        self.assertEqual(inst.identifier[0].system, "http://someveterinarianclinic.org/fhir/NamingSystem/herds")
        self.assertEqual(inst.identifier[0].value, "12345")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.name, "John's herd")
        self.assertEqual(inst.quantity, 25)
        self.assertEqual(inst.text.status, "additional")
        self.assertEqual(inst.type, "animal")
    
    def testGroup2(self):
        inst = self.instantiate_from("group-example-member.json")
        self.assertIsNotNone(inst, "Must have instantiated a Group instance")
        self.implGroup2(inst)
        
        js = inst.as_json()
        self.assertEqual("Group", js["resourceType"])
        inst2 = group.Group(js)
        self.implGroup2(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implGroup2(self, inst):
        self.assertTrue(inst.actual)
        self.assertEqual(inst.id, "102")
        self.assertEqual(inst.member[0].period.start.date, FHIRDate("2014-10-08").date)
        self.assertEqual(inst.member[0].period.start.as_json(), "2014-10-08")
        self.assertTrue(inst.member[1].inactive)
        self.assertEqual(inst.member[1].period.start.date, FHIRDate("2015-04-02").date)
        self.assertEqual(inst.member[1].period.start.as_json(), "2015-04-02")
        self.assertEqual(inst.member[2].period.start.date, FHIRDate("2015-08-06").date)
        self.assertEqual(inst.member[2].period.start.as_json(), "2015-08-06")
        self.assertEqual(inst.member[3].period.start.date, FHIRDate("2015-08-06").date)
        self.assertEqual(inst.member[3].period.start.as_json(), "2015-08-06")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.text.status, "additional")
        self.assertEqual(inst.type, "person")
    
    def testGroup3(self):
        inst = self.instantiate_from("group-example-patientlist.json")
        self.assertIsNotNone(inst, "Must have instantiated a Group instance")
        self.implGroup3(inst)
        
        js = inst.as_json()
        self.assertEqual("Group", js["resourceType"])
        inst2 = group.Group(js)
        self.implGroup3(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implGroup3(self, inst):
        self.assertTrue(inst.actual)
        self.assertEqual(inst.characteristic[0].code.coding[0].code, "attributed-to")
        self.assertEqual(inst.characteristic[0].code.coding[0].system, "http://example.org")
        self.assertEqual(inst.characteristic[0].code.text, "Patients primarily attributed to")
        self.assertFalse(inst.characteristic[0].exclude)
        self.assertEqual(inst.id, "example-patientlist")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.text.status, "additional")
        self.assertEqual(inst.type, "person")
    
    def testGroup4(self):
        inst = self.instantiate_from("group-example-herd1.json")
        self.assertIsNotNone(inst, "Must have instantiated a Group instance")
        self.implGroup4(inst)
        
        js = inst.as_json()
        self.assertEqual("Group", js["resourceType"])
        inst2 = group.Group(js)
        self.implGroup4(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implGroup4(self, inst):
        self.assertTrue(inst.active)
        self.assertTrue(inst.actual)
        self.assertEqual(inst.characteristic[0].code.text, "gender")
        self.assertFalse(inst.characteristic[0].exclude)
        self.assertEqual(inst.characteristic[0].valueCodeableConcept.text, "female")
        self.assertEqual(inst.code.coding[0].code, "388393002")
        self.assertEqual(inst.code.coding[0].display, "Genus Sus (organism)")
        self.assertEqual(inst.code.coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.code.coding[1].code, "POR")
        self.assertEqual(inst.code.coding[1].display, "porcine")
        self.assertEqual(inst.code.coding[1].system, "https://www.aphis.usda.gov")
        self.assertEqual(inst.code.text, "Porcine")
        self.assertEqual(inst.extension[0].url, "http://example.org/fhir/StructureDefinition/owner")
        self.assertEqual(inst.id, "herd1")
        self.assertEqual(inst.identifier[0].system, "https://vetmed.iastate.edu/vdl")
        self.assertEqual(inst.identifier[0].value, "20171120-1234")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.name, "Breeding herd")
        self.assertEqual(inst.quantity, 2500)
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.type, "animal")

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