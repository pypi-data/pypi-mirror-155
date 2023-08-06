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

from . import medicinalproductauthorization

from .fhirdate import FHIRDate
import logging


class MedicinalProductAuthorizationTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("MedicinalProductAuthorization", js["resourceType"])
        return medicinalproductauthorization.MedicinalProductAuthorization(js)
    
    def testMedicinalProductAuthorization1(self):
        inst = self.instantiate_from("medicinalproductauthorization-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a MedicinalProductAuthorization instance")
        self.implMedicinalProductAuthorization1(inst)
        
        js = inst.as_json()
        self.assertEqual("MedicinalProductAuthorization", js["resourceType"])
        inst2 = medicinalproductauthorization.MedicinalProductAuthorization(js)
        self.implMedicinalProductAuthorization1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implMedicinalProductAuthorization1(self, inst):
        self.assertEqual(inst.country[0].coding[0].code, "EU")
        self.assertEqual(inst.country[0].coding[0].system, "http://ema.europa.eu/example/country")
        self.assertEqual(inst.dataExclusivityPeriod.end.date, FHIRDate("2020-08-15").date)
        self.assertEqual(inst.dataExclusivityPeriod.end.as_json(), "2020-08-15")
        self.assertEqual(inst.dataExclusivityPeriod.start.date, FHIRDate("2010-08-15").date)
        self.assertEqual(inst.dataExclusivityPeriod.start.as_json(), "2010-08-15")
        self.assertEqual(inst.dateOfFirstAuthorization.date, FHIRDate("2010-08-15").date)
        self.assertEqual(inst.dateOfFirstAuthorization.as_json(), "2010-08-15")
        self.assertEqual(inst.id, "example")
        self.assertEqual(inst.identifier[0].system, "http://ema.europa.eu/example/marketingAuthorisationNumber")
        self.assertEqual(inst.identifier[0].value, "EU/1/11/999/001")
        self.assertEqual(inst.internationalBirthDate.date, FHIRDate("2010-08-15").date)
        self.assertEqual(inst.internationalBirthDate.as_json(), "2010-08-15")
        self.assertEqual(inst.jurisdictionalAuthorization[0].country.coding[0].code, "NO")
        self.assertEqual(inst.jurisdictionalAuthorization[0].country.coding[0].system, "http://ema.europa.eu/example/countryCode")
        self.assertEqual(inst.jurisdictionalAuthorization[0].id, "1")
        self.assertEqual(inst.jurisdictionalAuthorization[0].identifier[0].system, "http://ema.europa.eu/example/marketingauthorisationnumber")
        self.assertEqual(inst.jurisdictionalAuthorization[0].identifier[0].value, "123-456-789")
        self.assertEqual(inst.jurisdictionalAuthorization[1].country.coding[0].code, "NO")
        self.assertEqual(inst.jurisdictionalAuthorization[1].country.coding[0].system, "http://ema.europa.eu/example/countryCode")
        self.assertEqual(inst.jurisdictionalAuthorization[1].id, "2")
        self.assertEqual(inst.jurisdictionalAuthorization[1].identifier[0].system, "http://ema.europa.eu/example/marketingauthorisationnumber")
        self.assertEqual(inst.jurisdictionalAuthorization[1].identifier[0].value, "123-456-123")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.procedure.application[0].dateDateTime.date, FHIRDate("2015-08-01").date)
        self.assertEqual(inst.procedure.application[0].dateDateTime.as_json(), "2015-08-01")
        self.assertEqual(inst.procedure.application[0].identifier.system, "http://ema.europa.eu/example/applicationidentifier-number")
        self.assertEqual(inst.procedure.application[0].identifier.value, "IA38G")
        self.assertEqual(inst.procedure.application[0].type.coding[0].code, "GroupTypeIAVariationNotification")
        self.assertEqual(inst.procedure.application[0].type.coding[0].system, "http://ema.europa.eu/example/marketingAuthorisationApplicationType")
        self.assertEqual(inst.procedure.datePeriod.end.date, FHIRDate("2015-08-21").date)
        self.assertEqual(inst.procedure.datePeriod.end.as_json(), "2015-08-21")
        self.assertEqual(inst.procedure.datePeriod.start.date, FHIRDate("2015-08-02").date)
        self.assertEqual(inst.procedure.datePeriod.start.as_json(), "2015-08-02")
        self.assertEqual(inst.procedure.identifier.system, "http://ema.europa.eu/example/procedureidentifier-number")
        self.assertEqual(inst.procedure.identifier.value, "EMEA/H/C/009999/IA/0099/G")
        self.assertEqual(inst.procedure.type.coding[0].code, "VariationTypeIA")
        self.assertEqual(inst.procedure.type.coding[0].system, "http://ema.europa.eu/example/marketingAuthorisationProcedureType")
        self.assertEqual(inst.status.coding[0].code, "active")
        self.assertEqual(inst.status.coding[0].system, "http://ema.europa.eu/example/authorisationstatus")
        self.assertEqual(inst.statusDate.date, FHIRDate("2015-01-14").date)
        self.assertEqual(inst.statusDate.as_json(), "2015-01-14")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.validityPeriod.end.date, FHIRDate("2020-05-20").date)
        self.assertEqual(inst.validityPeriod.end.as_json(), "2020-05-20")
        self.assertEqual(inst.validityPeriod.start.date, FHIRDate("2015-08-16").date)
        self.assertEqual(inst.validityPeriod.start.as_json(), "2015-08-16")

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