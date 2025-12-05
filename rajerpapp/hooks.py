app_name = "rajerpapp"
app_title = "Rajerpapp"
app_publisher = "Abdulqadir"
app_description = "Erp"
app_email = "abdulkadirtravady@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "rajerpapp",
# 		"logo": "/assets/rajerpapp/logo.png",
# 		"title": "Rajerpapp",
# 		"route": "/rajerpapp",
# 		"has_permission": "rajerpapp.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/rajerpapp/css/rajerpapp.css"
# app_include_js = "/assets/rajerpapp/js/rajerpapp.js"

# include js, css files in header of web template
# web_include_css = "/assets/rajerpapp/css/rajerpapp.css"
# web_include_js = "/assets/rajerpapp/js/rajerpapp.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "rajerpapp/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "rajerpapp/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "rajerpapp.utils.jinja_methods",
# 	"filters": "rajerpapp.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "rajerpapp.install.before_install"
# after_install = "rajerpapp.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "rajerpapp.uninstall.before_uninstall"
# after_uninstall = "rajerpapp.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "rajerpapp.utils.before_app_install"
# after_app_install = "rajerpapp.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "rajerpapp.utils.before_app_uninstall"
# after_app_uninstall = "rajerpapp.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "rajerpapp.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Order": {
		"on_submit": "rajerpapp.boms.create_custom_bom"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"rajerpapp.tasks.all"
# 	],
# 	"daily": [
# 		"rajerpapp.tasks.daily"
# 	],
# 	"hourly": [
# 		"rajerpapp.tasks.hourly"
# 	],
# 	"weekly": [
# 		"rajerpapp.tasks.weekly"
# 	],
# 	"monthly": [
# 		"rajerpapp.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "rajerpapp.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "rajerpapp.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "rajerpapp.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["rajerpapp.utils.before_request"]
# after_request = ["rajerpapp.utils.after_request"]

# Job Events
# ----------
# before_job = ["rajerpapp.utils.before_job"]
# after_job = ["rajerpapp.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"rajerpapp.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []
