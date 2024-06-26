# https://github.com/django/django.git, branch main, commit adae619426b6f50046b3daaa744db52989c9d6db

import sys
import os
scriptPath = os.path.dirname(__file__)
sys.path.append(os.path.join(scriptPath, "../../"))
sys.path.append(os.path.join(scriptPath, "../projecttests"))
import general
import helper

import obfupy.transformers.rewriter as rewriter

import os

rewriterOptions = rewriter.Options()
# Don't bother to set extractFunction. The project uses inspect package to get local variable, extractFunction won't work for all functions.
rewriterOptions.extractFunction = not True
rewriterOptions.extractConstant = True # verified
rewriterOptions.extractBuiltinFunction = not True # auth_tests fails
rewriterOptions.renameLocalVariable = True # verified
rewriterOptions.aliasFunctionArgument = not True # auth_tests fails
rewriterOptions.addNopControlFlow = True # verified
rewriterOptions.invertBoolOperator = True # verified
rewriterOptions.expandIfCondition = True # verified
rewriterOptions.rewriteIf = True # verified
# Must be False since __doc__ is used in the project
rewriterOptions.removeDocString = False # verified
# Must be False since it compares with <= which not invertible, see function check_referrer_policy in django/django/core/checks/security/base.py
rewriterOptions.invertCompareOperator = False # verified
# This is not used since invertCompareOperator is False
rewriterOptions.invertCompareOperator.wrapInvertedCompareOperator = True
# sensitive_variables_wrapper is used by inspect, don't rename it
rewriterOptions.preservedNames = [ 'sensitive_variables_wrapper' ]

excludeFolderList = [
	'/tests/admin_scripts/custom_templates/', # the comment in the templates can't be removed.
	'/tests/sphinx/testdata', # the .py files are acturally data files, don't touch them.
]

def callback(data) :
	for folder in excludeFolderList :
		if folder in data.getFileName() :
			data.getOptions().enabled = False
			return
	if '/tests/migrations' in data.getFileName() :
		# test_alter_field_add_db_column_noop doesn't like it because assertIs will fail
		data.setOption(rewriterOptions.extractConstant, False)
		return
	if data.isFile() :
		return
	context = data.getContext()
	if context.isClass() :
		# Some classes inherits from enum.Enum and have if condition in class body.
		# If we rewrite the if condition, the newly generated assignment will cause enum.Enum throw exceptions.
		data.setOption(rewriterOptions.rewriteIf, False)
	else :
		data.setOption(rewriterOptions.rewriteIf, rewriterOptions[rewriterOptions.rewriteIf])

args = helper.parseCommandLine()
general.obfuscateProject(options = rewriterOptions, callback = callback, args = args)
outputPath = args['output']

def doTest() :
	os.chdir(outputPath)
	os.chdir('tests')
	mainCommand = 'python runtests.py '
	canTest = not lastTest
	testedCount = 0
	for folder in testFolderList :
		if not canTest :
			if folder == lastTest :
				canTest = True
		if not canTest :
			print('Skip ' + folder)
			continue
		command = mainCommand + folder
		print("\n")
		print('====================== Test ' + folder)
		result = os.system(command)
		if result != 0 :
			print('Error ' + folder)
			break
		testedCount += 1
		if countToTest > 0 and testedCount >= countToTest :
			break
	return

lastTest = 0 #'wsgi'
countToTest = -1
testFolderList = [
	"absolute_url_overrides",
	"admin_autodiscover",
	"admin_changelist",
	"admin_checks",
	"admin_custom_urls",
	"admin_default_site",
	"admin_docs",
	"admin_filters",
	"admin_inlines",
	"admin_ordering",
	"admin_registration",
	"admin_scripts",
	"admin_utils",
	"admin_views",
	"admin_widgets",
	"aggregation",
	"aggregation_regress",
	"annotations",
	"app_loading",
	"apps",
	"asgi",
	"async",
	"auth_tests",
	"backends",
	"base",
	"bash_completion",
	"basic",
	"builtin_server",
	"bulk_create",
	"cache",
	"check_framework",
	"conditional_processing",
	"constraints",
	"contenttypes_tests",
	"context_processors",
	"csrf_tests",
	"custom_columns",
	"custom_lookups",
	"custom_managers",
	"custom_methods",
	"custom_migration_operations",
	"custom_pk",
	"datatypes",
	"dates",
	"datetimes",
	"db_functions",
	"db_typecasts",
	"db_utils",
	"dbshell",
	"decorators",
	"defer",
	"defer_regress",
	"delete",
	"delete_regress",
	"deprecation",
	"dispatch",
	"distinct_on_fields",
	"empty",
	"empty_models",
	"expressions",
	"expressions_case",
	"expressions_window",
	"extra_regress",
	"field_deconstruction",
	"field_defaults",
	"field_subclassing",
	#"file_storage", # gbk encoding error
	"file_uploads",
	"files",
	"filtered_relation",
	"fixtures",
	"fixtures_model_package",
	"fixtures_regress",
	"flatpages_tests",
	"force_insert_update",
	"foreign_object",
	"forms_tests",
	"from_db_value",
	"generic_inline_admin",
	"generic_relations",
	"generic_relations_regress",
	"generic_views",
	"get_earliest_or_latest",
	"get_object_or_404",
	"get_or_create",
	# "gis_tests", # A GIS database backend is required to run gis_tests.
	"handlers",
	"httpwrappers",
	"humanize_tests",
	# "i18n", # gbk encoding error
	# "import_error_package", # Oops
	"indexes",
	"inline_formsets",
	"inspectdb",
	"introspection",
	"invalid_models_tests",
	"known_related_objects",
	"logging_tests",
	"lookup",
	"m2m_and_m2o",
	"m2m_intermediary",
	"m2m_multiple",
	"m2m_recursive",
	"m2m_regress",
	"m2m_signals",
	"m2m_through",
	"m2m_through_regress",
	"m2o_recursive",
	"mail",
	"managers_regress",
	"many_to_many",
	"many_to_one",
	"many_to_one_null",
	"max_lengths",
	"messages_tests",
	"middleware",
	"middleware_exceptions",
	"migrate_signals",
	"migration_test_data_persistence",
	"migrations",
	"migrations2",
	"model_enums",
	"model_fields",
	"model_forms",
	"model_formsets",
	"model_formsets_regress",
	"model_indexes",
	"model_inheritance",
	"model_inheritance_regress",
	"model_meta",
	"model_options",
	"model_package",
	"model_regress",
	"model_utils",
	"modeladmin",
	"multiple_database",
	"mutually_referential",
	"nested_foreign_keys",
	"no_models",
	"null_fk",
	"null_fk_ordering",
	"null_queries",
	"one_to_one",
	"or_lookups",
	"order_with_respect_to",
	"ordering",
	"pagination",
	"postgres_tests",
	"prefetch_related",
	"project_template",
	"properties",
	"proxy_model_inheritance",
	"proxy_models",
	"queries",
	"queryset_pickle",
	"raw_query",
	"redirects_tests",
	"requests_tests",
	"requirements",
	"reserved_names",
	"resolve_url",
	"responses",
	"reverse_lookup",
	"save_delete_hooks",
	"schema",
	"select_for_update",
	"select_related",
	"select_related_onetoone",
	"select_related_regress",
	"serializers",
	"servers",
	"sessions_tests",
	"settings_tests",
	"shell",
	"shortcuts",
	"signals",
	"signed_cookies_tests",
	"signing",
	"sitemaps_tests",
	"sites_framework",
	"sites_tests",
	"sphinx",
	"staticfiles_tests",
	"str",
	"string_lookup",
	"swappable_models",
	"syndication_tests",
	"template_backends",
	"template_loader",
	"template_tests",
	"templates",
	"test_client",
	"test_client_regress",
	"test_exceptions",
	"test_runner",
	# "test_runner_apps", # All are failures and they are not handled by this test script
	"test_utils",
	"timezones",
	"transaction_hooks",
	"transactions",
	"unmanaged_models",
	"unused",
	"update",
	"update_only_fields",
	"urlpatterns",
	"urlpatterns_reverse",
	"user_commands",
	# "utils_tests", # gbk and inspect related errors
	"validation",
	"validators",
	"version",
	# "view_tests", # It uses inspect package
	"wsgi",
	"xor_lookups",
]

doTest()
