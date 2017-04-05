from PIL import Image

def show(path, positions, colors, width, height, save=False):
    im = Image.new('RGB', (width, height))
    pixels = im.load()
    for i in range(len(positions)):
        pos = positions[i]
        pixels[pos[0], pos[1]] = colors[i]

    im.show()

    if save:
        im.save(path, "PNG")
