from datetime import timedelta, date, datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
from streamlit_option_menu import option_menu
from functions.age_grouping.age_grouping import *
from functions.bar_chart.bar_chart import *
from functions.cleaningData.cleaningFunc import *
from functions.download.downloadFun import *
from functions.pie_chart.pieChart import *
from functions.tx_curr.treatmentCurrent import *
from functions.tx_curr.tx_curr_card import *
from functions.tx_new.treatmentNew import *
from functions.tx_new.tx_new_display import *
from functions.viral_load.viral_load_calc import *
from functions.viral_load.viral_load_card import *

st.set_page_config(page_title="Report Dashboard 💻", page_icon="📑", layout="wide",
                   initial_sidebar_state="auto", )

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def main(low_memory=False):
    def condition(age):
        if 5 <= age <= 9:
            return "5 - 9"
        elif 10 <= age <= 14:
            return "10 - 14"
        elif 15 <= age <= 19:
            return "15 - 19"
        elif 20 <= age <= 24:
            return "20 - 24"
        elif 25 <= age <= 29:
            return "25 - 29"
        elif 30 <= age <= 34:
            return "30 - 34"
        elif 35 <= age <= 39:
            return "35 - 39"
        elif 40 <= age <= 44:
            return "40 - 44"
        elif 45 <= age <= 49:
            return "45 - 49"
        elif age >= 50:
            return "50+"
        else:
            female['Current_Age'].isnull()
            return "1 - 4"

    # ###########OUTPUT FUNCTION###############################
    def output():
        colm, colf, colp = st.columns(3)
        with colm:
            st.success("MALE")
            st.write(m.value_counts())

        with colf:
            st.warning("FEMALE")
            st.write(f.value_counts())

        with colp:
            st.info("PREGNANT/B FEEDING")
            st.write(p.value_counts())  # type: ignore

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

    def artStart(dataSet):
        return dataSet[(dataSet['ARTStartDate'] >= str(start_date)) &  # type: ignore
                       (dataSet['ARTStartDate'] <= str(end_date)) &  # type: ignore
                       (dataSet['TI'] != 'Yes')]  # type: ignore

    def trans_in(dataset):
        return dataset[(dataset['ARTStartDate'] >= str(start_date)) &  # type: ignore
                       (dataset['ARTStartDate'] <= str(end_date)) &  # type: ignore
                       (dataset['TI'] == 'Yes')]  # type: ignore

    def pharm():
        pharm_start = vl_data[(vl_data['Pharmacy_LastPickupdate'] >= str(start_date)) &  # type: ignore
                              (vl_data['Pharmacy_LastPickupdate'] <= str(end_date))]  # type: ignore
        return pharm_start

    # def outComes():
    #     outcomes_date = df[(df['Outcomes_Date'] >= str(start_date)) &  # type: ignore
    #                        (df['Outcomes_Date'] <= str(end_date))]  # type: ignore
    #     outcomes_date = outcomes_date['Outcomes_Date'].count()
    #     return outcomes_date

    def dateConverter(dateColumn):
        return pd.to_datetime(dateColumn, format="%d/%m/%Y", errors='ignore')

    ######################### DATE FUNCTION###############################
    def firstDate():
        firstDate.start_date = st.date_input("From", )

    def SecondDate():
        SecondDate.end_date = st.date_input("To", )

    # def fileName(name):
    #     fileName = data.name
    #     st.header(fileName)

    def convert_df(filename):
        return filename.to_csv().encode('utf-8')

    def selectLga(lgas, state):
        select_lgas = st.multiselect(
            'Select LGAs', lgas, key='lgas'
        )
        lgas = state.query('LGA == @select_lgas')
        lga = lgas
        facilities = lgas['FacilityName'].unique()
        return facilities, lga, select_lgas

    def selectState(df, states):
        select_state = st.multiselect(
            'Select States', states, key='states'
        )
        state = df.query('State == @select_state')
        lgas = state['LGA'].unique()
        return lgas, select_state, state

    activities = select_activities()
    reports = ['', 'HI Weekly Report',
               'M&E Weekly Report', 'M&E Monthly Report']

    with st.sidebar:
        # st.image('cpu.png',width = 200,)
        st.markdown('<p class="side-icon">💻</p>',
                    unsafe_allow_html=True)

    selected = option_menu(
        menu_title=None,
        options=['Monitoring', 'Reports', 'Download', 'EMR-NDR', 'Feedback'],
        icons=['pie-chart-fill', 'book', 'cloud-arrow-down', 'list-task', 'chat-square-text-fill'],
        orientation='horizontal',
        menu_icon='cast',
        default_index=0,
        styles={
            # "container": {"background-color": "#fff"},
            # "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {"--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#176c36"},
        }
    )
    with st.sidebar:
        st.markdown('<div class="sidebar">📝Dashboard</div>',
                    unsafe_allow_html=True)

    if selected == 'Monitoring':

        st.markdown('<p class="font">Monitoring Dashboard💻</p>',
                    unsafe_allow_html=True)
        # ############MONITORING MODULES#######################################

        monitoring = st.container()
        with monitoring:
            all_card = st.empty()
            # ###################### TREATMENT NEW CONTAINER###################
            txnewContainer = st.empty()
            placeholder = st.empty()

        data = placeholder.file_uploader(
            'Upload your Treatment Linelist here. Pls ART Linelist Only 🙏🙏🙏🙏', type=['csv'])
        st.session_state.data = data
        if data is not None:
            if data not in st.session_state:
                st.session_state.data = data
                placeholder.empty()

            # fileName(data)

            @st.cache(allow_output_mutation=True)
            def load_data1():
                df = pd.read_csv(st.session_state.data, encoding='unicode_escape', on_bad_lines='skip',
                                 low_memory=False)
                dob = dateConverter(df['DOB'])
                dob = dob.dt.date
                saveDate = date.today()
                df['today_date'] = saveDate
                df['New_Age'] = (saveDate - dob) / 365
                df['New_Age'] = df['New_Age'].dt.days
                return df

            df = load_data1()
            # columns = ['ARTStartDate']
            # columns2 = [df.columns[14]]
            # if [columns] == [columns2]:
            cleanDataSet(df)
            st.markdown('<br>', unsafe_allow_html=True)
            with st.sidebar:
                st.markdown('<br>', unsafe_allow_html=True)
                choice = st.selectbox('Select Indicator', activities)
                st.markdown('<br>', unsafe_allow_html=True)

            if choice == 'Treatment Current':
                if choice is not None:

                    st.markdown('<br>',
                                unsafe_allow_html=True)
                    st.markdown('<p class="tb">TX_CURR REPORT </p>',
                                unsafe_allow_html=True)

                    txCurrPlaceholder = st.empty()
                    placeholder.empty()
                    treatmentCurrent = tx_curr(df)
                    treatmentCurrent_count = txCurr(treatmentCurrent)
                    countMale = maleTxCurr(treatmentCurrent)
                    countFemale = femaleTxCurr(treatmentCurrent)
                    countAdult = adultTxCurr(treatmentCurrent)
                    countAdolescent = adolescentTxCurr(treatmentCurrent)
                    countPaed = paedTxCurr(treatmentCurrent)
                    pbsCoverage, pbs_count = pbsCheck(treatmentCurrent, treatmentCurrent_count)
                    rtt_count = returnToCare(treatmentCurrent)
                    txML_count = tx_ml(df)
                    ipt_screening, ipt_screening_query = iptScreening(treatmentCurrent)
                    tbDocumented_result_count = documentedTb(ipt_screening_query)
                    Current_TB_Status_count = CurrentTbStatus(ipt_screening_query)
                    tx_curr_report_table = txReportDataframe(pbs_count, pbsCoverage,
                                                             ipt_screening, Current_TB_Status_count,
                                                             tbDocumented_result_count, rtt_count, txML_count)

                    tx_curr_dataFrame = txCurrReportFormat(tx_curr_report_table)

                    txcurr_data = tx_curr(df)

                    states = txcurr_data['State'].unique()

                    with st.sidebar:
                        st.markdown('<br>', unsafe_allow_html=True)
                        lgas, select_state, state = selectState(txcurr_data, states)

                        st.markdown('<br>', unsafe_allow_html=True)
                        facilities, lga, select_lgas = selectLga(lgas, state)

                        st.markdown('<br>', unsafe_allow_html=True)
                        select_facilities = st.multiselect(
                            'Select Facilities', facilities, key='facilities'
                        )
                        facilities = state.query('FacilityName == @select_facilities')

                    with all_card:
                        displayCard(countAdolescent, countAdult, countFemale, countMale, countPaed,
                                    treatmentCurrent_count)

                    with txCurrPlaceholder:
                        st.table(tx_curr_dataFrame)

                    barChartDisplay = st.empty()
                    with barChartDisplay:
                        age_group = txcurr_data.query('Sex == "M" ')
                        fiftyplus, lessthanforty_four, lessthanforty_nine, lessthanfour, lessthanfourteen, \
                        lessthannineteen, lessthanone, lessthanten, lessthanthirty_four, lessthanthirty_nine, \
                        lessthantwenty_four, lessthantwenty_nine = age_grouping(
                            age_group)

                        male = [lessthanone, lessthanfour, lessthanten, lessthanfourteen,
                                lessthannineteen, lessthantwenty_four, lessthantwenty_nine,
                                lessthanthirty_four, lessthanthirty_nine, lessthanforty_four,
                                lessthanforty_nine, fiftyplus]

                        age_group_female = txcurr_data.query('Sex == "F" ')
                        fiftyplus, lessthanforty_four, lessthanforty_nine, lessthanfour, lessthanfourteen, \
                        lessthannineteen, lessthanone, lessthanten, lessthanthirty_four, lessthanthirty_nine, \
                        lessthantwenty_four, lessthantwenty_nine = age_grouping(
                            age_group_female)

                        female = [lessthanone, lessthanfour, lessthanten, lessthanfourteen,
                                  lessthannineteen, lessthantwenty_four, lessthantwenty_nine,
                                  lessthanthirty_four, lessthanthirty_nine, lessthanforty_four, lessthanforty_nine,
                                  fiftyplus]

                        female = [int(i) for i in female]
                        male = [int(i) for i in male]

                        bar_chart_display(female, male)

                    if select_state:
                        all_card.empty()
                        txCurrPlaceholder.empty()
                        barChartDisplay.empty()
                        treatmentCurrent = tx_curr(state)
                        treatmentCurrent_count = txCurr(treatmentCurrent)
                        countMale = maleTxCurr(treatmentCurrent)
                        countFemale = femaleTxCurr(treatmentCurrent)
                        countAdult = adultTxCurr(treatmentCurrent)
                        countAdolescent = adolescentTxCurr(treatmentCurrent)
                        countPaed = paedTxCurr(treatmentCurrent)
                        pbsCoverage, pbs_count = pbsCheck(treatmentCurrent, treatmentCurrent_count)
                        rtt_count = returnToCare(treatmentCurrent)
                        txMlSelect = df.query('State == @select_state')
                        txMlCheck = txMlSelect.query(
                            'ARTStatus_PreviousQuarter == "Active" & CurrentARTStatus_Pharmacy != "Active"  ')
                        txML_count = txMlCheck['ARTStatus_PreviousQuarter'].count()
                        ipt_screening, ipt_screening_query = iptScreening(treatmentCurrent)
                        tbDocumented_result_count = documentedTb(ipt_screening_query)
                        Current_TB_Status_count = CurrentTbStatus(ipt_screening_query)
                        tx_curr_report_table = txReportDataframe(pbs_count, pbsCoverage,
                                                                 ipt_screening, Current_TB_Status_count,
                                                                 tbDocumented_result_count, rtt_count, txML_count)
                        tx_curr_dataFrame = txCurrReportFormat(tx_curr_report_table)

                        with txCurrPlaceholder:
                            st.table(tx_curr_dataFrame)

                        with all_card:
                            displayCard(countAdolescent, countAdult, countFemale, countMale, countPaed,
                                        treatmentCurrent_count)

                        with barChartDisplay:
                            age_group = treatmentCurrent.query('Sex == "M" ')
                            fiftyplus, lessthanforty_four, lessthanforty_nine, lessthanfour, lessthanfourteen, \
                            lessthannineteen, lessthanone, lessthanten, lessthanthirty_four, lessthanthirty_nine, \
                            lessthantwenty_four, lessthantwenty_nine = age_grouping(
                                age_group)

                            male = [lessthanone, lessthanfour, lessthanten, lessthanfourteen,
                                    lessthannineteen, lessthantwenty_four, lessthantwenty_nine,
                                    lessthanthirty_four, lessthanthirty_nine, lessthanforty_four,
                                    lessthanforty_nine, fiftyplus]

                            age_group_female = treatmentCurrent.query('Sex == "F" ')
                            fiftyplus, lessthanforty_four, lessthanforty_nine, lessthanfour, lessthanfourteen, \
                            lessthannineteen, lessthanone, lessthanten, lessthanthirty_four, lessthanthirty_nine, \
                            lessthantwenty_four, lessthantwenty_nine = age_grouping(
                                age_group_female)

                            female = [lessthanone, lessthanfour, lessthanten, lessthanfourteen,
                                      lessthannineteen, lessthantwenty_four, lessthantwenty_nine,
                                      lessthanthirty_four, lessthanthirty_nine, lessthanforty_four,
                                      lessthanforty_nine,
                                      fiftyplus]

                            female = [int(i) for i in female]
                            male = [int(i) for i in male]

                            bar_chart_display(female, male)

                    if select_lgas:
                        all_card.empty()
                        txCurrPlaceholder.empty()
                        barChartDisplay.empty()
                        treatmentCurrent = tx_curr(lga)
                        treatmentCurrent_count = txCurr(treatmentCurrent)
                        countMale = maleTxCurr(treatmentCurrent)
                        countFemale = femaleTxCurr(treatmentCurrent)
                        countAdult = adultTxCurr(treatmentCurrent)
                        countAdolescent = adolescentTxCurr(treatmentCurrent)
                        countPaed = paedTxCurr(treatmentCurrent)
                        pbsCoverage, pbs_count = pbsCheck(treatmentCurrent, treatmentCurrent_count)
                        rtt_count = returnToCare(treatmentCurrent)
                        txMlSelect = df.query('LGA == @select_lgas')
                        txMlCheck = txMlSelect.query(
                            'ARTStatus_PreviousQuarter == "Active" & CurrentARTStatus_Pharmacy != "Active"  ')
                        txML_count = txMlCheck['ARTStatus_PreviousQuarter'].count()

                        ipt_screening, ipt_screening_query = iptScreening(treatmentCurrent)
                        tbDocumented_result_count = documentedTb(ipt_screening_query)
                        Current_TB_Status_count = CurrentTbStatus(ipt_screening_query)
                        tx_curr_report_table = txReportDataframe(pbs_count, pbsCoverage,
                                                                 ipt_screening, Current_TB_Status_count,
                                                                 tbDocumented_result_count, rtt_count, txML_count)
                        tx_curr_dataFrame = txCurrReportFormat(tx_curr_report_table)

                        with all_card:
                            displayCard(countAdolescent, countAdult, countFemale, countMale, countPaed,
                                        treatmentCurrent_count)

                        with txCurrPlaceholder:
                            st.table(tx_curr_dataFrame)

                        with barChartDisplay:
                            age_group = treatmentCurrent.query('Sex == "M" ')
                            fiftyplus, lessthanforty_four, lessthanforty_nine, lessthanfour, lessthanfourteen, \
                            lessthannineteen, lessthanone, lessthanten, lessthanthirty_four, lessthanthirty_nine, \
                            lessthantwenty_four, lessthantwenty_nine = age_grouping(
                                age_group)

                            male = [lessthanone, lessthanfour, lessthanten, lessthanfourteen,
                                    lessthannineteen, lessthantwenty_four, lessthantwenty_nine,
                                    lessthanthirty_four, lessthanthirty_nine, lessthanforty_four,
                                    lessthanforty_nine, fiftyplus]

                            age_group_female = treatmentCurrent.query('Sex == "F" ')
                            fiftyplus, lessthanforty_four, lessthanforty_nine, lessthanfour, lessthanfourteen, \
                            lessthannineteen, lessthanone, lessthanten, lessthanthirty_four, lessthanthirty_nine, \
                            lessthantwenty_four, lessthantwenty_nine = age_grouping(
                                age_group_female)

                            female = [lessthanone, lessthanfour, lessthanten, lessthanfourteen,
                                      lessthannineteen, lessthantwenty_four, lessthantwenty_nine,
                                      lessthanthirty_four, lessthanthirty_nine, lessthanforty_four,
                                      lessthanforty_nine,
                                      fiftyplus]

                            female = [int(i) for i in female]
                            male = [int(i) for i in male]

                            bar_chart_display(female, male)

                    if select_facilities:
                        all_card.empty()
                        txCurrPlaceholder.empty()
                        treatmentCurrent = tx_curr(facilities)
                        treatmentCurrent_count = txCurr(treatmentCurrent)
                        countMale = maleTxCurr(treatmentCurrent)
                        countFemale = femaleTxCurr(treatmentCurrent)
                        countAdult = adultTxCurr(treatmentCurrent)
                        countAdolescent = adolescentTxCurr(treatmentCurrent)
                        countPaed = paedTxCurr(treatmentCurrent)
                        pbsCoverage, pbs_count = pbsCheck(treatmentCurrent, treatmentCurrent_count)
                        rtt_count = returnToCare(treatmentCurrent)
                        txMlSelect = df.query('FacilityName == @select_facilities')
                        txMlCheck = txMlSelect.query(
                            'ARTStatus_PreviousQuarter == "Active" & CurrentARTStatus_Pharmacy != "Active"  ')
                        txML_count = txMlCheck['ARTStatus_PreviousQuarter'].count()
                        ipt_screening, ipt_screening_query = iptScreening(treatmentCurrent)
                        tbDocumented_result_count = documentedTb(ipt_screening_query)
                        Current_TB_Status_count = CurrentTbStatus(ipt_screening_query)
                        tx_curr_report_table = txReportDataframe(pbs_count, pbsCoverage,
                                                                 ipt_screening, Current_TB_Status_count,
                                                                 tbDocumented_result_count, rtt_count, txML_count)
                        tx_curr_dataFrame = txCurrReportFormat(tx_curr_report_table)

                        with all_card:
                            displayCard(countAdolescent, countAdult, countFemale, countMale, countPaed,
                                        treatmentCurrent_count)

                        with txCurrPlaceholder:
                            st.table(tx_curr_dataFrame)

                        with barChartDisplay:
                            age_group = treatmentCurrent.query('Sex == "M" ')
                            fiftyplus, lessthanforty_four, lessthanforty_nine, lessthanfour, lessthanfourteen, \
                            lessthannineteen, lessthanone, lessthanten, lessthanthirty_four, lessthanthirty_nine, \
                            lessthantwenty_four, lessthantwenty_nine = age_grouping(
                                age_group)

                            male = [lessthanone, lessthanfour, lessthanten, lessthanfourteen,
                                    lessthannineteen, lessthantwenty_four, lessthantwenty_nine,
                                    lessthanthirty_four, lessthanthirty_nine, lessthanforty_four,
                                    lessthanforty_nine, fiftyplus]

                            age_group_female = treatmentCurrent.query('Sex == "F" ')
                            fiftyplus, lessthanforty_four, lessthanforty_nine, lessthanfour, lessthanfourteen, \
                            lessthannineteen, lessthanone, lessthanten, lessthanthirty_four, lessthanthirty_nine, \
                            lessthantwenty_four, lessthantwenty_nine = age_grouping(
                                age_group_female)

                            female = [lessthanone, lessthanfour, lessthanten, lessthanfourteen,
                                      lessthannineteen, lessthantwenty_four, lessthantwenty_nine,
                                      lessthanthirty_four, lessthanthirty_nine, lessthanforty_four,
                                      lessthanforty_nine,
                                      fiftyplus]

                            female = [int(i) for i in female]
                            male = [int(i) for i in male]

                            bar_chart_display(female, male)

            if choice == 'Viral-Load Cascade' and choice is not None:
                placeholder.empty()

                st.markdown('<br>',
                            unsafe_allow_html=True)
                report_date = st.date_input("Select your reporting date", )
                st.markdown('<br>',
                            unsafe_allow_html=True)

                treatmentCurrent = tx_curr(df)
                treatmentCurrent_count = txCurr(treatmentCurrent)

                #######################ELIGIBLE ####################
                vl_data = treatmentCurrent
                vl_data['Ref_Date'] = report_date

                vl_data['ARTStartDate'] = dateConverter(vl_data['ARTStartDate'])

                vl_data['ARTStartDate'] = vl_data['ARTStartDate'].dt.date
                vl_data['DaysOnart'] = (
                        vl_data['Ref_Date'] - vl_data['ARTStartDate']).dt.days

                def viralLoadEligible(dataSet):
                    return dataSet.query(
                        ' DaysOnart >= 180  & CurrentARTStatus_Pharmacy == "Active" & Outcomes == "" ')

                vLEligible = viralLoadEligible(vl_data)
                vLEligibleCount = vLEligible['DaysOnart'].count()

                ##### VL eligible clients sample collected but awaiting results##############
                vlAwaiting_Result = sample_sent_awaiting(dateConverter, report_date, vLEligible)
                vlAwaiting_Result_count = vlAwaiting_Result['DateofCurrentViralLoad'].count()

                ####################### DOCUMENTED VL ####################
                vl_documented = documented_viralload(dateConverter, vl_data, report_date, viralLoadEligible)
                documentedViralload = vl_documented['PepID'].count()

                ####################### VL sample taken and sent to PCR Lab ####################
                vlSentToLab = documentedViralload + vlAwaiting_Result_count

                # #######################VL Eligible clients with Sample not yet taken####################
                vlSamplesNotYet = vLEligibleCount - vlSentToLab

                # #######################SUPPRESSED VL ####################
                suppressedVl = suppressed_viral_load(vl_documented)
                suppressedVl_count = suppressedVl.CurrentViralLoad.count()

                # #######################SUPPRESSION RATE ####################
                suppressionRate = ((suppressedVl_count / documentedViralload) * 100).round(1)

                # #######################VL COVERAGE ####################
                vlCoverage = ((documentedViralload / vLEligibleCount) * 100).round(1)

                st.markdown('<p class="tb">VIRAL LOAD CASCADE </p>',
                            unsafe_allow_html=True)

                states = df['State'].unique()

                with st.sidebar:
                    st.markdown('<br>', unsafe_allow_html=True)
                    lgas, select_state, state = selectState(treatmentCurrent, states)

                    st.markdown('<br>', unsafe_allow_html=True)
                    facilities, lga, select_lgas = selectLga(lgas, state)

                    st.markdown('<br>', unsafe_allow_html=True)

                    select_facilities = st.multiselect(
                        'Select Facilities', facilities, key='facilities'
                    )
                    facilities = state.query('FacilityName == @select_facilities')
                    st.markdown('<br>', unsafe_allow_html=True)
                    st.markdown('<br>', unsafe_allow_html=True)

                vl_cascade_table = st.empty()
                with vl_cascade_table:
                    vlCascade = vl_cascade_calc(documentedViralload, suppressedVl_count, suppressionRate,
                                                treatmentCurrent_count, vLEligibleCount,
                                                vlAwaiting_Result_count,
                                                vlCoverage, vlSamplesNotYet, vlSentToLab)
                    st.table(vlCascade)

                with all_card:
                    viral_load_display(documentedViralload, suppressedVl_count, suppressionRate,
                                       treatmentCurrent_count, vLEligibleCount, vlCoverage)
                pie = st.empty()
                with pie:
                    pieChart = pie_chart_value(suppressedVl)
                    pie_chart_vload(pieChart)

                barChartDisplay = st.empty()
                with barChartDisplay:
                    age_group = suppressedVl.query('Sex == "M" ')
                    fiftyplus, lessthanforty_four, lessthanforty_nine, lessthanfour, lessthanfourteen, \
                    lessthannineteen, lessthanone, lessthanten, lessthanthirty_four, lessthanthirty_nine, \
                    lessthantwenty_four, lessthantwenty_nine = age_grouping(
                        age_group)

                    male = [lessthanone, lessthanfour, lessthanten, lessthanfourteen,
                            lessthannineteen, lessthantwenty_four, lessthantwenty_nine,
                            lessthanthirty_four, lessthanthirty_nine, lessthanforty_four,
                            lessthanforty_nine, fiftyplus]

                    age_group_female = suppressedVl.query('Sex == "F" ')
                    fiftyplus, lessthanforty_four, lessthanforty_nine, lessthanfour, lessthanfourteen, \
                    lessthannineteen, lessthanone, lessthanten, lessthanthirty_four, lessthanthirty_nine, \
                    lessthantwenty_four, lessthantwenty_nine = age_grouping(
                        age_group_female)

                    female = [lessthanone, lessthanfour, lessthanten, lessthanfourteen,
                              lessthannineteen, lessthantwenty_four, lessthantwenty_nine,
                              lessthanthirty_four, lessthanthirty_nine, lessthanforty_four, lessthanforty_nine,
                              fiftyplus]

                    female = [int(i) for i in female]
                    male = [int(i) for i in male]

                    bar_chart_suppressed_vl(female, male)

                if select_state:
                    all_card.empty()
                    pie.empty()
                    vl_cascade_table.empty()
                    treatmentCurrent = tx_curr(state)
                    treatmentCurrent_count = txCurr(treatmentCurrent)

                    #######################ELIGIBLE ####################
                    viralLoadEligible = viral_load_eligible_calc(dateConverter, report_date, treatmentCurrent)
                    vLEligible = viralLoadEligible(treatmentCurrent)
                    vLEligibleCount = vLEligible['DaysOnart'].count()

                    ##### VL eligible clients sample collected but awaiting results##############

                    vlAwaiting_Result = sample_sent_awaiting(dateConverter, report_date, vLEligible)
                    vlAwaiting_Result_count = vlAwaiting_Result['DateofCurrentViralLoad'].count()

                    ####################### DOCUMENTED VL ####################
                    vl_documented = documented_viralload(dateConverter, treatmentCurrent, report_date,
                                                         viralLoadEligible)
                    documentedViralload = vl_documented['PepID'].count()

                    ####################### VL sample taken and sent to PCR Lab ####################
                    vlSentToLab = documentedViralload + vlAwaiting_Result_count

                    # #######################VL Eligible clients with Sample not yet taken####################
                    vlSamplesNotYet = vLEligibleCount - vlSentToLab

                    # #######################SUPPRESSED VL ####################
                    suppressedVl = suppressed_viral_load(vl_documented)
                    suppressedVl_count = suppressedVl.CurrentViralLoad.count()

                    # #######################SUPPRESSION RATE ####################
                    suppressionRate = ((suppressedVl_count / documentedViralload) * 100).round(1)

                    # #######################VL COVERAGE ####################
                    vlCoverage = ((documentedViralload / vLEligibleCount) * 100).round(1)

                with vl_cascade_table:
                    vlCascade = vl_cascade_calc(documentedViralload, suppressedVl_count, suppressionRate,
                                                treatmentCurrent_count, vLEligibleCount,
                                                vlAwaiting_Result_count,
                                                vlCoverage, vlSamplesNotYet, vlSentToLab)
                    st.table(vlCascade)

                with all_card:
                    viral_load_display(documentedViralload, suppressedVl_count, suppressionRate,
                                       treatmentCurrent_count, vLEligibleCount, vlCoverage)
                with pie:
                    pieChart = pie_chart_value(suppressedVl)
                    pie_chart_vload(pieChart)

                if select_lgas:
                    all_card.empty()
                    vl_cascade_table.empty()
                    pie.empty()
                    treatmentCurrent = tx_curr(lga)
                    treatmentCurrent_count = txCurr(treatmentCurrent)

                    #######################ELIGIBLE ####################
                    viralLoadEligible = viral_load_eligible_calc(dateConverter, report_date, treatmentCurrent)
                    vLEligible = viralLoadEligible(treatmentCurrent)
                    vLEligibleCount = vLEligible['DaysOnart'].count()

                    ##### VL eligible clients sample collected but awaiting results##############

                    vlAwaiting_Result = sample_sent_awaiting(dateConverter, report_date, vLEligible)
                    vlAwaiting_Result_count = vlAwaiting_Result['DateofCurrentViralLoad'].count()

                    ####################### DOCUMENTED VL ####################
                    vl_documented = documented_viralload(dateConverter, treatmentCurrent, report_date,
                                                         viralLoadEligible)
                    documentedViralload = vl_documented['PepID'].count()

                    ####################### VL sample taken and sent to PCR Lab ####################
                    vlSentToLab = documentedViralload + vlAwaiting_Result_count

                    # #######################VL Eligible clients with Sample not yet taken####################
                    vlSamplesNotYet = vLEligibleCount - vlSentToLab

                    # #######################SUPPRESSED VL ####################
                    suppressedVl = suppressed_viral_load(vl_documented)
                    suppressedVl_count = suppressedVl.CurrentViralLoad.count()

                    # #######################SUPPRESSION RATE ####################
                    suppressionRate = ((suppressedVl_count / documentedViralload) * 100).round(1)

                    # #######################VL COVERAGE ####################
                    vlCoverage = ((documentedViralload / vLEligibleCount) * 100).round(1)

                    with vl_cascade_table:
                        vlCascade = vl_cascade_calc(documentedViralload, suppressedVl_count, suppressionRate,
                                                    treatmentCurrent_count, vLEligibleCount,
                                                    vlAwaiting_Result_count,
                                                    vlCoverage, vlSamplesNotYet, vlSentToLab)
                        st.table(vlCascade)

                    with all_card:
                        viral_load_display(documentedViralload, suppressedVl_count, suppressionRate,
                                           treatmentCurrent_count, vLEligibleCount, vlCoverage)
                    pie = st.empty()
                    with pie:
                        pieChart = pie_chart_value(suppressedVl)
                        pie_chart_vload(pieChart)

                if select_facilities:
                    all_card.empty()
                    vl_cascade_table.empty()
                    pie.empty()
                    treatmentCurrent = tx_curr(facilities)
                    treatmentCurrent_count = txCurr(treatmentCurrent)

                    # ######################ELIGIBLE ####################
                    viralLoadEligible = viral_load_eligible_calc(dateConverter, report_date, treatmentCurrent)
                    vLEligible = viralLoadEligible(treatmentCurrent)
                    vLEligibleCount = vLEligible['DaysOnart'].count()

                    ##### VL eligible clients sample collected but awaiting results##############

                    vlAwaiting_Result = sample_sent_awaiting(dateConverter, report_date, vLEligible)
                    vlAwaiting_Result_count = vlAwaiting_Result['DateofCurrentViralLoad'].count()

                    ####################### DOCUMENTED VL ####################
                    vl_documented = documented_viralload(dateConverter, treatmentCurrent, report_date,
                                                         viralLoadEligible)
                    documentedViralload = vl_documented['PepID'].count()

                    ####################### VL sample taken and sent to PCR Lab ####################
                    vlSentToLab = documentedViralload + vlAwaiting_Result_count

                    # #######################VL Eligible clients with Sample not yet taken####################
                    vlSamplesNotYet = vLEligibleCount - vlSentToLab

                    # #######################SUPPRESSED VL ####################
                    suppressedVl = suppressed_viral_load(vl_documented)
                    suppressedVl_count = suppressedVl.CurrentViralLoad.count()

                    # #######################SUPPRESSION RATE ####################
                    suppressionRate = ((suppressedVl_count / documentedViralload) * 100).round(1)

                    # #######################VL COVERAGE ####################
                    vlCoverage = ((documentedViralload / vLEligibleCount) * 100).round(1)

                    with vl_cascade_table:
                        vlCascade = vl_cascade_calc(documentedViralload, suppressedVl_count, suppressionRate,
                                                    treatmentCurrent_count, vLEligibleCount,
                                                    vlAwaiting_Result_count,
                                                    vlCoverage, vlSamplesNotYet, vlSentToLab)
                        st.table(vlCascade)

                    with all_card:
                        viral_load_display(documentedViralload, suppressedVl_count, suppressionRate,
                                           treatmentCurrent_count, vLEligibleCount, vlCoverage)
                    pie = st.empty()
                    with pie:
                        pieChart = pie_chart_value(suppressedVl)
                        pie_chart_vload(pieChart)

            if choice == 'Treatment New' and data is not None:
                placeholder.empty()

                df['ARTStartDate'] = dateConverter(df.ARTStartDate)
                st.markdown('<br>',
                            unsafe_allow_html=True)
                # dt1, dt2 = st.columns(2)
                # with dt1:
                with st.sidebar:
                    # start date
                    firstDate()
                    start_date = firstDate.start_date

                with st.sidebar:
                    st.markdown('<br>', unsafe_allow_html=True)
                    # end date
                    SecondDate()
                    end_date = SecondDate.end_date

                transferIn = trans_in(df)
                art_start = artStart(df)
                art_start_count = art_start['PepID'].count()
                cd4CountCoverage, cd4_count_result = cd4_counts(art_start, art_start_count)
                pbsCoverage, pbs_count = pbsCheck(art_start, art_start_count)
                transferIn_count = transferIn['State'].count()
                ipt_screening, ipt_screening_query = iptScreening(art_start)
                tbDocumented_result_count = documentedTb(ipt_screening_query)
                Current_TB_Status_count = CurrentTbStatus(ipt_screening_query)
                tbStatus = tbTable(Current_TB_Status_count, ipt_screening, tbDocumented_result_count)
                tbMonitoring = monitoringDataframe(tbStatus)

                st.markdown('<br>',
                            unsafe_allow_html=True)
                st.markdown('<p class="tb">TB SCREENING </p>',
                            unsafe_allow_html=True)
                tb_container = st.empty()

                with tb_container:
                    st.table(tbMonitoring)

                states = df['State'].unique()

                with st.sidebar:
                    st.markdown('<br>',
                                unsafe_allow_html=True)
                    lgas, select_state, state = selectState(art_start, states)

                    st.markdown('<br>',
                                unsafe_allow_html=True)
                    facilities, lga, select_lgas = selectLga(lgas, state)

                    st.markdown('<br>',
                                unsafe_allow_html=True)

                    select_facilities = st.multiselect(
                        'Select Facilities', facilities, key='facilities'
                    )
                    facilities = state.query('FacilityName == @select_facilities')
                    st.markdown('<br>',
                                unsafe_allow_html=True)
                    st.markdown('<br>',
                                unsafe_allow_html=True)

                with txnewContainer:
                    txNewDisplay(art_start_count, cd4CountCoverage, cd4_count_result, pbs_count, pbsCoverage,
                                 transferIn_count)

                btn_download = st.empty()
                st.markdown('<br>',
                            unsafe_allow_html=True)

                with btn_download:
                    download(art_start, convert_df, key='btn1')

                pieChartDisplay = st.empty()
                with pieChartDisplay:
                    pieChart = pie_chart_value(art_start)
                    pie_chart_display(pieChart)

                barChartDisplay = st.empty()
                with barChartDisplay:
                    age_group = art_start.query('Sex == "M" ')
                    fiftyplus, lessthanforty_four, lessthanforty_nine, lessthanfour, lessthanfourteen, \
                    lessthannineteen, lessthanone, lessthanten, lessthanthirty_four, lessthanthirty_nine, \
                    lessthantwenty_four, lessthantwenty_nine = age_grouping(
                        age_group)

                    male = [lessthanone, lessthanfour, lessthanten, lessthanfourteen,
                            lessthannineteen, lessthantwenty_four, lessthantwenty_nine,
                            lessthanthirty_four, lessthanthirty_nine, lessthanforty_four,
                            lessthanforty_nine, fiftyplus]

                    age_group_female = art_start.query('Sex == "F" ')
                    fiftyplus, lessthanforty_four, lessthanforty_nine, lessthanfour, lessthanfourteen, \
                    lessthannineteen, lessthanone, lessthanten, lessthanthirty_four, lessthanthirty_nine, \
                    lessthantwenty_four, lessthantwenty_nine = age_grouping(
                        age_group_female)

                    female = [lessthanone, lessthanfour, lessthanten, lessthanfourteen,
                              lessthannineteen, lessthantwenty_four, lessthantwenty_nine,
                              lessthanthirty_four, lessthanthirty_nine, lessthanforty_four, lessthanforty_nine,
                              fiftyplus]

                    female = [int(i) for i in female]
                    male = [int(i) for i in male]

                    bar_chart_display(female, male)

                if select_state:
                    txnewContainer.empty()
                    pieChartDisplay.empty()
                    tb_container.empty()
                    btn_download.empty()
                    barChartDisplay.empty()
                    tx_new = artStart(state)
                    tx_new_count = tx_new['State'].count()
                    cd4CountCoverage, cd4_count_result = cd4_counts(tx_new, tx_new_count)
                    pbsCoverage, pbs_count = pbsCheck(tx_new, tx_new_count)
                    transferin_check = transferIn.query('State == @select_state')
                    transferIn_count = transferin_check['State'].count()
                    ipt_screening, ipt_screening_query = iptScreening(tx_new)
                    tbDocumented_result_count = documentedTb(ipt_screening_query)
                    Current_TB_Status_count = CurrentTbStatus(ipt_screening_query)
                    tbStatus = tbTable(Current_TB_Status_count, ipt_screening, tbDocumented_result_count)
                    tbMonitoring = monitoringDataframe(tbStatus)

                    with tb_container:
                        st.table(tbMonitoring)

                    with txnewContainer:
                        txNewDisplay(tx_new_count, cd4CountCoverage, cd4_count_result, pbs_count, pbsCoverage,
                                     transferIn_count)
                    with btn_download:
                        download(tx_new, convert_df, key="btn2")

                    with pieChartDisplay:
                        pieChart = pie_chart_value(tx_new)
                        pie_chart_display(pieChart)

                    with barChartDisplay:
                        age_group = tx_new.query('Sex == "M" ')
                        fiftyplus, lessthanforty_four, lessthanforty_nine, lessthanfour, lessthanfourteen, \
                        lessthannineteen, lessthanone, lessthanten, lessthanthirty_four, lessthanthirty_nine, \
                        lessthantwenty_four, lessthantwenty_nine = age_grouping(
                            age_group)

                        male = [lessthanone, lessthanfour, lessthanten, lessthanfourteen,
                                lessthannineteen, lessthantwenty_four, lessthantwenty_nine,
                                lessthanthirty_four, lessthanthirty_nine, lessthanforty_four,
                                lessthanforty_nine, fiftyplus]

                        age_group_female = tx_new.query('Sex == "F" ')
                        fiftyplus, lessthanforty_four, lessthanforty_nine, lessthanfour, lessthanfourteen, \
                        lessthannineteen, lessthanone, lessthanten, lessthanthirty_four, lessthanthirty_nine, \
                        lessthantwenty_four, lessthantwenty_nine = age_grouping(
                            age_group_female)

                        female = [lessthanone, lessthanfour, lessthanten, lessthanfourteen,
                                  lessthannineteen, lessthantwenty_four, lessthantwenty_nine,
                                  lessthanthirty_four, lessthanthirty_nine, lessthanforty_four, lessthanforty_nine,
                                  fiftyplus]

                        female = [int(i) for i in female]
                        male = [int(i) for i in male]

                        bar_chart_display(female, male)

                if select_lgas:
                    txnewContainer.empty()
                    tb_container.empty()
                    btn_download.empty()
                    pieChartDisplay.empty()
                    barChartDisplay.empty()
                    tx_new = artStart(lga)
                    tx_new_state = artStart(tx_new)
                    tx_new_count = tx_new_state['State'].count()
                    cd4CountCoverage, cd4_count_result = cd4_counts(tx_new, tx_new_count)
                    pbsCoverage, pbs_count = pbsCheck(tx_new, tx_new_count)
                    transferin_check = transferIn.query('LGA == @select_lgas')
                    transferIn_count = transferin_check['State'].count()
                    ipt_screening, ipt_screening_query = iptScreening(tx_new)
                    tbDocumented_result_count = documentedTb(ipt_screening_query)
                    Current_TB_Status_count = CurrentTbStatus(ipt_screening_query)
                    tbStatus = tbTable(Current_TB_Status_count, ipt_screening, tbDocumented_result_count)
                    tbMonitoring = monitoringDataframe(tbStatus)

                    with tb_container:
                        st.table(tbMonitoring)

                    with txnewContainer:
                        txNewDisplay(tx_new_count, cd4CountCoverage, cd4_count_result, pbs_count, pbsCoverage,
                                     transferIn_count)
                    with btn_download:
                        download(tx_new, convert_df, key="btn3")

                    with pieChartDisplay:
                        pieChart = pie_chart_value(tx_new)
                        pie_chart_display(pieChart)

                    with barChartDisplay:
                        age_group = tx_new.query('Sex == "M" ')
                        fiftyplus, lessthanforty_four, lessthanforty_nine, lessthanfour, lessthanfourteen, \
                        lessthannineteen, lessthanone, lessthanten, lessthanthirty_four, lessthanthirty_nine, \
                        lessthantwenty_four, lessthantwenty_nine = age_grouping(
                            age_group)

                        male = [lessthanone, lessthanfour, lessthanten, lessthanfourteen,
                                lessthannineteen, lessthantwenty_four, lessthantwenty_nine,
                                lessthanthirty_four, lessthanthirty_nine, lessthanforty_four,
                                lessthanforty_nine, fiftyplus]

                        age_group_female = tx_new.query('Sex == "F" ')
                        fiftyplus, lessthanforty_four, lessthanforty_nine, lessthanfour, lessthanfourteen, \
                        lessthannineteen, lessthanone, lessthanten, lessthanthirty_four, lessthanthirty_nine, \
                        lessthantwenty_four, lessthantwenty_nine = age_grouping(
                            age_group_female)

                        female = [lessthanone, lessthanfour, lessthanten, lessthanfourteen,
                                  lessthannineteen, lessthantwenty_four, lessthantwenty_nine,
                                  lessthanthirty_four, lessthanthirty_nine, lessthanforty_four, lessthanforty_nine,
                                  fiftyplus]

                        female = [int(i) for i in female]
                        male = [int(i) for i in male]

                        bar_chart_display(female, male)

                if select_facilities:
                    txnewContainer.empty()
                    tb_container.empty()
                    btn_download.empty()
                    pieChartDisplay.empty()
                    barChartDisplay.empty()
                    tx_new = artStart(facilities)
                    tx_new_state = artStart(tx_new)
                    tx_new_count = tx_new_state['State'].count()
                    cd4CountCoverage, cd4_count_result = cd4_counts(tx_new, tx_new_count)
                    pbsCoverage, pbs_count = pbsCheck(tx_new, tx_new_count)
                    transferin_check = transferIn.query('FacilityName == @select_facilities')
                    transferIn_count = transferin_check['State'].count()
                    ipt_screening, ipt_screening_query = iptScreening(tx_new)
                    tbDocumented_result_count = documentedTb(ipt_screening_query)
                    Current_TB_Status_count = CurrentTbStatus(ipt_screening_query)
                    tbStatus = tbTable(Current_TB_Status_count, ipt_screening, tbDocumented_result_count)
                    tbMonitoring = monitoringDataframe(tbStatus)

                    with tb_container:
                        st.table(tbMonitoring)

                    with txnewContainer:
                        txNewDisplay(tx_new_count, cd4CountCoverage, cd4_count_result, pbs_count, pbsCoverage,
                                     transferIn_count)
                    with btn_download:
                        download(tx_new, convert_df, key="btn4")

                    with pieChartDisplay:
                        pieChart = pie_chart_value(tx_new)
                        pie_chart_display(pieChart)

                    with barChartDisplay:
                        age_group = tx_new.query('Sex == "M" ')
                        fiftyplus, lessthanforty_four, lessthanforty_nine, lessthanfour, lessthanfourteen, \
                        lessthannineteen, lessthanone, lessthanten, lessthanthirty_four, lessthanthirty_nine, \
                        lessthantwenty_four, lessthantwenty_nine = age_grouping(
                            age_group)

                        male = [lessthanone, lessthanfour, lessthanten, lessthanfourteen,
                                lessthannineteen, lessthantwenty_four, lessthantwenty_nine,
                                lessthanthirty_four, lessthanthirty_nine, lessthanforty_four,
                                lessthanforty_nine, fiftyplus]

                        age_group_female = tx_new.query('Sex == "F" ')
                        fiftyplus, lessthanforty_four, lessthanforty_nine, lessthanfour, lessthanfourteen, \
                        lessthannineteen, lessthanone, lessthanten, lessthanthirty_four, lessthanthirty_nine, \
                        lessthantwenty_four, lessthantwenty_nine = age_grouping(
                            age_group_female)

                        female = [lessthanone, lessthanfour, lessthanten, lessthanfourteen,
                                  lessthannineteen, lessthantwenty_four, lessthantwenty_nine,
                                  lessthanthirty_four, lessthanthirty_nine, lessthanforty_four, lessthanforty_nine,
                                  fiftyplus]

                        female = [int(i) for i in female]
                        male = [int(i) for i in male]

                        bar_chart_display(female, male)
            if choice == 'Clinical Report':
                with st.sidebar:
                    option = st.selectbox('What would you like to do?',
                                          ('', 'MISSED APPOINTMENT', 'IIT', 'POTENTIAL IIT'))
                with st.sidebar:
                    # start date
                    firstDate()
                    start_date = firstDate.start_date

                with st.sidebar:
                    st.markdown('<br>', unsafe_allow_html=True)
                    # end date
                    SecondDate()
                    end_date = SecondDate.end_date

                st.write('You selected:', option)
                st.info('MMD <3')
                st.warning('MMD 3')
                st.success('MMD 4')
                st.warning('MMD 5')
                st.info('MMD 6')
                st.success('MISS APPOINTMENT')
                st.info('IIT')
                st.warning('POTENTIAL IIT')
                st.success('UNSUPPRESSED VL')
                st.info('LOW-LEVEL VL')

    # REPORT MODULES

    if selected == 'Reports':
        st.markdown('<p class="font">Reports Dashbooard✍</p>', unsafe_allow_html=True)
        # ######### FOR DISPLAYING THE CARDS##################
        weekly_display = st.container()

        placeholder = st.empty()
        if st.session_state.data is not None:
            linelist = placeholder.file_uploader(
                'Upload your Treatment Linelist here. Pls ART Linelist Only 🙏🙏🙏🙏', type=['csv'])
            placeholder.empty()
        else:
            linelist = placeholder.file_uploader(
                'Upload your Treatment Linelist here. Pls ART Linelist Only 🙏🙏🙏🙏', type=['csv'])

        if linelist is not None:
            placeholder.empty()

            @st.cache(allow_output_mutation=True)
            def load_data2():
                df = pd.read_csv(linelist, encoding='unicode_escape', on_bad_lines='skip', low_memory=False)

                return df

            vl_data = load_data2()
            cleanDataSet(vl_data)

            vl_data['Pharmacy_LastPickupdate'] = dateConverter(vl_data.Pharmacy_LastPickupdate)

            vl_data['ARTStartDate'] = dateConverter(vl_data.ARTStartDate)

            vl_data['DateofCurrentViralLoad'] = dateConverter(vl_data.DateofCurrentViralLoad)

            # #############END OF FUNCTION########################
            with st.sidebar:
                st.markdown('<br>',
                            unsafe_allow_html=True)
                report_type = st.selectbox('Select Report', reports)

            # #############&E Weekly Report########################
            if report_type == 'M&E Weekly Report':
                with st.sidebar:
                    st.markdown('<br>',
                                unsafe_allow_html=True)
                    # start date
                    firstDate()
                    start_date = firstDate.start_date
                with st.sidebar:
                    st.markdown('<br>',
                                unsafe_allow_html=True)
                    # end date
                    SecondDate()
                    end_date = SecondDate.end_date

                treatmentCurrent = tx_curr(vl_data)
                treatmentCurrent = treatmentCurrent['CurrentARTStatus_Pharmacy'].count()

                art_start = artStart(vl_data)
                art_start_count = art_start['PepID'].count()

                pharm_start = pharm()
                pharm_start_count = pharm_start['Pharmacy_LastPickupdate'].count(
                )

                vl_data['Outcomes_Date'] = dateConverter(vl_data.Outcomes_Date)
                outcomes_date = vl_data.query('Outcomes_Date >= @start_date &  Outcomes_Date <= @end_date')
                outcomes_date = outcomes_date['Outcomes_Date'].count()

                vl_data['LastPickupDateCal'] = pd.to_datetime(
                    vl_data['LastPickupDateCal'])

                vl_data = vl_data.query('CurrentARTStatus_Pharmacy =="Active" ')

                # arvRefill = df['DaysOfARVRefill'].astype(int)

                def calMissedApp(x):
                    return x['LastPickupDateCal'] + relativedelta(days=int(x['DaysOfARVRefill']))

                vl_data['appointmentDate'] = vl_data.apply(calMissedApp, axis=1)

                thisWeekMissedAppointment = vl_data[(vl_data['appointmentDate'] >= str(start_date)) &  # type: ignore
                                                    (vl_data['appointmentDate'] <= str(end_date))]  # type: ignore
                thisWeekMissedAppointment = thisWeekMissedAppointment['appointmentDate'].count(
                )

                ipt_screening = pharm_start['IPT_Screening_Date'].count()

                # items = [treatmentCurrent,art_start_count,pharm_start_count,ipt_screening,
                # thisWeekMissedAppointment,outcomes_date]
                #
                if pharm_start_count == 0:
                    pass
                else:
                    with weekly_display:
                        st.markdown(f"""
                                            <div class="txnew">
                                                <div class="card">
                                                    <div class="title">
                                                        Tx_Curr
                                                    </div>
                                                    <div class="circle">{treatmentCurrent}</div>
                                                </div>

                                            <div class="card">
                                                    <div class="title">
                                                        Tx_New
                                                    </div>
                                                    <div class="circle">{art_start_count}</div>
                                                </div>
                                            <div class="card">
                                                    <div class="title">
                                                        Attendance
                                                    </div>
                                                    <div class="circle">{pharm_start_count}</div>
                                                </div>
                                            <div class="card">
                                                    <div class="title">
                                                        IPT Screening
                                                    </div>
                                                    <div class="circle">{ipt_screening}</div>
                                                </div>
                                            <div class="card">
                                                    <div class="title">
                                                        MIssed Appt
                                                    </div>
                                                    <div class="circle">{thisWeekMissedAppointment}</div>
                                                </div>
                                            <div class="card">
                                                    <div class="title">
                                                        Outcomes
                                                    </div>
                                                    <div class="circle">{outcomes_date}</div>
                                                </div>
                                            
                                            </div>
                                                    """, unsafe_allow_html=True)

            # ######################## 'M&E Monthly Report ###########################
            if report_type == 'M&E Monthly Report':
                with st.sidebar:
                    st.markdown('<br>',
                                unsafe_allow_html=True)
                    option = st.selectbox(
                        'Select Report Type',
                        ('', 'Clinic Attendance', 'Treatment New', 'VL Test Results',
                         'Virologically Suppressed', 'Adult 1st line',
                         'Adult 2nd line', 'Child 1st line', 'Child 2nd line'))

                if option == 'Clinic Attendance':

                    with st.sidebar:
                        st.markdown('<br>',
                                    unsafe_allow_html=True)
                        # start date
                        firstDate()
                        start_date = firstDate.start_date
                    with st.sidebar:
                        st.markdown('<br>',
                                    unsafe_allow_html=True)
                        # end date
                        SecondDate()
                        end_date = SecondDate.end_date

                    pharm_start = pharm()

                    pharm_start_count = pharm_start['Pharmacy_LastPickupdate'].count(
                    )

                    if pharm_start_count == 0:
                        pass

                    else:
                        st.subheader(
                            f'Attendance for the period of {start_date} to {end_date}')

                        barChartDisplay = st.empty()
                        pregnant_status = st.empty()

                        age_group = pharm_start.query('Sex == "M" & CurrentARTStatus_Pharmacy == "Active" ')
                        fiftyplus, lessthanforty_four, lessthanforty_nine, lessthanfour, lessthanfourteen, \
                        lessthannineteen, lessthanone, lessthanten, lessthanthirty_four, lessthanthirty_nine, \
                        lessthantwenty_four, lessthantwenty_nine = age_grouping(age_group)

                        male = [lessthanone, lessthanfour, lessthanten, lessthanfourteen,
                                lessthannineteen, lessthantwenty_four, lessthantwenty_nine,
                                lessthanthirty_four, lessthanthirty_nine, lessthanforty_four,
                                lessthanforty_nine, fiftyplus]

                        age_group_female = pharm_start.query('Sex == "F" & CurrentARTStatus_Pharmacy == "Active" ')
                        fiftyplus, lessthanforty_four, lessthanforty_nine, lessthanfour, lessthanfourteen, \
                        lessthannineteen, lessthanone, lessthanten, lessthanthirty_four, lessthanthirty_nine, \
                        lessthantwenty_four, lessthantwenty_nine = age_grouping(age_group_female)

                        female = [lessthanone, lessthanfour, lessthanten, lessthanfourteen,
                                  lessthannineteen, lessthantwenty_four, lessthantwenty_nine,
                                  lessthanthirty_four, lessthanthirty_nine, lessthanforty_four, lessthanforty_nine,
                                  fiftyplus]

                        female = [int(i) for i in female]
                        male = [int(i) for i in male]

                        with barChartDisplay:
                            bar_chart_display(female, male)

                        age_group_pregnant = pharm_start.query('Sex == "F" & CurrentARTStatus_Pharmacy == "Active" '
                                                               '& CurrentPregnancyStatus == "Pregnant" ')
                        fiftyplus, lessthanforty_four, lessthanforty_nine, \
                        lessthannineteen, lessthanthirty_four, lessthanthirty_nine, \
                        lessthantwenty_four, lessthantwenty_nine = pregnant_grouping(age_group_pregnant)

                        pregnant = [lessthannineteen, lessthantwenty_four, lessthantwenty_nine,
                                    lessthanthirty_four, lessthanthirty_nine, lessthanforty_four,
                                    lessthanforty_nine, fiftyplus]

                        age_group_breastfeeding = pharm_start.query(
                            'Sex == "F" & CurrentARTStatus_Pharmacy == "Active" '
                            ' & CurrentPregnancyStatus == "Breastfeeding"')
                        fiftyplus, lessthanforty_four, lessthanforty_nine, lessthannineteen, \
                        lessthanthirty_four, lessthanthirty_nine, lessthantwenty_four, \
                        lessthantwenty_nine = pregnant_grouping(age_group_breastfeeding)

                        breastfeeding = [lessthannineteen, lessthantwenty_four, lessthantwenty_nine,
                                         lessthanthirty_four, lessthanthirty_nine, lessthanforty_four,
                                         lessthanforty_nine,
                                         fiftyplus]

                        pregnant = [int(i) for i in pregnant]
                        breastfeeding = [int(i) for i in breastfeeding]

                        with pregnant_status:
                            pregnant_breastfeeding_barchart(breastfeeding, pregnant)

                        st.write(age_group['Sex'].count())
                        st.write(age_group_female['Sex'].count())
                        st.write(age_group_pregnant['Sex'].count())
                        st.write(age_group_breastfeeding['Sex'].count())

                ######################### Treatment New ###########################
                dt1, dt2 = st.columns(2)
                if option == 'Treatment New':
                    with dt1:
                        # start date
                        start_date = st.date_input(
                            "From", )
                    with dt2:
                        # end date
                        end_date = st.date_input(
                            "To", )

                    art_start = artStart(vl_data)

                    pharm_start_count = art_start['ARTStartDate'].count(
                    )

                    if pharm_start_count == 0:
                        pass
                    else:

                        female = art_start.query(
                            'Sex == "F" & CurrentARTStatus_Pharmacy =="Active" ')

                        f = female['Current_Age'].apply(condition)

                        #######MALE#############
                        male = art_start.query(
                            'Sex == "M" & CurrentARTStatus_Pharmacy =="Active" ')

                        m = male['Current_Age'].apply(condition)

                        # PREGNANT/BREASTFEEDING

                        pregnant = art_start.query(
                            'Sex == "F" & CurrentPregnancyStatus =="Breastfeeding" | CurrentPregnancyStatus =="Pregnant" ')

                        p = pregnant['Current_Age'].apply(condition)

                        # fin = pd.DataFrame(["female",d])
                        st.subheader(
                            f'Treatment New for the period of {start_date} to {end_date}')
                        output()

                #####################Viral load result@@###############################
                if option == 'VL Test Results':

                    dt1, dt2 = st.columns()
                    with dt1:
                        # start date
                        firstDate()

                    with dt2:
                        # end date
                        SecondDate()

                    art_start = vl_data[
                        (vl_data['DateofCurrentViralLoad'] >= str(firstDate.start_date)) &  # type: ignore
                        (vl_data['DateofCurrentViralLoad'] <= str(SecondDate.end_date))]  # type: ignore

                    pharm_start_count = art_start['DateofCurrentViralLoad'].count(
                    )
                    if pharm_start_count == 0:
                        pass
                    else:

                        female = art_start.query(
                            'Sex == "F" & CurrentARTStatus_Pharmacy =="Active" ')

                        f = female['Current_Age'].apply(condition)

                        #######MALE#############
                        male = art_start.query(
                            'Sex == "M" & CurrentARTStatus_Pharmacy =="Active" ')

                        m = male['Current_Age'].apply(condition)

                        # PREGNANT/BREASTFEEDING

                        pregnant = art_start.query(
                            'Sex == "F" & CurrentPregnancyStatus =="Breastfeeding" | CurrentPregnancyStatus =="Pregnant" ')

                        p = pregnant['Current_Age'].apply(condition)

                        # fin = pd.DataFrame(["female",d])
                        output()

                ##################### Suppressed Viral load###############################
                if option == 'Virologically Suppressed':
                    dt1, dt2 = st.columns(2)

                    with dt1:
                        # start date
                        firstDate()

                    with dt2:
                        # end date
                        SecondDate()

                        art_start = vl_data[
                            (vl_data['DateofCurrentViralLoad'] >= str(firstDate.start_date)) &  # type: ignore
                            (vl_data['DateofCurrentViralLoad'] <= str(SecondDate.end_date))]  # type: ignore

                    pharm_start_count = art_start['DateofCurrentViralLoad'].count(
                    )

                    if pharm_start_count == 0:
                        pass
                    else:

                        female = art_start.query(
                            'Sex == "F" & CurrentARTStatus_Pharmacy =="Active" & CurrentViralLoad < 1000 ')

                        f = female['Current_Age'].apply(condition)

                        #######MALE#############
                        male = art_start.query(
                            'Sex == "M" & CurrentARTStatus_Pharmacy =="Active" & CurrentViralLoad < 1000 ')

                        m = male['Current_Age'].apply(condition)

                        # PREGNANT/BREASTFEEDING

                        pregnant = art_start.query(
                            'Sex == "F" & CurrentPregnancyStatus =="Breastfeeding" | CurrentPregnancyStatus =="Pregnant" & CurrentViralLoad < 1000 ')

                        p = pregnant['Current_Age'].apply(condition)

                        # fin = pd.DataFrame(["female",d])
                        output()

                ######################### Adult 1st line ###########################
                if option == 'Adult 1st line':

                    with dt1:
                        # start date
                        firstDate()

                    with dt2:
                        # end date
                        SecondDate()

                    pharm_start = vl_data[
                        (vl_data['Pharmacy_LastPickupdate'] >= str(firstDate.start_date)) &  # type: ignore
                        (vl_data['Pharmacy_LastPickupdate'] <= str(SecondDate.end_date))]  # type: ignore

                    pharm_start_count = pharm_start['Pharmacy_LastPickupdate'].count(
                    )

                    if pharm_start_count == 0:
                        pass

                    else:

                        female = pharm_start.query(
                            'Sex == "F" & CurrentARTStatus_Pharmacy =="Active" & CurrentRegimenLine == "Adult 1st line ARV regimen" ')

                        f = female['Current_Age'].apply(condition)

                        #######MALE#############
                        male = pharm_start.query(
                            'Sex == "M" & CurrentARTStatus_Pharmacy =="Active" & CurrentRegimenLine == "Adult 1st line ARV regimen"  ')

                        m = male['Current_Age'].apply(condition)

                        # PREGNANT/BREASTFEEDING

                        pregnant = pharm_start.query(
                            'Sex == "F" & CurrentPregnancyStatus =="Breastfeeding" | CurrentPregnancyStatus =="Pregnant" & CurrentRegimenLine == "Adult 1st line ARV regimen"   ')

                        p = pregnant['Current_Age'].apply(condition)

                        # fin = pd.DataFrame(["female",d])
                        st.subheader('Adult 1st Line ARV')
                        output()

                ######################### Adult 2nd line ###########################
                if option == 'Adult 2nd line':

                    with dt1:
                        # start date
                        firstDate()

                    with dt2:
                        # end date
                        SecondDate()

                        pharm_start = vl_data[
                            (vl_data['Pharmacy_LastPickupdate'] >= str(firstDate.start_date)) &  # type: ignore
                            (vl_data['Pharmacy_LastPickupdate'] <= str(firstDate.end_date))]  # type: ignore

                    pharm_start_count = pharm_start['Pharmacy_LastPickupdate'].count(
                    )

                    if pharm_start_count == 0:
                        pass

                    else:

                        female = pharm_start.query(
                            'Sex == "F" & CurrentARTStatus_Pharmacy =="Active" & CurrentRegimenLine == "Adult 2nd line ARV regimen"  ')

                        f = female['Current_Age'].apply(condition)

                        #######MALE#############
                        male = pharm_start.query(
                            'Sex == "M" & CurrentARTStatus_Pharmacy =="Active" & CurrentRegimenLine == "Adult 2nd line ARV regimen" ')

                        m = male['Current_Age'].apply(condition)

                        # PREGNANT/BREASTFEEDING

                        pregnant = female.query(
                            ' CurrentPregnancyStatus == "Breastfeeding" | CurrentPregnancyStatus =="Pregnant" ')

                        p = pregnant['Current_Age'].apply(condition)

                        # fin = pd.DataFrame(["female",d])
                        st.subheader('Adult 2nd Line ARV')
                        output()

                ######################### Child 1st line ###########################
                if option == 'Child 1st line':

                    with dt1:
                        # start date
                        firstDate()

                    with dt2:
                        # end date
                        SecondDate()

                        pharm_start = vl_data[
                            (vl_data['Pharmacy_LastPickupdate'] >= str(firstDate.start_date)) & (  # type: ignore
                                    vl_data['Pharmacy_LastPickupdate'] <= str(SecondDate.end_date))]  # type: ignore

                    pharm_start_count = pharm_start['Pharmacy_LastPickupdate'].count(
                    )

                    if pharm_start_count == 0:
                        pass

                    else:

                        female = pharm_start.query(
                            'Sex == "F" & CurrentARTStatus_Pharmacy =="Active" & CurrentRegimenLine == "Child 1st line ARV regimen" ')

                        f = female['Current_Age'].apply(condition)

                        #######MALE#############
                        male = pharm_start.query(
                            'Sex == "M" & CurrentARTStatus_Pharmacy =="Active" & CurrentRegimenLine == "Child 1st line ARV regimen"  ')

                        m = male['Current_Age'].apply(condition)

                        # PREGNANT/BREASTFEEDING
                        pregnant = female.query(
                            ' CurrentPregnancyStatus == "Breastfeeding" | CurrentPregnancyStatus =="Pregnant" ')

                        p = pregnant['Current_Age'].apply(condition)

                        # fin = pd.DataFrame(["female",d])
                        st.subheader('Child 1st Line ARV')
                        output()

                ######################### Child 2nd line ###########################
                if option == 'Child 2nd line':

                    with dt1:
                        # start date
                        firstDate()

                    with dt2:
                        # end date
                        SecondDate()

                        pharm_start = vl_data[
                            (vl_data['Pharmacy_LastPickupdate'] >= str(firstDate.start_date)) &  # type: ignore
                            (vl_data['Pharmacy_LastPickupdate'] <= str(SecondDate.end_date))]  # type: ignore

                    pharm_start_count = pharm_start['Pharmacy_LastPickupdate'].count(
                    )

                    if pharm_start_count == 0:
                        pass

                    else:

                        female = pharm_start.query(
                            'Sex == "F" & CurrentARTStatus_Pharmacy =="Active" & CurrentRegimenLine == "Child 2nd line ARV regimen"  ')

                        f = female['Current_Age'].apply(condition)

                        #######MALE#############
                        male = pharm_start.query(
                            'Sex == "M" & CurrentARTStatus_Pharmacy =="Active" & CurrentRegimenLine == "Child 2nd line ARV regimen" ')

                        m = male['Current_Age'].apply(condition)

                        pregnant = female.query(
                            ' CurrentPregnancyStatus == "Breastfeeding" | CurrentPregnancyStatus =="Pregnant" ')

                        p = pregnant['Current_Age'].apply(condition)

                        st.subheader('Child 2nd Line ARV')
                        output()

    if selected == 'Download':
        st.markdown('<p class="font">Downloads Dashboard 🌎</p>', unsafe_allow_html=True)
        with st.sidebar:
            select_downlaod = st.selectbox('Select what to download?',
                                           ('MISSED APPOINTMENT', 'IIT', 'POTENTIAL IIT', 'Vl ELIGIBILITY'))
        with st.sidebar:
            st.markdown('<br>', unsafe_allow_html=True)
            # start date
            firstDate()
            start_date = firstDate.start_date

        with st.sidebar:
            st.markdown('<br>', unsafe_allow_html=True)
            # end date
            SecondDate()
            end_date = SecondDate.end_date

        placeholder = st.empty()
        if st.session_state is not None:
            linelist = placeholder.file_uploader(
                'Upload your Treatment Linelist here. Pls ART Linelist Only 🙏🙏🙏🙏', type=['csv'])

        else:
            linelist = placeholder.file_uploader(
                'Upload your Treatment Linelist here. Pls ART Linelist Only 🙏🙏🙏🙏', type=['csv'])
            st.session_state = linelist
            placeholder.empty()
        if linelist is not None:
            placeholder.empty()
            df = pd.read_csv(linelist, encoding='unicode_escape', on_bad_lines='skip', low_memory=False)
            cleanDataSet(df)

            df['LastPickupDateCal'] = pd.to_datetime(
                df['LastPickupDateCal'])

            lastPic = df['LastPickupDateCal']
            arvRefill = df['DaysOfARVRefill'].astype(int)

            df = df.query('LastPickupDateCal != "" ')

            def calMissedApp(x):
                return x['LastPickupDateCal'] + relativedelta(days=int(x['DaysOfARVRefill']))

            df['appointmentDate'] = df.apply(calMissedApp, axis=1)
            df['appointmentDate'] = df['appointmentDate'].dt.date

            if select_downlaod == 'MISSED APPOINTMENT':
                states = df['State'].unique()

                with st.sidebar:
                    st.markdown('<br>', unsafe_allow_html=True)
                    lgas, select_state, state = selectState(df, states)

                    st.markdown('<br>', unsafe_allow_html=True)
                    facilities, lga, select_lgas = selectLga(lgas, state)

                    st.markdown('<br>', unsafe_allow_html=True)
                    select_facilities = st.multiselect(
                        'Select Facilities', facilities, key='facilities'
                    )
                    facilities = state.query('FacilityName == @select_facilities')

                missedAppointment = df.query('appointmentDate >= @start_date & appointmentDate <= @end_date')

                selected_column = st.multiselect('Select columns to download', missedAppointment.columns)

                selected_option = missedAppointment[selected_column]

                output = selected_option.reset_index(drop=True)

                if selected_option.empty:
                    st.info('Select columns to Download')
                else:
                    output

                    download(output, convert_df, key="btn4")

                if select_state:
                    missedAppointment = df.query('State == @select_state & appointmentDate >= @start_date & '
                                                 'appointmentDate <= @end_date')

                    # selected_column = st.multiselect('How would you like to be contacted?', missedAppointment.columns)

                    # selected_option = missedAppointment[selected_column]

                    output = missedAppointment.reset_index(drop=True)
                    output

    if selected == 'EMR-NDR':
        st.markdown('<p class="font">EMR VS NDR 📝</p>',
                    unsafe_allow_html=True)

        placeholder = st.empty()
        ndrholder = st.empty()
        emr = placeholder.file_uploader(
            'STEP 1: UPLOAD EMR LINELIST 🙏🙏🙏🙏', type=['csv'])

        ndr = ndrholder.file_uploader(
            'STEP 2: UPLOAD NDR LINELIST 🙏🙏🙏🙏', type=['csv'])

        if emr is not None:
            @st.cache(allow_output_mutation=True)
            def load_data3():
                df_emr = pd.read_csv(emr, encoding='unicode_escape', on_bad_lines='skip')
                return df_emr

            df_emr = load_data3()
            cleanDataSet(df_emr)

        if ndr is not None:
            placeholder.empty()
            ndrholder.empty()

            @st.cache(allow_output_mutation=True)
            def load_data4():
                df_ndr = pd.read_csv(ndr, encoding='unicode_escape', on_bad_lines='skip')
                return df_ndr

            df_ndr = load_data4()

        with st.sidebar:
            choice = st.selectbox('Select Indicator', activities)
        if choice == 'Treatment New':
            st.write(df_ndr['Current Status (28 Days)'].value_counts())
            st.write(df_emr['CurrentARTStatus_Pharmacy'].value_counts())

    if selected == 'Feedback':
        st.markdown('<p class="font">GOT A FEW MINUTES TO HELP ?</p>',
                    unsafe_allow_html=True)
        st.subheader('Help us improve!!!.')
        st.subheader(
            'Tell us what you think of our webapp. We welcome your feedback')


def select_activities():
    activities = ['', 'Treatment New', 'Treatment Current', 'Viral-Load Cascade',
                  'Clinical Report']
    return activities


hide_streamlit_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            # header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """

st.markdown(hide_table_row_index, unsafe_allow_html=True)
if __name__ == '__main__':
    main()
