import streamlit as st


def txNewDisplay(art_start_count, cd4CountCoverage, cd4_count, pbs, pbsCoverage, transferIn):
    st.markdown(f"""

                                        <div class="container">
                                        <div class="card">
                                            <div class="title">
                                            Tx_New<span>{f'{art_start_count:,d}'}</span>
                                            </div>
                                        </div>

                                        <div class="card">
                                            <div class="title">
                                            Trans IN<span>{f'{transferIn:,d}'}</span>
                                            </div>
                                        </div>

                                        <div class="card">
                                            <div class="title">
                                            PBS <span>{f'{pbs:,d}'}</span>
                                            </div>
                                        </div>

                                        <div class="card">
                                            <div class="title">
                                            PBS Coverage<span>{pbsCoverage}%</span>
                                            </div>
                                        </div>
                                        <div class="card">
                                            <div class="title">
                                            CD4 Count<span>{f'{cd4_count:,d}'}</span>
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
