import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import seaborn as sns

df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")

import preprocessor
import helper

df = preprocessor.preprocess(df, region_df)

st.sidebar.image("oo.jpeg", use_column_width=True)
st.sidebar.title("Olympics Analysis")

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Dataset', 'Medal Tally', 'Overall Analysis', 'Athlete wise Analysis')
)

if user_menu == 'Dataset':
    st.title("120 years of Olympic history")
    st.dataframe(df)



if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")

    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")

    st.table(medal_tally)


if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        # st.title(editions)
        st.subheader(editions)
    with col2:
        st.header("Hosts")
        st.subheader(cities)
    with col3:
        st.header("Sports")
        st.subheader(sports)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.subheader(events)
    with col2:
        st.header("Nations")
        st.subheader(nations)
    with col3:
        st.header("Athletes")
        st.subheader(athletes)

    st.write("")
    st.write("")

    ############################################################

    nations_over_time = helper.participating_countries_over_time(df)
    fig = px.line(nations_over_time, x = 'Year', y = 'Number of countries')
    st.title("Participating Nations Over the Years")
    st.plotly_chart(fig)

    st.write("")
    st.write("")

    #############################################################

    st.title("Number of Events in every Sport")
    
    fig, ax = plt.subplots(figsize=(18,18))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index = 'Sport', columns = 'Year', values = 'Event', aggfunc='count').fillna(0).astype(int))

    st.pyplot(fig)

    st.write("")
    st.write("")

    ##############################################################

    st.title("Most Successful athletes")

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select sport', sport_list)

    x = helper.most_successful(df, selected_sport)
    st.dataframe(x)




if user_menu == 'Athlete wise Analysis':

    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    
    # Plot KDE for each category
    plt.figure(figsize=(10, 6))
    sns.kdeplot(x1, label='Overall Age', shade=True)
    sns.kdeplot(x2, label='Gold Medalist', shade=True)
    sns.kdeplot(x3, label='Silver Medalist', shade=True)
    sns.kdeplot(x4, label='Bronze Medalist', shade=True)
    
    # Customize plot
    plt.title('Distribution of Age')
    plt.xlabel('Age')
    plt.ylabel('Density')
    plt.legend()

    st.title("Distribution of Age")
    st.pyplot(plt)

    

    #athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    #x1 = athlete_df['Age'].dropna()
    #x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    # x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    # x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    # fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    # fig.update_layout(autosize=False,width=1000,height=600)
    # st.title("Distribution of Age")
    # st.plotly_chart(fig)

    # st.write("")
    # st.write("")

    ################################################


    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    
    # Collect age data for Gold Medalists in each sport
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        gold_medal_ages = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()
        if not gold_medal_ages.empty:
            x.append(gold_medal_ages)
            name.append(sport)
    
    # Create a new figure
    plt.figure(figsize=(12, 8))
    
    # Plot KDE for each sport
    for ages, sport_name in zip(x, name):
        sns.kdeplot(ages, label=sport_name, shade=True)
    
    # Customize plot
    plt.title('Distribution of Age of Gold Medalists by Sport')
    plt.xlabel('Age')
    plt.ylabel('Density')
    plt.legend(title='Sport')
    
    # Show plot in Streamlit
    st.title("Distribution of Age wrt Sports (Gold Medalist)")
    st.pyplot(plt)
        

    # x = []
    # name = []
    # famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
    #                  'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
    #                  'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
    #                  'Water Polo', 'Hockey', 'Rowing', 'Fencing',
    #                  'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
    #                  'Tennis', 'Golf', 'Softball', 'Archery',
    #                  'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
    #                  'Rhythmic Gymnastics', 'Rugby Sevens',
    #                  'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    # for sport in famous_sports:
    #     temp_df = athlete_df[athlete_df['Sport'] == sport]
    #     x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
    #     name.append(sport)

    # fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    # fig.update_layout(autosize=False, width=1000, height=600)
    # st.title("Distribution of Age wrt Sports(Gold Medalist)")
    # st.plotly_chart(fig)

    st.write("")
    st.write("")

    ############################################

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    
    # Set up Streamlit title and selectbox
    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    
    # Retrieve data for the selected sport
    temp_df = helper.weight_v_height(df, selected_sport)
    
    # Create scatter plot
    fig, ax = plt.subplots(figsize=(10, 6))  # Specify figure size if needed
    sns.scatterplot(x='Weight', y='Height', hue='Medal', style='Sex', data=temp_df, s=60, ax=ax)
    
    # Customize plot
    ax.set_title('Height vs Weight by Medal and Sex')
    ax.set_xlabel('Weight')
    ax.set_ylabel('Height')
    
    # Display the plot in Streamlit
    st.pyplot(fig)



    # sport_list = df['Sport'].unique().tolist()
    # sport_list.sort()
    # sport_list.insert(0, 'Overall')

    # st.title('Height Vs Weight')
    # selected_sport = st.selectbox('Select a Sport', sport_list)
    # temp_df = helper.weight_v_height(df,selected_sport)
    # fig,ax = plt.subplots()
    # ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    # st.pyplot(fig)

    st.write("")
    st.write("")

    ############################################

    st.title("Men Vs Women Participation")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

