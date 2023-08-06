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

from . import measurereport

from .fhirdate import FHIRDate
import logging


class MeasureReportTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("MeasureReport", js["resourceType"])
        return measurereport.MeasureReport(js)
    
    def testMeasureReport1(self):
        inst = self.instantiate_from("measurereport-cms146-cat1-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a MeasureReport instance")
        self.implMeasureReport1(inst)
        
        js = inst.as_json()
        self.assertEqual("MeasureReport", js["resourceType"])
        inst2 = measurereport.MeasureReport(js)
        self.implMeasureReport1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implMeasureReport1(self, inst):
        self.assertEqual(inst.contained[0].id, "reporter")
        self.assertEqual(inst.date.date, FHIRDate("2014-04-01").date)
        self.assertEqual(inst.date.as_json(), "2014-04-01")
        self.assertEqual(inst.group[0].id, "CMS146-group-1")
        self.assertEqual(inst.group[0].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].population[0].count, 1)
        self.assertEqual(inst.group[0].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].population[1].count, 1)
        self.assertEqual(inst.group[0].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].population[2].count, 1)
        self.assertEqual(inst.group[0].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].population[3].count, 0)
        self.assertEqual(inst.group[0].stratifier[0].code[0].text, "stratifier-ages-up-to-9")
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].population[0].count, 1)
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].population[1].count, 1)
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].population[2].count, 1)
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].population[3].count, 0)
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].value.text, "true")
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].population[0].count, 0)
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].population[1].count, 0)
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].population[2].count, 0)
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].population[3].count, 0)
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].value.text, "false")
        self.assertEqual(inst.group[0].stratifier[1].code[0].text, "stratifier-ages-10-plus")
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].population[0].count, 0)
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].population[1].count, 0)
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].population[2].count, 0)
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].population[3].count, 0)
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].value.text, "true")
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].population[0].count, 1)
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].population[1].count, 1)
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].population[2].count, 1)
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].population[3].count, 0)
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].value.text, "false")
        self.assertEqual(inst.group[0].stratifier[2].code[0].text, "stratifier-gender")
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].population[0].count, 1)
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].population[1].count, 1)
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].population[2].count, 1)
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].population[3].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].value.text, "male")
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].population[0].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].population[1].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].population[2].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].population[3].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].value.text, "female")
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].population[0].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].population[1].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].population[2].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].population[3].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].value.text, "other")
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].population[0].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].population[1].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].population[2].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].population[3].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].value.text, "unknown")
        self.assertEqual(inst.id, "measurereport-cms146-cat1-example")
        self.assertEqual(inst.identifier[0].value, "measurereport-cms146-cat1-example-2017-03-13")
        self.assertEqual(inst.measure, "Measure/CMS146")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.period.end.date, FHIRDate("2014-03-31").date)
        self.assertEqual(inst.period.end.as_json(), "2014-03-31")
        self.assertEqual(inst.period.start.date, FHIRDate("2014-01-01").date)
        self.assertEqual(inst.period.start.as_json(), "2014-01-01")
        self.assertEqual(inst.status, "complete")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.type, "individual")
    
    def testMeasureReport2(self):
        inst = self.instantiate_from("measurereport-cms146-cat2-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a MeasureReport instance")
        self.implMeasureReport2(inst)
        
        js = inst.as_json()
        self.assertEqual("MeasureReport", js["resourceType"])
        inst2 = measurereport.MeasureReport(js)
        self.implMeasureReport2(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implMeasureReport2(self, inst):
        self.assertEqual(inst.contained[0].id, "reporter")
        self.assertEqual(inst.date.date, FHIRDate("2014-04-01").date)
        self.assertEqual(inst.date.as_json(), "2014-04-01")
        self.assertEqual(inst.group[0].id, "CMS146-group-1")
        self.assertEqual(inst.group[0].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].population[0].count, 500)
        self.assertEqual(inst.group[0].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].population[1].count, 200)
        self.assertEqual(inst.group[0].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].population[2].count, 500)
        self.assertEqual(inst.group[0].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].population[3].count, 100)
        self.assertEqual(inst.group[0].stratifier[0].code[0].text, "stratifier-ages-up-to-9")
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].population[0].count, 250)
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].population[1].count, 100)
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].population[2].count, 250)
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].population[3].count, 50)
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].value.text, "true")
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].population[0].count, 250)
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].population[1].count, 100)
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].population[2].count, 250)
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].population[3].count, 50)
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].value.text, "false")
        self.assertEqual(inst.group[0].stratifier[1].code[0].text, "stratifier-ages-10-plus")
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].population[0].count, 250)
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].population[1].count, 100)
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].population[2].count, 250)
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].population[3].count, 50)
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].value.text, "true")
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].population[0].count, 250)
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].population[1].count, 100)
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].population[2].count, 250)
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].population[3].count, 50)
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].value.text, "false")
        self.assertEqual(inst.group[0].stratifier[2].code[0].text, "stratifier-gender")
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].population[0].count, 250)
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].population[1].count, 100)
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].population[2].count, 250)
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].population[3].count, 50)
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].value.text, "male")
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].population[0].count, 250)
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].population[1].count, 100)
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].population[2].count, 250)
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].population[3].count, 50)
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].value.text, "female")
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].population[0].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].population[1].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].population[2].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].population[3].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].value.text, "other")
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].population[0].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].population[1].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].population[2].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].population[3].code.coding[0].code, "denominator-exclusions")
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].population[3].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].value.text, "unknown")
        self.assertEqual(inst.id, "measurereport-cms146-cat2-example")
        self.assertEqual(inst.identifier[0].value, "measurereport-cms146-cat2-example-2017-03-13")
        self.assertEqual(inst.measure, "Measure/CMS146")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.period.end.date, FHIRDate("2014-03-31").date)
        self.assertEqual(inst.period.end.as_json(), "2014-03-31")
        self.assertEqual(inst.period.start.date, FHIRDate("2014-01-01").date)
        self.assertEqual(inst.period.start.as_json(), "2014-01-01")
        self.assertEqual(inst.status, "complete")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.type, "subject-list")
    
    def testMeasureReport3(self):
        inst = self.instantiate_from("measurereport-cms146-cat3-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a MeasureReport instance")
        self.implMeasureReport3(inst)
        
        js = inst.as_json()
        self.assertEqual("MeasureReport", js["resourceType"])
        inst2 = measurereport.MeasureReport(js)
        self.implMeasureReport3(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implMeasureReport3(self, inst):
        self.assertEqual(inst.contained[0].id, "reporter")
        self.assertEqual(inst.date.date, FHIRDate("2014-04-01").date)
        self.assertEqual(inst.date.as_json(), "2014-04-01")
        self.assertEqual(inst.group[0].id, "CMS146-group-1")
        self.assertEqual(inst.group[0].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].population[0].count, 500)
        self.assertEqual(inst.group[0].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].population[1].count, 200)
        self.assertEqual(inst.group[0].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].population[2].count, 500)
        self.assertEqual(inst.group[0].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].population[3].count, 100)
        self.assertEqual(inst.group[0].stratifier[0].code[0].text, "stratifier-ages-up-to-9")
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].population[0].count, 250)
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].population[1].count, 100)
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].population[2].count, 250)
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].population[3].count, 50)
        self.assertEqual(inst.group[0].stratifier[0].stratum[0].value.text, "true")
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].population[0].count, 250)
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].population[1].count, 100)
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].population[2].count, 250)
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].population[3].count, 50)
        self.assertEqual(inst.group[0].stratifier[0].stratum[1].value.text, "false")
        self.assertEqual(inst.group[0].stratifier[1].code[0].text, "stratifier-ages-10-plus")
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].population[0].count, 250)
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].population[1].count, 100)
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].population[2].count, 250)
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].population[3].count, 50)
        self.assertEqual(inst.group[0].stratifier[1].stratum[0].value.text, "true")
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].population[0].count, 250)
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].population[1].count, 100)
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].population[2].count, 250)
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].population[3].count, 50)
        self.assertEqual(inst.group[0].stratifier[1].stratum[1].value.text, "false")
        self.assertEqual(inst.group[0].stratifier[2].code[0].text, "stratifier-gender")
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].population[0].count, 250)
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].population[1].count, 100)
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].population[2].count, 250)
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].population[3].count, 50)
        self.assertEqual(inst.group[0].stratifier[2].stratum[0].value.text, "male")
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].population[0].count, 250)
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].population[1].count, 100)
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].population[2].count, 250)
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].population[3].count, 50)
        self.assertEqual(inst.group[0].stratifier[2].stratum[1].value.text, "female")
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].population[0].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].population[1].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].population[2].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].population[3].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[2].value.text, "other")
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].population[0].code.coding[0].code, "initial-population")
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].population[0].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].population[1].code.coding[0].code, "numerator")
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].population[1].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].population[2].code.coding[0].code, "denominator")
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].population[2].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].population[3].code.coding[0].code, "denominator-exclusion")
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].population[3].count, 0)
        self.assertEqual(inst.group[0].stratifier[2].stratum[3].value.text, "unknown")
        self.assertEqual(inst.id, "measurereport-cms146-cat3-example")
        self.assertEqual(inst.identifier[0].value, "measurereport-cms146-cat3-example-2017-03-13")
        self.assertEqual(inst.measure, "Measure/CMS146")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.period.end.date, FHIRDate("2014-03-31").date)
        self.assertEqual(inst.period.end.as_json(), "2014-03-31")
        self.assertEqual(inst.period.start.date, FHIRDate("2014-01-01").date)
        self.assertEqual(inst.period.start.as_json(), "2014-01-01")
        self.assertEqual(inst.status, "complete")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.type, "summary")

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