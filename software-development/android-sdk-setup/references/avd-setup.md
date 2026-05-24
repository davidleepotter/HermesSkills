# Android Virtual Device (AVD) Setup

Create and manage Android emulators from the command line.

## Prerequisites

KVM must be available for hardware acceleration:

```bash
sudo apt-get install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils
sudo adduser $USER kvm
```

## List Available System Images

```bash
avdmanager list sdk --include_installed 2>/dev/null | grep "system-images"
# or
sdkmanager --list --include_metadata 2>/dev/null | grep "system-images"
```

Common system image IDs:
- `system-images;android-35;google_apis;x86_64` — Android 15, Google APIs, x86_64
- `system-images;android-35;default;x86_64` — Android 15, stock, x86_64
- `system-images;android-34;google_apis;x86_64` — Android 14, Google APIs, x86_64

## Create an AVD

```bash
# List available devices
avdmanager list device

# Create AVD (replace with your chosen device ID)
avdmanager create avd \
  -n "Pixel_6" \
  -k "system-images;android-35;google_apis;x86_64" \
  -d "pixel_6" \
  --force
```

## Launch the Emulator

```bash
export ANDROID_HOME="$HOME/Android/Sdk"
export PATH="$PATH:$ANDROID_HOME/emulator"

emulator -avd Pixel_6 -no-snapshot -no-window &
```

Key flags:
- `-no-snapshot` — fresh boot (no saved state)
- `-no-window` — headless mode (for servers)
- `-gpu swiftshader_indirect` — software GPU rendering

## Verify ADB Connection

```bash
adb devices
# Should show: emulator-5554    device
```

## Pitfalls

1. **KVM not available** — emulator will fall back to software rendering, which is very slow. Check with `kvm-ok` or `lsmod | grep kvm`.
2. **`avdmanager` requires `cmdline-tools` in PATH** — ensure `$ANDROID_HOME/cmdline-tools/latest/bin` is on PATH.
3. **Headless emulator** — on servers without a display, use `-no-window` and connect via `adb`.
4. **Emulator port conflicts** — if multiple emulators run, they use ports 5554, 5556, 5558, etc. (even ports for ADB, odd for console).
