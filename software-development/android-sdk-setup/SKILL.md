---
name: android-sdk-setup
description: "Install and configure the Android SDK (command-line tools only) on Linux for headless development without Android Studio."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [android, sdk, java, gradle, adb, vscode]
---

# Android SDK Setup on Linux

Install and configure the Android SDK for command-line development on Linux. No Android Studio required.

## When to Use

- Setting up Android development on a headless Linux server or VM
- CI/CD pipelines that need to build/test Android projects
- Minimal environment without a GUI (Android Studio is not needed)
- When you only need SDK tools, ADB, and the emulator

## Prerequisites

```bash
sudo apt-get update && sudo apt-get install -y openjdk-17-jdk-headless wget unzip curl git
```

## Step 1: Download SDK Command-Line Tools

```bash
export ANDROID_HOME="$HOME/Android/Sdk"
mkdir -p "$ANDROID_HOME"
cd /tmp
wget -q "https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip" -O cmdline-tools.zip
unzip -q cmdline-tools.zip
mkdir -p "$ANDROID_HOME/cmdline-tools"
mv cmdline-tools "$ANDROID_HOME/cmdline-tools/latest"
rm cmdline-tools.zip
```

## Step 2: Accept Licenses & Install Packages

```bash
export ANDROID_HOME="$HOME/Android/Sdk"
export ANDROID_SDK_ROOT="$ANDROID_HOME"
export JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"
export PATH="$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$PATH"

yes | sdkmanager --licenses
sdkmanager --install "platform-tools" "platforms;android-35" "build-tools;35.0.0" "cmdline-tools;latest" "emulator" "extras;android;m2repository"
```

## Step 3: Environment Variables

Add to `~/.bashrc` (or your shell config):

```bash
export ANDROID_HOME="$HOME/Android/Sdk"
export ANDROID_SDK_ROOT="$ANDROID_HOME"
export JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"
export PATH="$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator"
```

## Step 4: VS Code Extensions

Install via `snap run code --install-extension <id>` (NOT `snap/bin/code --install-extension` — that path is a broken symlink on Ubuntu).

Core extensions:
- `vscjava.vscode-java-pack` — Java language support (includes Gradle, Maven, debugger)
- Kotlin syntax extension — verify current publisher/ID on marketplace

## Pitfalls

1. **`snap/bin/code` is a broken symlink** — always use `snap run code` instead. The symlink exists but does not resolve.
2. **`sdkmanager` may warn about duplicate `cmdline-tools/latest`** — the first install creates it; subsequent `sdkmanager --install cmdline-tools;latest` will create `latest-N` instead. This is harmless.
3. **Kotlin extension IDs change** — publisher names on the VS Code marketplace shift; verify before installing. Use the marketplace search to confirm the current ID.
4. **Emulator requires KVM** — headless Linux without GPU will have slow/no emulator. For CI or headless servers, use `adb` with a physical device or an x86 emulator image.
5. **`ANDROID_HOME` vs `ANDROID_SDK_ROOT`** — set both; some tools check one, others check the other. They should point to the same path.

## See Also

- `references/vscode-extensions.md` — verified VS Code extension IDs and alternatives
- `references/avd-setup.md` — creating Android Virtual Devices from the CLI
