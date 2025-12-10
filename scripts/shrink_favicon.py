from PIL import Image
import os

root = os.path.abspath(os.path.dirname(__file__))
proj = os.path.abspath(os.path.join(root, '..'))
fav_dir = os.path.join(proj, 'favicon')
in96 = os.path.join(fav_dir, 'favicon-96x96.png')
out96 = in96
out192 = os.path.join(fav_dir, 'web-app-manifest-192x192.png')
out512 = os.path.join(fav_dir, 'web-app-manifest-512x512.png')
out_apple = os.path.join(fav_dir, 'apple-touch-icon.png')
out_ico = os.path.join(proj, 'favicon.ico')

if not os.path.exists(in96):
    raise FileNotFoundError(in96)

# Desired inner glyph size inside 96 canvas (smaller -> glyph appears smaller)
inner_96 = 60

img96 = Image.open(in96).convert('RGBA')

# Extract glyph bbox
bbox = img96.getbbox()
if not bbox:
    raise SystemExit('No non-transparent content found in 96 PNG')

glyph = img96.crop(bbox)
gw, gh = glyph.size

# Make square glyph canvas
size = max(gw, gh)
glyph_sq = Image.new('RGBA', (size, size), (0,0,0,0))
glyph_sq.paste(glyph, ((size-gw)//2, (size-gh)//2), glyph)

# Create 96 canvas with smaller glyph centered
canvas96 = Image.new('RGBA', (96,96), (0,0,0,0))
glyph_small = glyph_sq.resize((inner_96, inner_96), Image.LANCZOS)
canvas96.paste(glyph_small, ((96-inner_96)//2, (96-inner_96)//2), glyph_small)
canvas96.save(out96, format='PNG')
print('Wrote', out96)

# Create 512 canvas matching the same visual proportion
scale = 512 / 96
inner_512 = int(round(inner_96 * scale))
canvas512 = Image.new('RGBA', (512,512), (0,0,0,0))
glyph_512 = glyph_sq.resize((inner_512, inner_512), Image.LANCZOS)
canvas512.paste(glyph_512, ((512-inner_512)//2, (512-inner_512)//2), glyph_512)
canvas512.save(out512, format='PNG')
print('Wrote', out512)

# Create 192 and apple-touch by resizing the 512 canvas
canvas192 = canvas512.resize((192,192), Image.LANCZOS)
canvas192.save(out192, format='PNG')
print('Wrote', out192)

canvas_apple = canvas512.resize((180,180), Image.LANCZOS)
canvas_apple.save(out_apple, format='PNG')
print('Wrote', out_apple)

# Regenerate ICO with multiple sizes
ico_sizes = [16,32,48,64,128,256]
img_for_ico = canvas512.resize((256,256), Image.LANCZOS)
img_for_ico.save(out_ico, format='ICO', sizes=[(s,s) for s in ico_sizes])
print('Created', out_ico)
