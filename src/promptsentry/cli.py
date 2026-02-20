from pathlib import Path
import json
import argparse
import csv

from .detector import PromptSentryDetector


def risk_label(score: int) -> str:
    if score >= 18:
        return "HIGH"
    if score >= 10:
        return "MEDIUM"
    return "LOW"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--field", default="content")
    parser.add_argument("--min-score", type=int, default=8)
    parser.add_argument("--out", type=Path, default=None)

    args = parser.parse_args()

    detector = PromptSentryDetector()

    total = 0
    flagged = 0

    # 1) Scan and print to console (supports JSONL and CSV)
    suffix = args.input.suffix.lower()

    if suffix == ".jsonl":
        with args.input.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue

                total += 1

                record = json.loads(line)
                text = str(record.get(args.field, ""))

                result = detector.analyze(text)

                if result.score >= args.min_score:
                    flagged += 1
                    label = risk_label(result.score)

                    print("\n---")
                    print(f"Line {line_no} | score={result.score} | risk={label}")
                    print(text)

                    for finding in result.findings:
                        print(f"  - {finding.rule_name} (sev={finding.severity}): {finding.description}")
                        if finding.matches:
                            print(f"    matches: {finding.matches[:2]}")

    elif suffix == ".csv":
        with args.input.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row_no, row in enumerate(reader, start=1):
                total += 1
                text = str(row.get(args.field, ""))

                result = detector.analyze(text)

                if result.score >= args.min_score:
                    flagged += 1
                    label = risk_label(result.score)

                    print("\n---")
                    print(f"Row {row_no} | score={result.score} | risk={label}")
                    print(text)

                    for finding in result.findings:
                        print(f"  - {finding.rule_name} (sev={finding.severity}): {finding.description}")
                        if finding.matches:
                            print(f"    matches: {finding.matches[:2]}")

    else:
        raise SystemExit("Unsupported file type. Use .jsonl or .csv")

    # 2) Optional findings CSV export (always exports flagged findings)
    if args.out:
        with args.out.open("w", newline="", encoding="utf-8") as f_out:
            writer = csv.writer(f_out)
            writer.writerow(["row_or_line", "score", "risk", "text", "rule"])

            if suffix == ".jsonl":
                with args.input.open("r", encoding="utf-8") as f_in:
                    for line_no, line in enumerate(f_in, start=1):
                        line = line.strip()
                        if not line:
                            continue

                        record = json.loads(line)
                        text = str(record.get(args.field, ""))

                        result = detector.analyze(text)
                        if result.score >= args.min_score:
                            label = risk_label(result.score)
                            for finding in result.findings:
                                writer.writerow([line_no, result.score, label, text, finding.rule_name])

            elif suffix == ".csv":
                with args.input.open("r", encoding="utf-8") as f_in:
                    reader = csv.DictReader(f_in)
                    for row_no, row in enumerate(reader, start=1):
                        text = str(row.get(args.field, ""))

                        result = detector.analyze(text)
                        if result.score >= args.min_score:
                            label = risk_label(result.score)
                            for finding in result.findings:
                                writer.writerow([row_no, result.score, label, text, finding.rule_name])

        print(f"\nWrote findings CSV: {args.out}")

    # 3) Summary
    print("\n===")
    print(f"Scanned {total} records")
    print(f"Flagged {flagged} records")

    return 0