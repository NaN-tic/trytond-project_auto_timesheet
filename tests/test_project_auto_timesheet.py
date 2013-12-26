#!/usr/bin/env python
#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

import sys
import os
DIR = os.path.abspath(os.path.normpath(os.path.join(__file__,
    '..', '..', '..', '..', '..', 'trytond')))
if os.path.isdir(DIR):
    sys.path.insert(0, os.path.dirname(DIR))

import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import test_view, test_depends
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT
from trytond.transaction import Transaction


class ProjectAutoTimesheetTestCase(unittest.TestCase):
    'Test ProjectAutoTimesheet module'

    def setUp(self):
        trytond.tests.test_tryton.install_module('project_auto_timesheet')
        self.project_work = POOL.get('project.work')
        self.company = POOL.get('company.company')
        self.user = POOL.get('res.user')

    def test0005views(self):
        'Test views'
        test_view('project_auto_timesheet')

    def test0006depends(self):
        'Test depends'
        test_depends()

    def test0010company_setup(self):
        CONTEXT.update(company=1)
        with Transaction().start(DB_NAME, USER,
                context=CONTEXT) as transaction:
            company, = self.company.search([('rec_name', '=', 'B2CK')])
            self.user.write([self.user(USER)], {
                    'main_company': company.id,
                    'company': company.id,
                    })
            CONTEXT.update(self.user.get_preferences(context_only=True))

    def test0020project(self):
        with Transaction().start(DB_NAME, USER,
                context=CONTEXT) as transaction:
            pwork1 = self.project_work(timesheet_work_name='test1')
            pwork1.save()
            self.assertEqual(pwork1.work.name, 'test1')
            self.assertEqual(pwork1.timesheet_work_name, 'test1')
            pwork2 = self.project_work(timesheet_work_name='test2')
            pwork2.save()
            self.assertEqual(pwork2.work.name, 'test2')
            self.assertEqual(pwork2.timesheet_work_name, 'test2')

            work, = self.project_work.search([
                    ('timesheet_work_name', '=', 'test1')])
            self.assertEqual(work, pwork1)

            npwork1, npwork2 = self.project_work.copy([pwork1, pwork2])
            self.assertEqual(npwork1.work.name, 'test1')
            self.assertEqual(npwork1.timesheet_work_name, 'test1')
            self.assertNotEqual(npwork1.work, pwork1.work)
            self.assertEqual(npwork2.work.name, 'test2')
            self.assertEqual(npwork2.timesheet_work_name, 'test2')
            self.assertNotEqual(npwork2.work, pwork2.work)


def suite():
    suite = trytond.tests.test_tryton.suite()
    from trytond.modules.company.tests import test_company
    for test in test_company.suite():
        if test not in suite:
            suite.addTest(test)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            ProjectAutoTimesheetTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
