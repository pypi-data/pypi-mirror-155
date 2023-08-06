import requests
import json
import pyhectiqlab.settings as settings
import logging
from typing import List
from more_itertools import chunked

from pyhectiqlab.upload import upload_file

logger = logging.getLogger('pyhectiqlab')

def lab_request(path, request_type, form_data=None, query_args=None, body_args=None, token=None):

    if path.startswith('http://') or path.startswith('https://'):
        url = path
    else:
        url = settings.server_url + path
    if query_args:
        url += "?"
        for key, val in query_args.items():
            if val is not None:
                url += f"{key}={val}&"

    headers = {}
    if token:
        headers = {"X-API-Key": f"{token}"}
    body = None
    if body_args:
        body = json.dumps(body_args)
    files = None
    if form_data:
        body = form_data
        headers["content-type"] = 'application/x-www-form-urlencoded'
    if request_type=="GET":
        call = requests.get
    elif request_type=="PUT":
        call = requests.put
    elif request_type=="POST":
        call = requests.post
    try:
        res = call(url, data=body, headers=headers, files=files)
        logger.debug(url)
        logger.debug(res.status_code)
        logger.debug(body)

        if res.status_code==401:
            logger.debug(res.json()["detail"])
            return {"status_code": 401, "detail": res.json().get("detail")}
        else:
            data = res.json()
            logger.debug(res.json())
            if isinstance(data, list):
                data = {"result": data}
            data["status_code"] = res.status_code
            return data
    except:
        logger.debug(f"Error on call {url}")
        return {"status_code": 400}


def fetch_secret_api_token(username, password):
    res = lab_request(path="/app/auth/generate_secret_api_token", 
                request_type="POST", 
                form_data=dict(username=username, password=password))
    return res

def update_secret_api_token_name(api_key_uuid, name, token):
    res = lab_request(path=f"/app/auth/api-key/{api_key_uuid}", 
                request_type="PUT", 
                token=token,
                body_args=dict(name=name))
    return res

def fetch_minimum_python_version():
    res = lab_request(path="/minimum-supported-python-version", 
                request_type="GET")
    return res

def get_artifact_signed_url(artifact_uuid, token):
    res = lab_request(path=f"/app/artifacts/{artifact_uuid}/url", 
                request_type="GET", 
                token=token)
    return res

def create_run(name, project_path, token):
    res = lab_request(path=f"/{project_path}/runs", 
                request_type="POST", 
                token=token,
                body_args=dict(name=name))
    return res

def fetch_run(path, project_path, token):
    res = lab_request(path=f"/{project_path}/runs/{path}", 
                request_type="GET", 
                token=token)
    return res

def fetch_run_packages(path, project_path, token):
    res = lab_request(path=f"/{project_path}/runs/{path}/packages", 
                request_type="GET", 
                token=token)
    return res

def fetch_run_logs(path, project_path, token):
    res = lab_request(path=f"/{project_path}/runs/{path}/logs", 
                request_type="GET", 
                token=token)
    return res

def clear_logs(path, project_path, token):
    res = lab_request(path=f"/{project_path}/runs/{path}/clear-logs", 
                request_type="POST", 
                token=token)
    return res

def fetch_run_configs(path, project_path, token):
    res = lab_request(path=f"/{project_path}/runs/{path}/configs", 
                request_type="GET", 
                token=token)
    return res

def push_metrics(run_path, project_path, metrics_name, values, token):
    res = lab_request(path=f"/{project_path}/runs/{run_path}/metrics",
                     request_type="POST",
                     token=token,
                     body_args=dict(name=metrics_name, values=values))
    return res

def set_run_status(run_path, project_path, status, token):
    res = lab_request(path=f"/{project_path}/runs/{run_path}/status",
                     request_type="POST",
                     token=token,
                     body_args=dict(status=status))
    return res

def push_meta(run_path, project_path, key, value, token):
    res = lab_request(path=f"/{project_path}/runs/{run_path}/meta",
                     request_type="POST",
                     token=token,
                     body_args=dict(meta={"__meta__": {key:value}}))
    return res

def push_config(run_path, project_path, content, token):
    res = lab_request(path=f"/{project_path}/runs/{run_path}/meta",
                     request_type="POST",
                     token=token,
                     body_args=dict(meta={"__config__": content}))
    return res

def push_package_versions(run_path, project_path, data, token):
    res = lab_request(path=f"/{project_path}/runs/{run_path}/packages",
                     request_type="POST",
                     token=token,
                     body_args=dict(packages=data))
    return res

def push_git_package_state(run_path, project_path, data, token):
    res = lab_request(path=f"/{project_path}/runs/{run_path}/git_package_meta",
                     request_type="POST",
                     token=token,
                     body_args=dict(gitmeta=data))
    return res

def set_note(run_path, project_path, note, token):
    res = lab_request(path=f"/{project_path}/runs/{run_path}/note",
                     request_type="POST",
                     token=token,
                     body_args=dict(text=note))
    return res

def set_paper(run_path, project_path, content, token):
    res = lab_request(path=f"/{project_path}/runs/{run_path}/paper",
                     request_type="POST",
                     token=token,
                     body_args=dict(source=content))
    return res

def add_tag(run_path, project_path, name, color, token):
    res = lab_request(path=f"/{project_path}/runs/{run_path}/tags",
                     request_type="POST",
                     token=token,
                     body_args=dict(tag_name=name, tag_color=color, can_remove=False))
    return res

def log_mlmodel(run_path, project_path, mlmodel_name, version, token):
    res = lab_request(path=f"/{project_path}/runs/{run_path}/log_mlmodel",
                     request_type="POST",
                     token=token,
                     query_args=dict(mlmodel_name=mlmodel_name, version=version))
    return res

def log_dataset(run_path, project_path, dataset_name, version, token):
    res = lab_request(path=f"/{project_path}/runs/{run_path}/log_dataset",
                     request_type="POST",
                     token=token,
                     query_args=dict(dataset_name=dataset_name, version=version))
    return res

def append_logs(run_path, project_path, logs, token):
    if logs is None:
        return
    res = lab_request(path=f"/{project_path}/runs/{run_path}/logs",
                     request_type="POST",
                     token=token,
                     body_args=dict(logs=logs))
    return res

def add_artifact(run_path, project_path, filename: str, filepath: str, name: str = None, num_bytes: int = None, step: int = None, token: str = None):

    # Get policy
    args = dict(filename=filename)
    if name is not None:
        args['name'] = name
    else:
        args['name'] = filename
    if step is not None:
        args['step'] = step
    if num_bytes:
        args["num_bytes"] = num_bytes

    res = lab_request(path=f"/{project_path}/runs/{run_path}/artifacts",
                     request_type="POST",
                     token=token,
                     query_args=args)
    try:
        logger.debug('ops.add_artifacts:: Upload starting.')

        upload_file(filepath, res)
        logger.debug('ops.add_artifacts:: Upload completed.')
        return res
    except:
        # Unable
        logger.error(f'Unable to push artifact {filepath}.')
        return res

def get_mlmodel_download_info(mlmodel_name, project_path, version, page, token):
    res = lab_request(path=f"/{project_path}/mlmodels/{mlmodel_name}/download",
                     request_type="GET",
                     token=token,
                     query_args=dict(version=version, page=page))
    return res

def get_dataset_download_info(dataset_name, project_path, version, page, token):
    res = lab_request(path=f"/{project_path}/datasets/{dataset_name}/download",
                     request_type="GET",
                     token=token,
                     query_args=dict(version=version, page=page))
    return res

def get_app_download_info(app_name, project_path, page, token):
    res = lab_request(path=f"/{project_path}/apps/{app_name}/download",
                     request_type="GET",
                     token=token,
                     query_args=dict(page=page))
    return res

def add_mlmodel(run_path, 
                project_path,
                filenames: List[str], 
                full_paths: List[str], 
                num_bytes: List[int], 
                name: str, 
                short_description: str, 
                version: str, 
                token: str = None):

    # Create mlmodel
    body = dict(run_path=run_path, 
            name=name, 
            filenames=[], 
            short_description=short_description, 
            num_bytes=[], 
            version=version)
    res = lab_request(path=f"/{project_path}/mlmodels",
                         request_type="POST",
                         token=token,
                         body_args=body)
    assert res.get('status_code') == 200, f"An error occured while creating the mlmodel: {res.get('detail')}"
    mlmodel = res.get('mlmodel')
    logger.info(f"Creating mlmodel {mlmodel.get('name')}, version {mlmodel.get('version')}.")
    mlmodel_uuid = mlmodel.get('uuid')
    batch_size = 20 # Number of elements to send
    for batch in chunked(zip(filenames, full_paths, num_bytes), batch_size):
        batch_filenames = list(zip(*batch))[0]
        batch_num_bytes = list(zip(*batch))[2]

        # Get policy
        body = dict(filenames=batch_filenames, num_bytes=batch_num_bytes)

        res = lab_request(path=f"/app/mlmodels/{mlmodel_uuid}/add-files",
                         request_type="POST",
                         token=token,
                         body_args=body)
        assert res.get('status_code') == 200, f"An error occured while pushing new files: {res.get('detail')}"

        for filename, policy in res['policies'].items():
            logger.info(f'Uploading {filename}')
            if filename is None:
                continue

            upload_file(full_paths[filename], policy)
    return mlmodel

def add_dataset(run_path, 
                project_path,
                filenames: List[str], 
                full_paths: List[str], 
                num_bytes: List[int], 
                name: str, 
                short_description: str, 
                version: str, 
                resume_upload: bool,
                token: str = None):

    # Create dataset
    body = dict(run_path=run_path, 
            name=name, 
            filenames=[], 
            short_description=short_description, 
            num_bytes=[], 
            resume_upload=resume_upload,
            version=version)
    res = lab_request(path=f"/{project_path}/datasets",
                         request_type="POST",
                         token=token,
                         body_args=body)
    assert res.get('status_code') == 200, f"An error occured while creating the dataset: {res.get('detail')}"
    dataset = res.get('dataset')
    logger.info(f"Creating dataset {dataset.get('name')}, version {dataset.get('version')}.")
    dataset_uuid = dataset.get('uuid')
    batch_size = 20 # Number of elements to send
    for batch in chunked(zip(filenames, full_paths, num_bytes), batch_size):
        batch_filenames = list(zip(*batch))[0]
        batch_num_bytes = list(zip(*batch))[2]

        # Get policy
        body = dict(filenames=batch_filenames, num_bytes=batch_num_bytes, resume_upload=resume_upload)

        res = lab_request(path=f"/app/datasets/{dataset_uuid}/add-files",
                         request_type="POST",
                         token=token,
                         body_args=body)
        assert res.get('status_code') == 200, f"An error occured while pushing new files: {res.get('detail')}"

        for filename, policy in res['policies'].items():
            logger.info(f'Uploading {filename}')
            if filename is None:
                continue
            upload_file(full_paths[filename], policy)
    return dataset

def get_all_projects(token):
    res = lab_request(path="/app/user/projects",
                     request_type="GET",
                     token=token)
    return res