from cohort_manager.dao import InvalidCollectionException
MAJOR_COLLECTION_TYPE = "major"
COHORT_COLLECTION_TYPE = "cohort"


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
