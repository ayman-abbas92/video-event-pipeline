import json
import boto3
import gzip
import datetime

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    ## bucket = event['bucket']
    ## key = event['key']

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    print(f"Processing file from bucket: {bucket}, key: {key}")

    # Read the file from S3
    obj = s3.get_object(Bucket=bucket, Key=key)
    lines = obj['Body'].read().decode('utf-8').splitlines()

    campaigns_stats = {}
    device_stats_avg = {}

    for line in lines:
        try:
            # Assuming each line is a JSON object
            event = json.loads(line)
            campaign_id = event['campaign_id']
            price = event['client_price_amount']
            device = event['device_type']
            duration = event['duration']

            if not campaign_id or campaign_id == "":
                continue

            if campaign_id not in campaigns_stats:
                campaigns_stats[campaign_id] = {'total_price': 0, 'count': 0}
            campaigns_stats[campaign_id]['total_price'] += price or 0.0
            campaigns_stats[campaign_id]['count'] += 1

            if device not in device_stats_avg:
                device_stats_avg[device] = {'total_duration': 0, 'count': 0}
            device_stats_avg[device]['total_duration'] += duration or 0
            device_stats_avg[device]['count'] += 1
            # Calculate average duration for each device
            device_stats_avg[device]['avg_duration'] = device_stats_avg[device]['total_duration'] / device_stats_avg[device]['count']

        except json.JSONDecodeError:
            print(f"Error decoding JSON: {line}")
        except KeyError as e:
            print(f"Missing key in JSON: {e}")
        except Exception as e:
            print(f"Error processing line: {line}, Error: {e}")

    results = {
        'campaigns_stats': campaigns_stats,
        'device_stats_avg': device_stats_avg
    }

    # Save results to S3
    output_bucket = 'video-event-bucket-aggregated'
    output_key = datetime.datetime.now().strftime("%Y/%m/%d/aggregated_stats.json.gz")
    output_data = json.dumps(results).encode('utf-8')
    compressed_data = gzip.compress(output_data)
    s3.put_object(Bucket=output_bucket, Key=output_key, Body=compressed_data, ContentType='application/json', ContentEncoding='gzip')
    print(f"Aggregated stats saved to s3://{output_bucket}/{output_key}")
    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete')
    }