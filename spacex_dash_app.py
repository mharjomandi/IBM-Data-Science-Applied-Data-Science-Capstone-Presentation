# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

max_value = spacex_df['Payload Mass (kg)'].max()
min_value = spacex_df['Payload Mass (kg)'].min()


options_list = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': k, 'value': k } for k in sorted(spacex_df['Launch Site'].unique())]
print(options_list)

# Create a dash application
app = dash.Dash(__name__)


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36','font-size': 40}),
            # TASK 1: Add a dropdown list to enable Launch Site selection
            # The default select value is for ALL sites
            # dcc.Dropdown(id='site-dropdown',...)
				html.Div([
                    html.H2('Select Site:', style={'margin-right': '2em'}),
                    dcc.Dropdown(id='site-dropdown', options=options_list,  value='ALL',
                    placeholder="place holder here", searchable=True),

                    ]),
                    html.Br(),

                    # TASK 2: Add a pie chart to show the total successful launches count for all sites
                    # If a specific launch site was selected, show the Success vs. Failed counts for the site
                    html.Div(dcc.Graph(id='success-pie-chart')),
                    html.Br(),

                    html.P("Payload range (Kg):"),
                    # TASK 3: Add a slider to select payload range
                    #dcc.RangeSlider(id='payload-slider',...)				
				    # dcc.RangeSlider(min=min_value, max=max_value, step=1, value=[min_value, max_value], id='payload-slider'),
				    dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, marks={0: '0', 100: '100'}, value=[min_value, max_value]),
				    html.Br(),

                    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
				    # fig = px.scatter(df, x="sepal_width", y="sepal_length") dcc.Graph(figure=fig)
                    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
	Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):    
    
    if entered_site == 'ALL':
        filtered_df = filtered_df = spacex_df.loc[spacex_df['class']==1]
        pc_title = 'ALL Sites'
        fig = px.pie(filtered_df, values='class', names='Launch Site', title=pc_title)
    else:        
        filtered_df = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        pc_title = 'Site: '+ entered_site
        # return the outcomes piechart for a selected site Copied!

        fig = px.pie(filtered_df, names='class', title=pc_title)

    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
		Output(component_id='success-payload-scatter-chart', component_property='figure'),
		[Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]
	)
def get_scatter_chart(entered_site, payload):        
    filtered_df = spacex_df
    low, high = payload
    if entered_site == 'ALL':        
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    else:
        low, high = payload
        filtered_df = spacex_df[(spacex_df['Launch Site'] == entered_site) & (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
                
    fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version", size='Payload Mass (kg)', hover_data=['Payload Mass (kg)'])

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
