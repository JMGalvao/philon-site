from PIL import Image
import os

root = os.path.abspath(os.path.dirname(__file__))
# project root
proj = os.path.abspath(os.path.join(root, '..'))
src = os.path.join(proj, 'favicon', 'web-app-manifest-512x512.png')
out = os.path.join(proj, 'favicon.ico')

if not os.path.exists(src):
    raise FileNotFoundError(f'Input PNG not found: {src}')

sizes = [16, 32, 48, 64, 128, 256]
img = Image.open(src).convert('RGBA')
# save ICO with multiple sizes
img.save(out, format='ICO', sizes=[(s, s) for s in sizes])
print('Created', out)
