from dateutil.relativedelta import relativedelta

def missed_appointment_calculation(df):
    def calMissedApp(x):
        return x['LastPickupDateCal'] + relativedelta(days=int(x['DaysOfARVRefill']))

    df['appointmentDate'] = df.apply(calMissedApp, axis=1)
    df['appointmentDate'] = df['appointmentDate'].dt.date
    df['LastPickupDateCal'] = df['LastPickupDateCal'].dt.date
    df['Current_Age'] = df['Current_Age'].astype(int)
    df['DaysOfARVRefill'] = df['DaysOfARVRefill'].astype(int)
    df['IIT'] = df['appointmentDate'] + relativedelta(days=29)
