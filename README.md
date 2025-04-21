# 📊 Video Event Metrics Pipeline

This project sets up a simple serverless data pipeline using AWS services to process video impression events and compute basic metrics by campaign and device type.

## 🚀 Features
- Upload video event batches to S3 (`input/` folder).
- Automatically trigger a Lambda function to:
  - Compute total impressions and revenue per campaign.
  - Compute average play duration per device type.
  - Output results to S3 (`output/` folder).
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

### 1. Initialize and apply Terraform:
```bash
cd terraform
terraform init
terraform apply
```

### 2. Package the Lambda function:
```bash
./scripts/package_lambda.sh
```

### 3. Re-apply to upload the function (if needed):
```bash
terraform apply
```

---

## 📤 Upload Test Data
```bash
python scripts/upload_to_s3.py video-event-bucket-pipeline input/events.jsonl data/input/events.jsonl
```

---

## 📈 Output
The Lambda function writes the transformed results to:
```
s3://video-event-bucket-pipeline/output/events_output.json
```

---

## 🧪 Sample Metrics Output
```json
{
  "total_impressions_per_campaign": {"abc123": 10},
  "total_revenue_per_campaign": {"abc123": 200.0},
  "average_play_duration_per_device": {"mobile": 12.4, "desktop": 18.1}
}
```

---

## 🧠 Extend This Project
- Add schema validation using AWS Glue or `pydantic`
- Store metrics in DynamoDB or Redshift
- Add API Gateway to expose analytics endpoint
- Build a dashboard using Metabase https://www.metabase.com/

---

## 👤 Author
Ayman Abbas

---

## 🛡️ License
MIT or internal use — feel free to adapt and extend.
