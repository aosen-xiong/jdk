"""Guard package coverage against accidentally empty or incomplete manifests."""

import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from run import CLEAN, classify, validate_manifest


class ManifestTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / "src/java.xml/share/classes/javax/xml/namespace"
        self.folder.mkdir(parents=True)
        for name in ["QName.java", "NamespaceContext.java", "package-info.java"]:
            (self.folder / name).touch()
        self.manifest = {
            "package": "javax.xml.namespace",
            "module": "java.xml",
            "verified_files": ["QName", "NamespaceContext"],
            "candidates": [
                {
                    "id": name,
                    "module": "java.xml",
                    "path": str(
                        (self.folder / (name + ".java")).relative_to(self.root)
                    ),
                }
                for name in ["QName", "NamespaceContext"]
            ],
        }

    def validate(self, manifest):
        with patch("run.JDK", self.root):
            validate_manifest(manifest)

    def test_complete_package_accepts_documentation_only_file(self):
        self.validate(self.manifest)

    def test_removal_from_both_manifest_lists_is_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["verified_files"].remove("QName")
        manifest["candidates"] = [
            entry for entry in manifest["candidates"] if entry["id"] != "QName"
        ]
        with self.assertRaisesRegex(ValueError, "coverage changed"):
            self.validate(manifest)

    def test_empty_or_duplicate_selection_is_rejected(self):
        for selected in [[], ["QName", "QName"]]:
            with self.subTest(selected=selected), self.assertRaises(ValueError):
                self.validate({**self.manifest, "verified_files": selected})

    def test_new_source_requires_enrollment(self):
        (self.folder / "NewContract.java").touch()
        with self.assertRaisesRegex(ValueError, "coverage changed"):
            self.validate(self.manifest)

    def test_warnings_and_suppressions_do_not_pass_ci(self):
        source = Path("/example/Test.java")
        review = {
            "source_sha256": "hash",
            "all_declarations_reviewed": True,
            "top_level_declarations": ["Test"],
            "opted_in": True,
            "basis": "Reviewed fixture",
            "suppression_keys": [],
        }
        log = "Note: NullnessNoInitSubchecker is type-checking " + str(source)
        result = classify(
            log + "\nwarning: [type.anno.before.decl.anno] ordering",
            0,
            False,
            source,
            "hash",
            review,
        )
        self.assertNotIn(result["status"], CLEAN)
        result = classify(
            log, 0, False, source, "hash", {**review, "suppression_keys": ["nullness"]}
        )
        self.assertNotIn(result["status"], CLEAN)


if __name__ == "__main__":
    unittest.main()
