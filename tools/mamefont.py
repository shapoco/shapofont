import enum
from design import GrayBitmap
from itertools import product

OFST_FORMAT_VERSION = 0
OFST_FIRST_CODE = 1
OFST_GLYPH_TABLE_LEN = 2
OFST_LUT_SIZE = 3
OFST_FONT_DIMENSION_0 = 4
OFST_FONT_DIMENSION_1 = 5
OFST_FONT_FLAGS = 6
OFST_GLYPH_TABLE = 8
GLYPH_TABLE_ENTRY_SIZE = 4
OFST_ENTRY_POINT = 0
OFST_GLYPH_DIMENSION = 2

SHIFT_MAX_SIZE = 4
SHIFT_MAX_REPEAT = 4
REPEAT_MAX = 16
COPY_MAX_LENGTH = 16

MAX_LUT_SIZE = 64

VERBOSE = True


def format_char(c: int) -> str:
    if c >= 0x20 and c <= 0x7E:
        return f"'{chr(c)}' (0x{c:x})"
    else:
        return f"\\x{c:02x}"


def verbose_print(s: str = "") -> None:
    print(s)


class OpCode(enum.IntEnum):
    LKP = 0x00
    SLC = 0x40
    SLS = 0x50
    SRC = 0x60
    SRS = 0x70
    CPY = 0x80
    LDI = 0xC0
    REV = 0xC1
    RPT = 0xE0
    XOR = 0xF0
    HDR = -1


costs = {
    OpCode.RPT: 10001,
    OpCode.XOR: 10002,
    OpCode.SLC: 10003,
    OpCode.SRC: 10003,
    OpCode.SLS: 10003,
    OpCode.SRS: 10003,
    OpCode.CPY: 10004,
    OpCode.REV: 10005,
    OpCode.LKP: 10006,
    OpCode.LDI: 10007,
}


class ScanDirection(enum.IntEnum):
    HORIZONTAL = 0
    VERTICAL = 1


class ShiftDir(enum.IntEnum):
    LEFT = 0
    RIGHT = 1


class ShiftPostOp(enum.IntEnum):
    CLR = 0
    SET = 1


class Operation:
    def __init__(self, microcode: list[int], cost: float):
        self.microcode = microcode
        self.cost = cost

    def __repr__(self) -> str:
        ret = ""
        op_code = self.microcode[0]
        if (op_code & 0xC0) == OpCode.LKP:
            index = op_code & 0x3F
            ret += f"LKP({index})"
        elif (op_code & 0xC0) == OpCode.SLC:
            shift_size = (op_code & 0x0C) >> 2
            repeat_count = op_code & 0x03
            if (op_code & 0xF0) == OpCode.SLC:
                ret += "SLC"
            elif (op_code & 0xF0) == OpCode.SLS:
                ret += "SLS"
            elif (op_code & 0xF0) == OpCode.SRC:
                ret += "SRC"
            elif (op_code & 0xF0) == OpCode.SRS:
                ret += "SRS"
            ret += f"({shift_size + 1}, {repeat_count + 1})"
        elif (op_code & 0xC0) == OpCode.CPY:
            ret += "CPY"
        elif op_code == 0xC0:
            ret += f"LDI(0x{self.microcode[1]:02x})"
        elif (op_code & 0xE0) == OpCode.REV:
            ret += "REV"
        elif (op_code & 0xF0) == OpCode.RPT:
            ret += "RPT"
        elif op_code == 0xFF:
            ret += "(reserved)"
        else:
            ret += "XOR"

        return ret


class MameGlyph:
    def __init__(
        self, code: int, operations: list[Operation], glyphWidth: int, x_advance: int
    ):
        self.code = code
        self.operations = operations
        self.glyphWidth = glyphWidth
        self.x_advance = x_advance
        self.entry_point = 0xFFFF


class MameFont:
    def __init__(self, name: str, blob: list[int]):
        self.name = name
        self.blob = blob

    def generate_header(self) -> str:
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

    def generate_source(self) -> str:
        num_glyphs = self.blob[OFST_GLYPH_TABLE_LEN]
        glyph_table_size = num_glyphs * GLYPH_TABLE_ENTRY_SIZE
        microcode_size = (
            len(self.blob)
            - self.blob[OFST_LUT_SIZE]
            - glyph_table_size
            - OFST_GLYPH_TABLE
        )
        microcode_per_glyph = microcode_size / num_glyphs
        lut_size = self.blob[OFST_LUT_SIZE]
        lut_usage_percent = lut_size * 100 / MAX_LUT_SIZE
        total_size = len(self.blob)
        total_size_per_glyph = total_size / num_glyphs

        code = ""
        code += "// Generated from ShapoFont\n"
        code += f"//   Format Version: {self.blob[OFST_FORMAT_VERSION]}\n"
        code += f"//   First Code    : {self.blob[OFST_FIRST_CODE]}\n"
        code += f"//   Glyph Count   : {num_glyphs}\n"
        code += "//   Estimated Footprint:\n"
        code += f"//     Header        : {OFST_GLYPH_TABLE:4d} Bytes\n"
        code += f"//     Glyph Table   : {glyph_table_size:4d} Bytes\n"
        code += f"//     Lookup Table  : {lut_size:4d} Bytes ({lut_usage_percent:.2f}% used)\n"
        code += f"//     Microcodes    : {microcode_size:4d} Bytes ({microcode_per_glyph:.2f} Bytes/glyph)\n"
        code += f"//     Total         : {total_size:4d} Bytes ({total_size_per_glyph:.2f} Bytes/glyph)\n"
        code += "\n"
        code += "#include <stdint.h>\n"
        code += "#include <mamefont/mamefont.hpp>\n"
        code += "\n"
        code += f"static const uint8_t {self.name}_blob[] = {{\n"

        cols = 16
        i_col = 0
        i_start_of_header = 0
        i_start_of_glyph_table = OFST_GLYPH_TABLE
        i_start_of_lut = OFST_GLYPH_TABLE + glyph_table_size
        i_start_of_microcodes = OFST_GLYPH_TABLE + glyph_table_size + lut_size

        for i, b in enumerate(self.blob):
            if i == i_start_of_header:
                code += "  // Font Header\n"
            if i == i_start_of_glyph_table:
                code += "  // Glyph Table\n"
            if i == i_start_of_lut:
                code += "  // Lookup Table\n"
            if i == i_start_of_microcodes:
                code += "  // Microcodes\n"

            if i_col == 0:
                code += "  "
            code += f"0x{b:02X},"

            is_end_of_section = (
                i_col == cols - 1
                or i == i_start_of_glyph_table - 1
                or i == i_start_of_lut - 1
                or i == i_start_of_microcodes - 1
                or i == len(self.blob) - 1
            )

            if is_end_of_section:
                code += "\n"
                i_col = 0
            else:
                code += " "
                i_col += 1

        code += "};\n"
        code += "\n"
        code += f"extern const mamefont::Font {self.name}({self.name}_blob);\n"
        code += "\n"

        return code


class MameFontBuilder:
    def __init__(
        self,
        name: str,
        glyph_height: int,
        x_spacing: int,
        y_advance: int,
    ):
        self.name = name
        self.glyph_height = glyph_height
        self.x_spacing = x_spacing
        self.y_advance = y_advance
        self.vertical_scan = False
        self.bit_reverse = False
        self.glyphs: dict[int, MameGlyph] = {}

    def add_glyph(
        self,
        code: int,
        bmp: GrayBitmap,
    ):
        segments = bmp.to_byte_segments(
            vertical_scan=self.vertical_scan,
            bit_reverse=self.bit_reverse,
        )
        segments.insert(0, 0x00)  # pivot segment

        num_segments = len(segments)

        if VERBOSE:
            print(f"Compiling: {format_char(code)}")
            print(f"  segs: ", end="")
            for seg in segments:
                print(f"0x{seg:02x}", end=" ")
            print()

        class State:
            def __init__(self, i_pos: int):
                self.i_pos = i_pos
                self.next_ops: dict[int, Operation] = {}
                self.best_cost = 999999
                self.best_op: Operation | None = None
                self.best_prev: State | None = None

                # Find next available operations
                for i_next in range(i_pos + 1, len(segments)):
                    cand = suggest_operation(i_pos, i_next)
                    if cand is not None:
                        self.next_ops[i_next] = cand

        def suggest_operation(i_src: int, i_dst: int) -> Operation | None:
            cands: list[Operation] = []
            cands += try_ldi(i_src, i_dst)
            cands += try_shift(i_src, i_dst)
            cands += try_rpt(i_src, i_dst)
            cands += try_xor(i_src, i_dst)
            cands += try_cpy(i_src, i_dst)

            best_cand: Operation | None = None
            best_cost = float("inf")

            for cand in cands:
                if cand.cost < best_cost:
                    best_cost = cand.cost
                    best_cand = cand

            return best_cand

        def try_cpy(i_src: int, i_dst: int) -> list[Operation]:
            length = i_dst - i_src
            if length < 1 or length > COPY_MAX_LENGTH:
                return []

            offset_range = range(0, 4)

            for offset in offset_range:
                if i_src - length - offset < 0:
                    continue

                success = True
                for i in range(i_src + 1, i_dst + 1):
                    if segments[i - length - offset] != segments[i]:
                        success = False
                        break

                if success:
                    op_code = OpCode.CPY
                    op_code |= offset << 4
                    op_code |= length - 1
                    cost = costs[OpCode.CPY]
                    return [Operation([op_code], cost)]

            return []

        def try_ldi(i_src: int, i_dst: int) -> list[Operation]:
            if i_src + 1 == i_dst:
                op_code = OpCode.LDI
                cost = costs[op_code]
                return [Operation([op_code, segments[i_dst]], cost)]
            else:
                return []

        def try_shift(i_src: int, i_dst: int) -> list[Operation]:
            repeat_count = i_dst - i_src
            if repeat_count < 1 or repeat_count > SHIFT_MAX_REPEAT:
                return []

            shift_dir_range = [ShiftDir.LEFT, ShiftDir.RIGHT]
            shift_size_range = range(1, SHIFT_MAX_SIZE + 1)
            post_op_range = [ShiftPostOp.CLR, ShiftPostOp.SET]

            for shift_dir, shift_size, post_op in product(
                shift_dir_range, shift_size_range, post_op_range
            ):
                success = True
                modifier = (1 << shift_size) - 1
                if shift_dir != 0:
                    modifier <<= 8 - shift_size
                if post_op == 0:
                    modifier = modifier ^ 0xFF

                work = segments[i_src]
                for i_step in range(i_src, i_dst):
                    if shift_dir == ShiftDir.LEFT:
                        work = work << shift_size
                    else:
                        work = work >> shift_size
                    if post_op == ShiftPostOp.SET:
                        work |= modifier
                    else:
                        work &= modifier
                    if work != segments[i_step + 1]:
                        success = False
                        break

                if success:
                    if shift_dir == ShiftDir.LEFT:
                        if post_op == ShiftPostOp.CLR:
                            op_code = OpCode.SLC
                        else:
                            op_code = OpCode.SLS
                    else:
                        if post_op == ShiftPostOp.CLR:
                            op_code = OpCode.SRC
                        else:
                            op_code = OpCode.SRS
                    cost = costs[op_code]
                    op_code |= (shift_size - 1) << 2
                    op_code |= repeat_count - 1
                    return [Operation([op_code], cost)]

            return []

        def try_rpt(i_src: int, i_dst: int) -> list[Operation]:
            repeat_count = i_dst - i_src
            if repeat_count < 1 or repeat_count > REPEAT_MAX:
                return []

            work = segments[i_src]
            for i_step in range(i_src, i_dst):
                if segments[i_src] != segments[i_step + 1]:
                    return []

            op_code = OpCode.RPT | (repeat_count - 1)
            cost = costs[OpCode.RPT]
            return [Operation([op_code], cost)]

        def try_xor(i_src: int, i_dst: int) -> list[Operation]:
            if i_src + 1 != i_dst:
                return []

            mask_width_range = range(1, 2)
            mask_pos_range = range(0, 8)

            for mask_width, mask_pos in product(mask_width_range, mask_pos_range):
                mask = (1 << mask_width) - 1
                mask <<= mask_pos
                if segments[i_src] ^ mask == segments[i_dst]:
                    op_code = OpCode.XOR
                    op_code |= (mask_width - 1) << 3
                    op_code |= mask_pos
                    cost = costs[OpCode.XOR]
                    return [Operation([op_code], cost)]

            return []

        # Solve with Dijkstra's algorithm
        nodes = [State(i) for i in range(num_segments)]
        q = nodes.copy()
        q[0].best_cost = 0
        for i in range(1, num_segments):
            q[i].best_cost = 999999
        while len(q) > 0:
            q.sort(key=lambda n: n.best_cost)
            curr = q.pop(0)

            if curr.best_cost == 999999:
                # No more reachable states
                raise RuntimeError()

            for i_next, op in curr.next_ops.items():
                next_cost = curr.best_cost + op.cost
                if nodes[i_next].best_cost > next_cost:
                    nodes[i_next].best_cost = next_cost
                    nodes[i_next].best_prev = curr
                    nodes[i_next].best_op = op

        # Construct the microcode from the last node
        ops: list[Operation] = []
        curr = nodes[-1]
        while curr is not None:
            if curr.best_op is None:
                if curr.i_pos == 0:
                    break
                raise RuntimeError()
            ops.insert(0, curr.best_op)
            curr = curr.best_prev

        if VERBOSE:
            print("  ops: ", end="")
            for op in ops:
                print(op, end=" ")
            print()

        self.glyphs[code] = MameGlyph(
            code=code,
            operations=ops,
            glyphWidth=bmp.width,
            x_advance=bmp.width + self.x_spacing,
        )

    def build(self) -> MameGlyph:
        format_version = 1

        codes = sorted(self.glyphs.keys())

        # Generate Lookup Table
        segment_count: dict[int, int] = {}
        for code in codes:
            glyph = self.glyphs[code]
            for op in glyph.operations:
                if op.microcode[0] == OpCode.LDI:
                    seg = op.microcode[1]
                    segment_count[seg] = segment_count.get(seg, 0) + 1
        lut = sorted(
            segment_count.keys(), key=lambda item: segment_count[item], reverse=True
        )
        if len(lut) > MAX_LUT_SIZE:
            lut = lut[:MAX_LUT_SIZE]

        microcodes: list[int] = []
        for code in codes:
            glyph = self.glyphs[code]
            print(
                f"code: {format_char(code)}, glyph.width: {glyph.glyphWidth}, x_advance: {glyph.x_advance}"
            )
            glyph.entry_point = len(microcodes)
            for op in glyph.operations:
                # Replace LDI with LKP if the segment is in the LUT
                if op.microcode[0] == OpCode.LDI:
                    seg = op.microcode[1]
                    if seg in lut:
                        op.microcode = [OpCode.LKP | lut.index(seg)]
                # Append microcode
                microcodes += op.microcode

        code_first = codes[0]
        code_last = codes[-1]

        font_dimension_0 = self.glyph_height & 0x3F
        font_dimension_1 = self.y_advance & 0x3F
        font_flags = 0
        if self.vertical_scan:
            font_flags |= 0x80
        if self.bit_reverse:
            font_flags |= 0x40

        blob: list[int] = []

        # Font Header
        blob.append(format_version)
        blob.append(code_first)
        blob.append(code_last - code_first + 1)
        blob.append(len(lut))
        blob.append(font_dimension_0)
        blob.append(font_dimension_1)
        blob.append(0)  # reserved flags
        blob.append(font_flags)

        # Glyph Table
        for code in codes:
            glyph = self.glyphs[code]
            glyph_dimension_0 = glyph.glyphWidth & 0x3F
            glyph_dimension_1 = glyph.x_advance & 0x3F

            blob.append(glyph.entry_point & 0xFF)
            blob.append((glyph.entry_point >> 8) & 0xFF)
            blob.append(glyph_dimension_0)
            blob.append(glyph_dimension_1)

        # LUT
        blob += lut

        # Microcode
        blob += microcodes

        return MameFont(name=self.name, blob=blob)
