from dataclasses import dataclass
from typing import Callable

from PySide6.QtWidgets import QWidget

from useful_utilities_collection.core.app_context import AppContext


@dataclass
class ModuleDefinition:
    module_id: str
    title: str
    page_factory: Callable[[AppContext], QWidget]