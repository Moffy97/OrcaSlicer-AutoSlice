"""Purpose-based, single-nozzle Orca profile planner. Python 3.10+, stdlib only.

Experimental CLI prototype, not a replacement Orca GUI or a strength simulator.
"""
import argparse, hashlib, json, math, re, struct, subprocess
from pathlib import Path

PURPOSES = {
    'everyday': (3, 3, 3, 20., 1., .8),
    'finish': (3, 4, 3, 15., 1.2, 1.),
    'strong': (5, 4, 4, 40., 1.2, 1.2),
    'draft': (2, 2, 2, 10., .6, .6),
}
RATIOS = {'everyday': (.4, .5, .75), 'finish': (.25, .3, .35),
          'strong': (.35, .45, .55), 'draft': (.45, .6, .8)}
MODES = ('detail', 'balanced', 'fast')

def number(value):
    if isinstance(value, list):
        if len(value) != 1: raise ValueError('Prototype supports exactly one physical nozzle')
        value = value[0]
    value = float(value)
    if not math.isfinite(value): raise ValueError('Non-finite profile value')
    return value

def stl_box(path):
    data = Path(path).read_bytes(); vertices = []
    if len(data) >= 84 and 84 + struct.unpack_from('<I', data, 80)[0] * 50 == len(data):
        for offset in range(84, len(data), 50):
            vertices.extend(struct.unpack_from('<3f', data, offset + 12 + i * 12) for i in range(3))
    else:
        for line in data.decode('ascii').splitlines():
            fields = line.split()
            if len(fields) == 4 and fields[0] == 'vertex': vertices.append(tuple(map(float, fields[1:])))
    if not vertices or any(not math.isfinite(v) for xyz in vertices for v in xyz): raise ValueError('Invalid STL vertices')
    box = tuple(max(v[i] for v in vertices) - min(v[i] for v in vertices) for i in range(3))
    if min(box) <= 0: raise ValueError('STL must have positive X/Y/Z extent')
    return box

def align(value, lower, upper, step):
    if not 0 < lower <= upper or step < 0: raise ValueError('Invalid layer bounds/grid')
    if not step: return min(upper, max(lower, value))
    lo = math.ceil((lower - 1e-9) / step) * step
    hi = math.floor((upper + 1e-9) / step) * step
    if lo > hi + 1e-9: raise ValueError('No valid height on the supplied Z grid')
    return min(hi, max(lo, math.floor((value + 1e-9) / step) * step))

def candidates(machine, process, filament, box, purpose='everyday', budget=3, z_step=0.):
    if purpose not in PURPOSES or not 1 <= budget <= 5: raise ValueError('Invalid purpose/budget')
    if min(box) <= 0 or any(not math.isfinite(v) for v in (*box, z_step)) or z_step < 0: raise ValueError('Invalid geometry/grid')
    nozzle = number(machine['nozzle_diameter'])
    lower = number(machine['min_layer_height']); upper = number(machine['max_layer_height'])
    if not 0 < lower <= upper <= nozzle: raise ValueError('Explicit valid nozzle/layer bounds are required')
    flow = number(filament['filament_max_volumetric_speed'])
    if flow <= 0: raise ValueError('Explicit positive filament volumetric limit required')
    walls, top, bottom, density, top_mm, bottom_mm = PURPOSES[purpose]
    x, y, z = box; area = max(0., x - 2 * walls * nozzle) * max(0., y - 2 * walls * nozzle)
    wall_speed = number(process.get('outer_wall_speed', 80))
    infill_speed = number(process.get('sparse_infill_speed', 150))
    solid_speed = number(process.get('top_surface_speed', 80))
    if min(wall_speed, infill_speed, solid_speed) <= 0: raise ValueError('Positive absolute speeds are required')
    output = {}; total = 0
    for mode, ratio in zip(MODES, RATIOS[purpose]):
        base = align(nozzle * ratio, lower, upper, z_step)
        heights = {base}
        for value in [nozzle * .5, nozzle * .75] + [upper / n for n in range(1, int(upper / lower + 1e-8) + 1)]:
            if lower - 1e-8 <= value <= base + 1e-8: heights.add(align(value, lower, base, z_step))
        trials = []
        for height in sorted(heights, reverse=True):
            group = max(1, math.floor((upper + 1e-8) / height))
            tops = max(top, math.ceil((top_mm - 1e-8) / height)); bottoms = max(bottom, math.ceil((bottom_mm - 1e-8) / height))
            layers = math.ceil(z / height); shells = min(layers, tops + bottoms)
            wall_length = 2 * (x + y) * walls * layers
            solid_length = area * shells / nozzle
            fill_length = area * max(0., layers - shells) * density / (100 * nozzle * group)
            score = sum(max(length / speed, length * nozzle * h / flow) for length, speed, h in
                        [(wall_length, wall_speed, height), (solid_length, solid_speed, height), (fill_length, infill_speed, height * group)])
            cfg = dict(process)
            cfg.update(name=f'AutoSlice {mode} {height:.6f}', type='process', from_='user')
            cfg.pop('from_', None); cfg['from'] = 'user'
            cfg.update(layer_height=str(height), initial_layer_print_height=str(align(number(process.get('initial_layer_print_height', height)), lower, upper, z_step)),
                       wall_loops=str(walls), top_shell_layers=str(tops), bottom_shell_layers=str(bottoms),
                       top_shell_thickness=str(top_mm), bottom_shell_thickness=str(bottom_mm),
                       sparse_infill_density=f'{density:g}%', infill_combination='1', infill_combination_max_layer_height=str(upper))
            trials.append(dict(height=height, infill_every=group, screening_score=score, process=cfg))
        total += len(trials); trials.sort(key=lambda t: t['screening_score'])
        selected = trials[:min(2, budget)]
        if trials:
            diverse = next((t for t in trials if t['infill_every'] != trials[0]['infill_every']), None)
            if diverse and len(selected) < budget and diverse not in selected: selected.append(diverse)
        for trial in trials:
            if len(selected) >= budget: break
            if trial not in selected: selected.append(trial)
        output[mode] = selected
    return dict(purpose=purpose, logical_candidates=total, modes=output,
                note='Scores are coarse bounding-box estimates for screening only. Only native G-code provides measured estimates. Infill grouping is a ceiling where geometry allows; no strength certification.')

def metrics(path):
    text = Path(path).read_text(encoding='utf-8', errors='replace')
    match = re.search(r'^; estimated printing time \(normal mode\) = (.+)$', text, re.M)
    if not match: raise ValueError('Native print time absent')
    units = {'d': 86400, 'h': 3600, 'm': 60, 's': 1}
    seconds = sum(float(v) * units[u] for v, u in re.findall(r'([\d.]+)\s*([dhms])', match.group(1)))
    if seconds <= 0: raise ValueError('Invalid native estimate')
    return dict(seconds=seconds, time=match.group(1), total_layers=len(re.findall(r'^;LAYER_CHANGE\s*$', text, re.M)))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ('machine', 'process', 'filament', 'model', 'output'): parser.add_argument('--' + key, required=True, type=Path)
    parser.add_argument('--purpose', choices=PURPOSES, default='everyday'); parser.add_argument('--budget', type=int, default=3)
    parser.add_argument('--z-step', type=float, default=0.); parser.add_argument('--orca', type=Path)
    args = parser.parse_args()
    read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
    plan = candidates(read(args.machine), read(args.process), read(args.filament), stl_box(args.model), args.purpose, args.budget, args.z_step)
    args.output.mkdir(parents=True, exist_ok=True)
    native = {}; winners = {}; jobs = 0
    for mode, trials in plan['modes'].items():
        measured = []
        for index, trial in enumerate(trials):
            cfg = trial['process']; canonical = {k:v for k,v in cfg.items() if k not in ('name','print_settings_id')}
            # A custom G-code expression may depend on preset identity; retain its key then.
            if any('print_settings_id' in str(v) for k,v in cfg.items() if 'gcode' in k): canonical = cfg
            key = hashlib.sha256(json.dumps(canonical,sort_keys=True).encode()).hexdigest()
            folder = args.output / key[:16]; folder.mkdir(exist_ok=True)
            profile = folder / 'process.json'; profile.write_text(json.dumps(cfg,indent=2),encoding='utf-8')
            trial['profile'] = str(profile); trial.pop('process')
            if args.orca:
                if key not in native:
                    command = [str(args.orca.resolve()), '--datadir', str((args.output/'orca-data').resolve()), '--load-settings', str(args.machine.resolve())+';'+str(profile.resolve()),
                               '--load-filaments', str(args.filament.resolve()), '--arrange','0','--slice','0','--outputdir',str(folder.resolve()),str(args.model.resolve())]
                    with (folder/'slice.log').open('w',encoding='utf-8') as log:
                        result = subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,timeout=1800)
                    gcodes = list(folder.glob('*.gcode')); jobs += 1
                    if result.returncode or not gcodes: native[key] = {'error':'Native slicing failed; inspect local slice.log'}
                    else: native[key] = dict(gcode=str(gcodes[0]),**metrics(gcodes[0]))
                trial['native'] = native[key]
                if 'seconds' in native[key]: measured.append(trial)
        if measured: winners[mode] = min(measured,key=lambda t:t['native']['seconds'])
    plan['native_jobs'] = jobs; plan['winners'] = winners
    (args.output/'comparison.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
    print(f'Logical candidates: {plan["logical_candidates"]}; native jobs: {jobs}; report: {args.output/"comparison.json"}')
    if args.orca and len(winners) != len(MODES): raise SystemExit('Some modes have no valid native result; inspect comparison.json')

if __name__ == '__main__': main()
