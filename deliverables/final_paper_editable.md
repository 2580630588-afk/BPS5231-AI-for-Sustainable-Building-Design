# Rapid Evaluation of Office Window Options in Singapore: Prediction Transfer and Design Applicability across Plan Shapes

**BPS5231 AI for Sustainable Building Design — Final study**
*18 November 2026*

## Abstract

This study tests whether a fast surrogate estimates office cooling demand and paired window-strategy savings beyond familiar geometries. The main EnergyPlus 24.2 experiment comprises 1,890 annual simulations covering rectangles, L-shaped plans, equilateral triangles, regular pentagons and hexagons, and polygonal approximations of circles. Three documented glazing assemblies and two overhang depths give six paired options. The initial experiment uses 1,008 development cases and reserves 384 external cases. Another 252 diagnostic cases separate geometry changes from simultaneous orientation and window-to-wall-ratio changes. Polynomial Ridge, selected using grouped development cross-validation, achieves external cooling MAE of 0.47 kWh thermal/(m² year) and savings-rate MAE of 0.45 percentage points. Forest predictions transfer less successfully under combined input shifts. Operation changes alter percentage savings, while a representative daylight screen changes the preferred glazing at low window area. A local interface displays predictions, matching simulations and applicability warnings. The contribution is a bounded design-assessment workflow, not a novel learning algorithm or real-building validation.

An independent 30-run follow-up confirms low prediction error but finds no selection advantage over a simple daylight-feasible SHGC rule.

**Keywords:** office windows; cooling thermal demand; surrogate model; geometric transfer; daylight screening; reproducibility

## 1 Introduction and related work

Early design involves repeated comparisons between floor plans and facade options. Two distinct questions arise: whether a model predicts absolute demand on an unfamiliar plan, and whether intervention savings transfer accurately. A small error in total demand does not guarantee an accurate difference between two similar options. Moreover, an intervention with minimum cooling demand may have undesirable daylight performance.

Surrogates already approximate retrofit solutions [9]. Qiblawi et al. [5] investigate geometry changes and show that good prediction does not always imply out-of-sample generalisation. Jowett-Lockwood and Evins [6] examine different geometries and locations for inverse surrogates, which address a different task from the forward prediction here. Westermann and Evins [7] use uncertainty-aware surrogates to identify cases that merit simulation. Our geometric-distance warning is a novelty heuristic, not their Bayesian uncertainty method.

This study asks: how do demand and intervention effects transfer across shapes and areas; how do operating assumptions affect the results; and when does rapid prediction support a useful design comparison? A simple regularised response surface remains a valid preferred model. Algorithmic complexity is not itself a contribution.

## 2 Simulation and experiment

### 2.1 Geometry and thermal assumptions

The open Buildings.sg office template and Singapore IWEC weather are retained with attribution and hashes [1,4]. Final cases rebuild the geometry as a single well-mixed open-plan zone, height 3 m, with adiabatic floors and ceilings. This consistent simplification replaces the interim five-zone model. The previous 144 outcomes are not combined with the final training data. A separate matched five-zone experiment audits the zoning change.

Opaque assemblies use the source library's Generic Exterior Wall, Generic Interior Floor and Generic Roof, documented layer by layer in data/opaque_constructions.json. They are controlled assumptions, not calibrated Singapore office constructions. No urban obstruction, infiltration, bulk interzone airflow or detailed HVAC electricity model is added. Floor-area and window-area checks operate on generated surface coordinates.

The main L outline uses (0,0), (3,0), (3,1), (1,1), (1,3), (0,3), scaled to the target area. Its external-test variant has arm thickness 1.3. Concave floors and roofs are triangulated within the same zone. The other nonrectangular shapes are regular polygons. The circle is an equal-area 24-gon, with 12- and 48-gon convergence tests. It has planar window segments rather than detailed curved glass. Each wall has a centred window whose width and height scale with the square root of WWR. Horizontal overhangs extend from the window head and rotate with the building.

![Plan families](../results/figures/plan_shapes.png)

**Figure 1.** Representative 900 m² plans on a common scale. The experiment covers these families, not arbitrary architectural geometry.

### 2.2 Products and operation

The Guardian 2025 selector [3] supplies linked parameters for 6-16-4 double glazing with 90% argon: SN75 (U=1.0 W/(m² K), g=0.40, VT=0.75), SN70/35 (1.0, 0.35, 0.70), and SN40/23 (1.0, 0.23, 0.40). Each has no overhang or a 0.6 m overhang. The common baseline is SN75 without shading. Catalog g is used as nominal SHGC in SimpleGlazing; this does not reproduce full layer-level angular optics, frames or certified whole-window properties, and does not establish local supply or price.

Ideal loads use unlimited capacity, cooling at 26°C, heating at 20°C and humidistat targets of 40%–70% RH. Lighting is 9 W/m², equipment 22 W/m² and design occupancy 0.047501 persons/m². The inherited weekday 09:00–18:00 fractional occupancy profile has unoccupied weekends. Outdoor air is 0.6 ACH with occupancy scheduling and heat recovery disabled. Daylight dimming is off. The IWEC input uses the non-leap 2006 calendar and represents typical rather than observed study-year weather.

### 2.3 Dataset roles

| Dataset | Cases | Purpose |
| :--- | ---: | :--- |
| Rectangle development | 648 | Ratios 1, 2, 4; areas 600, 900, 1200 m² |
| Other-family development | 360 | Five nonrectangular families at 900 m² |
| Prespecified external tests | 384 | New ratios, areas and combinations |
| Operation sensitivity | 180 | Five one-factor changes on six forms |
| Circle convergence | 12 | 12- and 48-gon tests |
| Daylight application | 36 | Six representative contexts |
| Zoning comparison | 18 | One- versus five-zone rectangles |
| Post-hoc diagnostics | 252 | Shape-only and area-only changes |

**Table 1.** Original experiment, 1,890 simulations; 30 follow-up runs are reported separately in Section 4.5. Each context contains six paired options; rows are not independent measured buildings.

Development orientations are 0°, 45°, 90° and 135°, with WWR 0.2, 0.4 and 0.6. The 384 external cases use orientations 15° and 75° and WWR 0.3 and 0.5. They cover ratios 1.5/3, ratio 5 extrapolation, rectangular areas 750/1050/1500 m², and nonrectangular areas 750/1050 m². These are combined shifts, not isolated shape tests. After the initial evaluation, 144 matched-area shape tests and 108 matched-shape area tests were added. These explicitly post-hoc diagnostics never enter training or tuning. The machine-readable protocol distinguishes both stages.

## 3 Analysis methods

### 3.1 Outcomes and model evaluation

Cooling intensity is q = ΣQ/(3.6 × 10⁶ A), where Q is hourly Zone Ideal Loads Supply Air Total Cooling Energy in joules, summed across thermal zones, and A is floor area in m² [2]. This is supply-air cooling thermal demand under the stated conditions, not electricity, measured EUI or money saved. Paired saving is Δq = q baseline − q option; reduction is R = 100Δq/q baseline. Predictions use the same formulas with predicted baseline and option demand. Demand and saving errors use kWh thermal/(m² year); reduction errors use percentage points.

Features comprise log area, external-wall/floor-area ratio, compactness 4πA/P², footprint/bounding-box-area ratio, eight perimeter-weighted directional exposure descriptors, WWR, U, SHGC, VT and overhang depth. Geometry is described physically rather than by an arbitrary numeric family label. Linked product values and constant U prevent independent causal attribution to U, SHGC and VT.

Fixed models are a strategy-specific training mean, standardised inverse-distance five-neighbour interpolation, degree-two Polynomial Ridge with training-fold scaling and alpha 10, and random forest with 300 trees, depth 12, minimum leaf size 2 and seed 2026. Ridge is a regularised response surface, not evidence that sophisticated AI is necessary.

Six-fold grouped cross-validation keeps the six strategies together and combines rotationally equivalent regular-shape contexts. Whole-family holdout excludes each of the six families in turn. Rectangle-only and expanded training sets separately predict the same external cases. Model selection uses grouped development MAE only. Preprocessing is fitted within training folds [8]. Prediction and paired-effect metrics are reported independently.

### 3.2 Sensitivity and daylight screen

Sensitivity tests at 900 m², 0° and WWR 0.4 separately change ventilation to 0.3/1.2 ACH, operation to 07:00–20:00 at fraction 0.75, maximum RH to 60%, or humidity control to None. The schedule experiment changes both duration and occupancy profile. Ranges are exploratory rather than regulatory, and interactions are not estimated. The five-zone bridge matches opaque assemblies and operation, removes domestic-hot-water zone gains, and retains 3 m perimeter zones in three rectangles.

For the representative 2:1 rectangle, EnergyPlus SplitFlux calculates nine reference points at 10%, 50% and 90% of both dimensions, 0.8 m above the floor. Lighting-control fractions are zero. The illustrative screen requires mean point DA300 of at least 50% of occupied weekday hours. Nine equally weighted points do not constitute spatial daylight autonomy, glare evaluation or compliance. This original application covers two orientations and three WWRs; the independent follow-up uses four further contexts (Section 4.5).

## 4 Results and design implications

### 4.1 Absolute prediction and effect transfer

| Model | Grouped CV | External | Family holdout |
| :--- | ---: | ---: | ---: |
| Strategy mean | 9.97 | 5.47 | 8.54 |
| 5-NN interpolation | 5.38 | 1.89 | 4.43 |
| Polynomial Ridge | 0.70 | 0.47 | 1.28 |
| Random forest | 1.01 | 5.36 | 1.71 |


**Table 2.** Pooled cooling-demand MAE. External results use 384 combined-shift cases; whole-family holdout covers the 1,008 development cases under separate splits.

Ridge achieves external MAE 0.47, RMSE 0.63 and R² 0.995. Interpolation MAE is 1.89 and forest MAE 5.36. The external WWRs lie between development levels, challenging the forest's stepwise response. Post-hoc matched tests reduce forest MAE to 0.86, while Ridge gives 0.37, including 0.43 for shape-only and 0.28 for area-only changes. This supports the relevance of combined shifts but does not isolate one variable as the sole explanation.

Rectangle-only Ridge has external MAE 0.48, close to expanded Ridge at 0.47. Thus more shape families do not yield a large aggregate improvement in this controlled system. Whole-family Ridge MAE rises to 1.28. External WWRs also span a narrower interval, so external error below grouped-CV error does not imply universally easy transfer.

![Prediction errors](../results/figures/prediction_comparison.png)

**Figure 2.** Model comparisons under grouped and external testing. Complexity does not automatically improve transfer.

Expanded Ridge savings MAE is 0.64 and reduction-rate MAE 0.45 percentage points, versus interpolation at 1.99 and 1.40. On grouped validation, forest predicts differences more accurately than Ridge despite worse absolute-demand MAE. This demonstrates why the outcomes must remain separate. A paired-context bootstrap gives Ridge-minus-interpolation demand MAE difference -1.42, with descriptive 95% interval [-1.65, -1.20]. Resampling 64 simulated contexts does not quantify real-building uncertainty.

### 4.2 Sensitivity and geometric checks

Ventilation of 0.3 ACH reduces cooling intensity by about 15 units; 1.2 ACH adds about 30. The extended occupancy profile adds about 40 kWh thermal/(m² year). Saving percentages shift by up to 4.04 percentage points as operating loads change the baseline. Humidity-control changes have much smaller effects in this ideal-loads configuration, which does not establish that tropical humidity or real dehumidification electricity is unimportant.

![Sensitivity](../results/figures/sensitivity.png)

**Figure 3.** Operation changes affect demand and the denominator of percentage savings. The longer schedule also changes occupancy intensity.

The matched single-/five-zone tests differ by at most 1.90% in cooling and 0.27 percentage points in paired reductions. This is a rectangle-only audit, not proof of adequate zoning for every irregular occupied building. The 24-/48-gon cooling difference is at most 0.55% across six options at the reference context. Circle convergence is therefore bounded to that context.

### 4.3 A constrained design comparison

At 900 m², aspect ratio 2, 0° and WWR 0.2, SN40/23 plus a 0.6 m overhang minimises cooling at 99.45 kWh thermal/(m² year), but mean DA300 is 36.90%. Under the declared 50% screen, SN70/35 with the overhang becomes the lowest-demand feasible option: 102.77, with DA300 77.46%. It sacrifices about 3.31 thermal units per m² per year to pass the illustrative daylight screen. At WWR 0.4/0.6, the darkest shaded option passes.

![Daylight comparison](../results/figures/daylight_tradeoff.png)

**Figure 4.** Cooling versus sampled daylight in 36 rectangle cases. The horizontal line is a study screen, not a code threshold.

The constrained choice changes in two of six contexts. Surrogate and simulation choices agree, but these thermal contexts already occur in development data and daylight comes from simulation. Zero regret here demonstrates workflow consistency, not independent AI decision accuracy. There is no cost optimum, payback calculation or lighting-energy saving claim.

### 4.4 Speed, learning curve and interface

Nine sequential simulations across rectangle, L and circle cases have median runtime 1.21 s. A preloaded Ridge prediction takes about 0.198 ms on this workstation, excluding interface latency. Assuming the same median for every training case gives an illustrative data-generation cost of 20.3 minutes and break-even near 1008 additional individual-case queries. Validation, development and engineering costs increase total effort. A few one-off designs remain inexpensive to simulate directly.

The fixed learning curve gives external MAE 1.27/0.66/0.45/0.47 for 168/360/678/1008 training rows. More data do not improve accuracy monotonically. These are descriptive fixed-subset evaluations, not external-test tuning.

The local interface compares two forms and six window options, reporting predicted cooling, implied total demand and percentage reductions. Matching simulation values appear separately. Daylight appears only for supported contexts. Explicit bounds and a training-geometry distance rule flag possible extrapolation; the distance rule flags 24 of 384 external rows. It is not a calibrated error probability. Changed operation or unresolved project conditions require new simulation.

### 4.5 Independent follow-up and subgroup errors

After the original results, 30 additional annual runs were specified on 18 November. Before running them, the model predictions, cases, a 50% mean-point DA300 screen and a rule comparator were frozen in data/final_validation/protocol.json. None of these geometry/area/orientation/WWR combinations occurs in the original 1,890 cases. These follow-up results are reported separately and never used for fitting or tuning.

Four daylight contexts combine rectangle 1.5:1 at 850 m² and 30°, and rectangle 3:1 at 1100 m² and 60°, each at WWR 0.2/0.4, with six options. Cooling MAE is 0.47 kWh thermal/(m² year). Both the surrogate and the simple rule select the simulated minimum among daylight-feasible options in all four contexts. The rule selects the lowest SHGC, breaking ties by deeper overhang. Both methods receive the same simulated daylight feasibility. Their zero selection loss provides no evidence of a surrogate decision advantage over this rule. At WWR 0.2 both contexts select shaded SN70/35; at WWR 0.4 both select shaded SN40/23.

A fifth context tests the 600 m² wide-arm L at 0° and WWR 0.4. Its six cooling predictions have MAE 0.63 and maximum absolute error 1.38. This validates that specific combination, without validating all L shapes or other operating conditions. Across the five new contexts, the 75 within-context option-pair comparisons have difference MAE 0.52 and ordering agreement 97.3%. These dependent pairs are descriptive, not 75 independent observations.

The three highest-MAE shape/area subgroups of the original 384-case external test are:

| Shape / area m² | Contexts | MAE | Maximum error |
| :--- | ---: | ---: | ---: |
| rect5 / 900 | 4 | 0.94 | 3.00 |
| Lwide / 750 | 4 | 0.72 | 1.45 |
| rect2 / 1500 | 4 | 0.70 | 1.87 |

**Table 3.** Six paired strategies per context. Errors are kWh thermal/(m² year). All subgroups, empirical 95th-percentile errors and separate family-holdout/diagnostic results are provided in results/final_validation/stratified_errors.csv. Subgroup variation limits interpretation of pooled accuracy; these error summaries are not per-query confidence intervals.

The revised interface distinguishes exact simulation matches, evidence at other conditions of the same shape, and unsupported combinations. It lists the exact tested conditions and withholds comprehensive design recommendations when daylight is unavailable. The full study now contains 1,920 annual simulations: the original 1,890 plus 30 separately documented follow-up runs.

## 5 Reproducibility and limitations

The inspected interim branch lacked a results directory despite the README requiring it. The final local package contains generated IDFs, compact run records and logs, input and result tables, pinned dependencies, an executed notebook, model, interface and reproduction commands. Full reproduction requires EnergyPlus 24.2; quick reproduction starts with bundled outcomes. Large intermediate SQL files are regenerated. Hashes support integrity checks. No GitHub upload has been made.

All 1,920 simulations, including the 30 follow-up runs, have 8,760 hours and no severe errors. Unused-construction warnings are disclosed. The bridge retains inherited schedule-type warnings; daylight cases warn about omitted glare and zero controlled-light fractions, consistent with the declared scope. Successful execution does not validate physical accuracy.

Limits include one climate, selected regular polygons and two L outlines, well-mixed open-plan zones, assumed envelope assemblies, fixed operation, three linked products, nominal glazing optics and a sparse rectangle-only daylight screen. Tests omit arbitrary concave geometry, atria, partitions, urban shading, detailed HVAC, costs and embodied impacts. Small simulation runtimes limit the practical advantage for isolated tasks. These bounds prevent interpreting the interface as a universal design or compliance tool.

## 6 Conclusions

A regularised response surface provides accurate demand and savings estimates within this controlled experiment. Complex models are not automatically better, and adding more shape families produces only a small aggregate Ridge improvement. Operating assumptions affect saving percentages. A declared daylight screen creates a concrete design tradeoff at low WWR. The defensible application is repeated preliminary comparison with explicit limits and access to simulation, not universal facade recommendations or real-building electricity prediction.

The independent follow-up supports bounded prediction accuracy, while equal performance of the simple rule limits claims of AI-assisted selection benefit.

## References

**[1]** City Syntax Lab. Buildings.sg office template, 06_Office_SGP_2025_V5.idf. [Source](https://github.com/City-Syntax/buildings.sg)

**[2]** EnergyPlus 24.2. Input Output Reference: ideal loads and daylighting. [Source](https://bigladdersoftware.com/epx/docs/24-2/input-output-reference/group-daylighting.html)

**[3]** Guardian Glass (2025). Coated Glass digital selector, p. 2, double glazed 6-16-4, 90% argon. [Source](https://www.guardianglass.com/content/dam/guardianindustriesholdings/technical-center/europe/architectural/digital-glass-selector/Guardian-Glass-Digital-Selector-EN.pdf)

**[4]** Ladybug Tools. Singapore IWEC weather, WMO 486980. [Source](https://github.com/ladybug-tools/uwg/blob/master/resources/SGP_Singapore.486980_IWEC.epw)

**[5]** Qiblawi, S., Touchie, M., and Azar, E. (2026). Integrating building geometry changes into reduced-order modeling for rapid retrofit performance assessment. eSim 2026, 783–790. [Source](https://doi.org/10.26868/31114504.2026.77)

**[6]** Jowett-Lockwood, L., and Evins, R. (2025). Examining the generalizability of inverse surrogate models for different geometries and locations. Energy and Buildings 335, 115539. [Source](https://doi.org/10.1016/j.enbuild.2025.115539)

**[7]** Westermann, P., and Evins, R. (2020). Using Bayesian deep learning approaches for uncertainty-aware building energy surrogate models. [Source](https://arxiv.org/abs/2010.03029)

**[8]** Scikit-learn documentation. Grouped cross-validation and regression estimators. [Source](https://scikit-learn.org/stable/modules/cross_validation.html)

**[9]** Thrampoulidis, E., Mavromatidis, G., Lucchi, A., and Orehounig, K. (2021). A machine learning-based surrogate model to approximate optimal building retrofit solutions. Applied Energy 281, 116024. [Source](https://doi.org/10.1016/j.apenergy.2020.116024)