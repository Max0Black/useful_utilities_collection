from useful_utilities_collection.core.module_registry import ModuleDefinition
from useful_utilities_collection.modules.keyboard_lock.page import KeyboardLockPage

def create_module() -> ModuleDefinition:
    return ModuleDefinition(
        module_id="keyboard_lock",
        title="Keyboard Lock",
        page_factory=lambda context: KeyboardLockPage(context),
    )