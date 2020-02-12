# MetPy & AWS Lambda Example

This consists of two pieces, a lambda layer that provides MetPy, Cartopy, XArray, and related dependencies. The other piece is a sample lambda function in `lambda_function.py` which plots an example from MetPy and saves it to S3.

## Building the Lambda Layer

The `lambda-layer` folder contains a Dockerfile and a build script. Execute the build script to produce a `metpy_layer.zip`. Then upload the resulting zip file to S3 so that you can use it for the creation of the Lambda layer.

```
cd lambda-layer
./build.sh
aws s3 cp layer/metpy_layer.zip s3://yourbucketexample/metpy_layer.zip
```

## Creating the Lambda Layer

Go into the AWS Console -> Lambda -> Layers and create a new layer. Pick upload from S3 and pass the path where you uploaded your zip file. Pick works with Python 3.7.

## Creating the Lambda Function

Go into the AWS Console -> Lambda -> Functions and create a new function. When you create this function for the purposes of this demonstration you will want to give the role S3 access to write to the bucket you are using. When you create the function add a layer and pick the layer you created in the step above. Copy in the example code from lambda_function.py and give it a try. You can test with any input data, it doesn't depend on it so it doesn't matter.

