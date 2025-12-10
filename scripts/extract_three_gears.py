from PIL import Image
import os
from collections import deque

root = os.path.abspath(os.path.dirname(__file__))
proj = os.path.abspath(os.path.join(root, '..'))
src = os.path.join(proj, 'favicon', 'web-app-manifest-512x512.png')
out_dir = os.path.join(proj, 'favicon')
out_512 = os.path.join(out_dir, 'web-app-manifest-512x512.png')
out_192 = os.path.join(out_dir, 'web-app-manifest-192x192.png')
out_96 = os.path.join(out_dir, 'favicon-96x96.png')
out_apple = os.path.join(out_dir, 'apple-touch-icon.png')
out_ico = os.path.join(proj, 'favicon.ico')

if not os.path.exists(src):
    raise FileNotFoundError(src)

img = Image.open(src).convert('RGBA')
px = img.load()
W, H = img.size

# Build binary mask of non-transparent pixels
mask = [[0]*W for _ in range(H)]
for y in range(H):
    for x in range(W):
        if px[x,y][3] > 16:
            mask[y][x] = 1

visited = [[False]*W for _ in range(H)]
components = []

dirs = [(1,0),(-1,0),(0,1),(0,-1)]
for y in range(H):
    for x in range(W):
        if mask[y][x] and not visited[y][x]:
            q = deque()
            q.append((x,y))
            visited[y][x] = True
            minx, miny, maxx, maxy = x, y, x, y
            area = 0
            while q:
                cx, cy = q.popleft()
                area += 1
                if cx < minx: minx = cx
                if cy < miny: miny = cy
                if cx > maxx: maxx = cx
                if cy > maxy: maxy = cy
                for dx, dy in dirs:
                    nx, ny = cx+dx, cy+dy
                    if 0 <= nx < W and 0 <= ny < H and not visited[ny][nx] and mask[ny][nx]:
                        visited[ny][nx] = True
                        q.append((nx, ny))
            components.append({'bbox':(minx,miny,maxx+1,maxy+1),'area':area})

if not components:
    raise SystemExit('No components found')

# Sort components by area desc and pick top 3
components.sort(key=lambda c: c['area'], reverse=True)
selected = components[:3]

# Compute combined bbox to layout components with spacing
minx = min(c['bbox'][0] for c in selected)
miny = min(c['bbox'][1] for c in selected)
maxx = max(c['bbox'][2] for c in selected)
maxy = max(c['bbox'][3] for c in selected)

# Create a new canvas that fits the selected components with padding
pad = 24
canvas_w = (maxx - minx) + pad*2
canvas_h = (maxy - miny) + pad*2
canvas = Image.new('RGBA', (canvas_w, canvas_h), (0,0,0,0))

for c in selected:
    bx0, by0, bx1, by1 = c['bbox']
    crop = img.crop((bx0, by0, bx1, by1))
    # paste relative to minx/miny plus padding
    canvas.paste(crop, (bx0 - minx + pad, by0 - miny + pad), crop)

# Optionally scale down slightly to give more separation
scale = 0.88
new_w = int(round(canvas_w * scale))
new_h = int(round(canvas_h * scale))
canvas = canvas.resize((new_w, new_h), Image.LANCZOS)

# Center into 512 square
final_512 = Image.new('RGBA', (512,512), (0,0,0,0))
final_512.paste(canvas, ((512-new_w)//2, (512-new_h)//2), canvas)
final_512.save(out_512, format='PNG')
final_512.resize((192,192), Image.LANCZOS).save(out_192, format='PNG')
final_512.resize((96,96), Image.LANCZOS).save(out_96, format='PNG')
final_512.resize((180,180), Image.LANCZOS).save(out_apple, format='PNG')

# regenerate ICO
ico_img = final_512.resize((256,256), Image.LANCZOS)
ico_img.save(out_ico, format='ICO', sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])

print('Wrote extracted gears to', out_512)
