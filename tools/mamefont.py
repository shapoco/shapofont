import enum
from design import GrayBitmap
from itertools import product
import time
import math
import json

LIB_NAME = "MameFont"

VERBOSE = False

REPORT_INTERVAL_SEC = 5


def verbose_print(s: str = "") -> None:
    if VERBOSE:
        print(s)


class Field:
    def __init__(
        self,
        pos: int,
        width: int = 1,
        bias: int = 0,
        step: int = 1,
        min: int | None = None,
        max: int | None = None,
    ):
        self.pos = pos
        self.width = width
        self.bias = bias
        self.step = step
        self.min = bias if min is None else min
        self.max = (bias + step * ((1 << width) - 1)) if max is None else max
        self.range = range(self.min, self.max + 1, self.step)

    def read(self, value: int) -> int:
        return self.bias + self.step * ((value >> self.pos) & ((1 << self.width) - 1))

    def place(self, value: int) -> int:
        if value < self.min or value > self.max:
            raise ValueError(f"Value {value} out of range")
        if (value - self.bias) % self.step != 0:
            raise ValueError(f"Value {value} is not a multiple of step {self.step}")
        return ((value - self.bias) // self.step) << self.pos


OFST_FORMAT_VERSION = 0
OFST_FONT_FLAGS = 1
OFST_FIRST_CODE = 2
OFST_GLYPH_TABLE_LEN = 3
OFST_LUT_SIZE = 4
OFST_FONT_DIMENSION_0 = 5
OFST_FONT_DIMENSION_1 = 6
OFST_FONT_DIMENSION_2 = 7
OFST_GLYPH_TABLE = 8
OFST_ENTRY_POINT = 0
OFST_GLYPH_DIMENSION = 2

GLYPH_MAX_WIDTH = 64
GLYPH_MAX_HEIGHT = 64

FONT_FLAG_VERTICAL_FRAGMENT = 0x80
FONT_FLAG_MSB_FIRST = 0x40
FONT_FLAG_SHRINKED_GLYPH_TABLE = 0x20

FONT_DIM_FONT_HEIGHT = Field(0, 6, bias=1)
FONT_DIM_Y_SPACING = Field(0, 6)
FONT_DIM_MAX_GLYPH_WIDTH = Field(0, 6, bias=1)

GLYPH_DIM_WIDTH = Field(0, 6, bias=1)
GLYPH_DIM_X_SPACING = Field(0, 5, bias=-16)
GLYPH_DIM_X_LEFT_SHIFT = Field(5, 3)

GLYPH_SHRINKED_DIM_WIDTH = Field(0, 4, bias=1)
GLYPH_SHRINKED_DIM_X_SPACING = Field(4, 2)
GLYPH_SHRINKED_DIM_LEFT_SHIFT = Field(6, 2)

RPT_REPEAT_COUNT = Field(0, 4, bias=1)

SFT_REPEAT_COUNT = Field(0, 2, bias=1)
SFT_SHIFT_SIZE = Field(2, 2, bias=1)
SFT_POST_OP = Field(4, 1)
SFT_SHIFT_DIR = Field(5, 1)

XOR_MASK_POS = Field(0, 3)
XOR_MASK_WIDTH = Field(3, 1, bias=1)

CPY_LENGTH = Field(0, 3, bias=1)
CPY_OFFSET = Field(3, 2, bias=0)
CPY_BYTE_REVERSE = Field(5, 1)

CPX_OFFSET_BITS = 9
CPX_OFFSET_H = Field(0, CPX_OFFSET_BITS - 8)
CPX_INVERSE = Field(1, 1)
CPX_LENGTH = Field(2, 4, bias=4, step=4)
CPX_BYTE_REVERSE = Field(6, 1)
CPX_BIT_REVERSE = Field(7, 1)

LUP_INDEX = Field(0, 6)
LUD_INDEX = Field(0, 4)

MAX_LUT_SIZE = 1 << LUP_INDEX.width

ALIGN_SIZE = 2


def roundup_size(size: int) -> int:
    return (size + (ALIGN_SIZE - 1)) & ~(ALIGN_SIZE - 1)


def format_char(c: int) -> str:
    if c >= 0x20 and c <= 0x7E:
        return f"'{chr(c)}' (0x{c:x})"
    else:
        return f"\\x{c:02x}"


class Operator:
    def __init__(
        self, mnemonic, base_code: int, ranges: list[tuple[int, int]], cost: int
    ):
        self.mnemonic = mnemonic
        self.code = base_code
        self.ranges = ranges if ranges is not None else []
        self.cost = cost

    def match(self, target: int) -> bool:
        for start, end in self.ranges:
            if start <= target <= end:
                return True
        return False

    def __repr__(self) -> str:
        return f"Operator(mnemonic={self.mnemonic}, code=0x{self.code:02X}, ranges={self.ranges}, cost={self.cost})"


RPT = Operator("RPT", 0xE0, [(0xE0, 0xEF)], 1001)
CPY = Operator(
    "CPY",
    0x40,
    [(0x41, 0x5F), (0x61, 0x67), (0x69, 0x6F), (0x71, 0x77), (0x79, 0x7F)],
    1002,
)
XOR = Operator("XOR", 0xF0, [(0xF0, 0xFE)], 1004)
SFT = Operator("SFT", 0x00, [(0x00, 0x3F)], 1005)
LUP = Operator("LUP", 0x80, [(0x80, 0xBF)], 1006)
LUD = Operator("LUD", 0xC0, [(0xC0, 0xDF)], 1006)
LDI = Operator("LDI", 0x60, [(0x60, 0x60)], 1009)
CPX = Operator("CPX", 0x40, [(0x40, 0x40)], 3100)
ABO = Operator("ABO", 0xFF, [(0xFF, 0xFF)], 2000)

UNKNOWN = Operator("(unknown)", -1, [], 999999)

opcodes = [
    RPT,
    CPY,
    XOR,
    SFT,
    LUP,
    LUD,
    LDI,
    CPX,
    ABO,
]


class ScanDirection(enum.IntEnum):
    HORIZONTAL = 0
    VERTICAL = 1


class ShiftDir(enum.IntEnum):
    LEFT = 0
    RIGHT = 1


class ShiftPostOp(enum.IntEnum):
    CLR = 0
    SET = 1


def parse_opcode(target: int) -> Operator:
    for opcode in opcodes:
        if opcode.match(target):
            return opcode
    return UNKNOWN


def parse_instruction(
    bytecode: list[int], offset: int
) -> tuple[Operator, int, int, dict[str, int]]:
    byte1 = bytecode[offset]
    operator = parse_opcode(byte1)
    if operator == LUP:
        return (LUP, 1, 1, {"index": byte1 & 0x3F})
    elif operator == LUD:
        return (LUD, 1, 2, {"index": byte1 & 0x0F, "step": (byte1 >> 4) & 0x01})
    elif operator == SFT:
        repeat_count = (byte1 & 0x03) + 1
        params = {
            "shift_size": SFT_SHIFT_SIZE.read(byte1),
            "repeat_count": SFT_REPEAT_COUNT.read(byte1),
            "post_op": SFT_POST_OP.read(byte1),
            "shift_dir": SFT_SHIFT_DIR.read(byte1),
        }
        return (operator, 1, repeat_count, params)
    elif operator == LDI:
        params = {
            "byte": bytecode[offset + 1],
        }
        return (LDI, 2, 1, params)
    elif operator == XOR:
        params = {
            "mask_width": XOR_MASK_WIDTH.read(byte1),
            "mask_pos": XOR_MASK_POS.read(byte1),
        }
        return (XOR, 1, 1, params)
    elif operator == RPT:
        repeat_count = RPT_REPEAT_COUNT.read(byte1)
        params = {
            "repeat_count": repeat_count,
        }
        return (RPT, 1, repeat_count, params)
    elif operator == CPY:
        length = CPY_LENGTH.read(byte1)
        params = {
            "offset": CPY_OFFSET.read(byte1),
            "length": length,
            "byte_reverse": CPY_BYTE_REVERSE.read(byte1),
        }
        return (CPY, 1, length, params)
    elif operator == CPX:
        byte2 = bytecode[offset + 1]
        byte3 = bytecode[offset + 2]
        params = {
            "offset": ((CPX_OFFSET_H.read(byte3) << 8) | byte2),
            "length": CPX_LENGTH.read(byte3),
            "inverse": CPX_INVERSE.read(byte3),
            "byte_reverse": CPX_BYTE_REVERSE.read(byte3),
            "bit_reverse": CPX_BIT_REVERSE.read(byte3),
        }
        return (CPX, 3, params["length"], params)
    elif operator == ABO:
        return (ABO, 1, 0, {})
    else:
        return (UNKNOWN, 0, 0, {})


class Operation:
    def __init__(self, bytecode: list[int], orig_seq: list[int], cost: float):
        self.bytecode = bytecode
        self.orig_seq = orig_seq
        self.cost = cost

    def operator(self) -> Operator:
        (op, _, _, _) = parse_instruction(self.bytecode, 0)
        return op

    def __repr__(self) -> str:
        (op, _, _, params) = parse_instruction(self.bytecode, 0)
        ret = f"{op.mnemonic} ("
        for key, value in params.items():
            ret += f"{key}={value}, "
        ret = ret.rstrip(", ")
        ret += ")"
        return ret


class MameGlyph:
    def __init__(
        self, code: int, operations: list[Operation], glyphWidth: int, x_spacing: int
    ):
        self.code = code
        self.operations = operations
        self.glyph_width = glyphWidth
        self.x_spacing = x_spacing
        self.entry_point = 0xFFFF


class MameFont:
    def __init__(self, name: str, blob: list[int]):
        self.name = name
        self.blob = blob

    def get_num_glyphs(self) -> int:
        return self.blob[OFST_GLYPH_TABLE_LEN] + 1

    def get_flags(self) -> int:
        return self.blob[OFST_FONT_FLAGS]

    def is_shrinked_glyph_table(self) -> bool:
        return 0 != (self.get_flags() & FONT_FLAG_SHRINKED_GLYPH_TABLE)

    def get_glyph_table_entry_size(self) -> int:
        return 2 if self.is_shrinked_glyph_table() else 4

    def get_glyph_table_size(self) -> int:
        return self.get_num_glyphs() * self.get_glyph_table_entry_size()

    def get_lut_size(self) -> int:
        return self.blob[OFST_LUT_SIZE] + 1

    def generate_c_style_array(
        self, indent="  ", with_comment=True, hexadecimal=True
    ) -> str:
        cols = 16
        i_col = 0
        i_start_of_header = 0
        i_start_of_glyph_table = OFST_GLYPH_TABLE
        i_start_of_lut = i_start_of_glyph_table + self.get_glyph_table_size()
        i_start_of_bytecodes = i_start_of_lut + self.get_lut_size()

        code = ""
        for i, b in enumerate(self.blob):
            if with_comment:
                if i == i_start_of_header:
                    code += f"{indent}// Font Header\n"
                if i == i_start_of_glyph_table:
                    code += f"{indent}// Glyph Table\n"
                if i == i_start_of_lut:
                    code += f"{indent}// Lookup Table\n"
                if i == i_start_of_bytecodes:
                    code += f"{indent}// Bytecodes\n"

            if i_col == 0:
                code += f"{indent}"
            code += f"0x{b:02X}," if hexadecimal else f"{b},"

            is_end_of_section = (
                i_col == cols - 1
                or i == i_start_of_glyph_table - 1
                or i == i_start_of_lut - 1
                or i == i_start_of_bytecodes - 1
                or i == len(self.blob) - 1
            )

            if is_end_of_section:
                code += "\n"
                i_col = 0
            else:
                code += " "
                i_col += 1

        return code

    def generate_cpp_header(self) -> str:
        verbose_print(f"[{LIB_NAME}] Generating C++ header...")

        code = ""
        code += "#pragma once\n"
        code += "\n"
        code += "// Generated from ShapoFont\n"
        code += "\n"
        code += "#include <stdint.h>\n"
        code += "#include <mamefont/mamefont.hpp>\n"
        code += "\n"
        code += f"extern const mamefont::Font {self.name};\n"
        code += "\n"
        return code

    def generate_cpp_source(self) -> str:
        verbose_print(f"[{LIB_NAME}] Generating C++ source...")

        blob_size = len(self.blob)

        font_flags = self.get_flags()
        vertical_frag = 0 != (font_flags & FONT_FLAG_VERTICAL_FRAGMENT)
        msb1st = 0 != (font_flags & FONT_FLAG_MSB_FIRST)
        shrinked_glyph_table = self.is_shrinked_glyph_table()

        glyph_height = (self.blob[OFST_FONT_DIMENSION_0] & 0x3F) + 1
        max_glyph_width = (self.blob[OFST_FONT_DIMENSION_2] & 0x3F) + 1

        first_code = self.blob[OFST_FIRST_CODE]
        num_glyphs = self.get_num_glyphs()
        glyph_table_entry_size = self.get_glyph_table_entry_size()
        glyph_table_size = self.get_glyph_table_size()
        lut_size = self.get_lut_size()

        bytecode_offset = OFST_GLYPH_TABLE
        bytecode_offset += roundup_size(glyph_table_size)
        bytecode_offset += roundup_size(lut_size)
        bytecode_size = blob_size - bytecode_offset
        bytecode_per_glyph = bytecode_size / num_glyphs
        lut_usage_percent = lut_size * 100 / MAX_LUT_SIZE
        total_size = blob_size
        total_size_per_glyph = total_size / num_glyphs

        stats_inst_size = {}
        stats_orig_size = {}
        total_inst_size = 0
        total_orig_size = 0
        num_total_pixels = 0
        for glyph_code in range(first_code, first_code + num_glyphs):
            table_entry_offset = (
                OFST_GLYPH_TABLE + (glyph_code - first_code) * glyph_table_entry_size
            )
            if (
                self.blob[table_entry_offset] == 0xFF
                and self.blob[table_entry_offset + 1] == 0xFF
            ):
                # Ignore missing glyph
                continue

            if shrinked_glyph_table:
                glyph_width = (self.blob[table_entry_offset + 1] & 0xF) + 1
            else:
                glyph_width = (self.blob[table_entry_offset + 2] & 0x3F) + 1

            if vertical_frag:
                glyph_size_in_bytes = glyph_width * math.ceil(glyph_height / 8)
            else:
                glyph_size_in_bytes = math.ceil(glyph_width / 8) * glyph_height

            pc = bytecode_offset
            if shrinked_glyph_table:
                pc += self.blob[table_entry_offset] * ALIGN_SIZE
            else:
                pc += self.blob[table_entry_offset]
                pc += self.blob[table_entry_offset + 1] << 8

            num_remaining_bytes = glyph_size_in_bytes
            while num_remaining_bytes > 0:
                (opr, inst_size, orig_size, params) = parse_instruction(self.blob, pc)

                mne = opr.mnemonic
                if opr == LUD:
                    mne += f" (step={params["step"]})"

                stats_inst_size[mne] = stats_inst_size.get(mne, 0) + inst_size
                stats_orig_size[mne] = stats_orig_size.get(mne, 0) + orig_size
                total_inst_size += inst_size
                total_orig_size += orig_size
                if inst_size <= 0:
                    raise RuntimeError(
                        f"Unknown instruction: 0x{self.blob[pc]:02x} {opr}"
                    )

                pc += inst_size
                num_remaining_bytes -= orig_size

                if pc >= len(self.blob) and num_remaining_bytes != 0:
                    raise RuntimeError(
                        f"Byte code overrun: code=0x{glyph_code:04X}, pc=0x{pc:04X}, last_op={opr}, inst_size={inst_size}, orig_size={orig_size}, params={params}"
                    )

            num_total_pixels += glyph_width * glyph_height
        total_delta_size = total_inst_size - total_orig_size

        pixels_per_byte = num_total_pixels / total_size if total_size > 0 else 0

        code = ""
        code += f"// Generated by {LIB_NAME}\n"
        code += f"//   Format Version: {self.blob[OFST_FORMAT_VERSION]}\n"
        code += f"//   First Code      : {first_code}\n"
        code += f"//   Glyph Count     : {num_glyphs}\n"
        code += f"//   Font Height     : {glyph_height} px\n"
        code += f"//   Max Glyph Width : {max_glyph_width} px\n"
        code += f"//   Total Pixels    : {num_total_pixels} px\n"
        code += (
            f"//   Fragment Shape  : {"Vertical" if vertical_frag else "Horizontal"}\n"
        )
        code += f"//   Bit Order       : {"MSB First" if msb1st else "LSB First"}\n"
        code += f"//   Shrinked Format : {"Yes" if shrinked_glyph_table else "No"}\n"
        code += "//   Estimated Footprint:\n"
        code += f"//     Header        : {OFST_GLYPH_TABLE:4d} Bytes\n"
        code += f"//     Glyph Table   : {glyph_table_size:4d} Bytes ({glyph_table_entry_size} Bytes/glyph)\n"
        code += f"//     Lookup Table  : {lut_size:4d} Bytes ({lut_usage_percent:.2f}% used)\n"
        code += f"//     Bytecodes     : {bytecode_size:4d} Bytes ({bytecode_per_glyph:.2f} Bytes/glyph)\n"
        code += f"//     Total         : {total_size:4d} Bytes ({total_size_per_glyph:.2f} Bytes/glyph)\n"
        code += "//   Compression Performance:\n"
        inst_sorted = sorted(stats_inst_size.keys())
        total_comp_ratio = total_delta_size / total_orig_size * 100
        for inst in inst_sorted:
            inst_size = stats_inst_size[inst]
            orig_size = stats_orig_size[inst]
            delta_size = inst_size - orig_size
            comp_ratio = delta_size / total_orig_size * 100
            code += f"//     {inst:12s}: {orig_size:4d} --> {inst_size:4d} ({comp_ratio:+7.2f}%)\n"
        code += f"//     Total       : {total_orig_size:4d} --> {total_inst_size:4d} ({total_comp_ratio:+7.2f}%)\n"
        code += f"//   Memory Efficiency: {pixels_per_byte:6.3f} px/Byte\n"
        code += "\n"
        code += "#include <stdint.h>\n"
        code += "#include <mamefont/mamefont.hpp>\n"
        code += "\n"
        code += "#ifdef MAMEFONT_USE_PROGMEM\n"
        code += "#include <avr/pgmspace.h>\n"
        code += "#define MAMEFONT_PROGMEM PROGMEM\n"
        code += "#else\n"
        code += "#define MAMEFONT_PROGMEM\n"
        code += "#endif\n"
        code += "\n"
        code += f"const uint8_t {self.name}_blob[] MAMEFONT_PROGMEM = {{\n"

        code += self.generate_c_style_array()

        code += "};\n"
        code += "\n"
        code += f"extern const mamefont::Font {self.name}({self.name}_blob);\n"
        code += "\n"
        code += "#undef MAMEFONT_PROGMEM\n"

        return code

    def generate_json(self) -> str:
        verbose_print(f"[{LIB_NAME}] Generating JSON...")
        code = "{\n"
        code += f'  "name": "{self.name}",\n'
        code += f'  "blob": [\n'
        code += (
            self.generate_c_style_array(with_comment=False, hexadecimal=False)
            .rstrip()
            .rstrip(",")
            + "\n"
        )
        code += f"  ]\n"
        code += "}\n"
        return code


class MameFontBuilder:
    def __init__(
        self,
        name: str,
        glyph_height: int,
        x_spacing: int,
        y_advance: int,
        vertical_frag: bool = False,
        msb1st: bool = False,
    ):
        self.name = name
        self.glyph_height = glyph_height
        self.x_spacing = x_spacing
        self.y_spacing = y_advance - glyph_height
        self.vertical_frag = vertical_frag
        self.msb1st = msb1st
        self.glyphs: dict[int, MameGlyph] = {}

        if vertical_frag:
            if msb1st:
                self.acrh = "VM"
            else:
                self.acrh = "VL"
        else:
            if msb1st:
                self.acrh = "HM"
            else:
                self.acrh = "HL"

        self.next_report_time = time.time() + REPORT_INTERVAL_SEC
        self.report_finished = False

    def add_glyph(
        self,
        code: int,
        bmp: GrayBitmap,
    ):
        fragments = bmp.to_byte_segments(
            vertical_frag=self.vertical_frag,
            msb1st=self.msb1st,
        )

        if VERBOSE:
            print(f"[{self.name}:{self.acrh}] Adding glyph: {format_char(code)}")
            if False:
                print(f"  Fragments:")
                for i, byte in enumerate(fragments):
                    if i % 16 == 0:
                        print("    ", end="")
                    print(f"0x{byte:02x} ", end="")
                    if (i + 1) % 16 == 0 or i == len(fragments) - 1:
                        print()

        fragments.insert(0, 0x00)
        num_bytes = len(fragments)

        verbose_print(f"  Generating Instructions with Dijkstra's algorithm...")
        t_start = time.time()

        class State:
            def __init__(self, i_pos: int):
                self.i_pos = i_pos
                self.next_ops: dict[int, Operation] = {}
                self.best_cost = 999999
                self.best_op: Operation | None = None
                self.best_prev: State | None = None

                # Find next available operations
                for i_next in range(i_pos + 1, len(fragments)):
                    cand = suggest_operation(i_pos, i_next)
                    if cand is not None:
                        self.next_ops[i_next] = cand

        def suggest_operation(i_src: int, i_dst: int) -> Operation | None:
            goal_seq = fragments[i_src + 1 : i_dst + 1]
            best_op: Operation | None = None
            best_op = try_ldi(best_op, i_src, i_dst, goal_seq)
            best_op = try_xor(best_op, i_src, i_dst, goal_seq)
            best_op = try_sft(best_op, i_src, i_dst, goal_seq)
            best_op = try_rpt(best_op, i_src, i_dst, goal_seq)
            best_op = try_cpy(best_op, i_src, i_dst, goal_seq)
            best_op = try_cpx(best_op, i_src, i_dst, goal_seq)
            return best_op

        def try_cpy(
            best_op: Operation | None, i_src: int, i_dst: int, goal_seq: list[int]
        ) -> Operation | None:
            cost_limit = CPY.cost
            if best_op and best_op.cost < cost_limit:
                return best_op

            length = i_dst - i_src
            if length not in CPY_LENGTH.range:
                return best_op

            for byte_reverse in CPY_BYTE_REVERSE.range:
                search_sequence = goal_seq.copy()
                if byte_reverse != 0:
                    search_sequence = search_sequence[::-1]

                for offset in CPY_OFFSET.range:
                    if byte_reverse == 0 and length == 1 and offset == 0:
                        # Reserved for other instructions
                        continue

                    if byte_reverse != 0 and length == 1:
                        # Reserved for other instructions
                        continue

                    i_copy_start = i_src + 1 - length - offset
                    i_copy_end = i_copy_start + length
                    if i_copy_end <= 0:
                        copy_src = [0] * length
                    elif i_copy_start < 0:
                        copy_src = [0] * (-i_copy_start) + fragments[0:i_copy_end]
                    else:
                        copy_src = fragments[i_copy_start:i_copy_end]

                    if copy_src == search_sequence:
                        cost = CPY.cost
                        if byte_reverse != 0:
                            cost += 1

                        inst_code = CPY.code
                        inst_code |= CPY_LENGTH.place(length)
                        inst_code |= CPY_OFFSET.place(offset)
                        inst_code |= CPY_BYTE_REVERSE.place(byte_reverse)
                        return Operation([inst_code], goal_seq, cost)

            return best_op

        def try_cpx(
            best_op: Operation | None, i_src: int, i_dst: int, goal_seq: list[int]
        ) -> Operation | None:
            if best_op and best_op.cost < CPX.cost:
                return best_op

            length = i_dst - i_src
            if length not in CPX_LENGTH.range:
                return best_op

            for byte_reverse, bit_reverse, inverse in product(
                CPX_BYTE_REVERSE.range, CPX_BIT_REVERSE.range, CPX_INVERSE.range
            ):
                search_sequence = goal_seq.copy()
                if byte_reverse != 0:
                    search_sequence = search_sequence[::-1]
                if bit_reverse != 0:
                    for i in range(len(search_sequence)):
                        byte = search_sequence[i]
                        byte = ((byte & 0x0F) << 4) | ((byte & 0xF0) >> 4)
                        byte = ((byte & 0x33) << 2) | ((byte & 0xCC) >> 2)
                        byte = ((byte & 0x55) << 1) | ((byte & 0xAA) >> 1)
                        search_sequence[i] = byte
                if inverse != 0:
                    for i in range(len(search_sequence)):
                        search_sequence[i] = search_sequence[i] ^ 0xFF

                reversal_cost = byte_reverse + bit_reverse * 2

                # from recent sequence
                for offset in range(min(i_src + length + 2, 1 << CPX_OFFSET_BITS)):
                    i_copy_start = i_src + 1 - offset
                    i_copy_end = i_copy_start + length

                    if i_copy_end > i_src:
                        continue

                    if i_copy_end <= 0:
                        copy_src = [0] * length
                    elif i_copy_start < 0:
                        copy_src = [0] * (-i_copy_start) + fragments[0:i_copy_end]
                    else:
                        copy_src = fragments[i_copy_start:i_copy_end]

                    if copy_src == search_sequence:
                        byte2 = offset & 0xFF

                        byte3 = 0
                        byte3 |= CPX_OFFSET_H.place(offset >> 8)
                        byte3 |= CPX_LENGTH.place(length)
                        byte3 |= CPX_BYTE_REVERSE.place(byte_reverse)
                        byte3 |= CPX_BIT_REVERSE.place(bit_reverse)
                        byte3 |= CPX_INVERSE.place(inverse)

                        cost = CPX.cost + reversal_cost

                        return Operation([CPX.code, byte2, byte3], goal_seq, cost)

            return best_op

        def try_ldi(
            best_op: Operation | None, i_src: int, i_dst: int, goal_seq: list[int]
        ) -> Operation | None:
            if best_op and best_op.cost < LDI.cost:
                return best_op
            if i_src + 1 != i_dst:
                return best_op
            return Operation([LDI.code, fragments[i_dst]], goal_seq, LDI.cost)

        def try_sft(
            best_op: Operation | None, i_src: int, i_dst: int, goal_seq: list[int]
        ) -> Operation | None:
            if best_op and best_op.cost < SFT.cost:
                return best_op

            repeat_count = i_dst - i_src
            if repeat_count not in SFT_REPEAT_COUNT.range:
                return best_op

            for shift_dir, shift_size, post_op in product(
                SFT_SHIFT_DIR.range, SFT_SHIFT_SIZE.range, SFT_POST_OP.range
            ):
                fail = False
                modifier = (1 << shift_size) - 1
                if shift_dir != 0:
                    modifier <<= 8 - shift_size
                if post_op == 0:
                    modifier = modifier ^ 0xFF

                work = fragments[i_src]
                for i_step in range(i_src, i_dst):
                    if shift_dir == ShiftDir.LEFT:
                        work = work << shift_size
                    else:
                        work = work >> shift_size
                    if post_op == ShiftPostOp.SET:
                        work |= modifier
                    else:
                        work &= modifier
                    if work != fragments[i_step + 1]:
                        fail = True
                        break

                if fail:
                    continue

                inst_code = SFT.code
                inst_code |= SFT_SHIFT_DIR.place(shift_dir)
                inst_code |= SFT_SHIFT_SIZE.place(shift_size)
                inst_code |= SFT_POST_OP.place(post_op)
                inst_code |= SFT_REPEAT_COUNT.place(repeat_count)
                return Operation([inst_code], goal_seq, SFT.cost)

            return best_op

        def try_rpt(
            best_op: Operation | None, i_src: int, i_dst: int, goal_seq: list[int]
        ) -> Operation | None:
            if best_op and best_op.cost < RPT.cost:
                return best_op

            repeat_count = i_dst - i_src
            if repeat_count not in RPT_REPEAT_COUNT.range:
                return best_op

            for i in range(repeat_count):
                if fragments[i_src] != goal_seq[i]:
                    return best_op

            inst_code = RPT.code | (repeat_count - 1)
            return Operation([inst_code], goal_seq, RPT.cost)

        def try_xor(
            best_op: Operation | None, i_src: int, i_dst: int, goal_seq: list[int]
        ) -> Operation | None:
            if best_op and best_op.cost < XOR.cost:
                return best_op

            if i_src + 1 != i_dst:
                return best_op

            mask_width_range = range(1, 2)
            mask_pos_range = range(0, 8)

            for mask_width, mask_pos in product(mask_width_range, mask_pos_range):
                mask = (1 << mask_width) - 1
                mask <<= mask_pos
                if fragments[i_src] ^ mask == fragments[i_dst]:
                    inst_code = XOR.code | ((mask_width - 1) << 3) | mask_pos
                    return Operation([inst_code], goal_seq, XOR.cost)

            return best_op

        # Solve with Dijkstra's algorithm
        nodes = [State(i) for i in range(num_bytes)]

        if False and VERBOSE:
            print(f"   ", end="")
            for frag in fragments:
                print(f"   {frag:02X}", end="")
            print()

        def dump_nodes():
            if True or not VERBOSE:
                return

            node_indexes = list(range(num_bytes))
            while len(node_indexes) > 0:
                aa_empty_str = "|    "
                aa_line: list[str] = []
                for _ in range(num_bytes):
                    aa_line.append(aa_empty_str)
                aa_changed = False

                i_byte = num_bytes - 1
                while i_byte >= 0:
                    if i_byte not in node_indexes:
                        i_byte -= 1
                        continue

                    node_indexes.remove(i_byte)
                    node = nodes[i_byte]
                    if not node.best_prev:
                        i_byte -= 1
                        continue

                    prev = node.best_prev
                    op = node.best_op

                    not_empty = False
                    for i in range(prev.i_pos, node.i_pos):
                        if aa_line[i] != aa_empty_str:
                            not_empty = True
                            break
                    if not_empty:
                        i_byte -= 1
                        continue

                    for i in range(prev.i_pos, node.i_pos):
                        if i == prev.i_pos:
                            arrow = op.operator().mnemonic + "-"
                        else:
                            arrow = "----"
                        if i == node.i_pos - 1:
                            arrow += ">"
                        else:
                            arrow += "-"
                        aa_line[i] = arrow

                    aa_changed = True

                    i_byte = prev.i_pos

                if not aa_changed:
                    break

                print(f"      {"".join(aa_line)}")

        q = nodes.copy()
        q[0].best_cost = 0
        for i in range(1, num_bytes):
            q[i].best_cost = 999999
        while len(q) > 0:
            q.sort(key=lambda n: n.best_cost)
            curr = q.pop(0)

            if curr.best_cost == 999999:
                # No more reachable states
                raise RuntimeError()

            changed = False
            for i_next, op in curr.next_ops.items():
                next_cost = curr.best_cost + op.cost
                if next_cost < nodes[i_next].best_cost:
                    nodes[i_next].best_cost = next_cost
                    nodes[i_next].best_prev = curr
                    nodes[i_next].best_op = op
                    changed = True

            if changed:
                dump_nodes()

        # Construct the bytecode from the last node
        ops: list[Operation] = []
        curr = nodes[-1]
        while curr is not None:
            if curr.best_op is None:
                if curr.i_pos == 0:
                    break
                raise RuntimeError()
            ops.insert(0, curr.best_op)
            curr = curr.best_prev

        t_elapsed = time.time() - t_start
        verbose_print(
            f"    {len(ops)} instructions generated ({t_elapsed * 1000:.2f} ms)."
        )

        self.glyphs[code] = MameGlyph(
            code=code,
            operations=ops,
            glyphWidth=bmp.width,
            x_spacing=self.x_spacing,
        )

        now = time.time()
        if now >= self.next_report_time:
            print(f"[{self.name}:{self.acrh}] {len(self.glyphs)} glyphs added.")
            self.next_report_time = min(
                now + REPORT_INTERVAL_SEC, self.next_report_time + REPORT_INTERVAL_SEC
            )
            self.report_finished = True

    def build(self) -> MameGlyph:
        format_version = 1

        codes = sorted(self.glyphs.keys())

        # Generate Lookup Table
        verbose_print(f"[{self.name}:{self.acrh}] Generating Lookup Table...")
        byte_ref_count: dict[int, int] = {}
        for code in codes:
            glyph = self.glyphs[code]
            for op in glyph.operations:
                if LDI.match(op.bytecode[0]):
                    this_byte = op.bytecode[1]
                    byte_ref_count[this_byte] = byte_ref_count.get(this_byte, 0) + 1
        lut = sorted(
            byte_ref_count.keys(), key=lambda item: byte_ref_count[item], reverse=True
        )
        if len(lut) > MAX_LUT_SIZE:
            verbose_print(
                f"  Lookup Table shrunk: {len(lut)} --> {MAX_LUT_SIZE} bytes."
            )
            lut = lut[:MAX_LUT_SIZE]

        verbose_print(f"[{self.name}:{self.acrh}] Optimizing Lookup Table...")
        verbose_print("  Detecting frequent two-byte sequences...")
        byte_seq_count: dict[int, dict[int, int]] = {}
        for byte1 in lut:
            byte_seq_count[byte1] = {}
            for byte2 in lut:
                byte_seq_count[byte1][byte2] = 0
        for code in codes:
            glyph = self.glyphs[code]
            byte1 = -1
            for op in glyph.operations:
                if len(op.orig_seq) == 1 and op.orig_seq[0] in lut:
                    byte2 = op.orig_seq[0]
                    if byte1 >= 0:
                        byte_seq_count[byte1][byte2] += 1
                    byte1 = byte2

        verbose_print("  Detecting most referenced bytes...")
        byte_ref_by_seq_count: dict[int, int] = {}
        for byte in lut:
            byte_ref_by_seq_count[byte] = 0
        for byte1, dic in byte_seq_count.items():
            for byte2, count in dic.items():
                byte_ref_by_seq_count[byte1] += 1
                byte_ref_by_seq_count[byte2] += 1

        most_freq_byte_seq: list[tuple[int, int]] = []
        for byte1, dic in byte_seq_count.items():
            for byte2, count in dic.items():
                most_freq_byte_seq.append((byte1, byte2))
        most_freq_byte_seq = sorted(
            most_freq_byte_seq,
            key=lambda item: byte_seq_count[item[0]][item[1]],
            reverse=True,
        )

        if VERBOSE:
            print("  Most frequent two-byte sequences:")

            for seq in most_freq_byte_seq[:10]:
                (byte1, byte2) = seq
                count = byte_seq_count[byte1][byte2]
                print(f"    {byte1:02X}-->{byte2:02X} : {count:4}")
            print("  Most referenced bytes in sequences:")
            tmp = sorted(
                byte_ref_by_seq_count.items(), key=lambda item: item[1], reverse=True
            )
            for byte in tmp[:10]:
                (key, count) = byte
                print(f"    {key:02X} : {count:4}")

        def report_lut_score():
            if not VERBOSE:
                return
            tmp = lut[:16]

            byte1 = -1
            rpt_count = []
            seq_count = []
            total_score = 0
            print("    Content    :", end="")
            for byte2 in tmp:
                byte_score = byte_seq_count[byte2][byte2]
                rpt_count.append(byte_score)

                seq_score = 0
                if byte1 >= 0:
                    seq_score += byte_seq_count[byte1][byte2]
                byte1 = byte2
                seq_count.append(seq_score)

                total_score += byte_score + seq_score

                print("-->" if seq_score > 0 else "   ", end="")
                print(f"{byte2:02X}", end="")
            print()

            print("    Byte Score :", end="")
            for score in rpt_count:
                if score > 0:
                    print(f"{score:5d}", end="")
                else:
                    print("     ", end="")
            print()

            print("    Seq. Score :", end="")
            for score in seq_count:
                if score > 0:
                    print(f"{score:5d}", end="")
                else:
                    print("     ", end="")
            print()

            print(f"    Potential Effect of LUD: {total_score} ")

        # Reorder LUT
        if VERBOSE:
            print("  LUT Before Reorder:")
            report_lut_score()
            print("  Reordering LUT...")

        class LutSeq:
            def __init__(self, seq: list[int], frozen: bool = False):
                self.array = seq
                self.frozen = frozen

            def __repr__(self):
                return f"{'*' if self.frozen else ' '}[{' '.join(f'{b:02X}' for b in self.array)}]"

        # Place consecutive bytes next to each other
        seq_buff: list[LutSeq] = []
        seq_buff_size = 0
        head_frozen = False
        for byte1, byte2 in most_freq_byte_seq:
            if byte_seq_count[byte1][byte2] <= 0:
                break

            changed = False
            if byte1 in lut and byte2 not in lut:
                for seq in seq_buff:
                    if seq.array[0] == byte2:
                        if not seq.frozen:
                            lut.remove(byte1)
                            seq.array.insert(0, byte1)
                            seq_buff_size += 1
                            changed = True
                        break
            elif byte1 not in lut and byte2 in lut:
                for seq in seq_buff:
                    if seq.array[-1] == byte1:
                        if not seq.frozen:
                            lut.remove(byte2)
                            seq.array.append(byte2)
                            seq_buff_size += 1
                            changed = True
                        break
            elif byte1 in lut and byte2 in lut:
                if byte1 == byte2:
                    lut.remove(byte1)
                    seq_buff.append(LutSeq([byte1]))
                    seq_buff_size += 1
                else:
                    lut.remove(byte1)
                    lut.remove(byte2)
                    seq_buff.append(LutSeq([byte1, byte2]))
                    seq_buff_size += 2
                changed = True
            else:
                seq1 = None
                for seq in seq_buff:
                    if seq.array[-1] == byte1 and not seq.frozen:
                        seq1 = seq
                        break
                seq2 = None
                for seq in seq_buff:
                    if seq.array[0] == byte2 and not seq.frozen:
                        seq2 = seq
                        break
                if seq1 and seq2 and seq1 != seq2:
                    ins_pos = min(seq_buff.index(seq1), seq_buff.index(seq2))
                    seq_buff.remove(seq1)
                    seq_buff.remove(seq2)
                    seq_buff.insert(ins_pos, LutSeq(seq1.array + seq2.array))
                    changed = True

            if not changed:
                continue

            if seq_buff_size > LUD_INDEX.max and not head_frozen:
                for seq in seq_buff:
                    seq.frozen = True
                head_frozen = True

            if VERBOSE:
                print("    ", end="")
                for seq in seq_buff:
                    print(f"{seq} ", end="")
                print()

        new_lut = []
        for seq in seq_buff:
            new_lut += seq.array
        lut = new_lut + lut

        # Replace instructions with LUP as possible
        for code in codes:
            glyph = self.glyphs[code]
            for op in glyph.operations:
                if len(op.orig_seq) == 1 and op.orig_seq[0] in lut:
                    index = lut.index(op.orig_seq[0])
                    op.bytecode = [LUP.code | index]

        # Replace instructions with LUD as possible
        verbose_print("  Replacing instructions LUP --> LUD as possible...")
        for code in codes:
            glyph = self.glyphs[code]
            index1 = -1

            i_op = 0
            while i_op < len(glyph.operations):
                op = glyph.operations[i_op]

                index2 = -1
                if LUP.match(op.bytecode[0]):
                    index2 = op.bytecode[0] & 0x3F

                lud_applicable = (
                    index1 >= 0
                    and index2 >= 0
                    and index1 in LUD_INDEX.range
                    and (index1 == index2 or index1 + 1 == index2)
                )
                if lud_applicable:
                    step = 0 if index1 == index2 else 1
                    inst_code = LUD.code | index1 | (step << 4)
                    glyph.operations[i_op - 1].bytecode = [inst_code]
                    glyph.operations.remove(op)
                    index1 = -1
                    continue

                index1 = index2
                i_op += 1

        if VERBOSE:
            print("  LUT After Reorder:")
            report_lut_score()

        # Align LUT to 2-byte boundary
        while len(lut) % ALIGN_SIZE != 0 or len(lut) == 0:
            lut.append(0x00)

        # Determine to apply Shrinked Glyph Table or not
        shrinked_glyph_table = True
        cannot_shrink_reason = ""
        total_bytecode_size = 0
        for code in codes:
            # Check glyph dimensions
            glyph = self.glyphs[code]
            if glyph.glyph_width not in GLYPH_SHRINKED_DIM_WIDTH.range:
                shrinked_glyph_table = False
                cannot_shrink_reason = "Glyph width is out of range."
                break
            if glyph.x_spacing not in GLYPH_SHRINKED_DIM_X_SPACING.range:
                shrinked_glyph_table = False
                cannot_shrink_reason = "X spacing is out of range."
                break

            # Check bytecode size
            for op in glyph.operations:
                total_bytecode_size += len(op.bytecode)
            while total_bytecode_size % ALIGN_SIZE != 0:
                total_bytecode_size += 1
            if total_bytecode_size > (ALIGN_SIZE * 256):
                shrinked_glyph_table = False
                cannot_shrink_reason = "Total bytecode size is out of range."
                break

        if shrinked_glyph_table:
            verbose_print(f"[{self.name}:{self.acrh}] Applying Shrinked Glyph Table format.")
        else:
            verbose_print(f"[{self.name}:{self.acrh}] Shrinked Glyph Table format cannot be applied because: {cannot_shrink_reason}")

        # Construct bytecode block
        verbose_print(f"[{self.name}:{self.acrh}] Constructing bytecode block...")
        bytecodes: list[int] = []
        for code in codes:
            if False:
                verbose_print(f"  {format_char(code)}:")
            glyph = self.glyphs[code]
            glyph.entry_point = len(bytecodes)
            for op in glyph.operations:
                if False and VERBOSE:
                    inst_code_str = " ".join(f"0x{b:02X}" for b in op.bytecode)
                    print(f"    {inst_code_str:<10s} {op}")
                bytecodes += op.bytecode
            if shrinked_glyph_table:
                while len(bytecodes) % ALIGN_SIZE != 0:
                    bytecodes.append(ABO.code)

        for _ in range(3):
            bytecodes.append(ABO.code)

        verbose_print(f"[{self.name}:{self.acrh}] Generating blob...")
        if shrinked_glyph_table:
            verbose_print("  Using Shrinked Glyph Table format.")
        else:
            verbose_print("  Using Normal Glyph Table format.")

        code_first = codes[0]
        code_last = codes[-1]

        max_glyph_width = 1
        for glyph in self.glyphs.values():
            if glyph.glyph_width > max_glyph_width:
                max_glyph_width = glyph.glyph_width

        font_dimension_0 = FONT_DIM_FONT_HEIGHT.place(self.glyph_height)
        font_dimension_1 = FONT_DIM_Y_SPACING.place(self.y_spacing)
        font_dimension_2 = FONT_DIM_MAX_GLYPH_WIDTH.place(max_glyph_width)

        font_flags = 0
        if self.vertical_frag:
            font_flags |= 0x80
        if self.msb1st:
            font_flags |= 0x40
        if shrinked_glyph_table:
            font_flags |= 0x20

        blob: list[int] = []

        # Font Header
        blob.append(format_version)
        blob.append(font_flags)
        blob.append(code_first)
        blob.append(code_last - code_first)
        blob.append(len(lut) - 1)
        blob.append(font_dimension_0)
        blob.append(font_dimension_1)
        blob.append(font_dimension_2)

        # Glyph Table
        for code in range(code_first, code_last + 1):
            if code not in self.glyphs:
                # Dummy Entry for missing glyphs
                if shrinked_glyph_table:
                    blob.append(0xFF)
                    blob.append(0xFF)
                else:
                    blob.append(0xFF)
                    blob.append(0xFF)
                    blob.append(0xFF)
                    blob.append(0xFF)
                continue

            glyph = self.glyphs[code]
            if shrinked_glyph_table:
                shrinked_glyph_dim = 0
                shrinked_glyph_dim |= GLYPH_SHRINKED_DIM_WIDTH.place(glyph.glyph_width)
                shrinked_glyph_dim |= GLYPH_SHRINKED_DIM_X_SPACING.place(
                    glyph.x_spacing
                )
                blob.append((glyph.entry_point // 2) & 0xFF)
                blob.append(shrinked_glyph_dim)
            else:
                glyph_dim_0 = GLYPH_DIM_WIDTH.place(glyph.glyph_width)
                glyph_dim_1 = GLYPH_DIM_X_SPACING.place(glyph.x_spacing)
                blob.append(glyph.entry_point & 0xFF)
                blob.append((glyph.entry_point >> 8) & 0xFF)
                blob.append(glyph_dim_0)
                blob.append(glyph_dim_1)

        while len(blob) % 2 != 0:
            blob.append(0x00)

        # LUT
        blob += lut

        # Bytecode
        blob += bytecodes

        result = MameFont(name=self.name, blob=blob)

        if self.report_finished:
            print(f"[{self.name}:{self.acrh}] Build succeeded")

        return result
