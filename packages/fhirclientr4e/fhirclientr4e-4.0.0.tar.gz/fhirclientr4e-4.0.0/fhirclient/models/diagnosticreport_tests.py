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

from . import diagnosticreport

from .fhirdate import FHIRDate
import logging


class DiagnosticReportTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("DiagnosticReport", js["resourceType"])
        return diagnosticreport.DiagnosticReport(js)
    
    def testDiagnosticReport1(self):
        inst = self.instantiate_from("diagnosticreport-example-ultrasound.json")
        self.assertIsNotNone(inst, "Must have instantiated a DiagnosticReport instance")
        self.implDiagnosticReport1(inst)
        
        js = inst.as_json()
        self.assertEqual("DiagnosticReport", js["resourceType"])
        inst2 = diagnosticreport.DiagnosticReport(js)
        self.implDiagnosticReport1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implDiagnosticReport1(self, inst):
        self.assertEqual(inst.category[0].coding[0].code, "394914008")
        self.assertEqual(inst.category[0].coding[0].display, "Radiology")
        self.assertEqual(inst.category[0].coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.category[0].coding[1].code, "RAD")
        self.assertEqual(inst.category[0].coding[1].system, "http://terminology.hl7.org/CodeSystem/v2-0074")
        self.assertEqual(inst.code.coding[0].code, "45036003")
        self.assertEqual(inst.code.coding[0].display, "Ultrasonography of abdomen")
        self.assertEqual(inst.code.coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.code.text, "Abdominal Ultrasound")
        self.assertEqual(inst.conclusion, "Unremarkable study")
        self.assertEqual(inst.effectiveDateTime.date, FHIRDate("2012-12-01T12:00:00+01:00").date)
        self.assertEqual(inst.effectiveDateTime.as_json(), "2012-12-01T12:00:00+01:00")
        self.assertEqual(inst.id, "ultrasound")
        self.assertEqual(inst.issued.date, FHIRDate("2012-12-01T12:00:00+01:00").date)
        self.assertEqual(inst.issued.as_json(), "2012-12-01T12:00:00+01:00")
        self.assertEqual(inst.media[0].comment, "A comment about the image")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.status, "final")
        self.assertEqual(inst.text.status, "generated")
    
    def testDiagnosticReport2(self):
        inst = self.instantiate_from("diagnosticreport-example-f201-brainct.json")
        self.assertIsNotNone(inst, "Must have instantiated a DiagnosticReport instance")
        self.implDiagnosticReport2(inst)
        
        js = inst.as_json()
        self.assertEqual("DiagnosticReport", js["resourceType"])
        inst2 = diagnosticreport.DiagnosticReport(js)
        self.implDiagnosticReport2(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implDiagnosticReport2(self, inst):
        self.assertEqual(inst.category[0].coding[0].code, "394914008")
        self.assertEqual(inst.category[0].coding[0].display, "Radiology")
        self.assertEqual(inst.category[0].coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.category[0].coding[1].code, "RAD")
        self.assertEqual(inst.category[0].coding[1].system, "http://terminology.hl7.org/CodeSystem/v2-0074")
        self.assertEqual(inst.code.coding[0].code, "429858000")
        self.assertEqual(inst.code.coding[0].display, "Computed tomography (CT) of head and neck")
        self.assertEqual(inst.code.coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.code.text, "CT of head-neck")
        self.assertEqual(inst.conclusion, "CT brains: large tumor sphenoid/clivus.")
        self.assertEqual(inst.conclusionCode[0].coding[0].code, "188340000")
        self.assertEqual(inst.conclusionCode[0].coding[0].display, "Malignant tumor of craniopharyngeal duct")
        self.assertEqual(inst.conclusionCode[0].coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.effectiveDateTime.date, FHIRDate("2012-12-01T12:00:00+01:00").date)
        self.assertEqual(inst.effectiveDateTime.as_json(), "2012-12-01T12:00:00+01:00")
        self.assertEqual(inst.id, "f201")
        self.assertEqual(inst.issued.date, FHIRDate("2012-12-01T12:00:00+01:00").date)
        self.assertEqual(inst.issued.as_json(), "2012-12-01T12:00:00+01:00")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.status, "final")
        self.assertEqual(inst.text.status, "generated")
    
    def testDiagnosticReport3(self):
        inst = self.instantiate_from("diagnosticreport-example-papsmear.json")
        self.assertIsNotNone(inst, "Must have instantiated a DiagnosticReport instance")
        self.implDiagnosticReport3(inst)
        
        js = inst.as_json()
        self.assertEqual("DiagnosticReport", js["resourceType"])
        inst2 = diagnosticreport.DiagnosticReport(js)
        self.implDiagnosticReport3(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implDiagnosticReport3(self, inst):
        self.assertEqual(inst.code.coding[0].code, "47527-7")
        self.assertEqual(inst.code.coding[0].system, "http://loinc.org")
        self.assertEqual(inst.effectiveDateTime.date, FHIRDate("2013-02-11T10:33:33+11:00").date)
        self.assertEqual(inst.effectiveDateTime.as_json(), "2013-02-11T10:33:33+11:00")
        self.assertEqual(inst.id, "pap")
        self.assertEqual(inst.issued.date, FHIRDate("2013-02-13T11:45:33+11:00").date)
        self.assertEqual(inst.issued.as_json(), "2013-02-13T11:45:33+11:00")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.status, "final")
        self.assertEqual(inst.text.status, "additional")
    
    def testDiagnosticReport4(self):
        inst = self.instantiate_from("diagnosticreport-example-gingival-mass.json")
        self.assertIsNotNone(inst, "Must have instantiated a DiagnosticReport instance")
        self.implDiagnosticReport4(inst)
        
        js = inst.as_json()
        self.assertEqual("DiagnosticReport", js["resourceType"])
        inst2 = diagnosticreport.DiagnosticReport(js)
        self.implDiagnosticReport4(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implDiagnosticReport4(self, inst):
        self.assertEqual(inst.category[0].coding[0].code, "PAT")
        self.assertEqual(inst.category[0].coding[0].display, "Pathology (gross & histopath, not surgical)")
        self.assertEqual(inst.category[0].coding[0].system, "http://terminology.hl7.org/CodeSystem/v2-0074")
        self.assertEqual(inst.category[0].text, "Pathology")
        self.assertEqual(inst.code.coding[0].code, "4503")
        self.assertEqual(inst.code.coding[0].display, "Biopsy without Microscopic Description (1 Site/Lesion)-Standard")
        self.assertEqual(inst.code.coding[0].system, "https://www.acmeonline.com")
        self.assertEqual(inst.code.text, "Biopsy without Microscopic Description (1 Site/Lesion)-Standard")
        self.assertEqual(inst.effectiveDateTime.date, FHIRDate("2017-03-02").date)
        self.assertEqual(inst.effectiveDateTime.as_json(), "2017-03-02")
        self.assertEqual(inst.id, "gingival-mass")
        self.assertEqual(inst.identifier[0].system, "https://www.acmeonline.com")
        self.assertEqual(inst.identifier[0].value, "P73456090")
        self.assertEqual(inst.issued.date, FHIRDate("2017-03-15T08:13:08Z").date)
        self.assertEqual(inst.issued.as_json(), "2017-03-15T08:13:08Z")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.presentedForm[0].contentType, "application/pdf")
        self.assertEqual(inst.presentedForm[0].language, "en")
        self.assertEqual(inst.presentedForm[0].title, "LAB ID: P73456090 MAX JONES Biopsy without Microscopic Description (1 Site/Lesion)-Standard")
        self.assertEqual(inst.status, "final")
        self.assertEqual(inst.text.status, "generated")
    
    def testDiagnosticReport5(self):
        inst = self.instantiate_from("diagnosticreport-example-pgx.json")
        self.assertIsNotNone(inst, "Must have instantiated a DiagnosticReport instance")
        self.implDiagnosticReport5(inst)
        
        js = inst.as_json()
        self.assertEqual("DiagnosticReport", js["resourceType"])
        inst2 = diagnosticreport.DiagnosticReport(js)
        self.implDiagnosticReport5(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implDiagnosticReport5(self, inst):
        self.assertEqual(inst.code.coding[0].code, "PGxReport")
        self.assertEqual(inst.code.coding[0].display, "Pharmacogenetics Report")
        self.assertEqual(inst.code.coding[0].system, "https://system/PGxReport")
        self.assertEqual(inst.code.text, "Pharmacogenetics Report")
        self.assertEqual(inst.effectiveDateTime.date, FHIRDate("2016-10-15T12:34:56+11:00").date)
        self.assertEqual(inst.effectiveDateTime.as_json(), "2016-10-15T12:34:56+11:00")
        self.assertEqual(inst.id, "example-pgx")
        self.assertEqual(inst.issued.date, FHIRDate("2016-10-20T14:00:05+11:00").date)
        self.assertEqual(inst.issued.as_json(), "2016-10-20T14:00:05+11:00")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.presentedForm[0].contentType, "application/pdf")
        self.assertEqual(inst.presentedForm[0].creation.date, FHIRDate("2016-10-20T20:00:00+11:00").date)
        self.assertEqual(inst.presentedForm[0].creation.as_json(), "2016-10-20T20:00:00+11:00")
        self.assertEqual(inst.presentedForm[0].data, "cGRmSW5CYXNlNjRCaW5hcnk=")
        self.assertEqual(inst.presentedForm[0].hash, "571ef9c5655840f324e679072ed62b1b95eef8a0")
        self.assertEqual(inst.presentedForm[0].language, "en")
        self.assertEqual(inst.presentedForm[0].title, "Pharmacogenetics Report")
        self.assertEqual(inst.status, "final")
        self.assertEqual(inst.text.status, "generated")
    
    def testDiagnosticReport6(self):
        inst = self.instantiate_from("diagnosticreport-example-dxa.json")
        self.assertIsNotNone(inst, "Must have instantiated a DiagnosticReport instance")
        self.implDiagnosticReport6(inst)
        
        js = inst.as_json()
        self.assertEqual("DiagnosticReport", js["resourceType"])
        inst2 = diagnosticreport.DiagnosticReport(js)
        self.implDiagnosticReport6(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implDiagnosticReport6(self, inst):
        self.assertEqual(inst.code.coding[0].code, "38269-7")
        self.assertEqual(inst.code.coding[0].system, "http://loinc.org")
        self.assertEqual(inst.code.text, "DXA BONE DENSITOMETRY")
        self.assertEqual(inst.conclusionCode[0].coding[0].code, "391040000")
        self.assertEqual(inst.conclusionCode[0].coding[0].display, "At risk of osteoporotic fracture")
        self.assertEqual(inst.conclusionCode[0].coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.effectiveDateTime.date, FHIRDate("2008-06-17").date)
        self.assertEqual(inst.effectiveDateTime.as_json(), "2008-06-17")
        self.assertEqual(inst.id, "102")
        self.assertEqual(inst.issued.date, FHIRDate("2008-06-18T09:23:00+10:00").date)
        self.assertEqual(inst.issued.as_json(), "2008-06-18T09:23:00+10:00")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.status, "final")
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