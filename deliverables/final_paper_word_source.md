Office window strategies across plan shapes in Singapore

Prediction transfer and independent design validation

BPS5231 AI for Sustainable Building Design    |    18 November 2026

Abstract

This study evaluates whether a simulation-trained surrogate can estimate office cooling demand and window-intervention savings across unfamiliar plan shapes, and whether accurate prediction improves design selection. A controlled EnergyPlus 24.2 experiment contains 1,920 annual runs: 1,890 original simulations and 30 separately documented follow-up simulations. Rectangles, L shapes, equilateral triangles, regular pentagons and hexagons, and polygonal circle approximations are paired with three documented glazing assemblies and two overhang depths. Polynomial Ridge, selected using grouped development cross-validation, achieves a cooling-demand MAE of 0.47 kWh thermal/(m² year) and savings-rate MAE of 0.45 percentage points on 384 external cases. Whole-family holdout increases demand MAE to 1.28. The independent follow-up gives MAE 0.47 across 24 rectangular daylight cases and 0.63 across six 600 m² wide-arm L cases. Both the surrogate and a simple daylight-feasible SHGC rule select all four simulated optima, so no selection advantage over that rule is demonstrated. Ventilation and schedule assumptions alter reported savings. The contribution is a reproducible, explicitly bounded workflow for rapid quantitative comparison, rather than a new learning algorithm or a universally optimal facade strategy.

Keywords: building simulation; window design; geometric transfer; paired savings; daylight; surrogate validation

1 Introduction

Early office design requires repeated comparison of building proportions, orientation, window area and facade interventions. A useful prediction tool must provide more than a low average error: it should identify where its evidence applies, estimate intervention effects and support a defensible design decision. Amasyali and El-Gohary [1] show why prediction scope, data characteristics and evaluation measures deserve attention alongside algorithm choice. Westermann and Evins [2] place surrogate modelling within building-design workflows and emphasise sampling and application requirements.

Three questions are distinct. First, can a model predict absolute cooling demand for conditions absent from training? Second, can it predict the difference between a baseline and an intervention? Third, does using those predictions improve the selected intervention relative to a simple rule? Errors shared by two options may cancel in their difference, while small absolute errors can reverse closely spaced options. Accordingly, prediction accuracy and decision usefulness are evaluated separately here.

The study focuses on Singapore office middle floors under controlled operation and typical weather. Its research questions are: RQ1, how do cooling-demand and paired-saving predictions transfer across shapes and areas; RQ2, how sensitive are results to operation and geometric simplification; and RQ3, does a daylight-constrained surrogate decision outperform a transparent rule on new conditions? Evidence is limited to simulated open-plan zones and selected facade products. The paper reports negative as well as positive findings to define an appropriate practical role for the model.





2 Related research and study contribution

2.1 Surrogates and geometric generalisation

Surrogate-assisted building design is established rather than algorithmically novel. The review by Westermann and Evins [2] links model families and sampling choices to design applications. Thrampoulidis et al. [3] approximate retrofit solutions using machine learning and compare them with a simulation-optimisation approach. These studies motivate computationally convenient evaluation, but do not establish that a surrogate will improve every small design problem. Here, both a neighbour-based interpolation model and a regularised response surface are retained as substantive comparators.

Generalisation must be assessed against the intended deployment change. Jowett-Lockwood and Evins [4] investigate inverse surrogate models across geometries and locations; their inference task differs from the forward annual-demand prediction used here. Qiblawi et al. [5] explicitly introduce geometry changes and test unseen models, reporting that strong prediction within studied conditions need not imply successful out-of-sample performance. This motivates distinct context holdouts, whole-family holdouts and tests of new area and orientation combinations, rather than a single random split.

2.2 Design tradeoffs and uncertainty

Window design also requires more than minimising cooling. Pilechiha et al. [7] jointly consider energy, daylight and view quality. Kangazian and Emadian Razavi [8] evaluate combinations of glazing and shading using daylight, glare and energy criteria. For tropical open-plan offices, Seghier et al. [9] connect thermal and daylight assessment using OTTV and daylight prediction. Their work supports a combined-performance perspective, but the present experiment uses annual ideal-load cooling and a limited daylight screen, not OTTV, glare assessment or a complete comfort optimisation.

Westermann and Evins [6] develop uncertainty-aware surrogates that can identify predictions needing a higher-fidelity model. The present interface uses a simpler geometric-distance warning. That warning is not a calibrated prediction interval and cannot quantify uncertainty in climate, operation or the simulation assumptions. Kapoor and Narayanan [10] identify separation and evaluation failures that can inflate machine-learning claims. Their methodological argument supports fitting preprocessing within training folds and keeping the independent follow-up outside training and model selection.

Research strand | Implication for this study

Surrogate design and retrofit [2,3] | Compare useful simple models and include training-data cost.

Geometry generalisation [4,5] | Separate familiar contexts, new families and combined input shifts.

Window performance tradeoffs [7–9] | Screen daylight before selecting the minimum-cooling option.

Uncertainty and reproducibility [6,10] | Keep test cases separate and make applicability limits visible.

Table 1. Positioning of the study. Citations motivate the design of this experiment; their reported performance is not treated as a directly comparable benchmark.

The contribution is the combination of paired effects, separate transfer tests, a rule-based decision comparator and a reproducible interface. No claim is made that this combination is the first of its kind, that the selected algorithm is new, or that simulation agreement constitutes real-building validation.





3 Simulation design and data

3.1 Geometry and physical assumptions

The Buildings.sg office template [11] and Singapore IWEC weather file [12] provide the source inputs. EnergyPlus 24.2 [13] rebuilds each case as a single well-mixed zone, 3 m high, with adiabatic floor and ceiling. The main L outline is (0,0), (3,0), (3,1), (1,1), (1,3), (0,3), scaled to area; the wide-arm variant uses arm thickness 1.3. Other nonrectangular plans are regular polygons. The circle is represented by an equal-area 24-gon. Concave floor and roof surfaces are triangulated within the same thermal zone.

Figure 1. Representative equal-area plans. The circle is a segmented approximation; selected families do not represent arbitrary building geometry.

Dataset role | Runs | Conditions or purpose

Rectangle development | 648 | Ratios 1, 2, 4; 600, 900, 1200 m²

Other-family development | 360 | Five families, each at 900 m²

Prespecified external tests | 384 | New ratios, areas and input combinations

Operation sensitivity | 180 | Five one-factor changes across six forms

Circle and zoning audits | 30 | 12/48-gon cases and five-zone rectangles

Original daylight application | 36 | Six rectangular contexts

Post-hoc diagnostics | 252 | Matched shape-only and area-only changes

Independent follow-up | 30 | Four new daylight contexts and one L context

Total | 1920 | Six paired facade options per context

Table 2. Simulation allocation. The 30 follow-up runs remain separate from the original 1,890 and never enter training or model selection.

Development orientations are 0°, 45°, 90° and 135°, with window-to-wall ratio (WWR) 0.2, 0.4 and 0.6. External tests use 15°/75° and WWR 0.3/0.5. They include ratios 1.5, 3 and 5; rectangular areas 750, 1050 and 1500 m²; and selected nonrectangular cases at 750/1050 m². These simultaneous changes are distinguished from the later matched-variable diagnostics.





3.2 Envelope products and operation

Three Guardian assemblies [14] use 6–16–4 double glazing with 90% argon: SN75 (U = 1.0 W/(m² K), g = 0.40, VT = 0.75), SN70/35 (1.0, 0.35, 0.70) and SN40/23 (1.0, 0.23, 0.40). Each is paired with no overhang or a 0.6 m overhang. SN75 without shading is the baseline. Catalog g is approximated as nominal SHGC in SimpleGlazing. This does not reproduce detailed angular optics, frame performance or whole-window certification. Parameters are linked product combinations; independent causal effects of U, SHGC and VT cannot be inferred.

The template library supplies Generic Exterior Wall, Generic Interior Floor and Generic Roof assemblies, recorded layer by layer in the package. They are controlled assumptions rather than calibrated local constructions. Ideal loads use unlimited capacity, 26°C cooling, 20°C heating and humidistat targets of 40–70% RH. Lighting is 9 W/m², equipment 22 W/m² and design occupancy 0.047501 persons/m². Outdoor air is 0.6 ACH with occupancy scheduling and no heat recovery. The inherited weekday 09:00–18:00 fractional schedule has unoccupied weekends. The IWEC run uses a non-leap 2006 calendar, not observed 2026 weather. Urban obstruction, infiltration, detailed HVAC electricity and daylight dimming are excluded.

4 Analysis and validation methods

4.1 Outcomes and model inputs

Hourly Zone Ideal Loads Supply Air Total Cooling Energy, Q, is summed over 8,760 hours and all zones. Cooling intensity q, paired saving Δq and percentage reduction R are calculated as follows. A denotes floor area; b and s denote baseline and strategy. Predicted savings use the same formulas applied to predicted outcomes.

q = Σ Q / (3.6 × 10⁶ A)     [kWh thermal/(m² year)]

Δq = q_b − q_s                 R = 100 Δq / q_b

Demand and saving errors use kWh thermal/(m² year); errors in R use percentage points. MAE is the mean absolute difference between predicted and simulated values. Selection loss is the simulated cooling of the chosen feasible option minus the lowest simulated cooling among feasible options; zero denotes a tied or exact optimum. The output is cooling thermal demand, not electricity, bills or measured building EUI. Features comprise log area, wall/floor-area ratio, compactness 4πA/P², footprint/bounding-box-area ratio, eight perimeter-weighted directional exposures, WWR, U, SHGC, VT and overhang depth.

4.2 Models and data separation

Four fixed comparators are evaluated: a strategy-specific training mean; standardised inverse-distance five-neighbour interpolation; degree-two Polynomial Ridge with training-fold scaling and alpha 10; and random forest with 300 trees, depth 12, minimum leaf size 2 and seed 2026. Six-fold GroupKFold keeps the six paired strategies together and combines rotationally equivalent regular-shape contexts. Preprocessing is fitted only within each training fold [15]. Whole-family holdout separately excludes each of six families. Rectangle-only and expanded training sets predict the same external cases. Selection uses grouped development MAE only.

After the original evaluation, 144 shape-only and 108 area-only diagnostic runs were added without fitting or tuning. The 30-run follow-up was subsequently specified with frozen predictions and selection rules before simulation. Its geometry/area/orientation/WWR combinations do not occur in the original matrix. These stages address targeted questions after earlier results and are not presented as an entirely prospectively registered study.





5 Prediction transfer results

Model | Grouped CV MAE | External MAE | Family holdout MAE

Strategy mean | 9.97 | 5.47 | 8.54

5-NN interpolation | 5.38 | 1.89 | 4.43

Polynomial Ridge | 0.70 | 0.47 | 1.28

Random forest | 1.01 | 5.36 | 1.71

Table 3. Cooling-demand error in kWh thermal/(m² year). External metrics use 384 cases. Family holdout and grouped CV are separate evaluations of the 1,008 development cases.

Ridge is selected by grouped CV. Its external RMSE is 0.63 and R² is 0.995. External paired-saving MAE is 0.64 and reduction-rate MAE is 0.45 percentage points, compared with 1.99 and 1.40 for neighbour interpolation. On grouped validation, forest predicts paired differences more accurately than Ridge despite a worse absolute-demand MAE. Thus the two targets should not be conflated.

Rectangle-only Ridge has external MAE 0.48, close to 0.47 for expanded training. Adding nonrectangular families therefore yields little aggregate improvement under these controlled assumptions. The increase to 1.28 under whole-family holdout indicates a more difficult transfer task. External WWR values also span a narrower interval than development values, so their lower error is not evidence that unfamiliar geometries are universally easy to predict.

Forest external error increases under the combined shifts. The later matched tests give MAE 0.86 for forest and 0.37 for Ridge; Ridge shape-only and area-only MAEs are 0.43 and 0.28. The result is consistent with sensitivity to simultaneous input changes, including intermediate WWR values and the forest’s stepwise response, but does not isolate WWR as the sole cause. A paired-context bootstrap gives a descriptive Ridge-minus-interpolation demand-MAE difference of −1.42, with 95% interval [−1.65, −1.20]. The 64 simulated contexts do not represent a random sample of real buildings.

Original external subgroup | Contexts | MAE | Maximum error

Rectangle 5:1, 900 m² | 4 | 0.94 | 3.00

Wide-arm L, 750 m² | 4 | 0.72 | 1.45

Rectangle 2:1, 1500 m² | 4 | 0.70 | 1.87

Table 4. Three highest-MAE shape/area subgroups in the original external test. Each context contains six options. Full tables also report empirical 95th-percentile errors.

Subgroup reporting changes the practical interpretation of the pooled result: the elongated rectangle has approximately twice the aggregate MAE, and its worst individual error reaches 3.00. These empirical errors describe the tested cases rather than confidence bounds for a new query. The learning curve also gives external MAE 1.27, 0.66, 0.45 and 0.47 for 168, 360, 678 and 1,008 training rows. More samples do not guarantee monotonic improvement; these fixed-subset results were not used for external-test tuning.





6 Robustness and independent design application

6.1 Operation and geometry checks

At 900 m², 0° and WWR 0.4, one-factor tests change ventilation to 0.3/1.2 ACH, the occupancy profile to 07:00–20:00 at fraction 0.75, maximum RH to 60%, or humidity control to None. The schedule change alters both duration and fraction. Ventilation changes cooling intensity by about −15/+30 kWh thermal/(m² year), while the extended profile adds about 40. Saving percentages shift by up to 4.04 percentage points. Small humidity-control effects in this ideal-loads setup do not establish that real dehumidification electricity is unimportant.

Matched one- and five-zone rectangles differ by at most 1.90% in cooling demand and 0.27 percentage points in reduction. The 24- versus 48-gon circle differs by at most 0.55% across six options at one reference context. These checks support the declared simplifications only within their tested scope; neither establishes adequacy for arbitrary irregular or partitioned buildings.

6.2 Daylight screen and decision comparator

EnergyPlus SplitFlux evaluates nine points at 10%, 50% and 90% of each rectangular dimension, 0.8 m above the floor. Lighting-control fractions are zero. Mean point DA300 is the average percentage of occupied weekday hours reaching 300 lux, using hours ending 10:00–18:00. A study screen of at least 50% defines feasibility. It is neither spatial daylight autonomy nor a glare or regulatory compliance assessment. Feasibility is supplied by simulation to both selectors; there is no learned daylight model.

The original 900 m², 2:1 rectangle at 0° and WWR 0.2 illustrates the tradeoff: shaded SN40/23 gives cooling 99.45 but mean DA300 36.90%; shaded SN70/35 gives 102.77 and 77.46%. The screen therefore costs 3.31 thermal units per m² per year. These original thermal conditions occur in training, so they demonstrate the workflow rather than independent decision accuracy.

New context | WWR | Simulated best | Model and rule

1.5:1; 850 m²; 30° | 20% | SN70/35 + 0.6 m | Both match

1.5:1; 850 m²; 30° | 40% | SN40/23 + 0.6 m | Both match

3:1; 1100 m²; 60° | 20% | SN70/35 + 0.6 m | Both match

3:1; 1100 m²; 60° | 40% | SN40/23 + 0.6 m | Both match

Table 5. Independent daylight contexts, each with six options. The simple rule chooses minimum SHGC among feasible options, breaking ties by deeper shading and then product name.

The 24 new daylight cases have cooling MAE 0.47. Both selectors have zero selection loss relative to the simulated feasible optimum in all four contexts. This supports bounded prediction accuracy but demonstrates no model selection advantage over the rule. The additional 600 m² wide-arm L at 0° and WWR 0.4 has MAE 0.63 and maximum error 1.38 across six thermal cases. Across five new contexts, 75 within-context option pairs have difference MAE 0.52 and ordering agreement 97.3%; these dependent pairs are not 75 independent observations.





7 Practical use and limitations

The defensible design application is repeated quantitative comparison within a stated domain. A designer selects a plan, area, orientation and WWR, compares six facade combinations, checks whether matching simulations exist, and reviews daylight only where available. The interface distinguishes exact simulation matches, evidence at other conditions of the same shape, and unsupported combinations. It displays tested conditions rather than treating every permitted input as validated. In particular, the added 600 m² L case validates one combination, not all small L-shaped offices.

Thermal-only rankings should not be reported as comprehensive recommendations. Where daylight results are absent, the interface states that only cooling can be compared. The geometric-distance flag is a novelty heuristic, not an error probability; empirical subgroup errors likewise should not be displayed as individual confidence intervals. An uncertainty-aware approach such as [6] is a possible extension, but would still address surrogate error separately from assumptions about real buildings.

Nine sequential simulations have median runtime 1.21 s, while a preloaded single-case prediction took 0.198 ms in the original benchmark. Generating 1,008 training cases at the same median implies about 20.3 minutes and a break-even near 1,008 additional individual-case queries, before validation and engineering effort. A subsequent 20-request local test measured roughly 3 ms for a full six-option HTTP response, excluding browser rendering and startup. Few one-off designs remain cheap to simulate directly. These timings support interactive use, not a claim of universal computational necessity.

The study covers one typical climate, selected regular polygons, two L outlines, assumed constructions, fixed baseline operation and three linked glazing products. It excludes arbitrary concave forms, atria, furniture, partitions, urban shading, detailed HVAC electricity, cost and embodied impacts. Nonrectangular training uses only 900 m²; tests at other areas are discrete. Daylight remains limited to rectangular examples. These restrictions help explain why a smooth response surface succeeds and why a simple rule can tie the model in selection. The findings should not be extended to measured electricity or whole-project optimum design.

8 Reproducibility and conclusions

The local package includes source inputs and hashes, generated IDFs, compact records and warning logs, fixed scripts, result tables, an executed seven-cell notebook and the interface. Original and follow-up matrices remain separate. All 1,920 runs contain 8,760 hours and no severe errors. Warning categories are retained, including daylight warnings consistent with omitted glare and zero controlled-light fractions. Successful execution is not physical validation. A newly created Python 3.12.14 virtual environment installed from requirements.txt reran analysis, figures and verification in an independently extracted project copy with PYTHONPATH removed and user-site packages disabled. All 60 original model-metric rows matched exactly and the dependency check passed. This was the same Windows machine, not an independent computer or a full rerun of all original simulations.

The study concludes that a regularised response surface predicts demand and paired effects accurately within the tested simulation domain, while whole-family tests and subgroup errors expose limits hidden by pooled metrics. Operating assumptions change saving percentages. Daylight screening produces a meaningful facade tradeoff, but independent agreement with a simple rule provides no evidence that the surrogate improves intervention selection. The practical contribution is reproducible, bounded estimation with explicit evidence coverage. Future work should prioritise independent nonrectangular daylight validation, realistic operating uncertainty and calibrated decision risk before expanding the interface’s claims.

References

[1] Amasyali, K., and El-Gohary, N. M. (2018). A review of data-driven building energy consumption prediction studies. Renewable and Sustainable Energy Reviews, 81, 1192–1205.

https://doi.org/10.1016/j.rser.2017.04.095

[2] Westermann, P., and Evins, R. (2019). Surrogate modelling for sustainable building design – A review. Energy and Buildings, 198, 170–186.

https://doi.org/10.1016/j.enbuild.2019.05.057

[3] Thrampoulidis, E., Mavromatidis, G., Lucchi, A., and Orehounig, K. (2021). A machine learning-based surrogate model to approximate optimal building retrofit solutions. Applied Energy, 281, 116024.

https://doi.org/10.1016/j.apenergy.2020.116024

[4] Jowett-Lockwood, L., and Evins, R. (2025). Examining the generalizability of inverse surrogate models for different geometries and locations. Energy and Buildings, 335, 115539.

https://doi.org/10.1016/j.enbuild.2025.115539

[5] Qiblawi, S., Touchie, M., and Azar, E. (2026). Integrating building geometry changes into reduced-order modeling for rapid retrofit performance assessment. Proceedings of eSim 2026, 783–790.

https://doi.org/10.26868/31114504.2026.77

[6] Westermann, P., and Evins, R. (2021). Using Bayesian deep learning approaches for uncertainty-aware building energy surrogate models. Energy and AI, 3, 100039.

https://doi.org/10.1016/j.egyai.2020.100039

[7] Pilechiha, P., Mahdavinejad, M., Pour Rahimian, F., Carnemolla, P., and Seyedzadeh, S. (2020). Multi-objective optimisation framework for designing office windows: quality of view, daylight and energy efficiency. Applied Energy, 261, 114356.

https://doi.org/10.1016/j.apenergy.2019.114356

[8] Kangazian, A., and Emadian Razavi, S. Z. (2023). Multi-criteria evaluation of daylight control systems of office buildings considering daylighting, glare and energy consumption. Solar Energy, 263, 111928.

https://doi.org/10.1016/j.solener.2023.111928

[9] Seghier, T. E., Sepúlveda, A., Lim, Y.-W., and Mesloub, A. (2024). Optimising thermal-daylight performance in tropical open-plan offices: A coupled OTTV and daylight prediction approach. Journal of Building Engineering, 98, 111369.

https://doi.org/10.1016/j.jobe.2024.111369

[10] Kapoor, S., and Narayanan, A. (2023). Leakage and the reproducibility crisis in machine-learning-based science. Patterns, 4(9), 100804.

https://doi.org/10.1016/j.patter.2023.100804

[11] City Syntax Lab. Buildings.sg office template, 06_Office_SGP_2025_V5.idf. Model source.

https://github.com/City-Syntax/buildings.sg

[12] Ladybug Tools. Singapore IWEC weather, WMO 486980. Weather input.

https://github.com/ladybug-tools/uwg/blob/master/resources/SGP_Singapore.486980_IWEC.epw

[13] EnergyPlus (2024). Version 24.2 Input Output Reference. Ideal-loads and daylighting objects.

https://bigladdersoftware.com/epx/docs/24-2/input-output-reference/

[14] Guardian Glass (2025). Coated Glass digital selector, p. 2. 6–16–4 double glazing with 90% argon.

https://www.guardianglass.com/content/dam/guardianindustriesholdings/technical-center/europe/architectural/digital-glass-selector/Guardian-Glass-Digital-Selector-EN.pdf

[15] Scikit-learn. Cross-validation: evaluating estimator performance. Grouped cross-validation documentation.

https://scikit-learn.org/stable/modules/cross_validation.html