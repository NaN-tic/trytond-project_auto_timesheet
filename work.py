#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from itertools import izip
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta

__all__ = ['Work']
__metaclass__ = PoolMeta


class Work:
    __name__ = 'project.work'
    timesheet_work_name = fields.Function(fields.Char('Name', required=True),
        'get_timesheet_work_name', searcher='search_timesheet_work_name',
        setter='set_timesheet_work_name')

    @classmethod
    def create(cls, vlist):
        TimesheetWork = Pool().get('timesheet.work')
        vlist = [x.copy() for x in vlist]
        to_create = []
        to_values = []
        for values in vlist:
            if 'work' not in values:
                to_create.append({
                        'name': values.get('timesheet_work_name'),
                        })
                to_values.append(values)
        works = TimesheetWork.create(to_create)
        for values, work in izip(to_values, works):
            values['work'] = work.id
        return super(Work, cls).create(vlist)

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

    @classmethod
    def copy(cls, projects, default=None):
        if default is None:
            default = {}
        TimesheetWork = Pool().get('timesheet.work')
        to_copy = []
        for project in projects:
            to_copy.append(project.work)
        works = TimesheetWork.copy(to_copy)
        res = []
        for project, work in izip(projects, works):
            d = default.copy()
            d['work'] = work.id
            res += super(Work, cls).copy([project], default=d)
        return res
