import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
import math

# Function for generating test vectors
def gen_test(BW):
    data_in = [n for n in range(1000)]
    data_out = [0 for n in range(1000)]
    for k in range(4, 1000):
        data_out[k] = math.floor((data_in[k-1] + data_in[k-2] + data_in[k-3] + data_in[k-4])/4)
    return data_in, data_out

async def reset(dut):
    dut.i_rstb.value = 1
    await Timer(1, units = "ns")
    dut.i_rstb.value = 0
    await Timer(1, units = "ns")
    dut.i_rstb.value = 1
    return

@cocotb.test()
async def test_moving_average(dut):
    [data_in, data_out] = gen_test(dut.DATA_WD.value)
    dut.i_data.value = 0
    cocotb.start_soon(Clock(dut.i_clk, 1, units = "ns").start())
    await reset(dut)
    for n in range(len(data_in)):
        await FallingEdge(dut.i_clk)
        dut.i_data.value = int(data_in[n])
        if (n > 8):
            assert dut.o_data.value.signed_integer == data_out[n-1]
