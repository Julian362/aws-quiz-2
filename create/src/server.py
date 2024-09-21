from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError
server = Flask(__name__)

s3 = boto3.client(
    's3',)


from botocore.exceptions import ClientError

@server.route("/buckets/create", methods=['POST'])
def create_bucket():
    bucket_name = request.json.get('name')
    if not bucket_name:
        return jsonify({"error": "Bucket name is required"}), 400

    try:
        s3.head_bucket(Bucket=bucket_name)
        return jsonify({"error": f"Bucket '{bucket_name}' already exists."}), 400
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            try:
                s3.create_bucket(Bucket=bucket_name)
                return jsonify({"message": f"Bucket '{bucket_name}' created successfully!"}), 201
            except ClientError as e:
                return jsonify({"error": str(e)}), 400
        else:
            return jsonify({"error": str(e)}), 400





if __name__ == "__main__":
    server.run(host='0.0.0.0',port=1234)
