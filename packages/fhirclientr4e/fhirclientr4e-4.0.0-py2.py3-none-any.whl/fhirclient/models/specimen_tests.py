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

from . import specimen

from .fhirdate import FHIRDate
import logging


class SpecimenTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("Specimen", js["resourceType"])
        return specimen.Specimen(js)
    
    def testSpecimen1(self):
        inst = self.instantiate_from("specimen-example-isolate.json")
        self.assertIsNotNone(inst, "Must have instantiated a Specimen instance")
        self.implSpecimen1(inst)
        
        js = inst.as_json()
        self.assertEqual("Specimen", js["resourceType"])
        inst2 = specimen.Specimen(js)
        self.implSpecimen1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implSpecimen1(self, inst):
        self.assertEqual(inst.accessionIdentifier.system, "http://lab.acme.org/specimens/2011")
        self.assertEqual(inst.accessionIdentifier.value, "X352356-ISO1")
        self.assertEqual(inst.collection.collectedDateTime.date, FHIRDate("2015-08-16T07:03:00Z").date)
        self.assertEqual(inst.collection.collectedDateTime.as_json(), "2015-08-16T07:03:00Z")
        self.assertEqual(inst.collection.method.coding[0].code, "BAP")
        self.assertEqual(inst.collection.method.coding[0].system, "http://terminology.hl7.org/CodeSystem/v2-0488")
        self.assertEqual(inst.contained[0].id, "stool")
        self.assertEqual(inst.id, "isolate")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.note[0].text, "Patient dropped off specimen")
        self.assertEqual(inst.receivedTime.date, FHIRDate("2015-08-18T07:03:00Z").date)
        self.assertEqual(inst.receivedTime.as_json(), "2015-08-18T07:03:00Z")
        self.assertEqual(inst.status, "available")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.type.coding[0].code, "429951000124103")
        self.assertEqual(inst.type.coding[0].display, "Bacterial isolate specimen")
        self.assertEqual(inst.type.coding[0].system, "http://snomed.info/sct")
    
    def testSpecimen2(self):
        inst = self.instantiate_from("specimen-example-pooled-serum.json")
        self.assertIsNotNone(inst, "Must have instantiated a Specimen instance")
        self.implSpecimen2(inst)
        
        js = inst.as_json()
        self.assertEqual("Specimen", js["resourceType"])
        inst2 = specimen.Specimen(js)
        self.implSpecimen2(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implSpecimen2(self, inst):
        self.assertEqual(inst.accessionIdentifier.system, "https://vetmed.iastate.edu/vdl")
        self.assertEqual(inst.accessionIdentifier.value, "20171120-1234")
        self.assertEqual(inst.collection.collectedDateTime.date, FHIRDate("2017-11-14").date)
        self.assertEqual(inst.collection.collectedDateTime.as_json(), "2017-11-14")
        self.assertEqual(inst.container[0].type.coding[0].code, "RTT")
        self.assertEqual(inst.container[0].type.coding[0].display, "Red Top Tube")
        self.assertEqual(inst.container[0].type.coding[0].system, "https://vetmed.iastate.edu/vdl")
        self.assertEqual(inst.container[0].type.text, "Red Top Blood Collection Tube")
        self.assertEqual(inst.id, "pooled-serum")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.note[0].text, "Pooled serum sample from 30 individuals")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.type.coding[0].code, "Serum sample, pooled")
        self.assertEqual(inst.type.coding[0].display, "Serum sample, pooled")
        self.assertEqual(inst.type.coding[0].system, "https://vetmed.iastate.edu/vdl")
        self.assertEqual(inst.type.text, "Pooled serum sample")
    
    def testSpecimen3(self):
        inst = self.instantiate_from("specimen-example-urine.json")
        self.assertIsNotNone(inst, "Must have instantiated a Specimen instance")
        self.implSpecimen3(inst)
        
        js = inst.as_json()
        self.assertEqual("Specimen", js["resourceType"])
        inst2 = specimen.Specimen(js)
        self.implSpecimen3(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implSpecimen3(self, inst):
        self.assertEqual(inst.accessionIdentifier.system, "http://lab.acme.org/specimens/2015")
        self.assertEqual(inst.accessionIdentifier.value, "X352356")
        self.assertEqual(inst.collection.collectedDateTime.date, FHIRDate("2015-08-18T07:03:00Z").date)
        self.assertEqual(inst.collection.collectedDateTime.as_json(), "2015-08-18T07:03:00Z")
        self.assertEqual(inst.container[0].capacity.unit, "mls")
        self.assertEqual(inst.container[0].capacity.value, 50)
        self.assertEqual(inst.container[0].specimenQuantity.unit, "mls")
        self.assertEqual(inst.container[0].specimenQuantity.value, 10)
        self.assertEqual(inst.container[0].type.text, "Non-sterile specimen container")
        self.assertEqual(inst.id, "vma-urine")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.processing[0].description, "Acidify to pH < 3.0 with 6 N HCl.")
        self.assertEqual(inst.processing[0].procedure.coding[0].code, "ACID")
        self.assertEqual(inst.processing[0].procedure.coding[0].system, "http://terminology.hl7.org/CodeSystem/v2-0373")
        self.assertEqual(inst.processing[0].timeDateTime.date, FHIRDate("2015-08-18T08:10:00Z").date)
        self.assertEqual(inst.processing[0].timeDateTime.as_json(), "2015-08-18T08:10:00Z")
        self.assertEqual(inst.receivedTime.date, FHIRDate("2015-08-18T07:03:00Z").date)
        self.assertEqual(inst.receivedTime.as_json(), "2015-08-18T07:03:00Z")
        self.assertEqual(inst.status, "available")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.type.coding[0].code, "RANDU")
        self.assertEqual(inst.type.coding[0].display, "Urine, Random")
        self.assertEqual(inst.type.coding[0].system, "http://terminology.hl7.org/CodeSystem/v2-0487")
    
    def testSpecimen4(self):
        inst = self.instantiate_from("specimen-example-serum.json")
        self.assertIsNotNone(inst, "Must have instantiated a Specimen instance")
        self.implSpecimen4(inst)
        
        js = inst.as_json()
        self.assertEqual("Specimen", js["resourceType"])
        inst2 = specimen.Specimen(js)
        self.implSpecimen4(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implSpecimen4(self, inst):
        self.assertEqual(inst.accessionIdentifier.system, "http://acme.com/labs/accession-ids")
        self.assertEqual(inst.accessionIdentifier.value, "20150816-00124")
        self.assertEqual(inst.collection.collectedDateTime.date, FHIRDate("2015-08-16T06:40:17Z").date)
        self.assertEqual(inst.collection.collectedDateTime.as_json(), "2015-08-16T06:40:17Z")
        self.assertEqual(inst.container[0].type.coding[0].code, "SST")
        self.assertEqual(inst.container[0].type.coding[0].display, "Serum Separator Tube")
        self.assertEqual(inst.container[0].type.coding[0].system, "http://acme.com/labs")
        self.assertEqual(inst.id, "sst")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.type.coding[0].code, "119364003")
        self.assertEqual(inst.type.coding[0].display, "Serum sample")
        self.assertEqual(inst.type.coding[0].system, "http://snomed.info/sct")
    
    def testSpecimen5(self):
        inst = self.instantiate_from("specimen-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a Specimen instance")
        self.implSpecimen5(inst)
        
        js = inst.as_json()
        self.assertEqual("Specimen", js["resourceType"])
        inst2 = specimen.Specimen(js)
        self.implSpecimen5(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implSpecimen5(self, inst):
        self.assertEqual(inst.accessionIdentifier.system, "http://lab.acme.org/specimens/2011")
        self.assertEqual(inst.accessionIdentifier.value, "X352356")
        self.assertEqual(inst.collection.bodySite.coding[0].code, "49852007")
        self.assertEqual(inst.collection.bodySite.coding[0].display, "Structure of median cubital vein (body structure)")
        self.assertEqual(inst.collection.bodySite.coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.collection.bodySite.text, "Right median cubital vein")
        self.assertEqual(inst.collection.collectedDateTime.date, FHIRDate("2011-05-30T06:15:00Z").date)
        self.assertEqual(inst.collection.collectedDateTime.as_json(), "2011-05-30T06:15:00Z")
        self.assertEqual(inst.collection.method.coding[0].code, "LNV")
        self.assertEqual(inst.collection.method.coding[0].system, "http://terminology.hl7.org/CodeSystem/v2-0488")
        self.assertEqual(inst.collection.quantity.unit, "mL")
        self.assertEqual(inst.collection.quantity.value, 6)
        self.assertEqual(inst.contained[0].id, "hep")
        self.assertEqual(inst.container[0].capacity.unit, "mL")
        self.assertEqual(inst.container[0].capacity.value, 10)
        self.assertEqual(inst.container[0].description, "Green Gel tube")
        self.assertEqual(inst.container[0].identifier[0].value, "48736-15394-75465")
        self.assertEqual(inst.container[0].specimenQuantity.unit, "mL")
        self.assertEqual(inst.container[0].specimenQuantity.value, 6)
        self.assertEqual(inst.container[0].type.text, "Vacutainer")
        self.assertEqual(inst.id, "101")
        self.assertEqual(inst.identifier[0].system, "http://ehr.acme.org/identifiers/collections")
        self.assertEqual(inst.identifier[0].value, "23234352356")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.note[0].text, "Specimen is grossly lipemic")
        self.assertEqual(inst.receivedTime.date, FHIRDate("2011-03-04T07:03:00Z").date)
        self.assertEqual(inst.receivedTime.as_json(), "2011-03-04T07:03:00Z")
        self.assertEqual(inst.status, "available")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.type.coding[0].code, "122555007")
        self.assertEqual(inst.type.coding[0].display, "Venous blood specimen")
        self.assertEqual(inst.type.coding[0].system, "http://snomed.info/sct")

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