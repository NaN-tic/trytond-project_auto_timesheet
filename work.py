#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta

__all__ = ['Work']
__metaclass__ = PoolMeta


class Work:
    __name__ = 'project.work'

    timesheet_work_name = fields.Function(fields.Char('Name', required=True),
        'get_timesheet_work_name', searcher='search_timesheet_work_name',
        setter='set_timesheet_work_name')

    def get_timesheet_work_name(self, name):
        return self.work.name

    @classmethod
    def search_timesheet_work_name(cls, name, clause):
        return [('work.name',) + tuple(clause[1:])]

    @classmethod
    def set_timesheet_work_name(cls, works, name, value):
        Work = Pool().get('timesheet.work')
        Work.write([p.work for p in works], {
                'name': value,
                })
