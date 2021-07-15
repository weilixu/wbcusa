from storages.backends.s3boto3 import S3Boto3Storage

# this class is to store the user uploaded files in a different location and
# also to tell S3 to not override files with the same name


class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
