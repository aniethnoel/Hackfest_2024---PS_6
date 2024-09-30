#!/usr/bin/env python
# coding: utf-8

# # Hackfest 2024
# 
# ## Problem Statment 6:
# * Bringing together data of different formats to a more readable and analyzable document and create visualization tool to identify anomalies.
# 

# * In this notebook, we have explored the Audit Trail data using Python.
# * We have created some informative visual plots.
# * Both dynamic and simple plots.
# 
# We have also tried to build a dashboard too.
# * Faced challenges
# * From an industry point of view, where we need quick inferences, this is not suitable.
# * Lines of code and it may run into an error.

# ### Importing Data
# * Using **pandas** library for data handling

# In[4]:


import plotly.express as px
import plotly.graph_objs as go
import warnings
warnings.filterwarnings('ignore')


# In[1]:


import pandas as pd
df = pd.read_excel('/content/Audit Trail Report - Dummy data.xlsx')


# * Summary of the variables of the data

# In[2]:


df.info()


# * Let's look at the first 5 data points.

# In[3]:


df.head()


# ### Visualisations
# * Some normal bar and pie charts are there
# * Some dynamic plots in which if someone track the chart, they can get some more information of that observation.

# In[20]:


import plotly.express as px
import pandas as pd

# Group by SiteName and count the number of changes
changes_per_site = df.groupby('SiteName').size().reset_index(name='Number of Changes')

# Plot the number of changes per site
fig_site = px.bar(changes_per_site,
                  x='SiteName',
                  y='Number of Changes',
                  title='Number of Changes per Site',
                  labels={'SiteName': 'Site Name', 'Number of Changes': 'Number of Changes'},
                  text_auto=True)
fig_site.update_layout(xaxis={'categoryorder':'total descending'})
fig_site.show()


# In[13]:


fig10 = px.pie(df, names='RoleName', title='Role Distribution in Audits',
               labels={'RoleName': 'Role Name'})
fig10.show()


# In[14]:


import matplotlib.pyplot as plt
import seaborn as sns

# Aggregate data by user
user_activity = df['AuditUser'].value_counts()

# Plot user activity
plt.figure(figsize=(12, 6))
sns.barplot(x=user_activity.values, y=user_activity.index, palette='viridis')
plt.title('Activity of Different Users')
plt.xlabel('Number of Actions')
plt.ylabel('User')
plt.tight_layout()
plt.show()


# In[5]:


# Convert AuditTime to datetime if not already
df['AuditTime'] = pd.to_datetime(df['AuditTime'])

# 1. Audit Activity Over Time
audit_time_series = df.groupby(df['AuditTime'].dt.date).size().reset_index(name='AuditCount')
fig1 = px.line(audit_time_series, x='AuditTime', y='AuditCount', title='Audit Activity Over Time',
               labels={'AuditTime': 'Date', 'AuditCount': 'Number of Audits'})

# 2. Distribution of Audit Actions
audit_action_dist = df['AuditActionType'].value_counts().reset_index()
audit_action_dist.columns = ['AuditActionType', 'Count']
fig2 = px.bar(audit_action_dist, x='AuditActionType', y='Count', title='Distribution of Audit Actions',
              labels={'AuditActionType': 'Audit Action Type', 'Count': 'Frequency'})

# 3. Audit Actions by User Roles
audit_role_action = df.groupby(['RoleName', 'AuditActionType']).size().reset_index(name='Count')
fig3 = px.bar(audit_role_action, x='RoleName', y='Count', color='AuditActionType', title='Audit Actions by User Roles',
              labels={'RoleName': 'Role Name', 'Count': 'Frequency', 'AuditActionType': 'Audit Action Type'},
              barmode='stack')

# 4. Audit Actions by Study and Site
audit_study_site = df.groupby(['StudyName', 'SiteName', 'AuditActionType']).size().reset_index(name='Count')
fig4 = px.bar(audit_study_site, x='StudyName', y='Count', color='AuditActionType',
              facet_col='SiteName', facet_col_wrap=3, title='Audit Actions by Study and Site',
              labels={'StudyName': 'Study Name', 'Count': 'Frequency', 'AuditActionType': 'Audit Action Type'})

# 5. Time Taken for Audits (Time Difference)
df['AuditTimeDiff'] = df['AuditTime'].diff().dt.total_seconds()
fig5 = px.histogram(df, x='AuditTimeDiff', nbins=50, title='Time Taken for Audits',
                    labels={'AuditTimeDiff': 'Time Difference (Seconds)'},
                    log_y=True)  # Log scale for better visualization of long tails


# In[6]:


fig1.show()


# In[7]:


fig2.show()


# In[8]:


fig3.show()


# In[9]:


fig4.show()


# In[10]:


fig5.show()


# In[11]:


import pandas as pd
import plotly.express as px

# Extract hour and day of the week
df['Hour'] = df['AuditTime'].dt.hour
df['DayOfWeek'] = df['AuditTime'].dt.day_name()

# Heatmap of audit activity by hour and day of the week
activity_heatmap = df.groupby(['DayOfWeek', 'Hour']).size().reset_index(name='Count')
fig6 = px.density_heatmap(activity_heatmap, x='Hour', y='DayOfWeek', z='Count',
                          title='User Activity Heatmap',
                          labels={'Count': 'Number of Audits'})
fig6.show()


# In[16]:


# Create a pivot table of user vs. role activity
user_role_matrix = df.pivot_table(index='AuditUser', columns='RoleName', aggfunc='size', fill_value=0)

# Plot a heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(user_role_matrix, cmap='YlGnBu', cbar_kws={'label': 'Number of Actions'})
plt.title('Heatmap of User vs. Role Activity')
plt.xlabel('Role')
plt.ylabel('User')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[17]:


import plotly.express as px

# Preparing the data for interactive visualization
# Group by AuditUser and AuditActionType and count the occurrences
grouped_df = df.groupby(['AuditUser', 'AuditActionType']).size().reset_index(name='ActionCount')

# Create an interactive bar chart using Plotly
fig = px.bar(grouped_df,
             x='AuditUser',
             y='ActionCount',
             color='AuditActionType',
             hover_data=['AuditActionType'],
             labels={'ActionCount': 'Number of Actions', 'AuditUser': 'User', 'AuditActionType': 'Action Type'},
             title='User Actions in the Audit Trail')

# Add dropdowns to filter by user and action type
fig.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(
                    args=["visible", [True, False]],
                    label="All Users",
                    method="restyle"
                ),
                dict(
                    args=["visible", [False, True]],
                    label="Filter by User",
                    method="restyle"
                )
            ]),
            direction="down"
        )
    ]
)

# Show the interactive plot
fig.show()


# In[18]:


import plotly.express as px

df['Hour'] = df['AuditTime'].dt.hour
grouped_df = df.groupby(['AuditUser', 'AuditActionType', 'Hour']).size().reset_index(name='ActionCount')

# Create an interactive scatter plot
fig = px.scatter(grouped_df,
                 x='Hour',
                 y='ActionCount',
                 color='AuditActionType',
                 facet_col='AuditUser',
                 title='User Actions Over Time',
                 labels={'ActionCount': 'Number of Actions', 'Hour': 'Hour of Day', 'AuditUser': 'User', 'AuditActionType': 'Action Type'})

# Add dropdowns to filter by user and action type
fig.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(
                    args=["visible", [True, False, False]],
                    label="All Users",
                    method="restyle"
                ),
                dict(
                    args=["visible", [False, True, False]],
                    label="Filter by User",
                    method="restyle"
                ),
                dict(
                    args=["visible", [False, False, True]],
                    label="Filter by Time",
                    method="restyle"
                )
            ]),
            direction="down"
        )
    ]
)

# Display the interactive plot
fig.show()


# In[19]:


import plotly.express as px
import pandas as pd

df['Date'] = df['AuditTime'].dt.date
df['Time'] = df['AuditTime'].dt.time

# Group by relevant variables
grouped_df = df.groupby(['AuditUser', 'AuditActionType', 'Date', 'Time']).size().reset_index(name='ActionCount')

# Create a scatter plot with Date and Time on respective axes, with no dropdowns
fig = px.scatter(grouped_df,
                 x='Date',
                 y='Time',
                 size='ActionCount',
                 color='AuditActionType',
                 facet_col='AuditUser',
                 title='User Actions Over Time',
                 labels={'ActionCount': 'Number of Actions', 'Date': 'Date', 'Time': 'Time', 'AuditUser': 'User', 'AuditActionType': 'Action Type'},
                 height=800)

# Display the interactive plot
fig.show()


# In[21]:


import pandas as pd
import matplotlib.pyplot as plt

# Group by AuditTime and SubjectName, then count the AuditActions
grouped = df.groupby([df['AuditTime'], 'SubjectName']).count().reset_index()

# Plotting
plt.figure(figsize=(10, 6))

for subject in grouped['SubjectName'].unique():
    subject_data = grouped[grouped['SubjectName'] == subject]
    plt.plot(subject_data['AuditTime'], subject_data['AuditAction'], marker='o', label=subject)

plt.title('Audit Action Count Over Time by Subject')
plt.xlabel('Audit Time')
plt.ylabel('Audit Action Count')
plt.legend(title='Subject Name')
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# ### Dynamic Dashboard
# * Used **dash** package

# In[23]:


get_ipython().system('pip install pandas openpyxl')


# In[26]:


get_ipython().system('pip install dash')


# In[24]:


data = df


# In[29]:


#from dash import JupyterDash # Use Dash instead of jupyter_dash
from dash import Dash, dcc, html, Input, Output # Import Dash directly
import plotly.express as px

# Initialize the Dash app
app = Dash(__name__) # Initialize the app using Dash

# Convert 'AuditTime' to datetime format for better handling in plots
data['AuditTime'] = pd.to_datetime(data['AuditTime'])

# Define the layout of the app
app.layout = html.Div([
    html.H1("Audit Data Interactive Dashboard", style={'text-align': 'center'}),

    # Dropdown for selecting Subject Name
    dcc.Dropdown(
        id='subject_dropdown',
        options=[{'label': subject, 'value': subject} for subject in data['SubjectName'].unique()],
        value=data['SubjectName'].unique()[0],  # Default value
        multi=False,
        style={'width': '50%'}
    ),

    # Dropdown for selecting the type of plot
    dcc.Dropdown(
        id='plot_type_dropdown',
        options=[
            {'label': 'Line Plot', 'value': 'line'},
            {'label': 'Scatter Plot', 'value': 'scatter'},
            {'label': 'Bar Plot', 'value': 'bar'}
        ],
        value='line',  # Default value
        multi=False,
        style={'width': '50%', 'margin-top': '10px'}
    ),

    # Graph output
    dcc.Graph(id='dynamic_graph', style={'width': '90%', 'display': 'inline-block'}),

    # Date Picker Range for selecting date range
    dcc.DatePickerRange(
        id='date_picker',
        start_date=data['AuditTime'].min(),
        end_date=data['AuditTime'].max(),
        display_format='YYYY-MM-DD',
        style={'margin-top': '20px'}
    )
])

# Define the callback to update the graph based on user input
@app.callback(
    Output('dynamic_graph', 'figure'),
    [Input('subject_dropdown', 'value'),
     Input('plot_type_dropdown', 'value'),
     Input('date_picker', 'start_date'),
     Input('date_picker', 'end_date')]
)
def update_graph(selected_subject, plot_type, start_date, end_date):
    # Filter data based on subject and date range
    filtered_data = data[(data['SubjectName'] == selected_subject) &
                         (data['AuditTime'] >= start_date) &
                         (data['AuditTime'] <= end_date)]

    # Create the figure based on the selected plot type
    if plot_type == 'line':
        fig = px.line(filtered_data, x='AuditTime', y='AuditAction', color='AuditActionType',
                      title=f'{selected_subject} - Line Plot of Audit Actions Over Time')
    elif plot_type == 'scatter':
        fig = px.scatter(filtered_data, x='AuditTime', y='AuditAction', color='AuditActionType',
                         title=f'{selected_subject} - Scatter Plot of Audit Actions Over Time')
    elif plot_type == 'bar':
        fig = px.bar(filtered_data, x='AuditTime', y='AuditAction', color='AuditActionType',
                     title=f'{selected_subject} - Bar Plot of Audit Actions Over Time')

    # Update layout for better visualization
    fig.update_layout(xaxis_title='Audit Time', yaxis_title='Audit Action', hovermode='closest')

    return fig

# Run the app
app.run_server(mode='inline')


#  ---
#  <center> Thank You! </center>
