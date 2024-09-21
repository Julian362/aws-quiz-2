from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError

server = Flask(__name__)

s3 = boto3.client('s3')

@server.route("/buckets", methods=['GET'])
def list_objects():
    bucket_name = request.args.get('name')
    
    if not bucket_name:
        return jsonify({"error": "Bucket name is required"}), 400

    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            objects = [obj['Key'] for obj in response['Contents']]
            return jsonify({"bucket": bucket_name, "objects": objects})
        else:
            return jsonify({"bucket": bucket_name, "objects": []})  # No objects in the bucket

    except ClientError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    server.run(host='0.0.0.0',port=4321)
