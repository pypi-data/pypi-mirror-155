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

from . import imagingstudy

from .fhirdate import FHIRDate
import logging


class ImagingStudyTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("ImagingStudy", js["resourceType"])
        return imagingstudy.ImagingStudy(js)
    
    def testImagingStudy1(self):
        inst = self.instantiate_from("imagingstudy-example-xr.json")
        self.assertIsNotNone(inst, "Must have instantiated a ImagingStudy instance")
        self.implImagingStudy1(inst)
        
        js = inst.as_json()
        self.assertEqual("ImagingStudy", js["resourceType"])
        inst2 = imagingstudy.ImagingStudy(js)
        self.implImagingStudy1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implImagingStudy1(self, inst):
        self.assertEqual(inst.id, "example-xr")
        self.assertEqual(inst.identifier[0].system, "urn:dicom:uid")
        self.assertEqual(inst.identifier[0].use, "official")
        self.assertEqual(inst.identifier[0].value, "urn:oid:2.16.124.113543.6003.1154777499.30246.19789.3503430046")
        self.assertEqual(inst.identifier[1].type.coding[0].code, "ACSN")
        self.assertEqual(inst.identifier[1].type.coding[0].system, "http://terminology.hl7.org/CodeSystem/v2-0203")
        self.assertEqual(inst.identifier[1].use, "usual")
        self.assertEqual(inst.identifier[1].value, "W12342398")
        self.assertEqual(inst.identifier[2].use, "secondary")
        self.assertEqual(inst.identifier[2].value, "55551234")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.modality[0].code, "DX")
        self.assertEqual(inst.modality[0].system, "http://dicom.nema.org/resources/ontology/DCM")
        self.assertEqual(inst.note[0].text, "XR Wrist 3+ Views")
        self.assertEqual(inst.numberOfInstances, 2)
        self.assertEqual(inst.numberOfSeries, 1)
        self.assertEqual(inst.procedureCode[0].coding[0].code, "RPID2589")
        self.assertEqual(inst.procedureCode[0].coding[0].display, "XR Wrist 3+ Views")
        self.assertEqual(inst.procedureCode[0].coding[0].system, "http://www.radlex.org")
        self.assertEqual(inst.procedureCode[0].text, "XR Wrist 3+ Views")
        self.assertEqual(inst.reasonCode[0].coding[0].code, "357009")
        self.assertEqual(inst.reasonCode[0].coding[0].display, "Closed fracture of trapezoidal bone of wrist")
        self.assertEqual(inst.reasonCode[0].coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.series[0].bodySite.code, "T-15460")
        self.assertEqual(inst.series[0].bodySite.display, "Wrist Joint")
        self.assertEqual(inst.series[0].bodySite.system, "http://snomed.info/sct")
        self.assertEqual(inst.series[0].description, "XR Wrist 3+ Views")
        self.assertEqual(inst.series[0].instance[0].number, 1)
        self.assertEqual(inst.series[0].instance[0].sopClass.code, "urn:oid:1.2.840.10008.5.1.4.1.1.2")
        self.assertEqual(inst.series[0].instance[0].sopClass.system, "urn:ietf:rfc:3986")
        self.assertEqual(inst.series[0].instance[0].title, "PA VIEW")
        self.assertEqual(inst.series[0].instance[0].uid, "2.16.124.113543.6003.1154777499.30246.19789.3503430045.1.1")
        self.assertEqual(inst.series[0].instance[1].number, 2)
        self.assertEqual(inst.series[0].instance[1].sopClass.code, "urn:oid:1.2.840.10008.5.1.4.1.1.2")
        self.assertEqual(inst.series[0].instance[1].sopClass.system, "urn:ietf:rfc:3986")
        self.assertEqual(inst.series[0].instance[1].title, "LL VIEW")
        self.assertEqual(inst.series[0].instance[1].uid, "2.16.124.113543.6003.1154777499.30246.19789.3503430045.1.2")
        self.assertEqual(inst.series[0].laterality.code, "419161000")
        self.assertEqual(inst.series[0].laterality.display, "Unilateral left")
        self.assertEqual(inst.series[0].laterality.system, "http://snomed.info/sct")
        self.assertEqual(inst.series[0].modality.code, "DX")
        self.assertEqual(inst.series[0].modality.system, "http://dicom.nema.org/resources/ontology/DCM")
        self.assertEqual(inst.series[0].number, 3)
        self.assertEqual(inst.series[0].numberOfInstances, 2)
        self.assertEqual(inst.series[0].performer[0].function.coding[0].code, "PRF")
        self.assertEqual(inst.series[0].performer[0].function.coding[0].system, "http://terminology.hl7.org/CodeSystem/v3-ParticipationType")
        self.assertEqual(inst.series[0].started.date, FHIRDate("2011-01-01T11:01:20+03:00").date)
        self.assertEqual(inst.series[0].started.as_json(), "2011-01-01T11:01:20+03:00")
        self.assertEqual(inst.series[0].uid, "2.16.124.113543.6003.1154777499.30246.19789.3503430045.1")
        self.assertEqual(inst.started.date, FHIRDate("2017-01-01T11:01:20+03:00").date)
        self.assertEqual(inst.started.as_json(), "2017-01-01T11:01:20+03:00")
        self.assertEqual(inst.status, "available")
        self.assertEqual(inst.text.div, "<div xmlns=\"http://www.w3.org/1999/xhtml\">XR Wrist 3+ Views. John Smith (MRN: 09236). Accession: W12342398. Performed: 2017-01-01. 1 series, 2 images.</div>")
        self.assertEqual(inst.text.status, "generated")
    
    def testImagingStudy2(self):
        inst = self.instantiate_from("imagingstudy-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a ImagingStudy instance")
        self.implImagingStudy2(inst)
        
        js = inst.as_json()
        self.assertEqual("ImagingStudy", js["resourceType"])
        inst2 = imagingstudy.ImagingStudy(js)
        self.implImagingStudy2(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implImagingStudy2(self, inst):
        self.assertEqual(inst.id, "example")
        self.assertEqual(inst.identifier[0].system, "urn:dicom:uid")
        self.assertEqual(inst.identifier[0].value, "urn:oid:2.16.124.113543.6003.1154777499.30246.19789.3503430045")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.numberOfInstances, 1)
        self.assertEqual(inst.numberOfSeries, 1)
        self.assertEqual(inst.series[0].bodySite.code, "67734004")
        self.assertEqual(inst.series[0].bodySite.display, "Upper Trunk Structure")
        self.assertEqual(inst.series[0].bodySite.system, "http://snomed.info/sct")
        self.assertEqual(inst.series[0].description, "CT Surview 180")
        self.assertEqual(inst.series[0].instance[0].number, 1)
        self.assertEqual(inst.series[0].instance[0].sopClass.code, "urn:oid:1.2.840.10008.5.1.4.1.1.2")
        self.assertEqual(inst.series[0].instance[0].sopClass.system, "urn:ietf:rfc:3986")
        self.assertEqual(inst.series[0].instance[0].uid, "2.16.124.113543.6003.189642796.63084.16748.2599092903")
        self.assertEqual(inst.series[0].modality.code, "CT")
        self.assertEqual(inst.series[0].modality.system, "http://dicom.nema.org/resources/ontology/DCM")
        self.assertEqual(inst.series[0].number, 3)
        self.assertEqual(inst.series[0].numberOfInstances, 1)
        self.assertEqual(inst.series[0].uid, "2.16.124.113543.6003.2588828330.45298.17418.2723805630")
        self.assertEqual(inst.started.date, FHIRDate("2011-01-01T11:01:20+03:00").date)
        self.assertEqual(inst.started.as_json(), "2011-01-01T11:01:20+03:00")
        self.assertEqual(inst.status, "available")
        self.assertEqual(inst.text.div, "<div xmlns=\"http://www.w3.org/1999/xhtml\">CT Chest.  John Smith (MRN: 09236). Accession: W12342398. Performed: 2011-01-01. 3 series, 12 images.</div>")
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