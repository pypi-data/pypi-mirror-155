import os
from google.cloud import storage
from pubsub import publish

# TODO:
#   1. Wrap GCP functionality to create CapturML low-level API
#   2. Create CapturML high-level API
#   3. Define initialisation routine to handle authentication with GCP, Sentry, etc.




# authenticate
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/jackbl/Documents/captur/captur-app-5b837a97f077.json"

# def create_gcs_file(bucket_name, contents, destination_blob_name):
#     """Uploads a file to the bucket."""

#     # The ID of your GCS bucket
#     # bucket_name = "your-bucket-name"

#     # The contents to upload to the file
#     # contents = "these are my contents"

#     # The ID of your GCS object
#     # destination_blob_name = "storage-object-name"

#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)
#     blob = bucket.blob(destination_blob_name)

#     blob.upload_from_string(contents)

#     print(
#         f"{destination_blob_name} with contents {contents} uploaded to {bucket_name}."
#     )



# # create_gcs_file("ml-test-europe-west-2", "Here is some test data", "upload_test.txt")
# # print(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])


# # publish({
# #     "test_payload": 25,
# #     "test_string": "Some stuff"
# # }, "capturpwa", "ml-evaluation-development")

# # # If you don't specify credentials when constructing the client, the
# # # client library will look for credentials in the environment.
# # storage_client = storage.Client()

# # # Make an authenticated API request
# # buckets = list(storage_client.list_buckets())
# # print(buckets)

# publish({"hello": "pubsub"}, "capturpwa", "ml-pubsub-test")