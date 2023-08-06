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

from . import observation

from .fhirdate import FHIRDate
import logging


class ObservationTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("Observation", js["resourceType"])
        return observation.Observation(js)
    
    def testObservation1(self):
        inst = self.instantiate_from("observation-example-genetics-1.json")
        self.assertIsNotNone(inst, "Must have instantiated a Observation instance")
        self.implObservation1(inst)
        
        js = inst.as_json()
        self.assertEqual("Observation", js["resourceType"])
        inst2 = observation.Observation(js)
        self.implObservation1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implObservation1(self, inst):
        self.assertEqual(inst.code.coding[0].code, "55233-1")
        self.assertEqual(inst.code.coding[0].display, "Genetic analysis master panel-- This is the parent OBR for the panel holding all of the associated observations that can be reported with a molecular genetics analysis result.")
        self.assertEqual(inst.code.coding[0].system, "http://loinc.org")
        self.assertEqual(inst.extension[0].url, "http://hl7.org/fhir/StructureDefinition/observation-geneticsGene")
        self.assertEqual(inst.extension[0].valueCodeableConcept.coding[0].code, "3236")
        self.assertEqual(inst.extension[0].valueCodeableConcept.coding[0].display, "EGFR")
        self.assertEqual(inst.extension[0].valueCodeableConcept.coding[0].system, "http://www.genenames.org")
        self.assertEqual(inst.extension[1].url, "http://hl7.org/fhir/StructureDefinition/observation-geneticsDNARegionName")
        self.assertEqual(inst.extension[1].valueString, "Exon 21")
        self.assertEqual(inst.extension[2].url, "http://hl7.org/fhir/StructureDefinition/observation-geneticsGenomicSourceClass")
        self.assertEqual(inst.extension[2].valueCodeableConcept.coding[0].code, "LA6684-0")
        self.assertEqual(inst.extension[2].valueCodeableConcept.coding[0].display, "somatic")
        self.assertEqual(inst.extension[2].valueCodeableConcept.coding[0].system, "http://loinc.org")
        self.assertEqual(inst.id, "example-genetics-1")
        self.assertEqual(inst.issued.date, FHIRDate("2013-04-03T15:30:10+01:00").date)
        self.assertEqual(inst.issued.as_json(), "2013-04-03T15:30:10+01:00")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.status, "final")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.valueCodeableConcept.coding[0].code, "10828004")
        self.assertEqual(inst.valueCodeableConcept.coding[0].display, "Positive")
        self.assertEqual(inst.valueCodeableConcept.coding[0].system, "http://snomed.info/sct")
    
    def testObservation2(self):
        inst = self.instantiate_from("observation-example-bmd.json")
        self.assertIsNotNone(inst, "Must have instantiated a Observation instance")
        self.implObservation2(inst)
        
        js = inst.as_json()
        self.assertEqual("Observation", js["resourceType"])
        inst2 = observation.Observation(js)
        self.implObservation2(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implObservation2(self, inst):
        self.assertEqual(inst.bodySite.coding[0].code, "71341001:272741003=7771000")
        self.assertEqual(inst.bodySite.coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.bodySite.text, "Left Femur")
        self.assertEqual(inst.code.coding[0].code, "24701-5")
        self.assertEqual(inst.code.coding[0].display, "Femur DXA Bone density")
        self.assertEqual(inst.code.coding[0].system, "http://loinc.org")
        self.assertEqual(inst.code.text, "BMD - Left Femur")
        self.assertEqual(inst.id, "bmd")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.status, "final")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.valueQuantity.code, "g/cm-2")
        self.assertEqual(inst.valueQuantity.system, "http://unitsofmeasure.org")
        self.assertEqual(inst.valueQuantity.unit, "g/cm²")
        self.assertEqual(inst.valueQuantity.value, 0.887)
    
    def testObservation3(self):
        inst = self.instantiate_from("observation-example-respiratory-rate.json")
        self.assertIsNotNone(inst, "Must have instantiated a Observation instance")
        self.implObservation3(inst)
        
        js = inst.as_json()
        self.assertEqual("Observation", js["resourceType"])
        inst2 = observation.Observation(js)
        self.implObservation3(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implObservation3(self, inst):
        self.assertEqual(inst.category[0].coding[0].code, "vital-signs")
        self.assertEqual(inst.category[0].coding[0].display, "Vital Signs")
        self.assertEqual(inst.category[0].coding[0].system, "http://terminology.hl7.org/CodeSystem/observation-category")
        self.assertEqual(inst.category[0].text, "Vital Signs")
        self.assertEqual(inst.code.coding[0].code, "9279-1")
        self.assertEqual(inst.code.coding[0].display, "Respiratory rate")
        self.assertEqual(inst.code.coding[0].system, "http://loinc.org")
        self.assertEqual(inst.code.text, "Respiratory rate")
        self.assertEqual(inst.effectiveDateTime.date, FHIRDate("1999-07-02").date)
        self.assertEqual(inst.effectiveDateTime.as_json(), "1999-07-02")
        self.assertEqual(inst.id, "respiratory-rate")
        self.assertEqual(inst.meta.profile[0], "http://hl7.org/fhir/StructureDefinition/vitalsigns")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.status, "final")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.valueQuantity.code, "/min")
        self.assertEqual(inst.valueQuantity.system, "http://unitsofmeasure.org")
        self.assertEqual(inst.valueQuantity.unit, "breaths/minute")
        self.assertEqual(inst.valueQuantity.value, 26)
    
    def testObservation4(self):
        inst = self.instantiate_from("observation-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a Observation instance")
        self.implObservation4(inst)
        
        js = inst.as_json()
        self.assertEqual("Observation", js["resourceType"])
        inst2 = observation.Observation(js)
        self.implObservation4(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implObservation4(self, inst):
        self.assertEqual(inst.category[0].coding[0].code, "vital-signs")
        self.assertEqual(inst.category[0].coding[0].display, "Vital Signs")
        self.assertEqual(inst.category[0].coding[0].system, "http://terminology.hl7.org/CodeSystem/observation-category")
        self.assertEqual(inst.code.coding[0].code, "29463-7")
        self.assertEqual(inst.code.coding[0].display, "Body Weight")
        self.assertEqual(inst.code.coding[0].system, "http://loinc.org")
        self.assertEqual(inst.code.coding[1].code, "3141-9")
        self.assertEqual(inst.code.coding[1].display, "Body weight Measured")
        self.assertEqual(inst.code.coding[1].system, "http://loinc.org")
        self.assertEqual(inst.code.coding[2].code, "27113001")
        self.assertEqual(inst.code.coding[2].display, "Body weight")
        self.assertEqual(inst.code.coding[2].system, "http://snomed.info/sct")
        self.assertEqual(inst.code.coding[3].code, "body-weight")
        self.assertEqual(inst.code.coding[3].display, "Body Weight")
        self.assertEqual(inst.code.coding[3].system, "http://acme.org/devices/clinical-codes")
        self.assertEqual(inst.effectiveDateTime.date, FHIRDate("2016-03-28").date)
        self.assertEqual(inst.effectiveDateTime.as_json(), "2016-03-28")
        self.assertEqual(inst.id, "example")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.status, "final")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.valueQuantity.code, "[lb_av]")
        self.assertEqual(inst.valueQuantity.system, "http://unitsofmeasure.org")
        self.assertEqual(inst.valueQuantity.unit, "lbs")
        self.assertEqual(inst.valueQuantity.value, 185)
    
    def testObservation5(self):
        inst = self.instantiate_from("observation-example-haplotype2.json")
        self.assertIsNotNone(inst, "Must have instantiated a Observation instance")
        self.implObservation5(inst)
        
        js = inst.as_json()
        self.assertEqual("Observation", js["resourceType"])
        inst2 = observation.Observation(js)
        self.implObservation5(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implObservation5(self, inst):
        self.assertEqual(inst.code.coding[0].code, "55233-1")
        self.assertEqual(inst.code.coding[0].display, "Genetic analysis master panel-- This is the parent OBR for the panel holding all of the associated observations that can be reported with a molecular genetics analysis result.")
        self.assertEqual(inst.code.coding[0].system, "http://loinc.org")
        self.assertEqual(inst.extension[0].url, "http://hl7.org/fhir/StructureDefinition/observation-geneticsGene")
        self.assertEqual(inst.extension[0].valueCodeableConcept.coding[0].code, "2623")
        self.assertEqual(inst.extension[0].valueCodeableConcept.coding[0].display, "CYP2C9")
        self.assertEqual(inst.extension[0].valueCodeableConcept.coding[0].system, "http://www.genenames.org")
        self.assertEqual(inst.id, "example-haplotype2")
        self.assertEqual(inst.issued.date, FHIRDate("2013-04-03T15:30:10+01:00").date)
        self.assertEqual(inst.issued.as_json(), "2013-04-03T15:30:10+01:00")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.status, "unknown")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.valueCodeableConcept.coding[0].code, "PA16581679")
        self.assertEqual(inst.valueCodeableConcept.coding[0].display, "*4")
        self.assertEqual(inst.valueCodeableConcept.coding[0].system, "http://pharmakb.org")
    
    def testObservation6(self):
        inst = self.instantiate_from("observation-example-mbp.json")
        self.assertIsNotNone(inst, "Must have instantiated a Observation instance")
        self.implObservation6(inst)
        
        js = inst.as_json()
        self.assertEqual("Observation", js["resourceType"])
        inst2 = observation.Observation(js)
        self.implObservation6(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implObservation6(self, inst):
        self.assertEqual(inst.category[0].coding[0].code, "vital-signs")
        self.assertEqual(inst.category[0].coding[0].display, "Vital Signs")
        self.assertEqual(inst.category[0].coding[0].system, "http://terminology.hl7.org/CodeSystem/observation-category")
        self.assertEqual(inst.category[0].text, "Vital Signs")
        self.assertEqual(inst.code.coding[0].code, "8478-0")
        self.assertEqual(inst.code.coding[0].display, "Mean blood pressure")
        self.assertEqual(inst.code.coding[0].system, "http://loinc.org")
        self.assertEqual(inst.code.text, "Mean blood pressure")
        self.assertEqual(inst.effectiveDateTime.date, FHIRDate("1999-07-02").date)
        self.assertEqual(inst.effectiveDateTime.as_json(), "1999-07-02")
        self.assertEqual(inst.id, "mbp")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.status, "final")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.valueQuantity.code, "mm[Hg]")
        self.assertEqual(inst.valueQuantity.system, "http://unitsofmeasure.org")
        self.assertEqual(inst.valueQuantity.unit, "mm[Hg]")
        self.assertEqual(inst.valueQuantity.value, 80)
    
    def testObservation7(self):
        inst = self.instantiate_from("observation-example-genetics-brcapat.json")
        self.assertIsNotNone(inst, "Must have instantiated a Observation instance")
        self.implObservation7(inst)
        
        js = inst.as_json()
        self.assertEqual("Observation", js["resourceType"])
        inst2 = observation.Observation(js)
        self.implObservation7(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implObservation7(self, inst):
        self.assertEqual(inst.code.coding[0].code, "59041-4")
        self.assertEqual(inst.code.coding[0].display, "BRCA1+BRCA2 gene mutations tested for in Blood or Tissue by Molecular genetics method Nominal")
        self.assertEqual(inst.code.coding[0].system, "http://loinc.org")
        self.assertEqual(inst.extension[0].url, "http://hl7.org/fhir/StructureDefinition/observation-geneticsGene")
        self.assertEqual(inst.extension[0].valueCodeableConcept.coding[0].code, "KX470182.1")
        self.assertEqual(inst.extension[0].valueCodeableConcept.coding[0].display, "BRCA")
        self.assertEqual(inst.extension[0].valueCodeableConcept.coding[0].system, "https://www.ncbi.nlm.nih.gov/nuccore")
        self.assertEqual(inst.extension[1].url, "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity")
        self.assertEqual(inst.extension[1].valueCodeableConcept.coding[0].code, "413581001")
        self.assertEqual(inst.extension[1].valueCodeableConcept.coding[0].display, "Unknown racial group")
        self.assertEqual(inst.extension[1].valueCodeableConcept.coding[0].system, "http://browser.ihtsdotools.org/")
        self.assertEqual(inst.id, "example-genetics-brcapat")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.status, "final")
        self.assertEqual(inst.text.status, "generated")
    
    def testObservation8(self):
        inst = self.instantiate_from("observation-example-bmi.json")
        self.assertIsNotNone(inst, "Must have instantiated a Observation instance")
        self.implObservation8(inst)
        
        js = inst.as_json()
        self.assertEqual("Observation", js["resourceType"])
        inst2 = observation.Observation(js)
        self.implObservation8(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implObservation8(self, inst):
        self.assertEqual(inst.category[0].coding[0].code, "vital-signs")
        self.assertEqual(inst.category[0].coding[0].display, "Vital Signs")
        self.assertEqual(inst.category[0].coding[0].system, "http://terminology.hl7.org/CodeSystem/observation-category")
        self.assertEqual(inst.category[0].text, "Vital Signs")
        self.assertEqual(inst.code.coding[0].code, "39156-5")
        self.assertEqual(inst.code.coding[0].display, "Body mass index (BMI) [Ratio]")
        self.assertEqual(inst.code.coding[0].system, "http://loinc.org")
        self.assertEqual(inst.code.text, "BMI")
        self.assertEqual(inst.effectiveDateTime.date, FHIRDate("1999-07-02").date)
        self.assertEqual(inst.effectiveDateTime.as_json(), "1999-07-02")
        self.assertEqual(inst.id, "bmi")
        self.assertEqual(inst.meta.profile[0], "http://hl7.org/fhir/StructureDefinition/vitalsigns")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.status, "final")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.valueQuantity.code, "kg/m2")
        self.assertEqual(inst.valueQuantity.system, "http://unitsofmeasure.org")
        self.assertEqual(inst.valueQuantity.unit, "kg/m2")
        self.assertEqual(inst.valueQuantity.value, 16.2)
    
    def testObservation9(self):
        inst = self.instantiate_from("observation-example-body-height.json")
        self.assertIsNotNone(inst, "Must have instantiated a Observation instance")
        self.implObservation9(inst)
        
        js = inst.as_json()
        self.assertEqual("Observation", js["resourceType"])
        inst2 = observation.Observation(js)
        self.implObservation9(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implObservation9(self, inst):
        self.assertEqual(inst.category[0].coding[0].code, "vital-signs")
        self.assertEqual(inst.category[0].coding[0].display, "Vital Signs")
        self.assertEqual(inst.category[0].coding[0].system, "http://terminology.hl7.org/CodeSystem/observation-category")
        self.assertEqual(inst.category[0].text, "Vital Signs")
        self.assertEqual(inst.code.coding[0].code, "8302-2")
        self.assertEqual(inst.code.coding[0].display, "Body height")
        self.assertEqual(inst.code.coding[0].system, "http://loinc.org")
        self.assertEqual(inst.code.text, "Body height")
        self.assertEqual(inst.effectiveDateTime.date, FHIRDate("1999-07-02").date)
        self.assertEqual(inst.effectiveDateTime.as_json(), "1999-07-02")
        self.assertEqual(inst.id, "body-height")
        self.assertEqual(inst.meta.profile[0], "http://hl7.org/fhir/StructureDefinition/vitalsigns")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.status, "final")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.valueQuantity.code, "[in_i]")
        self.assertEqual(inst.valueQuantity.system, "http://unitsofmeasure.org")
        self.assertEqual(inst.valueQuantity.unit, "in")
        self.assertEqual(inst.valueQuantity.value, 66.89999999999999)
    
    def testObservation10(self):
        inst = self.instantiate_from("observation-example-eye-color.json")
        self.assertIsNotNone(inst, "Must have instantiated a Observation instance")
        self.implObservation10(inst)
        
        js = inst.as_json()
        self.assertEqual("Observation", js["resourceType"])
        inst2 = observation.Observation(js)
        self.implObservation10(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implObservation10(self, inst):
        self.assertEqual(inst.code.text, "eye color")
        self.assertEqual(inst.effectiveDateTime.date, FHIRDate("2016-05-18").date)
        self.assertEqual(inst.effectiveDateTime.as_json(), "2016-05-18")
        self.assertEqual(inst.id, "eye-color")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.status, "final")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.valueString, "blue")

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