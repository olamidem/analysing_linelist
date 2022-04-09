import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import date, datetime, timedelta
from streamlit_option_menu import option_menu


st.set_page_config(page_title="Report Dashbooard 💻", page_icon="📑", layout="wide",
                   initial_sidebar_state="auto",)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def main():

    activities = ['', 'Treatment Current',
                  'Treatment New', 'Pharmcay Reporting', 'HTS_POS', 'HTS_TXT']
    reports = ['', 'HI Weekly Report',
               'M&E Weekly Report', 'M&E Monthly Report']

    with st.sidebar:
        selected = option_menu(
            menu_title='Main Menu',  # required
            options=['Monitoring', 'Reports', 'Task', 'Feedback'],
            icons=['pie-chart-fill', 'book',
                   'list-task', 'chat-square-text-fill'],
            menu_icon='cast',
            default_index=0,
        )
    if selected == 'Monitoring':

        st.markdown('<p class="font">Monitoring Dashbooard💻</p>',
                    unsafe_allow_html=True)
############MONITORING MODULES#######################################

        coll1, coll2, coll3 = st.columns(3)
        all_card = st.container()

        data = st.file_uploader(
            'Upload your Treatment Linelist here. Pls ART Linelist Only 🙏🙏🙏🙏', type=['csv'])

        if data is not None:

            df = pd.read_csv(data)

            choice = st.selectbox(
                'What would you like to Analyse?', activities)

            if choice == 'Treatment Current':
                if choice is not None:

                    active = df.query('CurrentARTStatus_Pharmacy == "Active" ')
                    ltfu = df.query('CurrentARTStatus_Pharmacy == "LTFU" ')

                    treatmentCurrent = active['CurrentARTStatus_Pharmacy'].count(
                    )
                    interuptionInTreatment = ltfu['CurrentARTStatus_Pharmacy'].count(
                    )

    #######################ELIGIBLE ####################

                    df['Ref_Date'] = datetime.now().date()
                    df['ARTStartDate'] = pd.to_datetime(
                        df.ARTStartDate, format='%d/%m/%Y')

                    df['ARTStartDate'] = df['ARTStartDate'].dt.date
                    df['DaysOnart'] = (
                        df['Ref_Date'] - df['ARTStartDate']).dt.days

                    daysOnArt = df.query(
                        ' DaysOnart >= 180  & CurrentARTStatus_Pharmacy == "Active" ')
                    viralLoadEligible = daysOnArt['DaysOnart'].count()

                    # st.write(daysOnArt.reset_index(drop=True))
                    # st.write(daysOnArt['DaysOnart'].count())

####################### DOCUMENTED VL ####################
                    startDate = datetime.now().date()
                    endDate = datetime.now().date() + timedelta(days=-365)

                    daysOnArt['DateofCurrentViralLoad'] = pd.to_datetime(
                        daysOnArt.DateofCurrentViralLoad, format='%d/%m/%Y')
                    daysOnArt['DateofCurrentViralLoad'] = daysOnArt['DateofCurrentViralLoad'].dt.date

                    vl_documented = daysOnArt.query(
                        ' DateofCurrentViralLoad <= @startDate & DateofCurrentViralLoad >= @endDate')

                    documentedViralload = vl_documented['PepID'].count()

#######################SUPPRESSED VL ####################
                    suppressedVl = vl_documented.query(
                        'CurrentViralLoad < 1000')
                    suppressedVl = suppressedVl.CurrentViralLoad.count()

#######################SUPPRESSION RATE ####################
                    suppressionRate = (suppressedVl/documentedViralload) * 100
                    suppressionRate = suppressionRate.round(
                        2).astype(str) + "%"

#######################VL COVERAGE ####################
                    vlCoverage = (documentedViralload/viralLoadEligible) * 100
                    vlCoverage = vlCoverage.round(  # type: ignore
                        2).astype(str) + "%"  # type: ignore

                    outcomes = df.query(
                        'CurrentARTStatus_Pharmacy == "Active" & Outcomes != "" ')

                    with all_card:
                        st.markdown(f"""
                                    <div class="container">

                                    <div class="card">
                                        <div class="title">
                                        Active<span>{treatmentCurrent}</span>
                                        </div>
                                    </div>

                                    <div class="card">
                                        <div class="title">
                                        VL Eligible<span>{viralLoadEligible}</span>
                                        </div>
                                    </div>

                                    <div class="card">
                                        <div class="title">
                                        Documented VL<span>{documentedViralload}</span>
                                        </div>
                                    </div>

                                    <div class="card">
                                        <div class="title">
                                        Suppressed VL<span>{suppressedVl}</span>
                                        </div>
                                    </div>
                                    <div class="card">
                                        <div class="title">
                                        VL Coverage<span>{vlCoverage}</span>
                                        </div>
                                    </div>
                                    <div class="card">
                                        <div class="title">
                                        VL Suppression <span>{suppressionRate}</span>
                                        </div>
                                        <div class="content">
                                    </div>
                                    </div>
                                    """, unsafe_allow_html=True)

                    if outcomes['Outcomes'].count() == 0:
                        pass
                    else:
                        out = outcomes['Outcomes'].count()

                        st.markdown(f'<p class="caution">Dear User,<br> You have {out} Active Patients which they also have other Outcomes. See their Status below</p>',
                                    unsafe_allow_html=True)

                    active['Outcomes'] = active['Outcomes'].str.lower()
                    q = active.query(
                        ' Outcomes == "transferred out" | Outcomes == "death" | Outcomes == "discontinued Care" ')

                    col = q[['PepID', 'ARTStartDate', 'Sex',
                             'Pharmacy_LastPickupdate', 'DaysOfARVRefill', 'CurrentARTRegimen', 'CurrentARTStatus_Pharmacy', 'Outcomes', 'Outcomes_Date']]

                    index_no = col.reset_index(drop=True)
                    index_no

                pie_chart = df['CurrentARTStatus_Pharmacy'].value_counts()
                names = ['Active', 'LTFU']
                label = px.pie(values=pie_chart, names=names, hole=.3,
                               color_discrete_sequence=px.colors.sequential.RdBu)
                st.write(label)

            if choice == 'Treatment New':

                if data is not None:

                    df['ARTStartDate'] = pd.to_datetime(
                        df.ARTStartDate, format='%d/%m/%Y')

                    # df['ARTStartDate'] = df['ARTStartDate'].dt.strftime('%d/%m/%Y')
                    infer_datetime_format = True
                    # art_startdate = df['ARTStartDate'].to_list()
                    dt1, dt2 = st.columns(2)
                    with dt1:
                        # start date
                        start_date = st.date_input(
                            "From",)

                    with dt2:
                        # end date
                        end_date = st.date_input(
                            "To",)

                    art_start = df[(df['ARTStartDate'] >= str(start_date)) &  # type: ignore
                                   (df['ARTStartDate'] <= str(end_date))]  # type: ignore

                    art_start_count = art_start['IP'].count()

                    with coll1:
                        st.subheader('TX_NEW')
                        st.success(art_start_count)
                    with coll2:
                        st.subheader('TX_NEW')
                        st.success(art_start_count)
                    with coll3:
                        st.subheader('TX_NEW')
                        st.success(art_start_count)

                    # st.dataframe(art_start)
                    art_start['ARTStartDate'] = art_start['ARTStartDate'].dt.strftime(
                        '%d/%m/%Y')
                    info = art_start[['Sex', 'PepID',
                                      'ARTStartDate',
                                     'Pharmacy_LastPickupdate',
                                      'DaysOfARVRefill', 'CurrentARTRegimen', 'Current_Age', 'FirstCD4', 'CurrentINHReceived',
                                      'Current_TB_Status', 'PBS', 'IPT_Screening_Date', ]]

                    info_options = st.multiselect(
                        'Select Data to Analyze',
                        info.columns)
                    mask = art_start[info_options]
                    m = mask.reset_index(drop=True)
                    m

                    d = info.groupby("PepID").count()
                    st.write(d)

                    # info.value_counts()

                if choice == 'HTS_POS':
                    st.subheader('Hiv Test Service Positive')

                # if choice == 'HTS_TXT':
                #     st.subheader('All Hiv Test Service')

                # # st.write('start date:', start_date)
                # # st.write('end date:', end_date)
                # # st.sidebar.selectbox('select sate', s)
                # # st.sidebar.selectbox('select sate', e)


# REPORT MODULES
    if selected == 'Reports':

        st.markdown('<p class="font">Reports Dashbooard✍</p>',
                    unsafe_allow_html=True)

        report = st.file_uploader(
            'Upload your Treatment Linelist here. Pls ART Linelist Only 🙏🙏🙏🙏', type=['csv'])

        if report is not None:
            clinic = pd.read_csv(report)

            clinic['Pharmacy_LastPickupdate'] = pd.to_datetime(
                clinic.Pharmacy_LastPickupdate, format='%d/%m/%Y')

            clinic['ARTStartDate'] = pd.to_datetime(
                clinic.ARTStartDate, format='%d/%m/%Y')

            clinic['DateofCurrentViralLoad'] = pd.to_datetime(
                clinic.DateofCurrentViralLoad, format='%d/%m/%Y')

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
                    st.write(p.value_counts())

##############END OF FUNCTION########################

            report_type = st.selectbox(
                'What would you like to Analyse?', reports)

            if report_type == '':
                pass

            if report_type == 'M&E Monthly Report':

                option = st.selectbox(
                    'Select Report Type',
                    ('', 'Clinic Attendance', 'Treatment New', 'VL Test Results',
                     'Viroloogically Suppressed', 'Adult 1st line',
                     'Adult 2nd line', 'Child 1st line', 'Adult 2nd line'))

                dt1, dt2 = st.columns(2)

                if option == 'Clinic Attendance':

                    with dt1:
                        # start date
                        pharm_start_date = st.date_input(
                            "From",)
                    with dt2:
                        # end date
                        pharm_end_date = st.date_input(
                            "To",)

                        pharm_start = clinic[(clinic['Pharmacy_LastPickupdate'] >= str(pharm_start_date)) &  # type: ignore
                                             (clinic['Pharmacy_LastPickupdate'] <= str(pharm_end_date))]  # type: ignore

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
                            f'Clinic Attendance for the period of { pharm_start_date} to { pharm_end_date}')
                        # fin = pd.DataFrame(["female",d])
                        output()

                if option == 'Treatment New':

                    with dt1:
                        # start date
                        tx_start_date = st.date_input(
                            "From",)
                    with dt2:
                        # end date
                        tx_end_date = st.date_input(
                            "To",)

                        art_start = clinic[(clinic['ARTStartDate'] >= str(tx_start_date)) &  # type: ignore
                                           (clinic['ARTStartDate'] <= str(tx_end_date))]  # type: ignore

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
                            f'Treatment New for the period of { tx_start_date} to { tx_end_date}')
                        output()

#####################Viral load result@@###############################
                if option == 'VL Test Results':
                    with dt1:
                        # start date
                        vl_start_date = st.date_input(
                            "From",)
                    with dt2:
                        # end date
                        vl_end_date = st.date_input(
                            "To",)

                    art_start = clinic[(clinic['DateofCurrentViralLoad'] >= str(vl_start_date)) &  # type: ignore
                                       (clinic['DateofCurrentViralLoad'] <= str(vl_end_date))]  # type: ignore

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

                if option == 'Viroloogically Suppressed':

                    with dt1:
                        # start date
                        su_start_date = st.date_input(
                            "From",)
                    with dt2:
                        # end date
                        su_end_date = st.date_input(
                            "To",)

                        art_start = clinic[(clinic['DateofCurrentViralLoad'] >= str(su_start_date)) &  # type: ignore
                                           (clinic['DateofCurrentViralLoad'] <= str(su_end_date))]  # type: ignore

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

                if option == 'Adult 1st line':

                    with dt1:
                        # start date
                        adult_start_date = st.date_input(
                            "From",)
                    with dt2:
                        # end date
                        adult_end_date = st.date_input(
                            "To",)

                    pharm_start = clinic[(clinic['Pharmacy_LastPickupdate'] >= str(adult_start_date)) &  # type: ignore
                                         (clinic['Pharmacy_LastPickupdate'] <= str(adult_end_date))]  # type: ignore

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

                if option == 'Adult 2nd line':

                    with dt1:
                        # start date
                        sec_start_date = st.date_input(
                            "From",)
                    with dt2:
                        # end date
                        sec_end_date = st.date_input(
                            "To",)

                        pharm_start = clinic[(clinic['Pharmacy_LastPickupdate'] >= str(sec_start_date)) &  # type: ignore
                                             (clinic['Pharmacy_LastPickupdate'] <= str(sec_end_date))]  # type: ignore

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

                        pregnant = pharm_start.query(
                            'Sex == "F" & CurrentPregnancyStatus =="Breastfeeding" | CurrentPregnancyStatus =="Pregnant" & CurrentRegimenLine == "Adult 2nd line ARV regimen" | CurrentRegimenLine == "Child 2nd line ARV regimen"  ')

                        p = pregnant['Current_Age'].apply(condition)

                        # fin = pd.DataFrame(["female",d])
                        st.subheader('Adult 2nd Line ARV')
                        output()

                if option == 'Child 1st line':

                    with dt1:
                        # start date
                        child_start_date = st.date_input(
                            "From",)
                    with dt2:
                        # end date
                        child_end_date = st.date_input(
                            "To",)

                        pharm_start = clinic[(clinic['Pharmacy_LastPickupdate'] >= str(child_start_date)) & (
                            clinic['Pharmacy_LastPickupdate'] <= str(child_end_date))]  # type: ignore

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

                        # fin = pd.DataFrame(["female",d])
                        st.subheader('Child 1st Line ARV')
                        output()

                if option == 'Child 2nd line':

                    with dt1:
                        # start date
                        child2_start_date = st.date_input(
                            "From",)
                    with dt2:
                        # end date
                        child2_end_date = st.date_input(
                            "To",)

                        pharm_start = clinic[(clinic['Pharmacy_LastPickupdate'] >= str(child2_start_date)) &  # type: ignore
                                             (clinic['Pharmacy_LastPickupdate'] <= str(child2_end_date))]  # type: ignore

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

                        st.subheader('Child 2nd Line ARV')
                        output()

            if report_type == 'M&E Weekly Report':
                st.write(datetime.now())


if __name__ == '__main__':
    main()

hide_streamlit_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            # header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
