from google.cloud import storage
from google.cloud.storage import Blob

#Create a client object
storage_client = storage.Client.from_service_account_json("python-test2-key.json")

#CONSTANTS
BUCKET_NAME = 'python-test2-bucket'
source_file_name = "test2.txt"
destination_blob_name = "test2.txt"


bucket = storage_client.get_bucket(BUCKET_NAME)

blob = bucket.blob(source_file_name)
blob.upload_from_filename(destination_blob_name)

print(
    "File {} uploaded to {}.".format(
        source_file_name, destination_blob_name
    )
)
