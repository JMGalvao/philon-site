import re
import os
from xml.etree import ElementTree as ET
from math import floor, ceil
from PIL import Image

root = os.path.abspath(os.path.dirname(__file__))
proj = os.path.abspath(os.path.join(root, '..'))
svg_path = os.path.join(proj, 'assets', 'logo', 'logo.svg')
fav_dir = os.path.join(proj, 'favicon')
src512 = os.path.join(fav_dir, 'web-app-manifest-512x512.png')
out512 = src512
out192 = os.path.join(fav_dir, 'web-app-manifest-192x192.png')
out96 = os.path.join(fav_dir, 'favicon-96x96.png')
out_apple = os.path.join(fav_dir, 'apple-touch-icon.png')
out_ico = os.path.join(proj, 'favicon.ico')

if not os.path.exists(svg_path):
    raise FileNotFoundError(svg_path)
if not os.path.exists(src512):
    raise FileNotFoundError(src512)

# Parse SVG and compute numeric bbox from path 'd' attributes
tree = ET.parse(svg_path)
root_el = tree.getroot()
ns = ''
if root_el.tag.startswith('{'):
    ns = root_el.tag.split('}')[0] + '}'

all_coords = []
for path in root_el.findall('.//' + ns + 'path'):
    d = path.get('d')
    if not d:
        continue
    nums = re.findall(r'[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?', d)
    fnums = [float(n) for n in nums]
    for i in range(0, len(fnums)-1, 2):
        x = fnums[i]
        y = fnums[i+1]
        all_coords.append((x, y))

if not all_coords:
    raise SystemExit('No path coordinates found to compute bbox')

xs = [p[0] for p in all_coords]
ys = [p[1] for p in all_coords]
minx = min(xs)
miny = min(ys)
maxx = max(xs)
maxy = max(ys)

# Add padding (5% of max dim)
pad = max((maxx-minx), (maxy-miny)) * 0.05
minx_pad = floor(minx - pad)
miny_pad = floor(miny - pad)
width_pad = ceil((maxx - minx) + pad)
height_pad = ceil((maxy - miny) + pad)

new_viewbox = f"{minx_pad} {miny_pad} {width_pad} {height_pad}"
root_el.set('viewBox', new_viewbox)
root_el.set('width', '500')
root_el.set('height', '500')
tree.write(svg_path, encoding='utf-8', xml_declaration=True)
print('Updated viewBox to', new_viewbox)

# Map SVG viewBox (original assumed 0 0 500 500) to pixel crop on existing 512 PNG
orig_vb_w = 500.0
orig_vb_h = 500.0

img = Image.open(src512).convert('RGBA')
pw, ph = img.size

left = int((minx_pad / orig_vb_w) * pw)
top = int((miny_pad / orig_vb_h) * ph)
right = int(((minx_pad + width_pad) / orig_vb_w) * pw)
bottom = int(((miny_pad + height_pad) / orig_vb_h) * ph)

# Clamp
left = max(0, left)
top = max(0, top)
right = min(pw, right)
bottom = min(ph, bottom)

if right <= left or bottom <= top:
    raise SystemExit('Computed invalid crop box')

crop = img.crop((left, top, right, bottom))

# Make square by padding
cw, ch = crop.size
size = max(cw, ch)
sq = Image.new('RGBA', (size, size), (0,0,0,0))
sq.paste(crop, ((size - cw)//2, (size - ch)//2), crop)

# Export sizes
sq.resize((512,512), Image.LANCZOS).save(out512, format='PNG')
print('Wrote', out512)
sq.resize((192,192), Image.LANCZOS).save(out192, format='PNG')
print('Wrote', out192)
sq.resize((96,96), Image.LANCZOS).save(out96, format='PNG')
print('Wrote', out96)
sq.resize((180,180), Image.LANCZOS).save(out_apple, format='PNG')
print('Wrote', out_apple)

# Regenerate ICO
ico_sizes = [16,32,48,64,128,256]
img_for_ico = sq.resize((256,256), Image.LANCZOS)
img_for_ico.save(out_ico, format='ICO', sizes=[(s,s) for s in ico_sizes])
print('Created', out_ico)
