from fastapi import FastAPI, Depends
from starlette.middleware.base import DispatchFunction
from fastapi.middleware.cors import CORSMiddleware
from healthcheck import HealthCheck
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi_login import LoginManager
import boto3, os
from starlette.middleware.base import BaseHTTPMiddleware
from .middlewares import log_requests
from dotenv import load_dotenv
from .logger import logger
from .ias import list_pods, retrieve_config_object, template_config, \
                run_job, get_running_jobs, get_failed_jobs, get_succeeded_jobs
from iris import iris_classifier_api

load_dotenv()
health = HealthCheck()
app = FastAPI(title = "Irir Classifier API",              
              version = 1.0,
              description = "Simple API to make predict class of iris plant.")

app.include_router(iris_classifier_api.router)

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)

app.add_middleware(    
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]    
)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to Iris Classification."}


manager = LoginManager(os.getenv('SECRET'), token_url='/authenticate')
fake_db = {'jonnel': {'password': 'passwordLogin'}}

@app.get('/authenticate')
def authenticate() -> dict:
    '''
    Authenticates to a fake database and creates access token
    '''
# def login(data: OAuth2PasswordRequestForm = Depends()):
#     email = data.username
#     password = data.password
    user = os.getenv('FAKE_USER')
    password = os.getenv('FAKE_PASSWORD')
    if not user:
        raise InvalidCredentialsException 
    elif password != fake_db[user]['password']:
        raise InvalidCredentialsException
    access_token = manager.create_access_token(
        data=dict(sub=user)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

@app.get('/list-pods')
def list_kubernetes_pods() -> dict:
    '''
    Lists k8s pods with corresponding IPs in the logs
    '''
    list_pods()
    return {'Success': 'Check Logs for list of pod IPs'}

@app.get('/get-config-object')
def retrieve_kubernetes_config() -> dict:
    '''
    Grabs the configmap object of a designated namespace
    '''
    retrieve_config_object()
    return {'Retrieved': 'Objects'}

@app.get('/template-config')
def template_kubernetes_config() -> dict:
    '''
    Templates the YAML from the config map object
    '''
    template_config()
    return {'Config Template': 'Success'}

@app.get('/run-job')
def run_kubernetes_job() -> dict:
    '''
    Creates a k8s job from the templated configmap object
    '''
    run_job()
    return {'Job Run': 'Success'}


@app.get('/upload')
def upload():
    '''
    Checks if local s3 bucket in Minio can communicate with FastApi server
    '''
    s3 = boto3.client('s3',
                    endpoint_url=os.getenv('ENDPOINT_URL'),
                    aws_access_key_id=os.getenv('S3_ACCESS_KEY_ID'),
                    aws_secret_access_key=os.getenv('S3_SECRET_ACCESS_KEY'),
                    config=os.getenv('S3_CONFIG_SIGNATURE'),
                    region_name=os.getenv('S3_REGION'))
    return s3.list_buckets()


def application_data() -> dict:
    '''
    Contains maintainer information regarding Github Repository
    '''
    return {"maintainers": "Nick Gayliard, Charles Landau, Jonnel Benjamin, Tom Xu",
            "git_repo": "https://github.com/gh-ai-solu/dps/tree/dev"}

health.add_section("application", application_data)

@app.get("/healthcheck")
def healthcheck():
    '''
    Returns a JSON object of healthchecks regarding the application
    '''
    message, status_code, headers = health.run()
    return message, status_code, headers


@app.get("/get-running-job")
def running_kubernetes_job():
    '''
    Gets the running kubernetes jobs within the default namespace
    '''
    running_jobs = get_running_jobs()
    return running_jobs

@app.get("/get-failed-job")
def failed_kubernetes_job():
    '''
    Gets the failed kubernetes jobs within the default namespace
    '''
    failed_jobs = get_failed_jobs()
    return failed_jobs

@app.get("/get-succeeded-job")
def succeeded_kubernetes_job():
    '''
    Gets the succeeded kubernetes jobs within the default namespace
    '''
    succeeded_jobs = get_succeeded_jobs()
    return succeeded_jobs
