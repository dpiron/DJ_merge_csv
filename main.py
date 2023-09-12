import streamlit as st
from io import StringIO
import pandas as pd
import func as f

new_df1 = pd.DataFrame()
new_df2 = pd.DataFrame()
new_df3 = pd.DataFrame()
new_df4 = pd.DataFrame()
new_df5 = pd.DataFrame()
new_df6 = pd.DataFrame()

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


"### Import bank csv files"
cols = st.columns(2)
with cols[0]:
    denis_fortis_debit_raw = st.file_uploader('Denis Fortis Debit', type='csv')
    denis_fortis_credit_raw = st.file_uploader('Denis Fortis Credit', type='csv')
    julia_fortis_debit_raw = st.file_uploader('Julia Fortis Debit', type='csv')
with cols[1]:
    denis_belfius_debit_raw = st.file_uploader('Denis Belfius Debit', type='csv')
    denis_belfius_credit_raw = st.file_uploader('Denis Belfius Credit', type='txt')
    bc_wise_debit_raw = st.file_uploader('BC Wise Debit', type='csv')

if denis_fortis_debit_raw is not None:
    denis_fortis_debit = pd.read_csv(denis_fortis_debit_raw, sep=';')
    denis_fortis_debit = f.replace_none(denis_fortis_debit)
    new_df1["Date"] = denis_fortis_debit["Date d'exécution"]
    new_df1["Info"] = denis_fortis_debit["Type de transaction"] + ', ' + \
                     denis_fortis_debit["Nom de la contrepartie"] + ', ' + \
                     denis_fortis_debit["Communication"] + ', ' + \
                     denis_fortis_debit["Détails"]
    new_df1["Amount"] = denis_fortis_debit["Montant"]
    new_df1["Source"] = 'Fortis Denis Debit'
    new_df1["Paid by"] = 'D'

if denis_fortis_credit_raw is not None:
    denis_fortis_credit = pd.read_csv(denis_fortis_credit_raw, sep=';', encoding='latin-1')
    new_df2["Date"] = denis_fortis_credit["Date d'exécution"]
    new_df2["Info"] = denis_fortis_credit["Détails"]
    new_df2["Amount"] = denis_fortis_credit["Montant"]
    new_df2["Source"] = 'Fortis Denis Credit'
    new_df2["Paid by"] = 'D'

if denis_belfius_debit_raw is not None:
    denis_belfius_debit = pd.read_csv(denis_belfius_debit_raw, sep=';', encoding='latin-1', skiprows=12)
    denis_belfius_debit = f.replace_none(denis_belfius_debit)
    new_df3["Date"] = denis_belfius_debit["Date de comptabilisation"]
    new_df3["Info"] = denis_belfius_debit["Nom contrepartie contient"] + ', ' + \
                     denis_belfius_debit["Rue et numéro"] + ', ' + \
                     denis_belfius_debit["Code postal et localité"] + ', ' + \
                     denis_belfius_debit["Transaction"] + ', ' + \
                     denis_belfius_debit["Code pays"] + ', ' + \
                     denis_belfius_debit["Communications"]
    new_df3["Amount"] = denis_belfius_debit["Montant"]
    new_df3["Source"] = 'Belfius Denis Debit'
    new_df3["Paid by"] = 'D'

if denis_belfius_credit_raw is not None:
    stringio = StringIO(denis_belfius_credit_raw.getvalue().decode("utf-8"))
    data = stringio.readlines()
    denis_belfius_credit = f.decode_belfius_credit(data)
    new_df4["Date"] = denis_belfius_credit["1"]
    new_df4["Info"] = denis_belfius_credit["2"]
    new_df4["Amount"] = denis_belfius_credit["5"]
    new_df4["Source"] = 'Belfius Denis Credit'
    new_df4["Paid by"] = 'D'

if julia_fortis_debit_raw is not None:
    julia_fortis_debit = pd.read_csv(julia_fortis_debit_raw, sep=',')
    julia_fortis_debit = f.replace_none(julia_fortis_debit)
    new_df5["Date"] = julia_fortis_debit["Execution date"]
    new_df5["Info"] = julia_fortis_debit["Transaction type"] + ', ' + \
                      julia_fortis_debit["Name of other party"] + ', ' + \
                      julia_fortis_debit["Communication"] + ', ' + \
                      julia_fortis_debit["Details"]
    new_df5["Amount"] = julia_fortis_debit["Amount"]
    new_df5["Source"] = 'Fortis Julia Debit'
    new_df5["Paid by"] = 'J'

if bc_wise_debit_raw is not None:
    bc_wise_debit = pd.read_csv(bc_wise_debit_raw, sep=',')
    bc_wise_debit = f.replace_none(bc_wise_debit)
    new_df6["Date"] = bc_wise_debit["Date"]
    new_df6["Info"] = bc_wise_debit["Payment Reference"] + ', ' + \
                      bc_wise_debit["Payee Name"] + ', ' + \
                      bc_wise_debit["Merchant"] + ', ' + \
                      bc_wise_debit["Description"]
    new_df6["Amount"] = bc_wise_debit["Amount"]
    new_df6["Source"] = 'Wise BC Debit'
    new_df6["Paid by"] = 'BC'

if st.button('Calculate'):
    total_df = pd.concat([new_df1, new_df2, new_df3, new_df4, new_df5, new_df6], axis=0)
    amounts = total_df['Amount'].values.tolist()
    amounts = [x.replace(',','.') for x in amounts]
    amounts = [x.replace(' EUR','') for x in amounts]
    amounts = [float(x) for x in amounts]
    amounts = [str(x) for x in amounts]
    amounts = [x.replace('.',',') for x in amounts]
    total_df['Amount'] = amounts
    total_df = total_df.reset_index()

    csv = convert_df(total_df)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='output.csv',
        mime='text/csv',
    )
