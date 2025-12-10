from PIL import Image
import os

root = os.path.abspath(os.path.dirname(__file__))
proj = os.path.abspath(os.path.join(root, '..'))
fav_dir = os.path.join(proj, 'favicon')
src96 = os.path.join(fav_dir, 'favicon-96x96.png')
out96 = src96
out512 = os.path.join(fav_dir, 'web-app-manifest-512x512.png')
out_ico = os.path.join(proj, 'favicon.ico')

if not os.path.exists(src96):
    raise FileNotFoundError(f'Input 96 PNG not found: {src96}')

img = Image.open(src96).convert('RGBA')

# Crop to non-transparent bbox
bbox = img.getbbox()
if not bbox:
    print('No non-transparent content found; exiting')
    raise SystemExit(1)

crop = img.crop(bbox)

# Make square by padding crop
cw, ch = crop.size
size = max(cw, ch)
crop_square = Image.new('RGBA', (size, size), (0,0,0,0))
offset = ((size - cw)//2, (size - ch)//2)
crop_square.paste(crop, offset)

# Target inner size to fill most of canvas (leave 4px padding)
inner_96 = 88
resized_96 = crop_square.resize((inner_96, inner_96), Image.LANCZOS)
canvas96 = Image.new('RGBA', (96,96), (0,0,0,0))
canvas96.paste(resized_96, ((96-inner_96)//2, (96-inner_96)//2), resized_96)
canvas96.save(out96, format='PNG')
print('Wrote', out96)

# Upscale to 512 for ICO/source
resized_512 = crop_square.resize((512,512), Image.LANCZOS)
resized_512.save(out512, format='PNG')
print('Wrote', out512)

# regenerate multi-res ICO
ico_sizes = [16,32,48,64,128,256]
ico_img = resized_512
ico_img.save(out_ico, format='ICO', sizes=[(s,s) for s in ico_sizes])
print('Created', out_ico)
