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

    # Define tasks with desired timestamps.
    task_1 = RepTaskOrgTH(do_something, 1, second=[0, 10, 20, 30, 40, 50])

    # Define multiple arguments for given function at task
    task_2 = RepTaskOrgTH(do_anotherthing, 2, 'test_2', minute=[33, 34, 36], second=[0, 10, 20, 30, 40, 50])

    # Show set time for timer 1
    print('active timer 1 settings: {}'.format(task_1.set_timer))

    # Show current run-status for timer 1
    print(task_1.task_running())

    # Main-loop for other tasks
    run_loop = True
    while run_loop:
        time.sleep(0.0000001)

    task_1.stop_task()
    task_2.stop_task()


if __name__ == "__main__":
    main()
