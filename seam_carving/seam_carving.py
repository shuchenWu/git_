from collections import namedtuple
from utils_image import ImageMatrix


SeamEnergyWithBackPointer = namedtuple('SeamEnergyWithBackPointer', 'energy prev_x_coordinate')
_seam_energies = []  # the whole image's energy matrix with back_pointer


def read_image(image):
    im = ImageMatrix(image)
    print('original pixels: ', im.width, im.height)
    return im


def compute_energy_matrix(im):
    return [[im.energy(i, j) for j in range(im.width)] for i in range(im.height)]


def get_lowest_energy_seam(energy_matrix):

    previous_row = [SeamEnergyWithBackPointer(x, None) for x in energy_matrix[0]]
    _seam_energies.append(previous_row)
    for y in range(1, len(energy_matrix)):
        cur_row = energy_matrix[y]
        accumulate_energy = []
        for x, pixel_energy in enumerate(cur_row):
            x_left = max(x - 1, 0)
            x_right = min(x + 1, len(cur_row) - 1)
            x_range = range(x_left, x_right + 1)
            min_energy_x = min(x_range, key=lambda x: previous_row[x].energy)
            min_energy = SeamEnergyWithBackPointer(
                pixel_energy + previous_row[min_energy_x].energy, min_energy_x)
            accumulate_energy.append(min_energy)
        previous_row = accumulate_energy
        _seam_energies.append(previous_row)

    return min(range(len(previous_row)-1),
               key=lambda x: previous_row[x].energy)


def backtrack_seam_with_lowest_energy(last_row_idx):
    result = []

    for i in range(len(_seam_energies) - 1, -1, -1):
        result.append(last_row_idx)
        last_row_idx = _seam_energies[i][last_row_idx].prev_x_coordinate

    return reversed(result)


def remove_one_seam(indices):
    for idx, row in zip(indices, im.matrix):
        row.pop(idx)
    im.width -= 1

    _seam_energies.clear()


if __name__ == '__main__':
    n = input('how many pixels in width would you like to remove? ')
    im = read_image('sunset_full.png')
    for _ in range(int(n)):
        matrix = compute_energy_matrix(im)
        index_with_total_lowest_energy_in_last_line = get_lowest_energy_seam(matrix)
        indices = backtrack_seam_with_lowest_energy(index_with_total_lowest_energy_in_last_line)
        remove_one_seam(indices)
    e = im.matrix
    print('resized pixels', len(e[0]), len(e))
    filename = im.save_ppm(f'resized_{n}_sunset.ppm')
    #  convert ppm to png
    from PIL import Image
    im = Image.open(filename)
    im.save(filename.rsplit('.', maxsplit=1)[0] + '.png')
