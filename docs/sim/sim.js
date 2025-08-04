var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
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
var __read = (this && this.__read) || function (o, n) {
    var m = typeof Symbol === "function" && o[Symbol.iterator];
    if (!m) return o;
    var i = m.call(o), r, ar = [], e;
    try {
        while ((n === void 0 || n-- > 0) && !(r = i.next()).done) ar.push(r.value);
    }
    catch (error) { e = { error: error }; }
    finally {
        try {
            if (r && !r.done && (m = i["return"])) m.call(i);
        }
        finally { if (e) throw e.error; }
    }
    return ar;
};
var _this = this;
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
function parseColor(colorStr) {
    var rgb6 = colorStr.match(/^#([0-9a-fA-F]{6})$/);
    if (rgb6) {
        return [
            parseInt(rgb6[1].slice(0, 2), 16),
            parseInt(rgb6[1].slice(2, 4), 16),
            parseInt(rgb6[1].slice(4, 6), 16),
        ];
    }
    var rgb3 = colorStr.match(/^#([0-9a-fA-F]{3})$/);
    if (rgb3) {
        return [
            parseInt(rgb3[1].charAt(0) + rgb3[1].charAt(0), 16),
            parseInt(rgb3[1].charAt(1) + rgb3[1].charAt(1), 16),
            parseInt(rgb3[1].charAt(2) + rgb3[1].charAt(2), 16),
        ];
    }
    throw new Error("Invalid color format: ".concat(colorStr));
}
function encodeColor(rgb) {
    var e_1, _a;
    var threeDigits = true;
    try {
        for (var rgb_1 = __values(rgb), rgb_1_1 = rgb_1.next(); !rgb_1_1.done; rgb_1_1 = rgb_1.next()) {
            var ch = rgb_1_1.value;
            if (Math.floor(ch / 16) != ch % 16) {
                threeDigits = false;
                break;
            }
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (rgb_1_1 && !rgb_1_1.done && (_a = rgb_1.return)) _a.call(rgb_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    if (threeDigits) {
        return "#".concat(rgb.map(function (ch) { return ch.toString(16).slice(0, 1); }).join(''));
    }
    else {
        return "#".concat(rgb.map(function (ch) { return ch.toString(16).padStart(2, '0'); }).join(''));
    }
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
    function GrayBitmap(width, height, rawData, scanType, msb1st) {
        if (msb1st === void 0) { msb1st = false; }
        this.width = width;
        this.height = height;
        this.rawData = rawData;
        this.scanType = scanType;
        this.msb1st = msb1st;
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
                                sreg = rawData[ibyte++];
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
        this.grayData = grayData;
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
        this.dataOffset = dataOffset;
        this.bitmap = bitmap;
        this.width = width;
        this.height = height;
        this.xAdvance = xAdvance;
        this.xOffset = xOffset;
        this.yOffset = yOffset;
    }
    Glyph.prototype.render = function (ctx, x, y, textSize, dotSize, dotEmphasis, color) {
        if (!this.bitmap)
            return;
        var multSize = textSize * dotSize;
        var _a = __read(parseColor(color), 3), colR = _a[0], colG = _a[1], colB = _a[2];
        ctx.save();
        ctx.translate(x + this.xOffset * multSize, y + this.yOffset * multSize);
        for (var y_1 = 0; y_1 < this.height; y_1++) {
            for (var x_1 = 0; x_1 < this.width; x_1++) {
                var pixel = Math.round(100 * this.bitmap.grayData[y_1 * this.width + x_1] / 255);
                ctx.fillStyle = "rgb(".concat(colR, " ").concat(colG, " ").concat(colB, " / ").concat(pixel, "%)");
                if (dotSize < 2 || !dotEmphasis) {
                    ctx.fillRect(x_1 * multSize, y_1 * multSize, multSize, multSize);
                }
                else {
                    for (var i = 0; i < textSize; i++) {
                        for (var j = 0; j < textSize; j++) {
                            ctx.fillRect(x_1 * multSize + i * dotSize, y_1 * multSize + j * dotSize, dotSize - 1, dotSize - 1);
                        }
                    }
                }
            }
        }
        ctx.restore();
    };
    return Glyph;
}());
var Font = /** @class */ (function () {
    function Font(src) {
        this.src = src;
        this.glyphs = new Map();
        this.src = src;
        var success = false;
        if (!success)
            success = this.tryParseGfxFont(src);
        if (!success)
            throw new Error('Unknown Font Format');
    }
    Font.prototype.tryParseGfxFont = function (src) {
        var e_2, _a;
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
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_2) throw e_2.error; }
        }
        return true;
    };
    Font.prototype.getPreferredOriginY = function () {
        var e_3, _a;
        var y = 0;
        try {
            for (var _b = __values(this.glyphs.values()), _c = _b.next(); !_c.done; _c = _b.next()) {
                var glyph = _c.value;
                if (-glyph.yOffset > y) {
                    y = -glyph.yOffset;
                }
            }
        }
        catch (e_3_1) { e_3 = { error: e_3_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_3) throw e_3.error; }
        }
        return y;
    };
    return Font;
}());
var Character = /** @class */ (function () {
    function Character(font, glyph, x, y, size) {
        this.font = font;
        this.glyph = glyph;
        this.x = x;
        this.y = y;
        this.size = size;
    }
    Character.prototype.getRight = function () {
        return this.x + (this.glyph.xOffset + this.glyph.width) * this.size;
    };
    Character.prototype.getBottom = function () {
        return this.y + (this.glyph.yOffset + this.glyph.height) * this.size;
    };
    return Character;
}());
var App = /** @class */ (function () {
    function App() {
        var e_4, _a, e_5, _b;
        var _this = this;
        this.parseRequestId = -1;
        this.updatePreviewRequestId = -1;
        this.font = null;
        this.fontSrcBox =
            document.querySelector('#font-src');
        this.sampleTextBox =
            document.querySelector('#sample-text');
        this.screenSizeBox =
            document.querySelector('#screen-size');
        this.originXBox = document.querySelector('#origin-x');
        this.originY1Box = document.querySelector('#origin-y');
        this.originYAutoOffsetBox =
            document.querySelector('#origin-y-auto-offset');
        this.xAdvanceAdjustBox =
            document.querySelector('#x-advance-adjust');
        this.yAdvanceAdjustBox =
            document.querySelector('#y-advance-adjust');
        this.zoomBox = document.querySelector('#zoom');
        this.dotEmphasisBox =
            document.querySelector('#dot-emphasis');
        this.fgColorBox = document.querySelector('#fg-color');
        this.bgColorBox = document.querySelector('#bg-color');
        this.logBox = document.querySelector('#log');
        this.fontSrcBox.addEventListener('input', function () {
            _this.requestParse();
        });
        this.sampleTextBox.addEventListener('input', function () {
            _this.requestUpdatePreview();
        });
        var renderOptions = document.querySelector('#render-options');
        try {
            for (var _c = __values(renderOptions.querySelectorAll('input, select')), _d = _c.next(); !_d.done; _d = _c.next()) {
                var box = _d.value;
                box.addEventListener('change', function () { return _this.requestUpdatePreview(); });
                box.addEventListener('input', function () { return _this.requestUpdatePreview(); });
            }
        }
        catch (e_4_1) { e_4 = { error: e_4_1 }; }
        finally {
            try {
                if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
            }
            finally { if (e_4) throw e_4.error; }
        }
        var previewOptions = document.querySelector('#preview-options');
        try {
            for (var _e = __values(previewOptions.querySelectorAll('input, select')), _f = _e.next(); !_f.done; _f = _e.next()) {
                var box = _f.value;
                box.addEventListener('change', function () { return _this.requestUpdatePreview(); });
                box.addEventListener('input', function () { return _this.requestUpdatePreview(); });
            }
        }
        catch (e_5_1) { e_5 = { error: e_5_1 }; }
        finally {
            try {
                if (_f && !_f.done && (_b = _e.return)) _b.call(_e);
            }
            finally { if (e_5) throw e_5.error; }
        }
        document.querySelector('#color-swap').addEventListener('click', function () {
            var fg = _this.fgColorBox.value;
            var bg = _this.bgColorBox.value;
            _this.fgColorBox.value = bg;
            _this.bgColorBox.value = fg;
            _this.requestUpdatePreview();
        });
        document.querySelector('#color-rotate').addEventListener('click', function () {
            var e_6, _a;
            try {
                for (var _b = __values([_this.fgColorBox, _this.bgColorBox]), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var box = _c.value;
                    var rgb = parseColor(box.value);
                    var tmp = rgb[2];
                    rgb[2] = rgb[1];
                    rgb[1] = rgb[0];
                    rgb[0] = tmp;
                    box.value = encodeColor(rgb);
                }
            }
            catch (e_6_1) { e_6 = { error: e_6_1 }; }
            finally {
                try {
                    if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                }
                finally { if (e_6) throw e_6.error; }
            }
            _this.requestUpdatePreview();
        });
    }
    App.prototype.init = function () {
        return __awaiter(this, void 0, void 0, function () {
            var hash, srcUrl, sampleText, allowedUrls, params, params_1, params_1_1, param, _a, key, value, url, accepted, _b, _c, _d, key_1, prefix, fontSrc, fontText, error_1;
            var e_7, _e, e_8, _f;
            return __generator(this, function (_g) {
                switch (_g.label) {
                    case 0:
                        _g.trys.push([0, 4, , 5]);
                        hash = window.location.hash;
                        srcUrl = 'https://raw.githubusercontent.com/shapoco/shapofont/refs/heads/main/gfxfont/cpp/include/ShapoSansP_s12c09a01w02.h';
                        sampleText = ' !"#$%&\'()*+,-./\n0123456789:;<=>?\n@ABCDEFGHIJKLMNO\nPQRSTUVWXYZ[\\]^_\n`abcdefghijklmno\npqrstuvwxyz{|}~';
                        allowedUrls = {
                            '/shapofont/': 'https://raw.githubusercontent.com/shapoco/shapofont/refs/heads/main/gfxfont/cpp/include/',
                            '/ghuc/': 'https://raw.githubusercontent.com/',
                            '/gist/': 'https://gist.githubusercontent.com/',
                        };
                        if (hash.startsWith('#')) {
                            hash = hash.slice(1);
                            params = hash.split('&');
                            try {
                                for (params_1 = __values(params), params_1_1 = params_1.next(); !params_1_1.done; params_1_1 = params_1.next()) {
                                    param = params_1_1.value;
                                    _a = __read(param.split('='), 2), key = _a[0], value = _a[1];
                                    switch (key) {
                                        case 'u':
                                            {
                                                url = decodeURIComponent(value);
                                                accepted = false;
                                                try {
                                                    for (_b = (e_8 = void 0, __values(Object.entries(allowedUrls))), _c = _b.next(); !_c.done; _c = _b.next()) {
                                                        _d = __read(_c.value, 2), key_1 = _d[0], prefix = _d[1];
                                                        if (url.startsWith(prefix)) {
                                                            srcUrl = url;
                                                            accepted = true;
                                                        }
                                                        else if (url.startsWith(key_1)) {
                                                            srcUrl = prefix + url.slice(key_1.length);
                                                            accepted = true;
                                                            break;
                                                        }
                                                    }
                                                }
                                                catch (e_8_1) { e_8 = { error: e_8_1 }; }
                                                finally {
                                                    try {
                                                        if (_c && !_c.done && (_f = _b.return)) _f.call(_b);
                                                    }
                                                    finally { if (e_8) throw e_8.error; }
                                                }
                                                if (!accepted) {
                                                    throw new Error('Disallowed URL.');
                                                }
                                            }
                                            break;
                                        case 't':
                                            sampleText = decodeURIComponent(value);
                                            break;
                                        case 's':
                                            this.screenSizeBox.value = decodeURIComponent(value);
                                            break;
                                    }
                                }
                            }
                            catch (e_7_1) { e_7 = { error: e_7_1 }; }
                            finally {
                                try {
                                    if (params_1_1 && !params_1_1.done && (_e = params_1.return)) _e.call(params_1);
                                }
                                finally { if (e_7) throw e_7.error; }
                            }
                        }
                        this.sampleTextBox.value = sampleText;
                        if (!srcUrl) return [3 /*break*/, 3];
                        return [4 /*yield*/, fetch(srcUrl)];
                    case 1:
                        fontSrc = _g.sent();
                        return [4 /*yield*/, fontSrc.text()];
                    case 2:
                        fontText = _g.sent();
                        document.querySelector('#font-src').value =
                            fontText;
                        this.runParse();
                        _g.label = 3;
                    case 3: return [3 /*break*/, 5];
                    case 4:
                        error_1 = _g.sent();
                        this.logError(error_1.message);
                        return [3 /*break*/, 5];
                    case 5: return [2 /*return*/];
                }
            });
        });
    };
    App.prototype.requestParse = function () {
        var _this = this;
        this.parseRequestId = setTimeout(function () { return _this.runParse(); }, 300);
    };
    App.prototype.runParse = function () {
        if (this.parseRequestId >= 0) {
            clearTimeout(this.parseRequestId);
            this.parseRequestId = -1;
        }
        var fontSrc = this.fontSrcBox.value;
        try {
            var font = new Font(fontSrc);
            this.font = font;
            this.logInfo("firstCode: ".concat(codeToStr(font.firstCode), ", ") +
                "lastCode: ".concat(codeToStr(font.lastCode), ", ") +
                "yAdvance: ".concat(font.yAdvance));
        }
        catch (error) {
            this.font = null;
            this.logError(error.message);
        }
        this.requestUpdatePreview();
    };
    App.prototype.getTextSize = function () {
        return Number(document.querySelector('input[name="text-size"]:checked')
            .value);
    };
    App.prototype.requestUpdatePreview = function () {
        var _this = this;
        this.updatePreviewRequestId = setTimeout(function () { return _this.updatePreview(); }, 300);
    };
    App.prototype.updatePreview = function () {
        var e_9, _a, e_10, _b;
        if (this.updatePreviewRequestId >= 0) {
            clearTimeout(this.updatePreviewRequestId);
            this.updatePreviewRequestId = -1;
        }
        var canvas = document.querySelector('#preview-canvas');
        var font = this.font;
        if (!font) {
            var ctx_1 = canvas.getContext('2d');
            ctx_1.fillStyle = '#f00';
            ctx_1.fillText('No font loaded', 10, 20);
            return;
        }
        var text = this.sampleTextBox.value;
        var originX = Number(this.originXBox.value);
        var textSize = this.getTextSize();
        var originY = Number(this.originY1Box.value);
        var offsettedOriginY = originY;
        if (this.originYAutoOffsetBox.checked) {
            offsettedOriginY += this.font.getPreferredOriginY() * textSize;
        }
        var xAdvanceAdjust = Number(this.xAdvanceAdjustBox.value);
        var yAdvanceAdjust = Number(this.yAdvanceAdjustBox.value);
        var zoom = Number(this.zoomBox.value);
        var bgColorStr = this.bgColorBox.value;
        var fgColorStr = this.fgColorBox.value;
        var chars = this.layoutChars(font, text, originX, offsettedOriginY, textSize, xAdvanceAdjust, yAdvanceAdjust);
        var textRight = originX;
        var textBottom = originY;
        try {
            for (var chars_1 = __values(chars), chars_1_1 = chars_1.next(); !chars_1_1.done; chars_1_1 = chars_1.next()) {
                var c = chars_1_1.value;
                textRight = Math.max(textRight, c.getRight());
                textBottom = Math.max(textBottom, c.getBottom());
            }
        }
        catch (e_9_1) { e_9 = { error: e_9_1 }; }
        finally {
            try {
                if (chars_1_1 && !chars_1_1.done && (_a = chars_1.return)) _a.call(chars_1);
            }
            finally { if (e_9) throw e_9.error; }
        }
        var textWidth = textRight - originX;
        var textHeight = textBottom - originY;
        var screenSizeStr = this.screenSizeBox.value;
        var _c = __read(screenSizeStr.split('x').map(Number), 2), screenWidth = _c[0], screenHeight = _c[1];
        if (screenWidth <= 0) {
            screenWidth = Math.max(128, Math.ceil(textRight * 1.1 / 20) * 20);
        }
        if (screenHeight <= 0) {
            screenHeight = Math.max(32, Math.ceil(textBottom * 1.1 / 20) * 20);
        }
        var dotEmphasisAllowed = screenWidth < 320 && screenHeight < 320;
        this.dotEmphasisBox.disabled = !dotEmphasisAllowed;
        var dotEmphasis = this.dotEmphasisBox.checked && dotEmphasisAllowed;
        var dotSize = zoom;
        if (dotSize <= 0) {
            dotSize = Math.ceil(2000 / Math.max(screenWidth, screenHeight));
            dotSize = Math.max(1, Math.min(8, dotSize));
        }
        canvas.width = screenWidth * dotSize;
        canvas.height = screenHeight * dotSize;
        if (zoom > 0) {
            canvas.style.imageRendering = 'pixelated';
            canvas.style.width = "".concat(screenWidth * zoom, "px");
        }
        else {
            canvas.style.imageRendering = 'auto';
            canvas.style.width = '100%';
        }
        var ctx = canvas.getContext('2d');
        ctx.fillStyle = bgColorStr;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        {
            var lw = Math.max(1, screenWidth * dotSize / 900);
            // ctx.fillStyle = '#666';
            // ctx.fillRect(originX * dotSize - lw / 2, 0, lw, canvas.height);
            // ctx.fillRect(0, originY * dotSize - lw / 2, canvas.width, lw);
            // ctx.fillRect(textRight * dotSize - lw / 2, 0, lw, canvas.height);
            // ctx.fillRect(0, textBottom * dotSize - lw / 2, canvas.width, lw);
            ctx.strokeStyle = '#666';
            ctx.lineWidth = lw;
            ctx.strokeRect(originX * dotSize, originY * dotSize, textWidth * dotSize, textHeight * dotSize);
            ctx.strokeStyle = '#f00';
            ctx.lineWidth = lw;
            ctx.strokeRect(originX * dotSize - lw * 4, offsettedOriginY * dotSize - lw * 4, lw * 8, lw * 8);
            ctx.font = "".concat(Math.ceil(lw * 16), "px sans-serif");
            ctx.fillStyle = '#666';
            ctx.textBaseline = 'top';
            ctx.fillText("".concat(textWidth, "x").concat(textHeight), originX * dotSize, textBottom * dotSize);
        }
        try {
            for (var chars_2 = __values(chars), chars_2_1 = chars_2.next(); !chars_2_1.done; chars_2_1 = chars_2.next()) {
                var c = chars_2_1.value;
                c.glyph.render(ctx, c.x * dotSize, c.y * dotSize, c.size, dotSize, dotEmphasis, fgColorStr);
            }
        }
        catch (e_10_1) { e_10 = { error: e_10_1 }; }
        finally {
            try {
                if (chars_2_1 && !chars_2_1.done && (_b = chars_2.return)) _b.call(chars_2);
            }
            finally { if (e_10) throw e_10.error; }
        }
    };
    App.prototype.layoutChars = function (font, text, x, y, size, xAdvanceAdjust, yAdvanceAdjust) {
        var e_11, _a;
        var cursorX = x;
        var cursorY = y;
        var characters = [];
        try {
            for (var text_1 = __values(text), text_1_1 = text_1.next(); !text_1_1.done; text_1_1 = text_1.next()) {
                var c = text_1_1.value;
                var code = c.codePointAt(0);
                if (code == 0x0a) {
                    cursorX = x;
                    cursorY += font.yAdvance * size + yAdvanceAdjust;
                }
                else if (font.glyphs.has(code)) {
                    var glyph = font.glyphs.get(code);
                    if (glyph) {
                        characters.push(new Character(font, glyph, cursorX, cursorY, size));
                        cursorX += glyph.xAdvance * size + xAdvanceAdjust;
                    }
                }
            }
        }
        catch (e_11_1) { e_11 = { error: e_11_1 }; }
        finally {
            try {
                if (text_1_1 && !text_1_1.done && (_a = text_1.return)) _a.call(text_1);
            }
            finally { if (e_11) throw e_11.error; }
        }
        return characters;
    };
    App.prototype.logError = function (msg) {
        console.error(msg);
        this.logBox.textContent = "Error: ".concat(msg);
        this.logBox.style.color = '#c00';
    };
    App.prototype.logInfo = function (msg) {
        this.logBox.textContent = msg;
        this.logBox.style.color = '#0cf';
    };
    return App;
}());
document.addEventListener('DOMContentLoaded', function () { return __awaiter(_this, void 0, void 0, function () {
    var app;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                app = new App();
                return [4 /*yield*/, app.init()];
            case 1:
                _a.sent();
                return [2 /*return*/];
        }
    });
}); });
