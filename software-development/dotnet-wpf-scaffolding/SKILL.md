---
name: dotnet-wpf-scaffolding
description: "Create and scaffold .NET WPF projects from scratch, especially on non-Windows hosts where dotnet new templates are unavailable."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, windows, macos]
metadata:
  hermes:
    tags: [dotnet, wpf, windows, scaffolding, visual-studio-code, .net-8]
---

# .NET WPF Project Scaffolding

Create and scaffold .NET WPF projects from scratch — especially on non-Windows hosts where `dotnet new wpf` templates are unavailable.

## When to Use

- Creating a new WPF project on a Linux/macOS development host
- The `dotnet new wpf` command fails because Windows SDK targets are missing
- Need to manually create WPF project files (csproj, sln, xaml)
- Setting up a WPF project for VS Code development

## Why This Skill Exists

WPF is Windows-only. The .NET SDK on Linux/macOS does not include `Microsoft.NET.Sdk.WindowsDesktop` targets. Running `dotnet new wpf` on non-Windows **succeeds silently but produces a broken project** that fails to build. You must scaffold WPF projects manually on non-Windows hosts.

## Steps

### 1. Create Project Directory

```
<project>/
├── <Project>.csproj
├── <Project>.sln          (if creating a new solution)
├── App.xaml / App.xaml.cs
├── MainWindow.xaml / .cs
└── (optional) Themes/
```

### 2. Create .csproj (minimum)

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>WinExe</OutputType>
    <TargetFramework>net8.0-windows</TargetFramework>
    <Nullable>enable</Nullable>
    <UseWPF>true</UseWPF>
  </PropertyGroup>
</Project>
```

Key properties:
- `OutputType` = `WinExe` (not `Library`)
- `TargetFramework` must end in `-windows` (e.g., `net8.0-windows`)
- `UseWPF` = `true` enables WPF SDK imports
- `Nullable` = `enable` for nullable reference types

### 3. Create App.xaml

```xml
<Application x:Class="<Namespace>.App"
             xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             StartupUri="MainWindow.xaml">
</Application>
```

### 4. Create App.xaml.cs

```csharp
using System.Windows;

namespace <Namespace>
{
    public partial class App : Application
    {
        protected override void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);
            // Theme detection, resource loading, etc.
        }
    }
}
```

### 5. Create MainWindow.xaml + .cs

Standard WPF window with code-behind. Use `x:Class` to link XAML to code-behind.

### 6. Create .sln (if standalone)

See `references/sln-format.md` for the solution file format. Generate a GUID for the project key with `New-Guid` (PowerShell) or `uuidgen` (Linux).

### 7. Create .vscode/ Configuration (for VS Code users)

See `templates/vscode-dotnet-wpf.json` in this skill's files.

### 8. Build & Run (on Windows)

```bash
dotnet restore
dotnet build
dotnet run --project <Project>/<Project>.csproj
```

For hot reload:
```bash
dotnet watch run --project <Project>/<Project>.csproj
```

## Pitfalls

1. **Never run `dotnet new wpf` on Linux/macOS** — it will succeed but produce a broken project. Always scaffold manually.
2. **`dotnet sln add` fails on Linux** for WPF projects — create the .sln file manually.
3. **Target framework must be `netX.0-windows`** — not just `netX.0`. The `-windows` suffix is required for WPF.
4. **`StartupObject` property** — if App class isn't in the default namespace, add `<StartupObject>Namespace.App</StartupObject>` to the csproj.
5. **XAML namespace mapping** — `x:Class` in XAML must match the fully qualified class name in code-behind.
6. **VS Code debugging** — WPF debugging requires `coreclr` type in launch.json, not `clr`. Use `program` pointing to the compiled DLL.

## Theme Detection Pattern

For themed apps, detect Windows light/dark mode in `App.OnStartup`:

```csharp
using Microsoft.Win32;

private static bool DetectDarkMode()
{
    using var key = Registry.CurrentUser.OpenSubKey(
        @"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize");
    return key?.GetValue("AppsUseLightTheme") is int v && v == 0;
}
```

Then load `DarkTheme.xaml` or `LightTheme.xaml` as a merged resource dictionary.

## See Also

- `templates/vscode-dotnet-wpf.json` — VS Code workspace config template
- `references/sln-format.md` — .sln file format reference
