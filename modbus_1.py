import asyncio
from pymodbus.client import AsyncModbusTcpClient

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
    # print("1")
    async with AsyncModbusTcpClient('192.168.3.250', port=502) as client:
        # print("2")
        while True:
            status = await read_register(client, 2058)
            print(status[0])
            if status:
                if status[0] == 1:
                    # Read data from other registers
                    lpm = await read_register(client, 2008)
                    if lpm:
                        LPM= (lpm[0] / 100)

                    wp = await read_register(client, 2010)
                    if wp:
                        WP1=(wp[0])

                    bp1 = await read_register(client, 2030)
                    if bp1:
                        BP1=(bp1[0])

                    bp2 = await read_register(client, 2032)
                    if bp2:
                        BP2=(bp2[0])
                    noise = await read_register(client, 2016)
                    if noise:
                        Noise=(noise[0] / 100)    
                    body = await client.read_holding_registers(2004, 2)
                    if body.isError():
                        print(f"Error reading registers: {body}")
                    else:
                        msb = body.registers[1]
                        lsb = body.registers[0]
                        Body=(bit16_to_32(msb,lsb))
                        
                    cover = await client.read_holding_registers(2006, 2)
                    if cover.isError():
                        print(f"Error reading registers: {cover}")
                    else:
                        msb = cover.registers[1]
                        lsb = cover.registers[0]
                        Cover=(bit16_to_32(msb,lsb))
                    # Change the value of register 2058 to 3
                    await write_register(client, 2059, 3)
                    print("Data captured")

            await asyncio.sleep(1)  # Adjust sleep time as needed



asyncio.run(run_modbus_client())