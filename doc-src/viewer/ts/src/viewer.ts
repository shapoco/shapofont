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

enum ScanType {
  HORIZONTAL_PACKED,
  HORIZONTAL_FRAGMENT,
  VERTICAL_FRAGMENT,
}

class GrayBitmap {
  public scanType: ScanType;
  public msb1st: boolean;
  public width: number;
  public height: number;
  public data: Uint8Array;

  constructor(
      width: number, height: number, data: Uint8Array, scanType: ScanType,
      msb1st: boolean = false) {
    this.scanType = scanType;
    this.msb1st = msb1st;
    this.width = width;
    this.height = height;

    const grayData = new Uint8Array(width * height);

    switch (scanType) {
      case ScanType.HORIZONTAL_PACKED: {
        let ibyte = 0;
        let ibit = 0;
        let sreg = 0;
        for (let y = 0; y < height; y++) {
          for (let x = 0; x < width; x++) {
            if (ibit == 0) {
              sreg = data[ibyte++];
              if (msb1st) sreg = reverseByte(sreg);
              ibit = 8;
            }
            grayData[y * width + x] = ((sreg & 1) == 0) ? 0x00 : 0xFF;
            sreg >>= 1;
            ibit--;
          }
        }
      } break;

      default:
        throw new Error(`Unsupported scan type: ${scanType}`);
    }

    this.data = grayData;
  }
}

class Glyph {
  public dataOffset: number;
  public bitmap: GrayBitmap|null;
  public width: number;
  public height: number;
  public xAdvance: number;
  public xOffset: number;
  public yOffset: number;

  constructor(
      dataOffset: number, bitmap: GrayBitmap|null, width: number,
      height: number, xAdvance: number, xOffset: number, yOffset: number) {
    this.dataOffset = dataOffset;
    this.bitmap = bitmap;
    this.width = width;
    this.height = height;
    this.xAdvance = xAdvance;
    this.xOffset = xOffset;
    this.yOffset = yOffset;
  }

  public render(
      ctx: CanvasRenderingContext2D, x: number, y: number, size: number) {
    if (!this.bitmap) return;

    ctx.save();
    ctx.translate(x + this.xOffset * size, y + this.yOffset * size);
    ctx.scale(size, size);
    for (let y = 0; y < this.height; y++) {
      for (let x = 0; x < this.width; x++) {
        const pixel = this.bitmap.data[y * this.width + x];
        ctx.fillStyle = `rgb(${pixel}, ${pixel}, ${pixel})`;
        ctx.fillRect(x, y, 1, 1);
      }
    }
    ctx.restore();
  }
}

class Font {
  public src: string;
  public firstCode: number;
  public lastCode: number;
  public yAdvance: number;
  public glyphs: Map<number, Glyph> = new Map();

  constructor(src: string) {
    this.src = src;

    let success = false;
    if (!success) success = this.tryParseGfxFont(src);
    if (!success) throw new Error('Failed to parse font source');
  }

  tryParseGfxFont(src: string): boolean {
    src = src.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/.*$/gm, '');

    const mGfxFont = /GFXfont\s+(\w+)(\s*\w+)?\s*=\s*\{([^\}]+)\}/gm.exec(src);
    if (!mGfxFont) return false;

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
}

class App {
  private parseRequestId = -1;
  private updatePreviewRequestId = -1;
  private font: Font|null = null;

  constructor() {
    document.querySelector('#parse-btn').addEventListener('click', () => {
      this.runParse();
    });
    document.querySelector('#font-src').addEventListener('input', () => {
      this.requestParse();
    });
    document.querySelector('#sample-text').addEventListener('input', () => {
      this.requestUpdatePreview();
    });

    this.runParse();
  }

  private requestParse(): void {
    if (this.parseRequestId >= 0) {
      clearTimeout(this.parseRequestId);
    }
    this.parseRequestId = setTimeout(() => this.runParse(), 300);
  }

  private runParse(): void {
    const fontSrc =
        (document.querySelector('#font-src') as HTMLTextAreaElement).value;
    const output = document.querySelector('#output');
    output.innerHTML = '';  // Clear previous output

    try {
      const font = new Font(fontSrc);
      this.font = font;

      output.innerHTML = `firstCode: ${codeToStr(font.firstCode)}, ` +
          `lastCode: ${codeToStr(font.lastCode)}, ` +
          `yAdvance: ${font.yAdvance}`;

      let sampleText = '';
      for (const code of font.glyphs.keys()) {
        sampleText += String.fromCodePoint(code);
        if ((code + 1) % 16 == 0) {
          sampleText += '\n';
        }
      }
      (document.querySelector('#sample-text') as HTMLTextAreaElement).value =
          sampleText;
    } catch (error) {
      this.font = null;
      output.innerHTML = `Error: ${error.message}`;
    }

    this.requestUpdatePreview();
  }

  private requestUpdatePreview(): void {
    if (this.updatePreviewRequestId >= 0) {
      clearTimeout(this.updatePreviewRequestId);
    }
    this.updatePreviewRequestId = setTimeout(() => this.updatePreview(), 300);
  }

  private updatePreview(): void {
    this.updatePreviewRequestId = -1;

    const previewCanvas =
        document.querySelector('#text-preview') as HTMLCanvasElement;
    const ctx = previewCanvas.getContext('2d');
    if (!ctx) return;

    ctx.fillStyle = '#222';
    ctx.fillRect(0, 0, previewCanvas.width, previewCanvas.height);

    const font = this.font;
    const text =
        (document.querySelector('#sample-text') as HTMLTextAreaElement).value;

    let size = 2;
    let x = 16;
    let y = 16 + font.yAdvance * size;
    for (let c of text) {
      const code = c.codePointAt(0);
      if (code == 0x0a) {
        x = 16;
        y += font.yAdvance * size;
      } else if (font.glyphs.has(code)) {
        const glyph = font.glyphs.get(code);
        if (glyph) {
          glyph.render(ctx, x, y, size);
          x += glyph.xAdvance * size;
        }
      }
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  new App();
});
