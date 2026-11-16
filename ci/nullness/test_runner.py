"""Check classification boundaries that can otherwise create false coverage."""

import unittest
from pathlib import Path

from run import classify


class ClassificationTest(unittest.TestCase):
    """No skipped, interrupted, or unaudited unit may become a clean result."""

    def setUp(self):
        """Create a reviewed, opted-in compilation unit."""
        self.source = Path("/example/Example.java")
        self.visit = "Note: NullnessNoInitSubchecker is type-checking " + str(
            self.source
        )
        self.review = {
            "source_sha256": "hash",
            "all_declarations_reviewed": True,
            "top_level_declarations": ["Example"],
            "basis": "Scope inspected.",
            "opted_in": True,
            "suppression_keys": [],
        }

    def status(self, output, code=0, timeout=False, review=None):
        """Classify one synthetic completion record."""
        return classify(
            output, code, timeout, self.source, "hash", review or self.review
        )["status"]

    def test_clean_requires_visitation_and_current_review(self):
        """Silent completion and stale reviews are not coverage."""
        self.assertEqual(self.status(self.visit), "clean-without-suppressions")
        self.assertEqual(self.status(""), "not-visited")
        self.assertEqual(
            self.status(self.visit, review={**self.review, "source_sha256": "old"}),
            "scope-review-required",
        )

    def test_unmarked_and_suppressed_are_distinct(self):
        """Opt-in and suppression metadata remain visible in results."""
        self.assertEqual(
            self.status(self.visit, review={**self.review, "opted_in": False}),
            "not-opted-in",
        )
        self.assertEqual(
            self.status(
                self.visit,
                review={
                    **self.review,
                    "suppression_keys": ["nullness:return.type.incompatible"],
                },
            ),
            "clean-with-suppressions",
        )

    def test_crash_timeout_and_truncation_are_never_clean(self):
        """A visited file with interrupted checking is incomplete."""
        self.assertEqual(
            self.status(self.visit + "\nThe Checker Framework crashed"),
            "checker-or-compiler-crashed",
        )
        self.assertEqual(self.status(self.visit, timeout=True), "timed-out")
        self.assertEqual(
            self.status(self.visit + "\nonly showing the first 10 errors"),
            "incomplete-diagnostics",
        )

    def test_unsupported_mode_and_compiler_errors(self):
        """Configuration failures do not become annotation findings."""
        self.assertEqual(
            self.status(
                self.visit
                + "\nwarning: The following options were not recognized by any processor: '[mode]'"
            ),
            "profile-unsupported",
        )
        self.assertEqual(
            self.status(self.visit + "\nX.java:1: error: cannot find symbol", 1),
            "compiler-blocked",
        )

    def test_checker_error_and_unexplained_failure(self):
        """Known diagnostic keys and unknown failures remain separate."""
        self.assertEqual(
            self.status(
                self.visit + "\nX.java:1: error: [return.type.incompatible] bad", 1
            ),
            "checked-with-diagnostics",
        )
        self.assertEqual(
            self.status(self.visit, 1), "failed-without-classified-diagnostics"
        )


if __name__ == "__main__":
    unittest.main()
