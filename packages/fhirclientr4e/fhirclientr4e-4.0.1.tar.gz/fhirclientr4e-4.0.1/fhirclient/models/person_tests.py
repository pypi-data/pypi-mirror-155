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

from . import person

from .fhirdate import FHIRDate
import logging


class PersonTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("Person", js["resourceType"])
        return person.Person(js)
    
    def testPerson1(self):
        inst = self.instantiate_from("person-example-f002-ariadne.json")
        self.assertIsNotNone(inst, "Must have instantiated a Person instance")
        self.implPerson1(inst)
        
        js = inst.as_json()
        self.assertEqual("Person", js["resourceType"])
        inst2 = person.Person(js)
        self.implPerson1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implPerson1(self, inst):
        self.assertTrue(inst.active)
        self.assertEqual(inst.birthDate.date, FHIRDate("1963").date)
        self.assertEqual(inst.birthDate.as_json(), "1963")
        self.assertEqual(inst.gender, "female")
        self.assertEqual(inst.id, "f002")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.name[0].text, "Ariadne Bor-Jansma")
        self.assertEqual(inst.name[0].use, "usual")
        self.assertEqual(inst.photo.contentType, "image/jpeg")
        self.assertEqual(inst.telecom[0].system, "phone")
        self.assertEqual(inst.telecom[0].use, "home")
        self.assertEqual(inst.telecom[0].value, "+31201234567")
        self.assertEqual(inst.text.status, "generated")
    
    def testPerson2(self):
        inst = self.instantiate_from("person-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a Person instance")
        self.implPerson2(inst)
        
        js = inst.as_json()
        self.assertEqual("Person", js["resourceType"])
        inst2 = person.Person(js)
        self.implPerson2(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implPerson2(self, inst):
        self.assertTrue(inst.active)
        self.assertEqual(inst.address[0].city, "PleasantVille")
        self.assertEqual(inst.address[0].line[0], "534 Erewhon St")
        self.assertEqual(inst.address[0].postalCode, "3999")
        self.assertEqual(inst.address[0].state, "Vic")
        self.assertEqual(inst.address[0].use, "home")
        self.assertEqual(inst.birthDate.date, FHIRDate("1974-12-25").date)
        self.assertEqual(inst.birthDate.as_json(), "1974-12-25")
        self.assertEqual(inst.gender, "male")
        self.assertEqual(inst.id, "example")
        self.assertEqual(inst.identifier[0].period.start.date, FHIRDate("2001-05-06").date)
        self.assertEqual(inst.identifier[0].period.start.as_json(), "2001-05-06")
        self.assertEqual(inst.identifier[0].system, "urn:oid:1.2.36.146.595.217.0.1")
        self.assertEqual(inst.identifier[0].type.coding[0].code, "MR")
        self.assertEqual(inst.identifier[0].type.coding[0].system, "http://terminology.hl7.org/CodeSystem/v2-0203")
        self.assertEqual(inst.identifier[0].use, "usual")
        self.assertEqual(inst.identifier[0].value, "12345")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.name[0].family, "Chalmers")
        self.assertEqual(inst.name[0].given[0], "Peter")
        self.assertEqual(inst.name[0].given[1], "James")
        self.assertEqual(inst.name[0].use, "official")
        self.assertEqual(inst.name[1].given[0], "Jim")
        self.assertEqual(inst.name[1].use, "usual")
        self.assertEqual(inst.telecom[0].use, "home")
        self.assertEqual(inst.telecom[1].system, "phone")
        self.assertEqual(inst.telecom[1].use, "work")
        self.assertEqual(inst.telecom[1].value, "(03) 5555 6473")
        self.assertEqual(inst.telecom[2].system, "email")
        self.assertEqual(inst.telecom[2].use, "home")
        self.assertEqual(inst.telecom[2].value, "Jim@example.org")
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