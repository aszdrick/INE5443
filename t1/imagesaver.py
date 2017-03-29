from PIL import Image

def save(path, positions, colors, width, height, show=False):
    im = Image.new('RGB', (width, height))
    pixels = im.load()
    for i in range(len(positions)):
        pos = positions[i]
        pixels[pos[0], pos[1]] = colors[i]
    im.save(path, "PNG")

    if show:
        im.show()
