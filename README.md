# OrcaSlicer AutoSlice

[English](README.md) · [Italiano](README_IT.md)

**Native Orca GUI and Windows installer — 0.2.0 preview.** For ordinary single-nozzle FFF printers, without INDX, KlipperScreen or a printer connection.

## Download and use

Open [Releases](https://github.com/Moffy97/OrcaSlicer-AutoSlice/releases) and download `OrcaSlicer-AutoSlice-0.2.0-preview-Setup-x64.exe` from Assets (preview releases may require opening the releases list). A portable ZIP and complete corresponding source patch are also provided. This is an unofficial, unsigned community preview.

1. Install for your Windows user. The default folder is `%LOCALAPPDATA%\Programs\OrcaSlicer-AutoSlice`. It coexists with official Orca and the INDX/SV08 Max editions.
2. At first launch choose your actual printer in Orca's setup wizard, or import your own compatible presets. No fictional universal printer profile is preselected. Data lives in the separate `dati` folder; upgrades/uninstall preserve it. Existing profiles in other editions are not imported automatically.
3. Select one physical nozzle, one filament and a model on the current plate. Check the printer's min/max layer limits and the filament's positive volumetric-flow limit. Remove local layer/structure overrides and variable-height profiles before using the global comparison.
4. Click **Auto Slice**, next to **Slice plate**. Choose a purpose: everyday, surface finish, a loaded part, or shortest time. The preview's new controls currently use Italian labels: Uso quotidiano, Finitura e dettagli, Pezzo sollecitato, Minor tempo possibile.
5. The three **Dettaglio / Equilibrato / Veloce** cards show native time, grams, total layers, wall/surface height and maximum infill grouping. Choose a card and confirm to open its cached G-code in native Preview. Choosing a card does not slice again.
6. Cancel restores the original process settings, including unsaved process edits. During a job, cancellation waits for that finalist to finish before restoring. Normal manual slicing remains available beside Auto Slice.

## What it changes

The selected purpose sets wall count, Gyroid infill density, minimum top/bottom thickness and shell counts. Layer candidates use the current nozzle and machine limits. Combined infill can be taller than the perimeter layer, including with a single nozzle. Grouping is a maximum: native geometry checks determine where it is actually possible. First-layer height is retained within the machine bounds. Printer motion limits, temperatures, calibration, filament flow limit, custom G-code and line-width settings are retained.

A cheap bounding-box/path/flow estimate screens candidates before slicing. At most **3 finalists per mode** enter native slicing; identical effective process configurations share their result across modes. The dialog caches G-code, native statistics and process settings. The comparison locks project inputs so cached results stay valid. Changing purpose starts a new bounded comparison. Times and grams come from native G-code, never from the coarse screening score.

The three mode names express a quality/height envelope. Depending on the model and flow limit they can share the same winning configuration. This is not an exhaustive global optimizer or a strength simulation. More walls do not certify a load rating. Verify material, orientation, supports and the Preview before printing.

## Scope

This GUI preview supports **one physical nozzle and one project filament**. Multiple tools/materials, local structure overrides and variable-height profiles are deliberately rejected with an explanation. The INDX edition remains separate. Automatic mode may choose a different layer height from the sidebar; ordinary slicing retains the manual choice. No SV08 Max mechanical step size is assumed. This edition does not flash firmware, configure hardware, sync KlipperScreen or send/print jobs automatically.

The underlying engine shares source with the INDX fork, whose controls are hidden for ordinary printer profiles. The complete corresponding patch includes that common engine. It is not a plugin for the unmodified official executable. Existing native version metadata can still identify the shared fork as `2.5.0-indx`; this package's version is in VERSION.json.

## Source and rebuild

AGPL-3.0, see LICENSE. UPSTREAM.json pins the upstream commit; `python prepare_source.py` creates a new upstream checkout and applies the complete binary patch. Follow upstream's dependency/toolchain build instructions in that checkout. The GUI implementation is `src/slic3r/GUI/AutoSliceWorkspace.ipp`, included by IndxSync.cpp; MainFrame.cpp adds the button. Native cache restoration uses PartPlate. The installer recipe is `windows-installer.iss`; see WINDOWS_INSTALLER.md. SHA256SUMS covers repository files and the release has separate checksums for downloads.

The earlier stdlib Python 3.10+ CLI remains in `autoslice.py`. `python -m unittest -v` runs its focused tests. CLI use: `python autoslice.py --machine machine.json --process process.json --filament filament.json --model part.stl --output runs/example --purpose everyday --orca /path/to/orca-slicer.exe`. Export fully resolved compatible presets. STL coordinates must already fit the bed; the CLI preserves placement. Optional `--z-step` is explicit CLI-only verified metadata; the GUI assumes no grid.

## Related work

Orca already offers infill combination and variable layer height. [PrintWise](https://github.com/distractable2/PrintWise) analyzes models/profiles, and [orca-auto](https://github.com/3DCreationsByChad/orca-auto) automates CLI jobs. This project combines purpose-based preselection with bounded native comparison. It makes no novelty claim and incorporates no third-party optimizer source.
