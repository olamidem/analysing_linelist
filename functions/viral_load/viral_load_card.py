import streamlit as st

def viral_load_display(documentedViralload, suppressedVl, suppressionRate, treatmentCurrent_count, vLEligibleCount,
                       vlCoverage):
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