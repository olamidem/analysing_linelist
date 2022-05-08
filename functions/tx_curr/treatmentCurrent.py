import pandas as pd

def tx_curr(dataSet):
    active = dataSet.query(
        'CurrentARTStatus_Pharmacy == "Active" & Outcomes == ""  & ARTStartDate != ""  ')
    return active


def paedTxCurr(treatmentCurrent):
    paed = treatmentCurrent.query('Current_Age <10 ')
    countPaed = paed['Current_Age'].count()
    return countPaed


def adolescentTxCurr(treatmentCurrent):
    adolescent = treatmentCurrent.query('Current_Age >=10 & Current_Age <= 19 ')
    countAdolescent = adolescent['Current_Age'].count()
    return countAdolescent


def adultTxCurr(treatmentCurrent):
    adult = treatmentCurrent.query('Current_Age >= 20 ')
    countAdult = adult['Current_Age'].count()
    return countAdult


def femaleTxCurr(treatmentCurrent):
    tx_curr_female = treatmentCurrent.query('Sex == "F" ')
    countFemale = tx_curr_female['Sex'].count()
    return countFemale


def maleTxCurr(treatmentCurrent):
    tx_curr_male = treatmentCurrent.query('Sex == "M" ')
    countMale = tx_curr_male['Sex'].count()
    return countMale


def txCurr(treatmentCurrent):
    treatmentCurrent_count = treatmentCurrent['CurrentARTStatus_Pharmacy'].count()
    return treatmentCurrent_count

def tx_ml(df):
    txML = df.query('ARTStatus_PreviousQuarter == "Active" & CurrentARTStatus_Pharmacy != "Active"  ')
    txML_count = txML['ARTStatus_PreviousQuarter'].count()
    return txML_count


def returnToCare(treatmentCurrent):
    rtt = treatmentCurrent.query('ARTStatus_PreviousQuarter != "Active" & CurrentARTStatus_Pharmacy == "Active"  ')
    rtt_count = rtt['ARTStatus_PreviousQuarter'].count()
    return rtt_count

def txCurrReportFormat(tx_curr_report_table):
    tx_curr_dataFrame = pd.DataFrame(tx_curr_report_table)
    tx_curr_dataFrame['VALUES'] = ["{0:n}".format(int(x)) for x in tx_curr_dataFrame['VALUES']]
    tx_curr_dataFrame['VALUES'] = ["{:,}".format(int(x)) for x in tx_curr_dataFrame['VALUES']]
    tx_curr_dataFrame = tx_curr_dataFrame.set_index('INDICATORS').transpose()
    return tx_curr_dataFrame


def txReportDataframe( pbs_count, pbsCoverage,ipt_screening,Current_TB_Status_count,
                      tbDocumented_result_count,rtt_count, txML_count):
    tx_curr_report_table = {
        'INDICATORS': ['TOTAL PBS CAPTURED', 'PBS COVERAGE (%)', 'TOTAL SCREENED FOR TB', 'TB SUSPECT',
                       'DOCUMENTED TB RESULT', 'RTT', 'TX_ML'],
        'VALUES': [pbs_count, pbsCoverage, ipt_screening,
                   Current_TB_Status_count, tbDocumented_result_count, rtt_count, txML_count]
                               # 'INH PICKED', 'INH COMPLETED', 'POTENTIAL IIT'
    }
    return tx_curr_report_table
