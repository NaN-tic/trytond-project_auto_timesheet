#!/usr/bin/env python
#The COPYRIGHT file at the top level of this repository contains the full
#copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT
from trytond.transaction import Transaction


class ProjectAutoTimesheetTestCase(ModuleTestCase):
    'Test ProjectAutoTimesheet module'
    module = 'project_auto_timesheet'

    def setUp(self):
        super(ProjectAutoTimesheetTestCase, self).setUp()
        self.project_work = POOL.get('project.work')
        self.company = POOL.get('company.company')
        self.user = POOL.get('res.user')

    def test0010project(self):
        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            company, = self.company.search([
                    ('rec_name', '=', 'Dunder Mifflin'),
                    ])
            self.user.write([self.user(USER)], {
                    'main_company': company.id,
                    'company': company.id,
                    })
            new_context = self.user.get_preferences(context_only=True)
        with Transaction().start(DB_NAME, USER, context=new_context):
            pwork1 = self.project_work(name='test1')
            pwork1.save()
            self.assertEqual(pwork1.work.name, 'test1')
            self.assertEqual(pwork1.name, 'test1')
            pwork2 = self.project_work(name='test2')
            pwork2.save()
            self.assertEqual(pwork2.work.name, 'test2')
            self.assertEqual(pwork2.name, 'test2')

            work, = self.project_work.search([
                    ('name', '=', 'test1')])
            self.assertEqual(work, pwork1)

            npwork1, npwork2 = self.project_work.copy([pwork1, pwork2])
            self.assertEqual(npwork1.work.name, 'test1')
            self.assertEqual(npwork1.name, 'test1')
            self.assertNotEqual(npwork1.work, pwork1.work)
            self.assertEqual(npwork2.work.name, 'test2')
            self.assertEqual(npwork2.name, 'test2')
            self.assertNotEqual(npwork2.work, pwork2.work)
            pwork3 = self.project_work(name='test3', work=None)
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
