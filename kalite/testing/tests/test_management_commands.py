import json 
import os
import platform
import sys
import unittest
import importlib

from django.core.management.base import CommandError
from django.core import serializers

from fle_utils.django_utils import call_command_with_output
from kalite.facility.models import Facility

class ModelCreationCommandTests(unittest.TestCase):
    def test_no_args(self):
        try:
            (out, err, rc) = call_command_with_output('createmodel')
            self.assertFail()
        except CommandError as e:
            self.assertRegexpMatches(str(e), "No args specified")

    def test_no_options(self):
        try:
            (out, err, rc) = call_command_with_output('createmodel', 'some.model')
            self.assertFail()
        except CommandError as e:
            self.assertRegexpMatches(str(e), 
                                     "Please specifiy input data as a json string")

    def test_save_model(self):
        MODEL_NAME = 'kalite.facility.models.Facility'
        (out, err, rc) = call_command_with_output('createmodel',
                                                  MODEL_NAME,
                                                  json_data='{"name" : "kir1"}')
        self.assertEquals(rc, 0)
        module_path, model_name = MODEL_NAME.rsplit(".", 1)
        module = importlib.import_module(module_path)
        model = getattr(module, model_name)

        data = model.objects.get(pk=out.strip())
        self.assertEquals(data.name, "kir1")
        

class ReadModelCommandTests(unittest.TestCase):
    def test_no_args(self):
        try:
            (out, err, rc) = call_command_with_output('readmodel')
            self.assertFail()
        except CommandError as e:
            self.assertRegexpMatches(str(e), "Please specify model class name.")

    def test_no_options(self):
        try:
            (out, err, rc) = call_command_with_output('readmodel', 'some.model')
            self.assertFail()
        except CommandError as e:
            self.assertRegexpMatches(str(e), 
                                     "Please specify --id to fetch model.")

    def test_fetch_model(self):
        MODEL_NAME = 'kalite.facility.models.Facility'
        facility_name = 'kir1'
        # Create a Facility object first that will be fetched.
        facility = Facility(name=facility_name)
        facility.save()

        (out, err, rc) = call_command_with_output('readmodel',
                                                  MODEL_NAME,
                                                  id=facility.id)
        data_map = json.loads(out)
        self.assertEquals(data_map[0]['fields']['name'], facility_name)
