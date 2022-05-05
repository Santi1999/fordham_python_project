## User interface for FixedRateBond using Streamlit

from ecom_scrape import makedf
import streamlit as st

# Get inputs from Streamlit fields
def getSearch():
    search = st.text_input('What would you like to search for:', key='search_input_field')
    try:    search_input = str(search)
    except: search_input = None


    st.write(search_input)
    return search_input
    st.write(search_input)
   

# Display the cashflow schedule table and its bar chart
def displayResults(search_input):
   # if any inputs are None, the short-circuit return (no result display)
   if search_input == None:
       return

   
   item = makedf(search_input) # this is where we are going to use the function form the other files


   df = item.ebdf() # generate the cashflows
   df # display the DataFrame
#    df.set_index(['Date'],inplace=True)
#    st.bar_chart(df) # display the dataFrame as a bar chart

st.header('Item Price Finder')

# INPUT: Get inputs
search = getSearch()

# For debugging - show inputs
st.write(search)

# OUTPUT: Call the displayResults() function
displayResults(search)
