var __values = (this && this.__values) || function(o) {
    var s = typeof Symbol === "function" && Symbol.iterator, m = s && o[s], i = 0;
    if (m) return m.call(o);
    if (o && typeof o.length === "number") return {
        next: function () {
            if (o && i >= o.length) o = void 0;
            return { value: o && o[i++], done: !o };
        }
    };
    throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
};
function parseCInt(name, s) {
    s = s.trim();
    var sign = 1;
    if (s.startsWith('-')) {
        sign = -1;
        s = s.slice(1).trim();
    }
    if (/^0x([0-9a-fA-F]+)$/.test(s)) {
        return sign * parseInt(s.slice(2), 16);
    }
    else if (/^0[0-7]+$/.test(s)) {
        return sign * parseInt(s, 8);
    }
    else if (/^0b[01]+$/.test(s)) {
        return sign * parseInt(s.slice(2), 2);
    }
    else if (/^[0-9]+$/.test(s)) {
        return sign * parseInt(s, 10);
    }
    throw new Error("Failed to parse ".concat(name, ": ").concat(s));
}
function codeToStr(code) {
    if (code < 0 || code > 0x10FFFF) {
        throw new Error("Invalid Unicode code point: ".concat(code));
    }
    return "'".concat(String.fromCodePoint(code), "' (0x").concat(code.toString(16).toUpperCase(), ")");
}
function reverseByte(byte) {
    byte = ((byte << 4) & 0xF0) | ((byte >> 4) & 0x0F);
    byte = ((byte & 0xCC) >> 2) | ((byte & 0x33) << 2);
    byte = ((byte & 0xAA) >> 1) | ((byte & 0x55) << 1);
    return byte;
}
var ScanType;
(function (ScanType) {
    ScanType[ScanType["HORIZONTAL_PACKED"] = 0] = "HORIZONTAL_PACKED";
    ScanType[ScanType["HORIZONTAL_FRAGMENT"] = 1] = "HORIZONTAL_FRAGMENT";
    ScanType[ScanType["VERTICAL_FRAGMENT"] = 2] = "VERTICAL_FRAGMENT";
})(ScanType || (ScanType = {}));
var GrayBitmap = /** @class */ (function () {
    function GrayBitmap(width, height, data, scanType, msb1st) {
        if (msb1st === void 0) { msb1st = false; }
        this.scanType = scanType;
        this.msb1st = msb1st;
        this.width = width;
        this.height = height;
        var grayData = new Uint8Array(width * height);
        switch (scanType) {
            case ScanType.HORIZONTAL_PACKED:
                {
                    var ibyte = 0;
                    var ibit = 0;
                    var sreg = 0;
                    for (var y = 0; y < height; y++) {
                        for (var x = 0; x < width; x++) {
                            if (ibit == 0) {
                                sreg = data[ibyte++];
                                if (msb1st)
                                    sreg = reverseByte(sreg);
                                ibit = 8;
                            }
                            grayData[y * width + x] = ((sreg & 1) == 0) ? 0x00 : 0xFF;
                            sreg >>= 1;
                            ibit--;
                        }
                    }
                }
                break;
            default:
                throw new Error("Unsupported scan type: ".concat(scanType));
        }
        this.data = grayData;
    }
    return GrayBitmap;
}());
var Glyph = /** @class */ (function () {
    function Glyph(dataOffset, bitmap, width, height, xAdvance, xOffset, yOffset) {
        this.dataOffset = dataOffset;
        this.bitmap = bitmap;
        this.width = width;
        this.height = height;
        this.xAdvance = xAdvance;
        this.xOffset = xOffset;
        this.yOffset = yOffset;
    }
    Glyph.prototype.render = function (ctx, x, y, size) {
        if (!this.bitmap)
            return;
        ctx.save();
        ctx.translate(x + this.xOffset * size, y + this.yOffset * size);
        ctx.scale(size, size);
        for (var y_1 = 0; y_1 < this.height; y_1++) {
            for (var x_1 = 0; x_1 < this.width; x_1++) {
                var pixel = this.bitmap.data[y_1 * this.width + x_1];
                ctx.fillStyle = "rgb(".concat(pixel, ", ").concat(pixel, ", ").concat(pixel, ")");
                ctx.fillRect(x_1, y_1, 1, 1);
            }
        }
        ctx.restore();
    };
    return Glyph;
}());
var Font = /** @class */ (function () {
    function Font(src) {
        this.glyphs = new Map();
        this.src = src;
        var success = false;
        if (!success)
            success = this.tryParseGfxFont(src);
        if (!success)
            throw new Error('Failed to parse font source');
    }
    Font.prototype.tryParseGfxFont = function (src) {
        var e_1, _a;
        src = src.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/.*$/gm, '');
        var mGfxFont = /GFXfont\s+(\w+)(\s*\w+)?\s*=\s*\{([^\}]+)\}/gm.exec(src);
        if (!mGfxFont)
            return false;
        var fontParams = mGfxFont[3].split(',');
        if (fontParams.length < 5) {
            throw new Error('Too few parameters for struct GFXfont');
        }
        var mBitmaps = /^(\([^\)]+\)\s*)?(\w+)$/.exec(fontParams[0].trim());
        if (!mBitmaps)
            throw new Error('Failed to parse GFXfont.bitmap');
        var mGlyphs = /^(\([^\)]+\)\s*)?(\w+)$/.exec(fontParams[1].trim());
        if (!mGlyphs)
            throw new Error('Failed to parse GFXfont.glyph');
        this.firstCode = parseCInt('GFXfont.first', fontParams[2].trim());
        this.lastCode = parseCInt('GFXfont.last', fontParams[3].trim());
        this.yAdvance = parseCInt('GFXfont.yAdvance', fontParams[4].trim());
        var bmpArrayName = mBitmaps[2];
        var regexBmpArray = new RegExp("\\b(uint8_t|unsigned\\s+char)\\s+".concat(bmpArrayName) +
            "\\s*\\[\\s*\\](\\s*\\w+)?\\s*=\\s*\\{([^\\}]+)\\}", 'gm');
        var mBmpArray = regexBmpArray.exec(src);
        if (!mBmpArray) {
            throw new Error("Failed to find bitmap array: ".concat(bmpArrayName));
        }
        var bitmapData = new Uint8Array(mBmpArray[3]
            .split(',')
            .filter(function (s) { return s.trim() !== ''; })
            .map(function (s) { return parseCInt('bitmap data', s); }));
        var glyphArrayName = mGlyphs[2];
        var regexGlyphArray = new RegExp("\\bGFXglyph\\s*".concat(glyphArrayName) +
            "\\s*\\[\\s*\\](\\s*\\w+)?\\s*=\\s*\\{([^\\;]+)\\}\\s*;", 'gm');
        var mGlyphArray = regexGlyphArray.exec(src);
        if (!mGlyphArray) {
            throw new Error("Failed to find glyph array: ".concat(glyphArrayName));
        }
        var code = this.firstCode;
        try {
            for (var _b = __values(mGlyphArray[2].split(/}\s*,/)), _c = _b.next(); !_c.done; _c = _b.next()) {
                var glyphIniter = _c.value;
                glyphIniter = glyphIniter.trim();
                if (glyphIniter.endsWith('}')) {
                    glyphIniter = glyphIniter.slice(0, -1).trimEnd();
                }
                if (glyphIniter === '')
                    continue;
                if (glyphIniter.startsWith('{')) {
                    glyphIniter = glyphIniter.slice(1).trimStart();
                }
                else {
                    throw new Error("Failed to parse GFXglyph initialization: ".concat(glyphIniter));
                }
                var glyphParams = glyphIniter.split(',').map(function (s) { return s.trim(); });
                if (glyphParams.length < 6) {
                    throw new Error("Too few parameters for GFXglyph: ".concat(glyphParams.length));
                }
                var iBmpStart = parseCInt('GFXglyph.bitmapOffset', glyphParams[0]);
                var w = parseCInt('GFXglyph.width', glyphParams[1]);
                var h = parseCInt('GFXglyph.height', glyphParams[2]);
                var xAdvance = parseCInt('GFXglyph.xAdvance', glyphParams[3]);
                var xOffset = parseCInt('GFXglyph.xOffset', glyphParams[4]);
                var yOffset = parseCInt('GFXglyph.yOffset', glyphParams[5]);
                var bmp = null;
                if (w > 0 && h > 0) {
                    var iBmpEnd = iBmpStart + Math.ceil(w * h / 8);
                    if (iBmpStart < 0 || bitmapData.length <= iBmpStart) {
                        throw new Error("GFXglyph.bitmapOffset out of range: ".concat(iBmpStart));
                    }
                    if (iBmpEnd < 1 || bitmapData.length < iBmpEnd) {
                        throw new Error("End of bitmap data out of range: ".concat(iBmpEnd));
                    }
                    var numBmpBytes = Math.ceil(w * h / 8);
                    bmp = new GrayBitmap(w, h, bitmapData.subarray(iBmpStart, iBmpStart + numBmpBytes), ScanType.HORIZONTAL_PACKED, true);
                }
                else {
                    bmp = new GrayBitmap(w, h, new Uint8Array(0), ScanType.HORIZONTAL_PACKED, true);
                }
                var glyph = new Glyph(iBmpStart, bmp, w, h, xAdvance, xOffset, yOffset);
                this.glyphs.set(code, glyph);
                code++;
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return true;
    };
    return Font;
}());
var App = /** @class */ (function () {
    function App() {
        var _this = this;
        this.parseRequestId = -1;
        this.updatePreviewRequestId = -1;
        this.font = null;
        document.querySelector('#parse-btn').addEventListener('click', function () {
            _this.runParse();
        });
        document.querySelector('#font-src').addEventListener('input', function () {
            _this.requestParse();
        });
        document.querySelector('#sample-text').addEventListener('input', function () {
            _this.requestUpdatePreview();
        });
        this.runParse();
    }
    App.prototype.requestParse = function () {
        var _this = this;
        if (this.parseRequestId >= 0) {
            clearTimeout(this.parseRequestId);
        }
        this.parseRequestId = setTimeout(function () { return _this.runParse(); }, 300);
    };
    App.prototype.runParse = function () {
        var e_2, _a;
        var fontSrc = document.querySelector('#font-src').value;
        var output = document.querySelector('#output');
        output.innerHTML = ''; // Clear previous output
        try {
            var font = new Font(fontSrc);
            this.font = font;
            output.innerHTML = "firstCode: ".concat(codeToStr(font.firstCode), ", ") +
                "lastCode: ".concat(codeToStr(font.lastCode), ", ") +
                "yAdvance: ".concat(font.yAdvance);
            var sampleText = '';
            try {
                for (var _b = __values(font.glyphs.keys()), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var code = _c.value;
                    sampleText += String.fromCodePoint(code);
                    if ((code + 1) % 16 == 0) {
                        sampleText += '\n';
                    }
                }
            }
            catch (e_2_1) { e_2 = { error: e_2_1 }; }
            finally {
                try {
                    if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                }
                finally { if (e_2) throw e_2.error; }
            }
            document.querySelector('#sample-text').value =
                sampleText;
        }
        catch (error) {
            this.font = null;
            output.innerHTML = "Error: ".concat(error.message);
        }
        this.requestUpdatePreview();
    };
    App.prototype.requestUpdatePreview = function () {
        var _this = this;
        if (this.updatePreviewRequestId >= 0) {
            clearTimeout(this.updatePreviewRequestId);
        }
        this.updatePreviewRequestId = setTimeout(function () { return _this.updatePreview(); }, 300);
    };
    App.prototype.updatePreview = function () {
        var e_3, _a;
        this.updatePreviewRequestId = -1;
        var previewCanvas = document.querySelector('#text-preview');
        var ctx = previewCanvas.getContext('2d');
        if (!ctx)
            return;
        ctx.fillStyle = '#222';
        ctx.fillRect(0, 0, previewCanvas.width, previewCanvas.height);
        var font = this.font;
        var text = document.querySelector('#sample-text').value;
        var size = 2;
        var x = 16;
        var y = 16 + font.yAdvance * size;
        try {
            for (var text_1 = __values(text), text_1_1 = text_1.next(); !text_1_1.done; text_1_1 = text_1.next()) {
                var c = text_1_1.value;
                var code = c.codePointAt(0);
                if (code == 0x0a) {
                    x = 16;
                    y += font.yAdvance * size;
                }
                else if (font.glyphs.has(code)) {
                    var glyph = font.glyphs.get(code);
                    if (glyph) {
                        glyph.render(ctx, x, y, size);
                        x += glyph.xAdvance * size;
                    }
                }
            }
        }
        catch (e_3_1) { e_3 = { error: e_3_1 }; }
        finally {
            try {
                if (text_1_1 && !text_1_1.done && (_a = text_1.return)) _a.call(text_1);
            }
            finally { if (e_3) throw e_3.error; }
        }
    };
    return App;
}());
document.addEventListener('DOMContentLoaded', function () {
    new App();
});
