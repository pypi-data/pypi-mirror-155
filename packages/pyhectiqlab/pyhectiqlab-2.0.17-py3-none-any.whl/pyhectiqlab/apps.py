import os
from pyhectiqlab.utils import load_event_manager

import requests
from tqdm import tqdm
import logging
import json
import datetime as dt

logger = logging.getLogger('pyhectiqlab')

use_tqdm = os.getenv("HECTIQLAB_NO_TQDM", "0")!="1"

def app_info_at_path(dirpath: str):
    try:
        with open(os.path.join(dirpath, '.hlab_meta.json'), "r") as f:
            data = json.load(f)
        return data
    except:
        return None

def download_app(app_name: str,
                 project_path: str, 
                 save_path: str = './', 
                 overwrite: bool = False,
                 no_dir: bool = False):
    assert app_name, project_path
    manager = load_event_manager()
    if no_dir==False:
        dirpath = os.path.join(save_path, app_name)
        if os.path.isdir(dirpath) and overwrite==False:
            logger.warning(f'App is already downloaded at {dirpath}. Delete this folder or set overwrite==True to download again.')
            return dirpath
    else:
        dirpath = save_path

    if os.path.isdir(dirpath)==False:
        os.makedirs(dirpath)

    page = 1
    def fetch_download_urls(page: int):
        # Fetch the download files
        res = manager.add_event('get_app_download_info', 
                    args=(app_name, project_path, page), 
                    async_method=False)
        assert res.get('status_code')==200, res.get('detail')
        return res 

    res = fetch_download_urls(page)

    # Save the meta
    meta = res.get('meta')
    text = f"{meta.get('name')}\nProject: {project_path}\n"
    text += f"UUID: {meta.get('uuid')}\nDescription: {meta.get('short_description')}\n"
    text += f"Downloaded on: {dt.datetime.now()}"
    text += '\n--------------------------\n'

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
            content_downloaded = 0
            if use_tqdm:
                progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

            path = os.path.join(dirpath, name)
            with open(path, 'wb') as file:
                for data in response.iter_content(block_size):
                    content_downloaded += len(data)
                    if use_tqdm:
                        progress_bar.update(len(data))
                    file.write(data)
            if use_tqdm:
                progress_bar.close()

            if total_size_in_bytes != 0 and content_downloaded != total_size_in_bytes:
                logger.error(f"Something went wrong when downloading the file {path}.")
            logger.info(f'Content saved at {path}')

        # Next page
        page += 1
        res = fetch_download_urls(page)

    return dirpath


