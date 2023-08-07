"""
Knauer pump
Run with python -m pytest ./tests -m KPump and updates pump address below
"""
import asyncio
import math
import sys

import pint
import pytest

from flowchem import AzuraCompactPump
from flowchem.components.devices.Knauer.AzuraCompactPump import AzuraPumpHeads

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# noinspection PyUnusedLocal
@pytest.fixture(scope="session")
def event_loop(request):
    """

    Args:
        request:
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def pump():
    """Change to match your hardware ;)"""
    pump = AzuraCompactPump(ip_address="192.168.1.126")
    await pump.initialize()
    return pump


@pytest.mark.KPump
@pytest.mark.asyncio
async def test_pumphead(pump: AzuraCompactPump):
    assert await pump.get_headtype() in AzuraPumpHeads
    await pump.set_headtype(AzuraPumpHeads.FLOWRATE_TEN_ML)
    assert await pump.get_headtype() == AzuraPumpHeads.FLOWRATE_TEN_ML
    await pump.set_headtype(AzuraPumpHeads.FLOWRATE_FIFTY_ML)
    assert await pump.get_headtype() == AzuraPumpHeads.FLOWRATE_FIFTY_ML


@pytest.mark.KPump
@pytest.mark.asyncio
async def test_headtype(pump: AzuraCompactPump):
    assert await pump.get_headtype() in AzuraPumpHeads


@pytest.mark.KPump
@pytest.mark.asyncio
async def test_flow_rate(pump: AzuraCompactPump):
    await pump.set_flow("1.25 ml/min")
    await pump.start_flow()
    # FIXME
    assert pint.Quantity(await pump.get_flow()).magnitude == 1.25
    await pump.set_flow(f"{math.pi} ml/min")
    assert math.isclose(
        pint.Quantity(await pump.get_flow()).magnitude, math.pi, abs_tol=1e-3
    )
    await pump.stop_flow()


@pytest.mark.KPump
@pytest.mark.asyncio
async def test_analog_control(pump: AzuraCompactPump):
    await pump.enable_analog_control(True)
    assert await pump.is_analog_control_enabled() is True
    await pump.enable_analog_control(False)
    assert await pump.is_analog_control_enabled() is False


@pytest.mark.KPump
@pytest.mark.asyncio
async def test_is_running(pump: AzuraCompactPump):
    await pump.set_flow("1 ml/min")
    await pump.start_flow()
    assert pump.is_running() is True
    await pump.stop_flow()


@pytest.mark.KPump
@pytest.mark.asyncio
async def test_motor_current(pump: AzuraCompactPump):
    await pump.stop_flow()
    assert await pump.read_motor_current() == 0


@pytest.mark.KPump
@pytest.mark.asyncio
async def test_correction_factor(pump: AzuraCompactPump):
    init_val = await pump.get_correction_factor()
    await pump.set_correction_factor(0)
    assert await pump.get_correction_factor() == 0
    await pump.set_correction_factor(init_val)


@pytest.mark.KPump
@pytest.mark.asyncio
async def test_adjusting_factor(pump: AzuraCompactPump):
    init_val = await pump.get_adjusting_factor()
    await pump.set_adjusting_factor(1000)
    assert await pump.get_adjusting_factor() == 1000
    await pump.set_adjusting_factor(init_val)


@pytest.mark.KPump
@pytest.mark.asyncio
async def test_autostart(pump: AzuraCompactPump):
    await pump.enable_autostart()
    assert await pump.is_autostart_enabled() is True
    await pump.enable_autostart(False)


@pytest.mark.KPump
@pytest.mark.asyncio
async def test_start_in(pump: AzuraCompactPump):
    await pump.require_start_in()
    assert await pump.is_start_in_required() is True
    await pump.require_start_in(False)
