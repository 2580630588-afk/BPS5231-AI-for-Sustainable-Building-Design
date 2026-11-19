# BPS5231 final study: window options across office plan shapes

This is a **local final research package**, prepared for the 19 November 2026 submission. It has not been uploaded to GitHub. The existing interim files remain separate.

## Start here

- `deliverables/final_paper_nonrect_daylight.docx`: latest editable paper, seven pages including references.
- `deliverables/final_slides_english_interface.pptx`: latest seven-slide presentation with the English interface screenshot, without speaker notes.
- `deliverables/非矩形采光验证说明.md`: Chinese protocol, results and interpretation for the latest extension.
- `deliverables/期末研究说明与答辩稿.md`: Chinese interpretation, feedback response and five-minute narration.
- `analysis.ipynb`: executed analysis notebook.
- `app/serve.py`: local shape-comparison interface.

## Scope and experiment

The target is **cooling thermal demand**, not HVAC electricity or measured EUI. The original experiment has 1,890 completed EnergyPlus 24.2 cases: 1,008 development, 384 prespecified external, 180 operation sensitivity, 12 circle-convergence, 36 daylight application, 18 zoning-audit and 252 post-hoc diagnostic cases. A 30-run follow-up and a 120-run nonrectangular daylight extension bring the project total to 2,040 annual records. The latter 120 comprise 60 primary cases and 60 sampling-audit repetitions, representing ten independent physical contexts. No follow-up enters training or tuning.

Shapes include rectangles, two L outlines, equilateral triangles, regular pentagons/hexagons, and equal-area 24-sided circle approximations. This is a controlled open-plan intermediate-floor model, not universal building validation.

## Install the analysis environment

The latest clean-environment check used Python 3.12.14 (see `results/reproducibility_check.json`); the original environment is recorded in `results/python_environment.json`. From this directory:

```text
python -m venv .venv
```

Activate `.venv` using your operating system's normal activation command, then:

```text
python -m pip install -r requirements.txt
```

For predictable timings, use one numerical-library thread. On PowerShell:

```powershell
$env:OPENBLAS_NUM_THREADS = "1"
$env:OMP_NUM_THREADS = "1"
```

## Route A: reproduce analysis from included results

**All required analysis inputs are included**, especially `results/simulation_results.csv` (1,890 rows). Do not delete or ignore `results/` when uploading the repository.

```text
python scripts/analyze.py
python scripts/figures.py
python scripts/verify.py
```

These regenerate grouped and external predictions, paired effects, diagnostics, sensitivity summaries, learning curves and the surrogate. No EnergyPlus installation is required for this route. `analyze.py` is deterministic for model metrics; wall-clock timings naturally vary. `results/additional_analysis.json` contains the separately measured simulation benchmark. Reproducing that benchmark requires Route B.

The notebook executes the same analysis entry points. It can be opened in Jupyter. To regenerate its stored outputs without a Jupyter server:

```text
python scripts/build_notebook.py
```

## Route B: regenerate every simulation

Install **EnergyPlus 24.2**, using the official release, and provide the absolute executable path. The engine is not bundled. Original IDF and IWEC inputs are included with source hashes.

```text
python scripts/experiment.py prepare
python scripts/experiment.py run --energyplus "C:/path/to/EnergyPlus/energyplus.exe" --workers 6
python scripts/analyze.py
python scripts/benchmark.py --energyplus "C:/path/to/EnergyPlus/energyplus.exe"
python scripts/figures.py
python scripts/verify.py
```

Valid cached results are reused only when the IDF, weather and executable hashes agree. To force a complete independent rerun, use a fresh project copy with an empty `results/runs/` directory. `--group` selects comma-separated dataset roles from the matrix; `--limit` is for smoke checks only. Full analysis requires all 1,890 cases. Large transient files are removed after successful extraction, leaving a compact JSON record and EnergyPlus error/warning log for each case. SQL can be regenerated from the IDFs.

## November 18 follow-up (latest submission)

**Latest paper: `deliverables/final_paper_nonrect_daylight.docx`.** This editable English manuscript has native Word tables and equations, 10 research papers from 2018–2026, 5 technical sources, verified links and all 2,040 annual records in scope. Microsoft Word rendered it to 7 pages including references. The older PDF, Markdown and Word versions remain historical. Rebuild it with `python scripts/build_word_paper.py` using python-docx 1.2.0; its prose source is `deliverables/final_paper_nonrect_daylight_source.md`.

The original 1,890 runs and training split remain unchanged. A separate 30-run follow-up brings the total to **1,920**: four new rectangular daylight contexts (24 options) plus a 600 m² wide-arm L thermal context (6 options). Cases and predictions were fixed before these runs, after the earlier study results. See `data/final_validation/protocol.json` and `results/final_validation/`.

Run `python scripts/final_validation.py analyze` to reproduce the new metrics, shape/area subgroup table, pairwise comparison errors and decision-rule comparison. To regenerate the 30 simulations, run `python scripts/final_validation.py run --energyplus "C:/path/to/energyplus.exe"`. The frozen predictions must be retained. The model and the simple rule both select all four daylight-feasible optima: this does not demonstrate a model selection advantage.

Use **`deliverables/final_slides_english_interface.pptx`**, **`deliverables/final_paper_nonrect_daylight.docx`**, and `非矩形采光验证说明.md`. Earlier decks, papers and the PDF are retained for history. The notebook includes eight executed cells. Original `verify.py` checks the original 1,890; `final_validation.py analyze` checks the next 30; `nonrect_daylight.py analyze` checks the final 120.

## November 19 nonrectangular daylight extension

Five shapes (wide-arm L, triangle, regular pentagon, regular hexagon and 24-gon circle approximation) are tested at 850 m², 30°, and WWR 0.2/0.4. Each context has three glass products and two overhang depths. The 60 primary simulations use an area-weighted clipped 4 m grid; 60 repetitions use a 2 m grid to audit sampling sensitivity. These repetitions are not independent design cases.

The protocol, predictions and selection rule were fixed before corrected simulations. An initial centroid-only sampling attempt triggered EnergyPlus's 0.15 m window-plane restriction. Revision 2 applies a deterministic 0.20 m clearance to all sample points without changing cases, predictions, thresholds or rules. The original protocol, logs and completed records are retained under `data/nonrect_daylight/revisions/` and excluded from final analysis.

```text
python scripts/nonrect_daylight.py analyze
python scripts/nonrect_daylight.py run --energyplus "C:/path/to/energyplus.exe"
```

The 60 primary cases have cooling-demand MAE 0.375 kWh thermal/(m² year). Daylight changes four of ten cooling-only choices. The model selects all ten simulated feasible optima; the simple rule selects nine and incurs 0.208 kWh thermal/(m² year) loss in the triangle/20% WWR context. The 2 m grid changes no option's feasibility and no selected option. This result is bounded to the tested cases and does not validate SplitFlux against ray tracing or measurements.

For an isolated installation: `python -m venv .venv`, then `.venv\Scripts\python -m pip install -r requirements.txt`. Run commands using that environment's Python. `requirements-validated-lock.txt`, when present, records all installed versions from the clean-environment check. Its Windows/Python version is documented in `results/reproducibility_check.json`.

## Launch the comparison interface

On Windows, double-click `launch_interface.bat` in the extracted project folder. It selects a usable local Python environment and opens the browser after the server starts. Keep the terminal window open while using the app. You may also set `WINDOW_TRANSFER_PYTHON` to your Python executable.

Do not double-click `app/index.html` or open it through a static HTML preview: prediction requires the Python server. If the page says “Failed to fetch”, start the server and visit **http://127.0.0.1:8765/**. GitHub Pages alone cannot run this Python backend.

```text
python app/serve.py
```

Open **http://127.0.0.1:8765/**. Stop with Ctrl+C. The server binds only to localhost and makes no external network calls. It compares six options for two shapes and distinguishes predictions from matching simulations. Geometry-distance and range warnings are heuristics, not confidence intervals. Operation is fixed to the baseline scenario. Daylight is a lookup for supported rectangular cases and the ten new nonrectangular contexts, not a general daylight predictor. Parenthesised nonrectangular DA300 values are the 2 m sampling audit.

Do not load replacement `.pkl` files from untrusted sources. The included surrogate is generated by `scripts/analyze.py`.

## Regenerate documents

To regenerate the latest editable Word paper:

```text
python -m pip install -r requirements-documents.txt
python scripts/build_word_paper.py
```

The following commands regenerate the older Markdown/PDF workflow only:

```text
python scripts/build_paper_text.py
python scripts/render_paper.py
```

`build_paper_text.py` regenerates the Markdown from current results, overwriting manual edits. If you edited the Markdown, run only `render_paper.py`. The slide-generation script is optional and requires the authoring environment's `@oai/artifact-tool` and finalization utilities; that environment is not a requirement for reproducing the scientific results. The delivered PPTX itself is editable.

## Important interpretation limits

- Ridge is a regularised response surface. Its success is not proof that complex AI is necessary.
- Products use linked catalog values. Nominal g is approximated as SHGC in SimpleGlazing, without frames or full angular optics. No local pricing or availability is claimed.
- Mean nine-point DA300 is not spatial daylight autonomy or regulatory compliance. The 50% screen is illustrative. No glare, lighting-electricity or payback claim is made.
- The original daylight design contexts share thermal conditions with development cases and demonstrate a workflow. Four follow-up contexts are independent of training; both the model and simple rule select the feasible optimum in all four, so there is no demonstrated model selection advantage.
- One/five-zone comparisons cover rectangles only. The circular convergence check covers one context.
- Sensitivity ranges are exploratory. The extended schedule changes both hours and occupancy fraction.
- The initial tests were fixed before evaluation; the 252 diagnostic cases were added afterwards to distinguish geometry from concurrent input shifts.

## Files, sources and publication

`references.json` links the model, weather, product catalog, official documentation and literature. `data/opaque_constructions.json` records the selected library assemblies. `results/verification.json` discloses all warning categories. `package_manifest.json` hashes included files. Large benchmark folders, Python environments, runtime libraries and the full vendor brochure are excluded from the distributable ZIP; the three parameter rows and source link are retained.

The inspected interim branch tree is recorded in `data/interim_branch_tree.json`. It contained `data.zip` and `scripts.zip` but no results directory. The final upload should use this **expanded directory structure**, not nested data/script ZIPs. A future branch may be named `final-study`; no branch or remote content has been created or updated by this package.

No new licence is asserted over third-party IDF, weather or product information. Preserve their attribution and applicable terms.
