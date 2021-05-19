"""Libary for time dependend repetitive tasks.

Raises:
    ValueError: error fpr negative time; change type!
"""

from datetime import datetime
import time
import threading


class NoTimeToSetError(Exception):
    """Custom Exception - missing time."""

    def __str__(self):
        return 'Missing time to set. Example: RepTaskOrg(second=[0, 30])'


class ForbiddenTimeToSetError(Exception):
    """Custom Exception - forbidden time."""

    def __str__(self):
        return 'Forbidden time to set. Choose a valide time.'


class RepTaskOrg():
    """Timer to check repetitive tasks."""

    def __init__(self, year=None, month=None, day=None, hour=None, minute=None, second=None):
        """Set timer-object.

        Args:
            year (set, optional): valide year. Defaults to None.
            month (set, optional): valide month. Defaults to None.
            day (set, optional): valide day. Defaults to None.
            hour (set, optional): valide hour. Defaults to None.
            minute (set, optional): valide minute. Defaults to None.
            second (set, optional): valide second. Defaults to None.
            reminder (bool, optional): remind if time missed. Defaults to false.

        Raises:
            NoTimeToSetError: Error when no time is set
        """

        self.every_year = year
        self.every_month = month
        self.every_day = day
        self.every_hour = hour
        self.every_minute = minute
        self.every_second = second

        self.__trigger_status = False
        self.__condition = []

        __number_error_flag = False

        for check_element in [year, month, day, hour, minute, second]:
            if check_element == year and check_element is not None:
                self.__condition.append(self.__check_year)
                self.every_year = set(year)
            elif check_element == month and check_element is not None:
                self.__condition.append(self.__check_month)
                self.every_month = set(month)
                if any(test_month > 12 for test_month in set(month)):
                    __number_error_flag = True
                    break
            elif check_element == day and check_element is not None:
                self.__condition.append(self.__check_day)
                self.every_day = set(day)
                if any(test_month > 31 for test_month in set(day)):
                    __number_error_flag = True
                    break
            elif check_element == hour and check_element is not None:
                self.__condition.append(self.__check_hour)
                self.every_hour = set(hour)
                if any(test_month > 23 for test_month in set(hour)):
                    __number_error_flag = True
                    break
            elif check_element == minute and check_element is not None:
                self.__condition.append(self.__check_minute)
                self.every_minute = set(minute)
                if any(test_month > 59 for test_month in set(minute)):
                    __number_error_flag = True
                    break
            elif check_element == second and check_element is not None:
                self.__condition.append(self.__check_second)
                self.every_second = set(second)
                if any(test_month > 59 for test_month in set(second)):
                    __number_error_flag = True
                    break

        if len(self.__condition) == 0:
            raise NoTimeToSetError()

        if __number_error_flag:
            raise ForbiddenTimeToSetError()

    def __check_year(self, now):
        return now.year in self.every_year

    def __check_month(self, now):
        return now.moth in self.every_month

    def __check_day(self, now):
        return now.day in self.every_day

    def __check_hour(self, now):
        return now.hour in self.every_hour

    def __check_minute(self, now):
        return now.minute in self.every_minute

    def __check_second(self, now):
        return now.second in self.every_second

    def check_task(self):
        """Check the conditions. Returns true if choosen time is correct.

        Returns:
            bool: check status
        """

        now = datetime.now()

        if all(check_condition(now) for check_condition in self.__condition):
            if not self.__trigger_status:
                self.__trigger_status = True
                return True
        else:
            self.__trigger_status = False

        return False


class RepTaskOrgTH():
    """Timer to check repetitive tasks in individual threads."""

    def __init__(self, function, *function_arguments, year=None, month=None, day=None, hour=None, minute=None, second=None):
        """Set timer-object with threading.

        Args:
            function (function): function to execute.
            function_arguments (tuple): arguments of the given function.
            year (set, optional): valide year. Defaults to None.
            month (set, optional): valide month. Defaults to None.
            day (set, optional): valide day. Defaults to None.
            hour (set, optional): valide hour. Defaults to None.
            minute (set, optional): valide minute. Defaults to None.
            second (set, optional): valide second. Defaults to None.
            reminder (bool, optional): remind if time missed. Defaults to false.

        Raises:
            NoTimeToSetError: Error when no time is set
        """

        self.every_year = year
        self.every_month = month
        self.every_day = day
        self.every_hour = hour
        self.every_minute = minute
        self.every_second = second

        self.__trigger_status = False
        self.__condition = []

        self.run_taks = True

        self.__function = function
        self.__function_arguments = function_arguments

        __number_error_flag = False

        for check_element in [year, month, day, hour, minute, second]:
            if check_element == year and check_element is not None:
                self.__condition.append(self.__check_year)
                self.every_year = set(year)
            elif check_element == month and check_element is not None:
                self.__condition.append(self.__check_month)
                self.every_month = set(month)
                if any(test_month > 12 for test_month in set(month)):
                    __number_error_flag = True
                    break
            elif check_element == day and check_element is not None:
                self.__condition.append(self.__check_day)
                self.every_day = set(day)
                if any(test_month > 31 for test_month in set(day)):
                    __number_error_flag = True
                    break
            elif check_element == hour and check_element is not None:
                self.__condition.append(self.__check_hour)
                self.every_hour = set(hour)
                if any(test_month > 23 for test_month in set(hour)):
                    __number_error_flag = True
                    break
            elif check_element == minute and check_element is not None:
                self.__condition.append(self.__check_minute)
                self.every_minute = set(minute)
                if any(test_month > 59 for test_month in set(minute)):
                    __number_error_flag = True
                    break
            elif check_element == second and check_element is not None:
                self.__condition.append(self.__check_second)
                self.every_second = set(second)
                if any(test_month > 59 for test_month in set(second)):
                    __number_error_flag = True
                    break

        if len(self.__condition) == 0:
            raise NoTimeToSetError()

        if __number_error_flag:
            raise ForbiddenTimeToSetError()

        self.__therad = threading.Thread(target=self.__task_thread_new, args=(
            self.__function, self.__function_arguments,))
        self.__therad.start()

    def stop_task(self):
        """Stop a runnung task."""
        self.run_taks = False

    def restart_task(self):
        """Restart tastk."""
        self.run_taks = True
        if not self.__therad.is_alive():
            self.__therad = threading.Thread(target=self.__task_thread_new, args=(
                self.__function, self.__function_arguments,))
            self.__therad.start()

    def __task_thread_new(self, function, function_arguments):
        while self.run_taks:
            if self.__check_task():
                function(*function_arguments)
            time.sleep(0.001)

    def __check_year(self, now):
        return now.year in self.every_year

    def __check_month(self, now):
        return now.moth in self.every_month

    def __check_day(self, now):
        return now.day in self.every_day

    def __check_hour(self, now):
        return now.hour in self.every_hour

    def __check_minute(self, now):
        return now.minute in self.every_minute

    def __check_second(self, now):
        return now.second in self.every_second

    def __check_task(self):
        """Check the conditions. Returns true if choosen time is correct.

        Returns:
            bool: check status
        """

        now = datetime.now()

        if all(check_condition(now) for check_condition in self.__condition):
            if not self.__trigger_status:
                self.__trigger_status = True
                return True
        else:
            self.__trigger_status = False

        return False
