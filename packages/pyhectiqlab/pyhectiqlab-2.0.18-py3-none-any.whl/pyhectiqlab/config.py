import json
from pyhectiqlab.events_manager import EventsManager

class Config():
    """
    A pyhectiqlab.Config object is an abstract object designed to store 
    your configurations with a simple API.
    
    """
    def __init__(self, **kwargs):
        self._state = {}
        self._lock = False

        for key in kwargs:
            if key=="dict":
                raise KeyError("Key dict is a protected attribute.")
            if key=="keys":
                raise KeyError("Key keys is a protected attribute.")
            setattr(self, key, kwargs[key])

    def save(self, path):
        json.dump(self.dict, open(path, "w"))
    
    @classmethod
    def load(cls, path):
        return cls.from_dict(json.load(open(path, "r")))
    
    @staticmethod
    def download(run: str, project: str):
        """
        Download configuration from a run.

        run: Slug path to the run.
        project: Name of the project.
        """
        events_manager = EventsManager()
        result = events_manager.add_event("fetch_run_configs", (run, project), async_method=False)
        return Config._convert_json_res(result)

    def lock(self):
        """Freeze the state of the config.
        """
        self._lock = True

    def unlock(self):
        """Unfreeze the state of the config.
        """
        self._lock = False
    
    @staticmethod
    def from_dict(data):
        """Convert a dict to a Config object.
        `data` can be nested (dict within dict), which will generate sub configs.
        If `data` is not a dict, then the method returns `data`.

        Example:
        -------------
        d = {"a": {"b": 4}}
        config = Config.from_dict(d)
        assert config.a.b == 4
        """
        if isinstance(data, dict)==False:
            return data
        config = Config()
        for key in data:
            if isinstance(data[key], dict):
                config[key] = Config.from_dict(data[key])
            else:
                config[key] = data[key]
        return config

    @staticmethod
    def _convert_json_res(res: dict):
        """Convert the download config, meta into a Config.
        """
        meta = {}
        config = Config()
        
        if res is None:
            return Config(), {}
        
        for key, item in res.get("__meta__", {}).items():
            meta[key] = item

        config = Config.from_dict(res.get("__config__", {}))
        return config, meta

    @property
    def dict(self):
        """A property that converts a config to a dict. Supports nested Config.
        """
        d = {}
        for key, item in self._state.items():
            if isinstance(item, Config):
                d[key] = item.dict
            else:
                d[key] = item
        return d
    
    def keys(self):
        """List the config attributes.
        """
        return self._state.keys()

    def __contains__(self, key):
        return key in self._state

    def __getattr__(self, name):
        return self._state.get(name, None)

    def __setattr__(self, name, value):
        if name in ["_state", "_lock"]:
            object.__setattr__(self, name, value)
        else:
            if self._lock:
                raise Exception("Config is locked.")
            self._state[name] = value
            
    def __getstate__(self): 
        return self._state

    def __setstate__(self, d): 
        if self._lock == False:
            self._state.update(d)
        else:
            raise Exception("Config is locked.")
    
    def __getitem__(self, key):
        if key in self._state:
            return self._state[key]
        return None

    def __setitem__(self, key, value):
        if self._lock == False:
            self._state[key] = value
        else:
            raise Exception("Config is locked.")

    def __iter__(self):
        return self._state.__iter__()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return json.dumps(self.dict, indent=2)