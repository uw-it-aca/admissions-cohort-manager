from django.test import TestCase
from cohort_manager.models import AssignmentImport


class AssignmentImportTest(TestCase):
    csv_data = '''system_key,campus,app_year,app_quarter,app_number,AdmissionSelectionID,student_name,Last_School,Home_Addr_County,Ethnicity,Major_Assign1,Major_Assign2,Academics,AppStatus,FR_Year,HS_AdjustedGPA,HS_GPA,Number of Records,PersonalQuality,appl_status,appl_status_rsn
2101612,0,2019,4,1,123,a,CENTRAL H S,x,Caucasian,ENGL,,16,16,"2,019",0,4,1,15,16,0
2131178,0,2019,4,1,124,b,LAKE SR H S,y,Hispanic/Latino,BIOL,,16,14,"2,019",0,4,1,15,14,0
2139472,0,2019,4,1,125,c,MOUNTAIN SENIOR H S,z,Asian,B A,,16,16,"2,019",0,4,1,15,16,0'''

    def test_parse(self):
        imp = AssignmentImport(
            status_code='200', document=self.csv_data, imported_by='j')
        imp.validate()
