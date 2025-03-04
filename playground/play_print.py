import cups
import os
from PIL import Image

def list_printers():
    conn = cups.Connection()
    printers = conn.getPrinters()

    for printer_name, attributes in printers.items():
        print(f"Printer: {printer_name}")
        for key, value in attributes.items():
            print(f"  {key}: {value}")
        print("-" * 40)

def get_printer_attributes(printer_name, all=False):
    conn = cups.Connection()
    attributes = conn.getPrinterAttributes(printer_name)

    print(f"\nAttributes for printer: {printer_name}\n" + "-" * 50)
    for key, value in attributes.items():
        if not all:
            if key == 'media-supported' or \
               key == 'media-ready' or \
               key == 'media-type-supported' or \
               key == 'print-color-supported' or \
               key == 'print-scaling-supported' or \
               key == 'print-color-mode-supported':
                print(f"{key}: {value}")
        else:
            print(f"{key}: {value}")

def convert_to_pdf(image_path, output_path):
    # Open the image
    img = Image.open(image_path)

    # Convert to RGB if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Convert to PDF
    img.save(output_path, 'PDF', resolution=100.0)


def my_test_print_a4(printer_name):
    conn = cups.Connection()

    test_filepath = 'tests/test.pdf'
    # Check that the file exists
    if not os.path.exists(test_filepath):
        print(f"File {test_filepath} does not exist.")
        return
    
    options = {
        'media': 'iso_a4_210x297mm',
        'media-type': 'stationery',
        'print-scaling': 'auto-fit',
    }
    conn.printFile(printer_name, test_filepath, 'Test Print', options)

def my_test_print_photo(printer_name):
    conn = cups.Connection()

    test_filepath = 'tests/test_pic.JPG'
    # Check that the file exists
    if not os.path.exists(test_filepath):
        print(f"File {test_filepath} does not exist.")
        return
    
    pdf_filepath = test_filepath.replace('.JPG', '.pdf')
    convert_to_pdf(test_filepath, pdf_filepath)

    options = {
        'media': 'oe_4x-6-borderless_4x6in',
        'media-type': 'com.hp-photographic-glossy',
        'print-scaling': 'auto-fit',
        'print-color-mode': 'color',
        # 'document-format': 'image/jpeg',
    }
    conn.printFile(printer_name, pdf_filepath, 'Print '+ test_filepath, options)


if __name__ == "__main__":
    list_printers()

    # Get the desired printer from command line
    printer_name = 'HP_Envy_6500e_series_E862A7_USB'
    printer_name = input("Enter printer name: ") if printer_name == None else printer_name

    get_printer_attributes(printer_name, all=True)

    # Test print
    # my_test_print_a4(printer_name)

    # Test print photo
    my_test_print_photo(printer_name)