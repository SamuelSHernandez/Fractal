"""
- Author: Samuel Hernandez and Jaron Schultz
- Runtime: O(N^2)
- Description:
    Algorithm to generate the Mandelbrot set given
    coordinates x, y, and R.

    The mandelbrot set is a set of complex numbers
    where the values of the equation below do not
    diverge to infinity when iterated from z = 0.

        f(z) = z^2 + C

    Where z and C are complex numbers.

- for more info:
https://en.wikipedia.org/wiki/Mandelbrot_set
"""

from colorsys import hsv_to_rgb

from PIL import Image
from tqdm import tqdm


def get_complex_number(a, b):
    z = complex(a, b)
    return z


def get_c(x, y, x_max, y_max, scale, center_x, center_y):
    scaling_factor = 1.2 * scale

    upper_x = center_x + scaling_factor
    upper_y = -center_y + scaling_factor

    lower_x = center_x - scaling_factor
    lower_y = -center_y - scaling_factor

    width = upper_x - lower_x
    height = upper_y - lower_y

    c_x = (width * x / x_max) + lower_x
    c_y = (height * y / y_max) + lower_y

    return c_x, c_y


def escape(max_iter, cx, cy, set_degree):
    iter_count = 0
    z = complex(0, 0)
    c = complex(cx, cy)
    in_set = 0
    for i in range(0, max_iter):
        z = pow(z, set_degree)
        z += c
        iter_count += 1
        if abs(z) > 2:
            iter_count = i
            break
        elif i == max_iter - 1:  # if z never escapes, color it black
            in_set = 1

    return iter_count, in_set


def mandelbrot_render(
    iterate,
    x_s,
    y_s,
    scf,
    z_x,
    z_y,
    color_val,
    degree,
    number,
):
    """
    - rainbow:
        current implementation.
    - inverted colors:
        rgb = hsv_to_rgb(
        1/(((color_variation * (color[0] % 256)) / 255)+0.1), 1, 1 - color[1]
        )
    """
    progress = tqdm(total=100)  # progress status of code's completion
    mandelbrotValues = []
    for i in range(0, y_s):  # length
        for j in range(0, x_s):  # height
            c = get_c(j, i, x_s, y_s, scf, z_x, z_y)
            color = escape(iterate, c[0], c[1], degree)
            rgb = hsv_to_rgb(
                (color_val * (color[0] % 256)) / 255, 1, 1 - color[1]
            )
            rgb = [int(255 * u) for u in rgb]  # rescales values into rgb
            mandelbrotValues.extend(rgb)
            progress.update(10)
    mandelbrotValues = bytes(mandelbrotValues)
    img = Image.frombytes("RGB", (x_s, y_s), mandelbrotValues)  # creates image
    naming = str(number)
    img.save("./mandlebrot_img/m_" + naming + ".jpg")

    progress.close()


if __name__ == "__main__":
    """
    # Default presets
    x: -1.4790645 y: 0.0107495 R: 0.000015
    x: -0.744881555195, y:0.1001075148864 R: 0.00000000001
    """
    image_size = [1000, 1000]  # x, y
    iterations = 2000
    scaling_factor = (1.3,)
    zoom = [
        -0.744881555193959,
        0.100107514886258,
        0.00000000000005,
    ]  # zoom_x, zoom_y, max_zoom
    color_variation = 1
    degree = 2
    i = 1
    max_i = 1000

    while i <= max_i:
        scaling_factor = pow(1.03, (1 - i))
        mandelbrot_render(
            iterations,
            image_size[0],
            image_size[1],
            scaling_factor,
            zoom[0],
            zoom[1],
            color_variation,
            degree,
            i,
        )
        i += 1
