
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os

# Load static PDD data
csv_path1 = os.path.join("data","Electrons.csv")
csv_path2 = os.path.join("data","SXRT.csv")
@st.cache_data
def load_data(path):
    df = pd.read_csv(path, header = [0,1])
    df.columns = ["_".join(col).strip() for col in df.columns.values]
    return df
Data_Electrons = load_data(csv_path1)
Data_SXRT = load_data(csv_path2)

# Streamlit app
st.title("PDD Visualiser")

# Column selection
x_col = "Energy_Cone"   

# Checkboxes for Y columns
st.write("Select modalities to plot:")

main_col1, main_col2 = st.columns(2)
with main_col1:
    st.write("Electrons")
    y_options1 = Data_Electrons.columns[1:]  # skip the first column
    col1_sub, col2_sub, col3_sub = st.columns(3)
    selected_y1 = []
    with col1_sub:
        for col_name in y_options1[0:4]:
            if st.checkbox(col_name, value=False):
                selected_y1.append(col_name)

    with col2_sub:
        for col_name in y_options1[4:8]:
            if st.checkbox(col_name, value=False):
                selected_y1.append(col_name)   

    with col3_sub:
        for col_name in y_options1[8:12]:
            if st.checkbox(col_name, value=False):
                selected_y1.append(col_name)

bolus = st.radio("Use bolus for electron treatment?",["No bolus", "5mm bolus", "10mm bolus"], index=0)
shift_5mm = bolus == "5mm bolus"
shift_10mm = bolus == "10mm bolus"

with main_col2:
    st.write("Superficial")
    y_options2 = Data_SXRT.columns[1:]
    col4_sub, col5_sub, col6_sub = st.columns(3)
    selected_y2 = []
    with col4_sub:
        for col_name in y_options2[0:5]:
            if st.checkbox(col_name, value=False):
                selected_y2.append(col_name)
    with col5_sub:
        for col_name in y_options2[5:10]:
            if st.checkbox(col_name, value=False):
                selected_y2.append(col_name)   
    with col6_sub:
        for col_name in y_options2[10:15]:
            if st.checkbox(col_name, value=False):
                selected_y2.append(col_name)    

# Create plot
fig, ax = plt.subplots()

for y_col in selected_y1:
    x_data = Data_Electrons[x_col].copy()
    if shift_5mm:
        x_data = x_data - 5
    if shift_10mm:
        x_data = x_data - 10
    ax.plot(x_data, Data_Electrons[y_col], label=y_col)

for y_col in selected_y2:
    ax.plot(Data_SXRT[x_col], Data_SXRT[y_col], label=y_col)


ax.set_xlabel("Depth in patient(mm)")
ax.set_ylabel("PDD")

# --- Add X-axis grid every 5 mm ---
x_min = min(Data_Electrons[x_col].min(), Data_SXRT[x_col].min())
x_max = max(Data_Electrons[x_col].max(), Data_SXRT[x_col].max())
ax.set_xticks(range(int(x_min), int(x_max), 5))  # ticks every 5 mm
ax.set_yticks(range(0, 105, 5))  # ticks every 5 %
ax.grid(axis='x', linestyle='--', alpha=0.7)       # show X-axis grid
ax.grid(axis='y', linestyle='--', alpha=0.7)       # show X-axis grid
ax.legend()

st.pyplot(fig)
