from typing import List

import aiofiles, requests
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import parse_obj_as

from config import get_s3_client


async def upload_to_s3(file_name):
    '''
        This function is use to upload the file to S3 and then return the URL.
    '''
    bucket = get_s3_client()

    # Create new key
    k = bucket.new_key('/bill_analysis/' + file_name)

    # Upload the file
    k.set_contents_from_filename('/tmp/' + file_name)

    # Get URL
    url = k.generate_url(expires_in=0, query_auth=False)

    return url


async def upload_to_tmp(uploaded_file, file_name, to_s3 = False):
    # Save the file in tmp folder
    resp = {}

    try:
        async with aiofiles.open(f'/tmp/{file_name}', 'wb') as f:
            content = await uploaded_file.read()  # async read
            await f.write(content)  # async write
    except Exception as e:
        resp['status'] = False
    
    if to_s3:
        url = await upload_to_s3(file_name)
        resp['status'] = True
        resp['url'] = url
    else:
        resp['status'] = False
    
    return resp


def resp_fun(self, msg, alert_type, lod_link=''):
    '''
        This function is used to create the response message
    '''
    if alert_type == 'success':
        title = 'Success'
    else:
        title = 'Please notice !'
    
    if lod_link:
        resp = {'title': title, 'msg': msg, 'lod_link': lod_link, 'alert_type': alert_type}
    else:
        resp = {'title': title, 'msg': msg, 'alert_type': alert_type}

    return resp


def resp_format(data, status, schema=''):
    response_data = {
        'data': {
            'result': {},
            'error': {}
        },
        'responseDetail': '',
        'responseCode': ''
    }

    if schema:
        if type(data) == list:
            if len(data) > 0:
                resp_data = parse_obj_as(List[schema], data)
            else:
                resp_data = []
        else:
            resp_data = parse_obj_as(schema, data)
    else:
        resp_data = data
    
    response_data['data']['result'] = jsonable_encoder(resp_data)
    response_data['data']['error'] = ''
    response_data['responseDetail'] = ''
    response_data['responseCode'] = status

    return JSONResponse(response_data, status_code=status)

def get_hes_client_after_signing_in(username, password, use_prod_url=True):
    if use_prod_url:
        url = 'https://data.grampower.com/hes/'
    else:
        url = 'https://staging.grampower.com/hes/'

    request_client = requests.session()
    response = request_client.post(
        url,
        data={
            'username': username,
            'password': password
        }, verify=False
    )
    headers = {
        'X-CSRFToken': response.cookies['csrftoken'],
        'Referer': url
    }

    return request_client, headers