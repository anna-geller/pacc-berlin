"""
https://github.com/PrefectHQ/prefect/pull/7164
https://docs.python.org/3/library/lzma.html
https://docs.python.org/3/library/bz2.html
"""
from prefect import flow, task
from prefect.serializers import CompressedSerializer


@task(
    persist_result=True,
    # more complicated but allows specific compression library
    result_serializer=CompressedSerializer(compressionlib="zlib", serializer="pickle"),
)
def get_some_large_result():
    return 42


@flow(result_serializer="compressed/pickle")
def flow_with_compressed_serializer():
    get_some_large_result()
    return "Hi from Results with task with compressed pickle serializer! 👋"


if __name__ == "__main__":
    flow_with_compressed_serializer()
