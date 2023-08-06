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

from . import codesystem

from .fhirdate import FHIRDate
import logging


class CodeSystemTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("CodeSystem", js["resourceType"])
        return codesystem.CodeSystem(js)
    
    def testCodeSystem1(self):
        inst = self.instantiate_from("codesystem-example-supplement.json")
        self.assertIsNotNone(inst, "Must have instantiated a CodeSystem instance")
        self.implCodeSystem1(inst)
        
        js = inst.as_json()
        self.assertEqual("CodeSystem", js["resourceType"])
        inst2 = codesystem.CodeSystem(js)
        self.implCodeSystem1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implCodeSystem1(self, inst):
        self.assertEqual(inst.concept[0].code, "chol-mmol")
        self.assertEqual(inst.concept[0].property[0].code, "legacy")
        self.assertFalse(inst.concept[0].property[0].valueBoolean)
        self.assertEqual(inst.concept[1].code, "chol-mass")
        self.assertEqual(inst.concept[1].property[0].code, "legacy")
        self.assertTrue(inst.concept[1].property[0].valueBoolean)
        self.assertEqual(inst.concept[2].code, "chol")
        self.assertEqual(inst.concept[2].property[0].code, "legacy")
        self.assertTrue(inst.concept[2].property[0].valueBoolean)
        self.assertEqual(inst.contact[0].name, "FHIR project team")
        self.assertEqual(inst.contact[0].telecom[0].system, "url")
        self.assertEqual(inst.contact[0].telecom[0].value, "http://hl7.org/fhir")
        self.assertEqual(inst.content, "supplement")
        self.assertEqual(inst.date.date, FHIRDate("2016-01-28").date)
        self.assertEqual(inst.date.as_json(), "2016-01-28")
        self.assertTrue(inst.experimental)
        self.assertEqual(inst.id, "example-supplement")
        self.assertEqual(inst.name, "CholCodeLegacyStatus")
        self.assertEqual(inst.property[0].code, "legacy")
        self.assertEqual(inst.property[0].description, "hether the test is currently performed")
        self.assertEqual(inst.property[0].type, "boolean")
        self.assertEqual(inst.publisher, "ACME Co")
        self.assertEqual(inst.status, "draft")
        self.assertEqual(inst.supplements, "http://hl7.org/fhir/CodeSystem/example")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.url, "http://hl7.org/fhir/CodeSystem/example-supplement")
        self.assertEqual(inst.version, "201801103")
    
    def testCodeSystem2(self):
        inst = self.instantiate_from("codesystem-list-example-codes.json")
        self.assertIsNotNone(inst, "Must have instantiated a CodeSystem instance")
        self.implCodeSystem2(inst)
        
        js = inst.as_json()
        self.assertEqual("CodeSystem", js["resourceType"])
        inst2 = codesystem.CodeSystem(js)
        self.implCodeSystem2(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implCodeSystem2(self, inst):
        self.assertTrue(inst.caseSensitive)
        self.assertEqual(inst.concept[0].code, "alerts")
        self.assertEqual(inst.concept[0].definition, "A list of alerts for the patient.")
        self.assertEqual(inst.concept[0].display, "Alerts")
        self.assertEqual(inst.concept[1].code, "adverserxns")
        self.assertEqual(inst.concept[1].definition, "A list of part adverse reactions.")
        self.assertEqual(inst.concept[1].display, "Adverse Reactions")
        self.assertEqual(inst.concept[2].code, "allergies")
        self.assertEqual(inst.concept[2].definition, "A list of Allergies for the patient.")
        self.assertEqual(inst.concept[2].display, "Allergies")
        self.assertEqual(inst.concept[3].code, "medications")
        self.assertEqual(inst.concept[3].definition, "A list of medication statements for the patient.")
        self.assertEqual(inst.concept[3].display, "Medication List")
        self.assertEqual(inst.concept[4].code, "problems")
        self.assertEqual(inst.concept[4].definition, "A list of problems that the patient is known of have (or have had in the past).")
        self.assertEqual(inst.concept[4].display, "Problem List")
        self.assertEqual(inst.concept[5].code, "worklist")
        self.assertEqual(inst.concept[5].definition, "A list of items that constitute a set of work to be performed (typically this code would be specialized for more specific uses, such as a ward round list).")
        self.assertEqual(inst.concept[5].display, "Worklist")
        self.assertEqual(inst.concept[6].code, "waiting")
        self.assertEqual(inst.concept[6].definition, "A list of items waiting for an event (perhaps a surgical patient waiting list).")
        self.assertEqual(inst.concept[6].display, "Waiting List")
        self.assertEqual(inst.concept[7].code, "protocols")
        self.assertEqual(inst.concept[7].definition, "A set of protocols to be followed.")
        self.assertEqual(inst.concept[7].display, "Protocols")
        self.assertEqual(inst.concept[8].code, "plans")
        self.assertEqual(inst.concept[8].definition, "A set of care plans that apply in a particular context of care.")
        self.assertEqual(inst.concept[8].display, "Care Plans")
        self.assertEqual(inst.contact[0].telecom[0].system, "url")
        self.assertEqual(inst.contact[0].telecom[0].value, "http://hl7.org/fhir")
        self.assertEqual(inst.content, "complete")
        self.assertEqual(inst.description, "Example use codes for the List resource - typical kinds of use.")
        self.assertFalse(inst.experimental)
        self.assertEqual(inst.extension[0].url, "http://hl7.org/fhir/StructureDefinition/structuredefinition-wg")
        self.assertEqual(inst.extension[0].valueCode, "fhir")
        self.assertEqual(inst.extension[1].url, "http://hl7.org/fhir/StructureDefinition/structuredefinition-standards-status")
        self.assertEqual(inst.extension[1].valueCode, "draft")
        self.assertEqual(inst.extension[2].url, "http://hl7.org/fhir/StructureDefinition/structuredefinition-fmm")
        self.assertEqual(inst.extension[2].valueInteger, 1)
        self.assertEqual(inst.id, "list-example-codes")
        self.assertEqual(inst.identifier[0].system, "urn:ietf:rfc:3986")
        self.assertEqual(inst.identifier[0].value, "urn:oid:2.16.840.1.113883.4.642.4.1105")
        self.assertEqual(inst.meta.lastUpdated.date, FHIRDate("2019-11-01T09:29:23.356+11:00").date)
        self.assertEqual(inst.meta.lastUpdated.as_json(), "2019-11-01T09:29:23.356+11:00")
        self.assertEqual(inst.meta.profile[0], "http://hl7.org/fhir/StructureDefinition/shareablecodesystem")
        self.assertEqual(inst.name, "ExampleUseCodesForList")
        self.assertEqual(inst.publisher, "FHIR Project")
        self.assertEqual(inst.status, "draft")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.title, "Example Use Codes for List")
        self.assertEqual(inst.url, "http://terminology.hl7.org/CodeSystem/list-example-use-codes")
        self.assertEqual(inst.valueSet, "http://hl7.org/fhir/ValueSet/list-example-codes")
        self.assertEqual(inst.version, "4.0.1")
    
    def testCodeSystem3(self):
        inst = self.instantiate_from("codesystem-examplescenario-actor-type.json")
        self.assertIsNotNone(inst, "Must have instantiated a CodeSystem instance")
        self.implCodeSystem3(inst)
        
        js = inst.as_json()
        self.assertEqual("CodeSystem", js["resourceType"])
        inst2 = codesystem.CodeSystem(js)
        self.implCodeSystem3(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implCodeSystem3(self, inst):
        self.assertTrue(inst.caseSensitive)
        self.assertEqual(inst.concept[0].code, "person")
        self.assertEqual(inst.concept[0].definition, "A person.")
        self.assertEqual(inst.concept[0].display, "Person")
        self.assertEqual(inst.concept[1].code, "entity")
        self.assertEqual(inst.concept[1].definition, "A system.")
        self.assertEqual(inst.concept[1].display, "System")
        self.assertEqual(inst.contact[0].telecom[0].system, "url")
        self.assertEqual(inst.contact[0].telecom[0].value, "http://hl7.org/fhir")
        self.assertEqual(inst.contact[0].telecom[1].system, "email")
        self.assertEqual(inst.contact[0].telecom[1].value, "fhir@lists.hl7.org")
        self.assertEqual(inst.content, "complete")
        self.assertEqual(inst.date.date, FHIRDate("2019-11-01T09:29:23+11:00").date)
        self.assertEqual(inst.date.as_json(), "2019-11-01T09:29:23+11:00")
        self.assertEqual(inst.description, "The type of actor - system or human.")
        self.assertFalse(inst.experimental)
        self.assertEqual(inst.extension[0].url, "http://hl7.org/fhir/StructureDefinition/structuredefinition-wg")
        self.assertEqual(inst.extension[0].valueCode, "fhir")
        self.assertEqual(inst.extension[1].url, "http://hl7.org/fhir/StructureDefinition/structuredefinition-standards-status")
        self.assertEqual(inst.extension[1].valueCode, "trial-use")
        self.assertEqual(inst.extension[2].url, "http://hl7.org/fhir/StructureDefinition/structuredefinition-fmm")
        self.assertEqual(inst.extension[2].valueInteger, 0)
        self.assertEqual(inst.id, "examplescenario-actor-type")
        self.assertEqual(inst.identifier[0].system, "urn:ietf:rfc:3986")
        self.assertEqual(inst.identifier[0].value, "urn:oid:2.16.840.1.113883.4.642.4.859")
        self.assertEqual(inst.meta.lastUpdated.date, FHIRDate("2019-11-01T09:29:23.356+11:00").date)
        self.assertEqual(inst.meta.lastUpdated.as_json(), "2019-11-01T09:29:23.356+11:00")
        self.assertEqual(inst.name, "ExampleScenarioActorType")
        self.assertEqual(inst.publisher, "HL7 (FHIR Project)")
        self.assertEqual(inst.status, "draft")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.title, "ExampleScenarioActorType")
        self.assertEqual(inst.url, "http://hl7.org/fhir/examplescenario-actor-type")
        self.assertEqual(inst.valueSet, "http://hl7.org/fhir/ValueSet/examplescenario-actor-type")
        self.assertEqual(inst.version, "4.0.1")
    
    def testCodeSystem4(self):
        inst = self.instantiate_from("codesystem-example-summary.json")
        self.assertIsNotNone(inst, "Must have instantiated a CodeSystem instance")
        self.implCodeSystem4(inst)
        
        js = inst.as_json()
        self.assertEqual("CodeSystem", js["resourceType"])
        inst2 = codesystem.CodeSystem(js)
        self.implCodeSystem4(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implCodeSystem4(self, inst):
        self.assertTrue(inst.caseSensitive)
        self.assertEqual(inst.contact[0].name, "FHIR project team")
        self.assertEqual(inst.contact[0].telecom[0].system, "url")
        self.assertEqual(inst.contact[0].telecom[0].value, "http://hl7.org/fhir")
        self.assertEqual(inst.content, "not-present")
        self.assertEqual(inst.count, 92)
        self.assertEqual(inst.description, "This is an example code system summary for the ACME codes for body site.")
        self.assertTrue(inst.experimental)
        self.assertEqual(inst.id, "summary")
        self.assertEqual(inst.jurisdiction[0].coding[0].code, "CA")
        self.assertEqual(inst.jurisdiction[0].coding[0].system, "urn:iso:std:iso:3166")
        self.assertEqual(inst.name, "Code system summary example for ACME body sites")
        self.assertEqual(inst.publisher, "HL7 International")
        self.assertEqual(inst.status, "draft")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.url, "http://hl7.org/fhir/CodeSystem/summary")
        self.assertEqual(inst.useContext[0].code.code, "species")
        self.assertEqual(inst.useContext[0].code.system, "http://example.org/CodeSystem/contexttype")
        self.assertEqual(inst.useContext[0].valueCodeableConcept.coding[0].code, "337915000")
        self.assertEqual(inst.useContext[0].valueCodeableConcept.coding[0].display, "Homo sapiens (organism)")
        self.assertEqual(inst.useContext[0].valueCodeableConcept.coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.version, "4.0.1")
    
    def testCodeSystem5(self):
        inst = self.instantiate_from("codesystem-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a CodeSystem instance")
        self.implCodeSystem5(inst)
        
        js = inst.as_json()
        self.assertEqual("CodeSystem", js["resourceType"])
        inst2 = codesystem.CodeSystem(js)
        self.implCodeSystem5(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implCodeSystem5(self, inst):
        self.assertTrue(inst.caseSensitive)
        self.assertEqual(inst.concept[0].code, "chol-mmol")
        self.assertEqual(inst.concept[0].definition, "Serum Cholesterol, in mmol/L")
        self.assertEqual(inst.concept[0].designation[0].use.code, "internal-label")
        self.assertEqual(inst.concept[0].designation[0].use.system, "http://acme.com/config/fhir/codesystems/internal")
        self.assertEqual(inst.concept[0].designation[0].value, "From ACME POC Testing")
        self.assertEqual(inst.concept[0].display, "SChol (mmol/L)")
        self.assertEqual(inst.concept[1].code, "chol-mass")
        self.assertEqual(inst.concept[1].definition, "Serum Cholesterol, in mg/L")
        self.assertEqual(inst.concept[1].designation[0].use.code, "internal-label")
        self.assertEqual(inst.concept[1].designation[0].use.system, "http://acme.com/config/fhir/codesystems/internal")
        self.assertEqual(inst.concept[1].designation[0].value, "From Paragon Labs")
        self.assertEqual(inst.concept[1].display, "SChol (mg/L)")
        self.assertEqual(inst.concept[2].code, "chol")
        self.assertEqual(inst.concept[2].definition, "Serum Cholesterol")
        self.assertEqual(inst.concept[2].designation[0].use.code, "internal-label")
        self.assertEqual(inst.concept[2].designation[0].use.system, "http://acme.com/config/fhir/codesystems/internal")
        self.assertEqual(inst.concept[2].designation[0].value, "Obdurate Labs uses this with both kinds of units...")
        self.assertEqual(inst.concept[2].display, "SChol")
        self.assertEqual(inst.contact[0].name, "FHIR project team")
        self.assertEqual(inst.contact[0].telecom[0].system, "url")
        self.assertEqual(inst.contact[0].telecom[0].value, "http://hl7.org/fhir")
        self.assertEqual(inst.content, "complete")
        self.assertEqual(inst.date.date, FHIRDate("2016-01-28").date)
        self.assertEqual(inst.date.as_json(), "2016-01-28")
        self.assertEqual(inst.description, "This is an example code system that includes all the ACME codes for serum/plasma cholesterol from v2.36.")
        self.assertTrue(inst.experimental)
        self.assertEqual(inst.filter[0].code, "acme-plasma")
        self.assertEqual(inst.filter[0].description, "An internal filter used to select codes that are only used with plasma")
        self.assertEqual(inst.filter[0].operator[0], "=")
        self.assertEqual(inst.filter[0].value, "the value of this filter is either 'true' or 'false'")
        self.assertEqual(inst.id, "example")
        self.assertEqual(inst.identifier[0].system, "http://acme.com/identifiers/codesystems")
        self.assertEqual(inst.identifier[0].value, "internal-cholesterol-inl")
        self.assertEqual(inst.meta.profile[0], "http://hl7.org/fhir/StructureDefinition/shareablecodesystem")
        self.assertEqual(inst.name, "ACMECholCodesBlood")
        self.assertEqual(inst.publisher, "Acme Co")
        self.assertEqual(inst.status, "draft")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.title, "ACME Codes for Cholesterol in Serum/Plasma")
        self.assertEqual(inst.url, "http://hl7.org/fhir/CodeSystem/example")
        self.assertEqual(inst.version, "20160128")

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