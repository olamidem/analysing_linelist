import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import date, datetime, timedelta
from streamlit_option_menu import option_menu
from dateutil.relativedelta import relativedelta, MO
from pyecharts import options as opts
from pyecharts.charts import Bar,Pie,Liquid,Grid
from pyecharts.globals import SymbolType
import streamlit.components.v1 as components


st.set_page_config(page_title="Report Dashbooard 💻", page_icon="📑", layout="wide",
                   initial_sidebar_state="auto",)

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

    def tx_curr():
        active = df.query(
            'CurrentARTStatus_Pharmacy == "Active" & Outcomes == ""  ')
        return active

    def count_active():
        treatmentCurrent = active['CurrentARTStatus_Pharmacy'].count(
        )
        return treatmentCurrent

    def artStart():
        art_start = df[(df['ARTStartDate'] >= str(start_date)) &  # type: ignore
                       (df['ARTStartDate'] <= str(end_date))]  # type: ignore
        return art_start

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
        return pd.to_datetime(dateColumn,format="%d/%m/%Y", errors = 'ignore')
    
######################### DATE FUNCTION###############################
    def firstDate():
        firstDate.start_date = st.date_input( "From",)

    def SecondDate():
        SecondDate.end_date = st.date_input("To",)
    
    def cleanDataSet():
        df.replace(to_replace ='\\\\N' , value= '')
        df['Outcomes'] = df['Outcomes'].replace(to_replace= np.nan, value= "")
        df['PhoneNo'] =  df['PhoneNo'].replace(to_replace= ['null','NONE','NIL','NIL.'], value= "")
        df['ARTStartDate'] = df['ARTStartDate'].replace(to_replace= np.nan, value= "01/01/1900")
        df['DateofCurrentViralLoad'] = df['DateofCurrentViralLoad'].replace(to_replace= np.nan, value= "01/01/1900")
    def fileName(name):
        fileName = data.name
        st.header(fileName)               


    activities = ['', 'Treatment Current', 'Treatment New', 'Treatment PVLS',
                  'Pharmcay Reporting']
    reports = ['', 'HI Weekly Report',
               'M&E Weekly Report', 'M&E Monthly Report']

    with st.sidebar:
        selected = option_menu(
            menu_title='Main Menu',  # required
            options=['Monitoring', 'Reports', 'EMR-NDR', 'Feedback'],
            icons=['pie-chart-fill', 'book',
                   'list-task', 'chat-square-text-fill'],
            menu_icon='cast',
            default_index=0,
        )
    if selected == 'Monitoring':

        st.markdown('<p class="font">Monitoring Dashbooard💻</p>',
                    unsafe_allow_html=True)
############MONITORING MODULES#######################################
        montoring = st.container()
        with montoring:
            all_card = st.container()
            ####################### TREATMENT NEW CONTAINER###################
            txnewContainer = st.container()
            placeholder =st.empty()
            
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
                df = pd.read_csv(data, encoding = 'unicode_escape')
                return df
                
            df = load_data1() 
                
            cleanDataSet()
                
            choice = st.selectbox(
                    'What would you like to Analyse?', activities)
                
            if choice == 'Treatment Current':
                if choice is not None:
                    active = tx_curr()
                    treatmentCurrent = count_active()
                        
        #######################ELIGIBLE ####################
                    df = df.query('CurrentARTStatus_Pharmacy == "Active"  & ARTStartDate != ""')
                    df['Ref_Date'] = datetime.now().date()
                        
                    df['ARTStartDate'] = dateConverter(df['ARTStartDate'])
                        
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
                    endDate = datetime.now().date() + timedelta(days=-364)

                    daysOnArt['DateofCurrentViralLoad'] = dateConverter(daysOnArt.DateofCurrentViralLoad)
                        
                    daysOnArt['DateofCurrentViralLoad'] = daysOnArt['DateofCurrentViralLoad']
                    vl_documented = daysOnArt.query(
                            ' DateofCurrentViralLoad <= @startDate & DateofCurrentViralLoad >= @endDate')
                    col = vl_documented 
                    index_no = col.reset_index(drop=True)
                        
                    documentedViralload = vl_documented['PepID'].count()

    #######################SUPPRESSED VL ####################
                    vl_documented['CurrentViralLoad'] = vl_documented['CurrentViralLoad'].astype(float)
                    suppressedVl = vl_documented.query(
                            'CurrentViralLoad < 1000')
                    suppressedVl = suppressedVl.CurrentViralLoad.count()

    #######################SUPPRESSION RATE ####################
                    suppressionRate = ( suppressedVl/documentedViralload) * 100
                    suppressionRate = suppressionRate.round(2)

    #######################VL COVERAGE ####################
                    vlCoverage = (documentedViralload /viralLoadEligible) * 100
                    vlCoverage = vlCoverage.round(2) # type: ignore
    
    #######################END VL COVERAGE ####################
                        
    #######################FILTER BY STATE####################
                        
                    states = df['State'].unique()
                    filterByState = st.checkbox('Filter by State')
                    col1,col2,col3= st.columns(3)
                        
                    if filterByState:
                        with col1:
                            states = st.selectbox('What would you like to Analyse?', states)
                            state = df.query('State == @states')
                            lgas = state['LGA'].unique()
                        with col2:
                            lgas = st.selectbox('What would you like to Analyse?', lgas)
                            facility = state.query('LGA == @lgas')
                            facilities = facility['FacilityName'].unique()
                        with col3:
                            facilities = st.selectbox('What would you like to Analyse?', facilities)
                            facilities = state.query('FacilityName == @facilities')
                            
                            
                        def txCurr():
                            return facilities.query('CurrentARTStatus_Pharmacy == "Active" & Outcomes == "" ')
                            
                        def state_txCurr():
                            return state.query('CurrentARTStatus_Pharmacy == "Active" & Outcomes == "" ')
                            
                        stateTxCurr = state_txCurr()
                        stateTxCurr = stateTxCurr['State'].value_counts()
                        stateTxCurr
                            
                        txCurrent = txCurr()
                        txCurrentByState = txCurrent['State'].value_counts()
                        txCurrentByState
                        txCurrentByFacilities = txCurrent['FacilityName'].value_counts()
                        txCurrentByFacilities    
                            
                            
                        #     pass
                        outcomes = df.query(
                            'CurrentARTStatus_Pharmacy == "Active" & Outcomes != "" ')

                    with all_card:
                        st.markdown(f"""
                                        <marquee><h4>Below shown here use Date as of today</h4></marquee>
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
                            
                        
                    pieChart = {'Name':["TX_CURR", "Eligible", "Documented", "Suppressed"], 
                              'values':[treatmentCurrent, viralLoadEligible,documentedViralload,suppressedVl]}
                    pieChart = pd.DataFrame(pieChart)
                        
        
                    p = (
                            Pie(init_opts=opts.InitOpts(width="1200px", height="800px"))
                                .add(
                                    "",
                                    [list(z) for z in zip(pieChart['Name'],pieChart['values'] )],
                                    radius=["40%", "75%"],
                                )
                                .set_colors([ "green", "red", "orange", "purple"])
                                
                                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}", font_size=20)
                                
                                )
                                .render_embed()
                            )
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
                        
                    components.html(p, width=1200, height=800)
                        # components.html(grid.render_embed(), width=1000, height=500)
                        # with pi1:
                        #     components.html(l,width=1000, height=500)
                        # with pi2:
                        #     components.html(g,width=1000, height=500)
                        
                        
                      
                if choice == 'Treatment New':

                    if data is not None:
                        placeholder.empty()

                        df['ARTStartDate'] = pd.to_datetime(
                            df.ARTStartDate)

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
                            
                        art_start = artStart()
                        art_start_count = art_start['PepID'].count()
                        pbs = art_start.query('PBS == "Yes" ')
                        pbs = pbs['PBS'].count()

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
                                            PBS<span>{pbs}</span>
                                            </div>
                                        </div>

                                        <div class="card">
                                            <div class="title">
                                            Hold<span>1</span>
                                            </div>
                                        </div>

                                        <div class="card">
                                            <div class="title">
                                            Hold<span>1</span>
                                            </div>
                                        </div>
                                        <div class="card">
                                            <div class="title">
                                            Hold<span>1</span>
                                            </div>
                                        </div>
                                        <div class="card">
                                            <div class="title">
                                            Hold <span>1</span>
                                            </div>
                                            <div class="content">
                                        </div>
                                        </div>
                                        """, unsafe_allow_html=True)

                    
                if choice == 'Treatment PVLS':
                    if choice is not None:
                        placeholder.empty()
                        dt1, dt2 = st.columns(2)
                        df['DateofCurrentViralLoad'] = pd.to_datetime(df.DateofCurrentViralLoad, format='%d/%m/%Y')
                        
                        with dt1:
                            # start date
                            firstDate()
            
                        with dt2:
                            # end date
                            SecondDate()
                            
                        st.write(firstDate.start_date,SecondDate.end_date)

                        treatmentPvls = df.query('DateofCurrentViralLoad >= @firstDate.start_date &  DateofCurrentViralLoad <= @SecondDate.end_date ')
                        treatmentPvls = treatmentPvls['DateofCurrentViralLoad'].count()
                        st.info(treatmentPvls)
        

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
                df = pd.read_csv(report, encoding = 'unicode_escape')
                
                return df
            df = load_data2() 
            cleanDataSet()
                
            df['Pharmacy_LastPickupdate'] = pd.to_datetime(
                df.Pharmacy_LastPickupdate)

            df['ARTStartDate'] = pd.to_datetime(
                df.ARTStartDate)

            df['DateofCurrentViralLoad'] = pd.to_datetime(
                df.DateofCurrentViralLoad)


##############END OF FUNCTION########################

            report_type = st.selectbox(
                'What would you like to Analyse?', reports)

##############&E Weekly Report########################
            if report_type == 'M&E Weekly Report':
            
                dt1, dt2 = st.columns(2)
                with dt1:
                 # start date
                    start_date = st.date_input(
                        "From",)
                with dt2:
                    # end date
                    end_date = st.date_input(
                        "To",)
                

                active = tx_curr()
                treatmentCurrent = count_active()

                treatmentCurrent = count_active()

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
                    x): return x['LastPickupDateCal'] + relativedelta(days=int(x['DaysOfARVRefill']))
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
                            "From",)
                    with dt2:
                        # end date
                        end_date = st.date_input(
                            "To",)

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
                            f'Attendance for the period of { start_date} to { end_date}')
                        # fin = pd.DataFrame(["female",d])
                        output()

######################### Treatment New ###########################
                if option == 'Treatment New':
                    with dt1:
                     # start date
                        start_date = st.date_input(
                            "From",)
                    with dt2:
                        # end date
                        end_date = st.date_input(
                            "To",)

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
                            f'Treatment New for the period of { start_date} to { end_date}')
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

                        pharm_start = df[(df['Pharmacy_LastPickupdate'] >= str(firstDate.start_date)) & (  # type: ignore
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


hide_streamlit_style ="""
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            # header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style,unsafe_allow_html=True)
if __name__ == '__main__':
    main()

