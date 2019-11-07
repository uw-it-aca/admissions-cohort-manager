from cohort_manager.dao import InvalidCollectionException
from cohort_manager.models import Activity, Assignment, AssignmentImport
from datetime import datetime
from cohort_manager.utils import to_csv
from uw_adsel import AdSel
from datetime import datetime
from restclients_core.exceptions import DataFailureException


MAJOR_COLLECTION_TYPE = "major"
COHORT_COLLECTION_TYPE = "cohort"


def get_current_quarter():
    # Returns the quarter we're currently in
    # or the first quarter in the list if not
    client = AdSel()
    quarters = client.get_quarters()
    now = datetime.now()
    for quarter in quarters:
        if quarter.begin < now < quarter.end:
            return quarter
    return quarter[0]


def get_collection_by_id_type(id, collection_type):
    if collection_type == MAJOR_COLLECTION_TYPE:
        return _get_major_by_id(id.upper())
    elif collection_type == COHORT_COLLECTION_TYPE:
        return _get_cohort_by_id(int(id))
    else:
        raise InvalidCollectionException(collection_type)


def _get_cohort_by_id(cohort_id):
    # TODO: Once AdSel API exists make this a real call
    response = None
    if cohort_id == 1:
        response = {
            "collection_id": cohort_id,
            "residency": 'wa-res',
            "admit_decision": "Admit",
            "protected_group": False,
            "description": "WA resident general admits",
            "applications_assigned": 412
        }
    if cohort_id == 2:
        response = {
            "collection_id": cohort_id,
            "residency": 'non-res',
            "admit_decision": "Deny",
            "protected_group": False,
            "description": "Nonresident denied admissions",
            "applications_assigned": 45
        }
    if cohort_id == 99:
        response = {
            "collection_id": cohort_id,
            "residency": 'wa-res',
            "admit_decision": "Admit",
            "protected_group": True,
            "description": "Protected for that sweet, sweet NCAA money",
            "applications_assigned": 124
        }
    return response


def _get_major_by_id(major_id):
    # TODO: Once AdSel API exists make this a real call
    response = None
    if major_id == "CSE":
        response = {
            "collection_id": major_id,
            "residency": 'wa-res',
            "admit_decision": "Admit",
            "protected_group": False,
            "description": "Computer Science and Enginerding",
            "applications_assigned": 543
        }
    if major_id == "CHEM":
        response = {
            "collection_id": major_id,
            "residency": 'non-res',
            "admit_decision": "Admit",
            "protected_group": False,
            "description": "Chemistry",
            "applications_assigned": 235
        }
    if major_id == "ART H":
        response = {
            "collection_id": major_id,
            "residency": 'wa-res',
            "admit_decision": "Admit",
            "protected_group": False,
            "description": "Art History",
            "applications_assigned": 756
        }
    return response


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
    # TODO: Implement a real ADSEL API query
    if collection_type == MAJOR_COLLECTION_TYPE:
        client = AdSel()
        majors = client.get_majors_by_qtr(quarter_id)
        response = []
        for major in majors:
            response.append({'id': major.major_abbr,
                             'name': major.display_name})

        return response
    elif collection_type == COHORT_COLLECTION_TYPE:
        client = AdSel()
        cohorts = client.get_cohorts_by_qtr(quarter_id)
        response = []
        for cohort in cohorts:
            response.append({'id': cohort.cohort_number,
                             'name': cohort.cohort_number,
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
