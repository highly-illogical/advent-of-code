def read_input(filename: str) -> list[int]:
    """Reads input from file and returns a list of reports."""
    reports = []
    with open(filename) as file:
        for line in file:
            report = [int(level) for level in line.strip("\n").split(" ")]
            reports.append(report)
    return reports

def differences(report):
    return list(map(lambda x, y: y - x, report[:-1], report[1:]))

def difference_safety(d, sign):
    return d * sign > 0 and abs(d) <= 3

def check_report_safety_functional(report):
    diff = differences(report)
    sign = 1 if diff[0] > 0 else (0 if diff[0] == 0 else -1)
    diff_safe = [difference_safety(d, sign) for d in diff]
    return abs(sum(diff_safe)) == len(diff_safe)

def check_report_safety(report: list[int]) -> bool:
    """Takes a report as input and checks whether it's safe or not."""

    if len(report) < 1:
        raise ValueError("Report is empty")

    if len(report) == 1:
        return True
    
    sign = 1 if (report[1] - report[0] > 0) else -1

    for i in range(1, len(report)):
        difference = (report[i] - report[i-1]) * sign

        if difference <= 0 or difference > 3:
            return False

    return True

def check_report_safety_with_dampener(report: list[int], check_safety = check_report_safety) -> bool:
    """Takes a report as input and checks whether it's safe after applying the dampener."""

    if check_safety(report):
        return True

    for i in range(len(report)):
        damped_report = report[:i] + report[i+1:]
        if check_safety(damped_report):
            return True

    return False

def count_safe_reports(reports: list[list[int]], dampener: bool = False) -> int:
    if not dampener:
        return sum(int(check_report_safety(report)) for report in reports)
    else:
        return sum(int(check_report_safety_with_dampener(report)) for report in reports)        

if __name__ == '__main__':
    reports = read_input("input.txt")
    print(sum(check_report_safety_with_dampener(report, check_safety=check_report_safety_functional) for report in reports))