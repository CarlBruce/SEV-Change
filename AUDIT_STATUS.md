# Semantic-Equivalence Audit Status

This page reports the author's recorded stratified-sample decisions. It does not assert that all 408,184 question expressions in the candidate package were independently reviewed.

## Review sample and decision history

The author supplied a 1,400-pair review workbook: 700 original-question/variant pairs from RSRCC-V and 700 from DisasterM3-V, with 100 pairs per transformation per source. Three reviewers recorded judgments for every pair. Initial judgments agreed on 1,280 pairs (91.43%); 120 pairs involved disagreement or uncertainty. The senior-review field is populated for 278 pairs.

The earlier `v2.3` workbook recorded 1,358 equivalent and 42 non-equivalent final judgments. In the author-supplied `v2.4_42_人工裁定` workbook dated 2026-09-25, all 42 were re-adjudicated as equivalent; its final-judgment column therefore records 1,400 equivalent and zero non-equivalent pairs. The three initial-review columns were not changed. The source workbook's summary had retained the older 1,358/42 static values; a separate `v2.5` synchronized working copy links the summary to the final-judgment counts.

Six of the 42 DisasterM3 variants were also rewritten to restore the original target category or task, and the author separately confirmed the revised text as equivalent. Their sample IDs are S0726, S0739, S0826, S1009, S1078, and S1287. The `v2.5` working copy and candidate archive `v0.1.0-rc2` use these revised strings; the earlier workbooks and archive retain the old strings. Thus the six revised-text decisions must not be read as retroactive validation of the old strings.

## Evidence limits

The author-supplied re-adjudication workbook records the decisions but not per-pair adjudication reasons for the 42 changed judgments. The full reviewer workbook is not included in the public candidate archive. The 1,400/1,400 result is an observed result for this stratified sample, **not** a measured full-dataset equivalence rate or proof that every automatic variant is equivalent. Initial agreement is not a chance-corrected inter-annotator statistic. A reportable Fleiss' kappa and reproducible details of the AI risk-prompting system are not available.

Structural and SHA-256 checks establish package integrity only. Further image/answer/mask-grounded review, a shareable per-pair adjudication trail, and the unresolved RSRCC duplicate-identity audit remain important for a frozen research release.

## Model-result version boundary

The manuscript's seven-model predictions were produced before the six text revisions and were not rerun on `v0.1.0-rc2`. Existing aggregate scores describe the earlier evaluated candidate, not the corrected six strings. Do not attribute score changes or a revised robustness estimate to the re-adjudication without a common-version rerun.
