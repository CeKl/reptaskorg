"""REPeated TASK ORGanizer - reptaskorg

Libary for time dependend repetitive tasks.

MIT License
Copyright (c) 2021 Cedric Klimt

"""

from datetime import datetime, timedelta
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


class OffsetError(Exception):
    """Custom Exception - invalid offset."""

    def __str__(self):
        return 'Invalid offset. Choose a valide value.'


class RepTaskOrg():
    """Timer to check repetitive tasks."""

    def __init__(self, year=None, month=None, week=None, weekday=None, day=None, hour=None, minute=None, second=None, offset_hour=0, offset_minute=0):
        """Set timer-object.

        Args:
            year (set, optional): valide year. Defaults to None.
            month (set, optional): valide month. Defaults to None.
            week (set, optional): valide week. Defaults to None.
            weekday (set, optional): valide day of week. Defaults to None.
            day (set, optional): valide day. Defaults to None.
            hour (set, optional): valide hour. Defaults to None.
            minute (set, optional): valide minute. Defaults to None.
            second (set, optional): valide second. Defaults to None.
            offset_hour (int, optional): valide hour for offset. Defaults to 0.
            offset_minute (int, optional): valide minute for offset. Defaults to 0.

        Raises:
            NoTimeToSetError: Error when no time is set
        """

        self.every_year = year
        self.every_month = month
        self.every_week = week
        self.every_weekday = weekday
        self.every_day = day
        self.every_hour = hour
        self.every_minute = minute
        self.every_second = second

        self.__utc_offset = False
        if offset_hour or offset_minute:
            self.__utc_offset = True

        offset_direction = 1
        if offset_hour < 0 or offset_minute < 0:
            offset_direction = -1

        if -12 <= offset_hour <= 14:
            self.__offset_houer = abs(offset_hour) * offset_direction
        else:
            raise OffsetError()

        if -45 <= offset_minute <= 45:
            self.__offset_minute = abs(offset_minute) * offset_direction
        else:
            raise OffsetError()

        self.__trigger_status = False
        self.__condition = []

        __number_error_flag = False

        self.set_timer = {}

        for check_element in [year, month, week, weekday, day, hour, minute, second]:
            if check_element == year and check_element is not None:
                self.__condition.append(self.__check_year)
                self.every_year = sorted(set(year))
                self.set_timer['year'] = sorted(set(year))
            elif check_element == month and check_element is not None:
                self.__condition.append(self.__check_month)
                self.every_month = sorted(set(month))
                self.set_timer['month'] = sorted(set(month))
                if any(test_month > 12 for test_month in set(month)):
                    __number_error_flag = True
                    break
            elif check_element == week and check_element is not None:
                self.__condition.append(self.__check_week)
                self.every_week = sorted(set(week))
                self.set_timer['week'] = sorted(set(week))
                if any(test_week < 0 or test_week > 53 for test_week in set(week)):
                    __number_error_flag = True
                    break
            elif check_element == weekday and check_element is not None:
                self.__condition.append(self.__check_weekday)
                self.every_weekday = sorted(set(weekday))
                self.set_timer['weekday'] = sorted(set(weekday))
                if any(test_weekday > 6 for test_weekday in set(weekday)):
                    __number_error_flag = True
                    break
            elif check_element == day and check_element is not None:
                self.__condition.append(self.__check_day)
                self.every_day = sorted(set(day))
                self.set_timer['day'] = sorted(set(day))
                if any(test_day > 31 for test_day in set(day)):
                    __number_error_flag = True
                    break
            elif check_element == hour and check_element is not None:
                self.__condition.append(self.__check_hour)
                self.every_hour = sorted(set(hour))
                self.set_timer['hour'] = sorted(set(hour))
                if any(test_hour > 23 for test_hour in set(hour)):
                    __number_error_flag = True
                    break
            elif check_element == minute and check_element is not None:
                self.__condition.append(self.__check_minute)
                self.every_minute = sorted(set(minute))
                self.set_timer['minute'] = sorted(set(minute))
                if any(test_minute > 59 for test_minute in set(minute)):
                    __number_error_flag = True
                    break
            elif check_element == second and check_element is not None:
                self.__condition.append(self.__check_second)
                self.every_second = sorted(set(second))
                self.set_timer['second'] = sorted(set(second))
                if any(test_second > 59 for test_second in set(second)):
                    __number_error_flag = True
                    break

        if len(self.__condition) == 0:
            raise NoTimeToSetError()

        if __number_error_flag:
            raise ForbiddenTimeToSetError()

    def set_time_offset(self, offset_hour=0, offset_minute=0):
        offset_direction = 1
        if offset_hour < 0 or offset_minute < 0:
            offset_direction = -1

        if -12 <= offset_hour <= 14:
            self.__offset_houer = abs(offset_hour) * offset_direction
        else:
            raise OffsetError()

        if -45 <= offset_minute <= 45:
            self.__offset_minute = abs(offset_minute) * offset_direction
        else:
            raise OffsetError()

        self.__utc_offset = True

    def __get_time(self):
        if self.__utc_offset:
            current_time = datetime.utcnow() + timedelta(hours=self.__offset_houer,
                                                         minutes=self.__offset_minute)
        else:
            current_time = datetime.now()
        return current_time

    def __check_year(self, now):
        return now.year in self.every_year

    def __check_month(self, now):
        return now.moth in self.every_month

    def __check_week(self, now):
        return now.isocalendar()[1] in self.every_week

    def __check_weekday(self, now):
        return now.weekday() in self.every_weekday

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

        now = self.__get_time()

        if all(check_condition(now) for check_condition in self.__condition):
            if not self.__trigger_status:
                self.__trigger_status = True
                return True
        else:
            self.__trigger_status = False

        return False


class RepTaskOrgTH():
    """Timer to check repetitive tasks in individual threads."""

    def __init__(self, function, *function_arguments, year=None, month=None, week=None, weekday=None, day=None, hour=None, minute=None, second=None, offset_hour=0, offset_minute=0):
        """Set timer-object with threading.

        Args:
            function (function): function to execute.
            function_arguments (tuple): arguments of the given function.
            year (set, optional): valide year. Defaults to None.
            month (set, optional): valide month. Defaults to None.
            week (set, optional): valide week. Defaults to None.
            weekday (set, optional): valide day of week. Defaults to None.
            day (set, optional): valide day. Defaults to None.
            hour (set, optional): valide hour. Defaults to None.
            minute (set, optional): valide minute. Defaults to None.
            second (set, optional): valide second. Defaults to None.
            offset_hour (int, optional): valide hour for offset. Defaults to 0.
            offset_minute (int, optional): valide minute for offset. Defaults to 0.

        Raises:
            NoTimeToSetError: Error when no time is set
        """

        self.every_year = year
        self.every_month = month
        self.every_week = week
        self.every_weekday = weekday
        self.every_day = day
        self.every_hour = hour
        self.every_minute = minute
        self.every_second = second

        self.__utc_offset = False
        if offset_hour or offset_minute:
            self.__utc_offset = True

        offset_direction = 1
        if offset_hour < 0 or offset_minute < 0:
            offset_direction = -1

        if -12 <= offset_hour <= 14:
            self.__offset_houer = abs(offset_hour) * offset_direction
        else:
            raise OffsetError()

        if -45 <= offset_minute <= 45:
            self.__offset_minute = abs(offset_minute) * offset_direction
        else:
            raise OffsetError()

        self.__trigger_status = False
        self.__condition = []

        self.run_taks = True

        self.__function = function
        self.__function_arguments = function_arguments

        __number_error_flag = False

        self.set_timer = {}

        for check_element in [year, month, day, week, weekday, hour, minute, second]:
            if check_element == year and check_element is not None:
                self.__condition.append(self.__check_year)
                self.every_year = sorted(set(year))
                self.set_timer['year'] = sorted(set(year))
            elif check_element == month and check_element is not None:
                self.__condition.append(self.__check_month)
                self.every_month = sorted(set(month))
                self.set_timer['month'] = sorted(set(month))
                if any(test_month > 12 for test_month in set(month)):
                    __number_error_flag = True
                    break
            elif check_element == week and check_element is not None:
                self.__condition.append(self.__check_week)
                self.every_week = sorted(set(week))
                self.set_timer['week'] = sorted(set(week))
                if any(test_week < 0 or test_week > 53 for test_week in set(week)):
                    __number_error_flag = True
                    break
            elif check_element == weekday and check_element is not None:
                self.__condition.append(self.__check_weekday)
                self.every_weekday = sorted(set(weekday))
                self.set_timer['weekday'] = sorted(set(weekday))
                if any(test_weekday > 6 for test_weekday in set(weekday)):
                    __number_error_flag = True
                    break
            elif check_element == day and check_element is not None:
                self.__condition.append(self.__check_day)
                self.every_day = sorted(set(day))
                self.set_timer['day'] = sorted(set(day))
                if any(test_day > 31 for test_day in set(day)):
                    __number_error_flag = True
                    break
            elif check_element == hour and check_element is not None:
                self.__condition.append(self.__check_hour)
                self.every_hour = sorted(set(hour))
                self.set_timer['hour'] = sorted(set(hour))
                if any(test_hour > 23 for test_hour in set(hour)):
                    __number_error_flag = True
                    break
            elif check_element == minute and check_element is not None:
                self.__condition.append(self.__check_minute)
                self.every_minute = sorted(set(minute))
                self.set_timer['minute'] = sorted(set(minute))
                if any(test_minute > 59 for test_minute in set(minute)):
                    __number_error_flag = True
                    break
            elif check_element == second and check_element is not None:
                self.__condition.append(self.__check_second)
                self.every_second = sorted(set(second))
                self.set_timer['second'] = sorted(set(second))
                if any(test_second > 59 for test_second in set(second)):
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
        """Restart task."""
        self.run_taks = True
        if not self.__therad.is_alive():
            self.__therad = threading.Thread(target=self.__task_thread_new, args=(
                self.__function, self.__function_arguments,))
            self.__therad.start()

    def set_time_offset(self, offset_hour=0, offset_minute=0):
        offset_direction = 1
        if offset_hour < 0 or offset_minute < 0:
            offset_direction = -1

        if -12 <= offset_hour <= 14:
            self.__offset_houer = abs(offset_hour) * offset_direction
        else:
            raise OffsetError()

        if -45 <= offset_minute <= 45:
            self.__offset_minute = abs(offset_minute) * offset_direction
        else:
            raise OffsetError()

        self.__utc_offset = True

    def __get_time(self):
        if self.__utc_offset:
            current_time = datetime.utcnow() + timedelta(hours=self.__offset_houer,
                                                         minutes=self.__offset_minute)
        else:
            current_time = datetime.now()
        return current_time

    def __task_thread_new(self, function, function_arguments):
        while self.run_taks:
            if self.__check_task():
                function(*function_arguments)
            time.sleep(0.001)

    def __check_year(self, now):
        return now.year in self.every_year

    def __check_month(self, now):
        return now.moth in self.every_month

    def __check_week(self, now):
        return now.isocalendar()[1] in self.every_week

    def __check_weekday(self, now):
        return now.weekday() in self.every_weekday

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

        now = self.__get_time()

        if all(check_condition(now) for check_condition in self.__condition):
            if not self.__trigger_status:
                self.__trigger_status = True
                return True
        else:
            self.__trigger_status = False

        return False
