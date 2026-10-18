# Windows installer

Inno Setup 6.7.3. Per-user, separate application identity and data. No profile seed, file associations or automatic launch. First run uses Orca's printer wizard. Upgrades do not write the data directory; uninstall preserves it. The portable ZIP uses the same app and separate data folder through its launcher.

Build the matching app from UPSTREAM.json plus OrcaSlicer-AutoSlice.patch. Put it in AppSource, and the corresponding repository source materials in PackageSource. Run `ISCC.exe /DAppSource=C:\build\app /DPackageSource=C:\build\package /DOutputRoot=C:\build\out windows-installer.iss`. No compiler/toolchain is downloaded by the installer.

Installer and application are unsigned experimental community software. Source and licenses are included. User profiles in other installations are never copied automatically; use Orca's import/export tools yourself. Do not select the folder of another Orca edition for installation.
