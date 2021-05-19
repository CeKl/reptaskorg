# REPeated Task ORGanizer - reptaskorg

Libary for repeated execution of functions at specific times.

Examples:

- Every minute, when seconds 5 and 34 are reached:

    ```python
    task = RepTaskOrg(second=[5, 34])  # 00:00:05, 00:00:34, 00:01:05, ...

    ```

- Every day, when hour 2, 8 and 12 and seconds 5 and 34 are reached:

    ```python
    task = RepTaskOrg(hour=[2, 8, 12], second=[5, 34])  # 02:00:05, 02:00:31, 08:00:05, ...
    ```

- Every year, at the first second of may:

    ```python
    task = RepTaskOrg(month=[5])  # 2021.05.01 00:00:00, 2022.05.01 00:00:00, ...
    ```

## Installation

For installation use Pypi:

`pip install reptaskorg` or `pip3 install reptaskorg`

## Usage

### without threading

If you have no time-consuming tasks in your main loop RapTaskOrg is a good solution.

```python
import datetime
import time
from reptaskorg import RepTaskOrg

def do_something(alarm_number):
    print('{} - ALARM {}'.format(datetime.datetime.now().strftime('%H:%M:%S:%f'), alarm_number))


def main():
    # Define tasks with desired time stamps.
    task_1 = RepTaskOrg(second=[0, 10, 20, 30, 40, 50])
    task_2 = RepTaskOrg(
        minute=[37, 39],
        second=[0, 10, 20, 30, 40, 50]
        )

    # Call Task repeatedly to keep it up to date. 
    while True:
        # Outputs true as soon as the target time is reached
        if task_1.check_task():
            do_something(1)

        if task_2.check_task():
            do_something(2)
        time.sleep(0.001)


if __name__ == "__main__":
    main()

```

### with threading

If you have time-consuming tasks in your main loop use RepTaskOrgTH.

```python
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

```

You can stop and restart task-threads by:

```python
# stop task
task.stop_task()

# restart task
task.restart_task()
```

Information on the set timer are showed by:
```python
print(task.every_year)
print(task.every_month)
print(task.every_day)
print(task.every_hour)
print(task.every_minute)
print(task.every_second)
```

### Arguments
You can define a task with the arguments in teh following chapters.

#### RepTaskOrg:
```
Args:
    year (list, optional): valid year. Defaults to None.
    month (list, optional): valid month. Defaults to None.
    day (list, optional): valid day. Defaults to None.
    hour (list, optional): valid hours. Defaults to None.
    minute (list, optional): valid minute. Defaults to None.
    second (list, optional): valid second. Defaults to None.
```

#### RepTaskOrgTH:
```
Args:
    function (function): function to execute.
    function_arguments (tuple): parameters of the given function.
    year (set, optional): valid year. Defaults to None.
    month (set, optional): valid month. Defaults to None.
    day (set, optional): valid day. Defaults to None.
    hour (set, optional): valid hour. Defaults to None.
    minute (set, optional): valid minute. Defaults to None.
    second (set, optional): valid second. Defaults to None.
    reminder (bool, optional): remind if time missed. Defaults to false.
```
