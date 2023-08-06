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

from . import conceptmap

from .fhirdate import FHIRDate
import logging


class ConceptMapTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("ConceptMap", js["resourceType"])
        return conceptmap.ConceptMap(js)
    
    def testConceptMap1(self):
        inst = self.instantiate_from("conceptmap-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a ConceptMap instance")
        self.implConceptMap1(inst)
        
        js = inst.as_json()
        self.assertEqual("ConceptMap", js["resourceType"])
        inst2 = conceptmap.ConceptMap(js)
        self.implConceptMap1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implConceptMap1(self, inst):
        self.assertEqual(inst.contact[0].name, "FHIR project team (example)")
        self.assertEqual(inst.contact[0].telecom[0].system, "url")
        self.assertEqual(inst.contact[0].telecom[0].value, "http://hl7.org/fhir")
        self.assertEqual(inst.copyright, "Creative Commons 0")
        self.assertEqual(inst.date.date, FHIRDate("2012-06-13").date)
        self.assertEqual(inst.date.as_json(), "2012-06-13")
        self.assertEqual(inst.description, "A mapping between the FHIR and HL7 v3 AddressUse Code systems")
        self.assertTrue(inst.experimental)
        self.assertEqual(inst.group[0].element[0].code, "home")
        self.assertEqual(inst.group[0].element[0].display, "home")
        self.assertEqual(inst.group[0].element[0].target[0].code, "H")
        self.assertEqual(inst.group[0].element[0].target[0].display, "home")
        self.assertEqual(inst.group[0].element[0].target[0].equivalence, "equivalent")
        self.assertEqual(inst.group[0].element[1].code, "work")
        self.assertEqual(inst.group[0].element[1].display, "work")
        self.assertEqual(inst.group[0].element[1].target[0].code, "WP")
        self.assertEqual(inst.group[0].element[1].target[0].display, "work place")
        self.assertEqual(inst.group[0].element[1].target[0].equivalence, "equivalent")
        self.assertEqual(inst.group[0].element[2].code, "temp")
        self.assertEqual(inst.group[0].element[2].display, "temp")
        self.assertEqual(inst.group[0].element[2].target[0].code, "TMP")
        self.assertEqual(inst.group[0].element[2].target[0].display, "temporary address")
        self.assertEqual(inst.group[0].element[2].target[0].equivalence, "equivalent")
        self.assertEqual(inst.group[0].element[3].code, "old")
        self.assertEqual(inst.group[0].element[3].display, "old")
        self.assertEqual(inst.group[0].element[3].target[0].code, "BAD")
        self.assertEqual(inst.group[0].element[3].target[0].comment, "In the HL7 v3 AD, old is handled by the usablePeriod element, but you have to provide a time, there's no simple equivalent of flagging an address as old")
        self.assertEqual(inst.group[0].element[3].target[0].display, "bad address")
        self.assertEqual(inst.group[0].element[3].target[0].equivalence, "disjoint")
        self.assertEqual(inst.group[0].source, "http://hl7.org/fhir/address-use")
        self.assertEqual(inst.group[0].target, "http://terminology.hl7.org/CodeSystem/v3-AddressUse")
        self.assertEqual(inst.group[0].unmapped.code, "temp")
        self.assertEqual(inst.group[0].unmapped.display, "temp")
        self.assertEqual(inst.group[0].unmapped.mode, "fixed")
        self.assertEqual(inst.id, "101")
        self.assertEqual(inst.identifier.system, "urn:ietf:rfc:3986")
        self.assertEqual(inst.identifier.value, "urn:uuid:53cd62ee-033e-414c-9f58-3ca97b5ffc3b")
        self.assertEqual(inst.jurisdiction[0].coding[0].code, "US")
        self.assertEqual(inst.jurisdiction[0].coding[0].system, "urn:iso:std:iso:3166")
        self.assertEqual(inst.name, "FHIR-v3-Address-Use")
        self.assertEqual(inst.publisher, "HL7, Inc")
        self.assertEqual(inst.purpose, "To help implementers map from HL7 v3/CDA to FHIR")
        self.assertEqual(inst.sourceUri, "http://hl7.org/fhir/ValueSet/address-use")
        self.assertEqual(inst.status, "draft")
        self.assertEqual(inst.targetUri, "http://terminology.hl7.org/ValueSet/v3-AddressUse")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.title, "FHIR/v3 Address Use Mapping")
        self.assertEqual(inst.url, "http://hl7.org/fhir/ConceptMap/101")
        self.assertEqual(inst.useContext[0].code.code, "venue")
        self.assertEqual(inst.useContext[0].code.system, "http://terminology.hl7.org/CodeSystem/usage-context-type")
        self.assertEqual(inst.useContext[0].valueCodeableConcept.text, "for CCDA Usage")
        self.assertEqual(inst.version, "4.0.1")
    
    def testConceptMap2(self):
        inst = self.instantiate_from("conceptmap-example-2.json")
        self.assertIsNotNone(inst, "Must have instantiated a ConceptMap instance")
        self.implConceptMap2(inst)
        
        js = inst.as_json()
        self.assertEqual("ConceptMap", js["resourceType"])
        inst2 = conceptmap.ConceptMap(js)
        self.implConceptMap2(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implConceptMap2(self, inst):
        self.assertEqual(inst.contact[0].name, "FHIR project team (example)")
        self.assertEqual(inst.contact[0].telecom[0].system, "url")
        self.assertEqual(inst.contact[0].telecom[0].value, "http://hl7.org/fhir")
        self.assertEqual(inst.date.date, FHIRDate("2012-06-13").date)
        self.assertEqual(inst.date.as_json(), "2012-06-13")
        self.assertEqual(inst.description, "An example mapping")
        self.assertTrue(inst.experimental)
        self.assertEqual(inst.group[0].element[0].code, "code")
        self.assertEqual(inst.group[0].element[0].display, "Example Code")
        self.assertEqual(inst.group[0].element[0].target[0].code, "code2")
        self.assertEqual(inst.group[0].element[0].target[0].dependsOn[0].display, "Something Coded")
        self.assertEqual(inst.group[0].element[0].target[0].dependsOn[0].property, "http://example.org/fhir/property-value/example")
        self.assertEqual(inst.group[0].element[0].target[0].dependsOn[0].system, "http://example.org/fhir/example3")
        self.assertEqual(inst.group[0].element[0].target[0].dependsOn[0].value, "some-code")
        self.assertEqual(inst.group[0].element[0].target[0].display, "Some Example Code")
        self.assertEqual(inst.group[0].element[0].target[0].equivalence, "equivalent")
        self.assertEqual(inst.group[0].source, "http://example.org/fhir/example1")
        self.assertEqual(inst.group[0].target, "http://example.org/fhir/example2")
        self.assertEqual(inst.group[0].unmapped.mode, "other-map")
        self.assertEqual(inst.group[0].unmapped.url, "http://example.org/fhir/ConceptMap/map2")
        self.assertEqual(inst.id, "example2")
        self.assertEqual(inst.name, "FHIR-exanple-2")
        self.assertEqual(inst.publisher, "HL7, Inc")
        self.assertEqual(inst.purpose, "To illustrate mapping features")
        self.assertEqual(inst.sourceUri, "http://example.org/fhir/example1")
        self.assertEqual(inst.status, "draft")
        self.assertEqual(inst.targetUri, "http://example.org/fhir/example2")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.title, "FHIR Example 2")
        self.assertEqual(inst.url, "http://hl7.org/fhir/ConceptMap/example2")
        self.assertEqual(inst.version, "4.0.1")
    
    def testConceptMap3(self):
        inst = self.instantiate_from("conceptmap-example-specimen-type.json")
        self.assertIsNotNone(inst, "Must have instantiated a ConceptMap instance")
        self.implConceptMap3(inst)
        
        js = inst.as_json()
        self.assertEqual("ConceptMap", js["resourceType"])
        inst2 = conceptmap.ConceptMap(js)
        self.implConceptMap3(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implConceptMap3(self, inst):
        self.assertEqual(inst.contact[0].telecom[0].system, "url")
        self.assertEqual(inst.contact[0].telecom[0].value, "http://hl7.org/fhir")
        self.assertEqual(inst.contact[1].telecom[0].system, "url")
        self.assertEqual(inst.contact[1].telecom[0].value, "http://www.phconnect.org/group/laboratorymessagingcommunityofpractice/forum/attachment/download?id=3649725%3AUploadedFile%3A145786")
        self.assertEqual(inst.date.date, FHIRDate("2013-07-25").date)
        self.assertEqual(inst.date.as_json(), "2013-07-25")
        self.assertFalse(inst.experimental)
        self.assertEqual(inst.group[0].element[0].code, "ACNE")
        self.assertEqual(inst.group[0].element[0].target[0].code, "309068002")
        self.assertEqual(inst.group[0].element[0].target[0].equivalence, "equivalent")
        self.assertEqual(inst.group[0].element[1].code, "ACNFLD")
        self.assertEqual(inst.group[0].element[1].target[0].code, "119323008")
        self.assertEqual(inst.group[0].element[1].target[0].comment, "HL7 term is a historical term. mapped to Pus")
        self.assertEqual(inst.group[0].element[1].target[0].equivalence, "equivalent")
        self.assertEqual(inst.group[0].element[1].target[0].product[0].property, "TypeModifier")
        self.assertEqual(inst.group[0].element[1].target[0].product[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.group[0].element[1].target[0].product[0].value, "47002008")
        self.assertEqual(inst.group[0].element[2].code, "AIRS")
        self.assertEqual(inst.group[0].element[2].target[0].code, "446302006")
        self.assertEqual(inst.group[0].element[2].target[0].equivalence, "equivalent")
        self.assertEqual(inst.group[0].element[3].code, "ALL")
        self.assertEqual(inst.group[0].element[3].target[0].code, "119376003")
        self.assertEqual(inst.group[0].element[3].target[0].equivalence, "equivalent")
        self.assertEqual(inst.group[0].element[3].target[0].product[0].property, "TypeModifier")
        self.assertEqual(inst.group[0].element[3].target[0].product[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.group[0].element[3].target[0].product[0].value, "7970006")
        self.assertEqual(inst.group[0].element[4].code, "AMP")
        self.assertEqual(inst.group[0].element[4].target[0].code, "408654003")
        self.assertEqual(inst.group[0].element[4].target[0].equivalence, "equivalent")
        self.assertEqual(inst.group[0].element[4].target[0].product[0].property, "http://snomed.info/id/246380002")
        self.assertEqual(inst.group[0].element[4].target[0].product[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.group[0].element[4].target[0].product[0].value, "81723002")
        self.assertEqual(inst.group[0].element[5].code, "ANGI")
        self.assertEqual(inst.group[0].element[5].target[0].code, "119312009")
        self.assertEqual(inst.group[0].element[5].target[0].comment, "TBD in detail")
        self.assertEqual(inst.group[0].element[5].target[0].equivalence, "equivalent")
        self.assertEqual(inst.group[0].element[6].code, "ARTC")
        self.assertEqual(inst.group[0].element[6].target[0].code, "119312009")
        self.assertEqual(inst.group[0].element[6].target[0].comment, "TBD in detail")
        self.assertEqual(inst.group[0].element[6].target[0].equivalence, "equivalent")
        self.assertEqual(inst.group[0].element[7].code, "ASERU")
        self.assertEqual(inst.group[0].element[7].target[0].comment, "pending")
        self.assertEqual(inst.group[0].element[7].target[0].equivalence, "unmatched")
        self.assertEqual(inst.group[0].element[8].code, "ASP")
        self.assertEqual(inst.group[0].element[8].target[0].code, "119295008")
        self.assertEqual(inst.group[0].element[8].target[0].equivalence, "equivalent")
        self.assertEqual(inst.group[0].element[8].target[0].product[0].property, "http://snomed.info/id/246380002")
        self.assertEqual(inst.group[0].element[8].target[0].product[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.group[0].element[8].target[0].product[0].value, "14766002")
        self.assertEqual(inst.group[0].element[9].code, "ATTE")
        self.assertEqual(inst.group[0].element[9].target[0].comment, "TBD")
        self.assertEqual(inst.group[0].element[9].target[0].equivalence, "unmatched")
        self.assertEqual(inst.group[0].source, "http://terminology.hl7.org/CodeSystem/v2-0487")
        self.assertEqual(inst.group[0].target, "http://snomed.info/sct")
        self.assertEqual(inst.id, "102")
        self.assertEqual(inst.name, "Specimen mapping from v2 table 0487 to SNOMED CT")
        self.assertEqual(inst.publisher, "FHIR project team (original source: LabMCoP)")
        self.assertEqual(inst.sourceCanonical, "http://terminology.hl7.org/ValueSet/v2-0487")
        self.assertEqual(inst.status, "draft")
        self.assertEqual(inst.targetCanonical, "http://snomed.info/sct?fhir_vs")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.url, "http://hl7.org/fhir/ConceptMap/102")
        self.assertEqual(inst.version, "4.0.1")

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