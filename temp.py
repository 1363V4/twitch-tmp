from PIL import Image
from pathlib import Path


cwd = Path.cwd()
im = Image.open(cwd / "static/img" / "stario.png")
print(im.size)

smol = im.resize((32, 32))
print(smol.size)
smol.save(cwd / "smol.png")
