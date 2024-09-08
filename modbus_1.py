import asyncio
from datetime import datetime
from pymodbus.client import AsyncModbusTcpClient
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
    lpm = float(data_list[4])  # Ensure lpm is a float
    wp1 = int(data_list[5])  # Ensure wp1 is an int
    bp1 = int(data_list[6])  # Ensure bp1 is an int
    bp2 = int(data_list[7])  # Ensure bp2 is an int
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
    result = await client.read_holding_registers(address, count)
    if result.isError():
        print(f"Error reading registers from address {address}: {result}")
        return None
    return result.registers

async def write_register(client, address, value):
    result = await client.write_register(address, value)
    if result.isError():
        print(f"Error writing to register {address}: {result}")
    else:
        print(f"Successfully wrote value {value} to register {address}")

def bit16_to_32(msb, lsb):
    a = (msb << 16) + lsb
    r = ~a + 1
    return r * -1

async def run_modbus_client():
    async with AsyncModbusTcpClient('192.168.3.250', port=502) as client:
        while True:
            status = await read_register(client, 2059)
            print(status[0])
            if status:
                if status[0] == 1:
                    # Read data from other registers
                    lpm = await read_register(client, 2008)
                    if lpm:
                        LPM = lpm[0] / 100
                        print(LPM)

                    wp = await read_register(client, 2010)
                    if wp:
                        WP1 = wp[0]
                        print(WP1)

                    bp1 = await read_register(client, 2030)
                    if bp1:
                        BP1 = bp1[0]
                        print(BP1)

                    bp2 = await read_register(client, 2032)
                    if bp2:
                        BP2 = bp2[0]
                        print(BP2)

                    noise = await read_register(client, 2016)
                    if noise:
                        Noise = noise[0] / 100
                        print(Noise)   

                    body = await client.read_holding_registers(2004, 2)
                    if body.isError():
                        print(f"Error reading registers: {body}")
                    else:
                        msb = body.registers[1]
                        lsb = body.registers[0]
                        Body = bit16_to_32(msb, lsb)
                        print(Body)
                        
                    cover = await client.read_holding_registers(2006, 2)
                    if cover.isError():
                        print(f"Error reading registers: {cover}")
                    else:
                        msb = cover.registers[1]
                        lsb = cover.registers[0]
                        Cover = bit16_to_32(msb, lsb)
                        print(Cover)

                    # Change the value of register 2058 to 3
                    await write_register(client, 2059, 3)
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

            await asyncio.sleep(1)  # Adjust sleep time as needed


# Run the asyncio event loop
asyncio.run(run_modbus_client())


# import asyncio
# from datetime import datetime
# from pymodbus.client import AsyncModbusTcpClient
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
#     result = await client.read_holding_registers(address, count)
#     if result.isError():
#         print(f"Error reading registers from address {address}: {result}")
#         return None
#     return result.registers

# async def write_register(client, address, value):
#     result = await client.write_register(address, value)
#     if result.isError():
#         print(f"Error writing to register {address}: {result}")
#     else:
#         print(f"Successfully wrote value {value} to register {address}")
# def bit16_to_32(msb, lsb):
#     a = (msb << 16) + lsb
#     r = ~a + 1
#     return r * -1
# async def run_modbus_client():
#     # print("1")
#     async with AsyncModbusTcpClient('192.168.3.250', port=502) as client:
#         # print("2")
#         while True:
#             status = await read_register(client, 2059)
#             print(status[0])
#             if status:
#                 if status[0] == 1:
#                     # Read data from other registers
#                     lpm = await read_register(client, 2008)
#                     if lpm:
#                         LPM= (lpm[0] / 100)
#                         print(LPM)

#                     wp = await read_register(client, 2010)
#                     if wp:
#                         WP1=(wp[0])
#                         print(WP1)

#                     bp1 = await read_register(client, 2030)
#                     if bp1:
#                         BP1=(bp1[0])
#                         print(BP1)

#                     bp2 = await read_register(client, 2032)
#                     if bp2:
#                         BP2=(bp2[0])
#                         print(BP2)
#                     noise = await read_register(client, 2016)
#                     if noise:
#                         Noise=(noise[0] / 100)
#                         print(Noise)   
#                     body = await client.read_holding_registers(2004, 2)
#                     if body.isError():
#                         print(f"Error reading registers: {body}")
#                     else:
#                         msb = body.registers[1]
#                         lsb = body.registers[0]
#                         Body=(bit16_to_32(msb,lsb))
#                         print( Body)
                        
#                     cover = await client.read_holding_registers(2006, 2)
#                     if cover.isError():
#                         print(f"Error reading registers: {cover}")
#                     else:
#                         msb = cover.registers[1]
#                         lsb = cover.registers[0]
#                         Cover=(bit16_to_32(msb,lsb))
#                         print(Cover)
#                     # Change the value of register 2058 to 3
#                     await write_register(client, 2059, 3)
#                     print("Data captured")
#                     # Create Date and Time variables
#                     Date = datetime.datetime.now().strftime('%Y-%m-%d')
#                     Time = datetime.datetime.now().strftime('%H:%M')


#                     # Create a list and log the Date and Time
#                     data_list = [Date, Time, Body, Cover, LPM, WP1, BP1, BP2, Noise]
#                     print(f"Date: {Date}, Time: {Time}")

#                     # Update MongoDB
#                     update_mongodb(data_list)

#                     # Change the value of register 2058 to 3
#                     await write_register(client, 2059, 3)

#             await asyncio.sleep(1)  # Adjust sleep time as needed



# asyncio.run(run_modbus_client())