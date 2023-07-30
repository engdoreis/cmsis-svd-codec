import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString


class SvdDevice:
    root: ET.Element = None
    index: ET.Element = None
    peripherals: ET.Element = None

    def __init__(self, vendor: str, name: str, version: str):
        self.root = ET.Element(
            "device",
            attrib={
                "schemaVersion": "1.1",
                "xmlns:xs": "http://www.w3.org/2001/XMLSchema-instance",
                "xs:noNamespaceSchemaLocation": "CMSIS-SVD.xsd",
            },
        )
        self.index = self.root
        self.add_element("vendor", vendor)
        self.add_name(name)
        self.add_element("version", version)

    def add_name(self, name: str):
        self.add_element("name", name)

    def add_description(self, description: str):
        self.add_element(
            "description",
            " ".join(description.replace("\n", "").split()),
        )

    def add_license(self, license_text: str):
        self.add_element("licenseText", license_text)

    def add_address_config(self, width: int = 32, unit_bits: int = 8):
        self.add_element("addressUnitBits", str(unit_bits))
        self.add_element("width", str(width))

    def add_cpu(
        self,
        name: str,
        revision: str,
        device_num_Interrupts: int,
        endian: str = "little",
        mpu_present: bool = False,
        fpu_present: bool = False,
        vtor_present: bool = True,
        nvicPrioBits: int = 2,
        vendor_systick_config: bool = False,
    ):
        self.index = ET.SubElement(self.index, "cpu")
        self.add_element("name", name)
        self.add_element("revision", revision)
        self.add_element("endian", endian)
        self.add_element("mpuPresent", str(mpu_present).lower())
        self.add_element("fpuPresent", str(fpu_present).lower())
        self.add_element(
            "vtorPresent",
            str(vtor_present).lower(),
        )
        self.add_element(
            "nvicPrioBits",
            str(nvicPrioBits).lower(),
        )
        self.add_element(
            "vendorSystickConfig",
            str(vendor_systick_config).lower(),
        )
        self.add_element(
            "deviceNumInterrupts",
            str(device_num_Interrupts),
        )
        self.index = self.root

    def add_peripheral(
        self,
        name: str,
        version: str,
        derive_from: str = None,
    ) -> ET.Element:
        if self.peripherals == None:
            self.peripherals = ET.SubElement(self.root, "peripherals")

        return SvdPeripheral(
            self.peripherals,
            name,
            version,
            derive_from,
        )

    def add_element(self, tag: str, name: str, attrib={}) -> ET.Element:
        if self.index.find(tag) == None:
            child = ET.SubElement(self.index, tag, attrib=attrib)
            child.text = name
            return child
        return None

    def dump(self, filename: str):
        svd = ET.ElementTree(self.root)
        svd.write(
            filename,
            encoding="UTF-8",
            xml_declaration=True,
        )
        formated: str
        with open(filename, "r") as f:
            formated = parseString(f.read()).toprettyxml()

        with open(filename, "w") as f:
            f.write(formated)


class SvdPeripheral(SvdDevice):
    root: ET.Element = None
    index: ET.Element = None
    registers: ET.Element = None

    def __init__(
        self,
        parent: ET.Element,
        name: str,
        version: str,
        derive_from: str = None,
    ):
        self.root = parent
        if derive_from:
            self.index = ET.SubElement(
                self.root,
                "peripheral",
                derivedFrom=derive_from,
            )
        else:
            self.index = ET.SubElement(self.root, "peripheral")
        self.add_name(name)
        self.add_element("version", version)

    def add_base_address(self, addr: int):
        self.add_element("baseAddress", hex(addr))

    def add_size(self, size: int):
        self.add_element("size", hex(size))

    def add_address_block(
        self,
        offset: int,
        size: int,
        usage: str = "registers",
    ):
        parent = self.index
        self.index = ET.SubElement(self.index, "addressBlock")
        self.add_element("offset", hex(offset))
        self.add_element("size", hex(size))
        self.add_element("usage", usage)
        self.index = parent

    def add_interrupt(self, num: int):
        parent = self.index
        self.index = ET.SubElement(self.index, "interrupt")
        self.add_element(
            "name",
            parent.find("name").text + " IRQ",
        )
        self.add_element("value", str(num))
        self.index = parent

    def add_register(self, name: str) -> ET.Element:
        if self.registers == None:
            self.registers = ET.SubElement(self.index, "registers")

        return SvdRegister(self.registers, name)


class SvdRegister(SvdPeripheral):
    root: ET.Element = None
    index: ET.Element = None
    fields: ET.Element = None

    def __init__(self, parent: ET.Element, name: str):
        self.root = parent
        self.index = ET.SubElement(self.root, "register")
        self.add_name(name)

    def add_offset_address(self, offset: int):
        self.add_element("addressOffset", hex(offset))

    def add_reset_value(self, reset_val: int):
        self.add_element("resetValue", hex(reset_val))

    def add_field(self, name: str) -> ET.Element:
        if self.fields == None:
            self.fields = ET.SubElement(self.index, "fields")

        return SvdRegisterField(self.fields, name)


class SvdRegisterField(SvdRegister):
    root: ET.Element = None
    index: ET.Element = None

    def __init__(self, parent: ET.Element, name: str):
        self.root = parent
        self.index = ET.SubElement(self.root, "field")
        self.add_name(name)

    def add_bit_range(self, first_bit: int, last_bit: int):
        self.add_element(
            "bitRange",
            f"[{last_bit}:{first_bit}]",
        )

    def add_access_permission(self, read: bool, write: bool):
        access_map = [
            ["None", "write-only"],
            ["read-only", "read-write"],
        ]

        self.add_element("access", access_map[read][write])
