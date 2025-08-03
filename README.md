<p align="center"><img src="./img/logo.svg" width="50"></p>
<h1 align="center">ShapoFont</h1>
<p align="center"><img src="./img/cover.jpg" width="100%"></p>

- Bitmap fonts made primarily for embedded projects
- a Tool for generating font files from PNG images

## Naming Rule

![](./img/dimensions.svg)

|Option|Description|Default Value|
|:--:|:--|:--:|
|s|Body Size|(required)|
|c|Cap Height|s|
|a|Ascender Spacing|0|
||Descent|s - c - a|
|w|weight|1|

# Fonts

Click thumbnail to open the font with GFXfont Web Simulator.

## ShapoSansP

### s05

<a href="https://shapoco.github.io/shapofont/sim/#u=/shapofont/ShapoSansP_s05.h" target="_blank"><img src="./bitmap/ShapoSansP/s05/design.png"></a>

### s07c05a01

<a href="https://shapoco.github.io/shapofont/sim/#u=/shapofont/ShapoSansP_s07c05a01.h" target="_blank"><img src="./bitmap/ShapoSansP/s07c05a01/design.png"></a>

### s08c07

<a href="https://shapoco.github.io/shapofont/sim/#u=/shapofont/ShapoSansP_s08c07.h" target="_blank"><img src="./bitmap/ShapoSansP/s08c07/design.png"></a>

### s12c09a01w02

<a href="https://shapoco.github.io/shapofont/sim/#u=/shapofont/ShapoSansP_s12c09a01w02.h" target="_blank"><img src="./bitmap/ShapoSansP/s12c09a01w02/design.png"></a>

### s21c16a01w03

<a href="https://shapoco.github.io/shapofont/sim/#u=/shapofont/ShapoSansP_s21c16a01w03.h" target="_blank"><img src="./bitmap/ShapoSansP/s21c16a01w03/design.png"></a>

### s27c22a01w04

<a href="https://shapoco.github.io/shapofont/sim/#u=/shapofont/ShapoSansP_s27c22a01w04.h" target="_blank"><img src="./bitmap/ShapoSansP/s27c22a01w04/design.png"></a>

## ShapoSansMono

### s08c07

<a href="https://shapoco.github.io/shapofont/sim/#u=/shapofont/ShapoSansMono_s08c07.h" target="_blank"><img src="./bitmap/ShapoSansMono/s08c07/design.png"></a>

## ShapoSansDigitP

### s16c14w02

<a href="https://shapoco.github.io/shapofont/sim/#u=/shapofont/ShapoSansDigitP_s16c14w02.h&t=0.123456789" target="_blank"><img src="./bitmap/ShapoSansDigitP/s16c14w02/design.png"></a>

### s24c23w04

<a href="https://shapoco.github.io/shapofont/sim/#u=/shapofont/ShapoSansDigitP_s24c23w04.h&t=0.123456789" target="_blank"><img src="./bitmap/ShapoSansDigitP/s24c23w04/design.png"></a>

### s32c30w04

<a href="https://shapoco.github.io/shapofont/sim/#u=/shapofont/ShapoSansDigitP_s32c30w04.h&t=0.123456789" target="_blank"><img src="./bitmap/ShapoSansDigitP/s32c30w04/design.png"></a>

## MameSansP

### s48c40w08

<a href="https://shapoco.github.io/shapofont/sim/#u=/shapofont/MameSansP_s48c40w08.h" target="_blank"><img src="./bitmap/MameSansP/s48c40w08/design.png"></a>

## MameSquareWide

### s64c48a04w16

<a href="https://shapoco.github.io/shapofont/sim/#u=/shapofont/MameSquareWide_s64c48a04w16.h" target="_blank"><img src="./bitmap/MameSquareWide/s64c48a04w16/design.png"></a>

## MameSansDigitP

### s64w08

<a href="https://shapoco.github.io/shapofont/sim/#u=/shapofont/MameSansDigitP_s64w08.h&t=0.123456789" target="_blank"><img src="./bitmap/MameSansDigitP/s64w08/design.png"></a>

## MameSeg7

### s40c38w06

<a href="https://shapoco.github.io/shapofont/sim/#u=/shapofont/MameSeg7_s40c38w06.h&t=0.1234567%0a89ABCDEF" target="_blank"><img src="./bitmap/MameSeg7/s40c38w06/design.png"></a>

# Designing Font with Painting Tool

ShapoFonts are designed using Microsoft Paint and converted to some font formats by Python scripts.

![](./img/designing_with_mspaint.png)

## How to Design

1. Create a canvas of appropriate size with a black background.
2. Design your glyphs in white.
3. Draw a red line (**position marker**) of the same width at the bottom of each glyph.

    ![](./img/how_to_design.svg)

4. Save the image as `design.png`.
5. In a JSON5 file `shapofont.json5`, list the characters contained in the image.

    ```json5
    {
        "codes": [
            {"from": 0x20, "to": 0x7E},
        ]
    }
    ```

- The vertical positions of the position markers of the glyphs side by side must be aligned.
- There must be at least typeSize + ascenderSpacing pixels of space above the position marker.
- The order of characters in the image must exactly match the order of characters listed in the meta information.

## Directory Structure

Create a directory for each dimension identifier under the family name directory and place a design image and meta information in it.

```
ShapoSansP/  .................. Family Name
+-- s20c16w3a1/  ............. Dimension Identifier
    +-- design.png  ......... Font Design File
    +-- shapofont.json5  .... Meta Information
```

## Converting to Font Files

1. Create a Python virtual environment using `venv-setup.shrc`.
    - `Pillow` and `json5` will be installed.
2. Specify the above design directory in `tools/shapofont.py` to convert to each font format.
    - `-i`: path to input directory (dimension identifier)
    - `--outdir_gfx_c`: output directory for GFXfont format

Since the script extracts a family name and a dimension identifier from the directory path, they must be named correctly.

### Example:

```bash
source venv-setup.shrc
./venv/bin/python3 ./tools/shapofont.py \
      -i bitmap/ShapoSansP/s21c16a01w03 \
      --outdir_gfx_c path/to/output/dir/
```

In this repository, after creating the venv, simply run `make all` and all fonts will be converted automatically.

# License

see [LICENSE](LICENSE).

The rights to font files generated using the tools included in ShapoFont are subject to the rights of the original bitmap images and any fonts contained therein.

# Using GFXfont in LovyanGFX

Before including the generated GFXfont, define the `SHAPOFONT_GFXFONT_NAMESPACE=::lgfx::` macro so that it can be used with LovyanGFX.

```c++
#define SHAPOFONT_GFXFONT_NAMESPACE ::lgfx::
#include "shapofont/ShapoSansP_s11c09w2a1.h"
```

# Memo

## ASCII (JIS X 0201) Code Table

```
      0   1   2   3   4   5   6   7   8   9   A   B   C   D   E   F
0x00  NUL SOH STX ETX EOT ENQ ACK BEL BS  HT  LF  VT  FF  CR  SO  SI
0x10  DLE DC1 DC2 DC3 DC4 NAK SYN ETB CAN EM  SUB ESC FS  GS  RS  US
0x20  SP  !   "   #   $   %   &   '   (   )   *   +   ,   -   .   /
0x30  0   1   2   3   4   5   6   7   8   9   :   ;   <   =   >   ?
0x40  @   A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
0x50  P   Q   R   S   T   U   V   W   X   Y   Z   [   \   ]   ^   _
0x60  `   a   b   c   d   e   f   g   h   i   j   k   l   m   n   o
0x70  p   q   r   s   t   u   v   w   x   y   z   {   |   }   ~   DEL
0x80
0x90
0xA0      ｡   ｢   ｣   ､   ･   ｦ   ｧ   ｨ   ｩ   ｪ   ｫ   ｬ   ｭ   ｮ   ｯ
0xB0  ｰ   ｱ   ｲ   ｳ   ｴ   ｵ   ｶ   ｷ   ｸ   ｹ   ｺ   ｻ   ｼ   ｽ   ｾ   ｿ
0xC0  ﾀ   ﾁ   ﾂ   ﾃ   ﾄ   ﾅ   ﾆ   ﾇ   ﾈ   ﾉ   ﾊ   ﾋ   ﾌ   ﾍ   ﾎ   ﾏ
0xD0  ﾐ   ﾑ   ﾒ   ﾓ   ﾔ   ﾕ   ﾖ   ﾗ   ﾘ   ﾙ   ﾚ   ﾛ   ﾜ   ﾝ   ﾞ   ﾟ
0xE0
0xF0
```
