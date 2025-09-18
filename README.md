# CloudFlow Loyalty Platform

CloudFlow Loyalty Platform is a serverless, AWS-native solution for managing customer loyalty programs, including customer accounts, points accumulation/redemption, and rewards catalog. The platform leverages AWS Lambda, API Gateway, DynamoDB, and S3, with infrastructure managed via Terraform.

## Features

- **Customer API**: Register, update, and manage customer profiles.
- **Points Engine**: Calculate, earn, and redeem loyalty points.
- **Rewards API**: Manage rewards catalog and redemption.
- **Purchase Processor**: Batch process purchase data from S3 and award points.
- **RESTful API**: Exposed via API Gateway with proxy path mapping.
- **Infrastructure as Code**: Modular Terraform for networking, compute, and storage.
- **Automated Testing**: Unit, integration, and performance tests.

## Architecture

- **API Gateway**: Entry point for all client requests.
- **Lambda Functions**: Stateless compute for business logic.
- **DynamoDB**: NoSQL storage for customers, points, and rewards.
- **S3**: Storage for purchase data and artifacts.
- **CloudWatch**: Logging and monitoring.

See [docs/system-design.md](docs/system-design.md) for detailed architecture diagrams and data models.

## Directory Structure

```
terraform/           # Infrastructure as code (modular Terraform)
  modules/
    compute/
    networking/
    storage/
src/
  lambda/
    customer-api/
    points-engine/
    rewards-api/
    purchase-processor/
  tests/
    customer_api/
    integration/
    performance/
    script.sh
docs/
  system-design.md
  aws-well-architected-compliance.md
```

## Getting Started

### Prerequisites

- [Terraform](https://www.terraform.io/) >= 1.0
- AWS CLI credentials (with appropriate permissions)
- Python 3.9+ for Lambda code and tests
- [pip](https://pip.pypa.io/en/stable/) for dependencies

### Deployment

1. **Configure AWS Credentials**  
   Set your AWS credentials as environment variables or via AWS CLI.

2. **Initialize Terraform**
   ```sh
   cd terraform
   terraform init
   ```

3. **Apply Infrastructure**
   ```sh
   terraform apply
   ```

4. **Deploy Lambda Code**  
   (Terraform modules package and deploy Lambda functions from `src/lambda/`.)

### Testing

- **Unit Tests:**  
  Run with `pytest` in the `src/tests/customer_api/` directory.

- **Integration Tests:**  
  See `src/tests/integration/` and use `pytest`, parameterizing the API URL.

- **Performance Tests:**  
  Use [Locust](https://locust.io/) with `src/tests/performance/load_test.py`.

- **Manual API Testing:**  
  Use the provided [script.sh](src/tests/script.sh) with your API Gateway URL.

### API Endpoints

- `POST /customers` - Register new customer
- `GET /customers/{id}` - Get customer profile
- `PUT /customers/{id}` - Update customer profile
- `POST /points/earn` - Earn points
- `POST /points/redeem` - Redeem points
- `GET /points/{customer_id}` - Get points history
- `GET /rewards` - List rewards
- `POST /rewards` - Create reward
- `PUT /rewards/{id}` - Update reward
- `DELETE /rewards/{id}` - Deactivate reward

See [docs/system-design.md](docs/system-design.md) for full API details.

## Compliance & Best Practices

- Follows AWS Well-Architected Framework ([docs/aws-well-architected-compliance.md](docs/aws-well-architected-compliance.md))
- Secure by default: IAM least privilege, encrypted data, no hardcoded secrets
- Modular, reusable infrastructure and code

## License

MIT License

---

For more details, see [docs/system-design.md](docs/system-design.md)
