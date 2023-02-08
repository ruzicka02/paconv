from pathlib import Path
from time import time

from . import file_management
from . import logic


def convert(file_name: str, dims: tuple, palette_size: int = 6) -> float:
    """
    Converts an image to a pixel-art style.

    :param file_name: Name of file(s) or their relative path.
    :param dims: Target size of the resulting image.
    :param palette_size: Amount of colors in case the palette has to be generated.
    :return: Time duration of conversion (seconds).
    :raise FileNotFoundError: Image not found on given path.
    :raise ValueError: File with this name was found but was invalid.
    """
    start_time = time()

    print(f"Searched path is: {(Path().absolute() / Path(file_name)).parent.resolve()}")

    try:
        img = file_management.load_image(file_name, dims)
    except (ValueError, FileNotFoundError) as err:
        print(err)
        print("For more info, type:\n    python -m paconv --help")
        raise

    try:
        colors = file_management.load_colors(file_name)
    except FileNotFoundError:
        colors = file_management.generate_colors(file_name, color_count=palette_size)
    except ValueError as err:
        print(err)
        print("For more info, type:\n    python -m paconv --help\nFallback to generated color palette...")
        colors = file_management.generate_colors(file_name, color_count=palette_size)
        # raise

    res = logic.convert_img(img, colors)
    path = file_management.save_image(res, False)

    duration = time() - start_time

    print(f"Conversion was successful.\nImage saved to {path}")
    print(f"Duration: {duration:.2f} s")

    return duration
