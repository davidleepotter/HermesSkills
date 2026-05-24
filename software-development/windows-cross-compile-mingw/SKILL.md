---
name: windows-cross-compile-mingw
description: "Set up Linux host for Windows cross-compilation using mingw-w64 toolchain and CMake."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [windows, cross-compile, mingw, cmake, vscode, c, cpp]
---

# Windows Cross-Compilation from Linux (mingw-w64)

Set up a Linux host to build Windows (PE32/PE32+) binaries natively using the mingw-w64 cross-compiler toolchain and CMake.

## When to Use

- Building Windows executables (.exe, .dll) from a Linux development environment
- Cross-compiling C/C++ projects targeting Windows x86_64 or i686
- Preparing a CI/CD pipeline that produces Windows binaries on Linux

## Prerequisites Check

Before starting, verify the host has:
- `sudo` access (package installation requires privilege escalation)
- `apt` or `dnf` package manager
- A terminal (not read-only)

## Step 1: Install mingw-w64 Toolchain

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y mingw-w64 mingw-w64-dev mingw-w64-tools \
    gcc-mingw-w64 g++-mingw-w64 gdb-mingw-w64 cmake make

# Verify installation
x86_64-w64-mingw32-gcc --version
x86_64-w64-mingw32-g++ --version
```

Available targets:
- **x86_64-w64-mingw32** — 64-bit Windows (PE32+)
- **i686-w64-mingw32** — 32-bit Windows (PE32)

## Step 2: Create CMake Toolchain File

**CRITICAL PITFALL:** Do NOT use `-G "MinGW Makefiles"` on Ubuntu/Debian — this generator is not shipped with the distro's cmake package. Instead, use `-G "Unix Makefiles"` with a toolchain file.

Create `cmake/toolchain-mingw64.cmake` (see `templates/toolchain-mingw64.cmake`):

```cmake
set(CMAKE_SYSTEM_NAME Windows)
set(CMAKE_SYSTEM_PROCESSOR x86_64)
set(CMAKE_C_COMPILER x86_64-w64-mingw32-gcc)
set(CMAKE_CXX_COMPILER x86_64-w64-mingw32-g++)
set(CMAKE_RC_COMPILER x86_64-w64-mingw32-windres)
set(CMAKE_FIND_ROOT_PATH /usr/x86_64-w64-mingw32)
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
```

## Step 3: Configure CMakeLists.txt

Reference the toolchain file in your `CMakeLists.txt`:

```cmake
if(NOT DEFINED CMAKE_TOOLCHAIN_FILE)
    set(CMAKE_TOOLCHAIN_FILE "${CMAKE_CURRENT_SOURCE_DIR}/cmake/toolchain-mingw64.cmake" CACHE PATH "Toolchain file")
endif()

project(MyProject LANGUAGES C CXX)
```

Build command:
```bash
cmake -S . -B build -G "Unix Makefiles"
cmake --build build
```

## Step 4: VS Code Configuration

### Extensions to install
- `ms-vscode.cpptools` — C/C++ IntelliSense and debugging
- `ms-vscode.cmake-tools` — CMake integration
- `ms-vscode.cpp-devtools` — C++ development tools

### settings.json
Set the default compiler to the mingw-w64 cross-compiler:
```json
{
    "C_Cpp.default.compilerPath": "/usr/bin/x86_64-w64-mingw32-gcc",
    "C_Cpp.default.intelliSenseMode": "linux-mingw",
    "C_Cpp.default.configurationProvider": "ms-vscode.cmake-tools",
    "cmake.generator": "Unix Makefiles"
}
```

### c_cpp_properties.json
Configure IntelliSense include paths for the mingw-w64 sysroot (see `references/c_cpp_properties.md`).

### launch.json
Configure GDB debugger to use `x86_64-w64-mingw32-gdb` for debugging Windows binaries on Linux.

## Step 5: Verify

Build a small test project and check the output:
```bash
file build/MyApp.exe
# Should show: PE32+ executable (console) x86-64, for MS Windows
```

## Pitfalls

1. **`MinGW Makefiles` generator not found** — Ubuntu/Debian cmake does not include this generator. Always use `-G "Unix Makefiles"` with a toolchain file instead.
2. **Duplicate `main()` symbols** — Do not compile both `.c` and `.cpp` files with separate `main()` functions into the same executable target.
3. **Missing `mingw32-make`** — The `mingw-w64-tools` package does NOT install `mingw32-make`. The `make` binary on the host is sufficient when using a toolchain file.
4. **Static linking** — Add `-static-libgcc -static-libstdc++` to `CMAKE_EXE_LINKER_FLAGS` for self-contained Windows binaries.
5. **32-bit vs 64-bit** — Use `i686-w64-mingw32-*` compilers and `cmake/toolchain-mingw32.cmake` for 32-bit targets.

## References

- `templates/toolchain-mingw64.cmake` — Ready-to-use toolchain file
- `references/c_cpp_properties.md` — IntelliSense configuration details
