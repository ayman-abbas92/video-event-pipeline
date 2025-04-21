# 📊 Video Event Metrics Pipeline

This project sets up a simple serverless data pipeline using AWS services to process video impression events and compute basic metrics by campaign and device type.

## 🚀 Features
- Upload video event batches to S3 (`data/input/` folder).
- Automatically trigger a Lambda function to:
  - Compute total impressions and revenue per campaign.
  - Compute average play duration per device type.
  - Output results to S3 (`yyyy/mm/dd/` folder).
- Infrastructure managed with Terraform.

---

## 🗂️ Project Structure
```
video-event-pipeline/
├── data/
│   └── input/events.jsonl         # Sample input data
├── lambda/
│   └── lambda_function.py         # Lambda processing logic
├── scripts/
│   ├── package_lambda.sh          # Script to package Lambda zip
│   └── upload_to_s3.py            # Upload script for test data
├── terraform/
│   ├── main.tf                    # AWS resources (S3, Lambda, IAM)
│   ├── variables.tf               # Variable declarations
│   ├── terraform.tfvars           # Input values for variables
├── function.zip                   # Zipped Lambda function (generated)
└── README.md                      # You're here!
```

---

## 🧰 Prerequisites
- AWS CLI configured
- Terraform installed (`>= 1.0`)
- Python 3.8+
- `boto3` installed: `pip install boto3`

---

## 🏗️ Deployment

## 1. Create Terraform variables
```
aws_region               = "eu-west-2"
aws_bucket_name          = "video-event-bucket"
aws_lambda_function_name = "process_video_events"
aws_access_key           = "<your-aws-access-key>"
aws_secret_key           = "<your-aws-secret-key>"
```

### 2. Initialize and apply Terraform:
```bash
cd terraform
terraform init
terraform apply 
```

### 3. Package the Lambda function:
```bash
sudo chmod +x /scripts/package_lambda.sh
./scripts/package_lambda.sh
```

### 4. Re-apply to upload the function (if needed):
```bash
terraform apply
```

---

## 📤 Upload Test Data
```bash
python3 scripts/upload_to_s3.py video-event-bucket-pipeline data/input/events.txt data/input/events.txt
```

---

## 📈 Output
The Lambda function writes the transformed results to:
```
s3://video-event-bucket-aggregated/yyyy/mm/dd/aggregated_stats.json.gz
```

---

## 🧪 Sample Metrics Output
```json
{
    "campaigns_stats": {
        "C1": {"total_price": 1.2, "count": 2}, 
        "C2": {"total_price": 0.8, "count": 2}
    }, 
    "device_stats_avg": {
        "mobile": {"total_duration": 25, "count": 2, "avg_duration": 12.5}, 
        "desktop": {"total_duration": 32, "count": 2, "avg_duration": 16.0}
    }
}
```

---

## 🧠 Extend This Project
- Add schema validation using AWS Glue or `pydantic`
- Store metrics in DynamoDB or Redshift
- Build a dashboard using Metabase https://www.metabase.com/

---

## 👤 Author
Ayman Abbas

---

## 🛡️ License
MIT or internal use — feel free to adapt and extend.
