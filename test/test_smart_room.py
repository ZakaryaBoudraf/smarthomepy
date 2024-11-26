import unittest
import mock.GPIO as GPIO
from unittest.mock import patch, PropertyMock
from unittest.mock import Mock

from mock.adafruit_bmp280 import Adafruit_BMP280_I2C
from src.smart_room import SmartRoom
from mock.senseair_s8 import SenseairS8


class TestSmartRoom(unittest.TestCase):

    @patch.object(GPIO, "input")
    def test_check_room_occupancy_is_true(self, mock_infrared_sensor: Mock):
        system = SmartRoom()
        mock_infrared_sensor.return_value = True
        self.assertTrue(system.check_room_occupancy())

    @patch.object(GPIO, "input")
    def test_check_enough_light_is_true (self, mock_photoresistor: Mock):
        system = SmartRoom()
        mock_photoresistor.return_value = True
        self.assertTrue(system.check_enough_light())

    @patch.object(GPIO, "input")
    @patch.object(GPIO, "input")
    @patch.object(GPIO, "output")
    def test_manage_light_level_turns_on (self, mock_photoresistor: Mock, mock_infrared_sensor: Mock, mock_LED: Mock):
        system = SmartRoom()
        mock_infrared_sensor.return_value = True
        mock_photoresistor.return_value = False
        mock_LED.assert_called_once_with(system.LED_PIN, True)
        self.assertTrue(system.light_on)