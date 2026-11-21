function parseCInt(name: string, s: string): number {
  s = s.trim();
  let sign = 1;
  if (s.startsWith('-')) {
    sign = -1;
    s = s.slice(1).trim();
  }
  if (/^0x([0-9a-fA-F]+)$/.test(s)) {
    return sign * parseInt(s.slice(2), 16);
  } else if (/^0[0-7]+$/.test(s)) {
    return sign * parseInt(s, 8);
  } else if (/^0b[01]+$/.test(s)) {
    return sign * parseInt(s.slice(2), 2);
  } else if (/^[0-9]+$/.test(s)) {
    return sign * parseInt(s, 10);
  }
  throw new Error(`Failed to parse ${name}: ${s}`);
}

function parseColor(colorStr: string): number[] {
  const rgb6 = colorStr.match(/^#([0-9a-fA-F]{6})$/);
  if (rgb6) {
    return [
      parseInt(rgb6[1].slice(0, 2), 16),
      parseInt(rgb6[1].slice(2, 4), 16),
      parseInt(rgb6[1].slice(4, 6), 16),
    ];
  }
  const rgb3 = colorStr.match(/^#([0-9a-fA-F]{3})$/);
  if (rgb3) {
    return [
      parseInt(rgb3[1].charAt(0) + rgb3[1].charAt(0), 16),
      parseInt(rgb3[1].charAt(1) + rgb3[1].charAt(1), 16),
      parseInt(rgb3[1].charAt(2) + rgb3[1].charAt(2), 16),
    ];
  }
  throw new Error(`Invalid color format: ${colorStr}`);
}

function encodeColor(rgb: number[]): string {
  let threeDigits = true;
  for (const ch of rgb) {
    if (Math.floor(ch / 16) != ch % 16) {
      threeDigits = false;
      break;
    }
  }
  if (threeDigits) {
    return `#${rgb.map(ch => ch.toString(16).slice(0, 1)).join('')}`;
  } else {
    return `#${rgb.map(ch => ch.toString(16).padStart(2, '0')).join('')}`;
  }
}

function codeToStr(code: number): string {
  if (code < 0 || code > 0x10FFFF) {
    throw new Error(`Invalid Unicode code point: ${code}`);
  }
  return `'${String.fromCodePoint(code)}' (0x${
      code.toString(16).toUpperCase()})`;
}

function reverseByte(byte: number): number {
  byte = ((byte << 4) & 0xF0) | ((byte >> 4) & 0x0F);
  byte = ((byte & 0xCC) >> 2) | ((byte & 0x33) << 2);
  byte = ((byte & 0xAA) >> 1) | ((byte & 0x55) << 1);
  return byte;
}

function stripComments(src: string): string {
  return src.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/.*$/gm, '');
}

function stripPreprocessorLines(src: string): string {
  return src.replace(/^[ \t]*#.*$/gm, '');
}

/** Parses `{ .a = 1, .b = &x, ... }` style designated initializers into a map. */
function parseDesignatedInitializer(body: string): Map<string, string> {
  const fields = new Map<string, string>();
  const re = /\.(\w+)\s*=\s*([^,}]+)/g;
  let m: RegExpExecArray|null;
  while ((m = re.exec(body)) !== null) {
    fields.set(m[1], m[2].trim());
  }
  return fields;
}

function requireField(fields: Map<string, string>, owner: string, name: string): string {
  const value = fields.get(name);
  if (value === undefined) {
    throw new Error(`Missing field in ${owner}: .${name}`);
  }
  return value;
}

/** Finds `TYPE name[] = { ... }` and returns its integer elements. */
function findCIntArray(src: string, name: string, what: string): number[] {
  const re = new RegExp(
      `\\b(uint8_t|uint16_t|uint32_t|int8_t|int16_t|int32_t|unsigned\\s+char|char)\\s+(const\\s+)?${name}` +
          `\\s*\\[\\s*\\]\\s*=\\s*\\{([^\\}]*)\\}`,
      'm');
  const m = re.exec(src);
  if (!m) throw new Error(`Failed to find array: ${name} (${what})`);
  return m[3].split(',').map(s => s.trim()).filter(s => s !== '').map(s => parseCInt(what, s));
}

/** Reads `len` bits (MSB first) at bit position `bitPos`. Bytes past the end read as 0. */
function getBits(data: Uint8Array, bitPos: number, len: number): number {
  const mask = (1 << len) - 1;
  const bytePos = bitPos >> 3;
  const bitOfs = bitPos & 7;
  const hi = data[bytePos] ?? 0;
  if (bitOfs + len > 8) {
    const lo = data[bytePos + 1] ?? 0;
    return (((hi << 8) | lo) >> (16 - bitOfs - len)) & mask;
  }
  return (hi >> (8 - bitOfs - len)) & mask;
}

/**
 * Decoder for LVGL's compressed glyph bitmaps (lv_font_fmt_txt, bitmap_format 1 or 2).
 * Port of rle_next() / decompress() in lv_font_fmt_txt.c. Returns one level per pixel.
 */
class LvglRleDecoder {
  private readonly STATE_SINGLE = 0;
  private readonly STATE_REPEATED = 1;
  private readonly STATE_COUNTER = 2;
  private state = this.STATE_SINGLE;
  private rdp = 0;
  private prevV = 0;
  private count = 0;

  constructor(private data: Uint8Array, private bpp: number) {}

  private next(): number {
    let ret = 0;
    if (this.state === this.STATE_SINGLE) {
      ret = getBits(this.data, this.rdp, this.bpp);
      if (this.rdp !== 0 && this.prevV === ret) {
        this.count = 0;
        this.state = this.STATE_REPEATED;
      }
      this.prevV = ret;
      this.rdp += this.bpp;
    } else if (this.state === this.STATE_REPEATED) {
      const v = getBits(this.data, this.rdp, 1);
      this.count++;
      this.rdp += 1;
      if (v === 1) {
        ret = this.prevV;
        if (this.count === 11) {
          this.count = getBits(this.data, this.rdp, 6);
          this.rdp += 6;
          if (this.count !== 0) {
            this.state = this.STATE_COUNTER;
          } else {
            ret = getBits(this.data, this.rdp, this.bpp);
            this.prevV = ret;
            this.rdp += this.bpp;
            this.state = this.STATE_SINGLE;
          }
        }
      } else {
        ret = getBits(this.data, this.rdp, this.bpp);
        this.prevV = ret;
        this.rdp += this.bpp;
        this.state = this.STATE_SINGLE;
      }
    } else {
      ret = this.prevV;
      this.count--;
      if (this.count === 0) {
        ret = getBits(this.data, this.rdp, this.bpp);
        this.prevV = ret;
        this.rdp += this.bpp;
        this.state = this.STATE_SINGLE;
      }
    }
    return ret;
  }

  /** Decodes a w x h glyph. With `prefilter`, each line is XORed with the previous one. */
  public decode(w: number, h: number, prefilter: boolean): Uint8Array {
    const out = new Uint8Array(w * h);
    const line = new Uint8Array(w);
    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        const v = this.next();
        line[x] = (prefilter && y > 0) ? (line[x] ^ v) : v;
        out[y * w + x] = line[x];
      }
    }
    return out;
  }
}

enum ScanType {
  /** 1 bpp, rows packed back to back, MSB first (GFXfont) */
  HORIZONTAL_PACKED,
  /** 1/2/4/8 bpp, rows packed back to back, MSB first (LVGL plain format) */
  LVGL_PACKED,
  /** one level (0 .. 2^bpp-1) per byte, already unpacked */
  LEVELS,
}

class GrayBitmap {
  public grayData: Uint8Array;

  constructor(
      public width: number, public height: number, public rawData: Uint8Array,
      public scanType: ScanType, public msb1st: boolean = false,
      public bitsPerPixel: number = 1) {
    const grayData = new Uint8Array(width * height);

    switch (scanType) {
      case ScanType.HORIZONTAL_PACKED: {
        let ibyte = 0;
        let ibit = 0;
        let sreg = 0;
        for (let y = 0; y < height; y++) {
          for (let x = 0; x < width; x++) {
            if (ibit == 0) {
              sreg = rawData[ibyte++];
              if (msb1st) sreg = reverseByte(sreg);
              ibit = 8;
            }
            grayData[y * width + x] = ((sreg & 1) == 0) ? 0x00 : 0xFF;
            sreg >>= 1;
            ibit--;
          }
        }
      } break;

      case ScanType.LVGL_PACKED: {
        const maxLevel = (1 << bitsPerPixel) - 1;
        for (let i = 0; i < width * height; i++) {
          grayData[i] = Math.round(getBits(rawData, i * bitsPerPixel, bitsPerPixel) * 255 / maxLevel);
        }
      } break;

      case ScanType.LEVELS: {
        const maxLevel = (1 << bitsPerPixel) - 1;
        for (let i = 0; i < width * height; i++) {
          grayData[i] = Math.round(rawData[i] * 255 / maxLevel);
        }
      } break;

      default:
        throw new Error(`Unsupported scan type: ${scanType}`);
    }

    this.grayData = grayData;
  }
}

class Glyph {
  constructor(
      public dataOffset: number, public bitmap: GrayBitmap|null,
      public width: number, public height: number, public xAdvance: number,
      public xOffset: number, public yOffset: number) {
    this.dataOffset = dataOffset;
    this.bitmap = bitmap;
    this.width = width;
    this.height = height;
    this.xAdvance = xAdvance;
    this.xOffset = xOffset;
    this.yOffset = yOffset;
  }

  public render(
      ctx: CanvasRenderingContext2D, x: number, y: number, textSize: number,
      dotSize: number, dotEmphasis: boolean, color: string) {
    if (!this.bitmap) return;

    const multSize = textSize * dotSize;

    const [colR, colG, colB] = parseColor(color);

    ctx.save();
    ctx.translate(x + this.xOffset * multSize, y + this.yOffset * multSize);
    for (let y = 0; y < this.height; y++) {
      for (let x = 0; x < this.width; x++) {
        const pixel =
            Math.round(100 * this.bitmap.grayData[y * this.width + x] / 255);
        ctx.fillStyle = `rgb(${colR} ${colG} ${colB} / ${pixel}%)`;
        if (dotSize < 2 || !dotEmphasis) {
          ctx.fillRect(x * multSize, y * multSize, multSize, multSize);
        } else {
          for (let i = 0; i < textSize; i++) {
            for (let j = 0; j < textSize; j++) {
              ctx.fillRect(
                  x * multSize + i * dotSize, y * multSize + j * dotSize,
                  dotSize - 1, dotSize - 1);
            }
          }
        }
      }
    }
    ctx.restore();
  }
}

class Font {
  public format: string = '';
  public firstCode: number = 0;
  public lastCode: number = 0;
  public yAdvance: number = 0;
  public glyphs: Map<number, Glyph> = new Map();

  constructor(src: string) {
    src = stripComments(src);
    let success = false;
    if (!success) success = this.tryParseGfxFont(src);
    if (!success) success = this.tryParseLvglFont(src);
    if (!success) throw new Error('Unknown Font Format (GFXfont and LVGL fonts are supported)');
  }

  tryParseGfxFont(src: string): boolean {

    const mGfxFont = /GFXfont\s+(\w+)(\s*\w+)?\s*=\s*\{([^\}]+)\}/gm.exec(src);
    if (!mGfxFont) return false;
    this.format = 'GFXfont';

    const fontParams = mGfxFont[3].split(',');
    if (fontParams.length < 5) {
      throw new Error('Too few parameters for struct GFXfont');
    }

    const mBitmaps = /^(\([^\)]+\)\s*)?(\w+)$/.exec(fontParams[0].trim());
    if (!mBitmaps) throw new Error('Failed to parse GFXfont.bitmap');

    const mGlyphs = /^(\([^\)]+\)\s*)?(\w+)$/.exec(fontParams[1].trim());
    if (!mGlyphs) throw new Error('Failed to parse GFXfont.glyph');

    this.firstCode = parseCInt('GFXfont.first', fontParams[2].trim());
    this.lastCode = parseCInt('GFXfont.last', fontParams[3].trim());
    this.yAdvance = parseCInt('GFXfont.yAdvance', fontParams[4].trim());

    const bmpArrayName = mBitmaps[2];
    const regexBmpArray = new RegExp(
        `\\b(uint8_t|unsigned\\s+char)\\s+${bmpArrayName}` +
            `\\s*\\[\\s*\\](\\s*\\w+)?\\s*=\\s*\\{([^\\}]+)\\}`,
        'gm');
    const mBmpArray = regexBmpArray.exec(src);
    if (!mBmpArray) {
      throw new Error(`Failed to find bitmap array: ${bmpArrayName}`);
    }

    const bitmapData =
        new Uint8Array(mBmpArray[3]
                           .split(',')
                           .filter(s => s.trim() !== '')
                           .map(s => parseCInt('bitmap data', s)));


    const glyphArrayName = mGlyphs[2];
    const regexGlyphArray = new RegExp(
        `\\bGFXglyph\\s*${glyphArrayName}` +
            `\\s*\\[\\s*\\](\\s*\\w+)?\\s*=\\s*\\{([^\\;]+)\\}\\s*;`,
        'gm');
    const mGlyphArray = regexGlyphArray.exec(src);
    if (!mGlyphArray) {
      throw new Error(`Failed to find glyph array: ${glyphArrayName}`);
    }
    let code = this.firstCode;
    for (let glyphIniter of mGlyphArray[2].split(/}\s*,/)) {
      glyphIniter = glyphIniter.trim();
      if (glyphIniter.endsWith('}')) {
        glyphIniter = glyphIniter.slice(0, -1).trimEnd();
      }
      if (glyphIniter === '') continue;
      if (glyphIniter.startsWith('{')) {
        glyphIniter = glyphIniter.slice(1).trimStart();
      } else {
        throw new Error(
            `Failed to parse GFXglyph initialization: ${glyphIniter}`);
      }

      const glyphParams = glyphIniter.split(',').map(s => s.trim());
      if (glyphParams.length < 6) {
        throw new Error(
            `Too few parameters for GFXglyph: ${glyphParams.length}`);
      }
      const iBmpStart = parseCInt('GFXglyph.bitmapOffset', glyphParams[0]);
      const w = parseCInt('GFXglyph.width', glyphParams[1]);
      const h = parseCInt('GFXglyph.height', glyphParams[2]);
      const xAdvance = parseCInt('GFXglyph.xAdvance', glyphParams[3]);
      const xOffset = parseCInt('GFXglyph.xOffset', glyphParams[4]);
      const yOffset = parseCInt('GFXglyph.yOffset', glyphParams[5]);

      let bmp: GrayBitmap|null = null;

      if (w > 0 && h > 0) {
        const iBmpEnd = iBmpStart + Math.ceil(w * h / 8);
        if (iBmpStart < 0 || bitmapData.length <= iBmpStart) {
          throw new Error(`GFXglyph.bitmapOffset out of range: ${iBmpStart}`);
        }
        if (iBmpEnd < 1 || bitmapData.length < iBmpEnd) {
          throw new Error(`End of bitmap data out of range: ${iBmpEnd}`);
        }
        const numBmpBytes = Math.ceil(w * h / 8);

        bmp = new GrayBitmap(
            w, h, bitmapData.subarray(iBmpStart, iBmpStart + numBmpBytes),
            ScanType.HORIZONTAL_PACKED, true);
      } else {
        bmp = new GrayBitmap(
            w, h, new Uint8Array(0), ScanType.HORIZONTAL_PACKED, true);
      }

      const glyph = new Glyph(iBmpStart, bmp, w, h, xAdvance, xOffset, yOffset);
      this.glyphs.set(code, glyph);

      code++;
    }

    return true;
  }


  tryParseLvglFont(src: string): boolean {
    src = stripPreprocessorLines(src);

    const mFont = /\blv_font_t\s+(\w+)\s*=\s*\{([^\}]*)\}/m.exec(src);
    if (!mFont) return false;
    this.format = 'LVGL';

    const fontFields = parseDesignatedInitializer(mFont[2]);
    this.yAdvance = parseCInt('lv_font_t.line_height', requireField(fontFields, 'lv_font_t', 'line_height'));
    const dscName = requireField(fontFields, 'lv_font_t', 'dsc').replace(/^&\s*/, '');

    const mDsc = new RegExp(`\\blv_font_fmt_txt_dsc_t\\s+${dscName}\\s*=\\s*\\{([^\\}]*)\\}`, 'm').exec(src);
    if (!mDsc) throw new Error(`Failed to find font descriptor: ${dscName}`);
    const dscFields = parseDesignatedInitializer(mDsc[1]);

    // 0: plain, 1: RLE compressed with XOR prefilter, 2: RLE compressed without prefilter
    const bitmapFormat = parseCInt('bitmap_format', dscFields.get('bitmap_format') ?? '0');
    if (![0, 1, 2].includes(bitmapFormat)) throw new Error(`Unsupported bitmap_format: ${bitmapFormat}`);
    const compressed = bitmapFormat !== 0;
    this.format = compressed ? 'LVGL (compressed)' : 'LVGL';
    const bpp = parseCInt('bpp', requireField(dscFields, 'lv_font_fmt_txt_dsc_t', 'bpp'));
    if (![1, 2, 3, 4, 8].includes(bpp)) throw new Error(`Unsupported bpp: ${bpp}`);
    if (!compressed && bpp === 3) throw new Error('bpp = 3 is only valid for compressed fonts');

    const bitmapData = new Uint8Array(
        findCIntArray(src, requireField(dscFields, 'lv_font_fmt_txt_dsc_t', 'glyph_bitmap'), 'glyph bitmap'));

    // Glyph descriptors
    const glyphDscName = requireField(dscFields, 'lv_font_fmt_txt_dsc_t', 'glyph_dsc');
    const mGlyphDsc = new RegExp(
        `\\blv_font_fmt_txt_glyph_dsc_t\\s+${glyphDscName}\\s*\\[\\s*\\]\\s*=\\s*\\{([\\s\\S]*?)\\}\\s*;`, 'm').exec(src);
    if (!mGlyphDsc) throw new Error(`Failed to find glyph descriptors: ${glyphDscName}`);
    const GLYPH_DSC_FIELDS = ['bitmap_index', 'adv_w', 'box_w', 'box_h', 'ofs_x', 'ofs_y'];
    const glyphDscs: number[][] = [];
    for (const m of mGlyphDsc[1].matchAll(/\{([^\}]*)\}/g)) {
      const fields = parseDesignatedInitializer(m[1]);
      if (fields.size > 0) {
        glyphDscs.push(GLYPH_DSC_FIELDS.map(f => parseCInt(`glyph_dsc.${f}`, fields.get(f) ?? '0')));
      } else {
        const values = m[1].split(',').map(s => s.trim()).filter(s => s !== '');
        if (values.length < GLYPH_DSC_FIELDS.length) {
          throw new Error(`Too few parameters for lv_font_fmt_txt_glyph_dsc_t: ${m[0]}`);
        }
        glyphDscs.push(values.slice(0, GLYPH_DSC_FIELDS.length).map(v => parseCInt('glyph_dsc', v)));
      }
    }

    // Character maps: code point --> glyph id
    const cmapsName = requireField(dscFields, 'lv_font_fmt_txt_dsc_t', 'cmaps');
    const mCmaps = new RegExp(
        `\\blv_font_fmt_txt_cmap_t\\s+${cmapsName}\\s*\\[\\s*\\]\\s*=\\s*\\{([\\s\\S]*?)\\}\\s*;`, 'm').exec(src);
    if (!mCmaps) throw new Error(`Failed to find character maps: ${cmapsName}`);
    const codeToGid = new Map<number, number>();
    for (const m of mCmaps[1].matchAll(/\{([^\}]*)\}/g)) {
      const fields = parseDesignatedInitializer(m[1]);
      if (fields.size === 0) continue;
      const rangeStart = parseCInt('cmap.range_start', requireField(fields, 'cmap', 'range_start'));
      const rangeLength = parseCInt('cmap.range_length', requireField(fields, 'cmap', 'range_length'));
      const gidStart = parseCInt('cmap.glyph_id_start', requireField(fields, 'cmap', 'glyph_id_start'));
      const unicodeListName = fields.get('unicode_list') ?? 'NULL';
      const gidOfsListName = fields.get('glyph_id_ofs_list') ?? 'NULL';
      const unicodeList = unicodeListName === 'NULL' ? null : findCIntArray(src, unicodeListName, 'unicode list');
      const gidOfsList = gidOfsListName === 'NULL' ? null : findCIntArray(src, gidOfsListName, 'glyph id offset list');

      // Same rules as LVGL's lv_font_fmt_txt.c: the list pointers decide the format
      if (!unicodeList) {
        for (let rcp = 0; rcp < rangeLength; rcp++) {
          const gid = gidOfsList ? gidStart + (gidOfsList[rcp] ?? 0) : gidStart + rcp;
          codeToGid.set(rangeStart + rcp, gid);
        }
      } else {
        unicodeList.forEach((rcp, i) => {
          const gid = gidOfsList ? gidStart + (gidOfsList[i] ?? 0) : gidStart + i;
          codeToGid.set(rangeStart + rcp, gid);
        });
      }
    }

    for (const [code, gid] of codeToGid) {
      if (gid <= 0 || gid >= glyphDscs.length) continue;
      const [bitmapIndex, advW, boxW, boxH, ofsX, ofsY] = glyphDscs[gid];
      let bmp: GrayBitmap|null = null;
      if (boxW > 0 && boxH > 0) {
        if (bitmapIndex < 0 || bitmapData.length <= bitmapIndex) {
          throw new Error(`Glyph bitmap out of range: U+${code.toString(16).toUpperCase()}`);
        }
        if (compressed) {
          const levels = new LvglRleDecoder(bitmapData.subarray(bitmapIndex), bpp)
                             .decode(boxW, boxH, bitmapFormat === 1);
          bmp = new GrayBitmap(boxW, boxH, levels, ScanType.LEVELS, true, bpp);
        } else {
          const numBytes = Math.ceil(boxW * boxH * bpp / 8);
          if (bitmapData.length < bitmapIndex + numBytes) {
            throw new Error(`Glyph bitmap out of range: U+${code.toString(16).toUpperCase()}`);
          }
          bmp = new GrayBitmap(
              boxW, boxH, bitmapData.subarray(bitmapIndex, bitmapIndex + numBytes),
              ScanType.LVGL_PACKED, true, bpp);
        }
      }
      // LVGL: adv_w is in 1/16 px and rounded; ofs_y is the box bottom measured up from the baseline
      const xAdvance = (advW + 8) >> 4;
      this.glyphs.set(code, new Glyph(bitmapIndex, bmp, boxW, boxH, xAdvance, ofsX, -(ofsY + boxH)));
    }

    if (this.glyphs.size === 0) throw new Error('No glyphs found in LVGL font');
    const codes = Array.from(this.glyphs.keys());
    this.firstCode = Math.min(...codes);
    this.lastCode = Math.max(...codes);
    return true;
  }

  public getPreferredOriginY(): number {
    let y = 0;
    for (const glyph of this.glyphs.values()) {
      if (-glyph.yOffset > y) {
        y = -glyph.yOffset;
      }
    }
    return y;
  }
}

class Character {
  constructor(
      public font: Font, public glyph: Glyph, public x: number,
      public y: number, public size: number) {}

  public getRight(): number {
    return this.x + (this.glyph.xOffset + this.glyph.width) * this.size;
  }

  public getBottom(): number {
    return this.y + (this.glyph.yOffset + this.glyph.height) * this.size;
  }
}

const REPO_RAW_URL = 'https://raw.githubusercontent.com/shapoco/shapofont/refs/heads/main/';

/**
 * Short prefixes accepted in the `u=` hash parameter and their expansions.
 * The first match wins, so more specific prefixes come first.
 */
const URL_PREFIXES: [string, string][] = [
  ['/shapofont/lvgl/', REPO_RAW_URL + 'lvgl/'],
  ['/shapofont/', REPO_RAW_URL + 'gfxfont/cpp/include/'],
  ['/ghuc/', 'https://raw.githubusercontent.com/'],
  ['/gist/', 'https://gist.githubusercontent.com/'],
];

/**
 * Converts a URL the user pasted from the browser's address bar into a URL whose
 * content can be fetched from this page (CORS allowed). Only GitHub and Gist are accepted.
 */
function resolveFontUrl(input: string): string {
  input = input.trim();
  for (const [key, prefix] of URL_PREFIXES) {
    if (input.startsWith(key)) return prefix + input.slice(key.length);
  }

  let url: URL;
  try {
    url = new URL(input);
  } catch {
    throw new Error('Invalid URL.');
  }
  if (url.protocol !== 'https:') throw new Error('Only https:// URLs are accepted.');
  const parts = url.pathname.split('/').filter(p => p !== '');

  switch (url.hostname) {
    case 'raw.githubusercontent.com':
    case 'gist.githubusercontent.com':
      return url.origin + url.pathname;

    case 'github.com': {
      // https://github.com/<user>/<repo>/(blob|raw)/<ref>/<path>
      if (parts.length < 5 || !['blob', 'raw'].includes(parts[2])) {
        throw new Error('GitHub URL must point to a file: https://github.com/<user>/<repo>/blob/<branch>/<path>');
      }
      const [user, repo, , ...rest] = parts;
      return `https://raw.githubusercontent.com/${user}/${repo}/${rest.join('/')}`;
    }

    case 'gist.github.com': {
      // https://gist.github.com/<user>/<id>[#file-<name>]
      if (parts.length < 2) throw new Error('Gist URL must be https://gist.github.com/<user>/<id>');
      const [user, id] = parts;
      const mFile = /^file-(.+)$/.exec(url.hash.slice(1));
      const file = mFile ? mFile[1].replace(/-([^-]*)$/, '.$1') : '';
      return `https://gist.githubusercontent.com/${user}/${id}/raw/${file}`;
    }

    default:
      throw new Error(`Unsupported host: ${url.hostname} (GitHub and Gist only)`);
  }
}

/** Shortens a fetchable URL with the known prefixes, for a compact `u=` hash parameter. */
function shortenFontUrl(url: string): string {
  for (const [key, prefix] of URL_PREFIXES) {
    if (url.startsWith(prefix)) return key + url.slice(prefix.length);
  }
  return url;
}

function parseHashParams(hash: string): Map<string, string> {
  const params = new Map<string, string>();
  if (hash.startsWith('#')) hash = hash.slice(1);
  for (const param of hash.split('&')) {
    if (param === '') continue;
    const i = param.indexOf('=');
    if (i < 0) continue;
    params.set(param.slice(0, i), decodeURIComponent(param.slice(i + 1)));
  }
  return params;
}

class App {
  private parseRequestId = -1;
  private updatePreviewRequestId = -1;
  private font: Font|null = null;
  private fontUrlBox: HTMLInputElement;
  private fontUrlLoadButton: HTMLButtonElement;
  private fontUrlLog: HTMLSpanElement;
  private fontSrcBox: HTMLTextAreaElement;
  private sampleTextBox: HTMLTextAreaElement;
  private screenSizeBox: HTMLSelectElement;
  private originXBox: HTMLInputElement;
  private originY1Box: HTMLInputElement;
  private originYAutoOffsetBox: HTMLInputElement;
  private xAdvanceAdjustBox: HTMLInputElement;
  private yAdvanceAdjustBox: HTMLInputElement;
  private zoomBox: HTMLSelectElement;
  private dotEmphasisBox: HTMLInputElement;
  private fgColorBox: HTMLInputElement;
  private bgColorBox: HTMLInputElement;
  private logBox: HTMLPreElement;

  constructor() {
    this.fontUrlBox = document.querySelector('#font-url') as HTMLInputElement;
    this.fontUrlLoadButton = document.querySelector('#font-url-load') as HTMLButtonElement;
    this.fontUrlLog = document.querySelector('#font-url-log') as HTMLSpanElement;
    this.fontSrcBox =
        document.querySelector('#font-src') as HTMLTextAreaElement;
    this.sampleTextBox =
        document.querySelector('#sample-text') as HTMLTextAreaElement;
    this.screenSizeBox =
        document.querySelector('#screen-size') as HTMLSelectElement;
    this.originXBox = document.querySelector('#origin-x') as HTMLInputElement;
    this.originY1Box = document.querySelector('#origin-y') as HTMLInputElement;
    this.originYAutoOffsetBox =
        document.querySelector('#origin-y-auto-offset') as HTMLInputElement;
    this.xAdvanceAdjustBox =
        document.querySelector('#x-advance-adjust') as HTMLInputElement;
    this.yAdvanceAdjustBox =
        document.querySelector('#y-advance-adjust') as HTMLInputElement;
    this.zoomBox = document.querySelector('#zoom') as HTMLSelectElement;
    this.dotEmphasisBox =
        document.querySelector('#dot-emphasis') as HTMLInputElement;
    this.fgColorBox = document.querySelector('#fg-color') as HTMLInputElement;
    this.bgColorBox = document.querySelector('#bg-color') as HTMLInputElement;
    this.logBox = document.querySelector('#log') as HTMLPreElement;

    this.fontUrlLoadButton.addEventListener('click', () => {
      this.loadFontFromUrl(this.fontUrlBox.value, true);
    });
    this.fontUrlBox.addEventListener('keydown', (e: KeyboardEvent) => {
      if (e.key === 'Enter') this.loadFontFromUrl(this.fontUrlBox.value, true);
    });
    this.fontUrlBox.addEventListener('paste', () => {
      // The pasted text is in the box after this event has been handled
      setTimeout(() => this.loadFontFromUrl(this.fontUrlBox.value, true), 0);
    });
    this.fontSrcBox.addEventListener('input', () => {
      this.requestParse();
    });
    this.sampleTextBox.addEventListener('input', () => {
      this.requestUpdatePreview();
    });

    const renderOptions = document.querySelector('#render-options');
    for (let box of renderOptions.querySelectorAll('input, select')) {
      box.addEventListener('change', () => this.requestUpdatePreview());
      box.addEventListener('input', () => this.requestUpdatePreview());
    }

    const previewOptions = document.querySelector('#preview-options');
    for (let box of previewOptions.querySelectorAll('input, select')) {
      box.addEventListener('change', () => this.requestUpdatePreview());
      box.addEventListener('input', () => this.requestUpdatePreview());
    }

    document.querySelector('#color-swap').addEventListener('click', () => {
      const fg = this.fgColorBox.value;
      const bg = this.bgColorBox.value;
      this.fgColorBox.value = bg;
      this.bgColorBox.value = fg;
      this.requestUpdatePreview();
    });

    document.querySelector('#color-rotate').addEventListener('click', () => {
      for (const box of [this.fgColorBox, this.bgColorBox]) {
        const rgb = parseColor(box.value);
        const tmp = rgb[2];
        rgb[2] = rgb[1];
        rgb[1] = rgb[0];
        rgb[0] = tmp;
        box.value = encodeColor(rgb);
      }
      this.requestUpdatePreview();
    });
  }

  async init() {
    const DEFAULT_FONT_URL = REPO_RAW_URL + 'gfxfont/cpp/include/ShapoSansP_s12c09a01w02.h';
    let sampleText =
        ' !"#$%&\'()*+,-./\n0123456789:;<=>?\n@ABCDEFGHIJKLMNO\nPQRSTUVWXYZ[\\]^_\n`abcdefghijklmno\npqrstuvwxyz{|}~';
    let srcUrl = DEFAULT_FONT_URL;

    for (const [key, value] of parseHashParams(window.location.hash)) {
      switch (key) {
        case 'u':
          srcUrl = value;
          break;
        case 't':
          sampleText = value;
          break;
        case 's':
          this.screenSizeBox.value = value;
          break;
        case 'fg':
          this.fgColorBox.value = '#' + value;
          break;
        case 'bg':
          this.bgColorBox.value = '#' + value;
          break;
      }
    }

    this.sampleTextBox.value = sampleText;
    await this.loadFontFromUrl(srcUrl, false);
  }

  /** Fetches a font source from a GitHub/Gist URL into the source box and parses it. */
  private async loadFontFromUrl(input: string, updateHash: boolean): Promise<void> {
    if (input.trim() === '') return;
    let url: string;
    try {
      url = resolveFontUrl(input);
    } catch (error) {
      this.setUrlLog(`Error: ${error.message}`, true);
      return;
    }

    this.fontUrlBox.value = url;
    this.fontUrlLoadButton.disabled = true;
    this.setUrlLog(`Loading ${url} ...`, false);
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status} ${response.statusText}`);
      }
      this.fontSrcBox.value = await response.text();
      this.setUrlLog(`Loaded ${url} (${this.fontSrcBox.value.length} chars)`, false);
      if (updateHash) this.updateHash(url);
      this.runParse();
    } catch (error) {
      // fetch() reports CORS and network failures as TypeError without details
      const reason = error instanceof TypeError ? 'network error or the host does not allow cross-origin access' : error.message;
      this.setUrlLog(`Error: failed to load ${url}: ${reason}`, true);
    } finally {
      this.fontUrlLoadButton.disabled = false;
    }
  }

  private updateHash(url: string): void {
    const params = parseHashParams(window.location.hash);
    params.set('u', shortenFontUrl(url));
    const hash = '#' + Array.from(params).map(([k, v]) => `${k}=${encodeURIComponent(v)}`).join('&');
    history.replaceState(null, '', window.location.pathname + window.location.search + hash);
  }

  private setUrlLog(msg: string, isError: boolean): void {
    this.fontUrlLog.textContent = msg;
    this.fontUrlLog.style.color = isError ? '#f66' : '#0cf';
    if (isError) console.error(msg);
  }

  private requestParse(): void {
    if (this.parseRequestId >= 0) clearTimeout(this.parseRequestId);
    this.parseRequestId = setTimeout(() => this.runParse(), 300);
  }

  private runParse(): void {
    if (this.parseRequestId >= 0) {
      clearTimeout(this.parseRequestId);
      this.parseRequestId = -1;
    }

    const fontSrc = this.fontSrcBox.value;

    try {
      const font = new Font(fontSrc);
      this.font = font;

      this.logInfo(
          `format: ${font.format}, ` +
          `glyphs: ${font.glyphs.size}, ` +
          `firstCode: ${codeToStr(font.firstCode)}, ` +
          `lastCode: ${codeToStr(font.lastCode)}, ` +
          `yAdvance: ${font.yAdvance}`);
    } catch (error) {
      this.font = null;
      this.logError(error.message);
    }

    this.requestUpdatePreview();
  }

  private getTextSize(): number {
    return Number((document.querySelector('input[name="text-size"]:checked') as
                   HTMLInputElement)
                      .value);
  }

  private requestUpdatePreview(): void {
    if (this.updatePreviewRequestId >= 0) clearTimeout(this.updatePreviewRequestId);
    this.updatePreviewRequestId = setTimeout(() => this.updatePreview(), 300);
  }

  private updatePreview(): void {
    if (this.updatePreviewRequestId >= 0) {
      clearTimeout(this.updatePreviewRequestId);
      this.updatePreviewRequestId = -1;
    }

    const canvas =
        document.querySelector('#preview-canvas') as HTMLCanvasElement;

    const font = this.font;
    if (!font) {
      const ctx = canvas.getContext('2d');
      ctx.fillStyle = '#f00';
      ctx.fillText('No font loaded', 10, 20);
      return;
    }

    const text = this.sampleTextBox.value;
    const originX = Number(this.originXBox.value);
    const textSize = this.getTextSize();
    const originY = Number(this.originY1Box.value);
    let offsettedOriginY = originY;
    if (this.originYAutoOffsetBox.checked) {
      offsettedOriginY += this.font.getPreferredOriginY() * textSize;
    }
    const xAdvanceAdjust = Number(this.xAdvanceAdjustBox.value);
    const yAdvanceAdjust = Number(this.yAdvanceAdjustBox.value);
    const zoom = Number(this.zoomBox.value);
    const bgColorStr = this.bgColorBox.value;
    const fgColorStr = this.fgColorBox.value;

    const chars = this.layoutChars(
        font, text, originX, offsettedOriginY, textSize, xAdvanceAdjust,
        yAdvanceAdjust);

    let textRight = originX;
    let textBottom = originY;
    for (const c of chars) {
      textRight = Math.max(textRight, c.getRight());
      textBottom = Math.max(textBottom, c.getBottom());
    }
    const textWidth = textRight - originX;
    const textHeight = textBottom - originY;

    const screenSizeStr = this.screenSizeBox.value;
    let [screenWidth, screenHeight] = screenSizeStr.split('x').map(Number);
    if (screenWidth <= 0) {
      screenWidth = Math.max(128, Math.ceil(textRight * 1.1 / 20) * 20);
    }
    if (screenHeight <= 0) {
      screenHeight = Math.max(32, Math.ceil(textBottom * 1.1 / 20) * 20);
    }

    const dotEmphasisAllowed = screenWidth < 320 && screenHeight < 320;
    this.dotEmphasisBox.disabled = !dotEmphasisAllowed;
    const dotEmphasis = this.dotEmphasisBox.checked && dotEmphasisAllowed;

    let dotSize = zoom;
    if (dotSize <= 0) {
      dotSize = Math.ceil(2000 / Math.max(screenWidth, screenHeight));
      dotSize = Math.max(1, Math.min(8, dotSize));
    }

    canvas.width = screenWidth * dotSize;
    canvas.height = screenHeight * dotSize;

    if (zoom > 0) {
      canvas.style.imageRendering = 'pixelated';
      canvas.style.width = `${screenWidth * zoom}px`;
    } else {
      canvas.style.imageRendering = 'auto';
      canvas.style.width = '100%';
    }

    const ctx = canvas.getContext('2d');
    ctx.fillStyle = bgColorStr;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    {
      const lw = Math.max(1, screenWidth * dotSize / 900);
      // ctx.fillStyle = '#666';
      // ctx.fillRect(originX * dotSize - lw / 2, 0, lw, canvas.height);
      // ctx.fillRect(0, originY * dotSize - lw / 2, canvas.width, lw);
      // ctx.fillRect(textRight * dotSize - lw / 2, 0, lw, canvas.height);
      // ctx.fillRect(0, textBottom * dotSize - lw / 2, canvas.width, lw);
      ctx.strokeStyle = '#666';
      ctx.lineWidth = lw;
      ctx.strokeRect(
          originX * dotSize, originY * dotSize, textWidth * dotSize,
          textHeight * dotSize);


      ctx.strokeStyle = '#f00';
      ctx.lineWidth = lw;
      ctx.strokeRect(
          originX * dotSize - lw * 4, offsettedOriginY * dotSize - lw * 4,
          lw * 8, lw * 8);

      ctx.font = `${Math.ceil(lw * 16)}px sans-serif`;
      ctx.fillStyle = '#666';
      ctx.textBaseline = 'top';
      ctx.fillText(
          `${textWidth}x${textHeight}`, originX * dotSize,
          textBottom * dotSize);
    }

    for (const c of chars) {
      c.glyph.render(
          ctx, c.x * dotSize, c.y * dotSize, c.size, dotSize, dotEmphasis,
          fgColorStr);
    }
  }

  private layoutChars(
      font: Font, text: string, x: number, y: number, size: number,
      xAdvanceAdjust: number, yAdvanceAdjust: number): Character[] {
    let cursorX = x;
    let cursorY = y;
    const characters: Character[] = [];
    for (let c of text) {
      const code = c.codePointAt(0);
      if (code == 0x0a) {
        cursorX = x;
        cursorY += font.yAdvance * size + yAdvanceAdjust;
      } else if (font.glyphs.has(code)) {
        const glyph = font.glyphs.get(code);
        if (glyph) {
          characters.push(new Character(font, glyph, cursorX, cursorY, size));
          cursorX += glyph.xAdvance * size + xAdvanceAdjust;
        }
      }
    }
    return characters;
  }

  private logError(msg) {
    console.error(msg);
    this.logBox.textContent = `Error: ${msg}`;
    this.logBox.style.color = '#c00';
  }

  private logInfo(msg) {
    this.logBox.textContent = msg;
    this.logBox.style.color = '#0cf';
  }
}

document.addEventListener('DOMContentLoaded', async () => {
  const app = new App();
  await app.init();
});
