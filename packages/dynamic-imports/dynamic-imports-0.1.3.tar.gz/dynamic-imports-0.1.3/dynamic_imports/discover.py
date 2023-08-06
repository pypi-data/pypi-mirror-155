import pkgutil
import pyclbr
from types import ModuleType
from typing import List, Union

from ready_logger import logger

from .importers import import_class, import_module


def get_modules(
    package: ModuleType, recursive: bool = True, import_modules: bool = True
) -> Union[List[str], List[ModuleType]]:
    """Find all modules in a package or nested packages.

    Args:
        package (ModuleType): Top-level package where search should be started.
        recursive (bool, optional): Recurse into sub-packages. Defaults to True.
        import_modules (bool, optional): Import discovered modules. Defaults to True.

    Returns:
        Union[List[str], List[ModuleType]]: A list of imported modules or module names.
    """
    searcher = pkgutil.walk_packages if recursive else pkgutil.iter_modules
    modules = [
        name
        for _, name, ispkg in searcher(package.__path__, f"{package.__name__}.")
        if not ispkg
    ]
    if import_modules:
        return [import_module(name) for name in modules]
    return modules


def get_module_classes(
    module: Union[str, ModuleType],
    base_class: Union[str, ModuleType],
    module_path: Union[str, List[str]] = None,
    import_classes: bool = True,
) -> Union[List[str], List[ModuleType]]:
    """Find all implementations of `base_class` in `module`.

    Args:
        module (Union[str, ModuleType]): Module to search in.
        base_class (Union[str, ModuleType]): Base class who's derived implementations should be searched for.
        module_path (Union[str, List[str]], optional): Non-default path where module should be searched for. Defaults to None.
        import_classes (bool, optional): Return the class attributes from imported module if True, or class names if False. Defaults to True.

    Returns:
        Union[List[str], List[ModuleType]]: Imported classes or class names.
    """
    if isinstance(module, str):
        derived_classes = _derived_classes_from_module_name(
            base_class, module, module_path, import_classes
        )
    else:
        derived_classes = _derived_classes_from_module(
            base_class, module, import_classes
        )
    logger.info(
        f"Found {len(derived_classes)} derived classes of type {base_class} in {module}"
    )
    return derived_classes


def get_package_classes(
    package: ModuleType,
    base_class: Union[str, ModuleType],
    recursive: bool = True,
    module_path: Union[str, List[str]] = None,
    import_classes: bool = True,
) -> Union[List[str], List[ModuleType]]:
    """Find all implementations of `base_class` in `package`.

    Args:
        package (ModuleType): Top-level package where search should be started.
        base_class (Union[str, ModuleType]): Base class who's derived implementations should be searched for.
        recursive (bool, optional): Recurse into sub-packages. Defaults to True.
        module_path (Union[str, List[str]], optional): Non-default path where module should be searched for. Defaults to None.
        import_classes (bool, optional): Return the class attributes from imported module if True, or class names if False. Defaults to True.

    Returns:
        Union[List[str], List[ModuleType]]: Imported classes or class names.
    """
    pkg_classes = []
    for module in get_modules(package, recursive, import_classes):
        pkg_classes += get_module_classes(
            module, base_class, module_path, import_classes
        )
    return pkg_classes


def _derived_classes_from_module(
    class_type: Union[ModuleType, str], module: ModuleType, import_classes: bool = True
) -> Union[List[str], List[ModuleType]]:
    """Find all implementations of `base_class` in `module`.

    Args:
        class_type (Union[ModuleType, str]): Base class who's derived implementations should be searched for.
        module (ModuleType): Module to search in.
        import_classes (bool, optional): Return the class attributes from imported module if True, or class names if False. Defaults to True.

    Returns:
        Union[List[str], List[ModuleType]]: Imported classes or class names.
    """
    if isinstance(class_type, str):
        classes = [
            e
            for e in module.__dict__.values()
            if class_type in [c.__name__ for c in getattr(e, "__bases__", [])]
        ]
    else:
        classes = [
            e
            for e in module.__dict__.values()
            if class_type in getattr(e, "__bases__", [])
        ]
    if not import_classes:
        # get name of each class object.
        classes = [c.__name__ for c in classes]
    return classes


def _derived_classes_from_module_name(
    class_type: Union[ModuleType, str],
    module_name: str,
    module_path: str = None,
    import_classes: bool = True,
) -> Union[List[str], List[ModuleType]]:
    """Find all implementations of `base_class` in the module named `module_name`.

    Args:
        class_type (Union[ModuleType, str]): Base class who's derived implementations should be searched for.
        module_name (str): Name of module to search in.
        module_path (str, optional): Non-default path where module should be searched for. Defaults to None.
        import_classes (bool, optional): Return the class attributes from imported module if True, or class names if False. Defaults to True.

    Returns:
        Union[List[str], List[ModuleType]]: Imported classes or class names.
    """
    class_name = class_type.__name__ if not isinstance(class_type, str) else class_type
    # inspect static file.
    if module_path and not isinstance(module_path, list):
        module_path = [module_path]
    all_classes = pyclbr.readmodule(module_name, path=module_path).values()
    classes = [c.name for c in all_classes if any(s == class_name for s in c.super)]
    if import_classes:
        # use class names to import classes.
        return [import_class(module_name, c) for c in classes]
    return classes
