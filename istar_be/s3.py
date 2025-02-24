from . import settings
import boto3

image_dict = {}


class S3:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )

    def get_image(self, name):
        name = name.lower()
        if name in image_dict:
            return image_dict[name]

        file_obj = self.s3.get_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=name + ".jpeg"
        )
        image = file_obj["Body"].read()
        image_dict[name] = image
        return image
