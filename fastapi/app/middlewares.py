from fastapi import Request
import time, uuid
from .logger import logger
    
async def log_requests(request: Request, call_next):
    '''
    Logs the amount of time it takes for a request and return to complete via http
    Created from https://philstories.medium.com/fastapi-logging-f6237b84ea64
    '''
    idem = str(uuid.uuid1().hex)
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
    
    return response