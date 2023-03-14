import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import streamlit as st
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None
from PIL import Image

image = Image.open('DSP.png')
st.set_page_config(layout="wide")
st.title('Data Analysis & Tunnel Management (DATuM) Dashboard')

url = 'https://github.com/kenneth-yap/DATUM-streamlit/blob/d8e460492c008fbcb37ec80ea047f5909582609b/README.md'
st.write('[INSTRUCTIONS](%s)' % url)

# Upload file
uploaded_file = st.file_uploader('Upload a csv file', type = (['.csv']))

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else: 
    df = pd.read_csv('activities_default.csv')

# Data cleaner
df.pop("user")
df.pop("report_id")
df.pop("round_no")
df.pop("gang")
df.pop("equipment")
df.pop("delays")
df.pop("additional_info")

# Create new variables

## Tunnel chainage
df['tunnel_chainage'] = df['tunnel_meter_finish'] - df['tunnel_meter_start']
df.reset_index(drop=True, inplace=True)

## Time taken
# Change file format
df['time_start'] = pd.to_datetime(df['time_start'], format='%H:%M')
df['time_stop'] = pd.to_datetime(df['time_stop'], format='%H:%M')
df["date"] = pd.to_datetime(df["date"])
df["date_logged"] = pd.to_datetime(df["date_logged"])

# Create time taken variable
df['time_taken'] = (df.time_stop - df.time_start).astype('timedelta64[m]')

# Correct time that goes over night
for times in range(len(df.time_taken)):
    if df.time_taken[times]<0:
        df.time_taken[times] = df.time_taken[times] + 24*60

# Columns which are not required is dropped.
df.pop("time_start")
df.pop("time_stop")

# All NaN is replaced with a string.
df.fillna('Not available', inplace = True)
df = df.reset_index()

# Begin building app layout
fig = px.histogram(df, x="location", y="time_taken", color="activity",
     labels={"location": "Location",
             "time_taken": "Time taken (minutes)",
             "activity": "Activity (double click legend to isolate data)"
              })

fig.update_layout(title_text='Project Overview', title_x=0.5, xaxis_title=None, height = 800)
fig.for_each_trace(lambda t: t.update(hovertemplate=t.hovertemplate.replace("sum of", "")))
fig.for_each_yaxis(lambda a: a.update(title_text=a.title.text.replace("sum of", "")))

st.plotly_chart(fig, use_container_width=True)

st.header('Areas of interest')

# Filters

st.subheader('Filters')

col1, col2 = st.columns(2)

with col1:
    location = st.selectbox('Location of interest:', df['location'].unique())
with col2:
    activity = st.selectbox('Activity:', df['activity'].unique())

excavation_sequence = st.selectbox('Excavation sequence:',df['excavation_seq'].unique())

chainage_range = st.slider('Chainage', value = (float(df.tunnel_meter_start.min()), float(df.tunnel_meter_finish.max())))

# Apply first 4 filters
dff = df.loc[df.location.isin([location])]

# Find the total time spent on location
total_time = sum(dff.time_taken)
delay_time = sum(dff.time_taken[dff.activity == 'Delay'])

# Apply activity filter
dff = dff.loc[dff.activity.isin([activity])]

# Find the time spent on activity
activity_time = sum(dff.time_taken)

 # Apply last chainage filter
dff = dff.loc[dff.tunnel_meter_start>chainage_range[0]]
dff = dff.loc[dff.tunnel_meter_start<chainage_range[1]]

# Calculate number of data points available 
count_bench = sum(dff.excavation_seq == 'Bench (B)')
count_benchinv = sum(dff.excavation_seq == 'Bench/Invert (B/I)')
count_CTR = sum(dff.excavation_seq == 'CTR')
count_fullFace = sum(dff.excavation_seq == 'Full Face (FF)')
count_invert = sum(dff.excavation_seq == 'Invert (I)')
count_LHS = sum(dff.excavation_seq == 'LHS')
count_RHS = sum(dff.excavation_seq == 'RHS')
count_shaft = sum(dff.excavation_seq == 'Shaft (S)')
count_topHeading = sum(dff.excavation_seq == 'Top Heading (TH)')
count_notApplicable = sum(dff.excavation_seq == 'Not applicable')

# Create a dataframe for it
excavation_df = pd.DataFrame()
excavation_df['Bench (B)'] = [count_bench]
excavation_df['Bench/Invert (B/I)'] = [count_benchinv]
excavation_df['CTR'] = [count_CTR]
excavation_df['Full Face (FF)'] = [count_fullFace]
excavation_df['Invert (I)'] = [count_invert]
excavation_df['LHS'] = [count_LHS]
excavation_df['RHS'] = [count_RHS]
excavation_df['Shaft (S)'] = [count_shaft]
excavation_df['Top Heading (TH)'] = [count_topHeading]
excavation_df['Not applicable'] = [count_notApplicable]
excavation_df.reset_index(drop=True, inplace=True)

st.markdown('Activity counts at different excavations:')
st.dataframe(excavation_df)

# Apply final filters
dff = dff.loc[dff.excavation_seq.isin([excavation_sequence])]

# Calculate descriptive properties of the data
count_time = round(dff.time_taken.describe()[0], 4)
average_time = round(dff.time_taken.describe()[1], 4)
std_time = round(dff.time_taken.describe()[2], 4)
min_time = round(dff.time_taken.describe()[3], 4)
median_time = round(dff.time_taken.describe()[5], 4)
max_time = round(dff.time_taken.describe()[7], 4)

count_chain = round(dff.tunnel_chainage.describe()[0],4)
average_chain = round(dff.tunnel_chainage.describe()[1],4)
std_chain = round(dff.tunnel_chainage.describe()[2],4)
min_chain = round(dff.tunnel_chainage.describe()[3],4)
median_chain = round(dff.tunnel_chainage.describe()[5],4)
max_chain = round(dff.tunnel_chainage.describe()[7],4)

col5, col6 = st.columns(2)

with col5:
# Create table for time properties
    st.markdown('Time description (per advance):')
    time_describe_df = dff.time_taken.describe()
    time_describe_df.rename(index = {'count': 'Number of readings available'\
        ,'mean': 'Average [minutes]', 'std':'Standard deviation [minutes]'\
        , 'min':'Minimum time taken [minutes]', 'max':'Maximum time taken [minutes]'\
        , '50%': 'Median [minutes]', '25%': 'Lower interquartile range [minutes]'\
        , '75%':'Upper interquatile range [minutes]', }, inplace = True)
    st.table(time_describe_df)

with col6:
# Create table for chainage properties
    st.markdown('Chainage description (per advance):')
    tunnel_chainage_df = dff.tunnel_chainage.describe()
    tunnel_chainage_df.rename(index = {'count': 'Number of readings available'\
        ,'mean': 'Average [metres]', 'std':'Standard deviation [metres]'\
        , 'min':'Minimum distance [metres]', 'max':'Maximum distance [metres]'\
        , '50%': 'Median [metres]', '25%': 'Lower interquartile range [metres]'\
        , '75%':'Upper interquatile range [metres]', }, inplace = True)
    st.table(tunnel_chainage_df)

st.sidebar.image(image, use_column_width=True)

st.sidebar.subheader('Adjustments for removal/spraying rate:')

theo_area = st.sidebar.number_input('Theoretical excavation/spraying area (m^2)', value = 10.0, step=1e-3, format="%.3f")
over_area = st.sidebar.number_input('Overprofile of excavation/spraying area (m^2)', value = 0.0, step=1e-3, format="%.3f")
select_time = st.sidebar.number_input('Time taken per advance [min]', value = time_describe_df[1], step=1e-3, format="%.3f")
select_chain = st.sidebar.number_input('Distance per advance [metres]', value = tunnel_chainage_df[1], step=1e-3, format="%.3f")

st.sidebar.markdown('* Time and chainage description is provided to estimate the inputs above, but remember to change activity filter to obtain the correct description.')

# Calculate the advance rate
advance_rate = round(dff.groupby('date_logged').sum().sort_values(by='date_logged').reset_index()['tunnel_chainage'].mean(),3)

# Calculate the muck removal/spraying rate
if ((float(theo_area) + float(over_area)) >0) & (select_time > 0) & (select_chain > 0):
    volume_rate = str(round((float(select_chain)*(float(theo_area) + float(over_area))/select_time),3)) + ' m^3/min'
else:
    volume_rate = 'Fill in sidebar'

# Calculate the percentage of time spent
time_percent = round(activity_time/total_time*100,3)

st.subheader('Key insights:')
col3, col4 = st.columns(2)

with col3:
        st.metric('Advance rate of activity', str(advance_rate) + ' metres/day')
        st.metric('Removal/spraying rate', str(volume_rate))
with col4:
        st.metric('Proportion of time spent on activity', str(time_percent) + ' %')
        st.metric('Proportion of time spent on delays', str(round(delay_time/total_time*100, 3)) + ' %')

st.sidebar.subheader('Details of new project:')

theo_area_new = st.sidebar.number_input('New theoretical excavation/spraying area [m^2]', min_value = 0.0, step=1e-3, format="%.3f")
over_area_new = st.sidebar.number_input('New overprofile of excavation/spraying area [m^2]', min_value = 0.0, step=1e-3, format="%.3f")
advance_length = st.sidebar.number_input('New advance length [metres]', min_value = 0.0, step=1e-3, format="%.3f")
project_duration = st.sidebar.number_input('Estimated project duration [days]', min_value = 0.0, step=1e-3, format="%.3f")

# Calculate the new volumetric time required
if ((float(theo_area_new) + float(over_area_new)) >0) & (float(advance_length) >0):
    new_time_volume = str(round((theo_area_new+over_area_new)*advance_length/ \
        (float(select_chain)*(float(theo_area) + float(over_area))/select_time), 3)) + ' minutes'
else:
    new_time_volume = 'Fill in sidebar'

    # Calculate the new time required
if float(project_duration) > 0 :
    new_delay = str(round(project_duration/(1-(delay_time/total_time)),3)) + ' days'
else:
    new_delay = 'Fill in sidebar'

st.subheader('Estimations for new project:')
col3, col4 = st.columns(2)

with col3:
        st.metric('Estimated duration for activity (minutes)', str(new_time_volume))
with col4:
        st.metric('Project duration after factoring in delays (days)', str(new_delay))
