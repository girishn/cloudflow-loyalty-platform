# Networking Foundation
module "networking" {
  source = "./modules/networking"

  environment        = var.environment
  project_name       = var.project_name
  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones
}

# # Compute Resources
module "compute" {
  source = "./modules/compute"

  count = var.enable_compute ? 1 : 0

  environment              = var.environment
  project_name             = var.project_name
  vpc_id                   = module.networking.vpc_id
  private_subnets          = module.networking.private_app_subnets
  public_subnets           = module.networking.public_subnets
  lambda_security_group_id = module.networking.lambda_security_group_id
  lambda_subnet_ids        = module.networking.private_app_subnets
}

# # Storage
# module "storage" {
#   source = "./modules/storage"

#   count = var.enable_storage ? 1 : 0

#   environment  = var.environment
#   project_name = var.project_name
#   vpc_id       = module.networking.vpc_id
# }