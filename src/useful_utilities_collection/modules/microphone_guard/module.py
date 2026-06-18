from useful_utilities_collection.core.module_registry import ModuleDefinition
from useful_utilities_collection.modules.microphone_guard.page import MicrophoneGuardPage


def create_module() -> ModuleDefinition:
    return ModuleDefinition(
        module_id="microphone_guard",
        title="Microphone Guard",
        page_factory=lambda context: MicrophoneGuardPage(context),
    )