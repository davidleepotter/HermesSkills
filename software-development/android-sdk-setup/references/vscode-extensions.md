# VS Code Extensions for Android Development

Verified extension IDs for Android development in VS Code on Linux.

## Core Extensions

| Extension ID | Publisher | Purpose |
|---|---|---|
| `vscjava.vscode-java-pack` | vscjava | Java language pack (includes Gradle, Maven, debugger, test) |
| `redhat.java` | redhat | Java Language Server (included in java-pack) |
| `vscjava.vscode-gradle` | vscjava | Gradle build integration |
| `vscjava.vscode-java-debug` | vscjava | Java debugger |
| `vscjava.vscode-java-dependency` | vscjava | Project dependency explorer |
| `vscjava.vscode-java-test` | vscjava | Test explorer |
| `vscjava.vscode-maven` | vscjava | Maven support |

## Kotlin Extensions (verify IDs on marketplace)

- `kotlin.kotlinsyntax` — Kotlin syntax highlighting (publisher may change)
- `angelomol.vscode-kotlin-language` — Kotlin language support (may be unavailable)

## How to Install

```bash
# Correct (snap-based Ubuntu):
snap run code --install-extension <extension-id>

# WRONG (broken symlink):
snap/bin/code --install-extension <extension-id>   # DO NOT USE
```

## Notes

- Extension IDs on the VS Code marketplace can change. If an install fails with "Extension not found", search the marketplace directly for the current publisher and ID.
- The Java pack (`vscjava.vscode-java-pack`) is a meta-extension that installs all Java-related extensions at once. Install this first.
