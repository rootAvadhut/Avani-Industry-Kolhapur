import asyncio
import logging
from pymodbus.client import AsyncModbusTcpClient
from datetime import datetime
import os
from db_connection import get_db_collection
def update_mongodb(data_list):
    """
    Updates the MongoDB collection with values from the data_list based on the BODY field.
    
    Parameters:
    data_list (list): A list containing 'Date', 'Time', 'BODY', 'COVER', 'LPM', 'WP1', 'BP1', 'BP2', 'Noise'.
    """
    # Connect to the MongoDB collection
    collection = get_db_collection()
    
    # Extract values from data_list
    date_str = data_list[0]
    time_str = data_list[1]
    body = data_list[2]
    cover = data_list[3]  # This is still in the list but not used for filtering
    lpm = data_list[4]
    wp1 = data_list[5]
    bp1 = data_list[6]
    bp2 = data_list[7]
    noise = data_list[8]
    
    # Create an update document with the new values
    update_document = {
        'Date': date_str,
        'Time': time_str,
        'LPM': lpm,
        'WP1': wp1,
        'BP1': bp1,
        'BP2': bp2,
        'Noise': noise
    }
    
    # Update the document in MongoDB based on BODY
    result = collection.update_one(
        {'BODY': body},   # Filter by BODY only
        {'$set': update_document},  # Update fields
        upsert=False      # Only update existing documents
    )
    
    if result.matched_count > 0:
        print(f"Document with BODY {body} updated successfully.")
    else:
        print(f"No document found with BODY {body}.")


# Configure logging
log_file_path = 'temp/modbus_data.log'
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s')

async def read_register(client, address, count=1):
    result = await client.read_holding_registers(address, count)
    if result.isError():
        logging.error(f"Error reading registers from address {address}: {result}")
        return None
    return result.registers

async def write_register(client, address, value):
    result = await client.write_register(address, value)
    if result.isError():
        logging.error(f"Error writing to register {address}: {result}")
    else:
        logging.info(f"Successfully wrote value {value} to register {address}")

def bit16_to_32(msb, lsb):
    a = (msb << 16) + lsb
    r = ~a + 1
    return r * -1

async def run_modbus_client():
    async with AsyncModbusTcpClient('192.168.3.250', port=502) as client:
        while True:
            status = await read_register(client, 2058)
            if status and status[0] == 1:
                lpm = await read_register(client, 2008)
                wp = await read_register(client, 2010)
                bp1 = await read_register(client, 2030)
                bp2 = await read_register(client, 2032)
                noise = await read_register(client, 2016)
                body = await client.read_holding_registers(2004, 2)
                cover = await client.read_holding_registers(2006, 2)

                if lpm and wp and bp1 and bp2 and noise and body and cover:
                    LPM = lpm[0] / 100
                    WP1 = wp[0]
                    BP1 = bp1[0]
                    BP2 = bp2[0]
                    Noise = noise[0] / 100
                    msb_body = body.registers[1]
                    lsb_body = body.registers[0]
                    Body = bit16_to_32(msb_body, lsb_body)
                    msb_cover = cover.registers[1]
                    lsb_cover = cover.registers[0]
                    Cover = bit16_to_32(msb_cover, lsb_cover)

                    # Log the values
                    logging.info(f"LPM: {LPM}")
                    logging.info(f"WP1: {WP1}")
                    logging.info(f"BP1: {BP1}")
                    logging.info(f"BP2: {BP2}")
                    logging.info(f"Noise: {Noise}")
                    logging.info(f"BODY: {Body}")
                    logging.info(f"COVER: {Cover}")

                    # Data captured
                    logging.info("Data captured")

                    # Create Date and Time variables
                    Date = datetime.now().strftime('%Y-%m-%d')
                    Time = datetime.now().strftime('%H:%M:%S')

                    # Create a list and log the Date and Time
                    data_list = [Date, Time, Body, Cover, LPM, WP1, BP1, BP2, Noise]
                    logging.info(f"Date: {Date}, Time: {Time}")

                    # Update MongoDB
                    update_mongodb(data_list)

                    # Change the value of register 2058 to 3
                    await write_register(client, 2059, 3)

            await asyncio.sleep(1)

asyncio.run(run_modbus_client())
