

from osv import fields, osv
from openerp import netsvc
import time
import datetime
from dateutil import parser
import openerp.tools as tools
import pytz


tz_default = pytz.timezone("America/Chicago")

#
#  Job
#
class century_job(osv.osv):
    _auto = True
    _name = "century.job"
    _description = "A Job"
    _columns = {
	'name': fields.char('Name', size=30),
	'customer_id': fields.many2one('res.partner', "Customer"),
	'planner_id': fields.many2one('res.users', "Planner"),
	###  Address fields
	'street': fields.char('Street', size=128),
	'street2': fields.char('Street2', size=128),
	'zip': fields.char('Zip', change_default=True, size=24),
	'city': fields.char('City', size=128),
	'state_id': fields.many2one("res.country.state", 'State'),
	'country_id': fields.many2one('res.country', 'Country'),
	'phone': fields.char('Phone', size=64),
	'fax': fields.char('Fax', size=64),
	'other': fields.char('Other', size=64),
	##

	#Relationship
	"workorders": fields.one2many("century.workorder", "job_id", "Work Orders"),
    }
    _defaults = {
    }
    def open_map(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        partner = self.browse(cr, uid, ids[0], context=context)
        url = "http://maps.google.com/maps?oi=map&q="
        if partner.street:
            url += partner.street.replace(' ','+')
        if partner.city:
            url += '+'+partner.city.replace(' ','+')
        if partner.state_id:
            url += '+'+partner.state_id.name.replace(' ','+')
        if partner.country_id:
            url += '+'+partner.country_id.name.replace(' ','+')
        if partner.zip:
            url += '+'+partner.zip.replace(' ','+')

        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new'
        }
century_job()

#
#  Stone
#
class century_stone(osv.osv):
    _auto = True
    _name = "century.stone"
    _description = "Stone"
    _columns = {
	'name': fields.char('Stone Color', size=125),
	'level': fields.integer('Stone Level'),
	'plan_price': fields.float('Plan Price'),
    }

    _defaults = {
    }
century_stone()


#
#  Work Order Location
#
class century_workorder_location(osv.osv):
    _auto = True
    _name = "century.workorder.location"
    _description = "Work Order Location"
    _columns = {
	'name': fields.char('Name', size=125),
    }

    _defaults = {
    }
century_workorder_location()

#
#  Work Order Edge
#
class century_workorder_edge(osv.osv):
    _auto = True
    _name = "century.workorder.edge"
    _description = "Work Order Edge"
    _columns = {
	'name': fields.char('Name', size=125),
    }

    _defaults = {
    }
century_workorder_edge()

#
#  Work Order Backsplash
#
class century_workorder_backsplash(osv.osv):
    _auto = True
    _name = "century.workorder.backsplash"
    _description = "Backsplash"
    _columns = {
	'name': fields.char('Name', size=125),
    }

    _defaults = {
    }
century_workorder_backsplash()

#
#  Work Order Sink
#
class century_workorder_sink(osv.osv):
    _auto = True
    _name = "century.workorder.sink"
    _description = "Sink"
    _columns = {
	'name': fields.char('Name', size=125),
    }

    _defaults = {
    }
century_workorder_sink()

#
#  Work Order Schedule Activity Type
#
class century_workorder_scheduleactivity_type(osv.osv):
    _auto = True
    _name = "century.workorder.scheduleactivity.type"
    _description = "Schedule Activity Type"
    _columns = {
	'name': fields.char('Name', size=125),
    }

    _defaults = {
    }
century_workorder_scheduleactivity_type()

#
#  Work Order Schedule Activity State
#
class century_workorder_scheduleactivity_state(osv.osv):
    _auto = True
    _name = "century.workorder.scheduleactivity.state"
    _description = "Schedule Activity State"
    _columns = {
	'name': fields.char('Name', size=125),
	'sequence': fields.integer('Sequence'),
    }

    _defaults = {
    }
century_workorder_scheduleactivity_type()
#
#  Work Order Crew
#
class century_workorder_crew(osv.osv):
    _auto = True
    _name = "century.workorder.crew"
    _description = "Crew"
    _columns = {
	'name': fields.char('Name', size=125),
	'activity_type': fields.char('Activity', size=125),
    }

    _defaults = {
    }
century_workorder_crew()

#
#  Work Order Crew (inherited because of the way that openerp handles
#  many2many relationships... both classes need to exist before declaring
#  the many2many relationship.
#
#class century_workorder_crew1(osv.osv):
    #_auto = True
    #_name = "century.workorder.crew"
    #_inherit = "century.workorder.crew"
    #_description = "Crew"
    #_columns = {
	#'scheduleactivity_types': fields.many2many("century.workorder.scheduleactivity.type", "crew_to_scheduleactivity_type", "crew_id", "scheduleactivity_id", "Schedule Activity Types"),
    #}
#
    #_defaults = {
    #}
#century_workorder_crew1()

#
#  Work Order
#
def workorder_name(obj, cr, uid, context):
	#print context
	return obj.pool.get('ir.sequence').get(cr, uid, 'century.workorder'),

class century_workorder(osv.osv):
    _auto = True
    _name = "century.workorder"
    _description = "Work Order"
    _columns = {
	'name': fields.char('WO Number', size=10),
	'job_id': fields.many2one('century.job', "Job"),
	'type': fields.selection((
	    ('countertop', 'Countertop'),
	    ('backsplash', 'Backsplash'),
	    ('tile', 'Tile'),
	    ('hardwood_flooring', 'Hardwood Flooring'),
	    ('service_call', 'Service Call'),
	), "Work Order Type"),
	'location_id': fields.many2one('century.workorder.location', "Location"),
	'thickness': fields.selection((
	    ('3', '3 CM'),
	    ('2', '2 CM'),
	), "Thickness"),
	'stone_id': fields.many2one('century.stone', "Stone"),
	'sq_ft': fields.float('SqFt'),
	'edge_id': fields.many2one('century.workorder.edge', "Edge"),
	'backsplash_id': fields.many2one('century.workorder.backsplash', "Backsplash"),
	'demo': fields.selection((
	    ('1', 'Yes'),
	    ('0', 'No'),
	), "Demo"),
	'sink_id': fields.many2one('century.workorder.sink', "Sink"),
	'num_sinks': fields.integer('Sinks'),
	'special_instructions': fields.text('Special Instructions'),
	#Relationships
	"scheduleactivities": fields.one2many("century.workorder.scheduleactivity", "workorder_id", "Schedule Activities"),
    }

    _defaults = {
	'sq_ft': 0.0
	#NOTE: this method uses up sequence numbers when you abort creation
	#'name': lambda obj, cr, uid, context: workorder_name(obj,cr,uid,context)
    }



    def create(self, cr, uid, values, context=None):
	#NOTE: we can either do this here, or in default.
	#the nice thing about doing it in default is that it appears in the new
	#record on edit.  The nice thing about doing it here is that
	#it doesn't assign a number when you cancel... Pick your poison.
	values['name'] = self.pool.get('ir.sequence').get(cr, uid, 'century.workorder')
	activity_pool = self.pool.get('century.workorder.scheduleactivity')
	wo_type_2_activity_list = {
	  'countertop': ['Template', 'Fabrication', 'Installation'],
	  'tile': ['Tile Installation'],
	  'hardwood_flooring': ['Installation'],
	  'backsplash': ['Installation'],
	  'service_call': ['Service Call'],
	}
	
	a_activities = wo_type_2_activity_list.get(values['type'], ())
	#print "Activity list: " 
	#print a_activities
	id_workorder =  super(century_workorder, self).create(cr, uid, values, context=context)
	#rint "Ret from super: "
	#rint id_workorder
	for activity in a_activities:
	    print "Creating activity for: " + activity
	    activity_pool.create(cr,uid, {
		"type": activity,
		"workorder_id": id_workorder
	    })
	return id_workorder

century_workorder()


class century_workorder_scheduleactivity(osv.osv):

    _auto = True
    _name = "century.workorder.scheduleactivity"
    _description = "Schedule Activity"

    def _get_scheduleactivity_name(self, cr, uid, ids, field_name, arg, context):
	ret={}
	for activity in self.browse(cr, uid, ids, context):
		#ret[activity.id] = activity.type_id.name
		ret[activity.id] = activity.type
	return ret

    def write(self, cr, uid, ids, vals, context=None):
	print "in scheduleactivty::write: ", vals
	#if we're being asked to write the datetime...
	dt_utc = None
	try:
	    dt_utc = parser.parse(vals['datetime'])
	except Exception:
	    pass

	if dt_utc:
	    print "DT UTC: ", dt_utc
	    #get the user's time zone
	    user = self.pool.get('res.users').browse(cr,uid,uid)
	    tz_user = pytz.timezone(user.tz) if user.tz else tz_default
	    print "TZ User:", tz_user
	    #add in the timezone
	    dt_utc = dt_utc.replace(tzinfo=pytz.utc)
	    #localize the date we were given into the user's time
	    dt_tz_activity = dt_utc.astimezone(tz_user)
	    print "DT TZ: ", dt_tz_activity
	    #TODO: actually move the date hour and minute into vals
	    vals['date'] = dt_tz_activity.date()
	    vals['hour'] = "%02d" % dt_tz_activity.hour
	    vals['minute'] = "%02d" % dt_tz_activity.minute
	    print "New vals: ", vals


	return super(century_workorder_scheduleactivity, self).write(cr, uid, ids, vals, context=context)

    def onchange_datetime(self, cr, uid, ids, new_datetime):
	print "in onchange_datetime: ", new_datetime
	return {
		'date': "2012-08-09",
		'hour': "12",
		'minute': "30",
	}

    def _get_scheduleactivity_datetime(self, cr, uid, ids, field_name, arg, context):
	ret={}
	for activity in self.browse(cr, uid, ids, context):
		if activity.date:
			#dt_activity = parser.parse(activity.date) + datetime.timedelta(0, int(activity.hour)*60*60+int(activity.minute)*60)
			print "Date:", activity.date
			print "Hour:", activity.hour
			print "Minute:", activity.minute
			#get the user's time zone
			user = self.pool.get('res.users').browse(cr,uid,uid)
			tz_user = pytz.timezone(user.tz) if user.tz else tz_default
			print "user.tz:", user.tz
			print "TZ User:", tz_user
			#parse the activity date into a real datetime
			dt_tz_activity = parser.parse(activity.date)
			print "Activity TZ Date:", dt_tz_activity
			#convert the activity date to the user's time zone
			dt_utc_activity = tz_user.localize(dt_tz_activity).astimezone(pytz.utc)
			print "Activity UTC Date:", dt_utc_activity

			#add in hour and minute
			dt_utc_activity = dt_utc_activity + datetime.timedelta(hours=int(activity.hour), minutes=int(activity.minute))
			print "Activity UTC DT:", dt_utc_activity

			#eliminate the TZ info
			dt_utc_activity = dt_utc_activity.replace(tzinfo=None)
			print "Activity Save DT:", dt_utc_activity
			#save that
			ret[activity.id] = str(dt_utc_activity)
		else:
			ret[activity.id] = False
	return ret

    def _get_scheduleactivity_duration_float(self, cr, uid, ids, field_name, arg, context):
	ret={}
	for activity in self.browse(cr, uid, ids, context):
		ret[activity.id] = float(activity.duration)
	return ret
	
    def _get_possible_scheduling_states(self, cr, uid, ids, domain, read_group_order=None, access_rights_uid=None, context=None):
        stage_obj = self.pool.get('century.workorder.scheduleactivity.state')
        order = stage_obj._order
        access_rights_uid = access_rights_uid or uid
        if read_group_order == 'state_id desc':
            order = '%s desc' % order
        search_domain = []
        stage_ids = stage_obj._search(cr, uid, search_domain, order=order, access_rights_uid=access_rights_uid, context=context)
        result = stage_obj.name_get(cr, access_rights_uid, stage_ids, context=context)
        # restore order of the search
        result.sort(lambda x,y: cmp(stage_ids.index(x[0]), stage_ids.index(y[0])))

        fold = {}
	#TODO: consider folding... see project.py:_read_group_stage_ids
        print "ScheduleActivity _group_by_stage result: ", result
        return result, fold


    _group_by_full = {
	#'state': lambda *args, **kw: [ "Needs Scheduling", "Mon", "Tue", "Wed", "Thu", "Fri", "Future" ],
	'scheduling_state_id': _get_possible_scheduling_states,
    }
    _columns = {
	'workorder_id': fields.many2one('century.workorder', "Work Order", readonly=True),
	'sq_ft': fields.related(
	  'workorder_id',
	  'sq_ft',
	  type="float",
	  string="SqFt",
	  store=False,
	),
	'job_id': fields.related(
	  'workorder_id',
	  'job_id',
	  type="many2one",
	  relation="century.job",
	  string="Job",
	  store=False,
	),
	'stone_id': fields.related(
	  'workorder_id',
	  'stone_id',
	  type="many2one",
	  relation="century.stone",
	  string="Stone",
	  store=False,
	),

	'edge_id': fields.related(
	  'workorder_id',
	  'edge_id',
	  type="many2one",
	  relation="century.workorder.edge",
	  string="Edge",
	  store=False,
	),
	'sink_id': fields.related(
	  'workorder_id',
	  'sink_id',
	  type="many2one",
	  relation="century.workorder.sink",
	  string="Sink",
	  store=False,
	),

	'name': fields.function(
		_get_scheduleactivity_name,
		type='char',
		method=True,
		string="Activity Name",
	),
	'datetime': fields.function(
		_get_scheduleactivity_datetime,
		type='datetime',
		method=True,
		string="On",
		store=True

	),
	'duration_float': fields.function(
		_get_scheduleactivity_duration_float,
		type='float',
		method=True,
		string="Duration",
	),


	#'datetime': fields.datetime("On"),
	'type': fields.selection((
		('Template', 'Template'),
		('Fabrication', 'Fabrication'),
		('Installation', 'Installation'),
		('Service Call', 'Service Call'),
		('Tile Installation', 'Tile Installation'),
	),'Activity', readonly=True),

	'scheduling_state_id': fields.many2one('century.workorder.scheduleactivity.state', "Scheduling State"),
			
	#'type_id': fields.many2one('century.workorder.scheduleactivity.type', "Type"),
	#NOTE: we may want to make Activity Type its own Model.
	#      I tried this, with limited success because I couldn't get
	#      the domain filter to work, and I gave up.  However, this
	#      article:
	#        http://stackoverflow.com/questions/13286757/how-to-make-domain-dynamic-in-openerp
	#      suggests a couple of ways to do it, including using a function
        #      field, and using fields_view_get, and so on.

	'crew': fields.many2one('century.workorder.crew', "Crew", 
		domain= "[('activity_type', '=', type)]", change_default=True
	),
	'date': fields.date("Schedule Date"),
	'hour': fields.selection((
		('7', '7'),
		('8', '8'),
		('9', '9'),
		('10', '10'),
		('11', '11'),
		('12', '12'),
		('13', '13'),
		('14', '14'),
		('15', '15'),
		('16', '16'),
		('17', '17'),
	),'Hour'),
	'minute': fields.selection((
		('00', '00'),
		('15', '15'),
		('30', '30'),
		('45', '45'),
	),'Minute'),
	'duration': fields.selection((
		('1', '1h'),
		('1.5', '1h30m'),
		('2', '2h'),
		('2.5', '2h30m'),
		('3', '3h'),
		('3.5', '3h30m'),
		('4', '3h'),
	),'Duration'),

    }

    _defaults = {
    }
century_workorder_scheduleactivity()

# Modify the res.partner
class launch_map_partner(osv.osv):
    _inherit = "res.partner"

    def open_map(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        partner = self.browse(cr, uid, ids[0], context=context)
        url = "http://maps.google.com/maps?oi=map&q="
        if partner.street:
            url += partner.street.replace(' ','+')
        if partner.city:
            url += '+'+partner.city.replace(' ','+')
        if partner.state_id:
            url += '+'+partner.state_id.name.replace(' ','+')
        if partner.country_id:
            url += '+'+partner.country_id.name.replace(' ','+')
        if partner.zip:
            url += '+'+partner.zip.replace(' ','+')

        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new'
        }
