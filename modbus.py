import asyncio
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ConnectionException
from datetime import datetime
from db_connection import get_db_collection


def update_mongodb(data_list):
    """
    Updates the MongoDB collection with values from the data_list based on the BODY field.
    """
    collection = get_db_collection()
    
    # Extract values from data_list
    date_str = data_list[0]
    time_str = data_list[1]
    body = int(data_list[2])  # Convert numpy.int64 to int
    cover = int(data_list[3])  # Convert numpy.int64 to int
    lpm = float(data_list[4])  # Ensure LPM is a float
    wp1 = int(data_list[5])    # Ensure WP1 is an int
    bp1 = int(data_list[6])    # Ensure BP1 is an int
    bp2 = int(data_list[7])    # Ensure BP2 is an int
    noise = float(data_list[8])  # Ensure noise is a float
    
    update_document = {
        'Date': date_str,
        'Time': time_str,
        'LPM': lpm,
        'WP1': wp1,
        'BP1': bp1,
        'BP2': bp2,
        'Noise': noise
    }
    
    result = collection.update_one({'BODY': body}, {'$set': update_document}, upsert=False)
    
    if result.matched_count > 0:
        print(f"Document with BODY {body} updated successfully.")
    else:
        print(f"No document found with BODY {body}.")


async def read_register(client, address, count=1):
    try:
        result = await client.read_holding_registers(address, count)
        if result.isError():
            print(f"Error reading registers from address {address}: {result}")
            return None
        return result.registers
    except ConnectionException as e:
        print(f"Connection error when reading register {address}: {e}")
        return None


async def write_register(client, address, value):
    try:
        result = await client.write_register(address, value)
        if result.isError():
            print(f"Error writing to register {address}: {result}")
        else:
            print(f"Successfully wrote value {value} to register {address}")
    except ConnectionException as e:
        print(f"Connection error when writing to register {address}: {e}")


def bit16_to_32(msb, lsb):
    a = (msb << 16) + lsb
    r = ~a + 1
    return r * -1


async def run_modbus_client(stop_event):
    try:
        async with AsyncModbusTcpClient('192.168.3.250', port=502) as client:
            while not stop_event.is_set():
                # Read status register
                status = await read_register(client, 2059)
                print(status)

                if status and status[0] == 1:
                    # Read other required registers
                    lpm = await read_register(client, 2008)
                    wp = await read_register(client, 2010)
                    bp1 = await read_register(client, 2030)
                    bp2 = await read_register(client, 2032)
                    noise = await read_register(client, 2016)
                    body = await client.read_holding_registers(2004, 2)
                    cover = await client.read_holding_registers(2006, 2)

                    # If all data is captured successfully
                    if lpm and wp and bp1 and bp2 and noise and body and cover:
                        LPM = lpm[0] / 100
                        WP1 = wp[0]
                        BP1 = bp1[0]
                        BP2 = bp2[0]
                        Noise = noise[0] / 100

                        # Extract Body and Cover using bit16_to_32 function
                        msb_body = body.registers[1]
                        lsb_body = body.registers[0]
                        Body = bit16_to_32(msb_body, lsb_body)

                        msb_cover = cover.registers[1]
                        lsb_cover = cover.registers[0]
                        Cover = bit16_to_32(msb_cover, lsb_cover)

                        # Print the captured data
                        print(f"LPM: {LPM}, WP1: {WP1}, BP1: {BP1}, BP2: {BP2}, Noise: {Noise}, BODY: {Body}, COVER: {Cover}")

                        # Data captured
                        print("Data captured")

                        # Create Date and Time variables
                        Date = datetime.now().strftime('%Y-%m-%d')
                        Time = datetime.now().strftime('%H:%M')

                        # Create a list and log the Date and Time
                        data_list = [Date, Time, Body, Cover, LPM, WP1, BP1, BP2, Noise]
                        print(f"Date: {Date}, Time: {Time}")

                        # Update MongoDB
                        update_mongodb(data_list)

                        # Change the value of register 2058 to 3
                        await write_register(client, 2059, 3)

                # Sleep for 1 second before the next iteration
                await asyncio.sleep(1)

    except ConnectionException as e:
        print(f"Connection to PLC failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Modbus client stopped.")


# import asyncio
# from pymodbus.client import AsyncModbusTcpClient
# from pymodbus.exceptions import ConnectionException
# from datetime import datetime
# from db_connection import get_db_collection


# def update_mongodb(data_list):
#     """
#     Updates the MongoDB collection with values from the data_list based on the BODY field.
#     """
#     collection = get_db_collection()
    
#     # Extract values from data_list
#     date_str = data_list[0]
#     time_str = data_list[1]
#     body = int(data_list[2])  # Convert numpy.int64 to int
#     cover = int(data_list[3])  # Convert numpy.int64 to int
#     lpm = float(data_list[4])  # Ensure lpm is a float
#     wp1 = int(data_list[5])  # Ensure wp1 is an int
#     bp1 = int(data_list[6])  # Ensure bp1 is an int
#     bp2 = int(data_list[7])  # Ensure bp2 is an int
#     noise = float(data_list[8])  # Ensure noise is a float
    
#     update_document = {
#         'Date': date_str,
#         'Time': time_str,
#         'LPM': lpm,
#         'WP1': wp1,
#         'BP1': bp1,
#         'BP2': bp2,
#         'Noise': noise
#     }
    
#     result = collection.update_one({'BODY': body}, {'$set': update_document}, upsert=False)
    
#     if result.matched_count > 0:
#         print(f"Document with BODY {body} updated successfully.")
#     else:
#         print(f"No document found with BODY {body}.")

# async def read_register(client, address, count=1):
#     try:
#         result = await client.read_holding_registers(address, count)
#         if result.isError():
#             print(f"Error reading registers from address {address}: {result}")
#             return None
#         return result.registers
#     except ConnectionException as e:
#         print(f"Connection error when reading register {address}: {e}")
#         return None

# async def write_register(client, address, value):
#     try:
#         result = await client.write_register(address, value)
#         if result.isError():
#             print(f"Error writing to register {address}: {result}")
#         else:
#             print(f"Successfully wrote value {value} to register {address}")
#     except ConnectionException as e:
#         print(f"Connection error when writing to register {address}: {e}")

# def bit16_to_32(msb, lsb):
#     a = (msb << 16) + lsb
#     r = ~a + 1
#     return r * -1

# async def run_modbus_client(stop_event):
#     try:
        
#         async with AsyncModbusTcpClient('192.168.3.250', port=502) as client:
#             while not stop_event.is_set():
                
#                 status = await read_register(client, 2059)
#                 print(status)
#                 if status and status[0] == 1: 
#                     lpm = await read_register(client, 2008)
#                     wp = await read_register(client, 2010)
#                     bp1 = await read_register(client, 2030)
#                     bp2 = await read_register(client, 2032)
#                     noise = await read_register(client, 2016)
#                     body = await client.read_holding_registers(2004, 2)
#                     cover = await client.read_holding_registers(2006, 2)

#                     if lpm and wp and bp1 and bp2 and noise and body and cover:
#                         LPM = lpm[0] / 100
#                         WP1 = wp[0]
#                         BP1 = bp1[0]
#                         BP2 = bp2[0]
#                         Noise = noise[0] / 100
#                         msb_body = body.registers[1]
#                         lsb_body = body.registers[0]
#                         Body = bit16_to_32(msb_body, lsb_body)
#                         msb_cover = cover.registers[1]
#                         lsb_cover = cover.registers[0]
#                         Cover = bit16_to_32(msb_cover, lsb_cover)

#                         # Print the captured data
#                         print(f"LPM: {LPM}, WP1: {WP1}, BP1: {BP1}, BP2: {BP2}, Noise: {Noise}, BODY: {Body}, COVER: {Cover}")

#                         # Data captured
#                         print("Data captured")

#                         # Create Date and Time variables
#                         Date = datetime.now().strftime('%Y-%m-%d')
#                         Time = datetime.now().strftime('%H:%M')

#                         # Create a list and log the Date and Time
#                         data_list = [Date, Time, Body, Cover, LPM, WP1, BP1, BP2, Noise]
#                         print(f"Date: {Date}, Time: {Time}")

#                         # Update MongoDB
#                         update_mongodb(data_list)

#                         # Change the value of register 2058 to 3
#                         await write_register(client, 2059, 3)

#                 await asyncio.sleep(1)

#     except ConnectionException as e:
#         print(f"Connection to PLC failed: {e}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#     finally:
#         print("Modbus client stopped.")
