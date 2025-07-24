import time

session_start_time = 0
collect_end_time = 0
testloop_start_time = 0
session_end_time = 0
runtest_reports = []


def duration_to_str(duration, signs=4):
    return f"{duration:.{signs}f} sec"


def pytest_sessionstart(session):
    global session_start_time
    session_start_time = time.perf_counter()
    global runtest_reports
    runtest_reports = []


def pytest_collection_finish(session):
    global collect_end_time
    collect_end_time = time.perf_counter()


def pytest_runtestloop(session):
    global testloop_start_time
    testloop_start_time = time.perf_counter()


def pytest_runtest_logreport(report):
    # print()
    # print(">>> report: ", report.when)
    runtest_reports.append(report)


def pytest_sessionfinish(session, exitstatus):
    width = 13
    global session_end_time
    session_end_time = time.perf_counter()
    session_duration = session_end_time - session_start_time
    collection_duration = collect_end_time - session_start_time
    total_calls = [report for report in runtest_reports if report.when == "call"]
    total_calls_duration = sum(report.duration for report in total_calls)
    passed_calls = [report for report in total_calls if report.outcome == "passed"]
    passed_calls_duration = sum(report.duration for report in passed_calls)
    setups_duration = sum(report.duration for report in runtest_reports if report.when == "setup")

    print()
    print()
    print("total time".ljust(width), ":", duration_to_str(session_duration))
    print("collec time".ljust(width), ":", duration_to_str(collection_duration))
    print("setups time".ljust(width), ":", duration_to_str(setups_duration))
    if len(passed_calls) == len(total_calls):
        print("calls time".ljust(width), ":", duration_to_str(passed_calls_duration))
    else:
        print("calls time".ljust(width), ":",
              f"{duration_to_str(passed_calls_duration)} / {duration_to_str(total_calls_duration)}")
    if passed_calls:
        print("avg call time".ljust(width), ":", duration_to_str(passed_calls_duration / len(passed_calls)))
    print("passed".ljust(width), ":", f"{len(passed_calls)} / {len(total_calls)}",
          end='')
