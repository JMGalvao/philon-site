from PIL import Image
import os

root = os.path.abspath(os.path.dirname(__file__))
proj = os.path.abspath(os.path.join(root, '..'))
src = os.path.join(proj, 'favicon', 'web-app-manifest-512x512.png')
out_ico = os.path.join(proj, 'favicon.ico')
out_dir = os.path.join(proj, 'favicon')

if not os.path.exists(src):
    raise FileNotFoundError(f'Input PNG not found: {src}')

img = Image.open(src).convert('RGBA')

# Trim transparent borders
bbox = img.getbbox()
if bbox:
    trimmed = img.crop(bbox)
else:
    trimmed = img

# Make square by padding with transparent pixels
w, h = trimmed.size
size = max(w, h)
new = Image.new('RGBA', (size, size), (0, 0, 0, 0))
offset = ((size - w) // 2, (size - h) // 2)
new.paste(trimmed, offset)

# Sizes to export
png_sizes = {
    'web-app-manifest-512x512.png': 512,
    'web-app-manifest-192x192.png': 192,
    'favicon-96x96.png': 96,
    'apple-touch-icon.png': 180
}

for name, s in png_sizes.items():
    out_path = os.path.join(out_dir, name)
    resized = new.resize((s, s), Image.LANCZOS)
    resized.save(out_path, format='PNG')
    print('Wrote', out_path)

# Create multi-resolution ICO at project root
ico_sizes = [16, 32, 48, 64, 128, 256]
ico_img = new.resize((256, 256), Image.LANCZOS)
ico_img.save(out_ico, format='ICO', sizes=[(s, s) for s in ico_sizes])
print('Created', out_ico)
