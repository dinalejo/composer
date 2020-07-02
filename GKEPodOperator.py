import datetime
from airflow import models
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.contrib.operators.gcp_container_operator import GKEPodOperator
 
YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1) 
now = datetime.datetime.now()

with models.DAG(
        dag_id='start_pod_other_cluster', 
        schedule_interval=None, start_date=YESTERDAY) as dag: 
    
    kubernetes_main_pod = GKEPodOperator(task_id='execute_main', 
                                        name='main-pod', 
                                        namespace='production',
                                        image='gcr.io/google-containers/busybox', 
                                        cluster_name='demo-web-app',
                                        project_id='', 
                                        location='us-east1-b', 
                                        cmds=['sleep'], 
                                        arguments=['20'],
                                       # arguments=['test - ' + now.strftime("%m/%d/%Y, %H:%M:%S")],
                                       # resources={'limit_memory': 1, 'limit_cpu': 1, 'requests_cpu' : 0.4},
                                        resources={'requests_cpu' : 0.6},
                                       # replicas= '2',
                                        affinity={
                                                  'nodeAffinity': {
                                                                    'requiredDuringSchedulingIgnoredDuringExecution': {
                                                                        'nodeSelectorTerms': [{
                                                                            'matchExpressions': [{
                                                                                'key': 'cloud.google.com/gke-nodepool',
                                                                                'operator': 'In',
                                                                                'values': [
                                                                                    'production'
                                                                                ]
                                                                            }]
                                                                        }]
                                                                    }
                                                                }
                                                    }
                                        )
