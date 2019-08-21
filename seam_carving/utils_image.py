import struct
from PIL import Image


class ImageMatrix:
    def __init__(self, image):
        im = Image.open(image)
        self.width, self.height = im.size
        self.pixels = im.load()
        self.matrix = [[self.pixels[x, y] for x in range(im.width)] for y in range(im.height)]

    def ppm(self):
        return b'P6 %d %d 255\n' % (self.width, self.height) + \
               b''.join([struct.pack('BBB', *self.matrix[i][j])
                         for i in range(self.height) for j in range(self.width)])

    def save_ppm(self, filename):
        with open(filename, 'wb') as f:
            f.write(self.ppm())
        return filename

    def energy(self, i, j):
        if i == 0 or j == 0 or i == self.height - 1 or j == self.width - 1:
            return 1000
        else:  # Sobel operator
            return (self.distance(self.matrix[i-1][j], self.matrix[i+1][j]) +
                    self.distance(self.matrix[i][j-1], self.matrix[i][j+1]) +
                    self.distance(self.matrix[i-1][j-1], self.matrix[i+1][j+1]) +
                    self.distance(self.matrix[i+1][j-1], self.matrix[i-1][j+1]))

    @staticmethod
    def distance(pixel_a, pixel_b):
        return sum(abs(x - y) for x, y in zip(pixel_a, pixel_b))


# i1 = ImageMatrix('sunset_full.png')
# i2 = Image.open(i1.save_ppm('sunset.ppm'))
# print(i2.load()[24, 67])
# i2.show()
# print(i1.load()[35, 46])
# print(i1.pixels[24, 67])
# print(i1.matrix)
