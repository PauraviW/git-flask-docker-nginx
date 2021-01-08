Hi, Welcome to the Park Suggestion System!

This System displays the best parks for the user to visit based on his location, maximum travel distance and his favourite weather.  

Assumptions:
1) Best Weather : I think every user may have different preferences about "best" weather. Thus, getting that information from user will help.
2) Travel within 7 days: Since, the OpenWeather API forecasts for the next 7 days, I assumed that we will generate forecast for the next 7 days only.
3) Park Selection: Since, the user wishes to travel within a stipulated radius, I selected such parks that belong in that radius and then sorted them as per their dates and distances. 

The documentation for this API is in the API Information.docx

To use this app, please follow the given steps:
1) Open the terminal in this folder and run the file app1.py
	'python app1.py'
2) Open another terminal and try to run any of the following URLS:  
	a)	curl -i http://localhost:5000/suggestParks/api/v1.0/parks/latitude/42.2/longitude/-71.5/radius/23/weather/Clouds  
	b)  curl -i http://localhost:5000/suggestParks/api/v1.0/parks/latitude/40.2/longitude/-73.5/radius/2/weather/Clear