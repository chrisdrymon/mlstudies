import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd


def initial_layout():
    """Create the layout displayed when the page is first loaded. Should be a blank graph."""
    return html.Main([
        html.Button(id='next-epoch', children='Epoch 0'),
        dcc.Graph(id='figure', figure=fig)])


def activation(x, y, g_weights):
    """Return 0 or 1 according this activation function."""
    if g_weights[-1][0] + x*g_weights[-1][1] + y*g_weights[-1][2] > 0:
        return 1
    else:
        return 0


def update(f_weights):
    adjusted = True
    while adjusted is True:
        adjusted = False
        for i in range(len(data['x'])):
            if activation(data['x'][i], data['y'][i], f_weights) != data['label'][i]:
                adjusted = True
                delta = learning_rate * (data['label'][i] - activation(data['x'][i], data['y'][i], f_weights))
                new_weights = [0]*3
                new_weights[0] = f_weights[-1][0] + delta
                new_weights[1] = f_weights[-1][1] + delta * data['x'][i]
                new_weights[2] = f_weights[-1][2] + delta * data['y'][i]
                f_weights.append(new_weights)
            print(i, weights[-1])
    return f_weights


weights = [[0, 0, 0]]
data = {'x': [.5, 3, .26, .35, .45, .6, .7, .92], 'y': [.72, 1, .58, .95, .15, .3, .65, .45],
        'label': [1, 0, 1, 0, 1, 1, 0, 0]}
df = pd.DataFrame.from_dict(data)
learning_rate = 1
final_weights = update(weights)
dividing_line = []
print(len(final_weights))
for item in final_weights:
    print(item)

# This is for plotting the dividing line
for triplet in final_weights[1:]:
    # y-intercept calculation: x = -bias/a
    # x-intercept calculation: y = -bias/b
    if triplet[0] != 0:
        dividing_line.append([[0, -triplet[0]/triplet[2]], [-triplet[0]/triplet[1], 0]])

fig = px.scatter(x=df['x'], y=df['y'])
fig.update_layout(height=900, width=900, paper_bgcolor='#2C2D30', plot_bgcolor='#5D6F81', font_color='#D5C6BA',
                  legend_bgcolor='#C94827')
fig.update_traces(marker_symbol='circle-dot', marker_size=15, marker_color=df['label'],
                  marker_colorscale=['#E9CF7A', '#C94827'])

app = dash.Dash()
app.title = 'Perceptron'
app.layout = initial_layout()


@app.callback(
    [dash.dependencies.Output('figure', 'figure'),
     dash.dependencies.Output('next-epoch', 'children')],
    [dash.dependencies.Input('next-epoch', 'n_clicks')],
    [dash.dependencies.State('figure', 'figure')]
)
def update_output(click, figure):
    if click is None:
        click = 0
    if click >= len(dividing_line):
        return figure, f'Problem Solved!'
    figure['data'].append({'name': f'Update {click + 1}', 'x': dividing_line[click][1], 'y': dividing_line[click][0],
                           'line': {'color': '#2C2D30'}})
    return figure, f'Update {click + 2}'


app.run_server(debug=True, use_reloader=False)
