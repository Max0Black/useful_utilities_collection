import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import unittest
from useful_utilities_collection.core import translation

class TestTranslation(unittest.TestCase):
    def setUp(self):
        # Reset language to English before each test
        translation.set_language("en")

    def test_default_language_is_english(self):
        self.assertEqual(translation.get_language(), "en")

    def test_fallback_behavior(self):
        # Test that missing keys fallback to the key string itself
        missing_key = "nonexistent.key.path"
        self.assertEqual(translation.t(missing_key), missing_key)
        
        # Test fallback with a custom default
        self.assertEqual(translation.t(missing_key, default="Default Text"), "Default Text")

    def test_placeholder_formatting(self):
        # Test with string formatting variables (e.g. {level})
        translation.set_language("en")
        formatted = translation.t("dashboard.microphone_state_active", level=85)
        self.assertEqual(formatted, "Guard active · 85%")
        
        translation.set_language("de")
        formatted_de = translation.t("dashboard.microphone_state_active", level=85)
        self.assertEqual(formatted_de, "Guard aktiv · 85%")

    def test_all_languages_have_matching_keys(self):
        # Verify that English and German translation files have the exact same set of keys
        from useful_utilities_collection.core.translation import TRANSLATIONS
        
        self.assertIn("en", TRANSLATIONS)
        self.assertIn("de", TRANSLATIONS)
        
        en_keys = self._get_all_dotted_keys(TRANSLATIONS["en"])
        de_keys = self._get_all_dotted_keys(TRANSLATIONS["de"])
        
        missing_in_de = en_keys - de_keys
        missing_in_en = de_keys - en_keys
        
        self.assertEqual(missing_in_de, set(), f"Keys in English but missing in German: {missing_in_de}")
        self.assertEqual(missing_in_en, set(), f"Keys in German but missing in English: {missing_in_en}")

    def _get_all_dotted_keys(self, d, prefix=""):
        keys = set()
        for k, v in d.items():
            full_key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                keys.update(self._get_all_dotted_keys(v, full_key))
            else:
                keys.add(full_key)
        return keys

if __name__ == "__main__":
    unittest.main()
