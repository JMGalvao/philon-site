import re
import os
from xml.etree import ElementTree as ET
from math import floor, ceil
import cairosvg
from PIL import Image

root = os.path.abspath(os.path.dirname(__file__))
proj = os.path.abspath(os.path.join(root, '..'))
svg_path = os.path.join(proj, 'assets', 'logo', 'logo.svg')
fav_dir = os.path.join(proj, 'favicon')
out512 = os.path.join(fav_dir, 'web-app-manifest-512x512.png')
out192 = os.path.join(fav_dir, 'web-app-manifest-192x192.png')
out96 = os.path.join(fav_dir, 'favicon-96x96.png')
out_ico = os.path.join(proj, 'favicon.ico')

if not os.path.exists(svg_path):
    raise FileNotFoundError(svg_path)

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
    # group into (x,y) pairs
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

# Add padding (5% of max dim) for safety
pad = max((maxx-minx), (maxy-miny)) * 0.05
minx = floor(minx - pad)
miny = floor(miny - pad)
width = ceil((maxx - minx) + pad)
height = ceil((maxy - miny) + pad)

new_viewbox = f"{minx} {miny} {width} {height}"
root_el.set('viewBox', new_viewbox)
root_el.set('width', '500')
root_el.set('height', '500')
tree.write(svg_path, encoding='utf-8', xml_declaration=True)
print('Updated viewBox to', new_viewbox)

# Render PNGs from tightened SVG using cairosvg
print('Rendering 512 PNG...')
cairosvg.svg2png(url=svg_path, write_to=out512, output_width=512, output_height=512)
print('Rendering 192 PNG...')
cairosvg.svg2png(url=svg_path, write_to=out192, output_width=192, output_height=192)
print('Rendering 96 PNG...')
cairosvg.svg2png(url=svg_path, write_to=out96, output_width=96, output_height=96)

# Regenerate multi-size ICO
img = Image.open(out512).convert('RGBA')
ico_sizes = [16,32,48,64,128,256]
img.save(out_ico, format='ICO', sizes=[(s,s) for s in ico_sizes])
print('Created', out_ico)
