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

from . import chargeitem

from .fhirdate import FHIRDate
import logging


class ChargeItemTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("ChargeItem", js["resourceType"])
        return chargeitem.ChargeItem(js)
    
    def testChargeItem1(self):
        inst = self.instantiate_from("chargeitem-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a ChargeItem instance")
        self.implChargeItem1(inst)
        
        js = inst.as_json()
        self.assertEqual("ChargeItem", js["resourceType"])
        inst2 = chargeitem.ChargeItem(js)
        self.implChargeItem1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implChargeItem1(self, inst):
        self.assertEqual(inst.code.coding[0].code, "01510")
        self.assertEqual(inst.code.coding[0].display, "Zusatzpauschale für Beobachtung nach diagnostischer Koronarangiografie")
        self.assertEqual(inst.definitionUri[0], "http://www.kbv.de/tools/ebm/html/01520_2904360860826220813632.html")
        self.assertEqual(inst.enteredDate.date, FHIRDate("2017-01-25T23:55:04+01:00").date)
        self.assertEqual(inst.enteredDate.as_json(), "2017-01-25T23:55:04+01:00")
        self.assertEqual(inst.factorOverride, 0.8)
        self.assertEqual(inst.id, "example")
        self.assertEqual(inst.identifier[0].system, "http://myHospital.org/ChargeItems")
        self.assertEqual(inst.identifier[0].value, "654321")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.note[0].text, "The code is only applicable for periods longer than 4h")
        self.assertEqual(inst.note[0].time.date, FHIRDate("2017-01-25T23:55:04+01:00").date)
        self.assertEqual(inst.note[0].time.as_json(), "2017-01-25T23:55:04+01:00")
        self.assertEqual(inst.occurrencePeriod.end.date, FHIRDate("2017-01-25T12:35:00+01:00").date)
        self.assertEqual(inst.occurrencePeriod.end.as_json(), "2017-01-25T12:35:00+01:00")
        self.assertEqual(inst.occurrencePeriod.start.date, FHIRDate("2017-01-25T08:00:00+01:00").date)
        self.assertEqual(inst.occurrencePeriod.start.as_json(), "2017-01-25T08:00:00+01:00")
        self.assertEqual(inst.overrideReason, "Patient is Cardiologist's golf buddy, so he gets a 20% discount!")
        self.assertEqual(inst.performer[0].function.coding[0].code, "17561000")
        self.assertEqual(inst.performer[0].function.coding[0].display, "Cardiologist")
        self.assertEqual(inst.performer[0].function.coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.performer[1].function.coding[0].code, "224542009")
        self.assertEqual(inst.performer[1].function.coding[0].display, "Coronary Care Nurse")
        self.assertEqual(inst.performer[1].function.coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.priceOverride.currency, "EUR")
        self.assertEqual(inst.priceOverride.value, 40)
        self.assertEqual(inst.quantity.value, 1)
        self.assertEqual(inst.reason[0].coding[0].code, "123456")
        self.assertEqual(inst.reason[0].coding[0].display, "DIAG-1")
        self.assertEqual(inst.reason[0].coding[0].system, "http://hl7.org/fhir/sid/icd-10")
        self.assertEqual(inst.status, "billable")
        self.assertEqual(inst.text.div, "<div xmlns=\"http://www.w3.org/1999/xhtml\">Example of ChargeItem Usage in Context of the German EBM Billing code system</div>")
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