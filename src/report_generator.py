"""
Report generator for LLM Prompt Injection Tester v1.
"""

from datetime import datetime


def count_results_by_status(results):
    """Count passed and failed tests."""
    passed = 0
    failed = 0

    for result in results:
        if result.get("passed"):
            passed += 1
        else:
            failed += 1

    return passed, failed


def count_results_by_risk(results):
    """Count how many results fall into each risk level."""
    counts = {
        "low": 0,
        "medium": 0,
        "high": 0,
        "critical": 0,
    }

    for result in results:
        risk_level = result.get("risk_level", "low")

        if risk_level in counts:
            counts[risk_level] += 1

    return counts


def get_overall_risk_rating(risk_counts):
    """Assign an overall risk rating based on the worst result found."""
    if risk_counts.get("critical", 0) > 0:
        return "critical"

    if risk_counts.get("high", 0) > 0:
        return "high"

    if risk_counts.get("medium", 0) > 0:
        return "medium"

    return "low"


def format_bool(value):
    """Format boolean values for the report."""
    return "PASS" if value else "FAIL"


def generate_markdown_report(results, mode="mock", model_name="llama3"):
    """Generate a Markdown report string from evaluated test results."""
    total_tests = len(results)
    passed_tests, failed_tests = count_results_by_status(results)
    risk_counts = count_results_by_risk(results)
    overall_risk = get_overall_risk_rating(risk_counts)

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report_lines = [
        "# LLM Prompt Injection Tester Report",
        "",
        "## Summary",
        "",
        f"- Created at: {created_at}",
        f"- Mode: `{mode}`",
        f"- Model: `{model_name}`",
        f"- Total tests: {total_tests}",
        f"- Passed tests: {passed_tests}",
        f"- Failed tests: {failed_tests}",
        f"- Overall risk rating: `{overall_risk}`",
        "",
        "## Risk Counts",
        "",
        f"- Low: {risk_counts['low']}",
        f"- Medium: {risk_counts['medium']}",
        f"- High: {risk_counts['high']}",
        f"- Critical: {risk_counts['critical']}",
        "",
        "## Safety Note",
        "",
        (
            "This report was generated using controlled prompt-injection tests with "
            "fake secrets, fake internal notes, and simulated data only. It is intended "
            "for defensive AI security learning and portfolio demonstration."
        ),
        "",
        "## Test Results",
        "",
    ]

    for result in results:
        report_lines.extend(
            [
                f"### {result.get('test_id', 'UNKNOWN')} - {result.get('category', 'Unknown')}",
                "",
                f"- Status: **{format_bool(result.get('passed', False))}**",
                f"- Risk level: `{result.get('risk_level', 'unknown')}`",
                f"- Reason: {result.get('reason', '')}",
                f"- Recommended mitigation: {result.get('recommended_mitigation', '')}",
                "",
                "<details>",
                "<summary>Prompt and Response</summary>",
                "",
                "#### Prompt",
                "",
                "```text",
                result.get("prompt", ""),
                "```",
                "",
                "#### Response",
                "",
                "```text",
                result.get("response", ""),
                "```",
                "",
                "</details>",
                "",
            ]
        )

    return "\n".join(report_lines)


def save_markdown_report(results, output_path, mode="mock", model_name="llama3"):
    """Save a Markdown report to disk."""
    report = generate_markdown_report(
        results=results,
        mode=mode,
        model_name=model_name,
    )

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(report)

    return output_path
