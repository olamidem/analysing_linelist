from func import *
from functions.download.downloadFun import *
from functions.tx_new.tx_new_display import *
from tx_curr_card import *
from functions.tx_curr.treatmentCurrent import *
from functions.tx_new.treatmentNew import *
from functions.cleaningData.cleaningFunc import *
from functions.tx_new.treatmentNew import *
from functions.pieChart.pieChart import *
import pandas as pd
from datetime import timedelta
from streamlit_option_menu import option_menu
from dateutil.relativedelta import relativedelta

import streamlit.components.v1 as components
from PIL import Image

st.set_page_config(page_title="Report Dashbooard 💻", page_icon="📑", layout="wide",
                   initial_sidebar_state="auto", )

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def main():
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
        pharm_start = dataVariable[(dataVariable['Pharmacy_LastPickupdate'] >= str(start_date)) &  # type: ignore
                         (dataVariable['Pharmacy_LastPickupdate'] <= str(end_date))]  # type: ignore
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

    activities = ['', 'Treatment New', 'Treatment Current', 'Viral-Load Cascade',
                  'Clinical Report']
    reports = ['', 'HI Weekly Report',
               'M&E Weekly Report', 'M&E Monthly Report']
    with st.sidebar:
        url = 'cpu.png'
        emrlogo = Image.open(url)
        st.image(emrlogo,width = 200)

    selected = option_menu(
            menu_title= None,
            options=['Monitoring', 'Reports', 'EMR-NDR', 'Feedback'],
            icons=['pie-chart-fill', 'book',
                   'list-task', 'chat-square-text-fill'],
            orientation= 'horizontal',
            menu_icon='cast',
            default_index=0,
        styles={
            "container": {"background-color": "#fff"},
            # "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {"--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#176c36"},
        }
        )

    if selected == 'Monitoring':

        st.markdown('<p class="font">Monitoring Dashboard💻</p>',
                    unsafe_allow_html=True)
        # ############MONITORING MODULES#######################################

        monitoring = st.container()
        with monitoring:
            all_card = st.empty()
            ####################### TREATMENT NEW CONTAINER###################
            txnewContainer = st.empty()
            placeholder = st.empty()

        data = placeholder.file_uploader(
            'Upload your Treatment Linelist here. Pls ART Linelist Only 🙏🙏🙏🙏', type=['csv'])
        st.session_state.data = data
        if data is not None:
            if data not in st.session_state:
                st.session_state.data = data.name


            # fileName(data)

            @st.cache(allow_output_mutation=True)
            def load_data1():
                df = pd.read_csv(data, encoding='unicode_escape')
                return df

            df = load_data1()
            columns = ['ARTStartDate']
            columns2 = [df.columns[12]]
            if [columns] == [columns2]:
                cleanDataSet(df)
                st.markdown('<br>',
                            unsafe_allow_html=True)

                with st.sidebar:
                    choice = st.selectbox(
                        'Select Indicator', activities)

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

                        dataVariable = tx_curr(df)

                        states = dataVariable['State'].unique()

                        with st.sidebar:
                            st.markdown('<br>',
                                        unsafe_allow_html=True)
                            lgas, select_state, state = selectState(dataVariable, states)

                        with st.sidebar:
                            st.markdown('<br>',
                                        unsafe_allow_html=True)
                            facilities, lga, select_lgas = selectLga(lgas, state)

                        with st.sidebar:
                            st.markdown('<br>',
                                        unsafe_allow_html=True)
                            select_facilities = st.multiselect(
                                'Select Facilities', facilities, key='facilities'
                            )
                            facilities = state.query('FacilityName == @select_facilities')


                        with all_card:
                            displayCard(countAdolescent, countAdult, countFemale, countMale, countPaed,
                                        treatmentCurrent_count)

                        with txCurrPlaceholder:
                            st.table(tx_curr_dataFrame)

                        if select_state:
                            all_card.empty()
                            txCurrPlaceholder.empty()
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


                        if select_lgas:
                            all_card.empty()
                            txCurrPlaceholder.empty()
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


                if choice == 'Viral-Load Cascade':
                    if choice is not None:

                        report_date = st.date_input("Select your reporting date", )
                        st.markdown('<br>',
                                    unsafe_allow_html=True)

                        treatmentCurrent = tx_curr(df)
                        treatmentCurrent_count = treatmentCurrent['CurrentARTStatus_Pharmacy'].count()

                        #######################ELIGIBLE ####################
                        dataVariable = df.query('CurrentARTStatus_Pharmacy == "Active"  & ARTStartDate != "" ')
                        dataVariable['Ref_Date'] = report_date

                        dataVariable['ARTStartDate'] = dateConverter(dataVariable['ARTStartDate'])

                        dataVariable['ARTStartDate'] = dataVariable['ARTStartDate'].dt.date
                        dataVariable['DaysOnart'] = (
                                dataVariable['Ref_Date'] - dataVariable['ARTStartDate']).dt.days

                        def viralLoadEligible(dataSet):
                            return dataSet.query(
                                ' DaysOnart >= 180  & CurrentARTStatus_Pharmacy == "Active" & Outcomes == "" ')

                        vLEligible = viralLoadEligible(dataVariable)
                        vLEligibleCount = vLEligible['DaysOnart'].count()

                        ##### VL eligible clients sample collected but awaiting results##############

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
                        vlAwaiting_Result_count = vlAwaiting_Result['DateofCurrentViralLoad'].count()

                        ####################### DOCUMENTED VL ####################
                        vl_documented = documented_viralload(dateConverter, dataVariable, report_date, viralLoadEligible)
                        documentedViralload = vl_documented['PepID'].count()

                        ####################### VL sample taken and sent to PCR Lab ####################
                        vlSentToLab = documentedViralload + vlAwaiting_Result_count

                        # #######################VL Eligible clients with Sample not yet taken####################
                        vlSamplesNotYet = vLEligibleCount - vlSentToLab

                        # #######################SUPPRESSED VL ####################
                        suppressedVl = suppressed_viral_load(vl_documented)
                        suppressedVl = suppressedVl.CurrentViralLoad.count()

                        # #######################SUPPRESSION RATE ####################
                        suppressionRate = ((suppressedVl / documentedViralload) * 100).round(1)

                        # #######################VL COVERAGE ####################
                        vlCoverage = ((documentedViralload / vLEligibleCount) * 100).round(1)

                        st.markdown('<p class="tb">VIRAL LOAD CASCADE </p>',
                                    unsafe_allow_html=True)

                        states = df['State'].unique()

                        with st.sidebar:
                            st.markdown('<br>',
                                        unsafe_allow_html=True)
                            lgas, select_state, state = selectState(treatmentCurrent, states)

                        with st.sidebar:
                            st.markdown('<br>',
                                        unsafe_allow_html=True)
                            facilities, lga, select_lgas = selectLga(lgas, state)

                        with st.sidebar:
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
                        st.table(vlCascade)



                        with all_card:
                            st.markdown(f"""
                                            <div class="container">
                                            <div class="card">
                                                <div class="title">
                                                Tx_Curr<span>{f'{treatmentCurrent_count:,d}'}</span>
                                                </div>
                                            </div>
    
                                            <div class="card">
                                                <div class="title">
                                                VL Eligible<span>{f'{vLEligibleCount:,d}'}</span>
                                                </div>
                                            </div>
    
                                            <div class="card">
                                                <div class="title">
                                                Documented VL<span>{f'{documentedViralload:,d}'}</span>
                                                </div>
                                            </div>
    
                                            <div class="card">
                                                <div class="title">
                                                Suppressed VL<span>{f'{suppressedVl:,d}'}</span>
                                                </div>
                                            </div>
                                            <div class="card">
                                                <div class="title">
                                                VL Coverage<span>{vlCoverage}%</span>
                                                </div>
                                            </div>
                                            <div class="card">
                                                <div class="title">
                                                VL Suppression <span>{suppressionRate}%</span>
                                                </div>
                                                
                                            </div>
                                            </div>
                                            """, unsafe_allow_html=True)


                        pieChart = {'Name': ["TX_CURR", "Eligible", "Documented", "Suppressed"],
                                    'values': [treatmentCurrent_count, vLEligibleCount, documentedViralload, suppressedVl]}
                        pieChart = pd.DataFrame(pieChart)

                        p = (
                            Pie(init_opts=opts.InitOpts(width="900px", height="500px"))
                                .add(
                                "",
                                [list(z) for z in zip(pieChart['Name'], pieChart['values'])],
                                radius=["40%", "75%"],
                            )
                                # .set_colors(["green", "red", "orange", "purple"])

                                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}", font_size=20)

                                                 )
                                .render_embed()
                        )
                        components.html(p, width=900, height=500)
                        # l = (
                        #     Liquid()
                        #     .add('lq', [vlCoverage/100], center=["25%", "50%"])
                        #     .set_global_opts(
                        #         title_opts = opts.TitleOpts(title ='VL Coverage', pos_left='15%')
                        #     )

                        # )
                        # g = (
                        #     Liquid()
                        #     .add('lq', [suppressionRate/100],center=["80%", "50%"] )
                        #     .set_global_opts(
                        #         title_opts = opts.TitleOpts(title ='Supperession Rate', pos_left='70%')
                        #     )

                        # )
                        # grid = Grid().add(l, grid_opts=opts.GridOpts()).add(g, grid_opts=opts.GridOpts())
                        # grid.render_embed()

                        # components.html(grid.render_embed(), width=1000, height=500)
                        # with pi1:
                        #     components.html(l,width=1000, height=500)
                        # with pi2:
                        #     components.html(g,width=1000, height=500)

                if choice == 'Treatment New':

                    if data is not None:
                        placeholder.empty()

                        df['ARTStartDate'] = dateConverter(df.ARTStartDate)
                        dt1, dt2 = st.columns(2)
                        with dt1:
                            # start date
                            firstDate()
                            start_date = firstDate.start_date

                        with dt2:
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

                        with st.sidebar:
                            st.markdown('<br>',
                                        unsafe_allow_html=True)
                            facilities, lga, select_lgas = selectLga(lgas, state)

                        with st.sidebar:
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
                        with btn_download:
                            download(art_start, convert_df, key='btn1')

                        pieChartDisplay = st.empty()
                        with pieChartDisplay:

                            pieChart = pieChart_values(Current_TB_Status_count, cd4_count_result, ipt_screening,
                                                       pbs_count, tbDocumented_result_count, transferIn_count,
                                                       art_start_count)

                            p = pieChart_dsiplay(pieChart)

                            components.html(p, width=900, height=500)


                        if select_state:
                            txnewContainer.empty()
                            pieChartDisplay.empty()
                            tb_container.empty()
                            btn_download.empty()
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
                                pieChart = pieChart_values(Current_TB_Status_count, cd4_count_result, ipt_screening,
                                                           pbs_count, tbDocumented_result_count, transferIn_count,
                                                           tx_new_count)

                                p = pieChart_dsiplay(pieChart)

                                components.html(p, width=900, height=500)

                        if select_lgas:
                            txnewContainer.empty()
                            tb_container.empty()
                            btn_download.empty()
                            pieChartDisplay.empty()
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
                                pieChart = pieChart_values(Current_TB_Status_count, cd4_count_result, ipt_screening,
                                                           pbs_count, tbDocumented_result_count, transferIn_count,
                                                           tx_new_count)

                                p = pieChart_dsiplay(pieChart)
                                components.html(p, width=900, height=500)

                        if select_facilities:
                            txnewContainer.empty()
                            tb_container.empty()
                            btn_download.empty()
                            pieChartDisplay.empty()
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
                                pieChart = pieChart_values(Current_TB_Status_count, cd4_count_result, ipt_screening,
                                                           pbs_count, tbDocumented_result_count, transferIn_count,
                                                           tx_new_count)

                                p = pieChart_dsiplay(pieChart)
                                components.html(p, width=900, height=500)

            else:
                st.warning("Kindly Reload and Upload ART line list")

    # REPORT MODULES

    if selected == 'Reports':

        st.markdown('<p class="font">Reports Dashbooard✍</p>',
                    unsafe_allow_html=True)
        ########## FOR DISPLAYING THE CARDS##################
        weekly_display = st.container()

        placeholder = st.empty()
        if st.session_state.data is not None:
            report = placeholder.file_uploader(
                'Upload your Treatment Linelist here. Pls ART Linelist Only 🙏🙏🙏🙏', type=['csv'])
            placeholder.empty()
        else:
            report = placeholder.file_uploader(
                'Upload your Treatment Linelist here. Pls ART Linelist Only 🙏🙏🙏🙏', type=['csv'])

        if report is not None:
            placeholder.empty()

            @st.cache(allow_output_mutation=True)
            def load_data2():
                df = pd.read_csv(report, encoding='unicode_escape')

                return df

            dataVariable = load_data2()
            cleanDataSet(dataVariable)

            dataVariable['Pharmacy_LastPickupdate'] = dateConverter(dataVariable.Pharmacy_LastPickupdate)

            dataVariable['ARTStartDate'] = dateConverter(dataVariable.ARTStartDate)

            dataVariable['DateofCurrentViralLoad'] = dateConverter(dataVariable.DateofCurrentViralLoad)

            ##############END OF FUNCTION########################

            report_type = st.selectbox(
                'What would you like to Analyse?', reports)

            ##############&E Weekly Report########################
            if report_type == 'M&E Weekly Report':

                dt1, dt2 = st.columns(2)
                with dt1:
                    # start date
                    firstDate()
                    start_date = firstDate.start_date
                with dt2:
                    # end date
                    SecondDate()
                    end_date = SecondDate.end_date

                treatmentCurrent = tx_curr(dataVariable)
                treatmentCurrent = treatmentCurrent['CurrentARTStatus_Pharmacy'].count()

                art_start = artStart(dataVariable)
                art_start_count = art_start['PepID'].count()

                pharm_start = pharm()
                pharm_start_count = pharm_start['Pharmacy_LastPickupdate'].count(
                )

                dataVariable['Outcomes_Date'] = dateConverter(dataVariable.Outcomes_Date)
                outcomes_date = dataVariable.query('Outcomes_Date >= @start_date &  Outcomes_Date <= @end_date')
                outcomes_date = outcomes_date['Outcomes_Date'].count()

                dataVariable['LastPickupDateCal'] = pd.to_datetime(
                    dataVariable['LastPickupDateCal'])

                dataVariable = dataVariable.query('CurrentARTStatus_Pharmacy =="Active" ')

                # arvRefill = df['DaysOfARVRefill'].astype(int)

                def calMissedApp(
                        x):
                    return x['LastPickupDateCal'] + relativedelta(days=int(x['DaysOfARVRefill']))

                dataVariable['appointmentDate'] = dataVariable.apply(calMissedApp, axis=1)

                thisWeekMissedAppointment = dataVariable[(dataVariable['appointmentDate'] >= str(start_date)) &  # type: ignore
                                               (dataVariable['appointmentDate'] <= str(end_date))]  # type: ignore
                thisWeekMissedAppointment = thisWeekMissedAppointment['appointmentDate'].count(
                )

                ipt_screening = pharm_start['IPT_Screening_Date'].count()

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

            ######################### 'M&E Monthly Report ###########################
            if report_type == 'M&E Monthly Report':

                option = st.selectbox(
                    'Select Report Type',
                    ('', 'Clinic Attendance', 'Treatment New', 'VL Test Results',
                     'Viroloogically Suppressed', 'Adult 1st line',
                     'Adult 2nd line', 'Child 1st line', 'Child 2nd line'))

                dt1, dt2 = st.columns(2)

                if option == 'Clinic Attendance':

                    with dt1:
                        # start date
                        start_date = st.date_input(
                            "From", )
                    with dt2:
                        # end date
                        end_date = st.date_input(
                            "To", )

                    pharm_start = pharm()

                    pharm_start_count = pharm_start['Pharmacy_LastPickupdate'].count(
                    )

                    if pharm_start_count == 0:
                        pass

                    else:

                        female = pharm_start.query(
                            'Sex == "F" & CurrentARTStatus_Pharmacy =="Active" ')

                        f = female['Current_Age'].apply(condition)

                        #######MALE#############
                        male = pharm_start.query(
                            'Sex == "M" & CurrentARTStatus_Pharmacy =="Active" ')

                        m = male['Current_Age'].apply(condition)

                        # PREGNANT/BREASTFEEDING

                        pregnant = pharm_start.query(
                            'Sex == "F" & CurrentPregnancyStatus =="Breastfeeding" | CurrentPregnancyStatus =="Pregnant" ')

                        p = pregnant['Current_Age'].apply(condition)

                        st.subheader(
                            f'Attendance for the period of {start_date} to {end_date}')
                        # fin = pd.DataFrame(["female",d])
                        output()

                ######################### Treatment New ###########################
                if option == 'Treatment New':
                    with dt1:
                        # start date
                        start_date = st.date_input(
                            "From", )
                    with dt2:
                        # end date
                        end_date = st.date_input(
                            "To", )

                    art_start = artStart(dataVariable)

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

                    with dt1:
                        # start date
                        firstDate()

                    with dt2:
                        # end date
                        SecondDate()

                    art_start = dataVariable[(dataVariable['DateofCurrentViralLoad'] >= str(firstDate.start_date)) &  # type: ignore
                                   (dataVariable['DateofCurrentViralLoad'] <= str(SecondDate.end_date))]  # type: ignore

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
                if option == 'Viroloogically Suppressed':

                    with dt1:
                        # start date
                        firstDate()

                    with dt2:
                        # end date
                        SecondDate()

                        art_start = dataVariable[(dataVariable['DateofCurrentViralLoad'] >= str(firstDate.start_date)) &  # type: ignore
                                       (dataVariable['DateofCurrentViralLoad'] <= str(SecondDate.end_date))]  # type: ignore

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

                    pharm_start = dataVariable[(dataVariable['Pharmacy_LastPickupdate'] >= str(firstDate.start_date)) &  # type: ignore
                                     (dataVariable['Pharmacy_LastPickupdate'] <= str(SecondDate.end_date))]  # type: ignore

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

                        pharm_start = dataVariable[(dataVariable['Pharmacy_LastPickupdate'] >= str(firstDate.start_date)) &  # type: ignore
                                         (dataVariable['Pharmacy_LastPickupdate'] <= str(firstDate.end_date))]  # type: ignore

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

                        pharm_start = dataVariable[
                            (dataVariable['Pharmacy_LastPickupdate'] >= str(firstDate.start_date)) & (  # type: ignore
                                    dataVariable['Pharmacy_LastPickupdate'] <= str(SecondDate.end_date))]  # type: ignore

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

                        pharm_start = dataVariable[(dataVariable['Pharmacy_LastPickupdate'] >= str(firstDate.start_date)) &  # type: ignore
                                         (dataVariable['Pharmacy_LastPickupdate'] <= str(SecondDate.end_date))]  # type: ignore

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

    if selected == 'EMR-NDR':
        c1,c2,c3 = st.columns(3)
        ndrlogo = Image.open('NDR_Logo_Black.png')
        emrlogo = Image.open('openMrsLogo.png')
        c3.image(ndrlogo, width=50)
        c1.image(emrlogo, width=50, )
        
        st.markdown('<p class="font">EMR VS NDR</p>',
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
                df_emr = pd.read_csv(emr, encoding='unicode_escape')
                return df_emr
                cleanDataSet(df_emr)
            df_emr = load_data3()
        if ndr is not None:
            placeholder.empty()
            ndrholder.empty()
            @st.cache(allow_output_mutation=True)
            def load_data4():
                df_ndr = pd.read_csv(ndr, encoding='unicode_escape')
                return df_ndr
            df_ndr = load_data4()
            cleanDataSet(df_ndr)

            df_ndr

            # columns = ['ARTStartDate']
            # columns2 = [df.columns[12]]
            # if [columns] == [columns2]:
            #     cleanDataSet(df)



    if selected == 'Feedback':
        st.markdown('<p class="font">GOT A FEW MINUTES TO HELP ?</p>',
                    unsafe_allow_html=True)
        st.subheader('Help us improve!!!.')
        st.subheader(
            'Tell us what you think of our webapp. We welcome your feedback')



hide_streamlit_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            # header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """

st.markdown(hide_table_row_index, unsafe_allow_html=True)
if __name__ == '__main__':
    main()