"""Replay documentation-derived controls for javax.xml.namespace."""

import argparse
import json
import sys
from pathlib import Path

from contracts import review
from run import JDK, Study, write_json

ARGUMENT = {"argument.type.incompatible": 1}
CASES = {
    "qname-null-namespace-two": (
        'String test() { return new javax.xml.namespace.QName(null, "local").getNamespaceURI(); }',
        {},
    ),
    "qname-null-namespace-three": (
        """String test() {
            return new javax.xml.namespace.QName(null, "local", "p").getNamespaceURI();
        }""",
        {},
    ),
    "qname-equals-null": (
        "boolean test(javax.xml.namespace.QName q) { return q.equals(null); }",
        {},
    ),
    "qname-values": (
        """int test() {
            javax.xml.namespace.QName q = javax.xml.namespace.QName.valueOf("{urn:test}local");
            Object object = q;
            object.equals(null);
            return q.getNamespaceURI().length() + q.getLocalPart().length()
                + q.getPrefix().length() + q.toString().length();
        }
        static class Name extends javax.xml.namespace.QName {
            Name() { super(null, "local"); }
            @Override public String getLocalPart() { return super.getLocalPart(); }
        }""",
        {},
    ),
    "qname-null-local-one": (
        "void test() { new javax.xml.namespace.QName(null); }",
        ARGUMENT,
    ),
    "qname-null-local-two": (
        'void test() { new javax.xml.namespace.QName("urn:test", null); }',
        ARGUMENT,
    ),
    "qname-null-local-three": (
        'void test() { new javax.xml.namespace.QName("urn:test", null, "p"); }',
        ARGUMENT,
    ),
    "qname-null-prefix": (
        'void test() { new javax.xml.namespace.QName("urn:test", "local", null); }',
        ARGUMENT,
    ),
    "qname-null-valueof": (
        "void test() { javax.xml.namespace.QName.valueOf(null); }",
        ARGUMENT,
    ),
    "namespace-valid-client": (
        """int test(javax.xml.namespace.NamespaceContext context) {
            String prefix = context.getPrefix("urn:test");
            int length = prefix == null ? 0 : prefix.length();
            java.util.Iterator<String> prefixes = context.getPrefixes("urn:test");
            while (prefixes.hasNext()) { length += prefixes.next().length(); }
            return length + context.getNamespaceURI("p").length();
        }""",
        {},
    ),
    "namespace-null-prefix": (
        "void test(javax.xml.namespace.NamespaceContext c) { c.getNamespaceURI(null); }",
        ARGUMENT,
    ),
    "namespace-null-uri-prefix": (
        "void test(javax.xml.namespace.NamespaceContext c) { c.getPrefix(null); }",
        ARGUMENT,
    ),
    "namespace-null-uri-prefixes": (
        "void test(javax.xml.namespace.NamespaceContext c) { c.getPrefixes(null); }",
        ARGUMENT,
    ),
    "namespace-unchecked-prefix": (
        """int test(javax.xml.namespace.NamespaceContext c) {
            return c.getPrefix("urn:missing").length();
        }""",
        {"dereference.of.nullable": 1},
    ),
    "namespace-implementation": (
        """static class Context implements javax.xml.namespace.NamespaceContext {
            public String getNamespaceURI(String prefix) {
                if (prefix.equals("xml")) return javax.xml.XMLConstants.XML_NS_URI;
                if (prefix.equals("xmlns")) return javax.xml.XMLConstants.XMLNS_ATTRIBUTE_NS_URI;
                return "";
            }
            public @org.checkerframework.checker.nullness.qual.Nullable
            String getPrefix(String uri) {
                if (uri.equals(javax.xml.XMLConstants.XML_NS_URI)) return "xml";
                if (uri.equals(javax.xml.XMLConstants.XMLNS_ATTRIBUTE_NS_URI)) return "xmlns";
                if (uri.isEmpty()) return "";
                return null;
            }
            public java.util.Iterator<String> getPrefixes(String uri) {
                String prefix = getPrefix(uri);
                return prefix == null ? java.util.Collections.emptyIterator()
                    : java.util.Collections.singletonList(prefix).iterator();
            }
        }
        javax.xml.namespace.QName test() {
            javax.xml.namespace.NamespaceContext context = new Context();
            String prefix = context.getPrefix("urn:missing");
            return new javax.xml.namespace.QName(context.getNamespaceURI("unbound"), "local",
                prefix == null ? "" : prefix);
        }""",
        {},
    ),
    "namespace-invalid-implementation": (
        """static class Context implements javax.xml.namespace.NamespaceContext {
            public String getNamespaceURI(String prefix) { return null; }
            public @org.checkerframework.checker.nullness.qual.Nullable
            String getPrefix(String uri) { return null; }
            public java.util.Iterator<String> getPrefixes(String uri) { return null; }
        }""",
        {"return.type.incompatible": 2},
    ),
    "namespace-null-element": (
        """static abstract class Context implements javax.xml.namespace.NamespaceContext {
            public java.util.Iterator<String> getPrefixes(String uri) {
                return java.util.Collections.<
                    @org.checkerframework.checker.nullness.qual.Nullable String
                >singletonList(null).iterator();
            }
        }""",
        {"return.type.incompatible": 1},
    ),
}


def main():
    """Check the current working source contracts, preserving each control.

    Returns:
        Zero when every control has the expected result; one otherwise.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--label", default="namespace-contracts")
    parser.add_argument("--optin-baseline", action="store_true")
    args = parser.parse_args()
    study = Study(args.label)
    (study.root / "namespace_contracts.py").write_bytes(Path(__file__).read_bytes())
    cases = CASES
    if args.optin_baseline:
        cases = {
            key: (CASES[key][0], ARGUMENT)
            for key in (
                "qname-null-namespace-two",
                "qname-null-namespace-three",
                "qname-equals-null",
            )
        }
    results = []
    for name, (body, expected) in cases.items():
        patch = study.root / "fixtures" / name
        source = patch / "study/nullness/Consumer.java"
        source.parent.mkdir(parents=True)
        source.write_text(
            "package study.nullness;\n"
            '@org.checkerframework.framework.qual.AnnotatedFor("nullness")\n'
            "class Consumer {\n" + body + "\n}\n"
        )
        result = study.execute(
            name, "java.xml", source, review(source, "study.nullness.Consumer"), patch
        )
        result["expected_diagnostics"] = expected
        result["control_passed"] = (
            result["status"]
            == (
                "checked-with-diagnostics" if expected else "clean-without-suppressions"
            )
            and result["diagnostics_by_key"] == expected
            and result["visited"]
            and result["review_valid"]
        )
        results.append(result)
    if not args.optin_baseline:
        # Demonstrate why a clean body is insufficient to discover these inputs.
        patch = study.root / "fixtures" / "qname-without-nullable-namespace"
        qname = patch / "javax/xml/namespace/QName.java"
        qname.parent.mkdir(parents=True)
        original = (
            JDK / "src/java.xml/share/classes/javax/xml/namespace/QName.java"
        ).read_text()
        reduced = original
        for before, after in [
            ("final @Nullable String namespaceURI", "final String namespaceURI"),
            ("QName(@Nullable String namespaceURI", "QName(String namespaceURI"),
        ]:
            if reduced.count(before) != 1:
                raise ValueError("QName constructor contract missing or ambiguous")
            reduced = reduced.replace(before, after)
        qname.write_text(reduced)
        result = study.execute(
            "qname-constructor-removal-body",
            "java.xml",
            qname,
            review(qname, "javax.xml.namespace.QName"),
            patch,
        )
        result["expected_diagnostics"] = {}
        result["control_passed"] = result["status"] == "clean-without-suppressions"
        results.append(result)
        consumer = patch / "study/nullness/Consumer.java"
        consumer.parent.mkdir(parents=True)
        consumer.write_text(
            "package study.nullness;\n"
            '@org.checkerframework.framework.qual.AnnotatedFor("nullness")\n'
            "class Consumer { void test() {\n"
            'new javax.xml.namespace.QName(null, "local");\n'
            'new javax.xml.namespace.QName(null, "local", "p");\n'
            "} }\n"
        )
        result = study.execute(
            "qname-constructor-removal-client",
            "java.xml",
            consumer,
            review(consumer, "study.nullness.Consumer"),
            patch,
        )
        result["expected_diagnostics"] = {"argument.type.incompatible": 2}
        result["control_passed"] = (
            result["status"] == "checked-with-diagnostics"
            and result["diagnostics_by_key"] == result["expected_diagnostics"]
            and result["visited"]
            and result["review_valid"]
        )
        results.append(result)
    passed = all(result["control_passed"] for result in results)
    write_json(study.root / "summary.json", {"passed": passed, "results": results})
    print(json.dumps({"passed": passed, "evidence": str(study.root)}), flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
