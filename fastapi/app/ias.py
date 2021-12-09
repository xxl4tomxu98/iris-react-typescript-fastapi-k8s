from jinja2.loaders import BaseLoader
from kubernetes import client, config
import os, yaml
from .logger import logger
from jinja2 import Environment

def authenticate(conf=config):
    '''
    Function to authenticate to the cluster and list all available pods with corresponding IPs
    '''
    if os.getenv('KUBERNETES_SERVICE_HOST', False):
        conf.load_incluster_config()
    else:
        conf.load_kube_config(config_file='/etc/rancher/k3s/k3s.yaml')
    return conf

def list_pods():
    authenticate()
    v1 = client.CoreV1Api()
    logger.info("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        logger.info("%s\t%s\t%s" %
              (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

# Example of job CRUD https://github.com/kubernetes-client/python/blob/master/examples/job_crud.py
# def retrieve_config_object(workload):
def retrieve_config_object():    
    """
    A helper function that retrieves kubernetes configmap objects
    """
    authenticate()
    v1 = client.CoreV1Api()
    logger.info("Grabbing namespaced configmaps")
    ret = v1.read_namespaced_config_map('test-configmap', os.getenv('NAMESPACE'))
    # Not hitting the for loop when running k3s
    # for i in ret.items:
    #     logger.info("%s\t%s\t%s" %
    #           (i.metadata.labels['app'], i.metadata.namespace, i.metadata.name))
    # config_dir = os.getenv("DPS_WORKLOAD_CONFIG_PATH", "/etc/dps/manifests")
    logger.info(ret)
    return ret

# def template_config(config, **kwargs):
def template_config():
    """
    Take the output from retrieve_config_object and template it
    using e.g. Jinja
    Example: https://medium.com/@luongvinhthao/generate-yaml-file-with-python-and-jinja2-9474f4762b0d
    """
    configmap = retrieve_config_object()
    template = Environment(loader = BaseLoader).from_string(configmap.data['my-yaml.yaml'])
    data = template.render({'nsname':'test-namespace-for-cm'})
    return data

def run_job():
    """
    Uses the config objects (templated or not) to create Kubernetes Jobs
    Jobs docs: https://kubernetes.io/docs/concepts/workloads/controllers/job/
    """
    config_object = template_config()
    dct = yaml.safe_load(config_object)
    v1 = client.BatchV1Api()
    logger.info("Running k8s job")
    ret = v1.create_namespaced_job(os.getenv('NAMESPACE'), dct)

def get_running_jobs():
    """
    A function that finds running jobs with
    a given label
    See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/BatchV1Api.md#list_namespaced_job
    https://github.com/kubernetes-client/python/blob/master/examples/node_labels.py
    """
    authenticate()
    v1 = client.BatchV1Api().list_namespaced_job(os.getenv('NAMESPACE'))
    if v1.items[0].status.active == 1:
        logger.info(v1)
        return {'Success': 'Check Logger'}
    else:
        return {"Failure":"No Running Jobs found"}

def get_failed_jobs():
    """
    A function that finds failed jobs with
    a given label
    See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/BatchV1Api.md#list_namespaced_job
    https://github.com/kubernetes-client/python/blob/master/examples/node_labels.py

    """
    authenticate()
    v1 = client.BatchV1Api().list_namespaced_job(os.getenv('NAMESPACE'))
    if v1.items[0].status.failed == 1:
        logger.info(v1)
        return {'success': 'check logger'}
    else:
        return {"Failure":"No Failed Jobs found"}

def get_succeeded_jobs():
    """
    A function that finds succeeded jobs with
    a given label
    See: https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/BatchV1Api.md#list_namespaced_job
    https://github.com/kubernetes-client/python/blob/master/examples/node_labels.py

    """
    authenticate()
    v1 = client.BatchV1Api().list_namespaced_job(os.getenv('NAMESPACE'))
    if v1.items[0].status.succeeded == 1:
        logger.info(v1)
        return {'success': 'check logger'}
    else:
        return {"Failure":"No Succeeded Jobs found"}
    

if __name__ == '__main__':
    authenticate()