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

from . import visionprescription

from .fhirdate import FHIRDate
import logging


class VisionPrescriptionTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("VisionPrescription", js["resourceType"])
        return visionprescription.VisionPrescription(js)
    
    def testVisionPrescription1(self):
        inst = self.instantiate_from("visionprescription-example-1.json")
        self.assertIsNotNone(inst, "Must have instantiated a VisionPrescription instance")
        self.implVisionPrescription1(inst)
        
        js = inst.as_json()
        self.assertEqual("VisionPrescription", js["resourceType"])
        inst2 = visionprescription.VisionPrescription(js)
        self.implVisionPrescription1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implVisionPrescription1(self, inst):
        self.assertEqual(inst.created.date, FHIRDate("2014-06-15").date)
        self.assertEqual(inst.created.as_json(), "2014-06-15")
        self.assertEqual(inst.dateWritten.date, FHIRDate("2014-06-15").date)
        self.assertEqual(inst.dateWritten.as_json(), "2014-06-15")
        self.assertEqual(inst.id, "33124")
        self.assertEqual(inst.identifier[0].system, "http://www.happysight.com/prescription")
        self.assertEqual(inst.identifier[0].value, "15014")
        self.assertEqual(inst.lensSpecification[0].add, 1.75)
        self.assertEqual(inst.lensSpecification[0].axis, 160)
        self.assertEqual(inst.lensSpecification[0].backCurve, 8.7)
        self.assertEqual(inst.lensSpecification[0].brand, "OphthaGuard")
        self.assertEqual(inst.lensSpecification[0].color, "green")
        self.assertEqual(inst.lensSpecification[0].cylinder, -2.25)
        self.assertEqual(inst.lensSpecification[0].diameter, 14.0)
        self.assertEqual(inst.lensSpecification[0].duration.code, "month")
        self.assertEqual(inst.lensSpecification[0].duration.system, "http://unitsofmeasure.org")
        self.assertEqual(inst.lensSpecification[0].duration.unit, "month")
        self.assertEqual(inst.lensSpecification[0].duration.value, 1)
        self.assertEqual(inst.lensSpecification[0].eye, "right")
        self.assertEqual(inst.lensSpecification[0].note[0].text, "Shade treatment for extreme light sensitivity")
        self.assertEqual(inst.lensSpecification[0].power, -2.75)
        self.assertEqual(inst.lensSpecification[0].product.coding[0].code, "contact")
        self.assertEqual(inst.lensSpecification[0].product.coding[0].system, "http://terminology.hl7.org/CodeSystem/ex-visionprescriptionproduct")
        self.assertEqual(inst.lensSpecification[1].add, 1.75)
        self.assertEqual(inst.lensSpecification[1].axis, 160)
        self.assertEqual(inst.lensSpecification[1].backCurve, 8.7)
        self.assertEqual(inst.lensSpecification[1].brand, "OphthaGuard")
        self.assertEqual(inst.lensSpecification[1].color, "green")
        self.assertEqual(inst.lensSpecification[1].cylinder, -3.5)
        self.assertEqual(inst.lensSpecification[1].diameter, 14.0)
        self.assertEqual(inst.lensSpecification[1].duration.code, "month")
        self.assertEqual(inst.lensSpecification[1].duration.system, "http://unitsofmeasure.org")
        self.assertEqual(inst.lensSpecification[1].duration.unit, "month")
        self.assertEqual(inst.lensSpecification[1].duration.value, 1)
        self.assertEqual(inst.lensSpecification[1].eye, "left")
        self.assertEqual(inst.lensSpecification[1].note[0].text, "Shade treatment for extreme light sensitivity")
        self.assertEqual(inst.lensSpecification[1].power, -2.75)
        self.assertEqual(inst.lensSpecification[1].product.coding[0].code, "contact")
        self.assertEqual(inst.lensSpecification[1].product.coding[0].system, "http://terminology.hl7.org/CodeSystem/ex-visionprescriptionproduct")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.status, "active")
        self.assertEqual(inst.text.div, "<div xmlns=\"http://www.w3.org/1999/xhtml\">Sample Contract Lens prescription</div>")
        self.assertEqual(inst.text.status, "generated")
    
    def testVisionPrescription2(self):
        inst = self.instantiate_from("visionprescription-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a VisionPrescription instance")
        self.implVisionPrescription2(inst)
        
        js = inst.as_json()
        self.assertEqual("VisionPrescription", js["resourceType"])
        inst2 = visionprescription.VisionPrescription(js)
        self.implVisionPrescription2(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implVisionPrescription2(self, inst):
        self.assertEqual(inst.created.date, FHIRDate("2014-06-15").date)
        self.assertEqual(inst.created.as_json(), "2014-06-15")
        self.assertEqual(inst.dateWritten.date, FHIRDate("2014-06-15").date)
        self.assertEqual(inst.dateWritten.as_json(), "2014-06-15")
        self.assertEqual(inst.id, "33123")
        self.assertEqual(inst.identifier[0].system, "http://www.happysight.com/prescription")
        self.assertEqual(inst.identifier[0].value, "15013")
        self.assertEqual(inst.lensSpecification[0].add, 2.0)
        self.assertEqual(inst.lensSpecification[0].eye, "right")
        self.assertEqual(inst.lensSpecification[0].prism[0].amount, 0.5)
        self.assertEqual(inst.lensSpecification[0].prism[0].base, "down")
        self.assertEqual(inst.lensSpecification[0].product.coding[0].code, "lens")
        self.assertEqual(inst.lensSpecification[0].product.coding[0].system, "http://terminology.hl7.org/CodeSystem/ex-visionprescriptionproduct")
        self.assertEqual(inst.lensSpecification[0].sphere, -2.0)
        self.assertEqual(inst.lensSpecification[1].add, 2.0)
        self.assertEqual(inst.lensSpecification[1].axis, 180)
        self.assertEqual(inst.lensSpecification[1].cylinder, -0.5)
        self.assertEqual(inst.lensSpecification[1].eye, "left")
        self.assertEqual(inst.lensSpecification[1].prism[0].amount, 0.5)
        self.assertEqual(inst.lensSpecification[1].prism[0].base, "up")
        self.assertEqual(inst.lensSpecification[1].product.coding[0].code, "lens")
        self.assertEqual(inst.lensSpecification[1].product.coding[0].system, "http://terminology.hl7.org/CodeSystem/ex-visionprescriptionproduct")
        self.assertEqual(inst.lensSpecification[1].sphere, -1.0)
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.status, "active")
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