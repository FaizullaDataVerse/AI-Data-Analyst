import streamlit as st


def load_css():

    st.markdown(
        """
<style>

/* =====================================================
   GLOBAL
===================================================== */

.block-container{
    max-width:1450px;
    padding-top:1.5rem;
    padding-bottom:2rem;
}

.main{
    background:#0E1117;
}

/* Hide Streamlit default menu */

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

/* =====================================================
   HERO
===================================================== */

.hero{

    padding:35px;

    border-radius:20px;

    background:linear-gradient(
        135deg,
        #2F80ED,
        #6C63FF
    );

    color:white;

    margin-bottom:25px;

    box-shadow:0 10px 30px rgba(0,0,0,.25);

}

.hero h1{

    margin:0;

    font-size:42px;

    font-weight:700;

}

.hero p{

    margin-top:10px;

    opacity:.9;

    font-size:17px;

}

/* =====================================================
   DATASET CARD
===================================================== */

.dataset-card{

    background:#161B22;

    border-radius:18px;

    padding:20px;

    border:1px solid #2D333B;

    margin-bottom:20px;

}

/* =====================================================
   KPI CARD
===================================================== */

.kpi{

    background:#161B22;

    border-radius:18px;

    padding:20px;

    text-align:center;

    border:1px solid #2D333B;

    transition:.25s;

    min-height:120px;

}

.kpi:hover{

    transform:translateY(-4px);

    border-color:#4F8BF9;

    box-shadow:0 12px 25px rgba(79,139,249,.25);

}

.kpi h2{

    margin:10px 0;

    color:#4F8BF9;

    font-size:28px;

}

.kpi p{

    margin:0;

    color:#B5BAC1;

    font-size:15px;

}

/* =====================================================
   CHAT
===================================================== */

.stChatMessage{

    border-radius:18px;

    padding:12px;

}

.stChatMessage[data-testid="user"]{

    background:#1F2937;

}

.stChatMessage[data-testid="assistant"]{

    background:#161B22;

}

/* =====================================================
   BUTTONS
===================================================== */

.stButton>button{

    width:100%;

    border-radius:12px;

    border:none;

    background:#4F8BF9;

    color:white;

    font-weight:600;

    transition:.25s;

}

.stButton>button:hover{

    background:#3A73E8;

}

/* =====================================================
   CHAT INPUT
===================================================== */

.stChatInputContainer{

    border-radius:18px;

}

/* =====================================================
   TABS
===================================================== */

.stTabs [role="tab"]{

    border-radius:12px;

    font-size:16px;

    padding:12px 22px;

}

.stTabs [aria-selected="true"]{

    background:#4F8BF9;

    color:white;

}

/* =====================================================
   DATAFRAME
===================================================== */

[data-testid="stDataFrame"]{

    border-radius:15px;

    overflow:hidden;

    border:1px solid #2D333B;

}

/* =====================================================
   METRIC
===================================================== */

[data-testid="metric-container"]{

    background:#161B22;

    border:1px solid #2D333B;

    border-radius:16px;

    padding:15px;

}

/* =====================================================
   EXPANDER
===================================================== */

.streamlit-expanderHeader{

    font-size:18px;

    font-weight:600;

}

</style>
""",
        unsafe_allow_html=True,
    )