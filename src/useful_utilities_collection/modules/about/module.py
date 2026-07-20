from useful_utilities_collection.core.module_registry import ModuleDefinition
from useful_utilities_collection.core.translation import t
from useful_utilities_collection.modules.about.page import AboutPage


def create_module() -> ModuleDefinition:
    return ModuleDefinition(
        module_id="about",
        title=t("about.title"),
        page_factory=lambda context: AboutPage(context),
    )
