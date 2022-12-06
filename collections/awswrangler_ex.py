import awswrangler as wr

dirs = wr.s3.list_directories("s3://prefect-orion/")
print(dirs)

objects = wr.s3.list_objects("s3://prefect-orion/docs/")
print(objects)

# import os
# local_file_dir = "/Users/anna/repos/pacc-berlin"

wr.s3.download(path='s3://prefect-orion/docs/best_practices.md', local_file="best.md")
