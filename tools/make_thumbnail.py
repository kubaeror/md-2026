"""Generates thumbnail.png for the launcher (512x512, no external deps).

Usage: python tools/make_thumbnail.py
"""

import os
import struct
import zlib

W = H = 512
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "thumbnail.png")

DIGITS = {
    "0": [
        "01110",
        "10001",
        "10011",
        "10101",
        "11001",
        "10001",
        "01110",
    ],
    "2": [
        "01110",
        "10001",
        "00001",
        "00010",
        "00100",
        "01000",
        "11111",
    ],
    "6": [
        "00110",
        "01000",
        "10000",
        "11110",
        "10001",
        "10001",
        "01110",
    ],
}


def make_pixels():
    px = bytearray()
    for y in range(H):
        # dark blue -> deep navy vertical gradient
        t = y / (H - 1)
        base = (
            int(12 + 18 * t),
            int(22 + 26 * t),
            int(44 + 40 * t),
        )
        for x in range(W):
            r, g, b = base
            # subtle diagonal stripes
            if (x + y) % 64 < 2:
                r, g, b = r + 8, g + 10, b + 14
            px += bytes((r, g, b))
    return px


def blit_digits(px, text, scale, ox, oy, color):
    for ch in text:
        glyph = DIGITS[ch]
        for gy, row in enumerate(glyph):
            for gx, bit in enumerate(row):
                if bit == "1":
                    for sy in range(scale):
                        for sx in range(scale):
                            X = ox + gx * scale + sx
                            Y = oy + gy * scale + sy
                            if 0 <= X < W and 0 <= Y < H:
                                i = (Y * W + X) * 3
                                px[i], px[i + 1], px[i + 2] = color
        ox += (len(glyph[0]) + 1) * scale
    return ox


def main():
    px = make_pixels()
    scale = 34
    width = (5 + 1) * scale * 4 - scale
    ox = (W - width) // 2
    oy = (H - 7 * scale) // 2
    blit_digits(px, "2026", scale, ox, oy, (245, 190, 60))
    blit_digits(px, "2026", scale, ox + 3, oy + 3, (18, 30, 56))

    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += px[y * W * 3:(y + 1) * W * 3]

    def chunk(tag, data):
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")

    with open(OUT, "wb") as f:
        f.write(png)
    print(f"Wrote {OUT} ({len(png)} bytes)")


if __name__ == "__main__":
    main()
