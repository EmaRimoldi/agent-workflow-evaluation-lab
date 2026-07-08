# Validity Filter

This file defines which probes are used for the public agent-memory ablation
claims.

## Canonical Analysis Set

The canonical public figures use these probes:

| Probe | Status | Reason |
| --- | --- | --- |
| `P02` | valid | parallel mixed search styles, no memory |
| `P03` | valid | single-agent control |
| `P04` | valid | 30-second train-evaluation check |
| `P09` | valid | longer parallel mixed-style no-memory reference |
| `P10` | valid | parallel same-style no-memory reference |
| `P11` | valid | exploratory search without memory |
| `P12` | valid | exploratory search with shared memory |
| `P13` | valid | two exploratory agents without memory |
| `P15` | valid | seeded learning-rate hint |
| `P16` | valid | starts from seeded baseline |
| `P17` | valid | shared plus private memory |

These 11 probes contribute 247 training records.

## Excluded From Outcome Claims

| Probe | Status | Reason |
| --- | --- | --- |
| `P01` | context-only | older training template used about 315 seconds per attempt |
| `P05` | excluded | private-memory context was configured but empty |
| `P06` | excluded | shared-memory log was configured but empty |
| `P07` | excluded | shared-memory log was configured but empty |
| `P08` | excluded | private-memory context was configured but empty |
| `P14` | not run | planned private-memory probe did not execute |
| `P18` | not run | planned seeded parallel probe did not execute |

`P05`-`P08` are retained only as operational evidence that the memory pipeline
could silently fail. They are not valid private-memory or shared-memory tests.

The valid shared-memory evidence comes primarily from `P12` and `P17`.
