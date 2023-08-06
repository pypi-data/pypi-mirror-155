"""Root package info."""
import logging
import os

from lightning_app import _root_logger  # noqa: F401
from lightning_app import _logger  # noqa: F401
_logger.setLevel(logging.INFO)

from lightning_app import _console  # noqa: F401
_console.setLevel(logging.INFO)

from lightning_app import formatter  # noqa: F401
_console.setFormatter(formatter)



if not _root_logger.hasHandlers():
    _logger.addHandler(_console)
    _logger.propagate = False


from lightning.app import components
from lightning.app.core.app import LightningApp
from lightning.app.core.flow import LightningFlow
from lightning.app.core.work import LightningWork
from lightning.app.utilities.imports import _module_available
from lightning.app.utilities.packaging.build_config import BuildConfig
from lightning.app.utilities.packaging.cloud_compute import CloudCompute

if _module_available("lightning.app.components.demo"):
    from lightning.app.components import demo

from lightning_app import _PACKAGE_ROOT  # noqa: F401
from lightning_app import _PROJECT_ROOT  # noqa: F401

