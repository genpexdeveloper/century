# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://genpex.com/>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import time
from openerp.report import report_sxw
from openerp.osv import fields, osv, orm

class square_feet(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(square_feet, self).__init__(cr, uid, name, context=context)
        self.total_sqft = 0
        self.localcontext.update({
            'time': time,
            'set_location_sqft':self.set_location_sqft,
            'get_sqft_total':self.get_sqft_total,
            'get_fabrication_activity':self.get_fabrication_activity,
            'get_template_activity':self.get_template_activity,
            'get_installation_activity':self.get_installation_activity,
            'get_others_activity':self.get_others_activity,
        })

    def set_location_sqft(self,data):
        century_workorder_pool = self.pool.get('century.workorder')
        start_date = data['start_date']
        end_date = data['end_date']
        self.cr.execute("select id from century_workorder cw "\
                   "WHERE (cw.create_date >= %s) AND (cw.create_date <= %s)", (start_date, end_date))
        workorder_ids = self.cr.fetchall()
        century_workorder_ids=[i[0] for i in workorder_ids]
        
        Template_charge = 0.0
        Fabrication_charge = 0.0
        Installation_charge = 0.0
        Service_Call_charge = 0.0
        Tile_installation_charge = 0.0
        for workorder_id in century_workorder_ids:
            century_workorder_obj = century_workorder_pool.browse(self.cr, self.uid, workorder_id)
            for activity in century_workorder_obj.scheduleactivities:
                if activity.type == 'Template':
                    Template_charge += century_workorder_obj.sq_ft
                if activity.type == 'Fabrication':
                    Fabrication_charge += century_workorder_obj.sq_ft
                if activity.type == 'Installation':
                    Installation_charge += century_workorder_obj.sq_ft
                if activity.type == 'Service Call':
                    Service_Call_charge += century_workorder_obj.sq_ft
                if activity.type == 'Tile Installation':
                    Tile_installation_charge += century_workorder_obj.sq_ft
        Template_dict = {'Template':Template_charge}
        Fabrication_dict = {'Fabrication':Fabrication_charge}
        Installation_dict = {'Installation':Installation_charge}
        Service_Call_dict = {'Service Call':Service_Call_charge}
        Tile_installation_dict = {'Tile Installation':Tile_installation_charge}
        self.total_sqft = Template_charge + Fabrication_charge + Installation_charge + Service_Call_charge + Tile_installation_charge
        sq_ft_list = []
        sq_ft_list.append(Template_dict)
        sq_ft_list.append(Fabrication_dict)
        sq_ft_list.append(Installation_dict)
        sq_ft_list.append(Service_Call_dict)
        sq_ft_list.append(Tile_installation_dict)
        return sq_ft_list
    
    def get_sqft_total(self):
        return self.total_sqft
    
    def get_fabrication_activity(self,data,fabrication):
        century_workorder_pool = self.pool.get('century.workorder')
        start_date = data['start_date']
        end_date = data['end_date']
        self.cr.execute("select id from century_workorder cw "\
                   "WHERE (cw.create_date >= %s) AND (cw.create_date <= %s)", (start_date, end_date))
        workorder_ids = self.cr.fetchall()
        century_workorder_ids=[i[0] for i in workorder_ids]
        workorder_obj = []
        fabrication_activity_obj = []
        for wo_id in century_workorder_ids:
            workorder_obj.append(century_workorder_pool.browse(self.cr, self.uid, wo_id ))
        print "\n\n=======workorder_obj=",workorder_obj
        for workorder in workorder_obj:
            for activity in workorder.scheduleactivities:
                if activity.type == fabrication:
                    fabrication_activity_obj.append(activity)   
        return fabrication_activity_obj   

    def get_template_activity(self,data,template):
        century_workorder_pool = self.pool.get('century.workorder')
        start_date = data['start_date']
        end_date = data['end_date']
        self.cr.execute("select id from century_workorder cw "\
                   "WHERE (cw.create_date >= %s) AND (cw.create_date <= %s)", (start_date, end_date))
        workorder_ids = self.cr.fetchall()
        century_workorder_ids=[i[0] for i in workorder_ids]
        workorder_obj = []
        template_activity_obj = []
        for wo_id in century_workorder_ids:
            workorder_obj.append(century_workorder_pool.browse(self.cr, self.uid, wo_id ))
        print "\n\n=======workorder_obj=",workorder_obj
        for workorder in workorder_obj:
            for activity in workorder.scheduleactivities:
                if activity.type == template:
                    template_activity_obj.append(activity)   
        return template_activity_obj   

    def get_installation_activity(self,data,installation):
        century_workorder_pool = self.pool.get('century.workorder')
        start_date = data['start_date']
        end_date = data['end_date']
        self.cr.execute("select id from century_workorder cw "\
                   "WHERE (cw.create_date >= %s) AND (cw.create_date <= %s)", (start_date, end_date))
        workorder_ids = self.cr.fetchall()
        century_workorder_ids=[i[0] for i in workorder_ids]
        workorder_obj = []
        installation_activity_obj = []
        for wo_id in century_workorder_ids:
            workorder_obj.append(century_workorder_pool.browse(self.cr, self.uid, wo_id ))
        print "\n\n=======workorder_obj=",workorder_obj
        for workorder in workorder_obj:
            for activity in workorder.scheduleactivities:
                if activity.type == installation:
                    installation_activity_obj.append(activity)   
        return installation_activity_obj   

    def get_others_activity(self,data):
        century_workorder_pool = self.pool.get('century.workorder')
        start_date = data['start_date']
        end_date = data['end_date']
        self.cr.execute("select id from century_workorder cw "\
                   "WHERE (cw.create_date >= %s) AND (cw.create_date <= %s)", (start_date, end_date))
        workorder_ids = self.cr.fetchall()
        century_workorder_ids=[i[0] for i in workorder_ids]
        workorder_obj = []
        others_activity_obj = []
        for wo_id in century_workorder_ids:
            workorder_obj.append(century_workorder_pool.browse(self.cr, self.uid, wo_id ))
        print "\n\n=======workorder_obj=",workorder_obj
        for workorder in workorder_obj:
            for activity in workorder.scheduleactivities:
                if activity.type != "Template" and activity.type != "Fabrication" and activity.type != "Installation":
                    others_activity_obj.append(activity)   
        return others_activity_obj   



report_sxw.report_sxw(
    'report.century.workorder.report',
    'activity.date.wizard',
    'addons/century/report/square_feet.rml',
    parser=square_feet,
    header="True"
)



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

