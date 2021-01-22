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

# TEST - send email function
# from mailjet_rest import Client
# api_key = 'f0b62ec8d9479beeed284b8e2f97c38d'
# api_secret = '7f57fd3681038880dd2ffa8df220c1e8'
# mailjet = Client(auth=(api_key, api_secret), version='v3.1')
# data = {
#   'Messages': [
# 				{
# 						"From": {
# 								"Email": "UTP56479user@gmail.com",
# 								"Name": "Me"
# 						},
# 						"To": [
# 								{
# 										"Email": "uyen.a.tran@gmail.com",
# 										"Name": "You"
# 								}
# 						],
# 						"Subject": "Python-test2",
# 						"TextPart": "New events!",
# 						"HTMLPart": "<h3> New events</h3>"
# 				}
# 		]
# }
# result = mailjet.send.create(data=data)