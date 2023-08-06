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

from . import chargeitemdefinition

from .fhirdate import FHIRDate
import logging


class ChargeItemDefinitionTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("ChargeItemDefinition", js["resourceType"])
        return chargeitemdefinition.ChargeItemDefinition(js)
    
    def testChargeItemDefinition1(self):
        inst = self.instantiate_from("chargeitemdefinition-device-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a ChargeItemDefinition instance")
        self.implChargeItemDefinition1(inst)
        
        js = inst.as_json()
        self.assertEqual("ChargeItemDefinition", js["resourceType"])
        inst2 = chargeitemdefinition.ChargeItemDefinition(js)
        self.implChargeItemDefinition1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implChargeItemDefinition1(self, inst):
        self.assertEqual(inst.applicability[0].description, "Verify ChargeItem pertains to Device 12345")
        self.assertEqual(inst.applicability[0].expression, "%context.service.suppliedItem='Device/12345'")
        self.assertEqual(inst.applicability[0].language, "text/fhirpath")
        self.assertEqual(inst.description, "Financial details for  custom made device")
        self.assertEqual(inst.id, "device")
        self.assertEqual(inst.propertyGroup[0].priceComponent[0].amount.currency, "EUR")
        self.assertEqual(inst.propertyGroup[0].priceComponent[0].amount.value, 67.44)
        self.assertEqual(inst.propertyGroup[0].priceComponent[0].code.coding[0].code, "VK")
        self.assertEqual(inst.propertyGroup[0].priceComponent[0].code.coding[0].display, "Verkaufspreis (netto)")
        self.assertEqual(inst.propertyGroup[0].priceComponent[0].code.coding[0].system, "http://fhir.de/CodeSystem/billing-attributes")
        self.assertEqual(inst.propertyGroup[0].priceComponent[0].type, "base")
        self.assertEqual(inst.propertyGroup[1].applicability[0].description, "Gültigkeit Steuersatz")
        self.assertEqual(inst.propertyGroup[1].applicability[0].expression, "%context.occurenceDateTime > '2018-04-01'")
        self.assertEqual(inst.propertyGroup[1].applicability[0].language, "text/fhirpath")
        self.assertEqual(inst.propertyGroup[1].priceComponent[0].code.coding[0].code, "MWST")
        self.assertEqual(inst.propertyGroup[1].priceComponent[0].code.coding[0].display, "Mehrwersteuersatz")
        self.assertEqual(inst.propertyGroup[1].priceComponent[0].code.coding[0].system, "http://fhir.de/CodeSystem/billing-attributes")
        self.assertEqual(inst.propertyGroup[1].priceComponent[0].factor, 1.19)
        self.assertEqual(inst.propertyGroup[1].priceComponent[0].type, "tax")
        self.assertEqual(inst.propertyGroup[2].applicability[0].description, "Gültigkeit Steuersatz")
        self.assertEqual(inst.propertyGroup[2].applicability[0].expression, "%context.occurenceDateTime <= '2018-04-01'")
        self.assertEqual(inst.propertyGroup[2].applicability[0].language, "text/fhirpath")
        self.assertEqual(inst.propertyGroup[2].priceComponent[0].code.coding[0].code, "MWST")
        self.assertEqual(inst.propertyGroup[2].priceComponent[0].code.coding[0].display, "Mehrwersteuersatz")
        self.assertEqual(inst.propertyGroup[2].priceComponent[0].code.coding[0].system, "http://fhir.de/CodeSystem/billing-attributes")
        self.assertEqual(inst.propertyGroup[2].priceComponent[0].factor, 1.07)
        self.assertEqual(inst.propertyGroup[2].priceComponent[0].type, "tax")
        self.assertEqual(inst.status, "active")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.url, "http://sap.org/ChargeItemDefinition/device-123")
    
    def testChargeItemDefinition2(self):
        inst = self.instantiate_from("chargeitemdefinition-ebm-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a ChargeItemDefinition instance")
        self.implChargeItemDefinition2(inst)
        
        js = inst.as_json()
        self.assertEqual("ChargeItemDefinition", js["resourceType"])
        inst2 = chargeitemdefinition.ChargeItemDefinition(js)
        self.implChargeItemDefinition2(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implChargeItemDefinition2(self, inst):
        self.assertEqual(inst.applicability[0].description, "Excludes billing code 13250 for same Encounter")
        self.assertEqual(inst.applicability[0].expression, "[some CQL expression]")
        self.assertEqual(inst.applicability[0].language, "text/cql")
        self.assertEqual(inst.applicability[1].description, "Applies only once per Encounter")
        self.assertEqual(inst.applicability[1].expression, "[some CQL expression]")
        self.assertEqual(inst.applicability[1].language, "text/CQL")
        self.assertEqual(inst.code.coding[0].code, "30110")
        self.assertEqual(inst.code.coding[0].display, "Allergologiediagnostik I")
        self.assertEqual(inst.code.coding[0].system, "http://fhir.de/CodingSystem/kbv/ebm")
        self.assertEqual(inst.description, "Allergologisch-diagnostischer Komplex zur Diagnostik und/oder zum Ausschluss einer (Kontakt-)Allergie vom Spättyp (Typ IV), einschl. Kosten")
        self.assertEqual(inst.effectivePeriod.end.date, FHIRDate("2018-06-30").date)
        self.assertEqual(inst.effectivePeriod.end.as_json(), "2018-06-30")
        self.assertEqual(inst.effectivePeriod.start.date, FHIRDate("2018-04-01").date)
        self.assertEqual(inst.effectivePeriod.start.as_json(), "2018-04-01")
        self.assertEqual(inst.id, "ebm")
        self.assertEqual(inst.propertyGroup[0].priceComponent[0].amount.currency, "EUR")
        self.assertEqual(inst.propertyGroup[0].priceComponent[0].amount.value, 67.44)
        self.assertEqual(inst.propertyGroup[0].priceComponent[0].code.coding[0].code, "gesamt-euro")
        self.assertEqual(inst.propertyGroup[0].priceComponent[0].code.coding[0].display, "Gesamt (Euro)")
        self.assertEqual(inst.propertyGroup[0].priceComponent[0].code.coding[0].system, "http://fhir.de/CodeSystem/kbv/ebm-attribute")
        self.assertEqual(inst.propertyGroup[0].priceComponent[0].type, "base")
        self.assertEqual(inst.propertyGroup[0].priceComponent[1].code.coding[0].code, "gesamt-punkte")
        self.assertEqual(inst.propertyGroup[0].priceComponent[1].code.coding[0].display, "Gesamt (Punkte)")
        self.assertEqual(inst.propertyGroup[0].priceComponent[1].code.coding[0].system, "http://fhir.de/CodeSystem/kbv/ebm-attribute")
        self.assertEqual(inst.propertyGroup[0].priceComponent[1].factor, 633)
        self.assertEqual(inst.propertyGroup[0].priceComponent[1].type, "informational")
        self.assertEqual(inst.status, "active")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.url, "http://fhir.de/ChargeItemDefinition/kbv/ebm-30110")
        self.assertEqual(inst.version, "2-2018")

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