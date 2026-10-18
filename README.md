# OrcaSlicer AutoSlice — experimental purpose-based planner

[English](README.md) · [Italiano](README_IT.md)

Choose how a part will be used, screen layer/shell/infill combinations cheaply, then ask OrcaSlicer to slice only a few promising candidates. This separate project is for **ordinary single-nozzle printers**, without INDX, KlipperScreen or a printer connection.

**Current status: functional Python CLI prototype, not a finished OrcaSlicer GUI fork or Windows installer.** The INDX edition remains a separate project. This repository does not claim universal compatibility or mechanical-strength certification.

## Implemented

- Everyday, surface finish, more material for strength, and draft purposes.
- Detail / balanced / fast candidates from the selected nozzle's explicit minimum/maximum layer limits.
- Wall count, top/bottom layer count and physical thickness, infill density and infill grouping.
- Bounding-box, volumetric-flow and path-length screening before native slicing: up to 3 finalists per mode by default, maximum 5.
- Native CLI execution only when `--orca` is supplied. Identical process candidates across modes share a completed native job.
- Native print time and total layer count from G-code; best result per mode in `comparison.json`.
- Explicit optional Z grid; no SV08 Max mechanics are assumed. Machine and filament presets are preserved.

## Run

Python 3.10+, no extra packages. Export fully resolved **single-nozzle** machine, process and filament JSON presets from your compatible Orca version. The machine must declare `nozzle_diameter`, `min_layer_height`, `max_layer_height`; the filament must declare a positive `filament_max_volumetric_speed`. The prototype currently accepts STL and absolute numeric speed settings.

```sh
python autoslice.py --machine machine.json --process process.json --filament filament.json --model part.stl --output runs/example --purpose everyday
```

This plans and exports finalists only. Add `--orca /absolute/path/to/orca-slicer.exe` (or the executable on your platform) to obtain actual native slicing results. `--budget 3` controls finalists per mode. `--z-step` is optional and must come from your own verified machine configuration. Outputs stay in the selected directory; nothing is uploaded, sent to a printer or printed.

Open the selected G-code in Orca for review. A native failure is reported and never presented as a successful estimate. The report retains the actual jobs and failure information.

## What the fast estimate cannot know

Bounding boxes approximate geometry; they do not describe holes, thin features, support topology, cooling or travel. Screening can miss a faster candidate. Infill grouping is only a maximum where Orca's geometry checks permit it; top/bottom and bridges may still print every layer. More walls/material is a structural preference, not a verified load rating. No AI service, paid API or strength simulation is involved.

## Related work and scope

Orca already provides [infill combination](https://github.com/OrcaSlicer/OrcaSlicer/wiki/strength_settings_advanced), variable layer height and manual process controls. [PrintWise](https://github.com/distractable2/PrintWise) analyzes models and generates starting profiles. [orca-auto](https://github.com/3DCreationsByChad/orca-auto) automates CLI jobs. These overlap with parts of the idea; this project focuses on purpose-based preselection plus a bounded native comparison. A search on 18 October 2026 did not identify an exact complete equivalent; that is not proof of novelty.

## Development

`python -m unittest -v` runs the focused planner tests. Next: native Orca GUI integration, richer geometry analysis, preview/comparison UI and broader printer validation. No ready-to-install GUI download is advertised yet.

Community prototype, unofficial. AGPL-3.0; see LICENSE. OrcaSlicer itself remains under its upstream license. No third-party optimizer source is incorporated.

Native validation: a 10 mm single-nozzle cube produced all three modes from 15 logical candidates and 7 distinct native jobs (duplicates reused). Detail 4m42s/55 layers, balanced 3m39s/42 layers, fast 2m54s/32 layers. Test-specific estimates only. STL coordinates must already fit the selected bed; the prototype deliberately preserves positioning and does not auto-arrange.
