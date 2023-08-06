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

from . import healthcareservice

from .fhirdate import FHIRDate
import logging


class HealthcareServiceTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("HealthcareService", js["resourceType"])
        return healthcareservice.HealthcareService(js)
    
    def testHealthcareService1(self):
        inst = self.instantiate_from("healthcareservice-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a HealthcareService instance")
        self.implHealthcareService1(inst)
        
        js = inst.as_json()
        self.assertEqual("HealthcareService", js["resourceType"])
        inst2 = healthcareservice.HealthcareService(js)
        self.implHealthcareService1(inst2)
        self.evaluate_simplified_json(inst2)
    
    def implHealthcareService1(self, inst):
        self.assertTrue(inst.active)
        self.assertFalse(inst.appointmentRequired)
        self.assertEqual(inst.availabilityExceptions, "Reduced capacity is available during the Christmas period")
        self.assertTrue(inst.availableTime[0].allDay)
        self.assertEqual(inst.availableTime[0].daysOfWeek[0], "wed")
        self.assertEqual(inst.availableTime[1].availableEndTime.date, FHIRDate("05:30:00").date)
        self.assertEqual(inst.availableTime[1].availableEndTime.as_json(), "05:30:00")
        self.assertEqual(inst.availableTime[1].availableStartTime.date, FHIRDate("08:30:00").date)
        self.assertEqual(inst.availableTime[1].availableStartTime.as_json(), "08:30:00")
        self.assertEqual(inst.availableTime[1].daysOfWeek[0], "mon")
        self.assertEqual(inst.availableTime[1].daysOfWeek[1], "tue")
        self.assertEqual(inst.availableTime[1].daysOfWeek[2], "thu")
        self.assertEqual(inst.availableTime[1].daysOfWeek[3], "fri")
        self.assertEqual(inst.availableTime[2].availableEndTime.date, FHIRDate("04:30:00").date)
        self.assertEqual(inst.availableTime[2].availableEndTime.as_json(), "04:30:00")
        self.assertEqual(inst.availableTime[2].availableStartTime.date, FHIRDate("09:30:00").date)
        self.assertEqual(inst.availableTime[2].availableStartTime.as_json(), "09:30:00")
        self.assertEqual(inst.availableTime[2].daysOfWeek[0], "sat")
        self.assertEqual(inst.availableTime[2].daysOfWeek[1], "fri")
        self.assertEqual(inst.category[0].coding[0].code, "8")
        self.assertEqual(inst.category[0].coding[0].display, "Counselling")
        self.assertEqual(inst.category[0].coding[0].system, "http://terminology.hl7.org/CodeSystem/service-category")
        self.assertEqual(inst.category[0].text, "Counselling")
        self.assertEqual(inst.characteristic[0].coding[0].display, "Wheelchair access")
        self.assertEqual(inst.comment, "Providing Specialist psychology services to the greater Den Burg area, many years of experience dealing with PTSD issues")
        self.assertEqual(inst.contained[0].id, "DenBurg")
        self.assertEqual(inst.eligibility[0].code.coding[0].display, "DVA Required")
        self.assertEqual(inst.eligibility[0].comment, "Evidence of application for DVA status may be sufficient for commencing assessment")
        self.assertEqual(inst.id, "example")
        self.assertEqual(inst.identifier[0].system, "http://example.org/shared-ids")
        self.assertEqual(inst.identifier[0].value, "HS-12")
        self.assertEqual(inst.meta.tag[0].code, "HTEST")
        self.assertEqual(inst.meta.tag[0].display, "test health data")
        self.assertEqual(inst.meta.tag[0].system, "http://terminology.hl7.org/CodeSystem/v3-ActReason")
        self.assertEqual(inst.name, "Consulting psychologists and/or psychology services")
        self.assertEqual(inst.notAvailable[0].description, "Christmas/Boxing Day")
        self.assertEqual(inst.notAvailable[0].during.end.date, FHIRDate("2015-12-26").date)
        self.assertEqual(inst.notAvailable[0].during.end.as_json(), "2015-12-26")
        self.assertEqual(inst.notAvailable[0].during.start.date, FHIRDate("2015-12-25").date)
        self.assertEqual(inst.notAvailable[0].during.start.as_json(), "2015-12-25")
        self.assertEqual(inst.notAvailable[1].description, "New Years Day")
        self.assertEqual(inst.notAvailable[1].during.end.date, FHIRDate("2016-01-01").date)
        self.assertEqual(inst.notAvailable[1].during.end.as_json(), "2016-01-01")
        self.assertEqual(inst.notAvailable[1].during.start.date, FHIRDate("2016-01-01").date)
        self.assertEqual(inst.notAvailable[1].during.start.as_json(), "2016-01-01")
        self.assertEqual(inst.program[0].text, "PTSD outreach")
        self.assertEqual(inst.referralMethod[0].coding[0].code, "phone")
        self.assertEqual(inst.referralMethod[0].coding[0].display, "Phone")
        self.assertEqual(inst.referralMethod[1].coding[0].code, "fax")
        self.assertEqual(inst.referralMethod[1].coding[0].display, "Fax")
        self.assertEqual(inst.referralMethod[2].coding[0].code, "elec")
        self.assertEqual(inst.referralMethod[2].coding[0].display, "Secure Messaging")
        self.assertEqual(inst.referralMethod[3].coding[0].code, "semail")
        self.assertEqual(inst.referralMethod[3].coding[0].display, "Secure Email")
        self.assertEqual(inst.serviceProvisionCode[0].coding[0].code, "cost")
        self.assertEqual(inst.serviceProvisionCode[0].coding[0].display, "Fees apply")
        self.assertEqual(inst.serviceProvisionCode[0].coding[0].system, "http://terminology.hl7.org/CodeSystem/service-provision-conditions")
        self.assertEqual(inst.specialty[0].coding[0].code, "47505003")
        self.assertEqual(inst.specialty[0].coding[0].display, "Posttraumatic stress disorder")
        self.assertEqual(inst.specialty[0].coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.telecom[0].system, "phone")
        self.assertEqual(inst.telecom[0].use, "work")
        self.assertEqual(inst.telecom[0].value, "(555) silent")
        self.assertEqual(inst.telecom[1].system, "email")
        self.assertEqual(inst.telecom[1].use, "work")
        self.assertEqual(inst.telecom[1].value, "directaddress@example.com")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.type[0].coding[0].code, "394913002")
        self.assertEqual(inst.type[0].coding[0].display, "Psychotherapy")
        self.assertEqual(inst.type[0].coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.type[1].coding[0].code, "394587001")
        self.assertEqual(inst.type[1].coding[0].display, "Psychiatry")
        self.assertEqual(inst.type[1].coding[0].system, "http://snomed.info/sct")

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