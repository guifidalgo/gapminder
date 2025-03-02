import streamlit as st
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('gapminder.csv')
st.set_page_config(page_title='Gapminder', page_icon=':earth_americas:', layout='wide')

df_continents = df.groupby(['continent', 'year']).agg({'gdpPercap': 'mean', 'lifeExp': 'mean', 'pop': 'sum'}).reset_index()
df_years = df.groupby(['year']).agg({'gdpPercap': 'mean', 'lifeExp': 'mean', 'pop': 'sum'}).reset_index()

def page_header():
    st.title('Gapminder Dataset')
    st.write('This project utilizes the Gapminder dataset to analyze the relationship between GDP per capita, life expectancy, and population over time.')



def page_eda():
    st.header("Exploratory Data Analysis", divider=True)
    observations = df.shape[0]
    columns = df.shape[1]
    st.write(f'The dataset has {observations} observations and {columns} columns.')
    years = df['year'].unique().tolist()
    years = sorted(years)
    st.write(f'The dataset contains data for the years: {years}')
    
    # Calculate the amount of observations for each continent
    grouped_continent = df.groupby('continent').size().reset_index(name='count')
    st.dataframe(grouped_continent, hide_index=True)

    cols = st.columns([1,4,4])

    with cols[0]:
        selected_year = st.selectbox('Select a year', years)
    df_year = df[df['year'] == selected_year]

    fig1 = go.Figure()
    fig1.add_trace(go.Box(
        x=df_year['continent'],
        y=df_year['gdpPercap'],
        name='GDP per capita'
        ))
    fig1.update_layout(
    title='GDP per capita distribution',
    xaxis_title='GDP per capita',
    yaxis_title='Frequency'
    )
    fig2 = go.Figure()
    fig2.add_trace(go.Box(
        x=df_year['continent'],
        y=df_year['lifeExp'],
        name='Life Expectancy'
        ))
    fig2.update_layout(
    title='Life Expectancy distribution',
    xaxis_title='Life Expectancy',
    yaxis_title='Frequency'
    )

    cols[1].plotly_chart(fig1)
    cols[2].plotly_chart(fig2)

def page_global():
    st.header("Global Analysis", divider=True)

    fig1 = go.Figure()

    for continent in df['continent'].unique():
        fig1.add_trace(go.Scatter(
            x=df[df['continent'] == continent]['gdpPercap'],
            y=df[df['continent'] == continent]['lifeExp'],
            mode='markers',
            name=continent,
            hoverinfo='text',
            text='Country: ' + df[df['continent'] == continent]['country'] + '<br>Year: ' + df[df['continent'] == continent]['year'].astype(str)
        ))
    fig1.update_layout(
        title='Life Expectancy over time',
        xaxis_title='GDP per Capita',
        yaxis_title='Life Expectancy'
    )

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=df_years['year'],
        y=df_years['pop'],
        name='Population',
        hoverinfo='text',
        text = df_years['pop'].apply(lambda x: f'{x:,.0f}'),
        textposition='outside'
        
    ))
    fig2.update_layout(
        title='World Population over time',
        xaxis_title='Year',
        yaxis_title='Population'
    )

    st.plotly_chart(fig2)
    st.plotly_chart(fig1)

def page_continent():
    st.header("Continent Analysis",divider=True)
    
    cols = st.columns([1,3])
    selected_continent = cols[0].selectbox('Select a continent', df['continent'].unique())
    selected_years = cols[1].slider('Select a range of years', min_value=df['year'].min(), max_value=df['year'].max(), value=(df['year'].min(), df['year'].max()))
    min_year, max_year = selected_years

    dff = df_continents[(df_continents['continent'] == selected_continent) & (df_continents['year'] >= min_year) & (df_continents['year'] <= max_year)]
    dff_country = df[(df['continent'] == selected_continent) & (df['year'] >= min_year) & (df['year'] <= max_year)]

    fig1 = go.Figure()
    fig2 = go.Figure()
    fig3 = go.Figure()

    fig1.add_trace(go.Scatter(
        x=dff['year'],
        y=dff['gdpPercap'],
        mode='lines+markers',
        name='GDP per Capita'
    ))
    
    
    fig2.add_trace(go.Scatter(
        x=dff['year'],
        y=dff['lifeExp'],
        mode='lines+markers',
        name='Life Expectancy'
    ))
    fig3.add_trace(go.Scatter(
        x=dff['year'],
        y=dff['pop'],
        mode='lines+markers',
        name='Population'
    ))


    fig1.update_layout(
        title=f'{selected_continent} GDP per Capita over time',
        xaxis_title='Year',
        yaxis_title='GDP per Capita'
    )
    fig2.update_layout(
        title=f'{selected_continent} Life Expectancy over time',
        xaxis_title='Year',
        yaxis_title='Life Expectancy'
    )
    fig3.update_layout(
        title=f'{selected_continent} Population over time',
        xaxis_title='Year',
        yaxis_title='Population'
    )

    cols = st.columns(3)
    cols[0].plotly_chart(fig1)
    cols[1].plotly_chart(fig2)
    cols[2].plotly_chart(fig3)

    fig4 = go.Figure()
    for country in dff_country['country'].unique():
        df_country = dff_country[dff_country['country'] == country]
        fig4.add_trace(go.Scatter(
        x=df_country['gdpPercap'],
        y=df_country['lifeExp'],
        mode='markers',
        name=country,
        hoverinfo='text',
        text=df_country.apply(lambda row: f"Country: {row['country']}<br>Year: {row['year']}<br>Pop: {row['pop']:,}", axis=1)
    ))
    fig4.update_layout(
        title=f'{selected_continent} Life Expectancy vs GDP per Capita',
        xaxis_title='GDP per Capita',
        yaxis_title='Life Expectancy'
    )
    st.plotly_chart(fig4)

def page_country():
    st.header("Country Analysis", divider=True)
    cols=st.columns([1,1,2])
    selected_continent = cols[0].selectbox('Select a continent', df['continent'].unique(),key='countries_continent')
    selected_country = cols[1].selectbox('Select a country', df[df['continent'] == selected_continent]['country'].unique())
    selected_years = cols[2].slider('Select a range of years', min_value=df['year'].min(), max_value=df['year'].max(), value=(df['year'].min(), df['year'].max()),key='countries_years')
    min_year, max_year = selected_years
    dff = df[(df['continent'] == selected_continent) & (df['country'] == selected_country) & (df['year'] >= min_year) & (df['year'] <= max_year)]
    fig1 = go.Figure()
    fig2 = go.Figure()
    fig3 = go.Figure()
    fig4 = go.Figure()

    fig1.add_trace(go.Scatter(
        x=dff['year'],
        y=dff['gdpPercap'],
        mode='lines+markers',
        name='GDP per Capita'
    ))
    fig2.add_trace(go.Scatter(
        x=dff['year'],
        y=dff['lifeExp'],
        mode='lines+markers',
        name='Life Expectancy'
    ))
    fig3.add_trace(go.Scatter(
        x=dff['year'],
        y=dff['pop'],
        mode='lines+markers',
        name='Population'
    ))
    fig4.add_trace(go.Scatter(
        x=dff['gdpPercap'],
        y=dff['lifeExp'],
        mode='markers',
        name='Life Expectancy vs GDP per Capita',
        marker=dict(
            size=25,
            color=dff['year'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(
                title='Year',
                tickvals=dff['year'].unique(),
                ticktext=dff['year'].unique()
            )
        )
    ))

    fig1.update_layout(
        title=f'{selected_country} GDP per Capita over time',
        xaxis_title='Year',
        yaxis_title='GDP per Capita'
    )
    fig2.update_layout(
        title=f'{selected_country} Life Expectancy over time',
        xaxis_title='Year',
        yaxis_title='Life Expectancy'
    )
    fig3.update_layout(
        title=f'{selected_country} Population over time',
        xaxis_title='Year',
        yaxis_title='Population'
    )
    fig4.update_layout(
        title=f'{selected_country} Life Expectancy vs GDP per Capita',
        xaxis_title='GDP per Capita',
        yaxis_title='Life Expectancy'
    )


    cols = st.columns(3)
    cols[0].plotly_chart(fig1)
    cols[1].plotly_chart(fig2)
    cols[2].plotly_chart(fig3)
    st.plotly_chart(fig4)



def main():
    page_header()
    tabs = st.tabs(['EDA', 'Global', 'Continent', 'Country'])
    with tabs[0]:
        page_eda()
    with tabs[1]:
        page_global()
    with tabs[2]:
        page_continent()
    with tabs[3]:
        page_country()

if __name__ == '__main__':
    main()