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

from . import medicinalproduct

from .fhirdate import FHIRDate
import logging


class MedicinalProductTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("MedicinalProduct", js["resourceType"])
        return medicinalproduct.MedicinalProduct(js)
    
    def testMedicinalProduct1(self):
        inst = self.instantiate_from("medicinalproduct-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a MedicinalProduct instance")
        self.implMedicinalProduct1(inst)
        
        js = inst.as_json()
        self.assertEqual("MedicinalProduct", js["resourceType"])
        inst2 = medicinalproduct.MedicinalProduct(js)
        self.implMedicinalProduct1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implMedicinalProduct1(self, inst):
        self.assertEqual(inst.id, "example")
        self.assertEqual(inst.identifier[0].system, "http://ema.europa.eu/example/MPID")
        self.assertEqual(inst.identifier[0].value, "{mpid}")
        self.assertEqual(inst.manufacturingBusinessOperation[0].authorisationReferenceNumber.system, "http://ema.europa.eu/example/manufacturingAuthorisationReferenceNumber")
        self.assertEqual(inst.manufacturingBusinessOperation[0].authorisationReferenceNumber.value, "1324TZ")
        self.assertEqual(inst.manufacturingBusinessOperation[0].effectiveDate.date, FHIRDate("2013-03-15").date)
        self.assertEqual(inst.manufacturingBusinessOperation[0].effectiveDate.as_json(), "2013-03-15")
        self.assertEqual(inst.manufacturingBusinessOperation[0].operationType.coding[0].code, "Batchrelease")
        self.assertEqual(inst.manufacturingBusinessOperation[0].operationType.coding[0].system, "http://ema.europa.eu/example/manufacturingOperationType")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.name[0].countryLanguage[0].country.coding[0].code, "EU")
        self.assertEqual(inst.name[0].countryLanguage[0].country.coding[0].system, "http://ema.europa.eu/example/countryCode")
        self.assertEqual(inst.name[0].countryLanguage[0].jurisdiction.coding[0].code, "EU")
        self.assertEqual(inst.name[0].countryLanguage[0].jurisdiction.coding[0].system, "http://ema.europa.eu/example/jurisdictionCode")
        self.assertEqual(inst.name[0].countryLanguage[0].language.coding[0].code, "EN")
        self.assertEqual(inst.name[0].countryLanguage[0].language.coding[0].system, "http://ema.europa.eu/example/languageCode")
        self.assertEqual(inst.name[0].namePart[0].part, "Equilidem")
        self.assertEqual(inst.name[0].namePart[0].type.code, "INV")
        self.assertEqual(inst.name[0].namePart[1].part, "2.5 mg")
        self.assertEqual(inst.name[0].namePart[1].type.code, "STR")
        self.assertEqual(inst.name[0].namePart[2].part, "film-coated tablets")
        self.assertEqual(inst.name[0].namePart[2].type.code, "FRM")
        self.assertEqual(inst.name[0].productName, "Equilidem 2.5 mg film-coated tablets")
        self.assertEqual(inst.productClassification[0].coding[0].code, "WHOAnatomicalTherapeuticChemicalATCClassificationSystem|B01AF02")
        self.assertEqual(inst.productClassification[0].coding[0].system, "http://ema.europa.eu/example/WHOAnatomicalTherapeuticChemicalATCClassificationSystem")
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