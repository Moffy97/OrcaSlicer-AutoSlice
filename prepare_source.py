"""Reconstruct the exact modified Orca source. No toolchain or firmware install."""
from pathlib import Path
import json,subprocess,sys

root=Path(__file__).resolve().parent
meta=json.loads((root/'UPSTREAM.json').read_text())
target=root/'upstream-orca'
if target.exists():raise SystemExit('upstream-orca already exists; use a new directory to preserve local work.')
subprocess.run(['git','clone','--config','core.autocrlf=false','--no-checkout',meta['url'],str(target)],check=True)
subprocess.run(['git','-C',str(target),'checkout','--detach',meta['commit']],check=True)
subprocess.run(['git','-C',str(target),'apply','--check',str(root/'OrcaSlicer-AutoSlice.patch')],check=True)
subprocess.run(['git','-C',str(target),'apply',str(root/'OrcaSlicer-AutoSlice.patch')],check=True)
print('Source prepared:',target)
print('Build using the official OrcaSlicer dependency/toolchain instructions. No firmware was changed.')
