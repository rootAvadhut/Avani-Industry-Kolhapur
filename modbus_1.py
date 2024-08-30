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
async def run_modbus_client():
    async with AsyncModbusTcpClient('192.168.3.250', port=502) as client:
        while True:
            status = await read_register(client, 2058)
            if status:
                if status[0] == 1:
                    # Read data from other registers
                    lpm = await read_register(client, 2008)
                    if lpm:
                        print("LPM", lpm[0] / 100)

                    wp = await read_register(client, 2010)
                    if wp:
                        print("WP", wp[0])

                    bp1 = await read_register(client, 2030)
                    if bp1:
                        print("BP1", bp1[0])

                    bp2 = await read_register(client, 2032)
                    if bp2:
                        print("BP2", bp2[0])
                    noise = await read_register(client, 2016)
                    if noise:
                        print("Noise", noise[0] / 100)    
                    body_no = await read_register(client, 2004, 2)
                    if body_no:
                        msb, lsb = body_no
                        print("body_no", bit16_to_32(msb, lsb))
                    cover_no = await read_register(client, 2006, 2)
                    if cover_no:
                        msb, lsb = cover_no
                        print("cover_no", bit16_to_32(msb, lsb))

                    # Change the value of register 2058 to 3
                    await write_register(client, 2058, 3)
                    print("Data captured")

            await asyncio.sleep(1)  # Adjust sleep time as needed

def bit16_to_32(msb, lsb):
    a = (msb << 16) + lsb
    r = ~a + 1
    return r * -1

asyncio.run(run_modbus_client())