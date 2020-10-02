# MSFeeDashboard : Post Graduate college visualiser
##This is a dashboard based on Python’s framework Dash and Plotly. We have scraped college data for post graduate studies from the web using the Requests library from public websites like Yocket.in. 

The first plot is a choropleth map showing the distribution of colleges in the dataset. Hovering over a country reveals its most popular colleges and the total count.

<img src= "docs/Screenshot1.png">

A drop down menu allows you to view by country (currently only USA has been supported)
<img src = "docs/Screenshot4.png">

The second map is a heatmap showing deviation from the average fee in that country. Hovering over each state shows the top 5 universities and its deviation from the average
