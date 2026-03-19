# RetroPad – Build123D Parametric Modeling Assignment

A fully parametric CAD model of a retro game-pad device, created entirely through Python scripts using the **Build123D** library. The project consists of four individual part scripts and one assembly script that brings them all together.

## Project Structure

| File | Description |
|------|-------------|
| `RetroPad_Top.py` | Top shell with button slots, D-Pad cutout, connector bracket, standoffs, and elliptical peg |
| `RetroPad_Bottom.py` | Bottom shell with extended walls, standoffs, elliptical pegs, and connector cutout |
| `RetroPad_Button.py` | Four action buttons with cross-shaped guides and chamfered tops |
| `RetroPad_D_Pad.py` | D-Pad with elliptical base and plus-shaped directional pad |
| `main_assembly.py` | Assembly script — imports all parts, positions them, assigns colors, and exports a single STEP file |
| `STEP Files/` | Exported STEP files for each part and the complete assembly |
| `STL Files/` | Exported STL meshes for each individual part |

---

## a. Modeling Strategy

1. **Base-feature-first approach** — Each part script begins by creating the primary base feature (e.g., a `Box`) centered on the **origin**, using the origin and origin planes as the primary datum.

2. **Progressive detailing** — Additional features (cutouts, standoffs, brackets, pegs) are built on top of the base by referencing **specific faces** or the **origin planes** as datum surfaces, ensuring geometric associativity.

3. **Minimal sketches, solid-body operations** — Wherever possible, solid primitives (`Box`, `Cylinder`, `Ellipse` extrusions) were used directly instead of creating separate sketches, reducing complexity.

4. **Chamfers applied last** — Chamfers and edge treatments were applied at the end of each part's feature tree to avoid interference with downstream Boolean operations.

5. **Full parameterisation** — Every dimension is declared as a named variable at the top of each script (e.g., `total_length = 135 * MM`, `wall_thickness = 1 * MM`). This makes dimensions easily identifiable, updatable, and self-documenting.

6. **Assembly via positioning** — The assembly script (`main_assembly.py`) imports each finished part and positions them using `Location` transforms, then packages them into a `Compound` for a single STEP export.

7. **Dimension extraction from original design** — All dimensions and feature placement values were **measured directly from the original design files** provided with the assignment to ensure accuracy.

---

## b. Assumptions

- **Decimal precision** — Dimensions were captured up to **3 decimal places** (e.g., `10.429 mm`, `37.039 mm`) for accuracy while keeping values manageable.
- **Unit system** — All dimensions use **millimeters** (`* MM`), consistent with the original design files.
- **Wall / base thickness** — A uniform wall thickness of `1 mm` and base thickness of `3 mm` were applied unless the original design indicated otherwise.
- **Chamfer uniformity** — Corner chamfers and base outer chamfers were assumed to be uniform across all four corners/edges of the shells.
- **Assembly positioning** — Parts are positioned relative to the global origin; the bottom shell sits at `Z = 0` and the top shell is offset to `Z = 22.424 mm` (the total device height) to mate correctly.

---

## c. Verification of Correctness

Correctness was verified using a **multi-layered approach**:

1. **Visual comparison (GUI-based)** — Each generated part and the final assembly were imported into a GUI-based CAD viewer and **visually compared** against the original design files side by side.

2. **Dimensional verification** — Key dimensions (overall length, width, height, feature positions) were **measured in the GUI tool** and cross-checked against the original design to confirm geometric accuracy.

3. **Volumetric verification** — Part volumes were **compared between the generated models and the originals** in the GUI software to ensure no missing or extra material.

4. **Positioning check** — The assembly was inspected in the GUI tool to verify that all components are **correctly positioned relative to each other** (e.g., buttons sit in their slots, D-Pad aligns with its cutout).

5. **Scripted volume and geometric validation**  — Automated scripts written to programmatically calculate and compare volumes of each part for repeatable, quantitative verification.

### Volumetric Comparison

| Part           | Original Volume (mm3) | Generated Volume (mm3) | Difference (%) |
|----------------|----------------------|------------------------|----------------|
| Top Shell      | 24154.758            | 24154.438              | 0.000            |
| Bottom Shell   | 27603.164            | 27602.597              | 0.002            |
| Buttons        | 1151.097             | 1151.11                | 0.001            |
| D-Pad          | 7948.726             | 7949.135               | 0.005           |


### Geometric (Bounding Box) Comparison

| Part           | Dimension | Original (mm) | Generated (mm) | Match |
|----------------|-----------|---------------|-----------------|-------|
| Top Shell      | Length    | 135.000       | 135.000         | Yes   |
| Top Shell      | Width     | 53.000        | 53.000          | Yes   |
| Top Shell      | Height    | 14.824        | 14.824          | Yes   |
| Bottom Shell   | Length    | 135.000       | 135.000         | Yes   |
| Bottom Shell   | Width     | 53.000        | 53.000          | Yes   |
| Bottom Shell   | Height    | 19.424        | 19.424          | Yes   |
| Buttons        | Length    | 11.832        | 11.832          | Yes   |
| Buttons        | Width     | 11.832        | 11.832          | Yes   |
| Buttons        | Height    | 15.474        | 15.474          | Yes   |
| D-Pad          | Length    | 32.058        | 32.057          | Yes   |
| D-Pad          | Width     | 28.415        | 28.415          | Yes   |
| D-Pad          | Height    | 15.474        | 15.474          | Yes   |

---

## d. Total Time Spent

| Activity | Time |
|----------|------|
| Familiarising with Build123D syntax and API | ~2–3 hours |
| Scripting all parts and assembly | ~8 hours |
| Debugging ellipse extrude/subtract issue | ~2 hours |
| **Total** | **~12–13 hours** |

> **Note:** A significant portion of the scripting time (~2 hrs) was spent resolving an issue with extruding and subtracting elliptical shapes in the bottom shell, which initially produced unstitched surface bodies instead of a valid solid.

---

## e. AI Tools Used

| Tool | Usage |
|------|-------|
| **VS Code** | Primary development environment — used for writing, editing, and running all scripts. IntelliSense and syntax highlighting helped with Build123D API usage. |
| **Gemini (Google AI)** | Consulted for guidance on complex or challenging modeling situations, such as resolving the ellipse Boolean operation issue and understanding advanced Build123D API patterns. |

---

## How to Run

1. **Install Build123D** (if not already installed):
   ```bash
   pip install build123d
   ```

2. **Generate individual parts:**
   ```bash
   python RetroPad_Top.py
   python RetroPad_Bottom.py
   python RetroPad_Button.py
   python RetroPad_D_Pad.py
   ```

3. **Generate complete assembly:**
   ```bash
   python main_assembly.py
   ```

   Output files will be written to the `STEP Files/` and `STL Files/` directories (or the working directory, depending on your setup).
