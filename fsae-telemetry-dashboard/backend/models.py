from pydantic import BaseModel, Field
from typing import List

class MotorData(BaseModel):
    motorSPD: float = Field(description="Motor speed in m/s")
    motorTMP: float = Field(description="Motor temperature in Fahrenheit")


class ControllerData(BaseModel):
    controllerTMP: float = Field(description="Controller temperature in Fahrenheit")

class BatteryData(BaseModel):
    batteryVOLT: float = Field(description="Battery voltage in Volts")
    batteryTEMP: float = Field(description="Battery temperature in Fahrenheit")
    batteryCURR: float = Field(description="Battery current draw in Amps")

    """
    batteryCCL
    highestTEMP
    lowestTEMP
    relayState
    batterySOC
    batteryRestistance
    openVoltage
    Amphours
    """
    