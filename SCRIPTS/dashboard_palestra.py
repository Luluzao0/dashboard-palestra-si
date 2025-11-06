import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(page_title="Palestra",page_icon="📊",layout="wide")
@st.cache_data
def load():
 df=pd.read_excel("data/palestra_desenvolvimento.xlsx")
 df.columns=[c.strip() for c in df.columns]
 return df
df=load()
st.title("Analise Palestra SI")
c1,c2,c3=st.columns(3)
c1.metric("Total",len(df))
c2.metric("Nota",f"{df.iloc[:,-1].mean():.1f}/10")
c3.metric("Data","14-15/10")
st.divider()
st.subheader("Notas")
fig,ax=plt.subplots(figsize=(10,4))
df.iloc[:,-1].value_counts().sort_index().plot(kind="bar",ax=ax,color="#667eea")
st.pyplot(fig)
st.subheader("Faixa Etaria")
fig,ax=plt.subplots(figsize=(10,4))
df["Idade"].value_counts().plot(kind="bar",ax=ax,color="#764ba2")
st.pyplot(fig)
if st.checkbox("Tabela"):
 st.dataframe(df,use_container_width=True)
csv=df.to_csv(index=False,encoding="utf-8-sig")
st.download_button("Download CSV",csv,"dados.csv","text/csv")
