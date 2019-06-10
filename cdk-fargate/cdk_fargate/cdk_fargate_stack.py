from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_ssm as ssm,
    cdk
)


class CdkFargateStack(cdk.Stack):

    def __init__(self, app: cdk.App, id: str, **kwargs) -> None:
        super().__init__(app, id)

        # Create VPC and Fargate Cluster
        # NOTE: Limit AZs to avoid reaching resource quotas
        vpc = ec2.Vpc(
            self,
            "hqtrackbot-vpc",
            max_a_zs=1
        )

        cluster = ecs.Cluster(
            self,
            "hqtrackbot-cluster",
            vpc=vpc
        )

        task_def = ecs.FargateTaskDefinition(
            self,
            "hqtrackbot-task-definition",
            memory_mi_b="512",
            cpu="256"
        )

        task_def.add_container(
            "hqtrackbot-container",
            image=ecs.ContainerImage.from_registry("scottbrenner/hqtrackbot:latest"),
            environment={
                "REDDIT_SUBREDDITS": "hqtrackbot+electronicmusic+techno+proghouse+liquiddubstep+house+tech_house+OldSkoolDance+acidhouse+ambientmusic+AtmosphericDnB+BigBeat+boogiemusic+breakbeat+chicagohouse+chillout+Chipbreak+Chiptunes+complextro+cxd+darkstep+deephouse+DnB+DubStep+EDM+EBM+electronicdancemusic+ElectronicJazz+ElectronicBlues+electrohiphop+electrohouse+electronicmagic+electropop+electroswing+ExperimentalMusic+fidget+filth+frenchelectro+frenchhouse+funkhouse+fusiondancemusic+futurebeats+FutureFunkAirlines+FutureGarage+futuresynth+gabber+glitch+glitchop+Grime+happyhardcore+hardhouse+hardstyle+idm+industrialmusic+ItaloDisco+latinhouse+mashups+melodichouse+minimal+mixes+moombahcore+nightstep+OldskoolRave+Outrun+theOverload+partymusic+plunderphonics+psybient+PsyBreaks+psytrance+purplemusic+raggajungle+RealDubstep+skweee+swinghouse+tranceandbas+trap+tribalbeats+TropicalHouse+ukfunky+witchhouse+wuuB+SirBerryDinglesDiscog+AfroBashment",
                "AWS_ACCESS_KEY_ID": ssm.ParameterStoreSecureString(parameter_name="HQTB_AWS_ACCESS_KEY_ID", version=1).to_string(),
                "HQTB_AWS_METRIC_STREAM_ID": ssm.ParameterStoreSecureString(parameter_name="HQTB_AWS_METRIC_STREAM_ID", version=1).to_string(),
                "HQTB_AWS_SECRET_ACCESS_KEY": ssm.ParameterStoreSecureString(parameter_name="HQTB_AWS_SECRET_ACCESS_KEY", version=1).to_string(),
                "HQTB_REDDIT_CLIENT_ID": ssm.ParameterStoreSecureString(parameter_name="HQTB_REDDIT_CLIENT_ID", version=1).to_string(),
                "HQTB_REDDIT_CLIENT_SECRET": ssm.ParameterStoreSecureString(parameter_name="HQTB_REDDIT_CLIENT_SECRET", version=1).to_string(),
                "HQTB_REDDIT_PASSWORD": ssm.ParameterStoreSecureString(parameter_name="HQTB_REDDIT_PASSWORD", version=1).to_string(),
                "HQTB_REDDIT_USERNAME": ssm.ParameterStoreSecureString(parameter_name="HQTB_REDDIT_USERNAME", version=1).to_string(),
                "HQTB_YOUTUBE_DEVELOPER_KEY": ssm.ParameterStoreSecureString(parameter_name="HQTB_YOUTUBE_DEVELOPER_KEY", version=1).to_string(),
            }
        )

        # Instantiate ECS Service with just cluster and image
        ecs.FargateService(
            self,
            "hqtrackbot-fargate-service", 
            cluster=cluster,
            task_definition=task_def,
            service_name="hqtrackbot-service"
        )

app = cdk.App()
CdkFargateStack(app, "hqtrackbot")
app.run()
