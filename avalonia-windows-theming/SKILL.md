---
name: avalonia-windows-theming
description: "Scaffold an Avalonia MVVM desktop app with Windows Fluent theming, About dialog, icon/splash assets, git + .sln setup."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Avalonia, .NET, MVVM, Windows, Theming, Desktop]
    related_skills: [github-pr-workflow]
---

# Avalonia Windows-Themed MVVM Scaffold

Scaffold a fully working Avalonia MVVM desktop app with Windows Fluent theming, About dialog, custom icon/splash, git + .sln setup.

## Prerequisites

- .NET 8 SDK
- `dotnet new -i Avalonia.Templates`
- Authenticated with GitHub (`gh auth status`)

## Scaffolding Steps

### 1. Create Project

```bash
dotnet new avalonia.mvvm -n <AppName>
cd <AppName>
rm -rf <AppName>8  # remove duplicate template dir
rm -rf bin obj
```

### 2. Update `.csproj`

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>WinExe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ApplicationManifest>app.manifest</ApplicationManifest>
    <AvaloniaUseCompiledBindingsByDefault>true</AvaloniaUseCompiledBindingsByDefault>
    <ApplicationIcon>Assets\icon.ico</ApplicationIcon>
  </PropertyGroup>

  <ItemGroup>
    <AvaloniaResource Include="Assets\**" />
  </ItemGroup>

  <ItemGroup>
    <PackageReference Include="Avalonia" Version="11.2.1" />
    <PackageReference Include="Avalonia.Desktop" Version="11.2.1" />
    <PackageReference Include="Avalonia.Win32" Version="11.2.1" />
    <PackageReference Include="Avalonia.Themes.Fluent" Version="11.2.1" />
    <PackageReference Include="Avalonia.Fonts.Inter" Version="11.2.1" />
    <PackageReference Include="CommunityToolkit.Mvvm" Version="8.4.1" />
  </ItemGroup>
</Project>
```

### 3. Update `App.axaml` — add `local` namespace

```xml
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:local="using:<AppName>"
             x:Class="<AppName>.App"
             RequestedThemeVariant="Default">
    <Application.DataTemplates>
        <local:ViewLocator/>
    </Application.DataTemplates>
    <Application.Styles>
        <FluentTheme />
    </Application.Styles>
</Application>
```

### 4. Update `Program.cs` — remove `WithDeveloperTools`

```csharp
using Avalonia;
using System;

namespace <AppName>;

sealed class Program
{
    [STAThread]
    public static void Main(string[] args) => BuildAvaloniaApp()
        .StartWithClassicDesktopLifetime(args);

    public static AppBuilder BuildAvaloniaApp()
        => AppBuilder.Configure<App>()
            .UsePlatformDetect()
            .WithInterFont()
#if DEBUG
            .LogToTrace();
#else
            ;
#endif
}
```

### 5. Create `Assets/icon.ico` and `Assets/splash.png`

Run the Python script at `scripts/create-avalonia-assets.py` (see below) or use the embedded script.

### 6. Create About Dialog

**`Views/AboutDialog.axaml`:**

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        x:Class="<AppName>.Views.AboutDialog"
        Icon="/Assets/icon.ico"
        Title="About"
        Width="420"
        MinWidth="360"
        Height="340"
        MinHeight="280"
        WindowStartupLocation="CenterOwner"
        CanResize="False">
  <StackPanel Margin="32,24" Spacing="16" HorizontalAlignment="Center">
    <Image Source="/Assets/icon.ico" Width="64" Height="64" Margin="0,0,0,8" />
    <TextBlock Text="<AppName>" FontSize="24" FontWeight="SemiBold"
               HorizontalAlignment="Center"
               Foreground="{DynamicResource SystemControlForegroundBaseHighBrush}" />
    <TextBlock Text="Version 1.0.0" FontSize="14"
               HorizontalAlignment="Center"
               Foreground="{DynamicResource SystemControlForegroundBaseMediumBrush}" />
    <Border BorderBrush="{DynamicResource SystemControlForegroundBaseMediumLowBrush}"
            BorderThickness="0,1,0,0" Margin="0,8" />
    <TextBlock Text="Copyright (c) 2026 <AppName>. All rights reserved."
               FontSize="13" TextWrapping="Wrap" TextAlignment="Center"
               Foreground="{DynamicResource SystemControlForegroundBaseMediumBrush}" />
    <TextBlock Text="Powered by Avalonia UI" FontSize="12"
               HorizontalAlignment="Center"
               Foreground="{DynamicResource SystemControlForegroundBaseMediumBrush}"
               Margin="0,4,0,0" />
    <Button Content="Close" HorizontalAlignment="Center" Padding="24,8"
            FontSize="14" Click="OnCloseClick" Margin="0,16,0,0" />
  </StackPanel>
</Window>
```

**`Views/AboutDialog.axaml.cs`:**

```csharp
using Avalonia.Controls;
using Avalonia.Interactivity;

namespace <AppName>.Views;

public partial class AboutDialog : Window
{
    public AboutDialog() => InitializeComponent();

    private void OnCloseClick(object? sender, RoutedEventArgs e) => Close(true);
}
```

### 7. Create About button in MainWindow

In `Views/MainWindow.axaml`, add a footer button:

```xml
<StackPanel Grid.Row="2" Margin="12,8,12,12" HorizontalAlignment="Center">
  <Button Content="About"
          Command="{Binding ShowAboutCommand}"
          CommandParameter="{Binding RelativeSource={RelativeSource AncestorType=Window}}"
          Padding="28,8" HorizontalAlignment="Center" FontSize="14" />
</StackPanel>
```

### 8. ViewModel — `ShowAbout` command

Add to `ViewModels/MainWindowViewModel.cs`:

```csharp
using Avalonia.Controls;
using CommunityToolkit.Mvvm.Input;
using <AppName>.Views;

[RelayCommand]
private void ShowAbout(Window owner)
{
    var dialog = new AboutDialog();
    dialog.ShowDialog(owner);
}
```

### 9. Build, .sln, git

```bash
dotnet build                    # verify clean
dotnet new sln -n <AppName> --force
dotnet sln add <AppName>.csproj
git init
git add -A
git commit -m "Initial commit: <AppName> with Windows theming"
gh repo create <AppName> --private --source=. --remote=origin --push
# (if repo already exists: git remote set-url origin git@github.com:<user>/<AppName>.git && git push -u origin master)
```

## Pitfalls

- **`AppThemeVariant` → `ThemeVariant`** — Avalonia 11 renamed it. Use `ThemeVariant.Light` / `ThemeVariant.Dark`.
- **`ResizeMode="NoResize"` → `CanResize="False"`** — Avalonia 11 property rename.
- **`OnClosed(EventArgs)` → remove** — Avalonia `Window` doesn't override `OnClosed`; use the `Closed` event if needed.
- **`WithDeveloperTools()` doesn't exist** — remove it from `Program.cs`.
- **`IBrush` is in `Avalonia.Media`, not `Avalonia`** — add `using Avalonia.Media;`.
- **`FontWeights` is in `Avalonia.Media`** — add `using Avalonia.Media;`.
- **`App.axaml` needs `xmlns:local`** — without it, `ViewLocator` fails to parse.
- **`ItemsControl.ItemsPanel` closing tag** — must be `</ItemsControl.ItemsPanel>` not `</ItemsControl.ItemTemplate>`.
- **`AboutDialog.Close()` must return a value** — use `Close(true)` not `Close()`.
- **`icon.ico` must exist** — csproj `<ApplicationIcon>` will fail the build if missing.

## Asset Generation Script

Run `scripts/create-avalonia-assets.py` to generate `icon.ico` and `splash.png` from pixel arrays. No external dependencies needed (pure Python stdlib PNG writer).
