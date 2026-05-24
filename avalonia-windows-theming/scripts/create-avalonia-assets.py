"""Generate icon.ico and splash.png for Avalonia projects.
Pure Python stdlib — no PIL or external deps needed.
"""
import struct, zlib, sys

def create_png(width, height, pixels, filepath):
    """Create a PNG from a 2D array of (r,g,b) tuples."""
    signature = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff
    ihdr = struct.pack('>I', 13) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)
    raw_data = b''
    for y in range(height):
        raw_data += b'\x00'  # filter: None
        for x in range(width):
            r, g, b = pixels[y][x]
            raw_data += bytes([r, g, b])
    compressed = zlib.compress(raw_data)
    idat_crc = zlib.crc32(b'IDAT' + compressed) & 0xffffffff
    idat = struct.pack('>I', len(compressed)) + b'IDAT' + compressed + struct.pack('>I', idat_crc)
    iend_crc = zlib.crc32(b'IEND') & 0xffffffff
    iend = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc)
    with open(filepath, 'wb') as f:
        f.write(signature + ihdr + idat + iend)

def create_ico(width, height, pixels, filepath):
    """Create a .ico file with raw BGRA pixel data."""
    header = struct.pack('<HHH', 0, 1, 1)
    dib_header_size = 40
    dib_header = struct.pack('<IiiHHIIiiII',
        dib_header_size, width, height * 2, 1, 32, 0, 0, 0, 0, 0, 0)
    pixel_data = b''
    for y in range(height - 1, -1, -1):  # bottom-up
        for x in range(width):
            r, g, b = pixels[y][x]
            pixel_data += bytes([b, g, r, 255])  # BGRA
    image_size = len(pixel_data)
    entry = struct.pack('<BBBBHHII', width, height, 0, 0, 1, 32, image_size, 22)
    with open(filepath, 'wb') as f:
        f.write(header)
        f.write(entry)
        f.write(dib_header)
        f.write(pixel_data)

def make_splash_pixels(w=400, h=200):
    """Blue gradient background with calendar icon."""
    pixels = [[(0,0,0)] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            t = y / h
            r = int(20 + t * 30)
            g = int(40 + t * 50)
            b = int(80 + t * 80)
            pixels[y][x] = (r, g, b)
    cx, cy = w // 2 - 60, h // 2 - 40
    for dx in range(120):
        for dy in range(80):
            if 0 <= cy+dy < h and 0 <= cx+dx < w:
                pixels[cy+dy][cx+dx] = (240, 240, 255)
    for dx in range(120):
        for dy in range(15):
            if 0 <= cy+dy < h and 0 <= cx+dx < w:
                pixels[cy+dy][cx+dx] = (60, 100, 180)
    for row in range(1, 7):
        dy = row * (80 // 6)
        for dx in range(120):
            if 0 <= cy+dy < h and 0 <= cx+dx < w:
                pixels[cy+dy][cx+dx] = (200, 200, 220)
    for col in range(1, 7):
        dx = col * (120 // 7)
        for dy in range(80):
            if 0 <= cy+dy < h and 0 <= cx+dx < w:
                pixels[cy+dy][cx+dx] = (200, 200, 220)
    return pixels

def make_icon_pixels(size=64):
    """Blue gradient calendar icon."""
    pixels = [[(0,0,0)] * size for _ in range(size)]
    for y in range(size):
        for x in range(size):
            t = y / size
            pixels[y][x] = (int(30 + t * 40), int(60 + t * 60), int(120 + t * 60))
    cx2, cy2 = 12, 10
    for dx in range(40):
        for dy in range(40):
            if 0 <= cy2+dy < size and 0 <= cx2+dx < size:
                pixels[cy2+dy][cx2+dx] = (240, 240, 255)
    for dx in range(40):
        for dy in range(8):
            if 0 <= cy2+dy < size and 0 <= cx2+dx < size:
                pixels[cy2+dy][cx2+dx] = (60, 100, 180)
    for row in range(1, 7):
        dy = row * (40 // 6)
        for dx in range(40):
            if 0 <= cy2+dy < size and 0 <= cx2+dx < size:
                pixels[cy2+dy][cx2+dx] = (200, 200, 220)
    for col in range(1, 7):
        dx = col * (40 // 7)
        for dy in range(40):
            if 0 <= cy2+dy < size and 0 <= cx2+dx < size:
                pixels[cy2+dy][cx2+dx] = (200, 200, 220)
    return pixels

if __name__ == '__main__':
    outdir = sys.argv[1] if len(sys.argv) > 1 else 'Assets'
    splash = make_splash_pixels()
    create_png(400, 200, splash, f'{outdir}/splash.png')
    print('splash.png created')
    icon = make_icon_pixels()
    create_ico(64, 64, icon, f'{outdir}/icon.ico')
    print('icon.ico created')
    print('Done')
