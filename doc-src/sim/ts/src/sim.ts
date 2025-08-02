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
  public grayData: Uint8Array;

  constructor(
      public width: number, public height: number, public rawData: Uint8Array,
      public scanType: ScanType, public msb1st: boolean = false) {
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
      dotSize: number, dotEmphasis: boolean, rgb: string) {
    if (!this.bitmap) return;

    const multSize = textSize * dotSize;

    ctx.save();
    ctx.translate(x + this.xOffset * multSize, y + this.yOffset * multSize);
    for (let y = 0; y < this.height; y++) {
      for (let x = 0; x < this.width; x++) {
        const pixel =
            Math.round(100 * this.bitmap.grayData[y * this.width + x] / 255);
        ctx.fillStyle = `rgb(${rgb} / ${pixel}%)`;
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
  public firstCode: number;
  public lastCode: number;
  public yAdvance: number;
  public glyphs: Map<number, Glyph> = new Map();

  constructor(public src: string) {
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
}

class App {
  private parseRequestId = -1;
  private updatePreviewRequestId = -1;
  private font: Font|null = null;
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

  constructor() {
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

    this.fontSrcBox.addEventListener('input', () => {
      this.requestParse();
    });
    this.sampleTextBox.addEventListener('input', () => {
      this.requestUpdatePreview();
    });

    const renderOptions = document.querySelector('#render-options');
    for (let box of renderOptions.querySelectorAll('input, select')) {
      box.addEventListener('change', () => {
        this.requestUpdatePreview();
      });
    }

    const previewOptions = document.querySelector('#preview-options');
    for (let box of previewOptions.querySelectorAll('input, select')) {
      box.addEventListener('change', () => {
        this.requestUpdatePreview();
      });
    }

    this.sampleTextBox.value =
        ' !"#$%&\'()*+,-./\n0123456789:;<=>?\n@ABCDEFGHIJKLMNO\nPQRSTUVWXYZ[\\]^_\n`abcdefghijklmno\npqrstuvwxyz{|}~';
  }

  async init() {
    const fontSrc = await fetch(
        'https://raw.githubusercontent.com/shapoco/shapofont/refs/heads/main/gfxfont/cpp/include/ShapoSansP_s27c22a01w04.h');
    const fontText = await fontSrc.text();
    (document.querySelector('#font-src') as HTMLTextAreaElement).value =
        fontText;
    this.runParse();
  }

  private requestParse(): void {
    this.parseRequestId = setTimeout(() => this.runParse(), 300);
  }

  private runParse(): void {
    if (this.parseRequestId >= 0) {
      clearTimeout(this.parseRequestId);
      this.parseRequestId = -1;
    }

    const fontSrc = this.fontSrcBox.value;
    const log = document.querySelector('#log');
    log.innerHTML = '';  // Clear previous output

    try {
      const font = new Font(fontSrc);
      this.font = font;

      log.innerHTML = `firstCode: ${codeToStr(font.firstCode)}, ` +
          `lastCode: ${codeToStr(font.lastCode)}, ` +
          `yAdvance: ${font.yAdvance}`;
    } catch (error) {
      this.font = null;
      log.innerHTML = `Error: ${error.message}`;
    }

    this.requestUpdatePreview();
  }

  private getTextSize(): number {
    return Number((document.querySelector('input[name="text-size"]:checked') as
                   HTMLInputElement)
                      .value);
  }

  private requestUpdatePreview(): void {
    this.updatePreviewRequestId = setTimeout(() => this.updatePreview(), 300);
  }

  private updatePreview(): void {
    if (this.updatePreviewRequestId >= 0) {
      clearTimeout(this.updatePreviewRequestId);
      this.updatePreviewRequestId = -1;
    }

    const previewCanvas =
        document.querySelector('#preview-canvas') as HTMLCanvasElement;

    const font = this.font;
    if (!font) {
      const ctx = previewCanvas.getContext('2d');
      ctx.fillStyle = '#f00';
      ctx.fillText('No font loaded', 10, 20);
      return;
    }

    const text = this.sampleTextBox.value;
    const screenSizeStr = this.screenSizeBox.value;
    const [screenWidth, screenHeight] = screenSizeStr.split('x').map(Number);
    const zoom = Number(this.zoomBox.value);
    const dotEmphasis = this.dotEmphasisBox.checked;
    const textSize = this.getTextSize();
    const originX = Number(this.originXBox.value);
    let originY = Number(this.originY1Box.value);
    if (this.originYAutoOffsetBox.checked) {
      originY += this.font.getPreferredOriginY() * textSize;
    }
    const xAdvanceAdjust = Number(this.xAdvanceAdjustBox.value);
    const yAdvanceAdjust = Number(this.yAdvanceAdjustBox.value);

    const chars = this.layoutChars(
        font, text, originX, originY, textSize, xAdvanceAdjust, yAdvanceAdjust);

    let dotSize = zoom;
    if (dotSize <= 0) {
      dotSize = Math.ceil(2000 / Math.max(screenWidth, screenHeight));
      dotSize = Math.max(1, Math.min(8, dotSize));
    }

    previewCanvas.width = screenWidth * dotSize;
    previewCanvas.height = screenHeight * dotSize;

    if (zoom > 0) {
      previewCanvas.style.imageRendering = 'pixelated';
      previewCanvas.style.width = `${screenWidth * zoom}px`;
    } else {
      previewCanvas.style.imageRendering = 'auto';
      previewCanvas.style.width = '100%';
    }

    const ctx = previewCanvas.getContext('2d');
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, previewCanvas.width, previewCanvas.height);

    for (const c of chars) {
      c.glyph.render(
          ctx, c.x * dotSize, c.y * dotSize, c.size, dotSize, dotEmphasis,
          '255 255 255');
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
}

document.addEventListener('DOMContentLoaded', async () => {
  const app = new App();
  await app.init();
});
