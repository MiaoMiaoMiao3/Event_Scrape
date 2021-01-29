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
								"Email": os.environ["SENDER"],
								"Name": "Me"
						},
						"To": [
								{
										"Email": os.environ["RECEIVER"],
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