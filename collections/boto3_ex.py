from prefect_aws import AwsCredentials

aws = AwsCredentials.load("default")
s3 = aws.get_boto3_session().client(service_name="s3")
bucket = "prefect-orion"
object_name = "duck.png"
local_file_name = "images/duck.png"
# s3.upload_file(local_file_name, bucket, object_name)
s3.download_file(bucket, object_name, "new_duck.png")
# s3.list_objects()
# s3.head_object()
# s3.delete_object()
