from cohort_manager.dao import InvalidCollectionException
from uw_adsel import AdSel
from uw_adsel.models import CohortAssignment, MajorAssignment, Application, \
    PurpleGoldAssignment, PurpleGoldApplication
from restclients_core.exceptions import DataFailureException
from cohort_manager.models import SyskeyImport
import pytz


MAJOR_COLLECTION_TYPE = "major"
COHORT_COLLECTION_TYPE = "cohort"
PURPLEGOLD_COLLECTION_TYPE = "purplegold"


def get_quarters_with_current():
    client = AdSel()
    quarters = client.get_quarters()
    return quarters


def get_collection_by_id_type(id, collection_type, quarter):
    if collection_type == MAJOR_COLLECTION_TYPE:
        return _get_major_by_id(id.upper(), quarter)
    elif collection_type == COHORT_COLLECTION_TYPE:
        return _get_cohort_by_id(int(id), quarter)
    else:
        raise InvalidCollectionException(collection_type)


def _get_cohort_by_id(cohort_id, quarter):
    client = AdSel()
    cohorts = client.get_cohorts_by_qtr(quarter)
    for cohort in cohorts:
        if cohort.cohort_number == cohort_id:
            return {
                "collection_id": cohort_id,
                "residency": cohort.cohort_residency,
                "admit_decision": cohort.admit_decision,
                "protected_group": cohort.protected_group,
                "description": cohort.cohort_description,
                "applications_assigned": cohort.assigned_count
            }


def _get_major_by_id(major_id, quarter):
    client = AdSel()
    try:
        major = client.get_major_details_by_qtr_major(quarter, major_id)
        return {"collection_id": major.major_abbr,
                "applications_assigned": major.assigned_count,
                "program_code": major.program_code,
                "major_pathway": major.major_pathway,
                "display_name": major.display_name,
                "college": major.college,
                "division": major.division,
                "dtx": major.dtx,
                "assigned_resident": major.assigned_resident,
                "assigned_nonresident": major.assigned_nonresident,
                "assigned_international": major.assigned_international}
    except DataFailureException:
        return None


def get_applications_by_type_id_qtr(type, id, quarter):
    apps = []
    if type == COHORT_COLLECTION_TYPE:
        apps = get_applications_by_cohort_qtr(id, quarter)
    if type == MAJOR_COLLECTION_TYPE:
        apps = get_applications_by_major_qtr(id, quarter)
    if type == PURPLEGOLD_COLLECTION_TYPE:
        client = AdSel()
        apps = client.get_all_applications_by_qtr(quarter)
    return apps


def get_applications_by_cohort_qtr(cohort_id, quarter):
    matching_apps = []
    try:
        client = AdSel()
        applications = client.get_all_applications_by_qtr(quarter)

        for application in applications:
            if application.assigned_cohort == int(cohort_id):
                matching_apps.append(application)
    except DataFailureException:
        pass
    return matching_apps


def get_applications_by_major_qtr(major_id, quarter):
    try:
        client = AdSel()
        applications = client.get_all_applications_by_qtr(quarter)
        matching_apps = []
        for application in applications:
            if application.major_program_code == major_id:
                matching_apps.append(application)
    except DataFailureException:
        pass
    return matching_apps


def get_activity_log(**kwargs):
    activities = AdSel().get_filtered_activities(**kwargs)
    activity_json = []
    for activity in activities:
        try:
            date = pytz.utc.localize(activity.assignment_date)
        except ValueError:
            date = activity.assignment_date
        act = {'activity_date': date,
               'comment': activity.comment,
               'assigned_msg': activity.total_assigned,
               'submitted_msg': activity.total_submitted,
               'user': activity.user,
               'cohort': activity.cohort_number,
               'major': activity.major_abbr,
               'collection_type': 'Cohort' if activity.major_abbr is None
               else 'Major'}
        activity_json.append(act)
    return activity_json


def get_collection_list_by_type(collection_type, quarter_id):
    if collection_type == MAJOR_COLLECTION_TYPE:
        client = AdSel()
        majors = client.get_majors_by_qtr(quarter_id)
        response = []
        for major in majors:
            response.append({'value': major.program_code,
                             'abbr': major.major_abbr,
                             'text': major.display_name,
                             'division': major.division,
                             'college': major.college,
                             'dtx': major.dtx,
                             'assigned_count': major.assigned_count})

        return response
    elif collection_type == COHORT_COLLECTION_TYPE:
        client = AdSel()
        cohorts = client.get_cohorts_by_qtr(quarter_id)
        response = []
        for cohort in cohorts:
            response.append({'value': cohort.cohort_number,
                             'text': cohort.cohort_description,
                             'description': cohort.cohort_description,
                             'residency': cohort.cohort_residency,
                             'protected': cohort.protected_group,
                             'admit_decision': cohort.admit_decision,
                             'assigned_count': cohort.assigned_count
                             })

        sorted_response = sorted(response, key=lambda k: k['value'])
        return sorted_response
    else:
        raise InvalidCollectionException(collection_type)


def get_application_by_qtr_syskey(qtr_id, syskey):
    return AdSel().get_applications_by_qtr_syskey(qtr_id, syskey)


def get_apps_by_qtr_id_syskey_list(qtr_id, syskeys):
    app_list = []
    invalid_syskeys = []
    for syskey in syskeys:
        try:
            app_list += get_application_by_qtr_syskey(qtr_id, syskey)
        except DataFailureException:
            invalid_syskeys.append(syskey)
    return app_list, invalid_syskeys


def _get_collection(assignment_import):
    assignment_set = []
    if isinstance(assignment_import, SyskeyImport):
        if assignment_import.cohort:
            assignment = CohortAssignment()
            assignment.override_previous = assignment_import.is_reassign
            assignment.override_protected = \
                assignment_import.is_reassign_protected
            assignment.cohort_number = assignment_import.cohort
            assignment_set = assignment_import.get_assignments()
        elif assignment_import.major and len(assignment_import.major) > 0:
            assignment = MajorAssignment()
            assignment.major_code = assignment_import.major
            assignment_set = assignment_import.get_assignments()
    else:
        assignment = PurpleGoldAssignment()
        assignment_set = assignment_import.purplegoldlistassignment_set.all()

    assignment.assignment_type = "file" if \
        assignment_import.upload_filename is not None else "manual"
    assignment.comments = assignment_import.comment
    if assignment_import.upload_filename:
        assignment.comments += "\nFile: " + assignment_import.upload_filename
    assignment.user = assignment_import.created_by

    applicants_to_assign = []
    campus_lookup = {"Seattle": 1,
                     "Tacoma": 2,
                     "Bothell": 3}
    for imp_assignment in assignment_set:
        # Omit apps we couldn't find in Adsel
        if imp_assignment.admission_selection_id is None:
            continue
        app = imp_assignment.get_application()
        applicants_to_assign.append(app)
        assignment.quarter = assignment_import.quarter
        assignment.campus = campus_lookup.get(assignment_import.campus, 0)

    assignment.applicants = applicants_to_assign
    return assignment_import, assignment


def submit_collection(assignment_import):
    (assignment_import, assignment) = _get_collection(assignment_import)
    client = AdSel()
    client.get_quarters()
    if isinstance(assignment_import, SyskeyImport):
        if assignment_import.cohort:
            if assignment_import.upload_filename is not None:
                return client.assign_cohorts_bulk(assignment)
            else:
                return client.assign_cohorts_manual(assignment)
        elif assignment_import.major and len(assignment_import.major) > 0:
            return client.assign_majors(assignment)
    else:
        return client.assign_purple_gold(assignment)


def reset_collection(assignment_import, collection_type):
    if collection_type == COHORT_COLLECTION_TYPE:
        assignment = CohortAssignment()
        assignment.override_previous = True
        assignment.override_protected = True
        assignment.cohort_number = assignment_import.cohort
    elif collection_type == MAJOR_COLLECTION_TYPE:
        assignment = MajorAssignment()
        assignment.major_code = assignment_import.major

    assignment.assignment_type = "file" if \
        assignment_import.is_file_upload else "manual"
    assignment.comments = assignment_import.comment
    assignment.user = assignment_import.created_by
    assignment.campus = assignment_import.campus
    assignment.quarter = assignment_import.quarter

    applicants_to_assign = []
    for imp_assignment in assignment_import.get_assignments():
        app = imp_assignment.get_application()
        applicants_to_assign.append(app)
        assignment.quarter = assignment_import.quarter

    assignment.applicants = applicants_to_assign

    client = AdSel()
    if collection_type == COHORT_COLLECTION_TYPE:
        client.assign_cohorts_bulk(assignment)
    elif collection_type == MAJOR_COLLECTION_TYPE:
        client.assign_majors(assignment)


def reset_purplegold(import_args, apps):
    assignment = PurpleGoldAssignment()
    assignment.assignment_type = "file"
    assignment.quarter = import_args['quarter']
    assignment.campus = import_args['campus']
    assignment.user = import_args['created_by']
    assignment.comments = import_args['comment']

    applicants_to_assign = []
    for app in apps:
        applicants_to_assign.append(
            PurpleGoldApplication(adsel_id=app.adsel_id,
                                  award_amount=0))
    assignment.applicants = applicants_to_assign

    client = AdSel()
    client.assign_purple_gold(assignment)


def get_application_from_bulk_upload(upload_json):
    applications = []
    for application in upload_json:
        app = Application()
        app.adsel_id = application['admission_selection_id']
        app.application_number = application['application_number']
        app.assigned_cohort = application['assigned_cohort']
        app.assigned_major = application['assigned_major']
        app.campus = _get_campus_id(application['campus'])
        app.system_key = application['system_key']
        applications.append(app)
    return applications


def _get_campus_id(campus_name):
    mapping = {"Seattle": 1, "Tacoma": 2, "Bothell": 3}
    return mapping[campus_name]
