from useful_utilities_collection.core.module_registry import ModuleDefinition
from useful_utilities_collection.modules.dashboard.page import DashboardPage

def create_module() -> ModuleDefinition:
    return ModuleDefinition(
        module_id="dashboard",
        title="Dashboard",
        page_factory=lambda context: DashboardPage(context),
    )