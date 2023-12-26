import boto3

s3 = boto3.client(
    "s3",
    aws_access_key_id="AKIAXEDILO2IDNSIX3IF",
    aws_secret_access_key="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",
)
s3.put_object(
    Bucket="organisation-hospital",
    Key="patients/patient-1/",
    # Body="Hello World!",
)
