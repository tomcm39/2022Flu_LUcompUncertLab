# 2022 Flu Models

Goal: Database for individual predictions from metaculus
1. Indiviual predictions are a list of CSV files in the folder ./LU-humanjudgement/individualPredictions/ 
2. We need to create a single CSV file called "allIndividualPredictions.csv" that combines these individual files and formats them so they can be used for forecasting. 
    - Columns for "allIndividualPredictions.csv": QID, user, prediction_time, revision_number, cases_mapped, cases, density 
    - QID: This is the question id from each csv file. Every question created on metaculus is assigned a question id. This lets us track the question on the browser. 
    - user: This is the user_id variable from each csv file. Every user on metacuus is given a user id that tracks every forecast they make, including repeated forecasts for the same QID. 
    -  prediciton_time: This is the time variable in the CV file. The time, to the milisecond, is recorded for every submitted forecast. 
    -  revision_number: For every question a user can submit a first forecast and then revise their original forecast. Every original and revised forecast is recorded on the system. We need to create the variable revision_number that counts the submitted predictions for a single user for a single question. Revision_number equals 1 for the earliest submission, 2 for the next submitted predicition, etc. 
    - cases_mapped and density: Predictions of the number of incident cases are discretized into 200 ordered pairs. Further, the interval of cases a user can assign probabilities is mapped from [a,b] to [0,1]. The columns PDF(r=X.XX) contain both the cases and density values. The values inside each cell are the density values and the number X.XX in the column header (e.g. PDF(r=X.XX)) is the cases value mapped to the interval [0,1]. We need to create the variable cases_mapped that contain those r values and the variable density that contain those values in each cell. 
    - cases: We can map the mapped cases in the interval from 0 to 1 back to the original interval using the following formula: 0 + b * exp( exponent * cases_mapped ) where the parameters b and exponent can be found in "paramtersPerQuestion.csv". 
