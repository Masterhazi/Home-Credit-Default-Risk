import streamlit as st
import pickle
from sklearn.preprocessing import StandardScaler
import random

# Title of the app
st.title('Credit Default Risk Prediction')

# Updated list of column names
fin_cols = ['MONTHS_BALANCE_mean', 'CNT_INSTALMENT_mean', 'CNT_INSTALMENT_FUTURE_mean', 'SK_DPD_mean', 'SK_DPD_DEF_mean', 
            'DAYS_CREDIT_MEAN', 'CREDIT_DAY_OVERDUE_MEAN', 'AMT_CREDIT_MAX_OVERDUE_MEAN', 'AMT_CREDIT_SUM_MEAN', 
            'AMT_CREDIT_SUM_DEBT_MEAN', 'AMT_CREDIT_SUM_OVERDUE_MEAN', 'DAYS_CREDIT_ENDDATE_MEAN', 
            'DAYS_ENDDATE_FACT_MEAN', 'AMT_CREDIT_SUM_LIMIT_MEAN', 'CREDIT_LEFT', 'AMT_ANNUITY_mean', 'AMT_APPLICATION_mean', 
            'AMT_CREDIT_mean', 'AMT_DOWN_PAYMENT_mean', 'AMT_GOODS_PRICE_mean', 'HOUR_APPR_PROCESS_START_mean', 
            'RATE_DOWN_PAYMENT_mean', 'SELLERPLACE_AREA_mean', 'amt_income_total', 'amt_credit', 'amt_goods_price', 
            'days_birth', 'days_employed', 'days_registration', 'days_id_publish', 'hour_appr_process_start', 
            'days_last_phone_change', 'amt_req_credit_bureau_year', 'NUM_LATE_PAYMENTS_MEAN', 'DIFF_AMOUNT_MORE_OR_LESS_MEAN', 
            'def_60_cnt_social_circle (0-5)', 'name_contract_type(cash_loans/revolving_loans)', 
            'organization_type(check document to know your organisation type in our github page)', 
            'loan_purpose(Business development/Medicine/Other/celebration/Cancelled/Unused offer/Unknown)', 
            'payment_type(Cashless from the account of the employer/Non-cash from your account/Unknown)', 
            'channel_type(AP+(Cash loan)/Contact center/Unknown)']

num_cols = ['MONTHS_BALANCE_mean', 'CNT_INSTALMENT_mean', 'CNT_INSTALMENT_FUTURE_mean', 'SK_DPD_mean', 'SK_DPD_DEF_mean', 
            'DAYS_CREDIT_MEAN', 'CREDIT_DAY_OVERDUE_MEAN', 'AMT_CREDIT_MAX_OVERDUE_MEAN', 'AMT_CREDIT_SUM_MEAN', 
            'AMT_CREDIT_SUM_DEBT_MEAN', 'AMT_CREDIT_SUM_OVERDUE_MEAN', 'DAYS_CREDIT_ENDDATE_MEAN', 
            'DAYS_ENDDATE_FACT_MEAN', 'AMT_CREDIT_SUM_LIMIT_MEAN', 'CREDIT_LEFT', 'AMT_ANNUITY_mean', 'AMT_APPLICATION_mean', 
            'AMT_CREDIT_mean', 'AMT_DOWN_PAYMENT_mean', 'AMT_GOODS_PRICE_mean', 'HOUR_APPR_PROCESS_START_mean', 
            'RATE_DOWN_PAYMENT_mean', 'SELLERPLACE_AREA_mean', 'amt_income_total', 'amt_credit', 'amt_goods_price', 
            'days_birth', 'days_employed', 'days_registration', 'days_id_publish', 'hour_appr_process_start', 
            'days_last_phone_change', 'amt_req_credit_bureau_year', 'NUM_LATE_PAYMENTS_MEAN', 'DIFF_AMOUNT_MORE_OR_LESS_MEAN']

cat_cols = ['def_60_cnt_social_circle (0-5)', 'name_contract_type(cash_loans/revolving_loans)', 
            'organization_type(check document to know your organisation type in our github page)', 
            'loan_purpose(Business development/Medicine/Other/celebration/Cancelled/Unused offer/Unknown)', 
            'payment_type(Cashless from the account of the employer/Non-cash from your account/Unknown)', 
            'channel_type(AP+(Cash loan)/Contact center/Unknown)']

# Encoding dictionaries
loan_purpose_dict = {'Business development': 0, 'Medicine': 1, 'Other': 2, 'celebration': 3, 'Cancelled': 4, 'Unused offer': 5, 'Unknown': 6}
payment_type_dict = {'Cashless from the account of the employer': 0, 'Non-cash from your account': 1, 'Unknown': 3}
channel_type_dict = {'AP+ (Cash loan)': 0, 'Contact center': 1, 'Unknown': 2}
name_contract_type_dict = {'Cash loans': 0, 'revolving loans': 1}

# Initialize session state for random value filling
if 'random_values_filled' not in st.session_state:
    st.session_state.random_values_filled = False

# Collecting user inputs
inputs = {}
for i in range(len(fin_cols)):
    if st.session_state.random_values_filled:
        inputs[f"input_{i}"] = st.text_input(f'Enter {fin_cols[i]}', value=st.session_state.get(f"input_{i}", ""))
    else:
        inputs[f"input_{i}"] = st.text_input(f'Enter {fin_cols[i]}')

# Function to fill random values
def fill_random_values():
    st.session_state.random_values_filled = True
    for i in range(len(fin_cols)):
        if fin_cols[i] in num_cols:
            st.session_state[f"input_{i}"] = str(random.uniform(0, 100))  # Random float value for numerical columns
        elif 'def_60_cnt_social_circle' in fin_cols[i]:
            st.session_state[f"input_{i}"] = str(random.randint(0, 5))
        elif 'name_contract_type' in fin_cols[i]:
            st.session_state[f"input_{i}"] = str(random.randint(0, 1))
        elif 'organization_type' in fin_cols[i]:
            st.session_state[f"input_{i}"] = str(random.randint(0, 57))
        elif 'loan_purpose' in fin_cols[i]:
            st.session_state[f"input_{i}"] = str(random.randint(0, 6))
        elif 'payment_type' in fin_cols[i]:
            st.session_state[f"input_{i}"] = str(random.randint(0, 3))
        elif 'channel_type' in fin_cols[i]:
            st.session_state[f"input_{i}"] = str(random.randint(0, 3))



# Repopulating the fields if they were randomly filled
if st.session_state.random_values_filled:
    for i in range(len(fin_cols)):
        inputs[f"input_{i}"] = st.text_input(f'Enter {fin_cols[i]}', value=st.session_state.get(f"input_{i}", ""))



# Button to estimate
if st.button('Estimate'):
    # Encoding categorical variables
    for i in range(len(fin_cols)):
        if 'loan_purpose' in fin_cols[i]:
            inputs[f"input_{i}"] = loan_purpose_dict.get(inputs[f"input_{i}"], 6)  # Default to 6 ('Unknown')
        elif 'payment_type' in fin_cols[i]:
            inputs[f"input_{i}"] = payment_type_dict.get(inputs[f"input_{i}"], 3)  # Default to 3 ('Unknown')
        elif 'channel_type' in fin_cols[i]:
            inputs[f"input_{i}"] = channel_type_dict.get(inputs[f"input_{i}"], 2)  # Default to 2 ('Unknown')
        elif 'name_contract_type' in fin_cols[i]:
            inputs[f"input_{i}"] = name_contract_type_dict.get(inputs[f"input_{i}"], 1)  # Default to 1
        elif 'def_60_cnt_social_circle' in fin_cols[i]:
            try:
                inputs[f"input_{i}"] = int(inputs[f"input_{i}"])
            except ValueError:
                inputs[f"input_{i}"] = 0  # Default value
        elif 'organization_type' in fin_cols[i]:
            try:
                inputs[f"input_{i}"] = int(inputs[f"input_{i}"])
            except ValueError:
                inputs[f"input_{i}"] = 0  # Default value

    # Collecting and validating numerical data
    num_data = []
    for i in range(len(fin_cols)):
        if fin_cols[i] in num_cols:
            value = inputs[f"input_{i}"]
            if value != '':
                try:
                    num_data.append(float(value))
                except ValueError:
                    num_data.append(0.0)  # Default value for invalid inputs
            else:
                num_data.append(0.0)  # Default value for empty input

    # Collecting encoded categorical data
    cat_data = []
    for i in range(len(fin_cols)):
        if fin_cols[i] in cat_cols:
            value = inputs[f"input_{i}"]
            # Ensure the value is numerical
            if value != '':
                try:
                    cat_data.append(float(value))
                except ValueError:
                    cat_data.append(0.0)  # Default value
            else:
                cat_data.append(0.0)  # Default value

    # Standardizing numerical data
    ss = StandardScaler()
    num_tra = ss.fit_transform([num_data])

    # Merging num_tra and cat_data in the correct order of fin_cols
    final_data = []
    num_idx = 0
    cat_idx = 0
    for col in fin_cols:
        if col in num_cols:
            final_data.append(num_tra[0][num_idx])
            num_idx += 1
        else:
            final_data.append(cat_data[cat_idx])
            cat_idx += 1

    # Convert final_data to a numpy array with a numeric data type
    import numpy as np
    final_data = np.array(final_data, dtype=np.float32)

    # Verify data types
    # st.write("Final data types:", final_data.dtype)
    # st.write("Final data:", final_data)

    # Loading the model from the pickle file
    model = pickle.load(open('stacking_model_dec.pkl', 'rb'))

    # Making a prediction
    # Making a prediction
    try:
        prediction = model.predict([final_data])

        # Displaying more descriptive output based on the prediction value
        if prediction[0] == 0:
            st.success("The customer will **NOT** default on the loan.")
        elif prediction[0] == 1:
            st.warning("The customer **WILL** default on the loan.")
        else:
            st.error("Unexpected prediction value.")
            
    except Exception as e:
        st.error(f"Error during prediction: {e}")


        
