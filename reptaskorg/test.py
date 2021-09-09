import unittest
from reptaskorg import RepTaskOrg, RepTaskOrgTH
from datetime import datetime as dt


class TestRepTaskOrg(unittest.TestCase):

    def test_set_timer_1(self):
        task_0 = RepTaskOrg(second=[0, 10, 20, 30, 40, 50])
        test_intervall = {'second': [0, 10, 20, 30, 40, 50]}
        self.assertEqual(task_0.set_timer, test_intervall,
                         "Should be {}".format(test_intervall))

    def test_set_timer_2(self):
        task_0 = RepTaskOrg(
            year=[2021, 2022],
            month=[2],
            week=[12, 14],
            weekday=[1, 3, 5],
            day=[1, 3, 5, 22],
            hour=[6, 12, 18],
            minute=[45, 59],
            second=[0, 10, 20, 30, 40, 50]
        )
        test_intervall = {
            'year': [2021, 2022],
            'month': [2],
            'week': [12, 14],
            'weekday': [1, 3, 5],
            'day': [1, 3, 5, 22],
            'hour': [6, 12, 18],
            'minute': [45, 59],
            'second': [0, 10, 20, 30, 40, 50]
        }
        self.assertEqual(task_0.set_timer, test_intervall,
                         "Should be {}".format(test_intervall))

    def test_check_task(self):
        task_0 = RepTaskOrg(second=[0, 10, 20, 30, 40, 50])
        if dt.now().second in [0, 10, 20, 30, 40, 50]:
            self.assertTrue(task_0.check_task())
        else:
            self.assertFalse(task_0.check_task())


class TestRepTaskOrgTH(unittest.TestCase):

    def do_something(alarm_number):
        """Function which should be executed repeatedly."""

        print('{} - ALARM {}'.format(
            dt.now().strftime('%H:%M:%S:%f'),
            alarm_number
        ))

    def test_set_timer(self):
        task_0 = RepTaskOrgTH(self.do_something, 1, second=[0, 10, 20, 30, 40, 50])
        test_intervall = {'second': [0, 10, 20, 30, 40, 50]}
        self.assertEqual(task_0.set_timer, test_intervall,
                         "Should be {}".format(test_intervall))
        task_0.stop_task()

    def test_task_running_1(self):
        task_0 = RepTaskOrgTH(self.do_something, 1, second=[0, 10, 20, 30, 40, 50])
        self.assertTrue(task_0.task_running())
        task_0.stop_task()

    def test_task_running_2(self):
        task_0 = RepTaskOrgTH(self.do_something, 1, second=[0, 10, 20, 30, 40, 50])
        task_0.stop_task()
        self.assertFalse(task_0.task_running())

if __name__ == '__main__':
    unittest.main()
