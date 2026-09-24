# Semantic-Equivalence Audit Status

This file distinguishes the recorded review outcomes from the current release decision. It does not claim that all variants are semantically equivalent.

## Recorded review

The dataset author supplied and confirmed a stratified review workbook (`v2.3`, dated 2026-09-24). It contains 1,400 original-question/variant pairs: 700 from RSRCC-V and 700 from DisasterM3-V, with 100 pairs per transformation per source. Three reviewers recorded judgments for every pair. They agreed on 1,280 pairs (91.43%); 120 pairs had disagreement or uncertainty. The senior-review judgment field is populated for 278 pairs.

The original workbook's final-judgment column contains 1,358 “equivalent” and 42 “non-equivalent” labels. These are **recorded labels for the stratified sample**, not a guarantee for the full dataset or a final quality rate. The initial agreement percentage is not a chance-corrected inter-annotator agreement statistic. A reportable Fleiss' kappa and reproducible details of the AI risk-prompting system are not available.

## Pending re-adjudication

All 42 originally non-equivalent pairs are marked `待重新裁定` (“pending re-adjudication”) in the author's `v2.4` working workbook. The original reviewer judgments and final-judgment column remain unchanged there. Some pairs appear textually similar despite the original negative label, and the recorded senior-review reasons are incomplete. **Do not automatically delete all 42 or treat their original labels as confirmed corrections.**

The working audit workbooks are not part of this public candidate archive. No correction, exclusion, or re-scored model result is asserted by this repository. Before a frozen benchmark release, each pending pair needs a documented decision using the source images, question, answer, options and, for segmentation, target mask. Corrected question text must be rechecked; unresolved pairs must be excluded from strict equivalence scoring. The dataset and affected seven-model metrics then need a common-version rerun.

## Scope of existing model results

The candidate manuscript reports model results generated before the pending re-adjudication. Those results are provisional. They should not be interpreted as noise-free estimates of semantic-invariance robustness.
