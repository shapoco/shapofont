# [WIP] MameFont

Compressed font format definitions and tools for embedded projects.

# Flow

![](./img/flow.svg)

# Format Definition

## Blob Structure

|Size [Bytes]|Name|
|:--:|:--|
|8|Font Header|
|`glyphEntryStride` \* `glyphTableLen`|Character Table|
|`lutSize`|Lookup Table (LUT)|
|(Variable)|Microcode Blocks|

## Font Header

A structure that provides information common to the entire font.

|Size [Bytes]|Name|Description|
|:--|:--|:--|
|1|`formatVersion`|0x01|
|1|`glyphEntryStride`|Number of bytes of each Glyph Table Entry. Always 4 at version 1|
|1|`codeOffset`|ASCII code of the first entry of Glyph Table|
|1|`glyphTableLen`|Number of entries of Glyph Table|
|2|`lineDimension`|Dimension of Line|
|1|`lutSize`|Number of bytes of LUT|
|1|(Reserved)||

### `lineDimension`

|Bit Range|Name|Description|
|:--:|:--|:--|
|15:14|(Reserved)||
|13:8|`ySpacing`|Vertical spacing in pixels|
|7:6|(Reserved)||
|5:0|`glyphHeight`|Height of glyph in pixels|

## Glyph Table Entry

|Size [Bytes]|Name|Description|
|:--:|:--|:--|
|2|`entryPoint`|Offset from start of Microcode Block in bytes|
|2|`glyphDimension`|Dimension of glyph bitmap|

### `glyphDimension`

|Bit Range|Name|Description|
|:--:|:--|:--|
|15|`scanDirection`|0: horizontal, 1: vertical|
|14|(Reserved)||
|13:8|`xSpacing`|Horizontal spacing in pixels|
|7:6|(Reserved)||
|5:0|`glyphWidth`|Number of pixels of glyph bitmap|

## Microcode Block

|Size [Bytes]|Description|
|:--:|:--|
|(Variable)|Array of instructions|

## Instruction Set

|Value Range|Mnemonic|Description|
|:---|:---|:---|
|0x00-3f|`LKP`|Load from LUT|
|0x40-4f|`SLC`|Shift Previous Byte Left and Clear LSB|
|0x50-5f|`SLS`|Shift Previous Byte Left and Set LSB|
|0x60-6f|`SRC`|Shift Previous Byte Right and Clear MSB|
|0x70-7f|`SRS`|Shift Previous Byte Right and Set MSB|
|0x80-bf|`CPY`|Copy Previous Sequence|
|0xc0-df|`REV`|Reverse Previous Sequence|
|0xe0-ef|`RPT`|Repeat Previous Byte|
|0xf0-f7|`XOR`|XOR Previous Byte and Immediate|
|0xff|-|(Reserved)|

### Load from LUT (`LKP`)

|Bit Range|Value|
|:--:|:--|
|7:6|0b00|
|5:0|`index`|

```c
buff[cursor++] = lut[index];
```

### Shift Previous Byte and Clear/Set (`SLC`, `SLS`, `SRC`, `SRS`)

|Bit Range|Value|
|:--:|:--|
|7:6|0b01|
|5|`shift_dir` (0: Left, 1: Right)|
|4|`post_op` (0: Clear, 1: Set)|
|3|`shift_size - 1`|
|2:0|`len - 1`|

```c
for (int i = 0; i < len; i++) {
    if (shift_dir == 0) {
        buff[cursor] = buff[cursor - 1] << shift_size;
        if (post_op == 0) {
            buff[cursor] &= 0xfe;
        }
        else {
            buff[cursor] |= 0x01;
        }
    }
    else {
        buff[cursor] = buff[cursor - 1] >> shift_size;
        if (post_op == 0) {
            buff[cursor] &= 0x7f;
        }
        else {
            buff[cursor] |= 0x80;
        }
    }
    cursor++;
}
```

### Copy Previous Sequence (`CPY`)

|Bit Range|Value|
|:--:|:--|
|7:6|0b10|
|5:4|`offset`|
|3:0|`len - 1`|

```c
memcpy(buff + cursor, buff + (cursor - len - offset), len);
cursor += len;
```

### Reverse Previous Sequence (`REV`)

|Bit Range|Value|
|:--:|:--|
|7:5|0b110|
|4|`offset - 1`|
|3:0|`len - 1`|

```c
for (int i = 0; i < len; i++) {
    buff[cursor + i] = buff[cursor - offset - i];
}
cursor += len;
```

### Repeat Previous Byte (`RPT`)

|Bit Range|Value|
|:--:|:--|
|7:4|0b1110|
|3:0|`len - 1`|

```c
memset(buff + cursor, buff[cursor - 1], len);
cursor += len;
```

### XOR Previous Byte and Immediate (`XOR`)

|Bit Range|Value|
|:--:|:--|
|7:4|0b1111|
|3|`width - 1`|
|2:0|`bit`|

```c
int mask = width == 1 ? 0x01 : 0x03;
buff[cursor++] = buff[cursor - 1] ^ (mask << bit);
```

Combination of `width=2` and `bit=7` is reserved.

# Rendering

## Scan Path

Scan direction is defined in `scanDirection` for each glyph.

![](./img/scan_path.svg)
