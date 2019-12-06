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


def get_activity_log(assignment_type=None,
                     cohort_id=None,
                     major_id=None,
                     system_key=None):
    # Assumes that ONLY one filter is set
    if assignment_type is not None:
        return _get_activity_log_by_type(assignment_type)
    if cohort_id is not None:
        return _get_activity_log_by_cohort_id(cohort_id)
    if major_id is not None:
        return _get_activity_log_by_major_id(major_id)
    if system_key is not None:
        return _get_activity_log_by_system_key(system_key)
    else:
        return _get_activity_log_all()


def _get_activity_log_by_type(assignment_type):
    # TODO: Implement real ADSEL API query
    activity1 = Activity(activity_date=datetime(year=2019,
                                                month=8,
                                                day=14,
                                                hour=6,
                                                minute=4,
                                                second=12,),
                         user="javerage",
                         submitted_msg="Submitted: Assign 3 (manual) to"
                                       " Cohort 1",
                         assigned_msg="Assigned: 3 applications to Cohort 1",
                         comment="I'm adding 3 more applicants")
    activity2 = Activity(activity_date=datetime(year=2019,
                                                month=1,
                                                day=4,
                                                hour=16,
                                                minute=25,
                                                second=9,),
                         user="billsea",
                         submitted_msg="Submitted: Assign 325 (file) to "
                                       "Cohort 2",
                         assigned_msg="Assigned: 325 applications to Cohort 1",
                         comment="I'm adding 325 more applicants")
    activity3 = Activity(activity_date=datetime(year=2019,
                                                month=3,
                                                day=4,
                                                hour=16,
                                                minute=25,
                                                second=9,),
                         user="javerage",
                         submitted_msg="Submitted: Assign 1 (file) to "
                                       "Cohort 41",
                         assigned_msg="Assigned: 1 applications to Cohort 41",
                         comment="I'm adding 1 more applicants")
    activity4 = Activity(activity_date=datetime(year=2019,
                                                month=2,
                                                day=4,
                                                hour=16,
                                                minute=25,
                                                second=9,),
                         user="javerage",
                         submitted_msg="Submitted: Assign 325 (file) to "
                                       "Cohort 41",
                         assigned_msg="Assigned: 325 applications to "
                                      "Cohort 41",
                         comment="I'm adding 325 more applicants")
    return [activity1, activity2, activity3, activity4]


def _get_activity_log_by_major_id(major_id):
    # TODO: Implement real ADSEL API query
    activity1 = Activity(activity_date=datetime(year=2019,
                                                month=3,
                                                day=16,
                                                hour=6,
                                                minute=4,
                                                second=12,),
                         user="japplicant",
                         submitted_msg="Submitted: Assign 12 (manual) to "
                                       "Chemistry",
                         assigned_msg="Assigned: 12 applications to Chemistry",
                         comment="I'm adding 12 more applicants to chem")
    activity2 = Activity(activity_date=datetime(year=2019,
                                                month=11,
                                                day=4,
                                                hour=16,
                                                minute=25,
                                                second=9,),
                         user="jinter",
                         submitted_msg="Submitted: Assign 325 (file) to "
                                       "CSE",
                         assigned_msg="Assigned: 325 applications to CSE",
                         comment="I'm adding 325 more applicants to CSE")
    return [activity1, activity2]


def _get_activity_log_by_cohort_id(cohort_id):
    # TODO: Implement real ADSEL API query
    activity1 = Activity(activity_date=datetime(year=2019,
                                                month=8,
                                                day=14,
                                                hour=6,
                                                minute=4,
                                                second=12,),
                         user="billseata",
                         submitted_msg="Submitted: Assign 3 (manual) to "
                                       "Cohort 1",
                         assigned_msg="Assigned: 3 applications to Cohort 1",
                         comment="I'm adding 3 more applicants")
    activity2 = Activity(activity_date=datetime(year=2019,
                                                month=1,
                                                day=4,
                                                hour=16,
                                                minute=25,
                                                second=9,),
                         user="billsea",
                         submitted_msg="Submitted: Assign 11 (file) to "
                                       "Cohort 1",
                         assigned_msg="Assigned: 11 applications to Cohort 1",
                         comment="I'm adding 11 more applicants")
    return [activity1, activity2]


def _get_activity_log_by_system_key(system_key):
    # TODO: Implement real ADSEL API query
    activity1 = Activity(activity_date=datetime(year=2019,
                                                month=8,
                                                day=14,
                                                hour=6,
                                                minute=4,
                                                second=12,),
                         user="billbot",
                         submitted_msg="Submitted: Assign 3 (manual) to"
                                       " Cohort 1",
                         assigned_msg="Assigned: 3 applications to Cohort 1",
                         comment="I'm adding 3 more applicants, including "
                                 "syskey 123")
    activity2 = Activity(activity_date=datetime(year=2019,
                                                month=1,
                                                day=4,
                                                hour=16,
                                                minute=25,
                                                second=9,),
                         user="billsea",
                         submitted_msg="Submitted: Assign 325 (file) to CSE",
                         assigned_msg="Assigned: 3 applications to CSE",
                         comment="I'm adding 3 more applicants including "
                                 "syskey 123")
    return [activity1, activity2]


def _get_activity_log_all():
    # TODO: Implement real ADSEL API query
    return _get_activity_log_by_cohort_id('')\
           + _get_activity_log_by_type('a')\
           + _get_activity_log_by_major_id('')\
           + _get_activity_log_by_system_key('')


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
