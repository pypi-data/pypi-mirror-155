"""Mediator configuration management."""
from getpass import getpass
from importlib import import_module
import numpy as np
import oyaml as yaml
from pathlib import Path
import typing as tp
import e4clim
from e4clim import typing as e4tp
from .utils.tools import ensure_collection


def input_expand_user(fun: tp.Callable[[str], str]) -> tp.Callable[[str], Path]:
    """Decorator of :py:func:`input` to manage `'~'` in filepath."""
    def decorated_fun(prompt: str) -> Path:
        q = fun(prompt)
        return Path(q).expanduser()

    return decorated_fun


# Decorate open to manage ~ in paths with decorator_expand_user
input_path = input_expand_user(input)


class Config(tp.MutableMapping):
    """Configuration class."""

    #: Actual configuration.
    _cfg: e4tp.CfgType

    def __init__(self, cfg: tp.Union[e4tp.CfgType, str, Path] = None,
                 ask_for_cfg_filepath: bool = False) -> None:
        """Build configuration.

        :param cfg: Filepath of (pre-)configuration file.
        :param ask_for_cfg_filepath: Whether to ask for configuration-file
          path if :py:obj:`cfg` is `None`.
        """
        if isinstance(cfg, Config):
            # Copy constructor
            self._cfg = cfg._cfg
        elif isinstance(cfg, tp.MutableMapping):
            self._cfg = cfg
        elif isinstance(cfg, Path):
            self._cfg = _read_configuration(cfg)
        elif cfg is None and ask_for_cfg_filepath:
            cfg_filepath = None
            while not (isinstance(cfg_filepath, str) or
                       isinstance(cfg_filepath, Path) or
                       isinstance(cfg, list)):
                cfg_filepath = input_path(
                    'Application configuration filepath: ')

            self._cfg = _read_configuration(cfg_filepath)
        else:
            self._cfg = None

    @property
    def cfg(self) -> e4tp.CfgType:
        return self._cfg

    @cfg.setter
    def cfg(self, cfg: e4tp.CfgType) -> None:
        self._cfg = cfg

    def get_credentials(
            self, name: str, keys: tp.Iterable = ['user', 'passwd']) -> dict:
        """Get credentials given by :py:obj:`keys` argument
        for a container named :py:obj:`name` from file, or ask them.

        :param name: Name.
        :param keys: Name of asked credentials.

        :returns: Credential key-value pairs.
        """
        keys_filepath = Path(*ensure_collection(
            self.cfg['cfg_path']['keys'], list))

        cred, cfg_keys = _get_credentials_from_file(keys_filepath, name)

        cred, any_new = _get_pass_if_needed(keys, cred, name)

        _save_new_credentials_if_needed(any_new, keys_filepath, cfg_keys)

        # Return only asked key-value pairs
        return {k: cred.get(k) for k in keys}

    def get_data_root_directory(self, **kwargs) -> Path:
        """Get data root directory from mediator configuration.

        :returns: Data root-directory.
        """
        directory = self.get('data_dir')
        directory = (Path('data') if directory is None else
                     Path(*ensure_collection(directory, list)))

        return directory

    def get_project_data_directory(
            self, container: 'e4clim.container.base.ContainerBase' = None,
            makedirs: bool = True, subdirs: e4tp.StrIterableType = None,
            **kwargs) -> Path:
        """Get project data directory and create it if needed.

        :param container: Container for which to get data directory.
        :param makedirs: Make directories if needed.
        :param subdirs: List of additional subdirectories.

        :returns: Directory path.
        """
        subdirs = ensure_collection(subdirs, list)
        base_subdir = Path(self['project_name'])
        base_dir = Path(self.get_data_root_directory(**kwargs), base_subdir)
        if container:
            user_project_dir = container.med.cfg.get('project_dir')
            directory = (
                Path(base_dir, container.name) if user_project_dir is None else
                Path(*ensure_collection(user_project_dir, list)))
        else:
            directory = base_dir
        if subdirs is not None:
            directory = Path(directory, *subdirs)

        if makedirs:
            # Create directory if needed
            Path.mkdir(directory, parents=True, exist_ok=True)

        return directory

    def get_external_data_directory(
            self, container: 'e4clim.container.base.ContainerBase' = None,
            makedirs: bool = True, subdirs: e4tp.StrIterableType = None,
            **kwargs) -> Path:
        """Get external data directory and create it if needed.

        :param container: Data source for which to get data directory.
        :param makedirs: Make directories if needed.
        :param subdirs: List of additional subdirectories.

        :returns: Directory path.
        """
        subdirs = ensure_collection(subdirs, list)
        base_subdir = Path('extern')
        base_dir = Path(self.get_data_root_directory(**kwargs), base_subdir)
        if container:
            user_data_dir = container.cfg.get('data_dir')
            directory = (
                Path(base_dir, container.name) if user_data_dir is None else
                Path(*ensure_collection(user_data_dir, list)))
        else:
            directory = base_dir
        if subdirs is not None:
            directory = Path(directory, *subdirs)

        if makedirs:
            # Create directory if needed
            Path.mkdir(directory, parents=True, exist_ok=True)

        return directory

    def get_plot_root_directory(self, **kwargs) -> Path:
        """Get plot root directory from mediator configuration.

        :returns: Plot root-directory.
        """
        directory = self.get('plot_dir')
        directory = (Path('plot') if directory is None else
                     Path(*ensure_collection(directory, list)))

        return directory

    def get_plot_directory(
            self, container: 'e4clim.container.base.ContainerBase' = None,
            makedirs: bool = True, subdirs: e4tp.StrIterableType = None,
            **kwargs) -> Path:
        """Get project data directory and create it if needed.

        :param container: Container for which to get data directory.
        :param makedirs: Make directories if needed.
        :param subdirs: List of additional subdirectories.

        :returns: Directory path.
        """
        subdirs = ensure_collection(subdirs, list)
        base_dir = Path(self.get_plot_root_directory(**kwargs),
                        self['project_name'])

        directory = (Path(base_dir, container.name) if container is not None
                     else base_dir)
        if subdirs is not None:
            directory = Path(directory, *subdirs)

        if makedirs:
            # Create directory if needed
            Path.mkdir(directory, parents=True, exist_ok=True)

        return directory

    # Interface with cfg dictionary
    def get(self, key: str, default: e4tp.CfgMappingType = None) -> e4tp.CfgMappingType:
        """Get item from :py:attr:`cfg`.

        :param key: Key.
        :param default: Default value to return.

        :returns: Value.
        """
        return self.cfg.get(key, default)

    def __getitem__(self, key: str) -> e4tp.CfgMappingType:
        """Get item from :py:attr:`cfg`.

        :param key: Key.

        :returns: Value.
        """
        return self.cfg[key]

    def __setitem__(self, key: str, value: e4tp.CfgType) -> None:
        """Set item in :py:attr:`cfg`.

        :param key: Key.
        :param value: Value.
        """
        self.cfg[key] = value

    def __contains__(self, key: str) -> bool:
        """:py:attr:`cfg` contains.

        :param key: Key.

        :returns: Test result.
        """
        return key in self.cfg

    def __delitem__(self, key: str) -> None:
        """Delete key.

        :param key: Key.
        """
        del self.cfg[key]

    def __iter__(self):
        """Iterate :py:attr:`cfg`.

        :returns: tp.Iterable.
        """
        return iter(self.cfg)

    def __len__(self) -> int:
        """Length of :py:obj:`cfg`.

        :returns: Length.
        """
        return len(self.cfg)

    def __str__(self) -> str:
        """Return `str(self.cfg)`.

        :returns: String.
        """
        return str(self.cfg)

    def __bool__(self) -> bool:
        """Cast to boolean.

        :returns: Boolean cast.
        """
        return bool(self.cfg)


def _get_credentials_from_file(
        keys_filepath: e4tp.PathType, name: str) -> tp.Tuple[
            dict, tp.MutableMapping]:
    """Get credentials from file.

    :param keys_filepath: Keys filepath.
    :param name: Name.

    :returns: Credentials and keys dictionnary
    """
    if Path.is_file(keys_filepath):
        with open(keys_filepath, 'r') as f:
            cfg_keys = yaml.load(f, Loader=yaml.FullLoader)

        # Get or create container credentials dictionary
        if not isinstance(cfg_keys.get(name), tp.MutableMapping):
            cfg_keys[name] = {}
        cred = cfg_keys[name]
    else:
        cred = {}
        cfg_keys = {name: {}}

    return cred, cfg_keys


def _get_pass_if_needed(
        keys: tp.Iterable, cred: tp.MutableMapping,
        name: str) -> tp.Tuple[tp.MutableMapping, bool]:
    """Get pass if needed.

    :param keys: Names of keys to get.
    :param cred: Credentials parsed so far.
    :param name: Name.

    :returns: Updated credentials and is updated flag.
    """
    any_new = False
    for k in keys:
        if cred.get(k) is None:
            # Get credential value for key
            cred[k] = getpass('{} {}: '.format(name, k))
            any_new = True

    return cred, any_new


def _save_new_credentials_if_needed(
        any_new: bool, keys_filepath: e4tp.PathType,
        cfg_keys: tp.Mapping) -> None:
    """Save new credentials if needed.

    :param any_new: Whether credentials have been updated.
    :param keys_filepath: Filepath to keys.
    :param cfg_keys: Keys configuration.
    """
    if any_new:
        # Ask if user wants to save keys to keys file
        q = None
        while q not in ['no', 'yes', '']:
            q = input(
                'Save new credentials to {} ([yes]/no)? '.format(
                    keys_filepath))
        if q in ['yes', '']:
            with open(keys_filepath, 'r+') as f:
                yaml.dump(cfg_keys, f, default_flow_style=False)


def import_class_from_cfg(cfg: e4tp.CfgType) -> tp.Type:
    """Import class using container configuration.

    :param cfg: Configuration.

    :returns: Class.
    """
    theclass = None

    class_path = cfg.get('class')
    if class_path is not None:
        path_list = class_path.split('.')
        class_name = path_list.pop()
        module_path = '.'.join(path_list)
        module = import_module(module_path, package=__package__)
        theclass = getattr(module, class_name)

    return theclass


def _read_configuration(filepath: e4tp.StrIterableType) -> e4tp.CfgType:
    """Read source configuration from filepath.

    :param filepath: Configuration filepath.

    :returns: Configuration.
    """
    filepath = Path(*ensure_collection(filepath, list))
    with open(filepath, 'r') as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)

    return cfg


def get_param_rng(cfg: e4tp.CfgType, param_name) -> np.ndarray:
    """Get parameter range.

    :param cfg: Configuration.
    :param_name: Parameter name.

    :returns: Parameter range.
    """
    cfg_param = cfg[param_name]
    if isinstance(cfg_param, tp.Mapping):
        param_rng = np.arange(
            cfg_param['start'], cfg_param['stop'], cfg_param['step'])
    elif isinstance(cfg_param, tp.Sequence):
        param_rng = np.array(cfg_param).astype(float)
    elif (isinstance(cfg_param, float) or isinstance(cfg_param, int)):
        param_rng = np.array([cfg_param]).astype(float)

    return param_rng
