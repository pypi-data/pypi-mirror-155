import importlib
import importlib.util
import sys
from importlib import reload
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Dict, Union

from ready_logger import logger

# cache dynamically imported modules. map module name or path to imported module.
_dynamically_imported_modules: Dict[Union[str, Path], ModuleType] = {}


def import_module(module_name_or_path: Union[Path, str]) -> ModuleType:
    """Get a dynamically imported module from cache or import it now if it's not in cache.

    Args:
        module_name_or_path (Union[Path, str]): Name of module (e.g. `requests`) or path to module file (e.g. `/home/user/my_package/my_module.py`)

    Returns:
        ModuleType: The imported module.
    """
    module_name_or_path = str(module_name_or_path)
    if module_name_or_path in _dynamically_imported_modules:
        # use already imported module.
        return _dynamically_imported_modules[module_name_or_path]
    module = _load_module(module_name_or_path)
    _dynamically_imported_modules[module_name_or_path] = module
    return module


def import_function(
    module_name_or_path: Union[Path, str], function_name: str
) -> Callable:
    """Get reference to a function in a module, importing the module if needed.

    Args:
        module_name_or_path (Union[Path, str]): Name of module (e.g. `requests`) or path to module file (e.g. `/home/user/my_package/my_module.py`)
        function_name (str): Name of a function in module.

    Returns:
        Callable: The function.
    """
    return _get_module_attr(module_name_or_path, function_name)


def import_class(module_name_or_path: Union[Path, str], class_name: str) -> Any:
    """Get reference to a class in a module, importing the module if needed.

    Args:
        module_name_or_path (Union[Path, str]): Name of module (e.g. `requests`) or path to module file (e.g. `/home/user/my_package/my_module.py`)
        class_name (str): Name of a class in module.

    Returns:
        Callable: The class.
    """
    return _get_module_attr(module_name_or_path, class_name)


def reload_modules() -> None:
    """Reload all imported modules."""
    for mod_name, mod in _dynamically_imported_modules.items():
        if mod_name in sys.modules:
            _dynamically_imported_modules[mod_name] = reload(mod)
        else:
            logger.warning(f"Could not reload module {mod_name}")


def _load_module_file(file_path: Union[Path, str]) -> ModuleType:
    """Import the module at `file_path`.

    Args:
        file_path (Union[Path, str]): Path to module file (e.g. `/home/user/my_package/my_module.py`)

    Returns:
        ModuleType: The imported module.
    """
    logger.info(f"Importing module from file path: {file_path}")
    module_spec = importlib.util.spec_from_file_location(
        Path(file_path).stem, str(file_path)
    )
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


def _load_installed_module(module: str) -> ModuleType:
    """Import an installed module.

    Args:
        module (str): Name of module (e.g. `requests`)

    Returns:
        ModuleType: The imported module.
    """
    logger.info(f"Importing installed module: {module}")
    module = importlib.import_module(module)
    return module


def _load_module(name_or_path: Union[Path, str]) -> ModuleType:
    """Dynamically import a module from a file path or module name.

    Args:
        name_or_path (Union[Path, str]): Name of module (e.g. `requests`) or path to module file (e.g. `/home/user/my_package/my_module.py`)

    Returns:
        ModuleType: The imported module.
    """
    #
    # file path has '/' separator. module path has '.' separator.
    return (
        _load_module_file(name_or_path)
        if Path(name_or_path).suffix == ".py"
        else _load_installed_module(name_or_path)
    )


def _get_module_attr(module_name_or_path: Union[Path, str], attr_name: str) -> Any:
    """Get reference to a module's attribute, importing the module if needed.

    Args:
        module_name_or_path (Union[Path, str]): Name of module (e.g. `requests`) or path to module file (e.g. `/home/user/my_package/my_module.py`)
        attr_name (str): Name of the attribute.

    Returns:
        Any: The attribute.
    """
    module = import_module(module_name_or_path)
    if not hasattr(module, attr_name):
        raise AttributeError(
            f"Could not load {attr_name} from module {module_name_or_path}!"
        )
    return getattr(module, attr_name)
