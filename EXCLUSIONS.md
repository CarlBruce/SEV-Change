# Exclusion Record

The source DisasterM3 variant files contained 30,042 records. This SEV-Change release keeps 29,024 records that have both `pre_image_path` and `post_image_path`.

Exactly 1,018 records were excluded because they are single-image `Relational Reasoning` samples. They use `image_path` and lack the paired pre-/post-disaster inputs required by the benchmark definition.

| Category | Excluded records |
|---|---:|
| earthquake | 258 |
| explosion | 63 |
| fire | 30 |
| flood | 208 |
| hurricane | 228 |
| landslide | 12 |
| tornado | 75 |
| tsunami | 84 |
| volcano | 60 |
| conflict | 0 |
| **Total** | **1,018** |

The exclusion can be reproduced with:

```bash
python scripts/filter_bitemporal_records.py INPUT.json OUTPUT.json
```

The script refuses to remove a missing-pair record unless it is also identified as a single-image `Relational Reasoning` sample with an `image_path` field.
