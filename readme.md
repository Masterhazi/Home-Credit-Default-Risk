Home Credit Default Risk
Project Description
This repository is a simplified version of my solution to Kaggle competition "Home credit default risk". The competitors are asked to predict the Home Credit's clients repayment abilities, given customer's current application, as well as previous loan records, credit accounts information at other institutions and monthly payment data in the past. The predictions are evaluated on area under the ROC curve between the predicted probability and the observed target.

Dataset
application_{train|test}.csv Main table, broken into two files for Train (with TARGET) and Test (without TARGET).
bureau.csv All client's previous credits provided by other financial institutions that were reported to Credit Bureau (for clients who have a loan in our sample).
bureau_balance.csv Monthly balances of previous credits in Credit Bureau.
POS_CASH_balance.csv Monthly balance snapshots of previous POS (point of sales) and cash loans that the applicant had with Home Credit.
credit_card_balance.csv Monthly balance snapshots of previous credit cards that the applicant has with Home Credit.
previous_application.csv All previous applications for Home Credit loans of clients who have loans in our sample.
installments_payments.csv Repayment history for the previously disbursed credits in Home Credit related to the loans in our sample.