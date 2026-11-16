"""Scope review for fully inspected contract fixtures."""

from run import digest


def review(source, declaration, suppressions=()):
    """Bind the controlled source's known opted-in scope to its hash."""
    return {
        "source_sha256": digest(source),
        "all_declarations_reviewed": True,
        "top_level_declarations": [declaration],
        "opted_in": True,
        "suppression_keys": list(suppressions),
        "basis": "Controlled fixture, complete source reviewed, no opt-outs; suppression keys enumerated.",
    }
