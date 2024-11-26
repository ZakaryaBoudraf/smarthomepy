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

    # @patch.object(GPIO, "output")
    # @patch.object(GPIO, "input")
    # @patch.object(GPIO, "input")
    # def test_manage_light_level_turns_on (self, mock_infrared_sensor: Mock, mock_photoresistor: Mock, mock_light: Mock):
    #     mock_infrared_sensor.return_value = True
    #     mock_photoresistor.return_value = False
    #     system = SmartRoom()
    #     system.manage_light_level()
    #     mock_light.assert_called_with(True)
    #     self.assertTrue(system.light_on)

    # @patch.object(GPIO, "output")
    # @patch.object(SmartRoom, "check_occupancy")
    # @patch.object(SmartRoom, "check_enough_light")
    # def test_manage_light_level_turns_on(self, mock_enough_light: Mock, mock_occupancy: Mock, mock_light: Mock):
    #     mock_enough_light.return_value = False
    #     mock_occupancy.return_value = True
    #     system = SmartRoom()
    #     system.manage_light_level()
    #     mock_light.assert_called_with(system.LED_PIN, True)
    #     self.assertTrue(system.light_on)
    @patch.object(GPIO, "output")
    @patch.object(Adafruit_BMP280_I2C, "temperature", new_callable=PropertyMock)
    def test_manage_window_open_if_temp_inside_is_lower_than_outside (self, mock_temp_sensors: Mock, mock_window_servo: Mock):
        mock_temp_sensors.side_effect = [18,23]
        system = SmartRoom()
        system.manage_window()
        mock_window_servo.assert_called_with(12)
        self.assertTrue(system.window_open())

    @patch.object(GPIO, "output")
    @patch.object(Adafruit_BMP280_I2C, "temperature", new_callable=PropertyMock)
    def test_manage_window_close_if_temp_inside_is_higher_than_outside (self, mock_temp_sensors: Mock, mock_window_servo: Mock):
        mock_temp_sensors.side_effect = [25,18]
        system = SmartRoom()
        system.manage_window()
        mock_window_servo.assert_called_with(0)
        self.assertFalse(system.window_open())

    @patch.object(GPIO, "output")
    @patch.object(SenseairS8, "co2")
    def test_monitor_air_quality_co2_high_fan_turns_on (self, mock_co2_sensor: Mock, mock_fan: Mock):
        mock_co2_sensor.return_value = 800
        system = SmartRoom()
        system.monitor_air_quality()
        mock_fan.assert_called_with(system.FAN_PIN, True)
        self.assertTrue(system.fan_on)