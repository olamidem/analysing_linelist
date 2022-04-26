import streamlit as st
import locale
import numpy as np
import pandas as pd
from datetime import date, datetime, timedelta
from streamlit_option_menu import option_menu
from dateutil.relativedelta import relativedelta, MO
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Liquid, Grid
from pyecharts.globals import SymbolType
import streamlit.components.v1 as components

st.set_page_config(page_title="Report Dashbooard 💻", page_icon="📑", layout="wide",
                   initial_sidebar_state="auto", )

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def main():
    def condition(age):
        if age >= 5 and age <= 9:
            return "5 - 9"
        elif age >= 10 and age <= 14:
            return "10 - 14"
        elif age >= 15 and age <= 19:
            return "15 - 19"
        elif age >= 20 and age <= 24:
            return "20 - 24"
        elif age >= 25 and age <= 29:
            return "25 - 29"
        elif age >= 30 and age <= 34:
            return "30 - 34"
        elif age >= 35 and age <= 39:
            return "35 - 39"
        elif age >= 40 and age <= 44:
            return "40 - 44"
        elif age >= 45 and age <= 49:
            return "45 - 49"
        elif age >= 50:
            return "50+"
        else:
            female['Current_Age'].isnull()
            return "1 - 4"

    ############OUTPUT FUNCTION###############################
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

    def tx_curr(dataSet):
        active = dataSet.query(
            'CurrentARTStatus_Pharmacy == "Active" & Outcomes == ""  ')
        return active

    def artStart():
        return df[(df['ARTStartDate'] >= str(start_date)) &  # type: ignore
                  (df['ARTStartDate'] <= str(end_date)) &  # type: ignore
                  (df['TI'] != 'YES')]  # type: ignore

    def trans_in():
        return df[(df['ARTStartDate'] >= str(start_date)) &  # type: ignore
                  (df['ARTStartDate'] <= str(end_date)) &  # type: ignore
                  (df['TI'] == 'YES')]  # type: ignore

    def pharm():
        pharm_start = df[(df['Pharmacy_LastPickupdate'] >= str(start_date)) &  # type: ignore
                         (df['Pharmacy_LastPickupdate'] <= str(end_date))]  # type: ignore
        return pharm_start

    def outComes():
        outcomes_date = df[(df['Outcomes_Date'] >= str(start_date)) &  # type: ignore
                           (df['Outcomes_Date'] <= str(end_date))]  # type: ignore
        outcomes_date = outcomes_date['Outcomes_Date'].count()
        return outcomes_date

    def dateConverter(dateColumn):
        return pd.to_datetime(dateColumn, format="%d/%m/%Y", errors='ignore')

    ######################### DATE FUNCTION###############################
    def firstDate():
        firstDate.start_date = st.date_input("From", )

    def SecondDate():
        SecondDate.end_date = st.date_input("To", )

    def cleanDataSet():
        df.replace(to_replace='\\\\N', value='')
        df['Outcomes'] = df['Outcomes'].replace(to_replace=np.nan, value="")
        df['PhoneNo'] = df['PhoneNo'].replace(to_replace=['null', 'NONE', 'NIL', 'NIL.'], value="")
        df['ARTStartDate'] = df['ARTStartDate'].replace(to_replace=np.nan, value="01/01/1900")
        df['DateofCurrentViralLoad'] = df['DateofCurrentViralLoad'].replace(to_replace=np.nan, value="01/01/1900")
        df['PhoneNo'] = df['PhoneNo'].astype(str)

    def fileName(name):
        fileName = data.name
        st.header(fileName)

    ###### To set the locale environment to Default OS location################
    locale.setlocale(locale.LC_ALL, '')

    activities = ['', 'Treatment Current', 'Treatment New', 'Viral-Load Cascade',
                  'Clinical Report']
    reports = ['', 'HI Weekly Report',
               'M&E Weekly Report', 'M&E Monthly Report']

    with st.sidebar:
        selected = option_menu(
            menu_title='DashBoard',  # required
            options=['Monitoring', 'Reports', 'EMR-NDR', 'Feedback'],
            icons=['pie-chart-fill', 'book',
                   'list-task', 'chat-square-text-fill'],
            menu_icon='cast',
            default_index=0,
        )
    if selected == 'Monitoring':

        st.markdown('<p class="font">Monitoring Dashboard💻</p>',
                    unsafe_allow_html=True)
        ############MONITORING MODULES#######################################
        montoring = st.container()
        with montoring:
            all_card = st.container()
            ####################### TREATMENT NEW CONTAINER###################
            txnewContainer = st.container()
            placeholder = st.empty()

        data = placeholder.file_uploader(
            'Upload your Treatment Linelist here. Pls ART Linelist Only 🙏🙏🙏🙏', type=['csv'])
        st.session_state.data = data
        if data is not None:
            if data not in st.session_state:
                st.session_state.data = data.name
            placeholder.empty()
            fileName(data)

            @st.cache(allow_output_mutation=True)
            def load_data1():
                df = pd.read_csv(data, encoding='unicode_escape')
                return df

            df = load_data1()
            cleanDataSet()

            choice = st.selectbox(
                'What would you like to Analyse?', activities)

            if choice == 'Treatment Current':
                if choice is not None:
                    placeholder.empty()
                    dt1, dt2 = st.columns(2)
                    treatmentCurrent = tx_curr(df)
                    treatmentCurrent_count = treatmentCurrent['CurrentARTStatus_Pharmacy'].count()

                    tx_curr_male = treatmentCurrent.query('Sex == "M" ')
                    countMale = tx_curr_male['Sex'].count()

                    tx_curr_female = treatmentCurrent.query('Sex == "F" ')
                    countFemale = tx_curr_female['Sex'].count()

                    # st.write(firstDate.start_date, SecondDate.end_date)
                    with all_card:
                        st.markdown(f"""
                                        <div class="container">
                                        <div class="card">
                                            <div class="title">
                                            Tx_Curr<span>{"{0:n}".format(treatmentCurrent_count)}</span>
                                            </div>
                                        </div>

                                        <div class="card">
                                            <div class="title">
                                            Male<span>{"{0:n}".format(countMale)}</span>
                                            </div>
                                        </div>

                                        <div class="card">
                                            <div class="title">
                                            Female<span>{"{0:n}".format(countFemale)}</span>
                                            </div>
                                        </div>

                                        <div class="card">
                                            <div class="title">
                                        Adult<span>{0}</span>
                                            </div>
                                        </div>
                                        <div class="card">
                                            <div class="title">
                                         Adolescent<span>{0}</span>
                                            </div>
                                        </div>
                                        <div class="card">
                                            <div class="title">
                                            Paed<span>{0}</span>
                                            </div>
                                            <div class="content">
                                        </div>
                                        </div>
                                        """, unsafe_allow_html=True)

                    filterByState = st.checkbox('Filter by State')
                    states = df['State'].unique()
                    col1, col2, col3 = st.columns(3)

                    if filterByState:
                        with col1:
                            states = st.multiselect(
                                'What are your favorite colors',
                                states, key='states'
                            )
                            state = df.query('State == @states')
                            lgas = state['LGA'].unique()
                            st.write(state)

                        with col2:
                            lgas = st.multiselect(
                                'What are your favorite colors',
                                lgas, key='lgas'
                            )
                            lgas = state.query('LGA == @lgas')
                            facilities = lgas['FacilityName'].unique()
                            st.write(lgas)

                        with col3:
                            facilities = st.multiselect(
                                'What are your favorite colors',
                                facilities, key='facilities'
                            )
                            facilities = state.query('FacilityName == @facilities')
                            st.write(facilities)

            if choice == 'Viral-Load Cascade':
                if choice is not None:
                    report_date = st.date_input("Select your reporting date", )
                    treatmentCurrent = tx_curr(df)
                    treatmentCurrent = treatmentCurrent['CurrentARTStatus_Pharmacy'].count()

                    #######################ELIGIBLE ####################
                    df = df.query('CurrentARTStatus_Pharmacy == "Active"  & ARTStartDate != "" ')
                    df['Ref_Date'] = report_date

                    df['ARTStartDate'] = dateConverter(df['ARTStartDate'])

                    df['ARTStartDate'] = df['ARTStartDate'].dt.date
                    df['DaysOnart'] = (
                            df['Ref_Date'] - df['ARTStartDate']).dt.days

                    def viralLoadEligible(dataSet):
                        return dataSet.query(
                            ' DaysOnart >= 180  & CurrentARTStatus_Pharmacy == "Active" & Outcomes == "" ')

                    vLEligible = viralLoadEligible(df)
                    vLEligibleCount = vLEligible['DaysOnart'].count()

                    ####################### DOCUMENTED VL ####################
                    startDate = report_date
                    endDate = startDate + timedelta(days=-364)  # type: ignore
                    daysOnArt = viralLoadEligible(df)
                    daysOnArt['DateofCurrentViralLoad'] = dateConverter(daysOnArt.DateofCurrentViralLoad)

                    daysOnArt['DateofCurrentViralLoad'] = daysOnArt['DateofCurrentViralLoad']
                    vl_documented = daysOnArt.query(
                        ' DateofCurrentViralLoad <= @startDate & DateofCurrentViralLoad >= @endDate')
                    documentedViralload = vl_documented['PepID'].count()

                    # #######################SUPPRESSED VL ####################
                    vl_documented['CurrentViralLoad'] = vl_documented['CurrentViralLoad'].astype(float)
                    suppressedVl = vl_documented.query(
                        'CurrentViralLoad < 1000')
                    suppressedVl = suppressedVl.CurrentViralLoad.count()

                    # #######################SUPPRESSION RATE ####################
                    suppressionRate = ((suppressedVl / documentedViralload) * 100).round()

                    # #######################VL COVERAGE ####################
                    vlCoverage = ((documentedViralload / vLEligibleCount) * 100).round()

                    # # #######################FILTER BY STATE####################
                    # col1, col2, col3, filterByState, states = filterBY(df)
                    #
                    # if filterByState:
                    #     with col1:
                    #         lgas, state = chooseState(df, states)
                    #     with col2:
                    #         facilities, lgas = chooseLga(lgas, state)
                    #     with col3:
                    #         facilities = chooseFacility(facilities, state)
                    #
                    #     #####State Treatment Current###########
                    #     stateTxCurr = tx_curr(state)
                    #     stateTxCurr = stateTxCurr['State'].value_counts()
                    #     st.write(stateTxCurr)
                    #
                    #     #####State viralLoadEligible###########
                    #     stateEligible = viralLoadEligible(state)
                    #     stateEligible = stateEligible['State'].value_counts()
                    #     st.write(stateEligible)
                    #
                    #     ###### LGA's Treatment Current#####
                    #     lgaTreatmentCurrent = tx_curr(lgas)
                    #     lgaTreatmentCurrent = lgaTreatmentCurrent['LGA'].value_counts()
                    #     st.write(lgaTreatmentCurrent)
                    #
                    #     #####lGA's Eligible###########
                    #     lgasEligible = viralLoadEligible(lgas)
                    #     lgasEligible = lgasEligible['LGA'].value_counts()
                    #     st.write(lgasEligible)
                    #
                    #     txCurrent = tx_curr(facilities)
                    #     txCurrentByState = txCurrent['FacilityName'].value_counts()
                    #     st.write(txCurrentByState)
                    #     #####State facilityEligible###########
                    #     facilityEligible = viralLoadEligible(facilities)
                    #     facilityEligible = facilityEligible['FacilityName'].value_counts()
                    #     st.write(facilityEligible)

                    with all_card:
                        st.markdown(f"""
                                        <div class="container">
                                        <div class="card">
                                            <div class="title">
                                            Tx_Curr<span>{"{0:n}".format(treatmentCurrent)}</span>
                                            </div>
                                        </div>

                                        <div class="card">
                                            <div class="title">
                                            VL Eligible<span>{"{0:n}".format(vLEligibleCount)}</span>
                                            </div>
                                        </div>

                                        <div class="card">
                                            <div class="title">
                                            Documented VL<span>{"{0:n}".format(documentedViralload)}</span>
                                            </div>
                                        </div>

                                        <div class="card">
                                            <div class="title">
                                            Suppressed VL<span>{"{0:n}".format(suppressedVl)}</span>
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
                                            <div class="content">
                                        </div>
                                        </div>
                                        """, unsafe_allow_html=True)

                    pieChart = {'Name': ["TX_CURR", "Eligible", "Documented", "Suppressed"],
                                'values': [treatmentCurrent, vLEligibleCount, documentedViralload, suppressedVl]}
                    pieChart = pd.DataFrame(pieChart)

                    p = (
                        Pie(init_opts=opts.InitOpts(width="1200px", height="800px"))
                            .add(
                            "",
                            [list(z) for z in zip(pieChart['Name'], pieChart['values'])],
                            radius=["40%", "75%"],
                        )
                            .set_colors(["green", "red", "orange", "purple"])

                            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}", font_size=20)

                                             )
                            .render_embed()
                    )
                    components.html(p, width=1200, height=800)
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

                    art_start = artStart()
                    art_start_count = art_start['PepID'].count()

                    cd4_count = art_start.query('FirstCD4 != "" ')
                    cd4_count = cd4_count['FirstCD4'].count()
                    cd4CountCoverage = ((cd4_count / art_start_count) * 100).round()

                    pbs = art_start.query('PBS == "Yes" ')
                    pbs = pbs['PBS'].count()
                    pbsCoverage = ((pbs / art_start_count) * 100).round()

                    transferIn = trans_in()
                    transferIn = transferIn['TI'].count()

                    with txnewContainer:
                        st.markdown(f"""
                                        
                                        <div class="container">
                                        <div class="card">
                                            <div class="title">
                                            Tx_New<span>{art_start_count}</span>
                                            </div>
                                        </div>

                                        <div class="card">
                                            <div class="title">
                                            Trans IN<span>{transferIn}</span>
                                            </div>
                                        </div>

                                        <div class="card">
                                            <div class="title">
                                            PBS <span>{pbs}</span>
                                            </div>
                                        </div>

                                        <div class="card">
                                            <div class="title">
                                            PBS Coverage<span>{pbsCoverage}%</span>
                                            </div>
                                        </div>
                                        <div class="card">
                                            <div class="title">
                                            CD4 Count<span>{cd4_count}</span>
                                            </div>
                                        </div>
                                        <div class="card">
                                            <div class="title">
                                            CD4 Coverage
                                             <span>{cd4CountCoverage}%</span>
                                            </div>
                                            <div class="content">
                                        </div>
                                        </div>
                                        """, unsafe_allow_html=True)
                    # col1, col2, col3, filterByState, states = filterBY(df)
                    #
                    # if filterByState:
                    #     with col1:
                    #         lgas, state = chooseState(df, states)
                    #         st.write(state['State'].value_counts())
                    #     with col2:
                    #         facilities, lgas = chooseLga(lgas, state)
                    #     with col3:
                    #         facilities = chooseFacility(facilities, state)
    # REPORT MODULES

    if selected == 'Reports':

        st.markdown('<p class="font">Reports Dashbooard✍</p>',
                    unsafe_allow_html=True)
        ########## FOR DISPLAYING THE CARDS##################
        weekly_display = st.container()

        placeholder = st.empty()
        if st.session_state.data is not None:
            st.header(st.session_state.data)

            report = placeholder.file_uploader(
                'Upload your Treatment Linelist here. Pls ART Linelist Only 🙏🙏🙏🙏', type=['csv'])
            placeholder.empty()
        else:
            report = placeholder.file_uploader(
                'Upload your Treatment Linelist here. Pls ART Linelist Only 🙏🙏🙏🙏', type=['csv'])

        if report is not None:
            @st.cache(allow_output_mutation=True)
            def load_data2():
                df = pd.read_csv(report, encoding='unicode_escape')

                return df

            df = load_data2()
            cleanDataSet()

            df['Pharmacy_LastPickupdate'] = dateConverter(df.Pharmacy_LastPickupdate)

            df['ARTStartDate'] = dateConverter(df.ARTStartDate)

            df['DateofCurrentViralLoad'] = dateConverter(df.DateofCurrentViralLoad)

            ##############END OF FUNCTION########################

            report_type = st.selectbox(
                'What would you like to Analyse?', reports)

            ##############&E Weekly Report########################
            if report_type == 'M&E Weekly Report':

                dt1, dt2 = st.columns(2)
                with dt1:
                    # start date
                    start_date = firstDate()
                    start_date = firstDate.start_date
                with dt2:
                    # end date
                    end_date = SecondDate()
                    end_date = SecondDate.end_date

                treatmentCurrent = tx_curr(df)
                treatmentCurrent = treatmentCurrent['CurrentARTStatus_Pharmacy'].count()
                art_start = artStart()

                art_start_count = art_start['PepID'].count()
                pharm_start = pharm()

                pharm_start_count = pharm_start['Pharmacy_LastPickupdate'].count(
                )

                outcomes_date = outComes()
                placeholder.empty()

                df['LastPickupDateCal'] = pd.to_datetime(
                    df['LastPickupDateCal'])

                df = df.query('CurrentARTStatus_Pharmacy =="Active" ')

                # arvRefill = df['DaysOfARVRefill'].astype(int)

                def calMissedApp(
                        x):
                    return x['LastPickupDateCal'] + relativedelta(days=int(x['DaysOfARVRefill']))

                df['appointmentDate'] = df.apply(calMissedApp, axis=1)

                thisWeekMissedAppointment = df[(df['appointmentDate'] >= str(start_date)) &  # type: ignore
                                               (df['appointmentDate'] <= str(end_date))]  # type: ignore
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

                    art_start = artStart()

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

                    art_start = df[(df['DateofCurrentViralLoad'] >= str(firstDate.start_date)) &  # type: ignore
                                   (df['DateofCurrentViralLoad'] <= str(SecondDate.end_date))]  # type: ignore

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

                        art_start = df[(df['DateofCurrentViralLoad'] >= str(firstDate.start_date)) &  # type: ignore
                                       (df['DateofCurrentViralLoad'] <= str(SecondDate.end_date))]  # type: ignore

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

                    pharm_start = df[(df['Pharmacy_LastPickupdate'] >= str(firstDate.start_date)) &  # type: ignore
                                     (df['Pharmacy_LastPickupdate'] <= str(SecondDate.end_date))]  # type: ignore

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

                        pharm_start = df[(df['Pharmacy_LastPickupdate'] >= str(firstDate.start_date)) &  # type: ignore
                                         (df['Pharmacy_LastPickupdate'] <= str(firstDate.end_date))]  # type: ignore

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

                        pharm_start = df[
                            (df['Pharmacy_LastPickupdate'] >= str(firstDate.start_date)) & (  # type: ignore
                                    df['Pharmacy_LastPickupdate'] <= str(SecondDate.end_date))]  # type: ignore

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

                        pharm_start = df[(df['Pharmacy_LastPickupdate'] >= str(firstDate.start_date)) &  # type: ignore
                                         (df['Pharmacy_LastPickupdate'] <= str(SecondDate.end_date))]  # type: ignore

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
        emr = st.file_uploader(
            'STEP 1: UPLOAD EMR LINELIST 🙏🙏🙏🙏', type=['csv'])

        ndr = st.file_uploader(
            'STEP 2: UPLOAD NDR LINELIST 🙏🙏🙏🙏', type=['csv'])

    # Replace the placeholder with some text:
    # placeholder.text("Hello")

    # # Replace the text with a chart:
    # placeholder.line_chart({"data": [1, 5, 2, 6]})

    # # Replace the chart with several elements:
    # with placeholder.container():
    #     st.write("This is one element")
    #     st.write("This is another")

    # # Clear all those elements:

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
if __name__ == '__main__':
    main()
