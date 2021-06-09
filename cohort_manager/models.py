# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models
from uw_adsel.models import Application, PurpleGoldApplication
from uw_adsel import AdSel
from io import StringIO
import csv
from restclients_core.exceptions import DataFailureException


class SyskeyAssignment(models.Model):
    CAMPUS_CHOICES = ((1, 'Seattle'), (2, 'Tacoma'), (3, 'Bothell'))

    assignment_import = models.ForeignKey('SyskeyImport',
                                          on_delete=models.PROTECT)
    system_key = models.PositiveIntegerField()
    application_number = models.PositiveIntegerField(null=True)
    admission_selection_id = models.PositiveIntegerField(null=True)
    assigned_cohort = models.IntegerField(null=True)
    assigned_major = models.CharField(max_length=30, null=True)
    major_program_code = models.TextField(null=True)
    campus = models.PositiveSmallIntegerField(
        default=1, choices=CAMPUS_CHOICES)
    application_not_found = models.BooleanField(default=False)

    @staticmethod
    def create_from_adsel_appliction(application, assignment_import):
        syskey_app = SyskeyAssignment()
        syskey_app.assignment_import = assignment_import
        syskey_app.system_key = application.system_key
        syskey_app.application_number = application.application_number
        syskey_app.admission_selection_id = application.adsel_id
        syskey_app.assigned_cohort = application.assigned_cohort
        syskey_app.assigned_major = application.assigned_major
        syskey_app.major_program_code = application.major_program_code
        syskey_app.campus = application.campus
        syskey_app.save()

    @staticmethod
    def create_missing(system_key, assignment_import):
        syskey_app = SyskeyAssignment()
        syskey_app.assignment_import = assignment_import
        syskey_app.system_key = system_key
        syskey_app.application_not_found = True
        syskey_app.save()

    @staticmethod
    def create_from_syskey_list(assignment_import, syskeys):
        applications = []
        adsel = AdSel()
        try:
            applications = \
                adsel.get_applications_by_qtr_syskey_list(
                    assignment_import.quarter,
                    syskeys
                )
        except DataFailureException as ex:
            pass
        found_syskeys = dict.fromkeys(syskeys, False)
        for app in applications:
            found_syskeys[app.system_key] = True
            SyskeyAssignment.create_from_adsel_appliction(app,
                                                          assignment_import)
        missing_syskeys = [key for key, value
                           in found_syskeys.items() if not value]
        for key in missing_syskeys:
            SyskeyAssignment.create_missing(key, assignment_import)

    def json_data(self):
        return {
            'system_key': self.system_key,
            'application_number': self.application_number,
            'admission_selection_id': self.admission_selection_id,
            'assigned_cohort': self.assigned_cohort,
            'assigned_major': self.assigned_major,
            'campus': self.get_campus_display(),
            "application_not_found": self.application_not_found
        }

    def get_application(self):
        app = Application()
        app.adsel_id = int(self.admission_selection_id)
        app.system_key = self.system_key
        app.application_number = self.application_number

        return app


class Import(models.Model):
    comment = models.TextField()
    campus = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    imported_date = models.DateTimeField(null=True)
    imported_status = models.SmallIntegerField(null=True)
    imported_message = models.TextField(null=True)
    quarter = models.IntegerField()
    upload_filename = models.CharField(max_length=100, null=True)
    is_submitted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def json_data(self):
        return {
            'id': self.pk,
            'comment': self.comment,
            'upload_filename': self.upload_filename,
            'created_date': self.created_date.isoformat() if (
                self.created_date is not None) else None,
            'created_by': self.created_by,
            'imported_date': self.imported_date.isoformat() if (
                self.imported_date is not None) else None,
            'imported_status': self.imported_status,
            'imported_message': self.imported_message,
            'is_submitted': True if self.is_submitted else False,
            'quarter': self.quarter
        }


class PurpleGoldImport(Import):
    @staticmethod
    def create_from_json(upload_body, user):
        pg_import = PurpleGoldImport()
        pg_import.comment = upload_body.get('comment', "")
        pg_import.quarter = upload_body.get('qtr_id')
        pg_import.upload_filename = upload_body.get('file_name')
        pg_import.created_by = user

        # Saving import before creating FK relationships
        pg_import.save()

        assignments = upload_body.get('assignments')
        PurpleGoldListAssignment.create_from_json(pg_import, assignments)

        return pg_import

    def json_data(self):
        assignments = self.purplegoldlistassignment_set.all()
        data = super().json_data()
        data['assignments'] = [a.json_data() for a in assignments]
        return data


class SyskeyImport(Import):
    is_override = models.NullBooleanField(default=False)
    cohort = models.IntegerField(blank=True, null=True)
    major = models.CharField(max_length=128, blank=True, null=True)
    decision = models.CharField(max_length=128, blank=True, null=True)
    is_reassign = models.BooleanField(default=False)
    is_reassign_protected = models.BooleanField(default=False)

    @staticmethod
    def create_from_json(upload_body, user):
        sys_import = SyskeyImport()
        sys_import.comment = upload_body.get('comment', "")
        sys_import.quarter = upload_body.get('qtr_id')
        sys_import.upload_filename = upload_body.get('file_name')
        sys_import.created_by = user

        cohort_id = upload_body.get('cohort_id')
        major_id = upload_body.get('major_id')
        decision_id = upload_body.get('decision_id')
        if cohort_id:
            sys_import.cohort = cohort_id
        if major_id:
            sys_import.major = major_id
        if decision_id:
            sys_import.decision = decision_id

        # Saving import before creating FK relationships
        sys_import.save()

        syskey_list = upload_body.get('syskey_list')
        SyskeyAssignment.create_from_syskey_list(sys_import, syskey_list)

        return sys_import

    def json_data(self):
        assignments = self.syskeyassignment_set.all()
        data = super().json_data()

        extra_data = {
            'cohort': self.cohort,
            'major': self.major,
            'decision': self.decision,
            'is_override': True if self.is_override else False,
            'is_reassign': True if self.is_reassign else False,
            'is_reassign_protected':
                True if self.is_reassign_protected else False,
            'assignments': [a.json_data() for a in assignments]
        }
        data.update(extra_data)
        return data

    def get_assignments(self):
        return self.syskeyassignment_set.all()

    def remove_assignments(self, ids_to_remove):
        assignments = self.get_assignments()
        assignments.filter(admission_selection_id__in=ids_to_remove).delete()


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
    FIELD_FRPQA = 'Frpqa'
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
    FIELD_ASSIGNED_MAJOR_CODE = 'AdSelAssignedMajorProgramCode'
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
    quarter = models.IntegerField()
    campus = models.CharField(max_length=30)
    cohort = models.CharField(max_length=30, blank=True, null=True)
    major = models.CharField(max_length=128, blank=True, null=True)
    is_submitted = models.BooleanField(default=False)
    is_reassign = models.BooleanField(default=False)
    is_reassign_protected = models.BooleanField(default=False)

    def json_data(self):
        assignments = self.assignment_set.all()
        if len(assignments) == 0:
            assignments = self.purplegoldassignment_set.all()
        return {
            'id': self.pk,
            'comment': self.comment,
            'cohort': self.cohort,
            'major': self.major,
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
            'quarter': self.quarter
        }

    def remove_assignments(self, ids_to_remove):
        assignments = self.assignment_set.all()
        if len(assignments) == 0:
            assignments = self.purplegoldassignment_set.all()
        assignments.filter(admission_selection_id__in=ids_to_remove).delete()

    def get_assignments(self):
        return self.assignment_set.all()


class Assignment(models.Model):
    CAMPUS_CHOICES = ((1, 'Seattle'), (2, 'Tacoma'), (3, 'Bothell'))

    assignment_import = models.ForeignKey(AssignmentImport,
                                          on_delete=models.PROTECT)
    system_key = models.CharField(max_length=30)
    application_number = models.PositiveIntegerField()
    admission_selection_id = models.CharField(max_length=30)
    assigned_cohort = models.IntegerField(null=True)
    assigned_major = models.CharField(max_length=30, null=True)
    campus = models.PositiveSmallIntegerField(
        default=1, choices=CAMPUS_CHOICES)
    sdb_app_status = models.IntegerField(null=True)

    def json_data(self):
        return {
            'system_key': self.system_key,
            'application_number': self.application_number,
            'admission_selection_id': self.admission_selection_id,
            'assigned_cohort': self.assigned_cohort,
            'assigned_major': self.assigned_major,
            'campus': self.get_campus_display(),
            'sdb_app_status': self.sdb_app_status
        }

    @staticmethod
    def create_from_applications(assign_import, applications):
        for application in applications:
            assign = Assignment()
            assign.assignment_import = assign_import
            assign.system_key = application.system_key
            assign.application_number = application.application_number
            assign.admission_selection_id = application.adsel_id
            assign.assigned_major = application.assigned_major
            assign.assigned_cohort = application.assigned_cohort
            assign.campus = application.campus
            assign.save()

    @staticmethod
    def create_from_file(assign_import):
        reader = csv.DictReader(StringIO(assign_import.document),
                                delimiter='\t')
        try:
            assignments = Assignment._create_from_reader(reader, assign_import)
        except ValueError:
            reader = csv.DictReader(StringIO(assign_import.document),
                                    delimiter=',')
            assignments = Assignment._create_from_reader(reader, assign_import)
        return assignments

    @staticmethod
    def _create_from_reader(reader, assign_import):
        assignments = []
        for idx, row in enumerate(reader):
            assignment = Assignment()
            assignment.assignment_import = assign_import
            assignment.system_key = \
                row.get(AssignmentImport.FIELD_SYSTEM_KEY)
            assignment.application_number = \
                row.get(AssignmentImport.FIELD_APPLICATION_NUMBER)
            assignment.admission_selection_id = \
                row.get(AssignmentImport.FIELD_ADSEL_ID)
            # Fix STFE-139
            try:
                assignment.sdb_app_status = \
                    int(row.get(AssignmentImport.FIELD_APPLICATION_STATUS))
            except (ValueError, TypeError):
                raise ValueError("Error with column %s" %
                                 AssignmentImport.FIELD_APPLICATION_STATUS)
            cohort_data = row.get(AssignmentImport.FIELD_ASSIGNED_COHORT)
            try:
                if len(cohort_data) > 0:
                    assignment.assigned_cohort = cohort_data
            except TypeError:
                raise ValueError("%s column not present" %
                                 AssignmentImport.FIELD_ASSIGNED_COHORT)
            major_data = row.get(
                AssignmentImport.FIELD_ASSIGNED_MAJOR_CODE)
            try:
                if len(major_data) > 0:
                    assignment.assigned_major = major_data
            except TypeError:
                raise ValueError("%s column not present" %
                                 AssignmentImport.FIELD_ASSIGNED_MAJOR_CODE)
            assignments.append(assignment)
        return assignments

    def get_application(self):
        app = Application()
        app.adsel_id = int(self.admission_selection_id)
        app.system_key = self.system_key
        app.application_number = self.application_number

        return app


class PurpleGoldListAssignment(models.Model):
    FIELD_PURPLEGOLD_NEW = "awardAmount"
    FIELD_ADSEL_ID = "admissionSelectionID"

    pg_import = models.ForeignKey(PurpleGoldImport,
                                  on_delete=models.PROTECT)
    admission_selection_id = models.CharField(max_length=30)
    purple_gold_new = models.FloatField(null=True)

    def json_data(self):
        return {
            'admission_selection_id': self.admission_selection_id,
            'purple_gold_new': self.purple_gold_new,
        }

    @staticmethod
    def create_from_json(pg_import, assignments):
        pg_assignments = []
        for assignment in assignments:
            assign_args = {
                'pg_import': pg_import,
                'admission_selection_id': assignment['admissionSelectionID'],
                'purple_gold_new': assignment['awardAmount']

            }
            pg_assign = PurpleGoldListAssignment(**assign_args)
            pg_assignments.append(pg_assign)
        PurpleGoldListAssignment.objects.bulk_create(pg_assignments)

    def get_application(self):
        app = PurpleGoldApplication()
        app.adsel_id = self.admission_selection_id
        app.award_amount = int(self.purple_gold_new)

        return app
