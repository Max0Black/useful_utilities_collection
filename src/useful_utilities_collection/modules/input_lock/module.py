from useful_utilities_collection.core.module_registry import ModuleDefinition
from useful_utilities_collection.modules.input_lock.page import InputLockPage

def create_module() -> ModuleDefinition:
    return ModuleDefinition(
        module_id="input_lock",
        title="Input Lock",
        page_factory=lambda context: InputLockPage(context),
    )