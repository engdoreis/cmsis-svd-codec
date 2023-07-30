# cmsis-svd-codec
This library allows you to programmatically create a svd file for your Microcontroller.
This is particularly useful when you have to parse the data from another
file descriptor format in order to build a svd file.

## How to install
```
pip install cmsis-svd-codec
```

## Example

```python
from cmsis_svd_codec import SvdDevice

device = SvdDevice("RISC-V", "CoffeeBean", version="1.0")

# Fill the device top level details.
device.add_description("Single core 5-stage pipeline RISC-V processor ...")
device.add_license("""Licensed under the Apache License, Version 2.0, see LICENSE for details."""
device.add_cpu("Ibex", "rev01", device_num_Interrupts=2)
device.add_address_config(width="32")

# Add a peripheral to the device.
peripheral = device.add_peripheral("UART0", version="0.1")
peripheral.add_description("Simple UART peripheral")
peripheral.add_base_address(0x4000_0000)
peripheral.add_size(32)
peripheral.add_interrupt(21)
peripheral.add_address_block(offset=0x000, size=0x1000)

# Add a register to the peripheral.
reg = peripheral.add_register("FIFO_STATUS")
reg.add_description("TX and RX fifo status.")
reg.add_offset_address(0x0)

# Add fields to the register.
reg_field = reg.add_field("tx_full")
reg_field.add_description("1 when the tx fifo is full, 0 otherwise.")
reg_field.add_bit_range(first_bit=0, last_bit=0)
reg_field.add_access_permission(read=True, write=False)

reg_field = reg.add_field("tx_fifo_depth")
reg_field.add_description("How may bit there are in the tx fifo.")
reg_field.add_bit_range(first_bit=1, last_bit=4)
reg_field.add_access_permission(read=True, write=False)

# Create a svd file.
device.dump('CoffeeBean.svd')
```

## Contributing 
Please open issues and submit pull request to the repository.