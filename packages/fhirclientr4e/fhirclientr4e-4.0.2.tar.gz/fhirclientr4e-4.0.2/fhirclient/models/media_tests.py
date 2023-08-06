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

from . import media

from .fhirdate import FHIRDate
import logging


class MediaTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("Media", js["resourceType"])
        return media.Media(js)
    
    def testMedia1(self):
        inst = self.instantiate_from("media-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a Media instance")
        self.implMedia1(inst)
        
        js = inst.as_json()
        self.assertEqual("Media", js["resourceType"])
        inst2 = media.Media(js)
        self.implMedia1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implMedia1(self, inst):
        self.assertEqual(inst.content.contentType, "image/gif")
        self.assertEqual(inst.content.creation.date, FHIRDate("2009-09-03").date)
        self.assertEqual(inst.content.creation.as_json(), "2009-09-03")
        self.assertEqual(inst.content.id, "a1")
        self.assertEqual(inst.createdDateTime.date, FHIRDate("2017-12-17").date)
        self.assertEqual(inst.createdDateTime.as_json(), "2017-12-17")
        self.assertEqual(inst.frames, 1)
        self.assertEqual(inst.height, 145)
        self.assertEqual(inst.id, "example")
        self.assertEqual(inst.issued.date, FHIRDate("2017-12-17T14:56:18Z").date)
        self.assertEqual(inst.issued.as_json(), "2017-12-17T14:56:18Z")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.modality.coding[0].code, "diagram")
        self.assertEqual(inst.modality.coding[0].system, "http://terminology.hl7.org/CodeSystem/media-modality")
        self.assertEqual(inst.status, "completed")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.type.coding[0].code, "image")
        self.assertEqual(inst.type.coding[0].display, "Image")
        self.assertEqual(inst.type.coding[0].system, "http://terminology.hl7.org/CodeSystem/media-type")
        self.assertEqual(inst.width, 126)
    
    def testMedia2(self):
        inst = self.instantiate_from("media-example-dicom.json")
        self.assertIsNotNone(inst, "Must have instantiated a Media instance")
        self.implMedia2(inst)
        
        js = inst.as_json()
        self.assertEqual("Media", js["resourceType"])
        inst2 = media.Media(js)
        self.implMedia2(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implMedia2(self, inst):
        self.assertEqual(inst.content.contentType, "application/dicom")
        self.assertEqual(inst.extension[0].url, "http://nema.org/fhir/extensions#0002-0010")
        self.assertEqual(inst.extension[0].valueUri, "urn:oid:1.2.840.10008.1.2.1")
        self.assertEqual(inst.height, 480)
        self.assertEqual(inst.id, "1.2.840.11361907579238403408700.3.1.04.19970327150033")
        self.assertEqual(inst.identifier[0].system, "urn:dicom:uid")
        self.assertEqual(inst.identifier[0].type.text, "InstanceUID")
        self.assertEqual(inst.identifier[0].use, "official")
        self.assertEqual(inst.identifier[0].value, "urn:oid:1.2.840.11361907579238403408700.3.1.04.19970327150033")
        self.assertEqual(inst.identifier[1].system, "http://acme-imaging.com/accession/2012")
        self.assertEqual(inst.identifier[1].type.text, "accessionNo")
        self.assertEqual(inst.identifier[1].value, "1234567")
        self.assertEqual(inst.identifier[2].system, "urn:dicom:uid")
        self.assertEqual(inst.identifier[2].type.text, "studyId")
        self.assertEqual(inst.identifier[2].value, "urn:oid:1.2.840.113619.2.21.848.34082.0.538976288.3")
        self.assertEqual(inst.identifier[3].system, "urn:dicom:uid")
        self.assertEqual(inst.identifier[3].type.text, "seriesId")
        self.assertEqual(inst.identifier[3].value, "urn:oid:1.2.840.113619.2.21.3408.700.0.757923840.3.0")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.modality.coding[0].code, "US")
        self.assertEqual(inst.modality.coding[0].system, "http://dicom.nema.org/resources/ontology/DCM")
        self.assertEqual(inst.status, "completed")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.view.coding[0].code, "399067008")
        self.assertEqual(inst.view.coding[0].display, "Lateral projection")
        self.assertEqual(inst.view.coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.width, 640)
    
    def testMedia3(self):
        inst = self.instantiate_from("media-example-xray.json")
        self.assertIsNotNone(inst, "Must have instantiated a Media instance")
        self.implMedia3(inst)
        
        js = inst.as_json()
        self.assertEqual("Media", js["resourceType"])
        inst2 = media.Media(js)
        self.implMedia3(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implMedia3(self, inst):
        self.assertEqual(inst.bodySite.coding[0].code, "85151006")
        self.assertEqual(inst.bodySite.coding[0].display, "Structure of left hand (body structure)")
        self.assertEqual(inst.bodySite.coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.content.contentType, "image/jpeg")
        self.assertEqual(inst.content.creation.date, FHIRDate("2016-03-15").date)
        self.assertEqual(inst.content.creation.as_json(), "2016-03-15")
        self.assertEqual(inst.content.id, "a1")
        self.assertEqual(inst.content.url, "http://someimagingcenter.org/fhir/Binary/A12345")
        self.assertEqual(inst.createdDateTime.date, FHIRDate("2016-03-15").date)
        self.assertEqual(inst.createdDateTime.as_json(), "2016-03-15")
        self.assertEqual(inst.height, 432)
        self.assertEqual(inst.id, "xray")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.modality.coding[0].code, "39714003")
        self.assertEqual(inst.modality.coding[0].display, "Skeletal X-ray of wrist and hand")
        self.assertEqual(inst.modality.coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.status, "completed")
        self.assertEqual(inst.text.div, "<div xmlns=\"http://www.w3.org/1999/xhtml\">Xray of left hand for Patient Henry Levin (MRN 12345) 2016-03-15</div>")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.width, 640)
    
    def testMedia4(self):
        inst = self.instantiate_from("media-example-sound.json")
        self.assertIsNotNone(inst, "Must have instantiated a Media instance")
        self.implMedia4(inst)
        
        js = inst.as_json()
        self.assertEqual("Media", js["resourceType"])
        inst2 = media.Media(js)
        self.implMedia4(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implMedia4(self, inst):
        self.assertEqual(inst.content.contentType, "audio/mpeg")
        self.assertEqual(inst.content.data, "dG9vIGJpZyB0b28gaW5jbHVkZSB0aGUgd2hvbGU=")
        self.assertEqual(inst.content.id, "a1")
        self.assertEqual(inst.duration, 65)
        self.assertEqual(inst.id, "sound")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.status, "completed")
        self.assertEqual(inst.text.div, "<div xmlns=\"http://www.w3.org/1999/xhtml\">Sound recording of speech example for Patient Henry Levin (MRN 12345):<br/><img src=\"#11\" alt=\"diagram\"/></div>")
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