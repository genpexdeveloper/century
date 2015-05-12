{
        "name" : "Century",
        "version" : "0.1",
        "category" : "Generic Modules/Others",
        "description" : """
This module provides the Century Job Scheduling Application
============================================================

The following models are provided:

  * Job - A Job
  * Schedule Activity - an activity to be scheduled
  * Stone - A type of stone
  * Work Order - A Work order
""",
        "author": "Shaun Dawson @ WhiteHawk Software",
        "website" : "http://www.whitehawksoftware.org",
	"summary" : "Century Scheduling",
	"sequence" : 10,
        "depends" : [ 
		"base",
		'project',
	],
	"data" : [
		#"security/ir.model.access.csv",
	],
	
        "update_xml" : [
		"century_view.xml",
		"wizard/activity_date_wizard_view.xml",
		"report/report_view.xml",
	],
        "init_xml" : [
	],
        "demo_xml" : [
	],
	"test": [
	],
	"css": [
	],
	"images": [
	],
        "installable" : True,
	"application" : True,
        "auto_install" : False,
        "active" : False,
}



