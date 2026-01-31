from typing import final

import pandas as pd
from pathlib import Path

PATH = Path(__file__).parent.parent

assessments = pd.read_csv(f'{PATH}/data/assessments.csv')
studentAssessment = pd.read_csv(f'{PATH}/data/studentAssessment.csv')
vle = pd.read_csv(f'{PATH}/data/vle.csv')
studentsVle = pd.read_csv(f'{PATH}/data/studentVle.csv')
studentInfo = pd.read_csv(f'{PATH}/data/studentInfo.csv')
studentRegistration = pd.read_csv(f'{PATH}/data/studentRegistration.csv')

base = studentInfo.merge(studentRegistration, how='left', on=["id_student", "code_module", "code_presentation"])

assessments = studentAssessment.merge(assessments, how='left', on='id_assessment')
assessments['score'] = (assessments['score']/100) * assessments['weight']

scores = assessments.groupby(['code_module','code_presentation','id_student'])['score'].sum().reset_index()


final_df = base.merge(scores, how='left', on=['id_student', 'code_module', 'code_presentation'])

merged = final_df.copy()

vle_merged = studentsVle.merge(vle, how='left', on=["id_site", "code_module", "code_presentation"])
print(vle_merged.head())
vle_agg = vle_merged.groupby(["id_student", "code_module", "code_presentation"]).agg(total_clicks=("sum_click", "sum"),activity_diversity=( "activity_type","nunique")).reset_index()

final_df = merged.merge(vle_agg, how="left", on=["id_student", "code_module", "code_presentation"])
#final_df = final_df.groupby(['code_module','code_presentation','id_student']).agg(final_score = ("score","sum"),is_banked = ("is_banked","max"))
#final_df.to_csv(f'{PATH}/data/data_assessment.csv', index=True)

final_df = final_df[final_df['final_result'] != "Withdrawn"]

#final_df = final_df.drop(["final_result"],axis=1)


final_df.to_csv(f'{PATH}/data/regression_df.csv', index=False)

print(final_df.head())
