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

from . import organizationaffiliation

from .fhirdate import FHIRDate
import logging


class OrganizationAffiliationTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("OrganizationAffiliation", js["resourceType"])
        return organizationaffiliation.OrganizationAffiliation(js)
    
    def testOrganizationAffiliation1(self):
        inst = self.instantiate_from("organizationaffiliation-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a OrganizationAffiliation instance")
        self.implOrganizationAffiliation1(inst)
        
        js = inst.as_json()
        self.assertEqual("OrganizationAffiliation", js["resourceType"])
        inst2 = organizationaffiliation.OrganizationAffiliation(js)
        self.implOrganizationAffiliation1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implOrganizationAffiliation1(self, inst):
        self.assertTrue(inst.active)
        self.assertEqual(inst.code[0].coding[0].code, "provider")
        self.assertEqual(inst.code[0].coding[0].system, "http://terminology.hl7.org/CodeSystem/organization-role")
        self.assertEqual(inst.id, "example")
        self.assertEqual(inst.identifier[0].system, "http://www.acme.org/practitioners")
        self.assertEqual(inst.identifier[0].value, "23")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.period.end.date, FHIRDate("2012-03-31").date)
        self.assertEqual(inst.period.end.as_json(), "2012-03-31")
        self.assertEqual(inst.period.start.date, FHIRDate("2012-01-01").date)
        self.assertEqual(inst.period.start.as_json(), "2012-01-01")
        self.assertEqual(inst.specialty[0].coding[0].code, "408443003")
        self.assertEqual(inst.specialty[0].coding[0].display, "General medical practice")
        self.assertEqual(inst.specialty[0].coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.telecom[0].system, "email")
        self.assertEqual(inst.telecom[0].use, "work")
        self.assertEqual(inst.telecom[0].value, "general.practice@example.org")
        self.assertEqual(inst.text.status, "generated")
    
    def testOrganizationAffiliation2(self):
        inst = self.instantiate_from("orgrole-example-hie.json")
        self.assertIsNotNone(inst, "Must have instantiated a OrganizationAffiliation instance")
        self.implOrganizationAffiliation2(inst)
        
        js = inst.as_json()
        self.assertEqual("OrganizationAffiliation", js["resourceType"])
        inst2 = organizationaffiliation.OrganizationAffiliation(js)
        self.implOrganizationAffiliation2(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implOrganizationAffiliation2(self, inst):
        self.assertTrue(inst.active)
        self.assertEqual(inst.code[0].coding[0].code, "member")
        self.assertEqual(inst.code[0].coding[0].display, "Member")
        self.assertEqual(inst.code[0].coding[0].system, "http://hl7.org/fhir/organization-role")
        self.assertEqual(inst.code[0].text, "Hospital member")
        self.assertEqual(inst.id, "orgrole2")
        self.assertEqual(inst.identifier[0].system, "http://example.org/www.monumentHIE.com")
        self.assertEqual(inst.identifier[0].type.text, "member hospital")
        self.assertEqual(inst.identifier[0].use, "secondary")
        self.assertEqual(inst.identifier[0].value, "hosp32")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.text.status, "generated")
    
    def testOrganizationAffiliation3(self):
        inst = self.instantiate_from("orgrole-example-services.json")
        self.assertIsNotNone(inst, "Must have instantiated a OrganizationAffiliation instance")
        self.implOrganizationAffiliation3(inst)
        
        js = inst.as_json()
        self.assertEqual("OrganizationAffiliation", js["resourceType"])
        inst2 = organizationaffiliation.OrganizationAffiliation(js)
        self.implOrganizationAffiliation3(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implOrganizationAffiliation3(self, inst):
        self.assertTrue(inst.active)
        self.assertEqual(inst.code[0].coding[0].code, "provider")
        self.assertEqual(inst.code[0].coding[0].display, "Provider")
        self.assertEqual(inst.code[0].coding[0].system, "http://hl7.org/fhir/organization-role")
        self.assertTrue(inst.code[0].coding[0].userSelected)
        self.assertEqual(inst.code[0].text, "Provider of rehabilitation services")
        self.assertEqual(inst.id, "orgrole1")
        self.assertEqual(inst.identifier[0].system, "http://example.org/www.foundingfathersmemorial.com")
        self.assertEqual(inst.identifier[0].use, "secondary")
        self.assertEqual(inst.identifier[0].value, "service002")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.period.end.date, FHIRDate("2022-02-01").date)
        self.assertEqual(inst.period.end.as_json(), "2022-02-01")
        self.assertEqual(inst.period.start.date, FHIRDate("2018-02-09").date)
        self.assertEqual(inst.period.start.as_json(), "2018-02-09")
        self.assertEqual(inst.specialty[0].coding[0].code, "394602003")
        self.assertEqual(inst.specialty[0].coding[0].display, "Rehabilitation - specialty")
        self.assertEqual(inst.specialty[0].coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.specialty[0].text, "Rehabilitation")
        self.assertEqual(inst.telecom[0].system, "phone")
        self.assertEqual(inst.telecom[0].use, "work")
        self.assertEqual(inst.telecom[0].value, "202-109-8765")
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