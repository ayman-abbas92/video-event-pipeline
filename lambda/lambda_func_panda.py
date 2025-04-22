import json
import boto3
import os
import pandas as pd
from datetime import datetime
from io import BytesIO, StringIO
import gzip

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    print(f"Processing file from bucket: {bucket}, key: {key}")

    # Read the file from S3
    obj = s3.get_object(Bucket=bucket, Key=key)
    file_content = obj['Body'].read().decode('utf-8')

   # Load into a pandas DataFrame
    try:
        df = pd.read_json(StringIO(file_content), lines=True)
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
        return {'statusCode': 400, 'body': 'Invalid JSON file'}

    # Normalize dimensions: replace null or empty with 'undefined'
    for col in ['impression_id', 'campaign_id', 'datetime', '', 'device_type', 'quartile']:
        df[col] = df[col].fillna('').replace('', 'undefined')

    # Clean numeric fields: fill null/empty with 0.0 and ensure float type
    for col in ['client_price_amount', 'duration']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

    # Campaigns: total price and count
    campaigns_stats_df = df.groupby('campaign_id')['client_price_amount'].agg(
        total_price='sum', count='count'
    ).reset_index()

    campaigns_stats = campaigns_stats_df.set_index('campaign_id').to_dict(orient='index')

    # Devices: average duration
    device_stats_df = df.groupby('device_type')['duration'].agg(
        total_duration='sum', count='count', avg_duration='mean'
    ).reset_index()

    # Calculate average duration per device (if quartile is used)
    # Step 1: Group by device_type and impression_id to get duration per impression
    # impression_level = df.groupby(['device_type', 'impression_id'])['duration'].sum().reset_index()

    # Step 2: Now group by device_type again to get average duration per impression
    # avg_duration_per_device = impression_level.groupby('device_type')['duration'].mean().reset_index(name='avg_duration')


    device_stats_avg = device_stats_df.set_index('device_type').to_dict(orient='index')

    # Final results
    results = {
        'campaigns_stats': campaigns_stats,
        'device_stats_avg': device_stats_avg
    }

    # Save results to S3
    output_bucket = 'video-event-bucket-aggregated'
    output_key = datetime.datetime.now().strftime("%Y/%m/%d/aggregated_stats.json.gz")

    output_data = json.dumps(results).encode('utf-8')
    compressed_data = gzip.compress(output_data)

    s3.put_object(
        Bucket=output_bucket,
        Key=output_key,
        Body=compressed_data,
        ContentType='application/json',
        ContentEncoding='gzip'
    )

    print(f"Aggregated stats saved to s3://{output_bucket}/{output_key}")

    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete')
    }