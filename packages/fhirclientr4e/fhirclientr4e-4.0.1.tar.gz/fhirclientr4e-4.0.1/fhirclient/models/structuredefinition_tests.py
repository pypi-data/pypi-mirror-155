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

from . import structuredefinition

from .fhirdate import FHIRDate
import logging


class StructureDefinitionTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("StructureDefinition", js["resourceType"])
        return structuredefinition.StructureDefinition(js)
    
    def testStructureDefinition1(self):
        inst = self.instantiate_from("structuredefinition-example-section-library.json")
        self.assertIsNotNone(inst, "Must have instantiated a StructureDefinition instance")
        self.implStructureDefinition1(inst)
        
        js = inst.as_json()
        self.assertEqual("StructureDefinition", js["resourceType"])
        inst2 = structuredefinition.StructureDefinition(js)
        self.implStructureDefinition1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implStructureDefinition1(self, inst):
        self.assertTrue(inst.abstract)
        self.assertEqual(inst.baseDefinition, "http://hl7.org/fhir/StructureDefinition/Composition")
        self.assertEqual(inst.date.date, FHIRDate("2018-11-05T17:57:00+11:00").date)
        self.assertEqual(inst.date.as_json(), "2018-11-05T17:57:00+11:00")
        self.assertEqual(inst.derivation, "constraint")
        self.assertEqual(inst.differential.element[0].id, "Composition")
        self.assertEqual(inst.differential.element[0].path, "Composition")
        self.assertEqual(inst.differential.element[1].id, "Composition.section")
        self.assertEqual(inst.differential.element[1].path, "Composition.section")
        self.assertEqual(inst.differential.element[1].slicing.description, "Slice by .section.code when using this library of sections")
        self.assertEqual(inst.differential.element[1].slicing.discriminator[0].path, "code")
        self.assertEqual(inst.differential.element[1].slicing.discriminator[0].type, "pattern")
        self.assertTrue(inst.differential.element[1].slicing.ordered)
        self.assertEqual(inst.differential.element[1].slicing.rules, "closed")
        self.assertEqual(inst.differential.element[2].id, "Composition.section:procedure")
        self.assertEqual(inst.differential.element[2].path, "Composition.section")
        self.assertEqual(inst.differential.element[2].sliceName, "procedure")
        self.assertEqual(inst.differential.element[3].fixedString, "Procedures Performed")
        self.assertEqual(inst.differential.element[3].id, "Composition.section:procedure.title")
        self.assertEqual(inst.differential.element[3].min, 1)
        self.assertEqual(inst.differential.element[3].path, "Composition.section.title")
        self.assertEqual(inst.differential.element[4].id, "Composition.section:procedure.code")
        self.assertEqual(inst.differential.element[4].min, 1)
        self.assertEqual(inst.differential.element[4].path, "Composition.section.code")
        self.assertEqual(inst.differential.element[4].patternCodeableConcept.coding[0].code, "29554-3")
        self.assertEqual(inst.differential.element[4].patternCodeableConcept.coding[0].display, "Procedure Narrative")
        self.assertEqual(inst.differential.element[4].patternCodeableConcept.coding[0].system, "http://loinc.org")
        self.assertEqual(inst.differential.element[5].id, "Composition.section:medications")
        self.assertEqual(inst.differential.element[5].path, "Composition.section")
        self.assertEqual(inst.differential.element[5].sliceName, "medications")
        self.assertEqual(inst.differential.element[6].fixedString, "Medications Administered")
        self.assertEqual(inst.differential.element[6].id, "Composition.section:medications.title")
        self.assertEqual(inst.differential.element[6].min, 1)
        self.assertEqual(inst.differential.element[6].path, "Composition.section.title")
        self.assertEqual(inst.differential.element[7].id, "Composition.section:medications.code")
        self.assertEqual(inst.differential.element[7].min, 1)
        self.assertEqual(inst.differential.element[7].path, "Composition.section.code")
        self.assertEqual(inst.differential.element[7].patternCodeableConcept.coding[0].code, "29549-3")
        self.assertEqual(inst.differential.element[7].patternCodeableConcept.coding[0].display, "Medication administered Narrative")
        self.assertEqual(inst.differential.element[7].patternCodeableConcept.coding[0].system, "http://loinc.org")
        self.assertEqual(inst.differential.element[8].id, "Composition.section:plan")
        self.assertEqual(inst.differential.element[8].path, "Composition.section")
        self.assertEqual(inst.differential.element[8].sliceName, "plan")
        self.assertEqual(inst.differential.element[9].fixedString, "Discharge Treatment Plan")
        self.assertEqual(inst.differential.element[9].id, "Composition.section:plan.title")
        self.assertEqual(inst.differential.element[9].min, 1)
        self.assertEqual(inst.differential.element[9].path, "Composition.section.title")
        self.assertFalse(inst.experimental)
        self.assertEqual(inst.id, "example-section-library")
        self.assertEqual(inst.kind, "complex-type")
        self.assertEqual(inst.name, "DocumentSectionLibrary")
        self.assertEqual(inst.status, "active")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.title, "Document Section Library (For testing section templates)")
        self.assertEqual(inst.type, "Composition")
        self.assertEqual(inst.url, "http://hl7.org/fhir/StructureDefinition/example-section-library")
    
    def testStructureDefinition2(self):
        inst = self.instantiate_from("structuredefinition-example-composition.json")
        self.assertIsNotNone(inst, "Must have instantiated a StructureDefinition instance")
        self.implStructureDefinition2(inst)
        
        js = inst.as_json()
        self.assertEqual("StructureDefinition", js["resourceType"])
        inst2 = structuredefinition.StructureDefinition(js)
        self.implStructureDefinition2(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implStructureDefinition2(self, inst):
        self.assertFalse(inst.abstract)
        self.assertEqual(inst.baseDefinition, "http://hl7.org/fhir/StructureDefinition/Composition")
        self.assertEqual(inst.date.date, FHIRDate("2018-11-05T17:47:00+11:00").date)
        self.assertEqual(inst.date.as_json(), "2018-11-05T17:47:00+11:00")
        self.assertEqual(inst.derivation, "constraint")
        self.assertEqual(inst.differential.element[0].id, "Composition")
        self.assertEqual(inst.differential.element[0].path, "Composition")
        self.assertEqual(inst.differential.element[1].id, "Composition.section")
        self.assertEqual(inst.differential.element[1].path, "Composition.section")
        self.assertEqual(inst.differential.element[1].slicing.description, "Slice by .section.code")
        self.assertEqual(inst.differential.element[1].slicing.discriminator[0].path, "code")
        self.assertEqual(inst.differential.element[1].slicing.discriminator[0].type, "pattern")
        self.assertTrue(inst.differential.element[1].slicing.ordered)
        self.assertEqual(inst.differential.element[1].slicing.rules, "closed")
        self.assertEqual(inst.differential.element[2].id, "Composition.section:procedure")
        self.assertEqual(inst.differential.element[2].min, 1)
        self.assertEqual(inst.differential.element[2].path, "Composition.section")
        self.assertEqual(inst.differential.element[2].sliceName, "procedure")
        self.assertEqual(inst.differential.element[2].type[0].code, "BackboneElement")
        self.assertEqual(inst.differential.element[2].type[0].profile[0], "http://hl7.org/fhir/StructureDefinition/document-section-library")
        self.assertEqual(inst.differential.element[3].id, "Composition.section:medications")
        self.assertEqual(inst.differential.element[3].min, 1)
        self.assertEqual(inst.differential.element[3].path, "Composition.section")
        self.assertEqual(inst.differential.element[3].sliceName, "medications")
        self.assertEqual(inst.differential.element[3].type[0].code, "BackboneElement")
        self.assertEqual(inst.differential.element[3].type[0].profile[0], "http://hl7.org/fhir/StructureDefinition/document-section-library")
        self.assertEqual(inst.differential.element[4].id, "Composition.section:plan")
        self.assertEqual(inst.differential.element[4].min, 0)
        self.assertEqual(inst.differential.element[4].path, "Composition.section")
        self.assertEqual(inst.differential.element[4].sliceName, "plan")
        self.assertEqual(inst.differential.element[4].type[0].code, "BackboneElement")
        self.assertEqual(inst.differential.element[4].type[0].profile[0], "http://hl7.org/fhir/StructureDefinition/document-section-library")
        self.assertFalse(inst.experimental)
        self.assertEqual(inst.id, "example-composition")
        self.assertEqual(inst.kind, "complex-type")
        self.assertEqual(inst.name, "DocumentStructure")
        self.assertEqual(inst.status, "active")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.title, "Document Structure (For testing section templates)")
        self.assertEqual(inst.type, "Composition")
        self.assertEqual(inst.url, "http://hl7.org/fhir/StructureDefinition/example-composition")

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