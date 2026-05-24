---
name: avalonia-development
description: Building Avalonia UI applications — scaffolding, debugging build errors, and API migration from WPF templates.
---

# Avalonia UI Development

Building Avalonia UI applications (MVVM, XAML, theming) — scaffolding, debugging, and migration from WPF templates.

## When to Use
- Creating new Avalonia projects
- Fixing build errors in Avalonia apps
- Migrating WPF/XAML knowledge to Avalonia
- Debugging Avalonia XAML compilation errors

## Common Pitfalls

### XAML Compilation Errors (AVLN1001/AVLN2000)
Avalonia parses XAML at build time — invalid XAML fails the entire build. When you see `AVLN1001` or `AVLN2000`:
1. Check the reported file and line number
2. Verify all namespace declarations (`xmlns:local="using:NamespaceName"`)
3. Verify all property names exist on the target type (Avalonia renames properties from WPF)
4. Check for mismatched/open tags (e.g., `ItemsControl.ItemsPanel` end tag must be `</ItemsControl.ItemsPanel>`, not `</ItemsControl.ItemTemplate>`)

### Avalonia 11 API Changes from WPF Templates
The `dotnet new avalonia.mvvm` template uses outdated API names:

| WPF / Old Avalonia | Avalonia 11 |
|---|---|
| `ResizeMode="NoResize"` | `CanResize="False"` |
| `AppThemeVariant` | `ThemeVariant` |
| `WithDeveloperTools()` | Removed — use `WithInterFont()` + `LogToTrace()` |
| `OnClosed(EventArgs)` override | Use `Closed += ...` event |
| `Avalonia.IBrush` | Just `IBrush` (with `using Avalonia.Media;`) |
| `FontWeights` in `Avalonia.Media` | `FontWeight` enum, use `FontWeight.Normal` / `FontWeight.Bold` directly |

### Missing Assets
Avalonia's build task (`GenerateAvaloniaResourcesTask`) fails if any `AvaloniaResource` referenced in the csproj doesn't exist on disk. Always verify assets exist before building.

### Icon Files
Avalonia expects `.ico` files for `ApplicationIcon` and `Icon` properties. PNG files alone won't work for the icon field. Use a proper ICO format (not just a renamed PNG).

### AboutDialog.Close()
In Avalonia, `Window.Close()` without arguments doesn't return a result. Use `Close(true)` or `Close(false)` when you need the dialog result.

## Workflow
1. Create project: `dotnet new avalonia.mvvm -n ProjectName`
2. Verify build immediately: `dotnet build`
3. Fix any template-to-runtime API mismatches before adding features
4. Add assets to `Assets/` directory
5. Update csproj `AvaloniaResource` includes if adding new asset directories
6. Build again before committing

## Support Files
- `references/avalonia-11-api-changes.md` — Detailed Avalonia 11 API migration notes
