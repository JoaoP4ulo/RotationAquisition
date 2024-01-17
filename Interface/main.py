import serial
import openpyxl
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from datetime import datetime
import struct
import time

# Replace 'COMx' with the actual serial port name (e.g., 'COM3' on Windows or '/dev/ttyUSB0' on Linux)
serial_port = serial.Serial('COM9', baudrate=9600, timeout=1)

# Create a new Excel workbook and add a sheet
workbook = Workbook()
sheet = workbook.active

# Initialize column headers
sheet['A1'] = 'Timestamp'
sheet['B1'] = 'Rot 1'
sheet['C1'] = 'Rot 2'
sheet['D1'] = ' Rot 3'

row_index = 2  # Start writing data from the second row

try:
    while True:
        # Read data from the serial port (assuming 6 bytes for 3 UINT16 numbers)
        serial_data = serial_port.read(6)

        if len(serial_data) == 6:
            # Unpack the data into three UINT16 numbers
            data_tuple = struct.unpack('HHH', serial_data)

            # Get current timestamp
            timestamp = datetime.now().strftime('%H:%M:%S')

            # Write data to Excel sheet
            sheet[f'A{row_index}'] = timestamp
            sheet[f'B{row_index}'] = data_tuple[0]
            sheet[f'C{row_index}'] = data_tuple[1]
            sheet[f'D{row_index}'] = data_tuple[2]

            # Increment row index
            row_index += 1

            # Save the workbook periodically (adjust the interval as needed)
            if row_index % 10 == 0:
                workbook.save('serial_data.xlsx')

            # Optional: Print data to the console
            print(f'Timestamp: {timestamp}, Data1: {data_tuple[0]}, Data2: {data_tuple[1]}, Data3: {data_tuple[2]}')

            # Optional: Add a delay to control the update rate
            time.sleep(1)

except KeyboardInterrupt:
    # Save the workbook when the program is interrupted
    workbook.save('serial_data.xlsx')
    print("Program terminated. Excel file saved.")
    serial_port.close()