# Avalonia 11 API Changes (from WPF / older templates)

Discovered during AvaloniaTest project build debugging (2026-05-23).

## Property Renames

### Window Properties
- `ResizeMode="NoResize"` → `CanResize="False"`
- `WindowStartupLocation` — unchanged

### Theme Variant
- `AppThemeVariant.Light` / `AppThemeVariant.Dark` → `ThemeVariant.Light` / `ThemeVariant.Dark`
- `App.Current?.RequestedThemeVariant` — unchanged

### Font Styling
- `FontWeights.Normal` / `FontWeights.Bold` → `FontWeight.Normal` / `FontWeight.Bold`
- `FontWeight` is an enum, not a static class

## Removed APIs
- `AppBuilder.WithDeveloperTools()` — removed in Avalonia 11
- `Window.OnClosed(EventArgs)` override — Avalonia uses `Closed` event, not virtual method override

## Namespace Fixes
- `IBrush` — use `using Avalonia.Media;` then reference as `IBrush`, NOT `Avalonia.IBrush`
- `Window` — use `using Avalonia.Controls;` in viewmodel files that reference Window types
- `FontWeight` — from `Avalonia.Media` namespace, not `Avalonia.Media.FontWeights`

## Dialog Pattern
- `AboutDialog.Close(true)` or `Close(false)` — bare `Close()` doesn't set result
- Command binding with `CommandParameter="{Binding RelativeSource={RelativeSource AncestorType=Window}}"` passes owner window to viewmodels

## Build Error Patterns

### AVLN1001 — Invalid XAML
Caused by: missing namespace declarations, invalid property names, mismatched XML tags

### AVLN2000 — Property Resolution Failure
Caused by: WPF property names Avalonia renamed (e.g., `ResizeMode`), wrong control type properties

### FileNotFoundException on AvaloniaResource
Caused by: csproj `<AvaloniaResource Include="...">` references files that don't exist on disk

## Fix: Program.cs Template
```csharp
public static AppBuilder BuildAvaloniaApp()
    => AppBuilder.Configure<App>()
        .UsePlatformDetect()
        .WithInterFont()
        .LogToTrace();
```
