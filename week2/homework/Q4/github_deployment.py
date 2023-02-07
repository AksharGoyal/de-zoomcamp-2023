from prefect.deployments import Deployment 
from prefect.filesystems import GitHub
from web_to_gcs_homework_q4 import etl_gcs_to_bq

github_block = GitHub.load("prefect-zoomcamp-github")

github_deployment = Deployment.build_from_flow(
    flow=etl_gcs_to_bq,
    name='Load to GCS via Github',
    storage=github_block,
    entrypoint='week2/homework/Q4/web_to_gcs_bq.py:etl_gcs_to_bq',
    parameters={'months':[11], 'color':'green', 'year':2020}
)

github_deployment.apply()