from django.db import models
from django.core.exceptions import ValidationError
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


class AssignmentImportManager(models.Manager):
    pass


class AssignmentImport(models.Model):
    status_code = models.CharField(max_length=3, null=True)
    document = models.TextField()
    imported_date = models.DateTimeField(auto_now_add=True)
    imported_by = models.CharField(max_length=30)
    cohort = models.CharField(
        max_length=30, blank=True, validators=[validate_cohort])
    major = models.CharField(
        max_length=30, blank=True, validators=[validate_major])

    objects = AssignmentImportManager()

    def json_data(self):
        return {
            'id': self.pk,
            'status_code': self.status_code,
            'imported_date': self.imported_date.isoformat(),
            'imported_by': self.imported_by,
            'assignment_errors': self.assignment_errors,
            'assignments': [a.json_data() for a in self.assignments]
        }

    @property
    def assignments(self):
        assignments, errors = [], []
        for idx, row in enumerate(csv.DictReader(StringIO(self.document))):
            assignment = Assignment(
                system_key=row.get('system_key'),
                campus=row.get('campus'),
                year=row.get('app_year'),
                quarter=row.get('app_quarter'),
                application_number=row.get('app_number'),
                admission_selection_id=row.get('AdmissionSelectionID'),
                cohort=self.cohort,
                major=self.major,
            )
            try:
                assignment.validate()
                assignments.append(assignment)
            except ValidationError as ex:
                errors.append({idx: ex})
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
