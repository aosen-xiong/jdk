package javax.xml.namespace;

import java.util.Collections;
import java.util.Iterator;
import org.checkerframework.checker.nullness.qual.Nullable;
import org.checkerframework.framework.qual.AnnotatedFor;

@AnnotatedFor("nullness")
class Invalid {
    void callers(NamespaceContext context) {
        // :: error: (argument.type.incompatible)
        new QName(null);
        // :: error: (argument.type.incompatible)
        new QName("urn:test", null);
        // :: error: (argument.type.incompatible)
        new QName("urn:test", null, "p");
        // :: error: (argument.type.incompatible)
        new QName("urn:test", "local", null);
        // :: error: (argument.type.incompatible)
        QName.valueOf(null);
        // :: error: (argument.type.incompatible)
        context.getNamespaceURI(null);
        // :: error: (argument.type.incompatible)
        context.getPrefix(null);
        // :: error: (argument.type.incompatible)
        context.getPrefixes(null);
        // :: error: (dereference.of.nullable)
        context.getPrefix("urn:missing").length();
    }

    static class Context implements NamespaceContext {
        public String getNamespaceURI(String prefix) {
            // :: error: (return.type.incompatible)
            return null;
        }
        public @Nullable String getPrefix(String uri) { return null; }
        public Iterator<String> getPrefixes(String uri) {
            // :: error: (return.type.incompatible)
            return null;
        }
    }

    static abstract class NullElementContext implements NamespaceContext {
        public Iterator<String> getPrefixes(String uri) {
            // :: error: (return.type.incompatible)
            return Collections.<@Nullable String>singletonList(null).iterator();
        }
    }
}
