# TEST - Uploading file to bucket
# from google.cloud import storage
# from google.cloud.storage import Blob

# #Create a client object
# storage_client = storage.Client.from_service_account_json("python-test2-key.json")

# #CONSTANTS
# BUCKET_NAME = 'python-test2-bucket'
# source_file_name = "test2.txt"
# destination_blob_name = "test2.txt"


# bucket = storage_client.get_bucket(BUCKET_NAME)

# blob = bucket.blob(source_file_name)
# blob.upload_from_filename(destination_blob_name)

# print(
#     "File {} uploaded to {}.".format(
#         source_file_name, destination_blob_name
#     )
# )


from mailjet_rest import Client
from google.cloud import storage
import os

storage_client = storage.Client.from_service_account_json("python-test2-key.json")
BUCKET_NAME = 'python-test2-bucket'
bucket = storage_client.get_bucket(BUCKET_NAME)
filename = list(bucket.list_blobs(prefix=''))
bucket_data = bucket.blob("event.txt").download_as_string().decode('cp1252')

api_key = os.environ['MAILJETKEY']
api_secret = os.environ['MAILJETSECRET']
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
data = {
  'Messages': [
				{
						"From": {
								"Email": "UTP56479user@gmail.com",
								"Name": "Me"
						},
						"To": [
								{
										"Email": "uyen.a.tran@gmail.com",
										"Name": "You"
								}
						],
						"Subject": "Desktop Events Test",
						"TextPart": "",
						"HTMLPart": f"<h3>Greetings! Things you should look into this weekend: </h3> <div style='white-space: pre-wrap'>{bucket_data}</div>"
				}
		]
}
result = mailjet.send.create(data=data)
print('email sent.')