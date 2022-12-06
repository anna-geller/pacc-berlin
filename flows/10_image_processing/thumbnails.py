"""
This will process 1,000 images concurrently and will generate thumnails for them.
It took me on my local machine running with local Orion instance 66 seconds, same for mapped/for loop

Best to run it on local Orion to avoid issues with Cloud rate limits.

unzip cats.zip
ls cats | wc -l
python flows/10_image_processing/thumbnails.py
ls cats/thumbnails | wc -l
"""
from pathlib import Path, PosixPath
from PIL import Image
from prefect import task, flow, unmapped
from typing import Tuple


@task
def get_images(img_dir: PosixPath, extension: str = "png"):
    return [i for i in img_dir.glob(f"*.{extension}")]


@task
def process_image(
    infile: PosixPath,
    out_dir: PosixPath,
    size: Tuple[int, int] = (128, 128),
    extension: str = "png",
):
    with Image.open(infile) as im:
        im.thumbnail(size)
    im.save(Path(out_dir, infile.stem + f"-thumbnail.{extension}"))


@flow
def generate_thumbnails(
    in_dir: str = "small", extension: str = "png", size: Tuple[int, int] = (128, 128)
):
    img_dir = Path(".", in_dir)
    out_dir = Path(".", in_dir, "thumbnails_mapped")
    images = get_images.submit(img_dir, extension)
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    process_image.map(
        images.result(), unmapped(out_dir), unmapped(size), unmapped(extension)
    )


if __name__ == "__main__":
    generate_thumbnails(in_dir="cats", extension="jpg")
    # generate_thumbnails(in_dir="small", extension="png")
