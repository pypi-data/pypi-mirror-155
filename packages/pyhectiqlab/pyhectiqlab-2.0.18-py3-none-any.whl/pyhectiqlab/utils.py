import os
import logging
import ast
import requests
from tqdm import tqdm

from pyhectiqlab.config import Config
from pyhectiqlab.events_manager import EventsManager

logger = logging.getLogger('pyhectiqlab')

def load_event_manager():
    events_manager = EventsManager()
    assert events_manager.is_logged(), "User not authentificated"
    return events_manager

def download_existing_run_artifact(artifact_uuid: str, savepath: str = "./"):
    events_manager = load_event_manager()
    data = events_manager.add_event('get_artifact_signed_url', 
                                    (artifact_uuid, ), 
                                    auth=True, async_method=False)
    if 'detail' in data:
        logger.error(data['detail'])
        return

    if 'url' not in data:
        logger.error('The answer is unexpected.')
        return

    url = data['url']
    artifact_name = data['name']
    response = requests.get(url, stream=True)
    total_size_in_bytes= int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    
    path = os.path.join(savepath, artifact_name)
    with open(path, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        logger.error("ERROR, something went wrong when downloading the file.")
    
    logger.info(f'Content saved at {path}')
    return path

def download_run_artifact(artifact_uuid: str, savepath: str = "./"):
    return download_existing_run_artifact(artifact_uuid=artifact_uuid, savepath=savepath)
    
def convert_custom_fields_to_config(data: dict):
    """Convert a dict representation of a config file
    into a Config object.

    data [dict]: Dict representation of a config

    Returns:
        config [Config]
    """
    config = Config()
    
    if data is None:
        return config
    
    c = config
    for key in data:
        keys = key.split("/")
        for i,k in enumerate(keys):
            if i==0:
                continue
            if i<len(keys)-1:
                if k not in c.dict:
                    setattr(c, k, Config())
                c = getattr(c, k)
            else:
                d = data[key]
                try:
                    d = ast.literal_eval(d)
                except:
                    True
                setattr(c, k, d)
        c = config
    return config

def list_all_files_in_dir(local_folder: str):
    filenames = []
    for el in os.walk(local_folder):
        for f in os.listdir(el[0]):
            complete_path = os.path.join(el[0], f)
            if os.path.isdir(complete_path)==False:
                if os.path.isfile(complete_path):
                    filenames.append(complete_path)
    return filenames