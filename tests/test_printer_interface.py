import os
import pytest
import logging
from components.interfaces import PrinterInterface

@pytest.mark.parametrize("printer_type,print_options", 
                         [
                             ("Fake printer",{}), 
                             ("HP_Envy_6500e_series_E862A7",
                              {
                                  "media": "oe_4x-6-borderless_4x6in",
                                  "media-type": "com.hp-photographic-glossy",
                                  "print-scaling": "auto-fit",
                                  "print-color-mode": "color"})
                         ])
def test_printer_interface(printer_type, print_options):
    # Setup logging for test
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()
    logger.info(f"Testing printer interface with {printer_type}")

    try:
        printer = PrinterInterface(printer_type, print_options)
    except Exception as e:
        pytest.skip(f"Skipping test for {printer_type} due to exception: {e}")

    # Setup the printer
    assert printer.setup() == True, f"Failed to setup {printer_type}"
            