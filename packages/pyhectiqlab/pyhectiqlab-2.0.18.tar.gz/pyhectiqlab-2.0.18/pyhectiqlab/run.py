import os
import sys

from pyhectiqlab.metrics import MetricsManager
from pyhectiqlab.settings import app_url
from pyhectiqlab.events_manager import EventsManager
from pyhectiqlab.stream import LogHandler
from pyhectiqlab.buffer import Buffer
from pyhectiqlab.watermark import Watermark
from pyhectiqlab.notebooks import get_notebook_file
from pyhectiqlab.decorators import write_method, action_method

from pyhectiqlab.mlmodels import download_mlmodel as ops_download_mlmodel
from pyhectiqlab.mlmodels import upload_mlmodel as ops_upload_mlmodel
from pyhectiqlab.datasets import download_dataset as ops_download_dataset
from pyhectiqlab.datasets import upload_dataset as ops_upload_dataset
from pyhectiqlab.mlmodels import mlmodel_info_at_path
from pyhectiqlab.datasets import dataset_info_at_path

from functools import partial
from typing import Optional, Union
import tempfile
import logging
import traceback
logger = logging.getLogger("pyhectiqlab")
import shutil

class Run():
    
    def __init__(self, name: str = None, project: str = None, read_only: bool = False, path: str = None):
        """Initiate a new run
        name: Run name. It can contains special caracters.
            A slug version will be used for reference and slug uniqueness in a project is enforced. 
        project: Name of the project to connect to (e.g., `hectiqai/dev`).
        read_only: If True, no data will be pushed to the lab. Use this to prevent from pushing 
                data in the cloud. In a read only mode, the run is an empty shell where most methods
                are unexecuted.
        """
        assert project, "The arugment `project` is required."
        assert name or path, "One of `name` or `path` must be specified."
        self._read_only = read_only
        if self._preflight():
            if path:
                self.run_view = self.events_manager.add_event('fetch_run', args=(path, project), auth=True, async_method=False)
            else:
                self.run_view = self.events_manager.add_event('create_run', args=(name, project), auth=True, async_method=False)
            self._setup_run()

    @classmethod
    def existing(cls, path: str, project: str, read_only: bool = False):
        """Connect to an existing run using the path. The path
        can be found in web application.
        
        Example usage:
        --------------------
        run = Run.existing('first-run', project='hectiqlab/dev')
        """
        cls = cls(path=path, project=project, read_only=read_only)
        return cls

    def _preflight(self):
        """Check if user is logged in. Do the correct setup if read only mode.
        """
        self.events_manager = EventsManager(self._read_only)
        self.events_manager.compare_python_version()
        
        self.log_streams = {}
        self._stream_exception()

        if self._read_only:
            print('Read only mode.')
            self.setup_read_only()
            return False
        
        if self.events_manager.is_logged()==False:
            self.user_is_not_logged()
            return False

        return True

    def _setup_run(self):
        try:
            assert self.run_view.get('status_code')==200, f'An error occured. {str(self.run_view)}'

            if self.run_view.get("is_new", False)==False:
                print(f"Attaching to an existing run (ID :{self.run_view.get('p_id')}).")

            if self.run_view.get('readonly', True):
                print("Warning::Run is read only because you are not the author of the run.")
                self._read_only = True
                self.setup_read_only()
                return 

            if self.run_view.get('slug', None) is None:
                print("An error occured while creating the run. Verify the project is correctly spelled and make sure you have access to the project. Switching to read only mode with an empty run.")
                if self.run_view.get('detail'):
                    print("Error: ", self.run_view.get('detail'))
                self.setup_read_only()
                return
        except:
            logger.debug(traceback.format_exc())
            print("An error occured while creating the run. Verify the project is correctly spelled and make sure you have access to the project. Switching to read only mode with an empty run.")
            if self.run_view.get('detail'):
                print("Error: ", self.run_view.get('detail'))
            else:
                if self.run_view.get("status_code")==400:
                    print("You got an error 400 without any details. The server may be unreachable (check your internet connection). Please report this problem at https://github.com/HectiqAI/lab/discussions")
                else:
                    print(f"Error {self.run_view.get('status_code')} without details. Please report this problem at https://github.com/HectiqAI/lab/discussions")

            self.setup_read_only()
            return 

        self.metrics_manager = MetricsManager(push_method=self._push_metrics)
        self.logs_buffer = Buffer(push_method=self._push_logs)
        self.add_log_stream("pyhectiqlab", level=logging.INFO)

    def user_is_not_logged(self):
        print("User not authentificated. Use `hectiqlab add-profile` in command line.")
        self.setup_read_only()

    def setup_read_only(self):
        self._read_only = True
        self.run_view = {}
        self.events_manager = EventsManager(True)
        self.metrics_manager = None
        self.logs_buffer = None

    @write_method
    @action_method
    def add_artifact(self, filepath: str, name: str = None, step: int = None, wait_response: bool = False):
        """Log a file as an artifacts. If a file already exists with the name, it will be overwritten.

        filepath [str] : Path to the file.
        name [str]: Use this to overwrite the name of the artifact. If None, the basename of the filepath is used.
                    Use this especially if you are using step artifacts and you want to group multiple files
                    with different names.
        step [int]: The optional step stamp of the artifacts.
        wait_response [bool]: Set to true to upload sync. If False, the upload is made in background.
        """
        filename = os.path.basename(filepath)
        num_bytes = os.path.getsize(filepath)
        args = (self._id, self._project_path, filename, filepath, name, num_bytes, step)
        self.events_manager.add_event("add_artifact", args, async_method=bool(1-wait_response))

    @write_method
    @action_method
    def add_mlmodel_usage(self, mlmodel_name: str, version: str = None):
        """Manually log that the run is using a specific model. You don't need
        to use this method if you already use `run.download_mlmodel`.

        mlmodel_name: Name of the mlmodel
        version: Version of the mlmodel. If None, the latest version is used.
        """
        args = (self._id, self._project_path, mlmodel_name, version)
        self.events_manager.add_event("log_mlmodel", args)

    @write_method
    @action_method
    def add_mlmodel_usage_from_dirpath(self, dirpath:str):
        """Manually log that the run is using a specific model, but where 
        the name and the version are extracted from the path of the mlmodel. You don't need
        to use this method if you already use `run.download_mlmodel`.

        dirpath: Path to the mlmodel
        """
        meta = mlmodel_info_at_path(dirpath)
        assert meta is not None, f'Could not find the mlmodel at {dirpath}'

        logger.info(f"Found {meta.get('name')} - {meta.get('version')}")
        args = (self._id, self._project_path, meta.get('name'), meta.get('version'))
        self.events_manager.add_event("log_mlmodel", args)
        return
        
    @write_method
    @action_method        
    def add_mlmodel(self, source_path: str, name: str, version: str = None, description: str = None,
                push_dir: bool = False):
        """Add a mlmodel.

        source_path: Path to the directory/file of the mlmodel
        name: Name of the model without spaces and backslash (e.g., 'text-model')
        version: Version in format '{major}.{minor}.{micro}' (e.g., 1.2.0). If None, 
            the version 1.0.0 is assigned or an increment of minor of the latest version of the
            model with this name (e.g. 1.3.3 -> 1.4.0)
        description: Short description.
        push_dir: Must be set to True if the source_path is a directory
        """
        mlmodel = ops_upload_mlmodel(source_path=source_path, 
            mlmodel_name=name,
             run_id=self._id,
             project_path=self._project_path,
             version=version,
             short_description=description,
             push_dir=push_dir)
        if mlmodel is not None:
            self.add_mlmodel_usage(mlmodel.get('name'), version=mlmodel.get('version'))

    @write_method
    @action_method
    def download_mlmodel(self, mlmodel_name: str, version: str = None, save_path: str = './', overwrite:bool = False):
        """Download an existing mlmodel from the run's project.

        source_path: Path to the directory/file of the mlmodel
        mlmodel_name: Name of the model without spaces and backslash (e.g., 'text-model')
        version: Specific version of the model. If None, the latest version is fetched.
        save_path: Path to where the model is saved.
        overwrite: Set to True to overwrite in save_path.
        """
        dirpath = ops_download_mlmodel(mlmodel_name=mlmodel_name, 
                        project_path=self._project_path, 
                        version=version, 
                        save_path=save_path, 
                        overwrite=overwrite)
        if dirpath is not None:
            self.add_mlmodel_usage_from_dirpath(dirpath)
        return dirpath
        
    @write_method
    @action_method
    def add_dataset(self, source_path: str, name: str, version: str = None, description: str = None,
                push_dir: bool = False, resume_upload: bool = False):
        """Add a dataset.

        source_path: Path to the directory/file of the dataset
        name: Name of the dataset without spaces and backslash (e.g., 'text-dataset')
        version: Version in format '{major}.{minor}.{micro}' (e.g., 1.2.0). If None, 
            the version 1.0.0 is assigned or an increment of minor of the latest version of the
            dataset with this name (e.g. 1.3.3 -> 1.4.0)
        description: Short description.
        push_dir: Must be set to True if the source_path is a directory
        resume_upload: Use resume_upload to resume a failed upload.
        """
        dataset = ops_upload_dataset(source_path=source_path, 
            dataset_name=name,
             run_id=self._id, 
             project_path=self._project_path,
             version=version,
             short_description=description,
             push_dir=push_dir,
             resume_upload=resume_upload)
        if dataset is not None:
            self.add_dataset_usage(dataset.get('name'), version=dataset.get('version'))

    @write_method
    @action_method
    def add_dataset_usage(self, dataset_name: str, version: str = None):
        """Manually log that the run is using a specific dataset You don't need
        to use this method if you already use `run.download_dataset`.
    
        dataset_name: Name of the dataset
        version: Version of the dataset. If None, the latest version is used.

        """
        args = (self._id, self._project_path, dataset_name, version)
        self.events_manager.add_event("log_dataset", args)

    @write_method
    @action_method
    def add_dataset_usage_from_dirpath(self, dirpath:str):
        """Manually log that the run is using a specific dataset. You don't need
        to use this method if you already use `run.download_dataset`.

        dirpath: Path to the mlmodel
        """
        meta = dataset_info_at_path(dirpath)
        assert meta is not None, f'Could not find the dataset at {dirpath}'

        logger.info(f"{meta.get('name')} - {meta.get('version')}")
        args = (self._id, self._project_path, meta.get('name'), meta.get('version'))
        self.events_manager.add_event("log_dataset", args)
        return

    @write_method
    @action_method
    def download_dataset(self, dataset_name: str, version: str = None, save_path: str = './', overwrite:bool = False):
        """Download an existing dataset from the run's project.

        source_path: Path to the directory/file of the dataset
        mlmodel_name: Name of the dataset without spaces and backslash (e.g., 'text-dataset')
        version: Specific version of the dataset. If None, the latest version is fetched.
        save_path: Path to where the dataset is saved.
        overwrite: Set to True to overwrite in save_path.
        """
        dirpath = ops_download_dataset(dataset_name=dataset_name, 
                        project_path=self._project_path, 
                        version=version, 
                        save_path=save_path, 
                        overwrite=overwrite)
        if dirpath is not None:
            self.add_dataset_usage_from_dirpath(dirpath)   
        return dirpath
    
    @write_method
    @action_method
    def add_config(self, config: Union['pyhectiqlab.Config', dict]):
        """
        Add a config object of a dicté
        """
        if isinstance(config, dict):
            args = (self._id, self._project_path, config)
        else:
            args = (self._id, self._project_path, config.dict)
        self.events_manager.add_event("push_config", args)

    @write_method
    @action_method
    def add_tf_model_as_artifact(self, model: 'tf.keras.Model', filename: str, step: int = None):
        """Add a tensorflow model as an artifact.
        """
        save_path = tempfile.mkdtemp()
        model.save_weights(f"{save_path}/{filename}")
        p = tempfile.mkdtemp()
        shutil.make_archive(f"{p}/{filename}", 'zip', save_path)
        self.add_artifact(f"{p}/{filename}.zip", step=step)

    @write_method
    @action_method
    def add_directory_as_zip_artifact(self, dirpath: str, name: str = None, step: int = None, wait_response: bool = False):
        """Compress a full directory and add the compressed file as an artifact.

        name [str]: Use this to overwrite the name of the artifact. If None, the basename of the filepath is used.
                    Use this especially if you are using step artifacts and you want to group multiple files
                    with different names.
        step [int]: The optional step stamp of the artifacts.
        """
        p = tempfile.mkdtemp()
        filename = os.path.basename(dirpath)
        shutil.make_archive(f"{p}/{filename}", 'zip', root_dir=dirpath)
        self.add_artifact(f"{p}/{filename}.zip", name=name, step=step, wait_response=wait_response)

    @write_method
    @action_method
    def set_metrics_aggr(self, aggr: 'str' = "none"):
        """
        Set an aggregation method for the metrics. 

        aggr [str]: The aggregate method. One of ['none', 'sum', 'max', 'mean']  (default is none)
                    If 'none', all metrics are pushed to the lab. Otherwise, only the aggregated value is
                    pushed. If you plan to exceed the maximum rate (1000 metrics/5 seconds), it is best to use an aggregation method.
        """
        assert aggr in ['none', 'sum', 'max', 'mean']
        self.metrics_manager.set_aggr(aggr)

    @write_method
    @action_method
    def add_metrics(self, key: 'str', step: float, value: float):
        """Add a metrics. The metrics is saved even if there already exists a value
        for the same key and step. 

        key [str]: Key used for the metrics. The format with backlash such as `metrics/train`
            will be recognized to organize the metrics.
        value [float]. If tensor, is casted to float.
        step [float]: Step
        """
        self.metrics_manager.add(key, float(value), step)

    @write_method
    @action_method
    def add_tag(self, name: str, color: str = None):
        """Add tag to a run. If the tag does not already exists by this name,
        a new tag is created with the given description and color.
        """
        args = (self._id, self._project_path, name, color)
        self.events_manager.add_event("add_tag", args)

    @write_method
    @action_method
    def add_package_versions(self, packages: Optional[dict] =None, with_sys: bool = True, with_python: bool = True, with_git: bool = True):
        """Save the version of the imported packages.

        Usage:
        add_package_versions(globals())
        """
        water = Watermark()
        versions = {}
        if with_python:
            versions["python"] = water.get_pyversions()
        if with_sys:
            versions["system"] = water.get_sysinfo()
        if packages:
            versions["packages"] = water.get_all_import_versions(packages)
        if with_git:
            git_info = water.get_git_info()
            if git_info:
                versions["git"] = water.get_git_info()

        args = (self._id, self._project_path, versions)
        self.events_manager.add_event("push_package_versions", args)

    @write_method
    @action_method
    def add_package_repo_state(self, package: str = None):
        """Save the branch/commit/origin of the git repo in which
        a package is located.

        Example:
            self.add_package_repo_state('pyhectiqlab')
        """
        water = Watermark()
        result = water.get_repo_info(package)
        data = {package: result}
        args = (self._id, self._project_path, data)
        self.events_manager.add_event("push_git_package_state", args)

    @write_method
    @action_method
    def add_current_notebook(self, name: str = None, stamp: str = 'datetime'):
        """If the run is executed in a jupyter notebook, this
        will add your current notebook as an artifact.
        
        name [str] : Name of the artifact. Optional.
        stamp [str]: Add a stamp on the notebook name.
                    One of 'datetime', 'date', None
        """
        path, fname = get_notebook_file(stamp)
        self.add_artifact(path, name=fname or name)

    @write_method
    @action_method
    def failed(self):
        """Set the run to the failed status.
        """
        args = (self._id, self._project_path, "failed")
        self.events_manager.add_event("set_run_status", args)

    @write_method
    @action_method
    def stopped(self):
        """Set the run to the stopped status.
        """
        args = (self._id, self._project_path, "stopped")
        self.events_manager.add_event("set_run_status", args)
        
    @write_method
    @action_method
    def completed(self):
        """Set the run to the completed with success status.
        """
        args = (self._id, self._project_path, "completed")
        self.events_manager.add_event("set_run_status", args)
        
    @write_method
    @action_method
    def pending(self):
        """Set the run to the pending status.
        """
        args = (self._id, self._project_path, "pending")
        self.events_manager.add_event("set_run_status", args)
        
    @write_method
    @action_method
    def running(self):
        """Set the run to the running status.
        """
        args = (self._id, self._project_path, "running")
        self.events_manager.add_event("set_run_status", args)
        
    @write_method
    @action_method
    def training(self):
        """Set the run to the training status.
        """
        args = (self._id, self._project_path, "training")
        self.events_manager.add_event("set_run_status", args)
        
    @write_method
    @action_method
    def add_meta(self, key, value):
        """Add or update a meta information in the format of
        key/value.
        """ 
        args = (self._id, self._project_path, key, value)
        self.events_manager.add_event("push_meta", args)
        
    @write_method
    @action_method
    def set_note(self, text: str):
        """Add or update a custom note field for the run.
        """
        args = (self._id, self._project_path, text)
        self.events_manager.add_event("set_note", args)
    
    @write_method
    @action_method
    def set_paper(self, content: str):
        """Overwrite the content of the paper of the run.
        """
        args = (self._id, self._project_path, content)
        self.events_manager.add_event("set_paper", args)

    @write_method
    @action_method
    def clear_logs(self):
        """Clear the entire saved logs.
        """
        args = (self._id, self._project_path)
        self.events_manager.add_event("clear_logs", args)

    def _stream_exception(self):
        """
        Handle the exception with `sys.excepthook`.
        """
        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                self.stopped()
            else:
                self.add_tag(name="failed")
                self.failed()
            l = self.add_log_stream("pyhectiqlab", level=logging.ERROR)
            l.critical("Automatic exception handler", exc_info=(exc_type, exc_value, exc_traceback))

            # Flush cache before leaving
            self.logs_buffer.flush_cache()
            self.metrics_manager.flush_cache()
            sys.exit(0)                
            
        sys.excepthook = handle_exception
        return 

    def add_log_stream(self, logger_name: Optional[str] = None, 
                        format: Optional[Union[str, "logging.Formatter"]] = "%(asctime)s - %(levelname)s - %(message)s", 
                        level: Optional[int] = 30):
        """Start tailing the logs on a logger name.
        If logger_name is None, the default __name__ will be taken and
        you may use the returned logger.
        """
        if self.dry_mode or self.read_only:
            logger.error(f"A logger named {logger_name} is returned but the logs aren't saved because you are in a read-only mode.")
            return logging.getLogger(logger_name)
        
        if (logger_name is None or logger_name=="pyhectiqlab")and level<10:
            logger.error(f"Cannot assign a level {level} (<10) on root logger. Use a `logger_name` to specify a different stream. Level is switch to 10.")
            level = 10

        # Start recording
        self.logs_buffer.start(key=logger_name)

        if logger_name not in self.log_streams:
            # Add log
            func = partial(self.logs_buffer.add, key=logger_name)
            log_recorder = LogHandler(func)
            log_recorder.set_name("hectiqlab")
            log_recorder.set_name("hectiqlab")
            log_recorder.setLevel(level)
            console = logging.StreamHandler()
            console.setLevel(level)
            log = logging.getLogger(logger_name)
            log.setLevel(level)
            log.addHandler(log_recorder)
            if isinstance(format, str):
                formatter = logging.Formatter(format)
            else:
                formatter = format
            log_recorder.setFormatter(formatter)
            self.log_streams[logger_name] = log

        return self.log_streams[logger_name]

    def remove_log_stream(self, logger_name: Optional[str] = None):
        """Stop recording a certain log stream.
        """
        self.logs_buffer.stop(key=logger_name)
        if logger_name in self.log_streams:
            log = self.log_streams[logger_name]
            for handler in log.handlers:
                if handler.get_name()=="hectiqlab":
                    log.removeHandler(handler)

        self.log_streams.pop(logger_name, None)

    @write_method
    @action_method
    def _push_logs(self, key, msg):
        args = (self._id, self._project_path, "".join(msg))
        self.events_manager.add_event("append_logs", args)
        
    @write_method
    @action_method
    def _push_metrics(self, key, values):
        if len(values)>0:
            args = (self._id, self._project_path, key, values)
            self.events_manager.add_event("push_metrics", args)

    @property
    def _id(self):
        return self.run_view.get('slug')

    @property
    def _project_path(self):
        return self.run_view.get('project', {}).get('path', '')

    @property
    def read_only(self):
        return self._read_only

    @property
    def dry_mode(self):
        return self._read_only

    @property
    def action_mode(self):
        if self.dry_mode:
            return 'dry'
        if self.read_only:
            return 'read-only'
        return 'read-write'
    
    @property
    def author(self):
        author = self.run_view.get('author')
        if author is None:
            return 'Undefined'
        return author.get('firstname') + ' ' + author.get('lastname')
        
    def __str__(self):
        pad = 8
        project = self.run_view.get('project', {})
        path = f"/{project.get('path')}/runs/{self.run_view.get('slug')}"
        return f"<Run {self.run_view.get('p_id')} {self.run_view.get('slug')}>"\
                f"\n{'Name'.ljust(pad)}: {self.run_view.get('name')}"\
                f"\n{'Project'.ljust(pad)}: {project.get('name')} ({project.get('path')})"\
                f"\n{'author'.ljust(pad)}: {self.author}"\
                f"\n{'mode'.ljust(pad)}: {self.action_mode}"\
                f"\n{'url'.ljust(pad)}: {app_url+path} "

    def __repr__(self):
        return self.__str__()
    