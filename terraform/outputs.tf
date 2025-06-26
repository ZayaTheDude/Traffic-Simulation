# Outputs for Terraform
output "ecs_cluster_id" {
  value = aws_ecs_cluster.traffic_simulation_cluster.id
}
