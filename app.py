import streamlit as st
import numpy as np
import time
import pandas as pd
from tensorflow.keras.models import load_model

# Load the saved model
model = load_model('C:/Users/ESTEEM/Documents/POC/RUL/Model')

# Load x_test and y_test
x_test = np.load('x_test.npy')

st.set_page_config(
    page_title="RUL Dashboard",
    page_icon=":wrench:")

st.write("Every 1/2 a second the model predicts the remaining useful lifetime given reading from the past ... Displayed below is the prediction and a plot of the predicted RUL versus the actual RUL observed. All predictions are done in real time with the latency also displayed below.")

# Display a random number that updates every second
number_placeholder = st.empty()
chart_placeholder = st.empty()
latency_placeholder = st.empty()
warning_placeholder = st.empty()

# Load values from output
RUL = []

# counter
i = 0

while True:
    # Begin count
    start = time.time()

    # Pick next RUL from data
    RUL.append(model.predict(x_test[i].reshape(1, 50, 17), verbose=0)[0][0])

    # End count
    end = time.time()

    # Calculate latency
    latency = end-start
    
    # Update the display with the new number
    number_placeholder.metric(label="Remaining Useful Lifetime", value=f"{RUL[i]:.2f} hours")
    chart_placeholder.line_chart(RUL)
    latency_placeholder.metric(label="latency", value=f"{1000*latency:.2f} ms")

    # If RUL is low print warning
    if RUL[i] < 150:
        warning_placeholder.error("!!WARNING!! RUL IS LOW: CONSIDER PREVENTATIVE MAINTENANCE TO EXTEND ENGINE LIFETIME")
    else:
        warning_placeholder.empty()
    
    # Wait for 1 second before the next update
    time.sleep(0.5)

    # Update counter
    i += 1