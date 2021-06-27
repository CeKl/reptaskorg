# REPeated TASK ORGanizer - reptaskorg

Libary for repeated execution of functions at specific times.

[![Python](https://img.shields.io/pypi/pyversions/reptaskorg.svg)](https://badge.fury.io/py/reptaskorg)
[![PyPI](https://badge.fury.io/py/reptaskorg.svg)](https://badge.fury.io/py/reptaskorg)
[![Python](https://img.shields.io/github/license/CeKl/reptaskorg.svg)](https://opensource.org/licenses/MIT)
[![DeepSource](https://deepsource.io/gh/CeKl/reptaskorg.svg/?label=active+issues&token=mnSch-Vhc33NaLvBemavHOoD)](https://deepsource.io/gh/CeKl/reptaskorg/?ref=repository-badge)


Examples:

- Every minute, when seconds 5 and 34 are reached:

    ```python
    task = RepTaskOrg(second=[5, 34])  # 00:00:05, 00:00:34, 00:01:05, ...

    ```

- Every day, when hours 2, 8 and 12 and seconds 5 and 34 are reached:

    ```python
    task = RepTaskOrg(hour=[2, 8, 12], second=[5, 34])  # 02:00:05, 02:00:34, 08:00:05, ...
    ```

- Every year, at the first second of may:

    ```python
    task = RepTaskOrg(month=[5])  # 2021.05.01 00:00:00, 2022.05.01 00:00:00, ...
    ```

- Every monday at 8 am:

    ```python
    task = RepTaskOrg(weekday=[0], hour=[8])  # 2021.05.03 08:00:00, 2022.05.10 08:00:00, ...
    ```
- Every day in week 19 at 8 am:

    ```python
    task = RepTaskOrg(week=[18], hour=[8])  # 2021.05.03 08:00:00, 2022.05.04 08:00:00, ...
    ```

## Table of Contents
- [Install](#install)
- [Usage](#usage)
    - [without threading](#without-threading)
    - [with threading](#with-threading)
    - [other features](#other-features)
- [Arguments](#arguments)
- [Release Notes](#release-notes)

## Install

For installation use [Pypi](https://pypi.org/project/reptaskorg/):

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

If you have time-consuming tasks in your main loop use RepTaskOrgTH. Here a separate thread is started for each task.

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
### other features
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
print(task.every_week)
print(task.every_weekday)
print(task.every_day)
print(task.every_hour)
print(task.every_minute)
print(task.every_second)
```

By default, the Libary uses the current system time. You can set a UTC-time-offset by:

```python
# UTC
task_1 = RepTaskOrg(second=[0, 10, 20, 30, 40, 50], offset_hour=0, offset_minute=0)
task_2 = RepTaskOrgTH(do_something, 1, second=[0, 10, 20, 30, 40, 50], offset_hour=0, offset_minute=0)

# United States (Pacific Time Zone) = UTC -08:00
task_3 = RepTaskOrg(second=[0, 10, 20, 30, 40, 50], offset_hour=-8, offset_minute=0)
task_4 = RepTaskOrgTH(do_something, 1, second=[0, 10, 20, 30, 40, 50], offset_hour=-8, offset_minute=0)
```

## Arguments
You can define a task with the arguments in the following chapters.

### RepTaskOrg:
```
Args:
    year (list, optional): valid year. Defaults to None.
    month (list, optional): valid month. Defaults to None.
    week (set, optional): valide week. Defaults to None.
    weekday (set, optional): valide day of week. Defaults to None.
    day (list, optional): valid day. Defaults to None.
    hour (list, optional): valid hours. Defaults to None.
    minute (list, optional): valid minute. Defaults to None.
    second (list, optional): valid second. Defaults to None.
    offset_hour (int, optional): valide hour for offset. Defaults to 0.
    offset_minute (int, optional): valide minute for offset. Defaults to 0.
```

### Release Notes:
```
Args:
    function (function): function to execute.
    function_arguments (tuple): parameters of the given function.
    year (set, optional): valid year. Defaults to None.
    month (set, optional): valid month. Defaults to None.
    week (set, optional): valide week. Defaults to None.
    weekday (set, optional): valide day of week. Defaults to None.
    day (set, optional): valid day. Defaults to None.
    hour (set, optional): valid hour. Defaults to None.
    minute (set, optional): valid minute. Defaults to None.
    second (set, optional): valid second. Defaults to None.
    offset_hour (int, optional): valide hour for offset. Defaults to 0.
    offset_minute (int, optional): valide minute for offset. Defaults to 0.
```

## Release Notes
### 0.2.2
* Bugfix if only weekday was set
* Introduction weeks as argument

### 0.2.1
* Introduction weekday as argument

### 0.2
* Introduction UTC - offset as argument

### 0.1.1 
* Revision of the documentation

### 0.1
* Initial release

- - -
[MIT License](https://opensource.org/licenses/MIT) Copyright (c) 2021 Cedric Klimt