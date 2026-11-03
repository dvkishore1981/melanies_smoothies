# Import python packages.
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app.
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write( "Choose the froots you want in your custom Smoothie:")

import streamlit as st

title = st.text_input("Name on Smoothie:")
st.write("The Name on the Smoothie will be:", title)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'))
##st.dataframe(data=my_dataframe, use_container_width=True)

Ingredients_list = st.multiselect(
    "Choose up to 5 Ingredients",my_dataframe, max_selections=5  
)
#st.write(Ingredients_list)

Ingredients_string = ''
name_on_order = ''

if Ingredients_list:    
    Ingredients_string = ''
    name_on_order = title

for fruit_chosen in Ingredients_list:
      Ingredients_string += fruit_chosen + ''
      smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
      st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + Ingredients_string + """', '""" +name_on_order+ """')"""

#st.write(my_insert_stmt)
#st.stop()

time_to_insert = st.button ('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")
