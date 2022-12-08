# Image Processing locally - `for` loop vs `mapping`

## Mapping

```python
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
```

## For loop

```python
"""
This will process 10,000 images concurrently and will generate thumnails for them.
It took me on my local machine running with local Orion instance

Best to run it on local Orion to avoid issues with Cloud rate limits.
ls train | wc -l
ls train/thumbnails | wc -l
"""
from pathlib import Path, PosixPath
from PIL import Image
from prefect import task, flow
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
    out_dir = Path(".", in_dir, "thumbnails")
    images = get_images.submit(img_dir, extension)
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    for img in images.result():
        img_ = str(img).replace(f"{in_dir}/", "")
        process_image.with_options(name=img_).submit(img, out_dir, size, extension)

if __name__ == "__main__":
    generate_thumbnails(in_dir="cats", extension="jpg")
```

## For loop with S3 images

```python
from dotenv import load_dotenv
import os
from prefect.filesystems import S3
from utilities.deploy_utils import DEFAULT_BLOCK, save_block

load_dotenv()

s3 = S3(
    bucket_path=os.environ.get("AWS_S3_BUCKET_NAME", DEFAULT_BLOCK),
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", DEFAULT_BLOCK),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", DEFAULT_BLOCK),
)
```

```python
"""
pip install s3fs
pip install prefect-aws
pip install aiobotocore==2.3.4
aws s3 ls s3://prefect-orion/demo/
unzip cats.zip
"""
from prefect.filesystems import S3

s3 = S3.load("default")
s3.put_directory("cats", "cats")

# in a flow:
# s3.get_directory(from_path="cats", local_path="cats_local")
```

slow upload process file by file - easier to upload zip file with 1k images and unzip before processing & before putting to mapping

```python
"""
This will process 10,000 images concurrently and will generate thumnails for them.
It took me on my local machine running with local Orion instance

Best to run it on local Orion to avoid issues with Cloud rate limits.

unzip cats.zip
ls cats | wc -l
python flows/10_image_processing/thumbnails_for_loop_s3_images.py
ls cats/thumbnails | wc -l
"""
from pathlib import Path, PosixPath
from PIL import Image
from prefect import task, flow
from typing import Tuple
from prefect.filesystems import S3

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
    out_dir = Path(".", in_dir, "thumbnails")
    s3 = S3.load("default")
    s3.get_directory(from_path=in_dir, local_path=in_dir)
    images = get_images.submit(img_dir, extension)
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    for img in images.result():
        img_ = str(img).replace(f"{in_dir}/", "")
        process_image.with_options(name=img_).submit(img, out_dir, size, extension)

if __name__ == "__main__":
    generate_thumbnails(in_dir="cats", extension="jpg")
```