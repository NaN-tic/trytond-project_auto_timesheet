#!/usr/bin/env python
#The COPYRIGHT file at the top level of this repository contains the full
#copyright notices and license terms.
import doctest
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool

from trytond.modules.company.tests import create_company, set_company


class ProjectAutoTimesheetTestCase(ModuleTestCase):
    'Test ProjectAutoTimesheet module'
    module = 'project_auto_timesheet'

    @with_transaction()
    def test0010project(self):
        pool = Pool()
        ProjectWork = pool.get('project.work')

        company = create_company()
        with set_company(company):
            pwork1 = ProjectWork(name='test1')
            pwork1.save()
            self.assertEqual(pwork1.work.name, 'test1')
            self.assertEqual(pwork1.name, 'test1')
            pwork2 = ProjectWork(name='test2')
            pwork2.save()
            self.assertEqual(pwork2.work.name, 'test2')
            self.assertEqual(pwork2.name, 'test2')

            work, = ProjectWork.search([('name', '=', 'test1')])
            self.assertEqual(work, pwork1)

            npwork1, npwork2 = ProjectWork.copy([pwork1, pwork2])
            self.assertEqual(npwork1.work.name, 'test1')
            self.assertEqual(npwork1.name, 'test1')
            self.assertNotEqual(npwork1.work, pwork1.work)
            self.assertEqual(npwork2.work.name, 'test2')
            self.assertEqual(npwork2.name, 'test2')
            self.assertNotEqual(npwork2.work, pwork2.work)
            pwork3 = ProjectWork(name='test3', work=None)
            pwork3.save()
            self.assertEqual(pwork3.work.name, 'test3')
            self.assertEqual(pwork3.name, 'test3')


def suite():
    suite = trytond.tests.test_tryton.suite()
    from trytond.modules.company.tests import test_company
    for test in test_company.suite():
        if test not in suite:
            suite.addTest(test)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            ProjectAutoTimesheetTestCase))
    return suite
