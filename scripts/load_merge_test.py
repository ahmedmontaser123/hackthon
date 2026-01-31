import pandas as pd
from pathlib import Path

if __name__ == "__main__":

    PATH = Path(__file__).parent.parent

    students_assessments = pd.read_csv(f'{PATH}/data/anonymiseddata/studentAssessment.csv')
    student_info = pd.read_csv(f'{PATH}/data/anonymiseddata/studentInfo.csv')
    courses = pd.read_csv(f'{PATH}/data/anonymiseddata/courses.csv')
    assessments = pd.read_csv(f'{PATH}/data/anonymiseddata/assessments.csv')
    student_registration = pd.read_csv(f'{PATH}/data/anonymiseddata/studentRegistration.csv')
    vle = pd.read_csv(f'{PATH}/data/anonymiseddata/vle.csv')
    studentsVle = pd.read_csv(f'{PATH}/data/anonymiseddata/studentVle.csv')


    base = student_info.merge(student_registration, how='left', on=["id_student", "code_module", "code_presentation"])

    assessments_full = students_assessments.merge(assessments, how='left', on="id_assessment")

    assessments_agg = assessments_full.groupby(["id_student","code_module","code_presentation"]).agg(avg_score = ("score","mean"),max_score = ("score","max"),num_submissions = ("score","count"),score_min = ("score","min"))


    base = base.merge(assessments_agg, how='left', on=["id_student","code_module","code_presentation"])


    vle_merged = studentsVle.merge(vle.drop(["code_module","code_presentation"],axis = 1), how='left', on=["id_site"])
    print(vle_merged.head())
    vle_agg = vle_merged.groupby(["id_student", "code_module", "code_presentation"]).agg(total_clicks=("sum_click", "sum"),activity_diversity=("activity_type", "nunique")).reset_index()

    final_df = base.merge(vle_agg, how='left', on=["id_student", "code_module", "code_presentation"])
    final_df.reset_index().to_csv(f'{PATH}/data/anonymiseddata/final_vle_test.csv', index=False)

    
