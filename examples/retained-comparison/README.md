# Synthetic retained comparison

This is a synthetic fixture, not a new scientific experiment or a claim about Pinyin-VSR. Every metric is invented for this example. This source folder contains no managed task record; the [M2 verification record](../../docs/M2-VERIFICATION.md) documents successful verification of disposable copies.

The contract asks whether a candidate improves the baseline by at least 0.01 absolute error units. Baseline error is 0.20 and candidate error is 0.23. Gain is baseline minus candidate, or −0.03, so the correct bounded result is no promotion. The task can complete even though the candidate loses.

Files demonstrate a command criterion and an evidence-review criterion:

- [contract.md](contract.md): frozen-rule input example.
- [result.md](result.md): a negative finding satisfying the task's purpose.
- [reviews.json](reviews.json): an illustrative review input, not a record of independent review.
- [metrics.json](evidence/metrics.json) and [derived.json](evidence/derived.json): synthetic inputs and arithmetic.
- [check_arithmetic.py](check_arithmetic.py): a runnable example verifier, with no rctl dependency.

From this directory, run the example check with:

```sh
uv run --offline --no-project python check_arithmetic.py
```

It detects inconsistent metric direction, arithmetic, or promotion labeling in the synthetic evidence. M2 integration tests and the installed-package smoke copy this folder into a temporary project's `tasks/retained-comparison`, call begin, verify with reviews, and close. The smoke also omits the review and observes unknown with phase active before supplying it. The fixture's prewritten result specifies expected behavior; a real task writes its result after the governed work.
