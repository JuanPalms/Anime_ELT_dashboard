"""
This module generates an image describing the project pipeline using the diagrams library.
"""
from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.integration import Eventbridge
from diagrams.aws.storage import S3
from diagrams.onprem.client import User
from diagrams.programming.flowchart import Database, Action
from diagrams.programming.language import Python

with Diagram("Pipeline de análisis de anime", show=False):
    with Cluster("AWS"):
        lambda_function = Lambda("Web Scrapping\n+ Limpieza de datos")
        eventbridge = Eventbridge("CloudWatch Events")
        s3_bucket = S3("Bucket S3")
        ec2_instance = EC2("Instancia EC2\n+ Streamlit")

    with Cluster("Web Scrapping"):
        web_scrapping = Python("Extracción de datos")
        clean_data = Python("Limpieza de datos")

    with Cluster("Dashboard"):
        user = User("Usuario")
        cache = Database("Datos en caché")
        dashboard = Python("Dashboard Streamlit")
        process_data = Python("Procesamiento de datos")

    eventbridge >> lambda_function >> s3_bucket
    s3_bucket >> ec2_instance >> dashboard >> cache
    user >> dashboard

    lambda_function - Edge(color="blue", style="dashed") - ec2_instance

    web_scrapping >> Edge(color="red", style="dotted") - clean_data
    clean_data >> Edge(color="red", style="dotted") - lambda_function

    process_data >> Edge(color="green", style="dotted") - dashboard
    ec2_instance >> process_data
