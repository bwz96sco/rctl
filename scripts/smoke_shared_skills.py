"""Native experiment compatibility using installed-wheel skill assets by default."""

import json
import re
import shutil
import subprocess

import yaml


def walkthrough(cli, project, repo, skills_root, python):
    task_name = "tasks/native-experiment"
    task = project / task_name
    source = skills_root / "skills/research-experiment"
    cli(
        "task",
        "new",
        task_name,
        "--kind",
        "analysis",
        "--title",
        "Native experiment smoke",
    )
    contract_text = (source / "assets/experiment-contract.md").read_text()
    metadata, body = contract_text[4:].split("\n---\n", 1)
    # Validate the unedited domain template metadata against schemas from the wheel.
    for kind, template in (
        ("contract", "experiment-contract.md"),
        ("result", "result-template.md"),
    ):
        subprocess.run(
            [
                str(python),
                "-c",
                "import sys, yaml; from rctl.documents import validate_schema; "
                "validate_schema(yaml.safe_load(sys.stdin.read().split('---')[1]), 'shared template', sys.argv[1])",
                kind,
            ],
            input=(source / "assets" / template).read_text(),
            text=True,
            check=True,
            capture_output=True,
        )
    contract = yaml.safe_load(metadata)
    contract.update(
        task_id=task.name, title="Check a retained synthetic negative comparison"
    )
    evidence = ["result.md", "evidence/metrics.json", "evidence/derived.json"]
    contract["criteria"] = [
        {
            "id": "AC-01",
            "requirement": "Recompute the retained synthetic gain and promotion decision.",
            "evidence_refs": evidence[1:],
            "failure_action": "Correct arithmetic or leave the claim unresolved.",
            "method": {
                "type": "command",
                "argv": [str(python), "check_arithmetic.py"],
                "timeout_seconds": 10,
                "inputs": ["check_arithmetic.py", *evidence[1:]],
            },
        },
        {
            "id": "AC-02",
            "requirement": "Inspect comparability and confine the negative claim to synthetic aggregates.",
            "evidence_refs": evidence,
            "failure_action": "Correct interpretation or leave review unresolved.",
            "method": {"type": "review", "reviewer": "either"},
        },
        {
            "id": "AC-03",
            "requirement": "The domain result has completed provenance and evidence fields.",
            "evidence_refs": ["result.md"],
            "failure_action": "Fill missing domain evidence fields.",
            "method": {
                "type": "command",
                "argv": [str(python), "validate-result.py", "."],
                "timeout_seconds": 10,
                "inputs": ["validate-result.py", "contract.md", "result.md"],
            },
        },
    ]
    replacements = {
        "<bounded question>": "Does the retained candidate meet the +0.01 gain rule?",
        "<supplied|problem|candidate>": "supplied",
        "<stable-id-or-C#>": "rctl-synthetic-fixture",
        "<bounded-role; problem_validation for a problem origin>": "method_comparison",
        "<operationalized negative result>": "Baseline minus candidate below +0.01 declines promotion.",
        "<complete-method benefit, conditional ablation, diagnosis/problem validation, or control screen>": "Retained synthetic comparison; no complete-method performance claim.",
        "<fixed ID/version, provenance and settings; distinguish main, published and enhanced controls>": "synthetic-control-v1: invented error 0.20 from evidence/metrics.json; no published or enhanced control.",
        "<one bounded change>": "Compare invented candidate error 0.23.",
        "<shared raw inputs/tools, private generated records, permitted feedback and any diagnostic assistance>": "Both values come from the same retained fixture; no private records, feedback or diagnostic assistance.",
        "<fixed data, development exposure and held-out split>": "Retained synthetic aggregates; no dataset, development exposure or held-out claim.",
        "<primary endpoint, separate secondary/diagnostic metrics, direction and evaluator>": "Primary endpoint is error reduction; lower error is better. check_arithmetic.py uses decimal arithmetic; no secondary metrics.",
        "<seeds, aggregation, selection and claim rule>": "No seeds or population aggregation; gain must be at least +0.01.",
        "<runner and task-relative evidence paths>": "evidence/metrics.json and evidence/derived.json",
        "<supplied total and comparable per-arm generation/execution allowances; mark unresolved allocation>": "Both arms use retained invented values; local arithmetic and structure checks only, no generation or training.",
        "<existing authorization and storage policy>": "Disposable local synthetic fixture, no external writes.",
        "<Up to six bounded stop, kill, relaunch, or fallback rules; distinguish smoke from scientific runs.>": "Stop after the declared local checks; failures require correction before closure.",
        "<State whether bounded negative or inconclusive results satisfy the criteria.>": "A negative result closes when arithmetic and interpretation pass. Unknown review cannot close.",
        "<run>": "retained-input",
        "<smoke or claim-carrying>": "synthetic smoke",
        "<config>": "metrics.json",
        "<seeds>": "none",
        "<budget>": "local only",
        "<path>": "evidence/derived.json",
    }
    for before, after in replacements.items():
        body = body.replace(before, after)
    remaining = re.findall(r"<[^>]+>", body)
    assert not remaining, remaining
    (task / "contract.md").write_text(
        "---\n" + yaml.safe_dump(contract, sort_keys=False) + "---\n" + body
    )
    shutil.copy(repo / "examples/retained-comparison/check_arithmetic.py", task)
    shutil.copytree(repo / "examples/retained-comparison/evidence", task / "evidence")
    shutil.copy(source / "scripts/validate-result.py", task)
    cli("contract", "check", task_name)
    cli("begin", task_name)
    result = (
        (source / "assets/result-template.md")
        .read_text()
        .replace("replace-task-id", task.name)
    )
    result = result.replace("assessment: inconclusive", "assessment: not_supported")
    fields = {
        "Supported claim": "Synthetic gain is -0.03, below +0.01; decline promotion.",
        "Mechanism tested": "not_applicable",
        "Comparison scope": "Retained synthetic comparison; no complete-method performance claim.",
        "Actual run IDs": "retained-input; no newly trained model",
        "Commands, configs, and code state": "check_arithmetic.py and evidence/metrics.json copied from the rctl fixture",
        "Evidence references": "evidence/metrics.json and evidence/derived.json",
        "Failed or null runs": "No training runs; the synthetic comparison is negative.",
        "Aggregation": "Single retained synthetic aggregate; no population inference.",
        "Baseline relation": "synthetic-control-v1 error 0.20 versus candidate error 0.23; no enhanced control.",
        "Information condition": "Both values use the same invented metric fixture; no private records, feedback or diagnostic assistance.",
        "Endpoint results": "Primary error reduction is -0.03; the single synthetic pair regresses. Local checks only; no training costs or secondary metrics.",
        "Comparability": "Same invented metric and threshold; this is a fixture, not research performance evidence.",
        "Material amendments": "none; revision 1",
        "Deviations": "none",
        "Next action": "Stop after current checks and review pass.",
        "Reopen condition": "A changed fixture or a new scientific task.",
        "Durable promotions": "none",
        "Claims not made": "No model superiority, training validity, dataset inference, or host-delivery claim.",
    }
    for label, value in fields.items():
        result = re.sub(
            rf"(?m)^- {re.escape(label)}:.*$", f"- {label}: {value}", result
        )
    remaining = re.findall(r"<[^>]+>", result)
    assert not remaining, remaining
    (task / "result.md").write_text(result)
    cli("verify", task_name, expected=5)
    cli("close", task_name, expected=5)
    reviews = {
        "schema_version": 1,
        "task_id": task.name,
        "contract_revision": 1,
        "checks": [
            {
                "criterion_id": "AC-02",
                "reviewer": "agent",
                "verdict": "unknown",
                "rationale": "Synthetic negative test: review intentionally unresolved.",
                "evidence_refs": evidence,
            }
        ],
    }
    reviews_path = task / "reviews.json"
    reviews_path.write_text(json.dumps(reviews))
    cli("verify", task_name, "--reviews", f"{task_name}/reviews.json", expected=5)
    cli("close", task_name, expected=5)
    reviews["checks"][0].update(
        verdict="pass",
        rationale="Fixture review: 0.20 - 0.23 = -0.03 is below the fixed +0.01 threshold; result declines promotion and limits its claim to invented aggregates without training or population inference.",
    )
    reviews_path.write_text(json.dumps(reviews))
    # A valid review cannot rescue a failing actual arithmetic check.
    derived_path = task / "evidence/derived.json"
    original = derived_path.read_text()
    bad = json.loads(original)
    bad["promote"] = True
    derived_path.write_text(json.dumps(bad))
    cli("verify", task_name, "--reviews", f"{task_name}/reviews.json", expected=4)
    cli("close", task_name, expected=4)
    derived_path.write_text(original)
    cli("verify", task_name, "--reviews", f"{task_name}/reviews.json")
    closure = cli("close", task_name)["data"]["closure"]
    assert closure["assessment"] == "not_supported"
    return json.loads((task / ".rctl/record.json").read_text())
