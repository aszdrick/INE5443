from PIL import Image

def save(positions, colors, grid_size, path):
    im = Image.new('RGB', (grid_size, grid_size))
    pixels = im.load()
    for i in range(len(positions)):
        pos = positions[i]
        pixels[pos[0], pos[1]] = colors[i]
    im.save(path, "PNG")
