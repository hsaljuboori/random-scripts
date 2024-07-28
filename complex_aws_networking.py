from diagrams import Cluster, Diagram, Edge
from diagrams.aws.network import ELB, Route53, VPC, NATGateway, InternetGateway
from diagrams.aws.compute import EC2
from diagrams.aws.storage import S3
from diagrams.aws.database import RDS
from diagrams.aws.security import IAMRole, KMS
from diagrams.aws.management import Cloudwatch

with Diagram("Complex AWS Networking", show=False):
    dns = Route53("DNS")
    
    with Cluster("VPC"):
        igw = InternetGateway("Internet Gateway")
        nat = NATGateway("NAT Gateway")

        with Cluster("Public Subnet"):
            lb = ELB("Load Balancer")
            web_servers = [EC2("Web Server 1"),
                           EC2("Web Server 2")]

        with Cluster("Private Subnet"):
            app_servers = [EC2("App Server 1"),
                           EC2("App Server 2")]

            with Cluster("Database Cluster"):
                db_primary = RDS("Primary DB")
                db_replicas = [RDS("Replica DB 1"), RDS("Replica DB 2")]

        with Cluster("S3 Buckets"):
            s3_bucket1 = S3("Bucket 1")
            s3_bucket2 = S3("Bucket 2")

    kms = KMS("Key Management Service")
    iam = IAMRole("IAM Role")
    monitoring = Cloudwatch("CloudWatch")

    # Connections
    dns >> lb
    igw >> lb
    lb >> web_servers
    for web_server in web_servers:
        web_server >> app_servers
    for app_server in app_servers:
        app_server >> db_primary
        app_server >> s3_bucket1
        app_server >> s3_bucket2
    db_primary >> db_replicas
    db_primary >> kms
    app_servers >> iam
    app_servers >> nat >> igw

