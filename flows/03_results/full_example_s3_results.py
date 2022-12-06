"""
pip install s3fs
"""
from prefect.filesystems import S3
import subprocess
import time


def get_s3_result_files(bucket_path: str = "s3://prefect-orion/demo/"):
    out = subprocess.run(f"aws s3 ls {bucket_path}", shell=True, capture_output=True)
    files = out.stdout.decode().split("\n")[:-1]
    print(files)
    return files


def clear_s3_result_files(bucket_path: str = "s3://prefect-orion/demo/"):
    subprocess.run(f"aws s3 rm {bucket_path} --recursive", shell=True)


def create_s3_block(name: str = "demo"):
    s3 = S3(bucket_path=f"prefect-orion/{name}")
    uuid = s3.save(name, overwrite=True)
    slug = s3.dict().get("block_type_slug")
    print(f"Created block {slug}/{name} with ID: {uuid}")


if __name__ == "__main__":
    create_s3_block()
    clear_s3_result_files()
    from prefect import flow
    from prefect.orion.schemas.states import Completed

    @flow(persist_result=True, result_storage="s3/demo")
    def foo():
        return Completed(data="completed")

    foo()
    time.sleep(3)
    get_s3_result_files()
    clear_s3_result_files()
