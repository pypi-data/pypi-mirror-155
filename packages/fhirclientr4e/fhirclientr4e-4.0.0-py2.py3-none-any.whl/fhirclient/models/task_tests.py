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

from . import task

from .fhirdate import FHIRDate
import logging


class TaskTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("Task", js["resourceType"])
        return task.Task(js)
    
    def testTask1(self):
        inst = self.instantiate_from("task-example6.json")
        self.assertIsNotNone(inst, "Must have instantiated a Task instance")
        self.implTask1(inst)
        
        js = inst.as_json()
        self.assertEqual("Task", js["resourceType"])
        inst2 = task.Task(js)
        self.implTask1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implTask1(self, inst):
        self.assertEqual(inst.authoredOn.date, FHIRDate("2016-10-31T08:25:05+10:00").date)
        self.assertEqual(inst.authoredOn.as_json(), "2016-10-31T08:25:05+10:00")
        self.assertEqual(inst.businessStatus.text, "test completed and posted")
        self.assertEqual(inst.code.text, "Lipid Panel")
        self.assertEqual(inst.description, "Create order for getting specimen, Set up inhouse testing,  generate order for any sendouts and submit with specimen")
        self.assertEqual(inst.executionPeriod.end.date, FHIRDate("2016-10-31T18:45:05+10:00").date)
        self.assertEqual(inst.executionPeriod.end.as_json(), "2016-10-31T18:45:05+10:00")
        self.assertEqual(inst.executionPeriod.start.date, FHIRDate("2016-10-31T08:25:05+10:00").date)
        self.assertEqual(inst.executionPeriod.start.as_json(), "2016-10-31T08:25:05+10:00")
        self.assertEqual(inst.groupIdentifier.system, "http:/goodhealth.org/accession/identifiers")
        self.assertEqual(inst.groupIdentifier.use, "official")
        self.assertEqual(inst.groupIdentifier.value, "G20170201-001")
        self.assertEqual(inst.id, "example6")
        self.assertEqual(inst.identifier[0].system, "http:/goodhealth.org/identifiers")
        self.assertEqual(inst.identifier[0].use, "official")
        self.assertEqual(inst.identifier[0].value, "20170201-001")
        self.assertEqual(inst.intent, "order")
        self.assertEqual(inst.lastModified.date, FHIRDate("2016-10-31T18:45:05+10:00").date)
        self.assertEqual(inst.lastModified.as_json(), "2016-10-31T18:45:05+10:00")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.output[0].type.text, "DiagnosticReport generated")
        self.assertEqual(inst.output[1].type.text, "collected specimen")
        self.assertEqual(inst.performerType[0].coding[0].code, "performer")
        self.assertEqual(inst.performerType[0].coding[0].display, "Performer")
        self.assertEqual(inst.performerType[0].coding[0].system, "http://terminology.hl7.org/CodeSystem/task-performer-type")
        self.assertEqual(inst.performerType[0].text, "Performer")
        self.assertEqual(inst.priority, "routine")
        self.assertEqual(inst.reasonCode.text, "The Task.reason should only be included if there is no Task.focus or if it differs from the reason indicated on the focus")
        self.assertEqual(inst.restriction.period.end.date, FHIRDate("2016-11-02T09:45:05+10:00").date)
        self.assertEqual(inst.restriction.period.end.as_json(), "2016-11-02T09:45:05+10:00")
        self.assertEqual(inst.restriction.repetitions, 1)
        self.assertEqual(inst.status, "completed")
        self.assertEqual(inst.text.status, "generated")
    
    def testTask2(self):
        inst = self.instantiate_from("task-example-fm-poll.json")
        self.assertIsNotNone(inst, "Must have instantiated a Task instance")
        self.implTask2(inst)
        
        js = inst.as_json()
        self.assertEqual("Task", js["resourceType"])
        inst2 = task.Task(js)
        self.implTask2(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implTask2(self, inst):
        self.assertEqual(inst.authoredOn.date, FHIRDate("2018-10-12T08:25:05+10:00").date)
        self.assertEqual(inst.authoredOn.as_json(), "2018-10-12T08:25:05+10:00")
        self.assertEqual(inst.code.coding[0].code, "poll")
        self.assertEqual(inst.code.coding[0].system, "http://terminology.hl7.org/CodeSystem/financialtaskcode")
        self.assertEqual(inst.id, "fm-example2")
        self.assertEqual(inst.identifier[0].system, "http:/happyvalley.com/task")
        self.assertEqual(inst.identifier[0].use, "official")
        self.assertEqual(inst.identifier[0].value, "20181012-005")
        self.assertEqual(inst.input[0].type.coding[0].code, "include")
        self.assertEqual(inst.input[0].type.coding[0].system, "http://terminology.hl7.org/CodeSystem/financialtaskinputtype")
        self.assertEqual(inst.input[0].valueCode, "ClaimResponse")
        self.assertEqual(inst.input[1].type.coding[0].code, "period")
        self.assertEqual(inst.input[1].type.coding[0].system, "http://terminology.hl7.org/CodeSystem/financialtaskinputtype")
        self.assertEqual(inst.input[1].valuePeriod.end.date, FHIRDate("2018-10-12").date)
        self.assertEqual(inst.input[1].valuePeriod.end.as_json(), "2018-10-12")
        self.assertEqual(inst.input[1].valuePeriod.start.date, FHIRDate("2018-10-01").date)
        self.assertEqual(inst.input[1].valuePeriod.start.as_json(), "2018-10-01")
        self.assertEqual(inst.intent, "order")
        self.assertEqual(inst.lastModified.date, FHIRDate("2018-10-12T08:25:05+10:00").date)
        self.assertEqual(inst.lastModified.as_json(), "2018-10-12T08:25:05+10:00")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.priority, "stat")
        self.assertEqual(inst.status, "requested")
        self.assertEqual(inst.text.status, "generated")
    
    def testTask3(self):
        inst = self.instantiate_from("task-example1.json")
        self.assertIsNotNone(inst, "Must have instantiated a Task instance")
        self.implTask3(inst)
        
        js = inst.as_json()
        self.assertEqual("Task", js["resourceType"])
        inst2 = task.Task(js)
        self.implTask3(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implTask3(self, inst):
        self.assertEqual(inst.authoredOn.date, FHIRDate("2016-10-31T08:25:05+10:00").date)
        self.assertEqual(inst.authoredOn.as_json(), "2016-10-31T08:25:05+10:00")
        self.assertEqual(inst.businessStatus.text, "waiting for specimen")
        self.assertEqual(inst.code.text, "Lipid Panel")
        self.assertEqual(inst.contained[0].id, "signature")
        self.assertEqual(inst.description, "Create order for getting specimen, Set up inhouse testing,  generate order for any sendouts and submit with specimen")
        self.assertEqual(inst.executionPeriod.start.date, FHIRDate("2016-10-31T08:25:05+10:00").date)
        self.assertEqual(inst.executionPeriod.start.as_json(), "2016-10-31T08:25:05+10:00")
        self.assertEqual(inst.groupIdentifier.system, "http:/goodhealth.org/accession/identifiers")
        self.assertEqual(inst.groupIdentifier.use, "official")
        self.assertEqual(inst.groupIdentifier.value, "G20170201-001")
        self.assertEqual(inst.id, "example1")
        self.assertEqual(inst.identifier[0].system, "http:/goodhealth.org/identifiers")
        self.assertEqual(inst.identifier[0].use, "official")
        self.assertEqual(inst.identifier[0].value, "20170201-001")
        self.assertEqual(inst.intent, "order")
        self.assertEqual(inst.lastModified.date, FHIRDate("2016-10-31T09:45:05+10:00").date)
        self.assertEqual(inst.lastModified.as_json(), "2016-10-31T09:45:05+10:00")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.performerType[0].coding[0].code, "performer")
        self.assertEqual(inst.performerType[0].coding[0].display, "Performer")
        self.assertEqual(inst.performerType[0].coding[0].system, "http://terminology.hl7.org/CodeSystem/task-performer-type")
        self.assertEqual(inst.performerType[0].text, "Performer")
        self.assertEqual(inst.priority, "routine")
        self.assertEqual(inst.reasonCode.text, "The Task.reason should only be included if there is no Task.focus or if it differs from the reason indicated on the focus")
        self.assertEqual(inst.restriction.period.end.date, FHIRDate("2016-11-02T09:45:05+10:00").date)
        self.assertEqual(inst.restriction.period.end.as_json(), "2016-11-02T09:45:05+10:00")
        self.assertEqual(inst.restriction.repetitions, 1)
        self.assertEqual(inst.status, "in-progress")
        self.assertEqual(inst.text.status, "generated")
    
    def testTask4(self):
        inst = self.instantiate_from("task-example-fm-reprocess.json")
        self.assertIsNotNone(inst, "Must have instantiated a Task instance")
        self.implTask4(inst)
        
        js = inst.as_json()
        self.assertEqual("Task", js["resourceType"])
        inst2 = task.Task(js)
        self.implTask4(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implTask4(self, inst):
        self.assertEqual(inst.authoredOn.date, FHIRDate("2018-10-04T08:25:05+10:00").date)
        self.assertEqual(inst.authoredOn.as_json(), "2018-10-04T08:25:05+10:00")
        self.assertEqual(inst.code.coding[0].code, "reprocess")
        self.assertEqual(inst.code.coding[0].system, "http://terminology.hl7.org/CodeSystem/financialtaskcode")
        self.assertEqual(inst.id, "fm-example4")
        self.assertEqual(inst.identifier[0].system, "http:/happyvalley.com/task")
        self.assertEqual(inst.identifier[0].use, "official")
        self.assertEqual(inst.identifier[0].value, "20181012-006")
        self.assertEqual(inst.input[0].type.coding[0].code, "origresponse")
        self.assertEqual(inst.input[0].type.coding[0].system, "http://terminology.hl7.org/CodeSystem/financialtaskinputtype")
        self.assertEqual(inst.input[1].type.coding[0].code, "reference")
        self.assertEqual(inst.input[1].type.coding[0].system, "http://terminology.hl7.org/CodeSystem/financialtaskinputtype")
        self.assertEqual(inst.input[1].valueString, "BR12345")
        self.assertEqual(inst.input[2].type.coding[0].code, "item")
        self.assertEqual(inst.input[2].type.coding[0].system, "http://terminology.hl7.org/CodeSystem/financialtaskinputtype")
        self.assertEqual(inst.input[2].valuePositiveInt, 2)
        self.assertEqual(inst.input[3].type.coding[0].code, "item")
        self.assertEqual(inst.input[3].type.coding[0].system, "http://terminology.hl7.org/CodeSystem/financialtaskinputtype")
        self.assertEqual(inst.input[3].valuePositiveInt, 3)
        self.assertEqual(inst.intent, "order")
        self.assertEqual(inst.lastModified.date, FHIRDate("2018-10-04T08:25:05+10:00").date)
        self.assertEqual(inst.lastModified.as_json(), "2018-10-04T08:25:05+10:00")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.priority, "stat")
        self.assertEqual(inst.status, "requested")
        self.assertEqual(inst.text.status, "generated")
    
    def testTask5(self):
        inst = self.instantiate_from("task-example3.json")
        self.assertIsNotNone(inst, "Must have instantiated a Task instance")
        self.implTask5(inst)
        
        js = inst.as_json()
        self.assertEqual("Task", js["resourceType"])
        inst2 = task.Task(js)
        self.implTask5(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implTask5(self, inst):
        self.assertEqual(inst.authoredOn.date, FHIRDate("2016-03-10T22:39:32-04:00").date)
        self.assertEqual(inst.authoredOn.as_json(), "2016-03-10T22:39:32-04:00")
        self.assertEqual(inst.code.text, "Refill Request")
        self.assertEqual(inst.id, "example3")
        self.assertEqual(inst.intent, "order")
        self.assertEqual(inst.lastModified.date, FHIRDate("2016-03-10T22:39:32-04:00").date)
        self.assertEqual(inst.lastModified.as_json(), "2016-03-10T22:39:32-04:00")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.status, "draft")
        self.assertEqual(inst.text.status, "generated")
    
    def testTask6(self):
        inst = self.instantiate_from("task-example-fm-status-resp.json")
        self.assertIsNotNone(inst, "Must have instantiated a Task instance")
        self.implTask6(inst)
        
        js = inst.as_json()
        self.assertEqual("Task", js["resourceType"])
        inst2 = task.Task(js)
        self.implTask6(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implTask6(self, inst):
        self.assertEqual(inst.authoredOn.date, FHIRDate("2018-10-04T08:25:05+10:00").date)
        self.assertEqual(inst.authoredOn.as_json(), "2018-10-04T08:25:05+10:00")
        self.assertEqual(inst.code.coding[0].code, "status")
        self.assertEqual(inst.code.coding[0].system, "http://terminology.hl7.org/CodeSystem/financialtaskcode")
        self.assertEqual(inst.id, "fm-example6")
        self.assertEqual(inst.identifier[0].system, "http:/happyvalley.com/task")
        self.assertEqual(inst.identifier[0].use, "official")
        self.assertEqual(inst.identifier[0].value, "20181012-001")
        self.assertEqual(inst.identifier[1].system, "http://nationalinsurers.com/identifiers/12345")
        self.assertEqual(inst.identifier[1].use, "official")
        self.assertEqual(inst.identifier[1].value, "123GB5674")
        self.assertEqual(inst.intent, "order")
        self.assertEqual(inst.lastModified.date, FHIRDate("2018-10-04T08:25:05+10:00").date)
        self.assertEqual(inst.lastModified.as_json(), "2018-10-04T08:25:05+10:00")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.output[0].type.coding[0].code, "status")
        self.assertEqual(inst.output[0].type.coding[0].system, "http://hl7.org/financial-taskoutputtype")
        self.assertEqual(inst.output[0].valueCode, "complete")
        self.assertEqual(inst.priority, "stat")
        self.assertEqual(inst.status, "completed")
        self.assertEqual(inst.text.status, "generated")
    
    def testTask7(self):
        inst = self.instantiate_from("task-example2.json")
        self.assertIsNotNone(inst, "Must have instantiated a Task instance")
        self.implTask7(inst)
        
        js = inst.as_json()
        self.assertEqual("Task", js["resourceType"])
        inst2 = task.Task(js)
        self.implTask7(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implTask7(self, inst):
        self.assertEqual(inst.authoredOn.date, FHIRDate("2016-10-31T08:45:05+10:00").date)
        self.assertEqual(inst.authoredOn.as_json(), "2016-10-31T08:45:05+10:00")
        self.assertEqual(inst.businessStatus.text, "waiting for patient")
        self.assertEqual(inst.code.text, "Specimen Collection")
        self.assertEqual(inst.executionPeriod.start.date, FHIRDate("2016-10-31T08:45:05+10:00").date)
        self.assertEqual(inst.executionPeriod.start.as_json(), "2016-10-31T08:45:05+10:00")
        self.assertEqual(inst.groupIdentifier.system, "http:/goodhealth.org/accession/identifiers")
        self.assertEqual(inst.groupIdentifier.use, "official")
        self.assertEqual(inst.groupIdentifier.value, "G20170201-001")
        self.assertEqual(inst.id, "example2")
        self.assertEqual(inst.identifier[0].system, "http:/goodhealth.org/identifiers")
        self.assertEqual(inst.identifier[0].use, "official")
        self.assertEqual(inst.identifier[0].value, "20170201-002")
        self.assertEqual(inst.intent, "filler-order")
        self.assertEqual(inst.lastModified.date, FHIRDate("2016-10-31T09:45:05+10:00").date)
        self.assertEqual(inst.lastModified.as_json(), "2016-10-31T09:45:05+10:00")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.performerType[0].coding[0].code, "performer")
        self.assertEqual(inst.performerType[0].coding[0].display, "Performer")
        self.assertEqual(inst.performerType[0].coding[0].system, "http://terminology.hl7.org/CodeSystem/task-performer-type")
        self.assertEqual(inst.performerType[0].text, "Performer")
        self.assertEqual(inst.priority, "routine")
        self.assertEqual(inst.restriction.period.end.date, FHIRDate("2016-11-01T09:45:05+10:00").date)
        self.assertEqual(inst.restriction.period.end.as_json(), "2016-11-01T09:45:05+10:00")
        self.assertEqual(inst.restriction.repetitions, 1)
        self.assertEqual(inst.status, "accepted")
        self.assertEqual(inst.text.status, "generated")
    
    def testTask8(self):
        inst = self.instantiate_from("task-example-fm-release.json")
        self.assertIsNotNone(inst, "Must have instantiated a Task instance")
        self.implTask8(inst)
        
        js = inst.as_json()
        self.assertEqual("Task", js["resourceType"])
        inst2 = task.Task(js)
        self.implTask8(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implTask8(self, inst):
        self.assertEqual(inst.authoredOn.date, FHIRDate("2018-10-04T08:25:05+10:00").date)
        self.assertEqual(inst.authoredOn.as_json(), "2018-10-04T08:25:05+10:00")
        self.assertEqual(inst.code.coding[0].code, "release")
        self.assertEqual(inst.code.coding[0].system, "http://terminology.hl7.org/CodeSystem/financialtaskcode")
        self.assertEqual(inst.id, "fm-example3")
        self.assertEqual(inst.identifier[0].system, "http:/happyvalley.com/task")
        self.assertEqual(inst.identifier[0].use, "official")
        self.assertEqual(inst.identifier[0].value, "20181012-001")
        self.assertEqual(inst.input[0].type.coding[0].code, "origresponse")
        self.assertEqual(inst.input[0].type.coding[0].system, "http://hl7.org/financial-taskinputtype")
        self.assertEqual(inst.intent, "order")
        self.assertEqual(inst.lastModified.date, FHIRDate("2018-10-04T08:25:05+10:00").date)
        self.assertEqual(inst.lastModified.as_json(), "2018-10-04T08:25:05+10:00")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.priority, "stat")
        self.assertEqual(inst.status, "requested")
        self.assertEqual(inst.text.status, "generated")
    
    def testTask9(self):
        inst = self.instantiate_from("task-example-fm-cancel.json")
        self.assertIsNotNone(inst, "Must have instantiated a Task instance")
        self.implTask9(inst)
        
        js = inst.as_json()
        self.assertEqual("Task", js["resourceType"])
        inst2 = task.Task(js)
        self.implTask9(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implTask9(self, inst):
        self.assertEqual(inst.authoredOn.date, FHIRDate("2018-10-04T08:25:05+10:00").date)
        self.assertEqual(inst.authoredOn.as_json(), "2018-10-04T08:25:05+10:00")
        self.assertEqual(inst.code.coding[0].code, "cancel")
        self.assertEqual(inst.code.coding[0].system, "http://terminology.hl7.org/CodeSystem/financialtaskcode")
        self.assertEqual(inst.id, "fm-example1")
        self.assertEqual(inst.identifier[0].system, "http:/happyvalley.com/task")
        self.assertEqual(inst.identifier[0].use, "official")
        self.assertEqual(inst.identifier[0].value, "20181012-001")
        self.assertEqual(inst.intent, "order")
        self.assertEqual(inst.lastModified.date, FHIRDate("2018-10-04T08:25:05+10:00").date)
        self.assertEqual(inst.lastModified.as_json(), "2018-10-04T08:25:05+10:00")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.priority, "stat")
        self.assertEqual(inst.status, "requested")
        self.assertEqual(inst.text.status, "generated")
    
    def testTask10(self):
        inst = self.instantiate_from("task-example5.json")
        self.assertIsNotNone(inst, "Must have instantiated a Task instance")
        self.implTask10(inst)
        
        js = inst.as_json()
        self.assertEqual("Task", js["resourceType"])
        inst2 = task.Task(js)
        self.implTask10(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implTask10(self, inst):
        self.assertEqual(inst.authoredOn.date, FHIRDate("2016-10-31T08:25:05+10:00").date)
        self.assertEqual(inst.authoredOn.as_json(), "2016-10-31T08:25:05+10:00")
        self.assertEqual(inst.businessStatus.text, "specimen received, test in progress")
        self.assertEqual(inst.code.text, "Lipid Panel")
        self.assertEqual(inst.description, "Create order for getting specimen, Set up inhouse testing,  generate order for any sendouts and submit with specimen")
        self.assertEqual(inst.executionPeriod.start.date, FHIRDate("2016-10-31T08:25:05+10:00").date)
        self.assertEqual(inst.executionPeriod.start.as_json(), "2016-10-31T08:25:05+10:00")
        self.assertEqual(inst.groupIdentifier.system, "http:/goodhealth.org/accession/identifiers")
        self.assertEqual(inst.groupIdentifier.use, "official")
        self.assertEqual(inst.groupIdentifier.value, "G20170201-001")
        self.assertEqual(inst.id, "example5")
        self.assertEqual(inst.identifier[0].system, "http:/goodhealth.org/identifiers")
        self.assertEqual(inst.identifier[0].use, "official")
        self.assertEqual(inst.identifier[0].value, "20170201-001")
        self.assertEqual(inst.intent, "order")
        self.assertEqual(inst.lastModified.date, FHIRDate("2016-10-31T16:45:05+10:00").date)
        self.assertEqual(inst.lastModified.as_json(), "2016-10-31T16:45:05+10:00")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.output[0].type.text, "collected specimen")
        self.assertEqual(inst.performerType[0].coding[0].code, "performer")
        self.assertEqual(inst.performerType[0].coding[0].display, "Performer")
        self.assertEqual(inst.performerType[0].coding[0].system, "http://terminology.hl7.org/CodeSystem/task-performer-type")
        self.assertEqual(inst.performerType[0].text, "Performer")
        self.assertEqual(inst.priority, "routine")
        self.assertEqual(inst.reasonCode.text, "The Task.reason should only be included if there is no Task.focus or if it differs from the reason indicated on the focus")
        self.assertEqual(inst.restriction.period.end.date, FHIRDate("2016-11-02T09:45:05+10:00").date)
        self.assertEqual(inst.restriction.period.end.as_json(), "2016-11-02T09:45:05+10:00")
        self.assertEqual(inst.restriction.repetitions, 1)
        self.assertEqual(inst.status, "in-progress")
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