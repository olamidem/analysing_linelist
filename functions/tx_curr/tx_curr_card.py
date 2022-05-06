import streamlit as st

def displayCard(countAdolescent, countAdult, countFemale, countMale, countPaed, treatmentCurrent_count):
    st.markdown(f"""
                                            <div class="container">
                                            <div class="card">
                                                <div class="title">
                                                Tx_Curr<span>{f'{treatmentCurrent_count:,d}'}</span>
                                                </div>
                                            </div>

                                            <div class="card">
                                                <div class="title">
                                                Male<span>{f'{countMale:,d}'}</span>
                                                </div>
                                            </div>

                                            <div class="card">
                                                <div class="title">
                                                Female<span>{f'{countFemale:,d}'}</span>
                                                </div>
                                            </div>

                                            <div class="card">
                                                <div class="title">
                                            Adult<span>{f'{countAdult:,d}'}</span>
                                                </div>
                                            </div>
                                            <div class="card">
                                                <div class="title">
                                             Adolescent<span>{f'{countAdolescent:,d}'}</span>
                                                </div>
                                            </div>
                                            <div class="card">
                                                <div class="title">
                                                Paediatrics<span>{f'{countPaed:,d}'}</span>
                                                </div>
                                                <div class="content">
                                            </div>
                                            </div>
                                            """, unsafe_allow_html=True)
