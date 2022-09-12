import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError



streamlit.title("My parents new healthy diner")

streamlit.header("Breakfast Menu")
streamlit.text("🥣 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard-Boiled Free-Range Egg")
streamlit.text("🥑🍞 Avocado Toast")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

# write your own comment -what does the next line do? 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)


streamlit.text("FruityVice Fruit Advice")
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
my_data_row = my_cur.fetchall()
streamlit.text("Hello from Snowflake:")
streamlit.dataframe(my_data_row)
fruit_choice1 = streamlit.text_input('What fruit would you like information about?','banana')
streamlit.write('The user entered ', fruit_choice1)

fruits_to_show1 = my_fruit_list.loc[fruit_choice1]
# Display the table on the page.
streamlit.dataframe(fruits_to_show1)

#This will not work correctly, but just go with it for now
my_cur.execute("INSERT INTO PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST VALUES('from streamlit')")
