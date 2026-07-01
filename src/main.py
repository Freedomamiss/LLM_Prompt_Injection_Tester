"""
Main command-line entry point for LLM Prompt Injection Tester v1.
"""

import argparse
import json
from pathlib import Path

from report_generator import save_markdown_report
from test_runner import run_tests


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_JSON_OUTPUT = PROJECT_ROOT / "examples" / "sample_results.json"
DEFAULT_REPORT_OUTPUT = PROJECT_ROOT / "examples" / "sample_report.md"


def save_json_results(results, output_path):
    """Save evaluated test results to a JSON file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)

    return output_path


def print_summary(results, json_output_path, report_output_path):
    """Print a short command-line summary after the tests run."""
    total_tests = len(results)
    passed_tests = sum(1 for result in results if result.get("passed"))
    failed_tests = total_tests - passed_tests

    risk_counts = {
        "low": 0,
        "medium": 0,
        "high": 0,
        "critical": 0,
    }

    for result in results:
        risk_level = result.get("risk_level", "low")

        if risk_level in risk_counts:
            risk_counts[risk_level] += 1

    print("\nLLM Prompt Injection Tester v1")
    print("-" * 35)
    print(f"Total tests: {total_tests}")
    print(f"Passed:      {passed_tests}")
    print(f"Failed:      {failed_tests}")
    print("")
    print("Risk counts:")
    print(f"  Low:      {risk_counts['low']}")
    print(f"  Medium:   {risk_counts['medium']}")
    print(f"  High:     {risk_counts['high']}")
    print(f"  Critical: {risk_counts['critical']}")
    print("")
    print(f"JSON results saved to: {json_output_path}")
    print(f"Markdown report saved to: {report_output_path}")
    print("")


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Run safe, simulated prompt-injection tests against a mock model "
            "or a local Ollama model."
        )
    )

    parser.add_argument(
        "--mode",
        choices=["mock", "ollama"],
        default="mock",
        help="Model backend to use. Default: mock",
    )

    parser.add_argument(
        "--model",
        default="llama3",
        help="Ollama model name to use when --mode ollama is selected. Default: llama3",
    )

    parser.add_argument(
        "--json-output",
        default=str(DEFAULT_JSON_OUTPUT),
        help="Path where JSON results should be saved.",
    )

    parser.add_argument(
        "--report-output",
        default=str(DEFAULT_REPORT_OUTPUT),
        help="Path where the Markdown report should be saved.",
    )

    return parser.parse_args()


def main():
    """Run the command-line tool."""
    args = parse_arguments()

    json_output_path = Path(args.json_output)
    report_output_path = Path(args.report_output)

    try:
        results = run_tests(
            mode=args.mode,
            model_name=args.model,
        )

        save_json_results(results, json_output_path)

        save_markdown_report(
            results=results,
            output_path=report_output_path,
            mode=args.mode,
            model_name=args.model,
        )

        print_summary(
            results=results,
            json_output_path=json_output_path,
            report_output_path=report_output_path,
        )

    except Exception as error:
        print("\nAn error occurred while running the tester.")
        print(f"Error: {error}")
        raise


if __name__ == "__main__":
    main()
