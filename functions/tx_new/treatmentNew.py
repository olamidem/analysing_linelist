import pandas as pd
from scipy.special import logsumexp


def monitoringDataframe(tbStatus):
    tbMonitoring = pd.DataFrame(tbStatus)
    tbMonitoring['VALUES'] = ["{0:n}".format(int(x)) for x in tbMonitoring['VALUES']]
    tbMonitoring['VALUES'] = ["{:,}".format(int(x)) for x in tbMonitoring['VALUES']]
    tbMonitoring = tbMonitoring.set_index('TB SCREENING').transpose()
    return tbMonitoring


def CurrentTbStatus(ipt_screening_query):
    Current_TB_Status = ipt_screening_query.query(
        'Current_TB_Status == "Disease suspected" | Current_TB_Status '
        '== "On treatment for disease" | Current_TB_Status == '
        ' "Disease diagnosed"')
    Current_TB_Status_count = Current_TB_Status['Current_TB_Status'].count()
    return Current_TB_Status_count


def documentedTb(ipt_screening_query):
    tbDocumented_result = tbDocumentedResults(ipt_screening_query)
    tbDocumented_result_count = tbDocumented_result['State'].count()
    return tbDocumented_result_count


def tbTable(Current_TB_Status_count, ipt_screening, tbDocumented_result_count):
    tbStatus = {
        'TB SCREENING': ['TOTAL SCREENED FOR TB', 'TB SUSPECTED', 'DOCUMENTED TB RESULTS'],
        'VALUES': [ipt_screening, Current_TB_Status_count, tbDocumented_result_count]
    }
    return tbStatus


def iptScreening(art_start):
    ipt_screening_query = art_start.query('IPT_Screening_Date != "" ')
    ipt_screening = ipt_screening_query['IPT_Screening_Date'].count()
    return ipt_screening, ipt_screening_query


def tranfer_IN(df, trans_in):
    transferIn = trans_in(df)
    transferIn_count = transferIn['TI'].count()
    return transferIn_count


def pbsCheck(art_start, art_start_count):
    pbs = art_start.query('PBS == "Yes" ')
    pbs_count = pbs['PBS'].count()
    pbsCoverage = ((logsumexp(pbs_count) / logsumexp(art_start_count)) * 100).round(1)
    return pbsCoverage, pbs_count


def cd4_counts(art_start, art_start_count):
    cd4_count = art_start.query('FirstCD4 != "" ')
    cd4_count_result = cd4_count['FirstCD4'].count()
    cd4CountCoverage = ((logsumexp(cd4_count_result) / logsumexp(art_start_count)) * 100).round(1)
    return cd4CountCoverage, cd4_count_result


def tbDocumentedResults(ipt_screening_query):
    return ipt_screening_query.query('Sputum_AFB_Result == "Positive" | '
                                     'Sputum_AFB_Result == "Negative" | '
                                     'GeneXpert_Result == "Smear negative pulmonary '
                                     'tuberculosis patient" | GeneXpert_Result == "MTB '
                                     'not Detected" | GeneXpert_Result == "MTB '
                                     'Detected" | Chest_Xray_Result == "Suggestive" | '
                                     'Chest_Xray_Result == "Not Suggestive" | '
                                     'Culture_Result == "Posive" | Culture_Result == '
                                     '"Negative" ')
