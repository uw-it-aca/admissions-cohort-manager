from django.db import models
from django.core.exceptions import ValidationError
from cohort_manager.utils import to_csv, dict_to_csv, get_headers
from io import StringIO
import csv
import json


def validate_system_key(val):
    pass


def validate_year(val):
    pass


def validate_application_number(val):
    pass


def validate_cohort(val):
    pass


def validate_major(val):
    pass


class AssignmentImportManager(models.Manager):
    def create_from_file(self, uploaded_file, **kwargs):
        kwargs['is_file_upload'] = True
        kwargs['document'] = uploaded_file.read().decode('utf-16')
        kwargs['upload_filename'] = uploaded_file.name
        return AssignmentImport(**kwargs)

    def create_from_list(self, applications, **kwargs):
        document = to_csv(AssignmentImport.FIELD_NAMES)
        for application in applications:
            document += to_csv([application.system_key,
                                application.campus,
                                2009,
                                application.quarter_id,
                                application.application_number,
                                application.adsel_id])

        kwargs['is_file_upload'] = False
        kwargs['document'] = document
        return AssignmentImport(**kwargs)


class AssignmentImport(models.Model):
    FIELD_STUDENT_NAME = 'StudentName'
    FIELD_SYSTEM_KEY = 'SDBSrcSystemKey'
    FIELD_APPLICATION_NUMBER = 'ApplicationNbr'
    FIELD_GENDER = 'Gender'
    FIELD_UNDERREP_MINORITY = 'UnderrepresentedMinorityDesc'
    FIELD_IPEDS_RACE = 'IPEDSRaceEthnicityCategory'
    FIELD_RESIDENT_GROUP = 'ResidentGroup'
    FIELD_COHORT = 'SDBCohort'
    FIELD_APPLICATION_STATUS = 'SDBApplicationStatus'
    FIELD_HS_GPA = 'HighSchoolGPA'
    FIELD_LOW_INCOME = 'LowFamilyIncomeInd'
    FIELD_FIRST_GEN = 'FirstGenerationInd'
    FIELD_ATHLETE_CODE = 'AthleteCode'
    FIELD_REQUESTED_MAJOR_NAME = 'RequestedMajor1Name'
    FIELD_REQUESTED_MAJOR_COLLEGE = 'RequestedMajor1College'
    FIELD_REQUESTED_MAJOR_1_NAME = 'RequestedMajor1Name'
    FIELD_REQUESTED_MAJOR_1_COLLEGE = 'RequestedMajor1College'
    FIELD_ASSIGNED_MAJOR_NAME = 'AssignedMajor1Name'
    FIELD_PERMANENT_STATE = 'PermanentState'
    FIELD_FR_ADMISSIONS_RECOM = 'FRAdmissionsRecommendation'
    FIELD_FR_ACADEMIC = 'FRAcademic'
    FIELD_FRPQA = 'FRPQA'
    FIELD_CADR_ENG_DEF = 'CADREnglishDeficiency'
    FIELD_CADR_MATH_DEF = 'CADRMathDeficiency'
    FIELD_CADR_LABSCI_DEF = 'CADRLabScienceDeficiency'
    FIELD_SOCIALSCI_DEF = 'CADRSocialScienceDeficiency'
    FIELD_FORLANG_DEF = 'CADRForeignLanguageDeficiency'
    FIELD_MATH_LEVEL = 'MathLevelCode'
    FIELD_REASON = 'ReasonCode'
    FIELD_LAST_SCHOOL_CODE = 'LastSchoolCode'
    FIELD_LAST_SCHOOL_NAME = 'LastSchoolName'
    FIELD_HS_CODE = 'HighSchoolCode'
    FIELD_HS_NAME = 'HighSchoolName'
    FIELD_HS_CITY = 'HighSchoolCity'
    FIELD_HS_STATE = 'HighSchoolState'
    FIELD_HS_FRL_PCT = 'HighSchoolFRLPct'
    FIELD_ASSIGNED_COHORT = 'AssignedCohort'
    FIELD_ASSIGNED_MAJOR_CODE = 'AssignedMajorProgramCode'
    FIELD_HIGHEST_CONCORDED_SAT_MATH = 'HighestConcordedSATMath'
    FIELD_ADSEL_ID = 'AdmissionsSelectionId'
    FIELD_EMPTY = ''

    FIELD_NAMES = [FIELD_STUDENT_NAME, FIELD_SYSTEM_KEY,
                   FIELD_APPLICATION_NUMBER, FIELD_GENDER,
                   FIELD_UNDERREP_MINORITY, FIELD_IPEDS_RACE,
                   FIELD_RESIDENT_GROUP, FIELD_COHORT,
                   FIELD_APPLICATION_STATUS, FIELD_HS_GPA, FIELD_LOW_INCOME,
                   FIELD_FIRST_GEN, FIELD_ATHLETE_CODE,
                   FIELD_REQUESTED_MAJOR_NAME, FIELD_REQUESTED_MAJOR_COLLEGE,
                   FIELD_REQUESTED_MAJOR_1_NAME,
                   FIELD_REQUESTED_MAJOR_1_COLLEGE, FIELD_ASSIGNED_MAJOR_NAME,
                   FIELD_PERMANENT_STATE, FIELD_FR_ADMISSIONS_RECOM,
                   FIELD_FR_ACADEMIC, FIELD_FRPQA, FIELD_CADR_ENG_DEF,
                   FIELD_CADR_MATH_DEF, FIELD_CADR_LABSCI_DEF,
                   FIELD_SOCIALSCI_DEF, FIELD_FORLANG_DEF, FIELD_MATH_LEVEL,
                   FIELD_REASON, FIELD_LAST_SCHOOL_CODE,
                   FIELD_LAST_SCHOOL_NAME, FIELD_HS_CODE, FIELD_HS_NAME,
                   FIELD_HS_CITY, FIELD_HS_STATE, FIELD_HS_FRL_PCT,
                   FIELD_ASSIGNED_COHORT, FIELD_ASSIGNED_MAJOR_CODE,
                   FIELD_HIGHEST_CONCORDED_SAT_MATH, FIELD_ADSEL_ID,
                   FIELD_EMPTY]

    document = models.TextField()
    comment = models.TextField()
    is_override = models.NullBooleanField(default=False)
    is_file_upload = models.NullBooleanField(default=True)
    upload_filename = models.CharField(max_length=100, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    imported_date = models.DateTimeField(null=True)
    imported_status = models.SmallIntegerField(null=True)
    imported_message = models.TextField(null=True)
    cohort = models.CharField(
        max_length=30, blank=True, validators=[validate_cohort])
    major = models.CharField(
        max_length=30, blank=True, validators=[validate_major])
    is_submitted = models.BooleanField(default=False)
    is_reassign = models.BooleanField(default=False)
    is_reassign_protected = models.BooleanField(default=False)

    objects = AssignmentImportManager()

    def json_data(self):
        assignments, errors = self.assignments()
        return {
            'id': self.pk,
            'comment': self.comment,
            'is_override': True if self.is_override else False,
            'is_file_upload': True if self.is_file_upload else False,
            'upload_filename': self.upload_filename,
            'created_date': self.created_date.isoformat() if (
                self.created_date is not None) else None,
            'created_by': self.created_by,
            'imported_date': self.imported_date.isoformat() if (
                self.imported_date is not None) else None,
            'imported_status': self.imported_status,
            'imported_message': self.imported_message,
            'assignments': [a.json_data() for a in assignments],
            'is_submitted': True if self.is_submitted else False,
            'is_reassign': True if self.is_reassign else False,
            'is_reassign_protected':
                True if self.is_reassign_protected else False,
            'errors': errors,
        }

    def assignments(self):
        assignments, errors = [], []
        for idx, row in enumerate(csv.DictReader(StringIO(self.document),
                                                 delimiter='\t')):
            assignment = Assignment(
                system_key=row.get(self.FIELD_SYSTEM_KEY),
                campus=0,
                quarter=0,
                application_number=row.get(self.FIELD_APPLICATION_NUMBER),
                admission_selection_id=row.get(self.FIELD_ADSEL_ID),
                cohort=self.cohort,
                major=self.major,
            )
            try:
                assignment.validate()
            except ValidationError as ex:
                errors.append({idx: ex})
            assignments.append(assignment)
        return assignments, errors

    def remove_assignments(self, ids_to_remove):
        new_csv = ""
        # Write headers back to file
        new_csv += get_headers(self.FIELD_NAMES)
        for idx, row in enumerate(csv.DictReader(StringIO(self.document),
                                                 delimiter='\t')):
            if row[self.FIELD_ADSEL_ID] not in ids_to_remove:
                flat_row = json.loads(json.dumps(row))
                new_csv += dict_to_csv(flat_row, self.FIELD_NAMES)

        self.document = new_csv
        self.save()


class Assignment(models.Model):
    CAMPUS_CHOICES = ((0, 'Seattle'), (1, 'Tacoma'), (2, 'Bothell'))

    system_key = models.CharField(
        max_length=30, validators=[validate_system_key])
    campus = models.PositiveSmallIntegerField(
        default=0, choices=CAMPUS_CHOICES)
    quarter = models.PositiveSmallIntegerField()
    application_number = models.PositiveIntegerField(
        validators=[validate_application_number])
    admission_selection_id = models.CharField(max_length=30)
    cohort = models.CharField(
        max_length=30, blank=True, validators=[validate_cohort])
    major = models.CharField(
        max_length=30, blank=True, validators=[validate_major])

    class Meta:
        managed = False

    def validate(self):
        self.full_clean()

    def csv_data(self):
        return to_csv([
            self.system_key, self.campus, self.quarter,
            self.application_number, self.admission_selection_id])

    def json_data(self):
        return {
            'system_key': self.system_key,
            'application_number': self.application_number,
            'admission_selection_id': self.admission_selection_id,
            'cohort': self.cohort,
            'major': self.major,
        }
