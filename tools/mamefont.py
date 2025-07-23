import enum
from design import GrayBitmap
from itertools import product
import time
import math

LIB_NAME = "MameFont"

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
COPY_MAX_LENGTH = 8

MAX_LUT_SIZE = 64
LUD_INDEX_RANGE = 16

VERBOSE = True


def format_char(c: int) -> str:
    if c >= 0x20 and c <= 0x7E:
        return f"'{chr(c)}' (0x{c:x})"
    else:
        return f"\\x{c:02x}"


def verbose_print(s: str = "") -> None:
    if VERBOSE:
        print(s)


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
CPY = Operator("CPY", 0xA0, [(0xA1, 0xBF)], 1002)
REV = Operator("REV", 0xC0, [(0xC1, 0xCF), (0xD1, 0xDF)], 1003)
XOR = Operator("XOR", 0xF0, [(0xF0, 0xFE)], 1004)
SLC = Operator("SLC", 0x40, [(0x40, 0x4F)], 1005)
SLS = Operator("SLS", 0x50, [(0x50, 0x5F)], 1005)
SRC = Operator("SRC", 0x60, [(0x60, 0x6F)], 1005)
SRS = Operator("SRS", 0x70, [(0x70, 0x7F)], 1005)
LUS = Operator("LUS", 0x00, [(0x00, 0x3F)], 1006)
LUD = Operator("LUD", 0x80, [(0x80, 0x9F)], 1006)
LDI = Operator("LDI", 0xA0, [(0xA0, 0xA0)], 1009)
UNKNOWN = Operator("(unknown)", -1, [], 999999)

opcodes = [
    RPT,
    CPY,
    REV,
    XOR,
    SLC,
    SLS,
    SRC,
    SRS,
    LUS,
    LUD,
    LDI,
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
    microcode: list[int], offset: int
) -> tuple[Operator, int, int, dict[str, int]]:
    byte1 = microcode[offset]
    operator = parse_opcode(byte1)
    if operator == LUS:
        return (LUS, 1, 1, {"index": byte1 & 0x3F})
    elif operator == LUD:
        return (LUD, 1, 2, {"index": byte1 & 0x0F, "step": (byte1 >> 4) & 0x01})
    elif operator == SLC or operator == SLS or operator == SRC or operator == SRS:
        repeat_count = (byte1 & 0x03) + 1
        params = {
            "shift_size": ((byte1 & 0x0C) >> 2) + 1,
            "repeat_count": repeat_count,
        }
        return (operator, 1, repeat_count, params)
    elif operator == LDI:
        return (LDI, 2, 1, {"byte": microcode[offset + 1]})
    elif operator == CPY:
        length = (byte1 & 0x07) + 1
        params = {
            "offset": (byte1 >> 3) & 0x3,
            "length": length,
        }
        return (CPY, 1, length, params)
    elif operator == REV:
        offset = (byte1 >> 3) & 0x1
        length = (byte1 & 0x07) + 1
        return (REV, 1, length, {"offset": offset, "length": length})
    elif operator == RPT:
        repeat_count = (byte1 & 0x0F) + 1
        return (RPT, 1, repeat_count, {"repeat_count": repeat_count})
    elif operator == XOR:
        mask_width = ((byte1 >> 3) & 0x01) + 1
        mask_pos = byte1 & 0x07
        return (XOR, 1, 1, {"mask_width": mask_width, "mask_pos": mask_pos})
    else:
        return (UNKNOWN, 0, 0, {})


class Operation:
    def __init__(self, microcode: list[int], orig_seq: list[int], cost: float):
        self.microcode = microcode
        self.orig_seq = orig_seq
        self.cost = cost

    def operator(self) -> Operator:
        (op, _, _) = parse_instruction(self.microcode, 0)
        return op

    def __repr__(self) -> str:
        (op, _, _, params) = parse_instruction(self.microcode, 0)
        ret = f"{op.mnemonic} ("
        for key, value in params.items():
            ret += f"{key}={value}, "
        ret = ret.rstrip(", ")
        ret += ")"
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
        num_glyphs = self.blob[OFST_GLYPH_TABLE_LEN]
        glyph_table_size = num_glyphs * GLYPH_TABLE_ENTRY_SIZE
        lut_size = self.blob[OFST_LUT_SIZE]
        microcode_size = blob_size - OFST_GLYPH_TABLE - glyph_table_size - lut_size
        microcode_per_glyph = microcode_size / num_glyphs
        lut_usage_percent = lut_size * 100 / MAX_LUT_SIZE
        total_size = blob_size
        total_size_per_glyph = total_size / num_glyphs

        pc = OFST_GLYPH_TABLE + glyph_table_size + lut_size
        stats_inst_size = {}
        stats_orig_size = {}
        total_inst_size = 0
        total_orig_size = 0
        while pc < blob_size:
            (opr, inst_size, orig_size, _) = parse_instruction(self.blob, pc)
            stats_inst_size[opr.mnemonic] = (
                stats_inst_size.get(opr.mnemonic, 0) + inst_size
            )
            stats_orig_size[opr.mnemonic] = (
                stats_orig_size.get(opr.mnemonic, 0) + orig_size
            )
            total_inst_size += inst_size
            total_orig_size += orig_size
            if inst_size <= 0:
                raise RuntimeError(f"Unknown instruction: 0x{self.blob[pc]:02x} {opr}")
            pc += inst_size
        total_delta_size = total_inst_size - total_orig_size

        code = ""
        code += "// Generated from ShapoFont\n"
        code += f"//   Format Version: {self.blob[OFST_FORMAT_VERSION]}\n"
        code += f"//   First Code    : {self.blob[OFST_FIRST_CODE]}\n"
        code += f"//   Glyph Count   : {num_glyphs}\n"
        code += "//   Estimated Footprint:\n"
        code += f"//     Header        : {OFST_GLYPH_TABLE:4d} Bytes\n"
        code += f"//     Glyph Table   : {glyph_table_size:4d} Bytes ({GLYPH_TABLE_ENTRY_SIZE} Bytes/glyph)\n"
        code += f"//     Lookup Table  : {lut_size:4d} Bytes ({lut_usage_percent:.2f}% used)\n"
        code += f"//     Microcodes    : {microcode_size:4d} Bytes ({microcode_per_glyph:.2f} Bytes/glyph)\n"
        code += f"//     Total         : {total_size:4d} Bytes ({total_size_per_glyph:.2f} Bytes/glyph)\n"
        code += "//   Compression Performance:\n"
        inst_sorted = sorted(stats_inst_size.keys())
        total_comp_ratio = total_delta_size / total_orig_size * 100
        for inst in inst_sorted:
            inst_size = stats_inst_size[inst]
            orig_size = stats_orig_size[inst]
            delta_size = inst_size - orig_size
            comp_ratio = delta_size / total_orig_size * 100
            code += f"//     {inst:5s}: {orig_size:4d} --> {inst_size:4d} ({comp_ratio:+7.2f}%)\n"
        code += f"//     Total: {total_orig_size:4d} --> {total_inst_size:4d} ({total_comp_ratio:+7.2f}%)\n"
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
        sequence = bmp.to_byte_segments(
            vertical_scan=self.vertical_scan,
            bit_reverse=self.bit_reverse,
        )

        if VERBOSE:
            print(f"[{LIB_NAME}] Glyph added: {format_char(code)}")
            print(f"  Bytes:")
            for i, byte in enumerate(sequence):
                if i % 16 == 0:
                    print("    ", end="")
                print(f"0x{byte:02x} ", end="")
                if (i + 1) % 16 == 0 or i == len(sequence) - 1:
                    print()

        sequence.insert(0, 0x00)  # TODO: remove pivot byte
        num_bytes = len(sequence)

        verbose_print(f"  Generating Instructions...")
        t_start = time.time()

        class State:
            def __init__(self, i_pos: int):
                self.i_pos = i_pos
                self.next_ops: dict[int, Operation] = {}
                self.best_cost = 999999
                self.best_op: Operation | None = None
                self.best_prev: State | None = None

                # Find next available operations
                for i_next in range(i_pos + 1, len(sequence)):
                    cand = suggest_operation(i_pos, i_next)
                    if cand is not None:
                        self.next_ops[i_next] = cand

        def suggest_operation(i_src: int, i_dst: int) -> Operation | None:
            orig_seq = sequence[i_src + 1 : i_dst + 1]

            cands: list[Operation] = []
            cands += try_shift(i_src, i_dst, orig_seq)
            cands += try_cpy_rev(i_src, i_dst, orig_seq)
            cands += try_ldi(i_src, i_dst, orig_seq)
            cands += try_rpt(i_src, i_dst, orig_seq)
            cands += try_xor(i_src, i_dst, orig_seq)

            best_cand: Operation | None = None
            best_cost = float("inf")

            for cand in cands:
                if cand.cost < best_cost:
                    best_cost = cand.cost
                    best_cand = cand

            return best_cand

        def try_cpy_rev(i_src: int, i_dst: int, orig_seq: list[int]) -> list[Operation]:

            length = i_dst - i_src
            if length < 1 or length > COPY_MAX_LENGTH:
                return []

            for reverse in [False, True]:
                offset_range = range(0, 4)

                for offset in offset_range:
                    if i_src - length - offset < 0:
                        continue

                    if reverse and length == 1:
                        # Reserved for other instructions
                        continue

                    if not reverse and length == 1 and offset == 0:
                        # Reserved for other instructions
                        continue

                    fail = False
                    for i in range(length):
                        if reverse:
                            i_copy_from = i_src - offset - i
                        else:
                            i_copy_from = i_src - offset - length + 1 + i

                        if i_copy_from < 0:
                            copy_segment = 0x00
                        else:
                            copy_segment = sequence[i_copy_from]

                        if copy_segment != sequence[i_src + 1 + i]:
                            fail = True
                            break

                    if fail:
                        continue

                    op = REV if reverse else CPY
                    inst_code = op.code | (offset << 3) | (length - 1)
                    return [Operation([inst_code], orig_seq, op.cost)]

            return []

        def try_ldi(i_src: int, i_dst: int, orig_seq: list[int]) -> list[Operation]:
            if i_src + 1 == i_dst:
                return [Operation([LDI.code, sequence[i_dst]], orig_seq, LDI.cost)]
            else:
                return []

        def try_shift(i_src: int, i_dst: int, orig_seq: list[int]) -> list[Operation]:
            repeat_count = i_dst - i_src
            if repeat_count < 1 or repeat_count > SHIFT_MAX_REPEAT:
                return []

            shift_dir_range = [ShiftDir.LEFT, ShiftDir.RIGHT]
            shift_size_range = range(1, SHIFT_MAX_SIZE + 1)
            post_op_range = [ShiftPostOp.CLR, ShiftPostOp.SET]

            for shift_dir, shift_size, post_op in product(
                shift_dir_range, shift_size_range, post_op_range
            ):
                fail = False
                modifier = (1 << shift_size) - 1
                if shift_dir != 0:
                    modifier <<= 8 - shift_size
                if post_op == 0:
                    modifier = modifier ^ 0xFF

                work = sequence[i_src]
                for i_step in range(i_src, i_dst):
                    if shift_dir == ShiftDir.LEFT:
                        work = work << shift_size
                    else:
                        work = work >> shift_size
                    if post_op == ShiftPostOp.SET:
                        work |= modifier
                    else:
                        work &= modifier
                    if work != sequence[i_step + 1]:
                        fail = True
                        break

                if fail:
                    continue

                if shift_dir == ShiftDir.LEFT:
                    if post_op == ShiftPostOp.CLR:
                        op = SLC
                    else:
                        op = SLS
                else:
                    if post_op == ShiftPostOp.CLR:
                        op = SRC
                    else:
                        op = SRS
                inst_code = op.code | ((shift_size - 1) << 2) | (repeat_count - 1)
                return [Operation([inst_code], orig_seq, op.cost)]

            return []

        def try_rpt(i_src: int, i_dst: int, orig_seq: list[int]) -> list[Operation]:
            repeat_count = i_dst - i_src
            if repeat_count < 1 or repeat_count > REPEAT_MAX:
                return []

            for i_step in range(i_src, i_dst):
                if sequence[i_src] != sequence[i_step + 1]:
                    return []

            inst_code = RPT.code | (repeat_count - 1)
            return [Operation([inst_code], orig_seq, RPT.cost)]

        def try_xor(i_src: int, i_dst: int, orig_seq: list[int]) -> list[Operation]:
            if i_src + 1 != i_dst:
                return []

            mask_width_range = range(1, 2)
            mask_pos_range = range(0, 8)

            for mask_width, mask_pos in product(mask_width_range, mask_pos_range):
                mask = (1 << mask_width) - 1
                mask <<= mask_pos
                if sequence[i_src] ^ mask == sequence[i_dst]:
                    inst_code = XOR.code | ((mask_width - 1) << 3) | mask_pos
                    return [Operation([inst_code], orig_seq, XOR.cost)]

            return []

        # Solve with Dijkstra's algorithm
        nodes = [State(i) for i in range(num_bytes)]
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

            for i_next, op in curr.next_ops.items():
                next_cost = curr.best_cost + op.cost
                if next_cost < nodes[i_next].best_cost:
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

        t_elapsed = time.time() - t_start
        verbose_print(
            f"    {len(ops)} instructions generated ({t_elapsed * 1000:.2f} ms)."
        )

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
        verbose_print(f"[{LIB_NAME}] Generating Lookup Table...")
        byte_ref_count: dict[int, int] = {}
        for code in codes:
            glyph = self.glyphs[code]
            for op in glyph.operations:
                if LDI.match(op.microcode[0]):
                    this_byte = op.microcode[1]
                    byte_ref_count[this_byte] = byte_ref_count.get(this_byte, 0) + 1
        lut = sorted(
            byte_ref_count.keys(), key=lambda item: byte_ref_count[item], reverse=True
        )
        if len(lut) > MAX_LUT_SIZE:
            verbose_print(
                f"  Lookup Table shrunk: {len(lut)} --> {MAX_LUT_SIZE} bytes."
            )
            lut = lut[:MAX_LUT_SIZE]

        verbose_print(f"[{LIB_NAME}] Optimizing Lookup Table...")
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
        verbose_print("  LUT Before Reorder:")
        report_lut_score()
        verbose_print("  Reordering LUT...")

        class LutSeq:
            def __init__(self, seq: list[int], frozen: bool = False):
                self.array = seq
                self.frozen = frozen

            def __repr__(self):
                return f"{'*' if self.frozen else ''}[{' '.join(f'{b:02X}' for b in self.array)}]"

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

            if seq_buff_size >= LUD_INDEX_RANGE and not head_frozen:
                for seq in seq_buff:
                    seq.frozen = True
                head_frozen = True

            print("    ", end="")
            for seq in seq_buff:
                print(f"{seq} ", end="")
            print()

        new_lut = []
        for seq in seq_buff:
            new_lut += seq.array
        lut = new_lut + lut

        # Replace instructions with LUS as possible
        for code in codes:
            glyph = self.glyphs[code]
            for op in glyph.operations:
                if len(op.orig_seq) == 1 and op.orig_seq[0] in lut:
                    index = lut.index(op.orig_seq[0])
                    op.microcode = [LUS.code | index]

        # Replace instructions with LUD as possible
        verbose_print("  Replacing instructions LUS --> LUD as possible...")
        for code in codes:
            glyph = self.glyphs[code]
            index1 = -1

            i_op = 0
            while i_op < len(glyph.operations):
                op = glyph.operations[i_op]

                index2 = -1
                if LUS.match(op.microcode[0]):
                    index2 = op.microcode[0] & 0x3F

                lud_applicable = (
                    index1 >= 0
                    and index2 >= 0
                    and index1 < LUD_INDEX_RANGE
                    and (index1 == index2 or index1 + 1 == index2)
                )
                if lud_applicable:
                    step = 0 if index1 == index2 else 1
                    inst_code = LUD.code | index1 | (step << 4)
                    glyph.operations[i_op - 1].microcode = [inst_code]
                    glyph.operations.remove(op)
                    index1 = -1
                    continue

                index1 = index2
                i_op += 1

        verbose_print("  LUT After Reorder:")
        report_lut_score()

        # Construct microcode block
        verbose_print(f"[{LIB_NAME}] Constructing microcode block...")
        microcodes: list[int] = []
        for code in codes:
            verbose_print(f"  {format_char(code)}:")
            glyph = self.glyphs[code]
            glyph.entry_point = len(microcodes)
            for op in glyph.operations:
                if VERBOSE:
                    inst_code_str = " ".join(f"0x{b:02X}" for b in op.microcode)
                    print(f"    {inst_code_str:<10s} {op}")
                microcodes += op.microcode

        code_first = codes[0]
        code_last = codes[-1]

        font_dimension_0 = (self.glyph_height - 1) & 0x3F
        font_dimension_1 = (self.y_advance - 1) & 0x3F
        font_flags = 0
        if self.vertical_scan:
            font_flags |= 0x80
        if self.bit_reverse:
            font_flags |= 0x40

        verbose_print(f"[{LIB_NAME}] Generating blob...")

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
            glyph_dimension_0 = (glyph.glyphWidth - 1) & 0x3F
            glyph_dimension_1 = (glyph.x_advance - 1) & 0x3F

            blob.append(glyph.entry_point & 0xFF)
            blob.append((glyph.entry_point >> 8) & 0xFF)
            blob.append(glyph_dimension_0)
            blob.append(glyph_dimension_1)

        # LUT
        blob += lut

        # Microcode
        blob += microcodes

        return MameFont(name=self.name, blob=blob)
