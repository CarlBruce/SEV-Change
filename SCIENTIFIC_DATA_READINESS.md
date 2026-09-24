# Scientific Data Submission Readiness

This is a gap assessment for a possible *Scientific Data* Data Descriptor, not a declaration of journal compliance. It follows the journal's [submission guidelines](https://www.nature.com/sdata/publish/submission-guidelines), [data policies](https://www.nature.com/sdata/policies/data-policies), [repository guidance](https://www.nature.com/sdata/policies/repositories), and [code-availability policy](https://www.nature.com/sdata/policies/editorial-and-publishing-policies).

| Requirement | Current evidence | Remaining action |
|---|---|---|
| Reviewer access to complete described data | Seven downloadable ZIP parts, checksummed by `release/parts.json`; 11 JSON files checked against `manifest.json` | Test anonymous download and archive reconstruction from a clean environment before submission |
| Formal, persistent data deposition | GitHub candidate only; no verified dataset DOI | Deposit the frozen dataset in an appropriate long-term repository, provide a persistent identifier and exact version, and update the manuscript. The journal requires formal repository deposition from the second review round onward |
| Data Records: files, formats, fields and provenance | `DATA_DICTIONARY.md`, `SOURCES.md`, `EXCLUSIONS.md`, `manifest.json` | Pin the exact upstream source versions and document the source-image access/alignment procedure |
| Technical Validation | Machine structure/hash checks; stratified human-review summary in `AUDIT_STATUS.md` | Re-adjudicate 42 disputed labels, document reasons, freeze quality status and rerun affected metrics |
| Code Availability | Archive and dataset validators are available | Publish the actual transformation-generation, inference, normalization and scoring code with parameters and reproducible environment details |
| Reuse rights | Source terms documented in `LICENSE_STATUS.md`; uploader attested redistribution rights | Establish and publish a precise downstream license for derivative annotations, consistent with upstream rights; code licensing can be separate |
| Citation and versioning | Candidate identifier `v0.1.0-rc1`; no final paper metadata | Mint/verify DOI, create an immutable release tag, add correct dataset/paper citation metadata, and synchronize all documentation |

The journal expects Data Descriptors to explain data creation, records, technical quality, access and use. Repository documentation cannot substitute for a complete manuscript or resolve missing rights and archival decisions. `RELEASE_CHECKLIST.md` tracks the operational steps.
