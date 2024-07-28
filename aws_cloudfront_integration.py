from diagrams import Cluster, Diagram, Edge
from diagrams.aws.network import CloudFront, ELB, Route53
from diagrams.aws.compute import EC2
from diagrams.aws.storage import S3
from diagrams.aws.database import RDS
from diagrams.aws.security import WAF, Shield, IAMRole
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import ACM
from diagrams.generic.place import Datacenter

with Diagram("AWS CloudFront Integration", show=False):
    dns = Route53("DNS")
    
    with Cluster("AWS Cloud"):
        cf = CloudFront("CloudFront")
        waf = WAF("WAF")
        shield = Shield("Shield")

        with Cluster("Edge Locations"):
            edge = Datacenter("Edge Locations")
        
        with Cluster("Origin Servers"):
            lb = ELB("Load Balancer")
            with Cluster("Web Servers"):
                web_servers = [EC2("Web Server 1"), EC2("Web Server 2")]

            with Cluster("S3 Buckets"):
                s3_origin = S3("S3 Bucket")

            with Cluster("Database Cluster"):
                db_primary = RDS("Primary DB")
                db_replicas = [RDS("Replica DB 1"), RDS("Replica DB 2")]

    acm = ACM("ACM Certificate")
    iam = IAMRole("IAM Role")
    monitoring = Cloudwatch("CloudWatch")

    # Connections
    dns >> Edge(label="Route Traffic", color="blue") >> cf
    cf >> Edge(label="DDoS Protection", color="red") >> shield
    cf >> Edge(label="Web Application Firewall", color="green") >> waf
    cf >> Edge(label="Serve Content", color="blue") >> edge
    edge >> Edge(label="Fetch Content", style="dashed") >> [lb, s3_origin]
    lb >> web_servers
    web_servers >> db_primary
    db_primary >> db_replicas
    cf >> acm
    cf >> iam
    cf >> monitoring

