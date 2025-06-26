# ECS-specific configuration
resource "aws_ecs_cluster" "traffic_simulation_cluster" {
  name = var.ecs_cluster_name
}
