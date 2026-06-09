import os
from build123d import *

# ==========================================
# 1. FOLDER & FILE CONFIGURATION
# ==========================================
GENERATED_DIR = "..\STEP_Files"
ORIGINAL_DIR = "..\Original_Files"

FILE_MAPPING = {
    "test_bottom_shell.step": "Bottom Shell.step",
    "test_top_shell.step": "Top Shell.step",
    "test_button.step": "Button.step",
    "test_d_pad.step": "D-Pad.step"
}

# ==========================================
# 2. THE DUAL-TEST ENGINE
# ==========================================
def run_dual_verification(mapping, gen_dir, orig_dir):
    print("==========================================")
    print("🚀 STARTING DUAL-CRITERIA VERIFICATION")
    print("==========================================\n")
    
    total_parts = len(mapping)
    volume_passes = 0
    symmetry_passes = 0

    for gen_name, orig_name in mapping.items():
        gen_path = os.path.join(gen_dir, gen_name)
        orig_path = os.path.join(orig_dir, orig_name)
        
        print(f"Testing: {gen_name}")
        print(f"Against: {orig_name}")
        
        # 1. Load the files
        try:
            generated_part = import_step(gen_path)
            original_part = import_step(orig_path)
        except Exception as e:
            print(f"  ❌ ERROR: Could not load files. ({e})\n")
            continue

        # ------------------------------------------
        # TEST A: VOLUME COMPARISON
        # ------------------------------------------
        gen_vol = generated_part.volume
        orig_vol = original_part.volume
        vol_diff = abs(gen_vol - orig_vol)
        
        if vol_diff < 0.0001:
            print(f"  ✅ VOLUME TEST: PASS (Diff: {vol_diff:.4f} mm³)")
            volume_passes += 1
        else:
            print(f"  ❌ VOLUME TEST: FAIL (Diff: {vol_diff:.4f} mm³)")

        # ------------------------------------------
        # TEST B: SYMMETRIC DIFFERENCE
        # ------------------------------------------
        leftover_gen = generated_part - original_part
        leftover_orig = original_part - generated_part
        sym_diff_shape = leftover_gen + leftover_orig

        try:
            sym_diff_vol = sym_diff_shape.volume
        except AttributeError:
            sym_diff_vol = 0.0  # Empty shape means perfect match

        if sym_diff_vol < 0.0001:
            print(f"  ✅ SYMMETRY TEST: PASS (Diff: {sym_diff_vol:.4f} mm³)\n")
            symmetry_passes += 1
        else:
            print(f"  ❌ SYMMETRY TEST: FAIL (Diff: {sym_diff_vol:.4f} mm³)")
            
            # Export the error geometry for visual debugging
            error_file = f"ERROR_{gen_name}"
            export_step(sym_diff_shape, error_file)
            print(f"     -> Exported '{error_file}' to debug mismatched geometry.\n")

    # ==========================================
    # 3. FINAL SUMMARY REPORT
    # ==========================================
    print("==========================================")
    print("📊 FINAL EVALUATION SUMMARY")
    print("==========================================")
    print(f"Total Parts Tested:   {total_parts}")
    print(f"Volume Matches:       {volume_passes} / {total_parts}")
    print(f"Geometry Matches:     {symmetry_passes} / {total_parts}")
    
    if volume_passes == total_parts and symmetry_passes == total_parts:
        print("\n🎉 ALL TESTS PASSED! The dataset is geometrically perfect.")
    else:
        print("\n⚠️ SOME TESTS FAILED. Please review the output above.")

if __name__ == "__main__":
    run_dual_verification(FILE_MAPPING, GENERATED_DIR, ORIGINAL_DIR)