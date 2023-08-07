from math import pi

from loguru import logger

from flowchem.components.properties import Component
from flowchem.units import flowchem_ureg


class Tube(Component):
    """
    A tube.

    Arguments:
    - `length`: The length of the tube as a str.
    - `ID`: The inner diameter of the tube as a str.
    - `OD`: The outer diameter of the tube as a str.
    - `material`: The material of the tube.

    Attributes:
    - `ID`: The inner diameter of the tube, converted to a `pint.Quantity`.
    - `length`: The length of the tube, converted to a `pint.Quantity`.
    - `material`: The material of the tube.
    - `OD`: The outer diameter of the tube, converted to a `pint.Quantity`.
    - `volume`: The tube volume, as determined from the length and inner diameter, converted to a `pint.Quantity`.

    Raises:
        - ValueError: When the outer diameter is less than the inner diameter of the tube.
    """

    tube_counter = 0

    def __init__(self, length: str, ID: str, OD: str, material: str):
        """
        See the `Tube` attributes for a description of the arguments.

        ::: tip Note
        The arguments to __init__ are `str`s, not `pint.Quantity`s.
        :::
        """
        self.length = flowchem_ureg.parse_expression(length)
        self.ID = flowchem_ureg.parse_expression(ID)
        self.OD = flowchem_ureg.parse_expression(OD)

        # check to make sure units are valid
        for measurement in [self.length, self.ID, self.OD]:
            if measurement.dimensionality != flowchem_ureg.mm.dimensionality:
                logger.exception("Invalid units for tube length, ID, or OD")
                raise ValueError(
                    f"{measurement.units} is an invalid unit of measurement for length."
                )

        # ensure diameters are valid
        if self.OD <= self.ID:
            logger.exception("Invalid tube dimensions")
            raise ValueError(
                f"Outer diameter {OD} must be greater than inner diameter {ID}"
            )
        if self.length < self.OD or self.length < self.ID:
            logger.warning(
                f"Tube length ({self.length}) is less than diameter."
                "Make sure that this is not an error."
            )

        self.material = material
        self.volume = pi * ((self.ID / 2) ** 2) * self.length

        Tube.tube_counter += 1
        self.name = f"Tube_{Tube.tube_counter}"
        super(Tube, self).__init__(name=self.name)

    def __repr__(self):
        return f"Tube of length {self.length}, ID {self.ID}, OD {self.OD}"
