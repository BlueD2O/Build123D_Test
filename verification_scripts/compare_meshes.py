from pathlib import Path
import json
import numpy as np
import trimesh

ORIG_DIR = Path("../Original_STL")
GEN_DIR = Path("../STL_Files")
OUT_DIR = Path("validation_results")
OUT_DIR.mkdir(exist_ok=True)

PARTS = {
    "Top Shell": ("RetroPad - Top Shell.stl", "test_top_shell.stl"),
    "Bottom Shell": ("RetroPad - Bottom Shell.stl", "test_bottom_shell.stl"),
    "Buttons": ("RetroPad - Button.stl", "test_buttons.stl"),
    "D-Pad": ("RetroPad - D-Pad.stl", "test_d_pad.stl"),
}

# Parts where the generated file has multiple bodies but the original has one
# The script will extract the largest single body for comparison
SINGLE_BODY_PARTS = {"Buttons"}

TOL_EXTENTS = 0.05
TOL_VOL_ABS = 1.0
TOL_SYMDIFF_PCT = 0.1  # 0.1% of original volume

def load_mesh(path):
    mesh = trimesh.load_mesh(path, force="mesh")
    if isinstance(mesh, trimesh.Scene):
        mesh = trimesh.util.concatenate(tuple(
            g for g in mesh.geometry.values()
            if isinstance(g, trimesh.Trimesh)
        ))
    return mesh

def mesh_metrics(mesh):
    return {
        "watertight": bool(mesh.is_watertight),
        "volume": float(mesh.volume) if mesh.is_watertight else None,
        "extents": [float(x) for x in mesh.extents],
        "bounds": [[float(v) for v in row] for row in mesh.bounds],
        "faces": int(len(mesh.faces)),
        "vertices": int(len(mesh.vertices)),
    }

def safe_diff_volume(a, b):
    try:
        d1 = trimesh.boolean.difference([a, b], engine="manifold", check_volume=True)
        d2 = trimesh.boolean.difference([b, a], engine="manifold", check_volume=True)

        v1 = 0.0 if d1 is None else float(d1.volume)
        v2 = 0.0 if d2 is None else float(d2.volume)
        return v1 + v2, None
    except Exception as e:
        return None, str(e)

results = []

for part_name, (orig_name, gen_name) in PARTS.items():
    orig_path = ORIG_DIR / orig_name
    gen_path = GEN_DIR / gen_name

    if not orig_path.exists() or not gen_path.exists():
        results.append({
            "part": part_name,
            "status": "MISSING_FILE",
            "original": str(orig_path),
            "generated": str(gen_path),
        })
        continue

    orig = load_mesh(orig_path)
    gen = load_mesh(gen_path)

    # For multi-body parts, extract the largest single body for comparison
    if part_name in SINGLE_BODY_PARTS:
        bodies = gen.split(only_watertight=False)
        if len(bodies) > 1:
            gen = max(bodies, key=lambda m: m.volume if m.is_watertight else 0)
            print(f"  [{part_name}] Split into {len(bodies)} bodies, using largest for comparison")

    # Center both meshes on their centroid to eliminate positional offset
    orig.vertices -= orig.centroid
    gen.vertices -= gen.centroid

    orig_m = mesh_metrics(orig)
    gen_m = mesh_metrics(gen)

    extents_delta = np.abs(np.array(orig.extents) - np.array(gen.extents))
    max_extent_delta = float(extents_delta.max())

    volume_delta = None
    volume_delta_pct = None
    if orig.is_watertight and gen.is_watertight:
        volume_delta = float(abs(orig.volume - gen.volume))
        if abs(orig.volume) > 1e-9:
            volume_delta_pct = float(100.0 * volume_delta / abs(orig.volume))

    symdiff_volume, symdiff_error = (None, "Skipped: non-watertight mesh")
    if orig.is_watertight and gen.is_watertight:
        symdiff_volume, symdiff_error = safe_diff_volume(orig, gen)

    pass_extents = max_extent_delta <= TOL_EXTENTS
    pass_volume = (volume_delta is not None and volume_delta <= TOL_VOL_ABS)
    pass_symdiff = (symdiff_volume is not None and orig.is_watertight
                    and (symdiff_volume / abs(orig.volume) * 100) <= TOL_SYMDIFF_PCT)

    overall_pass = pass_extents and pass_volume and pass_symdiff

    results.append({
        "part": part_name,
        "status": "PASS" if overall_pass else "CHECK",
        "original_metrics": orig_m,
        "generated_metrics": gen_m,
        "max_extent_delta_mm": round(max_extent_delta, 6),
        "extent_delta_xyz_mm": [round(float(v), 6) for v in extents_delta],
        "volume_delta_mm3": None if volume_delta is None else round(volume_delta, 6),
        "volume_delta_percent": None if volume_delta_pct is None else round(volume_delta_pct, 6),
        "symmetric_difference_volume_mm3": None if symdiff_volume is None else round(symdiff_volume, 6),
        "symmetric_difference_error": symdiff_error,
        "pass_extents": pass_extents,
        "pass_volume": pass_volume,
        "pass_symdiff": pass_symdiff,
    })

def _np_converter(o):
    if isinstance(o, np.generic):
        return o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(f"Unserializable object {type(o)}")

json_path = OUT_DIR / "verification_report.json"
txt_path = OUT_DIR / "verification_report.txt"

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, default=_np_converter)

with open(txt_path, "w", encoding="utf-8") as f:
    f.write("RetroPad Verification Report\n")
    f.write("=" * 80 + "\n\n")
    for r in results:
        f.write(f"Part: {r['part']}\n")
        f.write(f"Status: {r['status']}\n")
        if r["status"] == "MISSING_FILE":
            f.write(f"Missing original: {r['original']}\n")
            f.write(f"Missing generated: {r['generated']}\n\n")
            continue

        f.write(f"Original extents (mm):  {r['original_metrics']['extents']}\n")
        f.write(f"Generated extents (mm): {r['generated_metrics']['extents']}\n")
        f.write(f"Extent delta xyz (mm):  {r['extent_delta_xyz_mm']}\n")
        f.write(f"Max extent delta (mm):  {r['max_extent_delta_mm']}\n")
        f.write(f"Original volume (mm^3):  {r['original_metrics']['volume']}\n")
        f.write(f"Generated volume (mm^3): {r['generated_metrics']['volume']}\n")
        f.write(f"Volume delta (mm^3):     {r['volume_delta_mm3']}\n")
        f.write(f"Volume delta (%):        {r['volume_delta_percent']}\n")
        f.write(f"Sym diff volume (mm^3):  {r['symmetric_difference_volume_mm3']}\n")
        f.write(f"Sym diff error:          {r['symmetric_difference_error']}\n")
        f.write(f"Watertight original:     {r['original_metrics']['watertight']}\n")
        f.write(f"Watertight generated:    {r['generated_metrics']['watertight']}\n")
        f.write(f"Pass extents:            {r['pass_extents']}\n")
        f.write(f"Pass volume:             {r['pass_volume']}\n")
        f.write(f"Pass symdiff:            {r['pass_symdiff']}\n")
        f.write("\n")

print(f"Wrote: {json_path}")
print(f"Wrote: {txt_path}")
