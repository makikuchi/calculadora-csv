import streamlit as st
import pandas as pd

st.title("Calculadora de Dados CSV")
st.write("Envie seu arquivo com as colunas necessárias para realizar o cálculo.")

arquivo_enviado = st.file_uploader("Faça o upload do seu arquivo CSV", type=["csv"])

if arquivo_enviado is not None:
    df_jwb_vendas = pd.read_csv(arquivo_enviado, sep=';')
    st.write("Dados originais:")
    st.dataframe(df_jwb_vendas.head())

    df_jwb_vendas.columns = df_jwb_vendas.columns.str.strip()
    colunas_financeiras = ["Vl.Total", "Vl.ICMS", "Vl.IPI", "Vl.PIS", "Vl.COFINS"]
    
    for col in colunas_financeiras:
        df_jwb_vendas[col] = df_jwb_vendas[col].astype(str).str.replace(r'\s+', '', regex=True).str.replace(',', '.').astype(float)

    try:
        df_jwb_vendas["NET"] = (
            df_jwb_vendas["Vl.Total"] 
            - df_jwb_vendas["Vl.ICMS"] 
            - df_jwb_vendas["Vl.IPI"] 
            - df_jwb_vendas["Vl.PIS"] 
            - df_jwb_vendas["Vl.COFINS"]
        )

        colunas_soma = ["Vl.Total", "Vl.ICMS", "Vl.IPI", "Vl.PIS", "Vl.COFINS", "NET"]
        df_exibicao = df_jwb_vendas.copy()

        totais = df_exibicao[colunas_soma].sum()

        linha_total = pd.DataFrame([totais], columns=colunas_soma)
        linha_total["Dt.Em"] = "TOTAL ACUMULADO"

        df_final_com_total = pd.concat([df_exibicao, linha_total], ignore_index=True)

        for col in colunas_soma:
            df_final_com_total[col] = df_final_com_total[col].map("{:,.2f}".format)
            
        st.write("Resultado com Total Acumulado:")
        st.dataframe(df_final_com_total)

        csv_final = df_final_com_total.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Baixar Resultado (CSV)",
            data=csv_final,
            file_name="dados_calculados.csv",
            mime="text/csv"
        )

    except KeyError:
        st.error("Erro: O arquivo enviado não contém as colunas necessárias para o cálculo. Verifique os nomes das colunas originais do CSV.")