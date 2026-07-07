from useful_utilities_collection.core.module_registry import ModuleDefinition
from useful_utilities_collection.core.translation import t
from useful_utilities_collection.modules.settings.page import SettingsPage


def create_module() -> ModuleDefinition:
    return ModuleDefinition(
        module_id="settings",
        title=t("settings.title"),
        page_factory=lambda context: SettingsPage(context),
    )
