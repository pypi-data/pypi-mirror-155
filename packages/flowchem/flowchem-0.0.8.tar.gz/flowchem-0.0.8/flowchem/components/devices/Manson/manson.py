"""
Original code from Manson website with edits.
No license originally specified.
"""

import re
import warnings
from typing import List, Literal, Tuple, Union

import aioserial
from loguru import logger

from flowchem.components.properties import ActiveComponent
from flowchem.exceptions import DeviceError, InvalidConfiguration
from flowchem.units import flowchem_ureg


class MansonPowerSupply(ActiveComponent):
    """Control module for Manson Power Supply (e.g. used to power LEDs in the photo-rector or as potentiostat)"""

    MODEL_ALT_RANGE = ["HCS-3102", "HCS-3014", "HCS-3204", "HCS-3202"]

    def __init__(self, aio: aioserial.AioSerial, name=None):
        """
        Control class for Manson Power Supply.
        """

        super().__init__(name)
        self._serial = aio

    @classmethod
    def from_config(cls, port, name=None, **serial_kwargs):
        """
        Create instance from config dict. Used by server to initialize obj from config.

        Only required parameter is 'port'.
        """
        try:
            serial_object = aioserial.AioSerial(port, **serial_kwargs)
        except aioserial.SerialException as error:
            raise InvalidConfiguration(
                f"Cannot connect to the MansonPowerSupply on the port <{port}>"
            ) from error

        return cls(serial_object, name)

    async def initialize(self):
        """Ensure the connection w/ device is working."""
        model_info = await self.get_info()
        if model_info == "":
            raise DeviceError("Communication with device failed!")
        if await self.get_info() not in self.MODEL_ALT_RANGE:
            raise InvalidConfiguration(
                f"Device is not supported! [Supported models: {self.MODEL_ALT_RANGE}]"
            )

    @staticmethod
    def _format_voltage(voltage_value: str) -> str:
        """Format a voltage in the format the power supply understands"""

        voltage = flowchem_ureg(voltage_value)
        # Zero fill by left pad with zeros, up to three digits
        return str(voltage.m_as("V") * 10).zfill(3)

    async def _format_amperage(self, amperage_value: str) -> str:
        """Format a current intensity in the format the power supply understands"""

        current = flowchem_ureg(amperage_value)
        multiplier = 100 if await self.get_info() in self.MODEL_ALT_RANGE else 10
        return str(current.m_as("A") * multiplier).zfill(3)

    async def _send_command(
        self,
        command: str,
    ) -> str:
        """Internal function to send command and read reply."""

        # Flush buffer
        self._serial.reset_input_buffer()

        # Write command
        await self._serial.write_async(f"{command}\r".encode("ascii"))

        # Read reply
        reply_string = []
        for line in await self._serial.readlines_async():
            reply_string.append(line.decode("ascii").strip())
            logger.debug(f"Received {repr(line)}!")

        return "\n".join(reply_string)

    async def get_info(self) -> str:
        """Returns the model name of the connected device"""
        response = await self._send_command("GMOD")

        pattern = re.compile(r".*\d{4}\s")
        match = pattern.match(response)

        if match:
            if response[0:4] == "HCS-":
                return match.group().rstrip()
            return "HCS-" + match.group().rstrip()
        return ""

    async def output_on(self) -> bool:
        """Turn on electricity on output"""
        response = await self._send_command("SOUT0")
        return response == "OK"

    async def output_off(self) -> bool:
        """Turn off electricity on output"""
        response = await self._send_command("SOUT1")
        return response == "OK"

    async def get_output_read(
        self,
    ) -> Tuple[str, str, Union[Literal["CC"], Literal["CV"], Literal["NN"]]]:
        """Returns actual values of voltage, current and mode"""
        response = await self._send_command("GETD")

        try:
            volt = float(response[0:4]) / 100 * flowchem_ureg.volt
            curr = float(response[4:8]) / 100 * flowchem_ureg.ampere
        except ValueError:
            warnings.warn("Invalid values from device!")
            return "0 V", "0 A", "NN"

        if response[8:9] == "0":
            return str(volt), str(curr), "CV"
        if response[8:9] == "1":
            return str(volt), str(curr), "CC"
        return str(volt), str(curr), "NN"

    async def get_output_voltage(self) -> str:
        """Returns output voltage in Volt"""
        voltage, _, _ = await self.get_output_read()
        return voltage

    async def get_output_current(self) -> str:
        """Returns output current in Ampere"""
        _, current, _ = await self.get_output_read()
        return current

    async def get_output_mode(self) -> Literal["CC", "CV", "NN"]:
        """Returns output mode: either current control (CC) or voltage control (CV)"""
        _, _, mode = await self.get_output_read()
        return mode

    async def get_output_power(self) -> str:
        """Returns output power in watts"""
        voltage, intensity, _ = await self.get_output_read()
        power = flowchem_ureg(voltage) * flowchem_ureg(intensity)
        return str(power.to("W"))

    async def get_max(self) -> Tuple[str, str]:
        """Returns maximum voltage and current, as tuple, or False."""
        response = await self._send_command("GMAX")

        max_v_raw = int(response[0:3]) * flowchem_ureg.volt
        max_c_raw = int(response[3:6]) * flowchem_ureg.ampere

        max_v = max_v_raw / 10
        # Some models report current as 0.1 A others at 0.01 A
        model = await self.get_info()
        divider = 100 if model in self.MODEL_ALT_RANGE else 10
        return str(max_v), str(max_c_raw / divider)

    async def get_setting(self) -> Tuple[str, str]:
        """Returns current setting as tuple (voltage, current)."""
        response = await self._send_command("GETS")

        # RegEx to only keep numbers
        response = re.sub(r"\D", "", response)
        v_setting = float(response[0:3]) / 10 * flowchem_ureg.volt
        c_setting = float(response[3:6]) * flowchem_ureg.ampere

        if await self.get_info() in self.MODEL_ALT_RANGE:
            c_setting /= 10

        return str(v_setting), str(c_setting / 10)

    async def set_voltage(self, voltage: str) -> bool:
        """Set target voltage"""

        cmd = "VOLT" + self._format_voltage(voltage)
        response = await self._send_command(cmd)
        return response == "OK"

    async def set_current(self, current: str) -> bool:
        """Set target current"""

        cmd = "CURR" + await self._format_amperage(current)
        response = await self._send_command(cmd)
        return response == "OK"

    async def set_all_preset(self, preset: List[Tuple[str, str]]) -> bool:
        """Set all 3 preset memory position with voltage/current values"""
        command = "PROM"

        for set_values in preset:
            voltage, current = set_values
            voltage_string = self._format_voltage(voltage)
            current_string = await self._format_amperage(current)
            command += voltage_string + current_string

        # Set new values (no reply from device on this command)
        await self._send_command(command)
        return True

    async def set_preset(self, index: int, voltage: str, current: str) -> bool:
        """Set preset position index with the provided values of voltage and current"""
        preset = await self.get_all_preset()
        try:
            volt_str = self._format_voltage(voltage)
            curr_str = await self._format_amperage(current)
            preset[index] = (volt_str, curr_str)
        except KeyError:
            warnings.warn(f"Preset {index} not found! Command ignored")
            return False
        return await self.set_all_preset(preset)

    async def get_all_preset(self) -> List[Tuple[str, str]]:
        """Get voltage and current for all 3 memory preset position"""
        response = await self._send_command("GETM")
        response_lines = response.split("\r")

        voltage = []
        current = []

        for preset in response_lines[0:3]:
            # Drop all but numbers
            preset = re.sub(r"\D", "", preset)
            try:
                # Three digits for voltage and three digits for current
                voltage.append(float(preset[0:3]))
                current.append(float(preset[3:6]))
            except (KeyError, ValueError):
                warnings.warn("Error reading presets!")

        # Transform current in Ampere and voltage in Volt
        current = [x / 10 for x in current]
        voltage = [x / 10 for x in voltage]

        # Usual issue with some models having higher precision for voltage
        if await self.get_info() in self.MODEL_ALT_RANGE:
            voltage = [x / 10 for x in voltage]

        voltage_str = [str(flowchem_ureg.Quantity(x, "V")) for x in voltage]
        current_str = [str(flowchem_ureg.Quantity(x, "A")) for x in current]

        return list(zip(voltage_str, current_str))

    async def get_preset(self, index) -> Tuple[str, str]:
        """Get voltage and current for given preset position [0..2]"""
        all_preset = await self.get_all_preset()
        try:
            return all_preset[index]
        except KeyError:
            warnings.warn(f"Preset {index} not found! Command ignored")
            return "", ""

    async def run_preset(self, index: int) -> bool:
        """Set Voltage and Current using values saved in one of the three memory locations: 0, 1 or 2"""
        if not 0 <= int(index) < 3:
            warnings.warn(f"Invalid preset value: <{index}>!")
            return False
        cmd = "RUNM" + str(int(index))
        response = await self._send_command(cmd)
        return response == "OK"

    async def remove_protection(self) -> bool:
        """I guess it removes overvoltage protection?"""
        response = await self._send_command("SPRO0")
        return bool(response)

    async def add_protection(self) -> bool:
        """I guess it adds overvoltage protection?"""
        response = await self._send_command("SPRO1")
        return bool(response)

    async def set_voltage_and_current(self, voltage: str, current: str):
        """Convenience method to set both voltage and current"""
        await self.set_voltage(voltage)
        await self.set_current(current)

    def get_router(self):
        """Creates an APIRouter for this MansonPowerSupply instance."""
        from fastapi import APIRouter

        router = APIRouter()
        router.add_api_route("/output/on", self.output_on, methods=["GET"])
        router.add_api_route("/output/off", self.output_off, methods=["GET"])
        router.add_api_route("/output/power", self.get_output_power, methods=["GET"])
        router.add_api_route("/output/mode", self.get_output_mode, methods=["GET"])
        router.add_api_route("/voltage/read", self.get_output_voltage, methods=["GET"])
        router.add_api_route("/voltage/max", self.set_voltage, methods=["PUT"])
        router.add_api_route("/current/read", self.get_output_current, methods=["GET"])
        router.add_api_route("/current/max", self.set_current, methods=["PUT"])
        router.add_api_route("/protection/add", self.add_protection, methods=["GET"])
        router.add_api_route(
            "/protection/remove", self.remove_protection, methods=["GET"]
        )

        return router
