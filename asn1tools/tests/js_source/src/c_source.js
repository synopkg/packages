/**
 * The MIT License (MIT)
 *
 * Copyright (c) 2019 Erik Moqvist
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use, copy,
 * modify, merge, publish, distribute, sublicense, and/or sell copies
 * of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
 * BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
 * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

/**
 * This file was generated by asn1tools version 0.145.2 Thu Jan 24 07:56:02 2019.
 */

class Encoder {
    constructor() {
        this.buf = [];
    }

    append_bytes(buf) {
        this.buf = this.buf.concat(Array.from(buf));
    }

    append_uint8(value) {
        this.append_bytes(new Uint8Array([value]));
    }

    append_uint16(value) {
        this.append_bytes(new Uint8Array([
            (value >> 8) & 0xff,
            value & 0xff
        ]));
    }

    append_uint32(value) {
        this.append_bytes(new Uint8Array([
            (value >> 24) & 0xff,
            (value >> 16) & 0xff,
            (value >> 8) & 0xff,
            value & 0xff
        ]));
    }

    append_int8(value) {
        this.append_uint8(value);
    }

    append_int16(value) {
        this.append_uint16(value);
    }

    append_int32(value) {
        this.append_uint32(value);
    }

    append_uint(value, number_of_bytes) {
        switch (number_of_bytes) {

        case 1:
            this.append_uint8(value);
            break;

        case 2:
            this.append_uint16(value);
            break;

        case 3:
            this.append_uint8(value >> 16);
            this.append_uint16(value);
            break;

        default:
            this.append_uint32(value);
            break;
        }
    }

    append_bool(value) {
        if (value) {
            this.append_uint8(255);
        } else {
            this.append_uint8(0);
        }
    }

    append_length_determinant(length) {
        if (length < 128) {
            this.append_int8(length);
        } else if (length < 256) {
            this.append_uint8(0x81);
            this.append_uint8(length);
        } else if (length < 65536) {
            this.append_uint8(0x82);
            this.append_uint16(length);
        } else if (length < 16777216) {
            length |= (0x83 << 24);
            this.append_uint32(length);
        } else {
            this.append_uint8(0x84);
            this.append_uint32(length);
        }
    }

    toUint8Array() {
        return new Uint8Array(this.buf);
    }
}

class Decoder {
    constructor(data) {
        this.buf = data;
        this.pos = 0
    }

    read_bytes(size) {
        var end = this.pos + size;

        if (this.buf.length < end) {
            throw Error("Out of data.");
        }

        var data = this.buf.subarray(this.pos, end);
        this.pos += size;

        return data;
    }

    read_uint8() {
        return this.read_bytes(1)[0];
    }

    read_uint16() {
        return ((this.read_bytes(1)[0] * 256)
                + this.read_bytes(1)[0]);
    }

    read_uint32() {
        return ((this.read_bytes(1)[0] * 16777216)
                + (this.read_bytes(1)[0] * 65536)
                + (this.read_bytes(1)[0] * 256)
                + this.read_bytes(1)[0]);
    }

    read_int8() {
        var value = this.read_uint8();

        if (value & 0x80) {
            value -= 256;
        }

        return value;
    }

    read_int16() {
        var value = this.read_uint16();

        if (value & 0x8000) {
            value -= 65536;
        }

        return value;
    }

    read_int32() {
        var value = this.read_uint32();

        if (value & 0x80000000) {
            value -= 0x100000000;
        }

        return value;
    }

    read_uint(number_of_bytes) {
        switch (number_of_bytes) {

        case 1:
            return this.read_uint8();

        case 2:
            return this.read_uint16();

        case 3:
            return ((this.read_uint8() * 65536)
                    + this.read_uint16());

        case 4:
            return this.read_uint32();

        default:
            throw Error("Too big value.");
        }
    }

    read_bool() {
        return this.read_uint8() !== 0;
    }

    read_length_determinant() {
        var length = this.read_uint8();

        if (length & 0x80) {
            switch (length & 0x7f) {

            case 1:
                length = this.read_uint8();
                break;

            case 2:
                length = this.read_uint16();
                break;

            case 3:
                length = ((this.read_uint8() * 65536)
                          + this.read_uint16());
                break;

            case 4:
                length = this.read_uint32();
                break;

            default:
                throw Error("Too big value.");
            }
        }

        return length;
    }

    read_tag() {
        var tag = this.read_uint8();

        if ((tag & 0x3f) === 0x3f) {
            do {
                tag *= 256;
                tag += this.read_uint8();
            } while ((tag & 0x80) === 0x80);
        }

        return tag;
    }
}

class Type {
    toUint8Array() {
        var encoder = new Encoder();

        this.encode(encoder);

        return encoder.toUint8Array();
    }

    fromUint8Array(buf) {
        this.decode(new Decoder(buf));
    }
}

function minimum_uint_length(value) {
    var length;

    if (value < 256) {
        length = 1;
    } else if (value < 65536) {
        length = 2;
    } else if (value < 16777216) {
        length = 3;
    } else {
        length = 4;
    }

    return length;
}

class CSourceA extends Type {
    constructor() {
        super();
        this.a = null;
        this.b = null;
        this.c = null;
        this.e = null;
        this.f = null;
        this.g = null;
        this.i = null;
        this.j = null;
    }

    encode(encoder) {
        encoder.append_int8(this.a);
        encoder.append_int16(this.b);
        encoder.append_int32(this.c);
        encoder.append_uint8(this.e);
        encoder.append_uint16(this.f);
        encoder.append_uint32(this.g);
        encoder.append_bool(this.i);
        encoder.append_bytes(this.j);
    }

    decode(decoder) {
        this.a = decoder.read_int8();
        this.b = decoder.read_int16();
        this.c = decoder.read_int32();
        this.e = decoder.read_uint8();
        this.f = decoder.read_uint16();
        this.g = decoder.read_uint32();
        this.i = decoder.read_bool();
        this.j = decoder.read_bytes(11);
    }
}

class CSourceB extends Type {
    static CHOICE_A = 0;
    static CHOICE_B = 1;
    static CHOICE_C = 2;

    constructor() {
        super();
        this.choice = null;
        this.value = {
            a: null,
            b: new CSourceA(),
            c: null
        };
    }

    encode(encoder) {
        switch (this.choice) {

        case CSourceB.CHOICE_A:
            encoder.append_uint(0x80, 1);
            encoder.append_int8(this.value.a);
            break;

        case CSourceB.CHOICE_B:
            encoder.append_uint(0x81, 1);
            this.value.b.encode(encoder);
            break;

        case CSourceB.CHOICE_C:
            encoder.append_uint(0x82, 1);
            break;

        default:
            throw Error("Bad choice.");
        }
    }

    decode(decoder) {
        var tag = decoder.read_tag();

        switch (tag) {

        case 0x80:
            this.choice = CSourceB.CHOICE_A;
            this.value.a = decoder.read_int8();
            break;

        case 0x81:
            this.choice = CSourceB.CHOICE_B;
            this.value.b.decode(decoder);
            break;

        case 0x82:
            this.choice = CSourceB.CHOICE_C;
            break;

        default:
            throw Error("Bad choice.");
        }
    }
}

class CSourceC extends Type {
    constructor() {
        super();
        this.elements = [];
    }

    encode(encoder) {
        var i;
        var number_of_length_bytes = minimum_uint_length(this.elements.length);
        encoder.append_uint8(number_of_length_bytes);
        encoder.append_uint(this.elements.length, number_of_length_bytes);

        for (i = 0; i < this.elements.length; i++) {
            this.elements[i].encode(encoder);
        }
    }

    decode(decoder) {
        var i;
        var length = decoder.read_uint(decoder.read_uint8());

        if (length > 2) {
            throw Error("Bad length.");
        }

        this.elements = [];

        for (i = 0; i < length; i++) {
            var element = new CSourceB();
            element.decode(decoder)
            this.elements.push(element)
        }
    }
}

export {
    CSourceA,
    CSourceB,
    CSourceC,
    Encoder,
    Decoder
};
