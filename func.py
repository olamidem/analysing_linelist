def tx_curr(dataSet):
    active = dataSet.query(
        'CurrentARTStatus_Pharmacy == "Active" & Outcomes == ""  ')
    return active
