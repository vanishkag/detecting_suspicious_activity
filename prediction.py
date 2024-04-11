from hdfs import InsecureClient
import json

hdfs_file_path = '/twitter_data/prediction_data.json'

json_file = 'prediction_data.json'

client = InsecureClient('http://localhost:9870', user='vanis')

try:
    if client.status(hdfs_file_path, strict=False):
        # Delete the existing file
        client.delete(hdfs_file_path)
        print(f"Existing file {hdfs_file_path} deleted.")
except Exception as err:
    if 'not a directory' in str(err):
        print(f"Error: {err}")
    else:
        raise err

# Upload new file to HDFS

try:
    client.upload(hdfs_file_path, json_file)
    print(f"File {json_file} uploaded to {hdfs_file_path}.")
except Exception as err:
    print(f"Error uploading file to HDFS: {err}")