from django.db import models
from django.core.exceptions import ValidationError
from cohort_manager.utils import to_csv
from io import StringIO
import csv


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


class AssignmentImport(models.Model):
    FIELD_SYSTEM_KEY = 'system_key'
    FIELD_CAMPUS = 'campus'
    FIELD_YEAR = 'app_year'
    FIELD_QUARTER = 'app_quarter'
    FIELD_APPLICATION_NUMBER = 'app_number'
    FIELD_SELECTION_ID = 'AdmissionSelectionID'
    FIELD_NAMES = [FIELD_SYSTEM_KEY, FIELD_CAMPUS, FIELD_YEAR, FIELD_QUARTER,
                   FIELD_APPLICATION_NUMBER, FIELD_SELECTION_ID]

    document = models.TextField()
    comment = models.TextField()
    is_file_upload = models.NullBooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    imported_date = models.DateTimeField(null=True)
    imported_status = models.SmallIntegerField(null=True)
    imported_message = models.TextField(null=True)
    cohort = models.CharField(
        max_length=30, blank=True, validators=[validate_cohort])
    major = models.CharField(
        max_length=30, blank=True, validators=[validate_major])

    def json_data(self):
        assignments, errors = self.assignments()
        return {
            'id': self.pk,
            'comment': self.comment,
            'is_file_upload': True if self.is_file_upload else False,
            'created_date': self.created_date.isoformat(),
            'created_by': self.created_by,
            'imported_date': self.imported_date.isoformat() if (
                self.imported_date is not None) else None,
            'imported_status': self.imported_status,
            'imported_message': self.imported_message,
            'assignments': [a.json_data() for a in assignments],
            'errors': errors,
        }

    def assignments(self):
        assignments, errors = [], []
        for idx, row in enumerate(csv.DictReader(StringIO(self.document))):
            assignment = Assignment(
                system_key=row.get(self.FIELD_SYSTEM_KEY),
                campus=row.get(self.FIELD_CAMPUS),
                year=row.get(self.FIELD_YEAR),
                quarter=row.get(self.FIELD_QUARTER),
                application_number=row.get(self.FIELD_APPLICATION_NUMBER),
                admission_selection_id=row.get(self.FIELD_SELECTION_ID),
                cohort=self.cohort,
                major=self.major,
            )
            try:
                assignment.validate()
            except ValidationError as ex:
                errors.append({idx: ex})
            assignments.append(assignment)
        return assignments, errors


class Assignment(models.Model):
    CAMPUS_CHOICES = ((0, 'Seattle'), (1, 'Tacoma'), (2, 'Bothell'))
    QTR_CHOICES = ((1, 'Winter'), (2, 'Spring'), (3, 'Summer'), (4, 'Autumn'))

    system_key = models.CharField(
        max_length=30, validators=[validate_system_key])
    campus = models.PositiveSmallIntegerField(
        default=0, choices=CAMPUS_CHOICES)
    year = models.PositiveSmallIntegerField(validators=[validate_year])
    quarter = models.PositiveSmallIntegerField(default=4, choices=QTR_CHOICES)
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
            self.system_key, self.campus, self.year, self.quarter,
            self.application_number, self.admission_selection_id])

    def json_data(self):
        return {
            'system_key': self.system_key,
            'campus': self.campus,
            'year': self.year,
            'quarter': self.quarter,
            'application_number': self.application_number,
            'admission_selection_id': self.admission_selection_id,
            'cohort': self.cohort,
            'major': self.major,
        }
