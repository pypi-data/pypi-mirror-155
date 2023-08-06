import os
from pyhectiqlab.utils import list_all_files_in_dir, load_event_manager

import requests
from tqdm import tqdm
import logging
import json
import datetime as dt
import packaging.version as pack_version
from slugify import slugify

logger = logging.getLogger('pyhectiqlab')

def mlmodel_info_at_path(dirpath: str):
    try:
        with open(os.path.join(dirpath, '.hlab_meta.json'), "r") as f:
            data = json.load(f)
        return data
    except:
        return None

def upload_mlmodel(source_path: str, mlmodel_name: str, project_path: str, run_id: str = None, version: str = None,
    short_description: str = None, push_dir:bool = False):

    slug_mlmodel_name = slugify(mlmodel_name)
    assert slug_mlmodel_name==mlmodel_name, f"The name is not slugified. Please use {slug_mlmodel_name} instead."


    manager = load_event_manager()

    if version is not None:
        v = pack_version.parse(version)
        assert isinstance(v, pack_version.Version), 'Cannot use legacy version names. Use a format major.minor.micro.'
        updated_version = f'{v.major}.{v.minor}.{v.micro}'
        assert updated_version==version, f'Please change version to {updated_version}.'

    if os.path.isdir(source_path):
        logger.info('Model is a directory. Listing all files...')
        paths = list_all_files_in_dir(source_path)
        filenames = [os.path.relpath(p, start=source_path) for p in paths]
        num_bytes = [os.path.getsize(p) for p in paths]
        full_paths = {f: os.path.abspath(p) for f,p in zip(filenames, paths)}
        logger.info(f'Found {len(filenames)} files')

        assert push_dir, 'Set push_dir=True to push a model directory.'

    else:
        filenames = [os.path.basename(source_path)]
        full_paths = {os.path.basename(source_path): os.path.abspath(source_path) }
        num_bytes = [os.path.getsize(source_path)]
    args = (run_id, project_path, filenames, full_paths, num_bytes, mlmodel_name, short_description, version)
    return manager.add_event("add_mlmodel", args, async_method=False)

def download_mlmodel(mlmodel_name: str,
                     project_path: str, 
                     version: str = None, 
                     save_path: str = './', 
                     overwrite: bool = False):
    assert project_path
    manager = load_event_manager()

    if version is not None:
        dirpath = os.path.join(save_path, mlmodel_name+'-'+version)
        if os.path.isdir(dirpath) and overwrite==False:
            logger.warning(f'Dataset is already downloaded at {dirpath}. Delete this folder or set overwrite==True to download again.')
            return dirpath

    page = 1
    # Fetch the download files
    res = manager.add_event('get_mlmodel_download_info', 
                args=(mlmodel_name, project_path, version, page), 
                async_method=False)
    assert res.get('status_code')==200, res.get('detail')
    version = res.get('meta').get('version')
    dirpath = os.path.join(save_path, mlmodel_name+'-'+version)
    logger.info(f'Fetching version {version}')

    if os.path.isdir(dirpath) and overwrite==False:
        logger.warning(f'Dataset is already downloaded at {dirpath}. Delete this folder or set overwrite==True to download again.')
        return dirpath

    if os.path.isdir(dirpath)==False:
        os.makedirs(dirpath)

    # Save the meta
    meta = res.get('meta')
    text = f"{meta.get('name')}\nVersion: {meta.get('version')}\nProject: {project_path}\n"
    text += f"UUID: {meta.get('uuid')}\nDescription: {meta.get('description')}\n"
    text += f"Downloaded on: {dt.datetime.now()}"
    text += '\n--------------------------\n'
    if meta.get('full_description'):
        text += meta.get('full_description')
    else:
        text += 'No description.'
    with open(os.path.join(dirpath, 'HLab_README.md'), "w") as f:
        f.write(text)

    with open(os.path.join(dirpath, '.hlab_meta.json'), "w") as f:
        json.dump(meta, f)

    while True: 

        files = res.get('results', [])

        if len(files)==0:
            logger.info("Download completed.")
            return dirpath

        logger.info(f'Downloading {len(files)} files')
        for file_meta in files:
            url = file_meta['url']
            name = file_meta['name']
            if os.path.dirname(name)!='':
                subdirpath = os.path.join(dirpath, os.path.dirname(name))
                if os.path.isdir(subdirpath) == False:
                    os.makedirs(subdirpath)
            logger.info(name)
            response = requests.get(url, stream=True)
            total_size_in_bytes= int(response.headers.get('content-length', 0))
            block_size = 1024
            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

            path = os.path.join(dirpath, name)
            with open(path, 'wb') as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)
            progress_bar.close()
            if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                logger.error(f"Oups, something went wrong while downloading the file {path}.")
            logger.info(f'Content saved at {path}')

        # Fetch the download files
        page += 1
        res = manager.add_event('get_mlmodel_download_info', 
                    args=(mlmodel_name, project_path, version, page), 
                    async_method=False)
        assert res.get('status_code')==200, res.get('detail')

    return dirpath