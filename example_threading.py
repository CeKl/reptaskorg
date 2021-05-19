import datetime
import time
from reptaskorg import RepTaskOrgTH


def do_something(alarm_number):
    """Function which should be executed repeatedly."""

    print('{} - ALARM {}'.format(
        datetime.datetime.now().strftime('%H:%M:%S:%f'),
        alarm_number
    ))


def do_anotherthing(alarm_number, alarm_comment):
    """Function which should be executed repeatedly with multiple arguments."""

    print('{} - ALARM {} {}'.format(
        datetime.datetime.now().strftime('%H:%M:%S:%f'),
        alarm_number,
        alarm_comment
    ))


def main():
    """Main-Function."""

    # Define tasks with desired time stamps.
    task_1 = RepTaskOrgTH(do_something, 1, second=[0, 10, 20, 30, 40, 50])

    # Define multiple arguments for given function at task
    task_2 = RepTaskOrgTH(do_anotherthing, 2, 'test_2', minute=[33, 34, 36], second=[0, 10, 20, 30, 40, 50])

    # Main-loop for other tasks
    while True:
        time.sleep(0.001)


if __name__ == "__main__":
    main()
