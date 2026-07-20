from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QCursor, QDesktopServices
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
    QPushButton,
)

from useful_utilities_collection.core.build_info import get_build_info
from useful_utilities_collection.core.translation import t
from useful_utilities_collection.ui.components import BasePage


class AboutPage(BasePage):
    def __init__(self, context):
        super().__init__(context)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self._repository_url = ""

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 28, 28, 28)
        root.setSpacing(18)

        # ── Page header (matches the other pages) ────────────────────
        header = QHBoxLayout()
        header.setSpacing(12)
        header.setContentsMargins(0, 0, 0, 0)

        self.title_label = QLabel()
        self.title_label.setObjectName("PageTitle")

        self.version_badge = QLabel()
        self.version_badge.setObjectName("AboutVersionBadge")

        header.addWidget(self.title_label)
        header.addStretch()
        header.addWidget(self.version_badge)

        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("MutedText")
        self.subtitle_label.setWordWrap(True)

        # ── Open-source highlight card ────────────────────────────────
        oss_card = QFrame()
        oss_card.setObjectName("AboutOssCard")
        oss_layout = QVBoxLayout(oss_card)
        oss_layout.setContentsMargins(18, 16, 18, 16)
        oss_layout.setSpacing(12)

        self.oss_title = QLabel()
        self.oss_title.setObjectName("AboutOssTitle")

        self.oss_body = QLabel()
        self.oss_body.setObjectName("MutedText")
        self.oss_body.setWordWrap(True)

        self.github_button = QPushButton()
        self.github_button.setObjectName("PrimaryButton")
        self.github_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.github_button.clicked.connect(self._open_repository)

        oss_layout.addWidget(self.oss_title)
        oss_layout.addWidget(self.oss_body)
        oss_layout.addWidget(self.github_button)

        # ── Build details card ─────────────────────────────────────────
        details_card = QFrame()
        details_card.setObjectName("Panel")
        details_layout = QVBoxLayout(details_card)
        details_layout.setContentsMargins(18, 18, 18, 18)
        details_layout.setSpacing(10)

        self.details_title = QLabel()
        self.details_title.setObjectName("SectionTitle")
        details_layout.addWidget(self.details_title)

        self._rows: dict[str, QLabel] = {}
        self._labels: dict[str, QLabel] = {}
        for key in (
            "about.field_author",
            "about.field_build_time",
            "about.field_build_source",
            "about.field_license",
            "about.field_internal_name",
            "about.field_original_filename",
            "about.field_python",
            "about.field_platform",
        ):
            details_layout.addWidget(self._build_row(key))

        self.copyright_label = QLabel()
        self.copyright_label.setObjectName("AboutCopyright")
        self.copyright_label.setWordWrap(True)

        root.addLayout(header)
        root.addWidget(self.subtitle_label)
        root.addWidget(oss_card)
        root.addWidget(details_card)
        root.addWidget(self.copyright_label)
        root.addStretch()

        # Re-translate dynamically when the UI language changes (fixes the
        # "Build Information" heading and field labels staying in the old
        # language after a switch in Settings).
        self.context.state_changed.connect(self.refresh)

        self.refresh()

    def _build_row(self, key: str) -> QWidget:
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(12)

        label = QLabel(t(key))
        label.setObjectName("AboutFieldLabel")
        label.setMinimumWidth(150)

        value = QLabel("—")
        value.setObjectName("AboutFieldValue")
        value.setTextInteractionFlags(Qt.TextSelectableByMouse)

        row.addWidget(label)
        row.addStretch()
        row.addWidget(value)

        container = QWidget()
        container.setLayout(row)

        self._rows[key] = value
        self._labels[key] = label
        return container

    def _open_repository(self) -> None:
        if self._repository_url:
            QDesktopServices.openUrl(QUrl(self._repository_url))

    def refresh(self) -> None:
        info = get_build_info()
        self._repository_url = info.get("repository_url", "")

        self.title_label.setText(t("about.page_title"))
        self.subtitle_label.setText(t("about.page_subtitle"))

        self.version_badge.setText(t("about.version_badge", version=info["version"]))

        self.oss_title.setText(t("about.oss_title"))
        self.oss_body.setText(t("about.oss_body"))
        self.github_button.setText(t("about.github_button"))

        self.details_title.setText(t("about.section_build_info"))

        self._labels["about.field_author"].setText(t("about.field_author"))
        self._labels["about.field_build_time"].setText(t("about.field_build_time"))
        self._labels["about.field_build_source"].setText(t("about.field_build_source"))
        self._labels["about.field_license"].setText(t("about.field_license"))
        self._labels["about.field_internal_name"].setText(t("about.field_internal_name"))
        self._labels["about.field_original_filename"].setText(t("about.field_original_filename"))
        self._labels["about.field_python"].setText(t("about.field_python"))
        self._labels["about.field_platform"].setText(t("about.field_platform"))

        self._rows["about.field_author"].setText(info["author"])
        self._rows["about.field_build_time"].setText(info["build_time"])
        self._rows["about.field_build_source"].setText(info["build_source"])
        self._rows["about.field_license"].setText(info["license"])
        self._rows["about.field_internal_name"].setText(info["internal_name"])
        self._rows["about.field_original_filename"].setText(info["original_filename"])
        self._rows["about.field_python"].setText(info["python_version"])
        self._rows["about.field_platform"].setText(info["platform"])

        self.copyright_label.setText(t("about.copyright", copyright=info["copyright"]))
