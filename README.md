# DATUM-streamlit

This app was created to visualize the data collected from tunnelling projects. It supplements the DATuM software developed in-house at Dr Sauer and partners.

## Input
The input of this app should be a .csv file with the following headings.

![](https://github.com/kenneth-yap/DATUM-streamlit/blob/main/table_headings.PNG)

It is important that all the headings have the exact same alphabets and capitalization. A few things to note:

* Please clean the data before uploading. If the chainage is unusually large the web app will have problems uploading the file and crash. This can be mitigated by removing start and end chainages with unusually large magnitude. The same applies to time. Overall, the columns that need to be cleaned are: (i) tunnel_meter_start, (ii) tunnel_meter_finish, (iii) time_start and (iv) time_stop.

* The maximum difference in largest and smallest chainage that the app can take is 1000000. Any chainage difference that is larger than this will cause the app to crash.

* If the data is not cleaned properly, it will produce erronous results - garbage in, garbage out. 

* The code will automatically calculate the time taken and the chainages between the start and end point. You don't have to create a new column on excel for that.

* There is a 200 mb file limit.

## Filters
After inputting the data that needs to be analysed, filters are applied to obtain key insights of the data. The filters can be split into filters for the graph and filters for descriptions. 

**Filter for dashboard**
* On the right of the histogram, a legend of activities is provided to indicate the porportion of time spent at each location for respective activities. To visualize a specific activity, simply double click on the activity from the legend and it will segregate the data accordingly. To return to visualizing all the data, simply double click again and it will return to its default view.

**Filter for key insights**
* 3 filters are provided to extract key insights of an activity at a specific location for a selected excavation.
* However, not all types of excavation is done at a given face. Therefore, a table that indicates the number of different excavations done at a given face is illustrated to show the type of excavation present at that location. Please use this table to reselect the excavations that you would like to observe. 

## Output

The output and the formulas associated with calculations are attached below:

* A plotly dashboard indicating the time allocated for each activity at each location.

* Insights into the current project
  - Advance rate of activity selected

  This value is extracted from the dataset uploaded and no sidebar inputs are required. It will change based on the 3 filters selected previously.

  ![](https://github.com/kenneth-yap/DATUM-streamlit/blob/main/advance_rate.PNG) 

  - Proportion of time spent on activity

  This value is extracted from the dataset uploaded and no sidebar inputs are required. It will change based on the 3 filters selected previously.

  ![](https://github.com/kenneth-yap/DATUM-streamlit/blob/main/proportion_time.PNG)

  - Removal/spraying rate

  This value, by default, will use the mean chainage and mean time taken. However, this is adjustable in the sidebar and the descriptive information of time taken and chainage per advance should be used to estimate a rough guess. Theoretical and overprofile of excavation/spraying area needs to be taken from the project brief and maunally inputted. By default, it will assume a combined area of 10 m^2.

  ![](https://github.com/kenneth-yap/DATUM-streamlit/blob/main/volume_rate.PNG)

  - Proportion of time spent on delays

  This value is extracted from the dataset uploaded and no sidebar inputs are required. It will change based on the 3 filters selected previously. If under the 'Activities' attribute, a 'Delay' activity is not present, this section will produce 0%. The recommended course of action is to rename which ever activity that is condered a cause of delay (e.g. 'Idle time' or 'Interruptions') to 'Delay' before uploading.

  ![](https://github.com/kenneth-yap/DATUM-streamlit/blob/main/proportion_delays.PNG)

* Projections for future projects
  - Estimated duration for activity

  By back-calculating the dimensions of the new tunnel, a required input in the side bar, a rough estimate of time taken for the activity cna be provided. it uses the removal/spraying rate from the previous calculation.

  ![](https://github.com/kenneth-yap/DATUM-streamlit/blob/main/estimated_duration.PNG)

  - Project duration after factoring in delays

  It will back calculate the project after factoring in delays. However, this section will not work if the 'Proportion of time spent on delays' is not working.

  ![](https://github.com/kenneth-yap/DATUM-streamlit/blob/main/estimated_duration.PNG)
