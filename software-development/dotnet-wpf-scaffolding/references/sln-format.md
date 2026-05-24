# .sln File Format Reference

Minimal .sln file for a single WPF project.

## Template

```
Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio Version 17
VisualStudioVersion = 17.0.31903.59
MinimumVisualStudioVersion = 10.0.40219.1
Project("{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}") = "ProjectName", "ProjectName\ProjectName.csproj", "{PROJECT_GUID}"
EndProject
Global
	GlobalSection(SolutionConfigurationPlatforms) = preSolution
		Debug|Any CPU = Debug|Any CPU
		Release|Any CPU = Release|Any CPU
	EndGlobalSection
	GlobalSection(ProjectConfigurationPlatforms) = postSolution
		{PROJECT_GUID}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
		{PROJECT_GUID}.Debug|Any CPU.Build.0 = Debug|Any CPU
		{PROJECT_GUID}.Release|Any CPU.ActiveCfg = Release|Any CPU
		{PROJECT_GUID}.Release|Any CPU.Build.0 = Release|Any CPU
	EndGlobalSection
EndGlobal
```

## GUID Generation

Generate a unique GUID for `PROJECT_GUID`:

- **PowerShell**: `New-Guid | ForEach-Object { $_.ToString('N') }`
- **Linux/macOS**: `uuidgen | tr '[:upper:]' '[:lower:]' | tr -d '-'`
- **Online**: https://www.guidgenerator.com/

## Notes

- `{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}` is the C# project type GUID (always the same)
- VisualStudioVersion 17 corresponds to Visual Studio 2022
- For VS 2019, use `VisualStudioVersion = 16.0.31115.217`
- The `MinimumVisualStudioVersion` line is informational
