# IntelliSense Configuration for mingw-w64 Cross-Compilation

## c_cpp_properties.json

Place in `.vscode/c_cpp_properties.json` or `~/.config/Code/User/c_cpp_properties.json`:

### 64-bit target (PE32+)
```json
{
    "configurations": [
        {
            "name": "Windows-x86_64-MinGW",
            "includePath": [
                "${workspaceFolder}/**",
                "/usr/x86_64-w64-mingw32/include/**",
                "/usr/include/**"
            ],
            "defines": ["_WIN32", "NDEBUG"],
            "compilerPath": "/usr/bin/x86_64-w64-mingw32-gcc",
            "cStandard": "c17",
            "cppStandard": "c++17",
            "intelliSenseMode": "linux-x64",
            "configurationProvider": "ms-vscode.cmake-tools",
            "browse": {
                "path": [
                    "${workspaceFolder}/**",
                    "/usr/x86_64-w64-mingw32/**",
                    "/usr/include/**"
                ],
                "limitSymbolsToIncludedHeaders": true
            }
        }
    ],
    "version": 4
}
```

### 32-bit target (PE32)
```json
{
    "configurations": [
        {
            "name": "Windows-i686-MinGW",
            "includePath": [
                "${workspaceFolder}/**",
                "/usr/i686-w64-mingw32/include/**",
                "/usr/include/**"
            ],
            "defines": ["_WIN32", "NDEBUG"],
            "compilerPath": "/usr/bin/i686-w64-mingw32-gcc",
            "cStandard": "c17",
            "cppStandard": "c++17",
            "intelliSenseMode": "linux-x64",
            "configurationProvider": "ms-vscode.cmake-tools",
            "browse": {
                "path": [
                    "${workspaceFolder}/**",
                    "/usr/i686-w64-mingw32/**",
                    "/usr/include/**"
                ],
                "limitSymbolsToIncludedHeaders": true
            }
        }
    ],
    "version": 4
}
```

## Key Fields Explained

| Field | Value | Purpose |
|-------|-------|---------|
| `compilerPath` | `/usr/bin/x86_64-w64-mingw32-gcc` | Tells IntelliSense which compiler to use for include paths and macros |
| `intelliSenseMode` | `linux-x64` | Use `linux-x64` (NOT `linux-gcc-x64`) — the mingw compiler reports itself as a Linux GCC |
| `defines` | `["_WIN32"]` | Define Windows target macros for conditional compilation |
| `configurationProvider` | `ms-vscode.cmake-tools` | Defer to CMake's detected compiler for IntelliSense |
| `browse.path` | mingw sysroot + workspace | Enables symbol navigation into Windows SDK headers |

## Common Issues

### IntelliSense shows errors for Windows headers
- Ensure `browse.path` includes the mingw sysroot (`/usr/x86_64-w64-mingw32/include/`)
- Verify `compilerPath` points to the correct cross-compiler
- Reload VS Code window after changing `c_cpp_properties.json`

### Wrong target architecture detected
- Check that `compilerPath` matches the intended target (x86_64 vs i686)
- The `intelliSenseMode` should be `linux-x64` for both — it controls the host platform, not the target

### Missing Windows SDK headers
- Ensure `mingw-w64-x86_64-dev` (or `mingw-w64-i686-dev`) is installed
- Check that `/usr/x86_64-w64-mingw32/include/` exists and is populated
