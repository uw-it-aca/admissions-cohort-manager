from django.db import models
from django.core.exceptions import ValidationError
from io import StringIO
import csv


class AssignmentImportManager(models.Manager):
    pass


class AssignmentImport(models.Model):
    status_code = models.CharField(max_length=3, null=True)
    document = models.TextField()
    imported_date = models.DateTimeField(auto_now_add=True)
    imported_by = models.CharField(max_length=30)
    assignment_errors = []

    objects = AssignmentImportManager()

    def validate(self):
        self.assignment_errors = []
        for idx, assignment in enumerate(self._parse(), start=1):
            try:
                assignment.validate()
            except ValidationError as ex:
                self.assignment_errors.append({idx: ex})

    def save(self, *args, **kwargs):
        self.full_clean()
        ret = super(AssignmentImport, self).save(*args, **kwargs)
        for assignment in self._parse():
            assignment.save()

    def _parse(self):
        assignments = []
        for row in csv.DictReader(StringIO(self.document)):
            assignments.append(Assignment(
                system_key=row.get('system_key'),
                campus=row.get('campus'),
                year=row.get('app_year'),
                quarter=row.get('app_quarter'),
                application_number=row.get('app_number'),
                admission_selection_id=row.get('AdmissionSelectionID'),
                assignment_import=self))
        return assignments


class AssignmentManager(models.Manager):
    pass


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
    assignment_import = models.ForeignKey(
        AssignmentImport, on_delete=models.CASCADE, blank=True)

    objects = AssignmentManager()

    def validate(self):
        self.full_clean()

    def save(self, *args, **kwargs):
        self.validate()
        return super(Assignment, self).save(*args, **kwargs)
