package javax.xml.namespace;

import java.util.Collections;
import java.util.Iterator;
import org.checkerframework.checker.nullness.qual.Nullable;
import org.checkerframework.framework.qual.AnnotatedFor;

@AnnotatedFor("nullness")
class Valid {
    int constructors() {
        QName two = new QName(null, "local");
        QName three = new QName(null, "local", "p");
        two.equals(null);
        return two.getNamespaceURI().length() + three.getPrefix().length()
                + QName.valueOf("{urn:test}local").getLocalPart().length();
    }

    int context(NamespaceContext context) {
        String prefix = context.getPrefix("urn:test");
        int length = prefix == null ? 0 : prefix.length();
        Iterator<String> prefixes = context.getPrefixes("urn:test");
        while (prefixes.hasNext()) {
            length += prefixes.next().length();
        }
        return length + context.getNamespaceURI("p").length();
    }

    static class Name extends QName {
        Name() { super(null, "local"); }
        @Override public String getLocalPart() { return super.getLocalPart(); }
    }

    static class Context implements NamespaceContext {
        public String getNamespaceURI(String prefix) {
            if (prefix.equals("xml")) return javax.xml.XMLConstants.XML_NS_URI;
            if (prefix.equals("xmlns")) return javax.xml.XMLConstants.XMLNS_ATTRIBUTE_NS_URI;
            return "";
        }

        public @Nullable String getPrefix(String uri) {
            if (uri.equals(javax.xml.XMLConstants.XML_NS_URI)) return "xml";
            if (uri.equals(javax.xml.XMLConstants.XMLNS_ATTRIBUTE_NS_URI)) return "xmlns";
            return uri.isEmpty() ? "" : null;
        }

        public Iterator<String> getPrefixes(String uri) {
            String prefix = getPrefix(uri);
            return prefix == null ? Collections.emptyIterator()
                    : Collections.singletonList(prefix).iterator();
        }
    }
}
