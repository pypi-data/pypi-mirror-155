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

from . import endpoint

from .fhirdate import FHIRDate
import logging


class EndpointTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("Endpoint", js["resourceType"])
        return endpoint.Endpoint(js)
    
    def testEndpoint1(self):
        inst = self.instantiate_from("endpoint-example-iid.json")
        self.assertIsNotNone(inst, "Must have instantiated a Endpoint instance")
        self.implEndpoint1(inst)
        
        js = inst.as_json()
        self.assertEqual("Endpoint", js["resourceType"])
        inst2 = endpoint.Endpoint(js)
        self.implEndpoint1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implEndpoint1(self, inst):
        self.assertEqual(inst.address, "https://pacs.hospital.org/IHEInvokeImageDisplay")
        self.assertEqual(inst.connectionType.code, "ihe-iid")
        self.assertEqual(inst.connectionType.system, "http://terminology.hl7.org/CodeSystem/endpoint-connection-type")
        self.assertEqual(inst.id, "example-iid")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.name, "PACS Hospital Invoke Image Display endpoint")
        self.assertEqual(inst.payloadType[0].text, "DICOM IID")
        self.assertEqual(inst.status, "active")
        self.assertEqual(inst.text.status, "generated")
    
    def testEndpoint2(self):
        inst = self.instantiate_from("endpoint-example-direct.json")
        self.assertIsNotNone(inst, "Must have instantiated a Endpoint instance")
        self.implEndpoint2(inst)
        
        js = inst.as_json()
        self.assertEqual("Endpoint", js["resourceType"])
        inst2 = endpoint.Endpoint(js)
        self.implEndpoint2(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implEndpoint2(self, inst):
        self.assertEqual(inst.address, "mailto:MARTIN.SMIETANKA@directnppes.com")
        self.assertEqual(inst.connectionType.code, "direct-project")
        self.assertEqual(inst.id, "direct-endpoint")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.name, "MARTIN SMIETANKA")
        self.assertEqual(inst.payloadType[0].coding[0].code, "urn:hl7-org:sdwg:ccda-structuredBody:1.1")
        self.assertEqual(inst.payloadType[0].coding[0].system, "urn:oid:1.3.6.1.4.1.19376.1.2.3")
        self.assertEqual(inst.status, "active")
        self.assertEqual(inst.text.status, "generated")
    
    def testEndpoint3(self):
        inst = self.instantiate_from("endpoint-example-wadors.json")
        self.assertIsNotNone(inst, "Must have instantiated a Endpoint instance")
        self.implEndpoint3(inst)
        
        js = inst.as_json()
        self.assertEqual("Endpoint", js["resourceType"])
        inst2 = endpoint.Endpoint(js)
        self.implEndpoint3(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implEndpoint3(self, inst):
        self.assertEqual(inst.address, "https://pacs.hospital.org/wado-rs")
        self.assertEqual(inst.connectionType.code, "dicom-wado-rs")
        self.assertEqual(inst.connectionType.system, "http://terminology.hl7.org/CodeSystem/endpoint-connection-type")
        self.assertEqual(inst.id, "example-wadors")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.name, "PACS Hospital DICOM WADO-RS endpoint")
        self.assertEqual(inst.payloadMimeType[0], "application/dicom")
        self.assertEqual(inst.payloadType[0].text, "DICOM WADO-RS")
        self.assertEqual(inst.status, "active")
        self.assertEqual(inst.text.status, "generated")
    
    def testEndpoint4(self):
        inst = self.instantiate_from("endpoint-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a Endpoint instance")
        self.implEndpoint4(inst)
        
        js = inst.as_json()
        self.assertEqual("Endpoint", js["resourceType"])
        inst2 = endpoint.Endpoint(js)
        self.implEndpoint4(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implEndpoint4(self, inst):
        self.assertEqual(inst.address, "http://fhir3.healthintersections.com.au/open/CarePlan")
        self.assertEqual(inst.connectionType.code, "hl7-fhir-rest")
        self.assertEqual(inst.connectionType.system, "http://terminology.hl7.org/CodeSystem/endpoint-connection-type")
        self.assertEqual(inst.contact[0].system, "email")
        self.assertEqual(inst.contact[0].use, "work")
        self.assertEqual(inst.contact[0].value, "endpointmanager@example.org")
        self.assertEqual(inst.header[0], "bearer-code BASGS534s4")
        self.assertEqual(inst.id, "example")
        self.assertEqual(inst.identifier[0].system, "http://example.org/enpoint-identifier")
        self.assertEqual(inst.identifier[0].value, "epcp12")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.name, "Health Intersections CarePlan Hub")
        self.assertEqual(inst.payloadMimeType[0], "application/fhir+xml")
        self.assertEqual(inst.payloadType[0].coding[0].code, "CarePlan")
        self.assertEqual(inst.payloadType[0].coding[0].system, "http://hl7.org/fhir/resource-types")
        self.assertEqual(inst.period.start.date, FHIRDate("2014-09-01").date)
        self.assertEqual(inst.period.start.as_json(), "2014-09-01")
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