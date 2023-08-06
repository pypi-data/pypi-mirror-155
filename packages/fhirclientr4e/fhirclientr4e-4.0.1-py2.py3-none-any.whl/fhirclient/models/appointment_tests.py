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

from . import appointment

from .fhirdate import FHIRDate
import logging


class AppointmentTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("Appointment", js["resourceType"])
        return appointment.Appointment(js)
    
    def testAppointment1(self):
        inst = self.instantiate_from("appointment-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a Appointment instance")
        self.implAppointment1(inst)
        
        js = inst.as_json()
        self.assertEqual("Appointment", js["resourceType"])
        inst2 = appointment.Appointment(js)
        self.implAppointment1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implAppointment1(self, inst):
        self.assertEqual(inst.appointmentType.coding[0].code, "FOLLOWUP")
        self.assertEqual(inst.appointmentType.coding[0].display, "A follow up visit from a previous appointment")
        self.assertEqual(inst.appointmentType.coding[0].system, "http://terminology.hl7.org/CodeSystem/v2-0276")
        self.assertEqual(inst.comment, "Further expand on the results of the MRI and determine the next actions that may be appropriate.")
        self.assertEqual(inst.created.date, FHIRDate("2013-10-10").date)
        self.assertEqual(inst.created.as_json(), "2013-10-10")
        self.assertEqual(inst.description, "Discussion on the results of your recent MRI")
        self.assertEqual(inst.end.date, FHIRDate("2013-12-10T11:00:00Z").date)
        self.assertEqual(inst.end.as_json(), "2013-12-10T11:00:00Z")
        self.assertEqual(inst.id, "example")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.participant[0].required, "required")
        self.assertEqual(inst.participant[0].status, "accepted")
        self.assertEqual(inst.participant[1].required, "required")
        self.assertEqual(inst.participant[1].status, "accepted")
        self.assertEqual(inst.participant[1].type[0].coding[0].code, "ATND")
        self.assertEqual(inst.participant[1].type[0].coding[0].system, "http://terminology.hl7.org/CodeSystem/v3-ParticipationType")
        self.assertEqual(inst.participant[2].required, "required")
        self.assertEqual(inst.participant[2].status, "accepted")
        self.assertEqual(inst.priority, 5)
        self.assertEqual(inst.serviceCategory[0].coding[0].code, "gp")
        self.assertEqual(inst.serviceCategory[0].coding[0].display, "General Practice")
        self.assertEqual(inst.serviceCategory[0].coding[0].system, "http://example.org/service-category")
        self.assertEqual(inst.serviceType[0].coding[0].code, "52")
        self.assertEqual(inst.serviceType[0].coding[0].display, "General Discussion")
        self.assertEqual(inst.specialty[0].coding[0].code, "394814009")
        self.assertEqual(inst.specialty[0].coding[0].display, "General practice")
        self.assertEqual(inst.specialty[0].coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.start.date, FHIRDate("2013-12-10T09:00:00Z").date)
        self.assertEqual(inst.start.as_json(), "2013-12-10T09:00:00Z")
        self.assertEqual(inst.status, "booked")
        self.assertEqual(inst.text.div, "<div xmlns=\"http://www.w3.org/1999/xhtml\">Brian MRI results discussion</div>")
        self.assertEqual(inst.text.status, "generated")
    
    def testAppointment2(self):
        inst = self.instantiate_from("appointment-example-request.json")
        self.assertIsNotNone(inst, "Must have instantiated a Appointment instance")
        self.implAppointment2(inst)
        
        js = inst.as_json()
        self.assertEqual("Appointment", js["resourceType"])
        inst2 = appointment.Appointment(js)
        self.implAppointment2(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implAppointment2(self, inst):
        self.assertEqual(inst.appointmentType.coding[0].code, "WALKIN")
        self.assertEqual(inst.appointmentType.coding[0].display, "A previously unscheduled walk-in visit")
        self.assertEqual(inst.appointmentType.coding[0].system, "http://terminology.hl7.org/CodeSystem/v2-0276")
        self.assertEqual(inst.comment, "Further expand on the results of the MRI and determine the next actions that may be appropriate.")
        self.assertEqual(inst.created.date, FHIRDate("2015-12-02").date)
        self.assertEqual(inst.created.as_json(), "2015-12-02")
        self.assertEqual(inst.description, "Discussion on the results of your recent MRI")
        self.assertEqual(inst.id, "examplereq")
        self.assertEqual(inst.identifier[0].system, "http://example.org/sampleappointment-identifier")
        self.assertEqual(inst.identifier[0].value, "123")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.minutesDuration, 15)
        self.assertEqual(inst.participant[0].required, "required")
        self.assertEqual(inst.participant[0].status, "needs-action")
        self.assertEqual(inst.participant[1].required, "required")
        self.assertEqual(inst.participant[1].status, "needs-action")
        self.assertEqual(inst.participant[1].type[0].coding[0].code, "ATND")
        self.assertEqual(inst.participant[1].type[0].coding[0].system, "http://terminology.hl7.org/CodeSystem/v3-ParticipationType")
        self.assertEqual(inst.participant[2].required, "required")
        self.assertEqual(inst.participant[2].status, "accepted")
        self.assertEqual(inst.priority, 5)
        self.assertEqual(inst.reasonCode[0].coding[0].code, "413095006")
        self.assertEqual(inst.reasonCode[0].coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.reasonCode[0].text, "Clinical Review")
        self.assertEqual(inst.requestedPeriod[0].end.date, FHIRDate("2016-06-09").date)
        self.assertEqual(inst.requestedPeriod[0].end.as_json(), "2016-06-09")
        self.assertEqual(inst.requestedPeriod[0].start.date, FHIRDate("2016-06-02").date)
        self.assertEqual(inst.requestedPeriod[0].start.as_json(), "2016-06-02")
        self.assertEqual(inst.serviceCategory[0].coding[0].code, "gp")
        self.assertEqual(inst.serviceCategory[0].coding[0].display, "General Practice")
        self.assertEqual(inst.serviceCategory[0].coding[0].system, "http://example.org/service-category")
        self.assertEqual(inst.specialty[0].coding[0].code, "394814009")
        self.assertEqual(inst.specialty[0].coding[0].display, "General practice")
        self.assertEqual(inst.specialty[0].coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.status, "proposed")
        self.assertEqual(inst.text.div, "<div xmlns=\"http://www.w3.org/1999/xhtml\">Brian MRI results discussion</div>")
        self.assertEqual(inst.text.status, "generated")
    
    def testAppointment3(self):
        inst = self.instantiate_from("appointment-example2doctors.json")
        self.assertIsNotNone(inst, "Must have instantiated a Appointment instance")
        self.implAppointment3(inst)
        
        js = inst.as_json()
        self.assertEqual("Appointment", js["resourceType"])
        inst2 = appointment.Appointment(js)
        self.implAppointment3(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implAppointment3(self, inst):
        self.assertEqual(inst.appointmentType.coding[0].code, "WALKIN")
        self.assertEqual(inst.appointmentType.coding[0].display, "A previously unscheduled walk-in visit")
        self.assertEqual(inst.appointmentType.coding[0].system, "http://terminology.hl7.org/CodeSystem/v2-0276")
        self.assertEqual(inst.comment, "Clarify the results of the MRI to ensure context of test was correct")
        self.assertEqual(inst.description, "Discussion about Peter Chalmers MRI results")
        self.assertEqual(inst.end.date, FHIRDate("2013-12-09T11:00:00Z").date)
        self.assertEqual(inst.end.as_json(), "2013-12-09T11:00:00Z")
        self.assertEqual(inst.id, "2docs")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.participant[0].required, "information-only")
        self.assertEqual(inst.participant[0].status, "accepted")
        self.assertEqual(inst.participant[1].required, "required")
        self.assertEqual(inst.participant[1].status, "accepted")
        self.assertEqual(inst.participant[2].required, "required")
        self.assertEqual(inst.participant[2].status, "accepted")
        self.assertEqual(inst.participant[3].required, "information-only")
        self.assertEqual(inst.participant[3].status, "accepted")
        self.assertEqual(inst.priority, 5)
        self.assertEqual(inst.serviceCategory[0].coding[0].code, "gp")
        self.assertEqual(inst.serviceCategory[0].coding[0].display, "General Practice")
        self.assertEqual(inst.serviceCategory[0].coding[0].system, "http://example.org/service-category")
        self.assertEqual(inst.serviceType[0].coding[0].code, "52")
        self.assertEqual(inst.serviceType[0].coding[0].display, "General Discussion")
        self.assertEqual(inst.specialty[0].coding[0].code, "394814009")
        self.assertEqual(inst.specialty[0].coding[0].display, "General practice")
        self.assertEqual(inst.specialty[0].coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.start.date, FHIRDate("2013-12-09T09:00:00Z").date)
        self.assertEqual(inst.start.as_json(), "2013-12-09T09:00:00Z")
        self.assertEqual(inst.status, "booked")
        self.assertEqual(inst.text.div, "<div xmlns=\"http://www.w3.org/1999/xhtml\">Brian MRI results discussion</div>")
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