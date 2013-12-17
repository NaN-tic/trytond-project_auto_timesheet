#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta


__all__ = ['Work']
__metaclass__ = PoolMeta


class Work(ModelSQL, ModelView):
    __name__ = 'project.work'

    timesheet_work_name = fields.Char('Work', required=True)

    @classmethod
    def create(cls, vlist):
        Timesheet_work = Pool().get('timesheet.work')
        for vl in vlist:
            timesheet_work = Timesheet_work.create(
                [{'name': vl['timesheet_work_name']}])
            vl['work'] = timesheet_work[0].id
        return super(Work, cls).create(vlist)

    @classmethod
    def __setup__(cls):
        super(Work, cls).__setup__()
        cls._error_messages.update({
                'to_many_duplicates': ('For this type of model you can only '
                    'duplicate one by one.'),
                })

    @classmethod
    def copy(cls, records, default=None):
        if default is None:
            default = {}
        default = default.copy()
        if len(records) > 1:
            cls.raise_user_error('to_many_duplicates')
        default.setdefault('work', None)
        default.setdefault('timesheet_work_name',
            "%s (copy)" % records[0].timesheet_work_name)
        default.setdefault('product', records[0].product)
        default.setdefault('party', records[0].party)
        return super(Work, cls).copy(records, default=default)
