from dateutil.relativedelta import relativedelta
from datetime import timedelta
import pandas as pd


def suppressed_viral_load(vl_documented):
    vl_documented['CurrentViralLoad'] = vl_documented['CurrentViralLoad'].astype(float)
    suppressedVl = vl_documented.query(
        'CurrentViralLoad < 1000')
    return suppressedVl


def documented_viralload(dateConverter, df, report_date, viralLoadEligible):
    startDate = report_date
    endDate = startDate + timedelta(days=-364)  # type: ignore
    daysOnArt = viralLoadEligible(df)
    daysOnArt['DateofCurrentViralLoad'] = dateConverter(daysOnArt.DateofCurrentViralLoad)
    daysOnArt['DateofCurrentViralLoad'] = daysOnArt['DateofCurrentViralLoad']
    vl_documented = daysOnArt.query(
        ' DateofCurrentViralLoad <= @startDate & DateofCurrentViralLoad >= @endDate')
    return vl_documented


def vl_cascade_calc(documentedViralload, suppressedVl, suppressionRate, treatmentCurrent_count, vLEligibleCount,
                    vlAwaiting_Result_count, vlCoverage, vlSamplesNotYet, vlSentToLab):
    vlCascade = {
        'INDICATORS': ['TX Current', 'VL Eligible', 'VL sample taken and sent to PCR Lab',
                       'VL results received and entered into patients folders/EMR',
                       'VL Coverage (%)',
                       'VL eligible sample collected but awaiting results',
                       'VL eligible samples not yet taken.',
                       'VL Suppressed (Less than 1000 copies /ml)',
                       'VL Suppression (%)'],
        'VALUES': [treatmentCurrent_count, vLEligibleCount, vlSentToLab, documentedViralload,
                   vlCoverage, vlAwaiting_Result_count, vlSamplesNotYet, suppressedVl,
                   suppressionRate]
    }
    vlCascade = pd.DataFrame(vlCascade)
    vlCascade['VALUES'] = ["{0:n}".format(int(x)) for x in vlCascade['VALUES']]
    vlCascade['VALUES'] = ["{:,}".format(int(x)) for x in vlCascade['VALUES']]
    vlCascade = vlCascade.set_index('INDICATORS').transpose()
    return vlCascade


def sample_sent_awaiting(dateConverter, report_date, vLEligible):
    startDate = report_date + timedelta(days=-90)
    endDate = report_date
    vLEligible['LastDateOfSampleCollection'] = dateConverter(
        vLEligible['LastDateOfSampleCollection'])
    vLEligible['LastDateOfSampleCollection'] = vLEligible['LastDateOfSampleCollection'].dt.date
    vlAwaitingResult = vLEligible.query(
        'LastDateOfSampleCollection <= @endDate & LastDateOfSampleCollection >= @startDate ')
    vlAwaitingResult['DateofCurrentViralLoad'] = dateConverter(
        vlAwaitingResult['DateofCurrentViralLoad'])
    vlAwaitingResult['DateofCurrentViralLoad'] = vlAwaitingResult['DateofCurrentViralLoad'].dt.date
    pickDate = report_date + timedelta(days=-365)
    vlAwaiting_Result = vlAwaitingResult.query('DateofCurrentViralLoad <= @pickDate')
    return vlAwaiting_Result


def viral_load_eligible_calc(dateConverter, report_date, vl_data):
    vl_data['Ref_Date'] = report_date
    vl_data['ARTStartDate'] = dateConverter(vl_data['ARTStartDate'])
    vl_data['ARTStartDate'] = vl_data['ARTStartDate']
    vl_data['DaysOnart'] = (
            vl_data['Ref_Date'] - vl_data['ARTStartDate']).dt.days

    def viralLoadEligible(dataSet):
        return dataSet.query(
            ' DaysOnart >= 180  & CurrentARTStatus_Pharmacy == "Active" & Outcomes == "" ')

    return viralLoadEligible
