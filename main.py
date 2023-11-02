from flask import Flask, render_template, request
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

app = Flask(__name__)

color_map = {
    'blue': '#1f77b4',
    'orange': '#ff7f0e',
    'green': '#2ca02c',
    # Add more colors as needed
}

def create_bar_chart(data, color):
    if 'Category' in data.columns and 'Value' in data.columns:
        fig = px.bar(data, x='Category', y='Value', labels={'Value': 'Values'}, title='Sample Bar Chart', color_discrete_sequence=[color])
        return fig.to_html(full_html=False)
    else:
        return 'Error: Missing required columns in data.'

def create_line_chart(data, color):
    fig = go.Figure(data=go.Scatter(x=data['Category'], y=data['Value'], mode='lines', line=dict(color=color)))
    fig.update_layout(title='Sample Line Chart')
    return fig.to_html(full_html=False)

def create_pie_chart(data):
    fig = px.pie(data, values='Value', names='Category', title='Sample Pie Chart')
    return fig.to_html(full_html=False)

def create_histogram(data):
    fig = px.histogram(data, x='Value', nbins=5, title='Sample Histogram')
    return fig.to_html(full_html=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data_file = request.files['data_file']
        try:
            data = pd.read_csv(data_file)
        except pd.errors.EmptyDataError:
            data = pd.DataFrame()

        chart_type = request.form.get('chart_type', 'bar')
        color_name = request.form.get('color', 'blue')
        color = color_map.get(color_name, '#1f77b4')

        if chart_type == 'bar':
            chart = create_bar_chart(data, color)
        elif chart_type == 'line':
            chart = create_line_chart(data, color)
        elif chart_type == 'pie':
            chart = create_pie_chart(data)
        elif chart_type == 'histogram':
            chart = create_histogram(data)
        else:
            chart = ''

        return render_template('index.html', chart=chart)
    else:
        return render_template('index.html')


#Main
if __name__ == '__main__':
    app.run(debug=True)