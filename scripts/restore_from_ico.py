from PIL import Image
import os

root = os.path.abspath(os.path.dirname(__file__))
proj = os.path.abspath(os.path.join(root, '..'))
ico_path = os.path.join(proj, 'favicon.ico')
out_dir = os.path.join(proj, 'favicon')
out_512 = os.path.join(out_dir, 'web-app-manifest-512x512.png')
out_192 = os.path.join(out_dir, 'web-app-manifest-192x192.png')
out_96 = os.path.join(out_dir, 'favicon-96x96.png')
out_apple = os.path.join(out_dir, 'apple-touch-icon.png')

if not os.path.exists(ico_path):
    raise FileNotFoundError(ico_path)

# Open ICO and pick the largest embedded image
ico = Image.open(ico_path)
frames = []
try:
    i = 0
    while True:
        ico.seek(i)
        frames.append(ico.copy())
        i += 1
except Exception:
    pass

if not frames:
    raise SystemExit('No frames found in favicon.ico')

# Choose frame with largest area
best = max(frames, key=lambda im: im.size[0]*im.size[1])
bw, bh = best.size
print('Found ico frame size', bw, 'x', bh)

# Upscale to 512 if smaller
if bw < 512 or bh < 512:
    img512 = best.resize((512,512), Image.LANCZOS).convert('RGBA')
else:
    img512 = best.convert('RGBA')

img512.save(out_512, format='PNG')
print('Wrote', out_512)

img512.resize((192,192), Image.LANCZOS).save(out_192, format='PNG')
print('Wrote', out_192)

img512.resize((96,96), Image.LANCZOS).save(out_96, format='PNG')
print('Wrote', out_96)

img512.resize((180,180), Image.LANCZOS).save(out_apple, format='PNG')
print('Wrote', out_apple)

print('Restoration complete')
