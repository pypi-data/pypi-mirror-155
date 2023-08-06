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

from . import operationdefinition

from .fhirdate import FHIRDate
import logging


class OperationDefinitionTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("OperationDefinition", js["resourceType"])
        return operationdefinition.OperationDefinition(js)
    
    def testOperationDefinition1(self):
        inst = self.instantiate_from("operationdefinition-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a OperationDefinition instance")
        self.implOperationDefinition1(inst)
        
        js = inst.as_json()
        self.assertEqual("OperationDefinition", js["resourceType"])
        inst2 = operationdefinition.OperationDefinition(js)
        self.implOperationDefinition1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implOperationDefinition1(self, inst):
        self.assertEqual(inst.base, "OperationDefinition/Questionnaire-populate")
        self.assertEqual(inst.code, "populate")
        self.assertEqual(inst.comment, "Only implemented for Labs and Medications so far")
        self.assertEqual(inst.contact[0].name, "System Administrator")
        self.assertEqual(inst.contact[0].telecom[0].system, "email")
        self.assertEqual(inst.contact[0].telecom[0].value, "beep@coyote.acme.com")
        self.assertEqual(inst.date.date, FHIRDate("2015-08-04").date)
        self.assertEqual(inst.date.as_json(), "2015-08-04")
        self.assertEqual(inst.description, "Limited implementation of the Populate Questionnaire implementation")
        self.assertEqual(inst.id, "example")
        self.assertTrue(inst.instance)
        self.assertEqual(inst.jurisdiction[0].coding[0].code, "GB")
        self.assertEqual(inst.jurisdiction[0].coding[0].display, "United Kingdom of Great Britain and Northern Ireland (the)")
        self.assertEqual(inst.jurisdiction[0].coding[0].system, "urn:iso:std:iso:3166")
        self.assertEqual(inst.kind, "operation")
        self.assertEqual(inst.name, "Populate Questionnaire")
        self.assertEqual(inst.overload[0].parameterName[0], "subject")
        self.assertEqual(inst.overload[0].parameterName[1], "local")
        self.assertEqual(inst.overload[1].comment, "local defaults to false when not passed as a parameter")
        self.assertEqual(inst.overload[1].parameterName[0], "subject")
        self.assertEqual(inst.parameter[0].max, "1")
        self.assertEqual(inst.parameter[0].min, 1)
        self.assertEqual(inst.parameter[0].name, "subject")
        self.assertEqual(inst.parameter[0].type, "Reference")
        self.assertEqual(inst.parameter[0].use, "in")
        self.assertEqual(inst.parameter[1].documentation, "If the *local* parameter is set to true, server information about the specified subject will be used to populate the instance.")
        self.assertEqual(inst.parameter[1].max, "1")
        self.assertEqual(inst.parameter[1].min, 0)
        self.assertEqual(inst.parameter[1].name, "local")
        self.assertEqual(inst.parameter[1].type, "Reference")
        self.assertEqual(inst.parameter[1].use, "in")
        self.assertEqual(inst.parameter[2].documentation, "The partially (or fully)-populated set of answers for the specified Questionnaire")
        self.assertEqual(inst.parameter[2].max, "1")
        self.assertEqual(inst.parameter[2].min, 1)
        self.assertEqual(inst.parameter[2].name, "return")
        self.assertEqual(inst.parameter[2].type, "QuestionnaireResponse")
        self.assertEqual(inst.parameter[2].use, "out")
        self.assertEqual(inst.publisher, "Acme Healthcare Services")
        self.assertEqual(inst.resource[0], "Questionnaire")
        self.assertEqual(inst.status, "draft")
        self.assertFalse(inst.system)
        self.assertEqual(inst.text.status, "generated")
        self.assertFalse(inst.type)
        self.assertEqual(inst.url, "http://h7.org/fhir/OperationDefinition/example")
        self.assertEqual(inst.useContext[0].code.code, "venue")
        self.assertEqual(inst.useContext[0].code.display, "Clinical Venue")
        self.assertEqual(inst.useContext[0].code.system, "http://build.fhir.org/codesystem-usage-context-type")
        self.assertEqual(inst.useContext[0].valueCodeableConcept.coding[0].code, "IMP")
        self.assertEqual(inst.useContext[0].valueCodeableConcept.coding[0].display, "inpatient encounter")
        self.assertEqual(inst.useContext[0].valueCodeableConcept.coding[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActCode")
        self.assertEqual(inst.version, "B")

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