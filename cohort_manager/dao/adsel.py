from cohort_manager.dao import InvalidCollectionException
from cohort_manager.models import Activity, Assignment, AssignmentImport
from uw_adsel import AdSel
from datetime import datetime


MAJOR_COLLECTION_TYPE = "major"
COHORT_COLLECTION_TYPE = "cohort"


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
    majors = client.get_majors_by_qtr(quarter)
    for major in majors:
        if major.major_abbr == major_id:
            return {"collection_id": major.major_abbr,
                    "applications_assigned": major.assigned_count}


def get_activity_log():
    # filtering removed for V1 release
    activities = AdSel().get_activities()
    activity_json = []
    for activity in activities:
        act = {'activity_date': activity.assignment_date,
               'comment': activity.comment,
               'assigned_msg': activity.total_assigned,
               'submitted_msg': activity.total_submitted,
               'user': activity.user,
               'cohort': activity.cohort_number,
               'major': activity.major_abbr}
        activity_json.append(act)
    return activity_json


def get_collection_list_by_type(collection_type, quarter_id):
    if collection_type == MAJOR_COLLECTION_TYPE:
        client = AdSel()
        majors = client.get_majors_by_qtr(quarter_id)
        response = []
        for major in majors:
            response.append({'value': major.major_abbr,
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

        return response
    else:
        raise InvalidCollectionException(collection_type)


def get_application_by_syskey(syskey):
    # TODO: Implement a real ADSEL API query
    if syskey == "123":
        assignment = Assignment(system_key="123",
                                campus=0,
                                year=2019,
                                quarter=1,
                                application_number=1,
                                admission_selection_id="123,0,2019,1,1",
                                cohort="1",
                                major="foo")
        return [assignment]
    if syskey == "asd":
        assignment = Assignment(system_key="asd",
                                campus=0,
                                year=2019,
                                quarter=1,
                                application_number=1,
                                admission_selection_id="123,0,2019,1,1",
                                cohort="1",
                                major="foo")
        assignment2 = Assignment(system_key="asd",
                                 campus=0,
                                 year=2019,
                                 quarter=1,
                                 application_number=2,
                                 admission_selection_id="asd,0,2019,1,2",
                                 cohort="1",
                                 major="foo")
        assignment3 = Assignment(system_key="asd",
                                 campus=0,
                                 year=2019,
                                 quarter=1,
                                 application_number=3,
                                 admission_selection_id="asd,0,2019,1,3",
                                 cohort="1",
                                 major="foo")
        return [assignment, assignment2, assignment3]
    if syskey == "123asd":
        assignment = Assignment(system_key="123asd",
                                campus=0,
                                year=2019,
                                quarter=1,
                                application_number=1,
                                admission_selection_id="123asd,0,2019,1,1",
                                cohort="1",
                                major="foo")
        assignment2 = Assignment(system_key="123asd",
                                 campus=0,
                                 year=2019,
                                 quarter=1,
                                 application_number=2,
                                 admission_selection_id="123asd,0,2019,1,2",
                                 cohort="1",
                                 major="foo")
        return [assignment, assignment2]


def get_apps_by_syskey_list(syskeys):
    app_list = []
    for syskey in syskeys:
        app_list += get_application_by_syskey(syskey)
    return app_list
