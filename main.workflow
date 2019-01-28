action "Docker Registry Login" {
  uses = "actions/docker/login@76ff57a"
  secrets = ["DOCKER_USERNAME", "DOCKER_PASSWORD"]
}

action "Docker Build" {
  uses = "actions/docker/cli@76ff57a"
  needs = ["Docker Registry Login"]
  args = "build -t scottbrenner/hqtrackbot ."
}

action "Docker Push" {
  uses = "actions/docker/cli@76ff57a"
  needs = ["Docker Build"]
  args = "push scottbrenner/hqtrackbot:latest"
}


action "New ECS Deployment" {
  uses = "actions/aws/cli@8d31870"
  needs = ["Create ECS Task Definition"]
  args = "--region us-west-1 ecs update-service --cluster hqtrackbot --service hqtrackbot --task-definition hqtrackbot --force-new-deployment"
  secrets = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
}