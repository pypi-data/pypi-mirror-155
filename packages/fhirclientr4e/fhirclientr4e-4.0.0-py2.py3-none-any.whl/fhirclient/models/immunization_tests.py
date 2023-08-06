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

from . import immunization

from .fhirdate import FHIRDate
import logging


class ImmunizationTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("Immunization", js["resourceType"])
        return immunization.Immunization(js)
    
    def testImmunization1(self):
        inst = self.instantiate_from("immunization-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a Immunization instance")
        self.implImmunization1(inst)
        
        js = inst.as_json()
        self.assertEqual("Immunization", js["resourceType"])
        inst2 = immunization.Immunization(js)
        self.implImmunization1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implImmunization1(self, inst):
        self.assertEqual(inst.doseQuantity.code, "mg")
        self.assertEqual(inst.doseQuantity.system, "http://unitsofmeasure.org")
        self.assertEqual(inst.doseQuantity.value, 5)
        self.assertEqual(inst.education[0].documentType, "253088698300010311120702")
        self.assertEqual(inst.education[0].presentationDate.date, FHIRDate("2013-01-10").date)
        self.assertEqual(inst.education[0].presentationDate.as_json(), "2013-01-10")
        self.assertEqual(inst.education[0].publicationDate.date, FHIRDate("2012-07-02").date)
        self.assertEqual(inst.education[0].publicationDate.as_json(), "2012-07-02")
        self.assertEqual(inst.expirationDate.date, FHIRDate("2015-02-15").date)
        self.assertEqual(inst.expirationDate.as_json(), "2015-02-15")
        self.assertEqual(inst.fundingSource.coding[0].code, "private")
        self.assertEqual(inst.fundingSource.coding[0].system, "http://terminology.hl7.org/CodeSystem/immunization-funding-source")
        self.assertEqual(inst.id, "example")
        self.assertEqual(inst.identifier[0].system, "urn:ietf:rfc:3986")
        self.assertEqual(inst.identifier[0].value, "urn:oid:1.3.6.1.4.1.21367.2005.3.7.1234")
        self.assertTrue(inst.isSubpotent)
        self.assertEqual(inst.lotNumber, "AAJN11K")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.note[0].text, "Notes on adminstration of vaccine")
        self.assertEqual(inst.occurrenceDateTime.date, FHIRDate("2013-01-10").date)
        self.assertEqual(inst.occurrenceDateTime.as_json(), "2013-01-10")
        self.assertEqual(inst.performer[0].function.coding[0].code, "OP")
        self.assertEqual(inst.performer[0].function.coding[0].system, "http://terminology.hl7.org/CodeSystem/v2-0443")
        self.assertEqual(inst.performer[1].function.coding[0].code, "AP")
        self.assertEqual(inst.performer[1].function.coding[0].system, "http://terminology.hl7.org/CodeSystem/v2-0443")
        self.assertTrue(inst.primarySource)
        self.assertEqual(inst.programEligibility[0].coding[0].code, "ineligible")
        self.assertEqual(inst.programEligibility[0].coding[0].system, "http://terminology.hl7.org/CodeSystem/immunization-program-eligibility")
        self.assertEqual(inst.reasonCode[0].coding[0].code, "429060002")
        self.assertEqual(inst.reasonCode[0].coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.route.coding[0].code, "IM")
        self.assertEqual(inst.route.coding[0].display, "Injection, intramuscular")
        self.assertEqual(inst.route.coding[0].system, "http://terminology.hl7.org/CodeSystem/v3-RouteOfAdministration")
        self.assertEqual(inst.site.coding[0].code, "LA")
        self.assertEqual(inst.site.coding[0].display, "left arm")
        self.assertEqual(inst.site.coding[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActSite")
        self.assertEqual(inst.status, "completed")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.vaccineCode.coding[0].code, "FLUVAX")
        self.assertEqual(inst.vaccineCode.coding[0].system, "urn:oid:1.2.36.1.2001.1005.17")
        self.assertEqual(inst.vaccineCode.text, "Fluvax (Influenza)")
    
    def testImmunization2(self):
        inst = self.instantiate_from("immunization-example-historical.json")
        self.assertIsNotNone(inst, "Must have instantiated a Immunization instance")
        self.implImmunization2(inst)
        
        js = inst.as_json()
        self.assertEqual("Immunization", js["resourceType"])
        inst2 = immunization.Immunization(js)
        self.implImmunization2(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implImmunization2(self, inst):
        self.assertEqual(inst.id, "historical")
        self.assertEqual(inst.identifier[0].system, "urn:ietf:rfc:3986")
        self.assertEqual(inst.identifier[0].value, "urn:oid:1.3.6.1.4.1.21367.2005.3.7.1234")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.note[0].text, "Notes on adminstration of a historical vaccine")
        self.assertEqual(inst.occurrenceString, "January 2012")
        self.assertFalse(inst.primarySource)
        self.assertEqual(inst.reportOrigin.coding[0].code, "record")
        self.assertEqual(inst.reportOrigin.coding[0].system, "http://terminology.hl7.org/CodeSystem/immunization-origin")
        self.assertEqual(inst.reportOrigin.text, "Written Record")
        self.assertEqual(inst.status, "completed")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.vaccineCode.coding[0].code, "GNFLU")
        self.assertEqual(inst.vaccineCode.coding[0].system, "urn:oid:1.2.36.1.2001.1005.17")
        self.assertEqual(inst.vaccineCode.text, "Influenza")
    
    def testImmunization3(self):
        inst = self.instantiate_from("immunization-example-protocol.json")
        self.assertIsNotNone(inst, "Must have instantiated a Immunization instance")
        self.implImmunization3(inst)
        
        js = inst.as_json()
        self.assertEqual("Immunization", js["resourceType"])
        inst2 = immunization.Immunization(js)
        self.implImmunization3(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implImmunization3(self, inst):
        self.assertEqual(inst.doseQuantity.code, "mg")
        self.assertEqual(inst.doseQuantity.system, "http://unitsofmeasure.org")
        self.assertEqual(inst.doseQuantity.value, 5)
        self.assertEqual(inst.expirationDate.date, FHIRDate("2018-12-15").date)
        self.assertEqual(inst.expirationDate.as_json(), "2018-12-15")
        self.assertEqual(inst.fundingSource.coding[0].code, "private")
        self.assertEqual(inst.fundingSource.coding[0].system, "http://terminology.hl7.org/CodeSystem/immunization-funding-source")
        self.assertEqual(inst.id, "protocol")
        self.assertEqual(inst.identifier[0].system, "urn:ietf:rfc:3986")
        self.assertEqual(inst.identifier[0].value, "urn:oid:1.3.6.1.4.1.21367.2005.3.7.1234")
        self.assertFalse(inst.isSubpotent)
        self.assertEqual(inst.lotNumber, "PT123F")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.occurrenceDateTime.date, FHIRDate("2018-06-18").date)
        self.assertEqual(inst.occurrenceDateTime.as_json(), "2018-06-18")
        self.assertEqual(inst.performer[0].function.coding[0].code, "OP")
        self.assertEqual(inst.performer[0].function.coding[0].system, "http://terminology.hl7.org/CodeSystem/v2-0443")
        self.assertEqual(inst.performer[1].function.coding[0].code, "AP")
        self.assertEqual(inst.performer[1].function.coding[0].system, "http://terminology.hl7.org/CodeSystem/v2-0443")
        self.assertTrue(inst.primarySource)
        self.assertEqual(inst.programEligibility[0].coding[0].code, "ineligible")
        self.assertEqual(inst.programEligibility[0].coding[0].system, "http://terminology.hl7.org/CodeSystem/immunization-program-eligibility")
        self.assertEqual(inst.protocolApplied[0].doseNumberPositiveInt, 1)
        self.assertEqual(inst.protocolApplied[0].series, "2-dose")
        self.assertEqual(inst.protocolApplied[0].targetDisease[0].coding[0].code, "40468003")
        self.assertEqual(inst.protocolApplied[0].targetDisease[0].coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.protocolApplied[1].doseNumberPositiveInt, 2)
        self.assertEqual(inst.protocolApplied[1].series, "3-dose")
        self.assertEqual(inst.protocolApplied[1].targetDisease[0].coding[0].code, "66071002")
        self.assertEqual(inst.protocolApplied[1].targetDisease[0].coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.route.coding[0].code, "IM")
        self.assertEqual(inst.route.coding[0].display, "Injection, intramuscular")
        self.assertEqual(inst.route.coding[0].system, "http://terminology.hl7.org/CodeSystem/v3-RouteOfAdministration")
        self.assertEqual(inst.site.coding[0].code, "LA")
        self.assertEqual(inst.site.coding[0].display, "left arm")
        self.assertEqual(inst.site.coding[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActSite")
        self.assertEqual(inst.status, "completed")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.vaccineCode.coding[0].code, "104")
        self.assertEqual(inst.vaccineCode.coding[0].system, "http://hl7.org/fhir/sid/cvx")
        self.assertEqual(inst.vaccineCode.text, "Twinrix (HepA/HepB)")
    
    def testImmunization4(self):
        inst = self.instantiate_from("immunization-example-refused.json")
        self.assertIsNotNone(inst, "Must have instantiated a Immunization instance")
        self.implImmunization4(inst)
        
        js = inst.as_json()
        self.assertEqual("Immunization", js["resourceType"])
        inst2 = immunization.Immunization(js)
        self.implImmunization4(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implImmunization4(self, inst):
        self.assertEqual(inst.id, "notGiven")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.occurrenceDateTime.date, FHIRDate("2013-01-10").date)
        self.assertEqual(inst.occurrenceDateTime.as_json(), "2013-01-10")
        self.assertTrue(inst.primarySource)
        self.assertEqual(inst.status, "not-done")
        self.assertEqual(inst.statusReason.coding[0].code, "MEDPREC")
        self.assertEqual(inst.statusReason.coding[0].display, "medical precaution")
        self.assertEqual(inst.statusReason.coding[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.vaccineCode.coding[0].code, "01")
        self.assertEqual(inst.vaccineCode.coding[0].display, "DTP")
        self.assertEqual(inst.vaccineCode.coding[0].system, "http://hl7.org/fhir/sid/cvx")
    
    def testImmunization5(self):
        inst = self.instantiate_from("immunization-example-subpotent.json")
        self.assertIsNotNone(inst, "Must have instantiated a Immunization instance")
        self.implImmunization5(inst)
        
        js = inst.as_json()
        self.assertEqual("Immunization", js["resourceType"])
        inst2 = immunization.Immunization(js)
        self.implImmunization5(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implImmunization5(self, inst):
        self.assertEqual(inst.doseQuantity.code, "ml")
        self.assertEqual(inst.doseQuantity.system, "http://unitsofmeasure.org")
        self.assertEqual(inst.doseQuantity.value, 0.5)
        self.assertEqual(inst.education[0].documentType, "253088698300010311120702")
        self.assertEqual(inst.education[0].presentationDate.date, FHIRDate("2013-01-10").date)
        self.assertEqual(inst.education[0].presentationDate.as_json(), "2013-01-10")
        self.assertEqual(inst.education[0].publicationDate.date, FHIRDate("2012-07-02").date)
        self.assertEqual(inst.education[0].publicationDate.as_json(), "2012-07-02")
        self.assertEqual(inst.expirationDate.date, FHIRDate("2015-02-28").date)
        self.assertEqual(inst.expirationDate.as_json(), "2015-02-28")
        self.assertEqual(inst.fundingSource.coding[0].code, "private")
        self.assertEqual(inst.fundingSource.coding[0].system, "http://terminology.hl7.org/CodeSystem/immunization-funding-source")
        self.assertEqual(inst.id, "subpotent")
        self.assertEqual(inst.identifier[0].system, "urn:ietf:rfc:3986")
        self.assertEqual(inst.identifier[0].value, "urn:oid:1.3.6.1.4.1.21367.2005.3.7.1234")
        self.assertFalse(inst.isSubpotent)
        self.assertEqual(inst.lotNumber, "AAJN11K")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.note[0].text, "Notes on adminstration of vaccine")
        self.assertEqual(inst.occurrenceDateTime.date, FHIRDate("2015-01-15").date)
        self.assertEqual(inst.occurrenceDateTime.as_json(), "2015-01-15")
        self.assertEqual(inst.performer[0].function.coding[0].code, "OP")
        self.assertEqual(inst.performer[0].function.coding[0].system, "http://terminology.hl7.org/CodeSystem/v2-0443")
        self.assertEqual(inst.performer[1].function.coding[0].code, "AP")
        self.assertEqual(inst.performer[1].function.coding[0].system, "http://terminology.hl7.org/CodeSystem/v2-0443")
        self.assertTrue(inst.primarySource)
        self.assertEqual(inst.programEligibility[0].coding[0].code, "ineligible")
        self.assertEqual(inst.programEligibility[0].coding[0].system, "http://terminology.hl7.org/CodeSystem/immunization-program-eligibility")
        self.assertEqual(inst.route.coding[0].code, "IM")
        self.assertEqual(inst.route.coding[0].display, "Injection, intramuscular")
        self.assertEqual(inst.route.coding[0].system, "http://terminology.hl7.org/CodeSystem/v3-RouteOfAdministration")
        self.assertEqual(inst.site.coding[0].code, "LT")
        self.assertEqual(inst.site.coding[0].display, "left thigh")
        self.assertEqual(inst.site.coding[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActSite")
        self.assertEqual(inst.status, "completed")
        self.assertEqual(inst.subpotentReason[0].coding[0].code, "partial")
        self.assertEqual(inst.subpotentReason[0].coding[0].system, "http://terminology.hl7.org/CodeSystem/immunization-subpotent-reason")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.vaccineCode.coding[0].code, "GNHEP")
        self.assertEqual(inst.vaccineCode.coding[0].system, "urn:oid:1.2.36.1.2001.1005.17")
        self.assertEqual(inst.vaccineCode.text, "Hepatitis B")

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