import streamlit as st
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('gapminder_unfiltered.csv')

st.set_page_config(page_title='Gapminder', page_icon=':earth_americas:', layout='wide')

continentes = df['continent'].unique().tolist()
continentes = sorted(continentes)
continente_selecionado = st.sidebar.selectbox('Continent', continentes)
dff = df[df['continent'] == continente_selecionado]

paises = dff['country'].unique().tolist()
paises = sorted(paises)
anos = dff['year'].unique().tolist()
ano_min = min(anos)
anos_max = max(anos)

pais_selecionado = st.sidebar.selectbox('Country', paises)
anos_selecionados = st.sidebar.slider('Years', ano_min, anos_max, (ano_min, anos_max))
ano_start = anos_selecionados[0]
ano_end = anos_selecionados[1]


dff = dff[(dff['country'] == pais_selecionado) & (dff['year'] >= ano_start) & (dff['year'] <= ano_end)]

fig1 = go.Figure(
    data = go.Scatter(
        x = dff['year'],
        y = dff['gdpPercap'],
        mode = 'lines+markers'
    )
)
fig1.update_layout(
    title=f'GDP per capita through the years',
    xaxis_title='Year',
    yaxis_title='GDP per capita'
)
fig2 = go.Figure(
    data = go.Scatter(
        x = dff['year'],
        y = dff['lifeExp'],
        mode = 'lines+markers'
    )
)
fig2.update_layout(
    title=f'Life Expectancy trough the years',
    xaxis_title='Year',
    yaxis_title='Life Expectancy'
)
fig3 = go.Figure(
    data = go.Scatter(
        x = dff['year'],
        y = dff['pop'],
        mode = 'lines+markers'
    )
)
fig3.update_layout(
    title=f'Population through the years',
    xaxis_title='Year',
    yaxis_title='Population'
)
st.header(f'{pais_selecionado}')
cols = st.columns(3)
cols[0].plotly_chart(fig1)
cols[1].plotly_chart(fig2)
cols[2].plotly_chart(fig3)

fig4 = go.Figure(
    data = go.Scatter(
        x = dff['gdpPercap'],
        y = dff['lifeExp'],
        mode = 'markers',
        marker=dict(
            size=dff['pop']/1e6,
            color=dff['year'],
            colorscale='Viridis',
        )
    )
)
fig4.update_layout(
    title=f'GDP per capita vs Life Expectancy',
    xaxis_title='GDP per capita',
    yaxis_title='Life Expectancy'
)

st.plotly_chart(fig4)