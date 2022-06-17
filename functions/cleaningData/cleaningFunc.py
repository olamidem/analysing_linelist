import numpy as np


def cleanDataSet(df):
    df.replace(to_replace='\\\\N', value='')
    df['Outcomes'] = df['Outcomes'].replace(to_replace=np.nan, value="")
    df['PhoneNo'] = df['PhoneNo'].replace(to_replace=['null', 'NONE', 'NIL', 'NIL.'], value="")
    df['ARTStartDate'] = df['ARTStartDate'].replace(to_replace=np.nan, value="01/01/1900")
    df['DateofCurrentViralLoad'] = df['DateofCurrentViralLoad'].replace(to_replace=np.nan, value="01/01/1900")
    df['LastDateOfSampleCollection'] = df['LastDateOfSampleCollection'].replace(to_replace=np.nan,
                                                                                value="01/01/1900")
    df['Current_Age'] = df['Current_Age'].replace(to_replace=np.nan, value=0)
    df['DaysOfARVRefill'] = df['DaysOfARVRefill'].replace(to_replace=np.nan, value=0)
    df['Current_TB_Status'] = df['Current_TB_Status'].replace(to_replace=np.nan, value="")
    df['IPT_Screening_Date'] = df['IPT_Screening_Date'].replace(to_replace=np.nan, value="")
    df['PhoneNo'] = df['PhoneNo'].astype(str)
