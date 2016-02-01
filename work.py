#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from itertools import izip
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta

__all__ = ['Work']
__metaclass__ = PoolMeta


class Work:
    __name__ = 'project.work'

    @classmethod
    def create(cls, vlist):
        TimesheetWork = Pool().get('timesheet.work')
        vlist = [x.copy() for x in vlist]
        to_create = []
        to_values = []
        for values in vlist:
            if 'work' not in values or values['work'] is None:
                to_create.append({
                        'name': values.get('name'),
                        })
                to_values.append(values)
        works = TimesheetWork.create(to_create)
        for values, work in izip(to_values, works):
            values['work'] = work.id
        return super(Work, cls).create(vlist)

    @classmethod
    def copy(cls, projects, default=None):
        if default is None:
            default = {}
        TimesheetWork = Pool().get('timesheet.work')
        to_copy = []
        for project in projects:
            to_copy.append(project.work)
        works = TimesheetWork.copy(to_copy)
        projects = super(Work, cls).copy(projects, default=default)
        to_write = []
        for project, work in izip(projects, works):
            to_write.extend(([project], {'work': work.id}))
        if to_write:
            cls.write(*to_write)
        return projects
