import asyncio
from pymodbus.client import AsyncModbusTcpClient

async def run_modbus_client_LPM():
    # Create an asynchronous Modbus TCP client
    async with AsyncModbusTcpClient('192.168.3.250', port=502) as client:
        # Read holding registers starting from address 0
        #42008 >2008
        result = await client.read_holding_registers(2008, 1)

        
        # result = await client.read_coils(0,10)
        # result = await client.read_input_registers(1,1)

        if result.isError():
            print(f"Error reading registers: {result}")
        else:
            # print(f"Registers: {result.registers[0]}")
            #LPM
            # print(type(result.registers[0]))
            result=result.registers[0]/100
            print("LPM",result)
            #WP
async def run_modbus_client_WP():
    # Create an asynchronous Modbus TCP client
    async with AsyncModbusTcpClient('192.168.3.250', port=502) as client:
        # Read holding registers starting from address 0
        #42008 >2008
        result = await client.read_holding_registers(2010, 1)

        
        # result = await client.read_coils(0,10)
        # result = await client.read_input_registers(1,1)

        if result.isError():
            print(f"Error reading registers: {result}")
        else:
            # print(f"Registers: {result.registers[0]}")
            #LPM
            # print(type(result.registers[0]))
            result=result.registers[0]
            print("WP",result)

async def run_modbus_client_Noise():
    # Create an asynchronous Modbus TCP client
    async with AsyncModbusTcpClient('192.168.3.250', port=502) as client:
        # Read holding registers starting from address 0
        #42008 >2008
        result = await client.read_holding_registers(2016, 1)

        
        # result = await client.read_coils(0,10)
        # result = await client.read_input_registers(1,1)

        if result.isError():
            print(f"Error reading registers: {result}")
        else:
            # print(f"Registers: {result.registers[0]}")
            #LPM
            # print(type(result.registers[0]))
            result=result.registers[0]/100
            print("Noise",result)

async def run_modbus_client_BP1():
    # Create an asynchronous Modbus TCP client
    async with AsyncModbusTcpClient('192.168.3.250', port=502) as client:
        # Read holding registers starting from address 0
        #42008 >2008
        result = await client.read_holding_registers(2030, 1)

        
        # result = await client.read_coils(0,10)
        # result = await client.read_input_registers(1,1)

        if result.isError():
            print(f"Error reading registers: {result}")
        else:
            # print(f"Registers: {result.registers[0]}")
            #LPM
            # print(type(result.registers[0]))
            result=result.registers[0]
            print("BP1",result)
async def run_modbus_client_BP2():
    # Create an asynchronous Modbus TCP client
    async with AsyncModbusTcpClient('192.168.3.250', port=502) as client:
        # Read holding registers starting from address 0
        #42008 >2008
        result = await client.read_holding_registers(2032, 1)

        
        # result = await client.read_coils(0,10)
        # result = await client.read_input_registers(1,1)

        if result.isError():
            print(f"Error reading registers: {result}")
        else:
            # print(f"Registers: {result.registers[0]}")
            #LPM
            # print(type(result.registers[0]))
            result=result.registers[0]
            print("BP2",result)

      
# Run the asyncio loop
# asyncio.run(run_modbus_client())

def bit16_to_32(msb,lsb):
    a=(msb<<16) +lsb
    r=~(a)+1
    r=r*-1
    return r
async def run_modbus_client_body_no():
    # Create an asynchronous Modbus TCP client
    async with AsyncModbusTcpClient('192.168.3.250', port=502) as client:
        # Read holding registers starting from address 0
        #42008 >2008
        result = await client.read_holding_registers(2004, 2)

        
        # result = await client.read_coils(0,10)
        # result = await client.read_input_registers(1,1)

        if result.isError():
            print(f"Error reading registers: {result}")
        else:
           msb = result.registers[1]
           lsb = result.registers[0]
           print("body_no",bit16_to_32(msb,lsb))
          
          


async def run_modbus_client_cover_no():
    # Create an asynchronous Modbus TCP client
    async with AsyncModbusTcpClient('192.168.3.250', port=502) as client:
        # Read holding registers starting from address 0
        #42008 >2008
        result = await client.read_holding_registers(2006, 2)

        
        # result = await client.read_coils(0,10)
        # result = await client.read_input_registers(1,1)

        if result.isError():
            print(f"Error reading registers: {result}")
        else:
           msb = result.registers[1]
           lsb = result.registers[0]
           print("cover_no",bit16_to_32(msb,lsb))
          
asyncio.run(run_modbus_client_body_no())       
asyncio.run(run_modbus_client_cover_no())
asyncio.run(run_modbus_client_LPM())
asyncio.run(run_modbus_client_WP())
asyncio.run(run_modbus_client_Noise())
asyncio.run(run_modbus_client_BP1())
asyncio.run(run_modbus_client_BP2())