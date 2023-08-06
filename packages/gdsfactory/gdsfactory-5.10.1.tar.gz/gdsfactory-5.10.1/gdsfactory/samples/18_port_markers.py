"""You can define a function to add pins """
import gdsfactory as gf
from gdsfactory.add_pins import add_pins_triangle
from gdsfactory.component import Component


def test_pins_custom() -> Component:
    """You can define the `pins_function` that we use to add markers to each port"""
    c = gf.components.straight(length=11.1)
    c = c.copy()
    add_pins_triangle(component=c)
    return c


if __name__ == "__main__":
    c = test_pins_custom()
    c.show(show_ports=False)
