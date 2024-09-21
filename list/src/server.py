from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError

server = Flask(__name__)

s3 = boto3.client('s3')

@server.route("/buckets", methods=['GET'])
def list_buckets():
    try:
        response = s3.list_buckets()
        buckets = response['Buckets']
        buckets_names = [bucket['Name'] for bucket in buckets]
        return jsonify(buckets_names)

    except ClientError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    server.run(host='0.0.0.0')
