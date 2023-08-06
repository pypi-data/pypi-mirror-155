import boto3
import logging

def put_metrics(namespace, metric_name, metric_value, metric_unit='Count', dimensions=[]):
    cloudwatch = boto3.client('cloudwatch')

    logging.info("Putting metric %s to cloudwatch", metric_name)

    response = cloudwatch.put_metric_data(
    MetricData = [
        {
            'MetricName': metric_name,
            'Unit': metric_unit,
            'Value': metric_value,
            'Dimensions': dimensions
        },
    ],
    Namespace=namespace
)