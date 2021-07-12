import datetime
import time
from reptaskorg import RepTaskOrg


def do_something(alarm_number):
    """Function which should be executed repeatedly"""

    print('{} - ALARM {}'.format(
        datetime.datetime.now().strftime('%H:%M:%S:%f'),
        alarm_number
        ))


def main():
    """Main-Function"""

    # Define tasks with desired timestamps.
    task_1 = RepTaskOrg(second=[0, 10, 20, 30, 40, 50])
    task_2 = RepTaskOrg(minute=[26, 28, 29], second=[0, 10, 20, 30, 40, 50])
    task_3 = RepTaskOrg(weekday=[0, 1, 2, 3, 4], hour=[8])
    task_4 = RepTaskOrg(week=[18])

    # Show set time for timer 1
    print('active timer 1 settings: {}'.format(task_1.set_timer))

    # Call Task repeatedly to keep it up to date.
    while True:
        # Outputs true as soon as the target time is reached.
        if task_1.check_task():
            do_something(1)

        if task_2.check_task():
            do_something(2)

        if task_3.check_task():
            do_something(3)

        if task_4.check_task():
            do_something(4)

        time.sleep(0.001)


if __name__ == "__main__":
    main()
