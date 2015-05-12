# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2014-Today BrowseInfo (<http://www.browseinfo.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import datetime
import time

from openerp.report import report_sxw

class activity_date_wizard(osv.osv_memory):
    _name = "activity.date.wizard"
    _columns={
        'start_date': fields.datetime('Start Period', required=True),
        'end_date': fields.datetime('End Period', required=True),
    }
    def print_report(self,cr, uid, ids, context=None):
        if context is None:
           context = {}
        data = self.read(cr, uid, ids)[0]
        datas = {
            'ids': context.get('active_ids',[]),
            'model': 'activity.date.wizard',
            'form': data
            }
        print "\n\n======data====",data
        return {
            'type': 'ir.actions.report.xml',
            'report_name':'century.workorder.report',
            'datas': datas,
            'name': 'Activity Total Square Feet'
            }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
