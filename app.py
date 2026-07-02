import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Expense Management Dashboard",page_icon="💰",layout="wide")

st.markdown("""
<style>
.main{
background:#f5f7fb;
}
            
h1{
color:#1e3a8a;
text-align:center;
font-weight:700;
font-size:42px;
}
            
[data-testid="stSidebar"]{
background:linear-gradient(180deg,#0d4674,#2b73c4);
}

[data-testid="stSidebar"] *{
color:white;
}
            
[data-testid="metric-container"]{
background:white;
border-radius:18px;
padding:20px;
border-left:8px solid #2b73c4;
box-shadow:0px 8px 25px rgba(0,0,0,.12);
transition:0.3s;
}

[data-testid="metric-container"]:hover{
transform:translateY(-6px);
box-shadow:0px 12px 30px rgba(37,99,235,.3);
}
            
.stDataFrame{
border-radius:10px;
}
            
.stButton>button{
background:#2b73c4;
color:white;
border:none;
border-radius:10px;
padding:10px 20px;
font-weight:bold;
}

.stButton>button:hover{
background:#1d8dd8;
}

.stDownloadButton>button{
background:#1d8dd8;
color:white;
border:none;
border-radius:10px;
padding:10px 20px;
font-weight:bold;
}

.stDownloadButton>button:hover{
background:#6facd5;
}
            
.stSelectbox>div>div{
border-radius:10px;
}

.stMultiSelect>div>div{
border-radius:10px;
}

.stSlider{
padding-top:10px;
}

hr{
border:1px solid #dbeafe;
}

</style>
""",unsafe_allow_html=True)

st.markdown("""
<h1>💰 Expense Management Dashboard</h1>
<p style='text-align:center;color:#64748b;font-size:18px;'>
Track, analyze and visualize your expenses with ease.
</p>
""", unsafe_allow_html=True)


d=pd.read_csv("expense.csv")

st.sidebar.header("Filters")

c=st.sidebar.multiselect(
"Category",
sorted(d["cat"].unique()),
default=sorted(d["cat"].unique())
)

p=st.sidebar.multiselect(
"Payment",
sorted(d["pay"].unique()),
default=sorted(d["pay"].unique())
)

a=int(d["amt"].min())
b=int(d["amt"].max())

r=st.sidebar.slider(
"Expense Amount",
min_value=a,
max_value=b,
value=(a,b)
)

x=d[
(d["cat"].isin(c))&
(d["pay"].isin(p))&
(d["amt"]>=r[0])&
(d["amt"]<=r[1])
]

t=x["amt"].sum()
av=round(x["amt"].mean(),2) if len(x)>0 else 0
mx=x["amt"].max() if len(x)>0 else 0
n=len(x)

m1,m2,m3,m4=st.columns(4)

m1.metric("Total Expense",f"₹{t}")
m2.metric("Average Expense",f"₹{av}")
m3.metric("Highest Expense",f"₹{mx}")
m4.metric("Transactions",n)

st.markdown("---")

st.subheader("Filtered Expense Records")
st.dataframe(x,use_container_width=True)

st.download_button(
    "⬇ Download Filtered CSV",
    x.to_csv(index=False),
    "filtered_expense.csv",
    "text/csv"
)

st.markdown("---")

st.subheader("Summary Statistics")
st.dataframe(x.describe(),use_container_width=True)

c1,c2=st.columns(2)

with c1:
    st.subheader("Average Expense by Category")
    g=x.groupby("cat")["amt"].mean()

    f=plt.figure(figsize=(6,4))
    plt.bar(g.index, g.values, color="#2563eb", edgecolor="black")
    plt.xlabel("Category")
    plt.ylabel("Average Expense")
    plt.xticks(rotation=20)
    st.pyplot(f)

with c2:
    st.subheader("Expense Share")
    g=x.groupby("cat")["amt"].sum()

    f=plt.figure(figsize=(6,4))
    plt.pie(
            g.values,
            labels=g.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=["#2563eb","#10b981","#f59e0b","#ef4444","#8b5cf6","#06b6d4"]
        )
    plt.axis("equal")
    st.pyplot(f)

c3,c4=st.columns(2)

with c3:
    st.subheader("Expense Distribution")

    f=plt.figure(figsize=(6,4))
    plt.hist(x["amt"], bins=10, color="#0ea5e9", edgecolor="black")
    plt.xlabel("Expense Amount")
    plt.ylabel("Frequency")
    st.pyplot(f)

with c4:
    st.subheader("Transaction ID vs Expense")

    f=plt.figure(figsize=(6,4))
    plt.scatter(x["id"], x["amt"], color="#f97316", s=80)
    plt.xlabel("Transaction ID")
    plt.ylabel("Expense Amount")
    st.pyplot(f)

st.markdown("---")
st.markdown("""
<div style="background:white;padding:18px;border-radius:15px;text-align:center;
box-shadow:0 5px 20px rgba(0,0,0,.1);font-size:18px;font-weight:600;color:#2563eb;">
💰 Expense Management Dashboard<br>
<small style="color:black;">Developed using Streamlit & Pandas | Palak Goyal</small>
</div>
""", unsafe_allow_html=True)