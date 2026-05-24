---
domain: huggingface.co
fetch_date: '2026-05-18T12:35:05.768382'
status: ok
url: https://huggingface.co/datasets/Locutusque/function-calling-chatml
---

![](https://cdn-avatars.huggingface.co/v1/production/uploads/68485b28c949339ca04c370c/U8ZDn5JZDJ0wr2nCCWUKZ.png)

#### dphn/dolphin-2.9.1-yi-1.5-34b

Text Generation • 34B • Updated • 4.74M • 63

system_message stringclasses 2
values | function_description stringlengths 0 5.86k | conversations listlengths 3 23 |
|---|---|---|
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "get_exchange_rate",
"description": "Get the exchange rate between two currencies",
"parameters": {
"type": "object",
"properties": {
"base_currency": {
"type": "string",
"description": "The currency to convert from"
},
... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"get_exchange_rate\",\n \"description\": \"Get the exchange rate between two currencies\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "get_news_headlines",
"description": "Get the latest news headlines",
"parameters": {
"type": "object",
"properties": {
"country": {
"type": "string",
"description": "The country for which to fetch news"
}
},
"... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"get_news_headlines\",\n \"description\": \"Get the latest news headlines\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\n ... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "generate_password",
"description": "Generate a random password",
"parameters": {
"type": "object",
"properties": {
"length": {
"type": "integer",
"description": "The length of the password"
},
"include_symbols": {... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"generate_password\",\n \"description\": \"Generate a random password\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\n ... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "generate_password",
"description": "Generate a random password with specified criteria",
"parameters": {
"type": "object",
"properties": {
"length": {
"type": "integer",
"description": "The length of the password"
},
... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"generate_password\",\n \"description\": \"Generate a random password with specified criteria\",\n \"parameters\": {\n \"type\": \"object\",\n \"prope... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "calculate_median",
"description": "Calculate the median of a list of numbers",
"parameters": {
"type": "object",
"properties": {
"numbers": {
"type": "array",
"items": {
"type": "number"
},
... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"calculate_median\",\n \"description\": \"Calculate the median of a list of numbers\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "calculate_loan_payment",
"description": "Calculate the monthly payment for a loan",
"parameters": {
"type": "object",
"properties": {
"principal": {
"type": "number",
"description": "The principal amount of the loan"
},
... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"calculate_loan_payment\",\n \"description\": \"Calculate the monthly payment for a loan\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "convert_temperature",
"description": "Convert temperature from one unit to another",
"parameters": {
"type": "object",
"properties": {
"temperature": {
"type": "number",
"description": "The temperature value"
},
"... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"convert_temperature\",\n \"description\": \"Convert temperature from one unit to another\",\n \"parameters\": {\n \"type\": \"object\",\n \"propertie... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "get_movie_details",
"description": "Get details of a movie",
"parameters": {
"type": "object",
"properties": {
"movie_title": {
"type": "string",
"description": "The title of the movie"
}
},
"required": [
... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"get_movie_details\",\n \"description\": \"Get details of a movie\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\n \"mo... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "calculate_tip",
"description": "Calculate the tip amount for a bill",
"parameters": {
"type": "object",
"properties": {
"bill_amount": {
"type": "number",
"description": "The total bill amount"
},
"tip_percentage"... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"calculate_tip\",\n \"description\": \"Calculate the tip amount for a bill\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\n ... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "create_contact",
"description": "Create a new contact",
"parameters": {
"type": "object",
"properties": {
"name": {
"type": "string",
"description": "The name of the contact"
},
"email": {
"type": ... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"create_contact\",\n \"description\": \"Create a new contact\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\n \"name\":... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "create_calendar_event",
"description": "Create a new calendar event",
"parameters": {
"type": "object",
"properties": {
"title": {
"type": "string",
"description": "The title of the event"
},
"start_time": {
... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"create_calendar_event\",\n \"description\": \"Create a new calendar event\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\n ... |
You are a helpful assistant, with no access to external functions. | [
{
"from": "system",
"value": "You are a helpful assistant, with no access to external functions."
},
{
"from": "human",
"value": "You are given a sequence of numbers: 2, 4, 6, 8, 10. Each number represents a moment in time, just like the waves in the ocean. As you continue the sequence, you noti... | |
You are a helpful assistant, with no access to external functions. | [
{
"from": "system",
"value": "You are a helpful assistant, with no access to external functions."
},
{
"from": "human",
"value": "What could be the potential cause of a loud knocking sound and engine slowdown in a 2010 Toyota Camry with a 4-cylinder engine, given the following diagnostic trouble... | |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "search_movie",
"description": "Search for a movie by title",
"parameters": {
"type": "object",
"properties": {
"title": {
"type": "string",
"description": "The title of the movie"
}
},
"required": [
... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"search_movie\",\n \"description\": \"Search for a movie by title\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\n \"ti... |
You are a helpful assistant, with no access to external functions. | [
{
"from": "system",
"value": "You are a helpful assistant, with no access to external functions."
},
{
"from": "human",
"value": "What are some practical tips and guidance we can provide in an excel table format to motivate individuals to make healthy food choices and empower them to cook nutrit... | |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "get_stock_price",
"description": "Get the current stock price",
"parameters": {
"type": "object",
"properties": {
"stock_symbol": {
"type": "string",
"description": "The symbol of the stock, e.g. AAPL"
}
},
"r... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"get_stock_price\",\n \"description\": \"Get the current stock price\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\n \... |
You are a helpful assistant, with no access to external functions. | [
{
"from": "system",
"value": "You are a helpful assistant, with no access to external functions."
},
{
"from": "human",
"value": "Enumerate five unique properties that differentiate maritime polar and continental tropical air masses based on their temperature, humidity, and pressure."
},
{
... | |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "calculate_loan_payment",
"description": "Calculate the monthly payment amount for a loan",
"parameters": {
"type": "object",
"properties": {
"loan_amount": {
"type": "number",
"description": "The total loan amount"
},
... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"calculate_loan_payment\",\n \"description\": \"Calculate the monthly payment amount for a loan\",\n \"parameters\": {\n \"type\": \"object\",\n \"pro... |
You are a helpful assistant, with no access to external functions. | [
{
"from": "system",
"value": "You are a helpful assistant, with no access to external functions."
},
{
"from": "human",
"value": "What is the mathematical formula to determine the maximum number of different ways a common kitchen item can be utilized? Hint: Consider the number of different surfa... | |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "get_news",
"description": "Get the latest news headlines",
"parameters": {
"type": "object",
"properties": {},
"required": []
}
} | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"get_news\",\n \"description\": \"Get the latest news headlines\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {},\n \"requir... |
You are a helpful assistant, with no access to external functions. | [
{
"from": "system",
"value": "You are a helpful assistant, with no access to external functions."
},
{
"from": "human",
"value": "What is the Python code for implementing a function that determines whether a given string is a palindrome or not? Please provide the code and explain your reasoning ... | |
You are a helpful assistant, with no access to external functions. | [
{
"from": "system",
"value": "You are a helpful assistant, with no access to external functions."
},
{
"from": "human",
"value": "What is the C++ code for creating a function that generates a simile to describe a given setting? The function should take in the setting as input and output a simile... | |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "calculate_tip",
"description": "Calculate the tip amount",
"parameters": {
"type": "object",
"properties": {
"bill_amount": {
"type": "number",
"description": "The total bill amount"
},
"tip_percentage": {
... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"calculate_tip\",\n \"description\": \"Calculate the tip amount\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\n \"bill... |
You are a helpful assistant, with no access to external functions. | [
{
"from": "system",
"value": "You are a helpful assistant, with no access to external functions."
},
{
"from": "human",
"value": "Using Python programming language, create a function that can identify the pattern of the numbered sequence 1, 4, 7, 10, etc., and output the formula for generating t... | |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "generate_random_number",
"description": "Generate a random number within a given range",
"parameters": {
"type": "object",
"properties": {
"min": {
"type": "number",
"description": "The minimum value of the range"
},
... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"generate_random_number\",\n \"description\": \"Generate a random number within a given range\",\n \"parameters\": {\n \"type\": \"object\",\n \"prope... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "search_books",
"description": "Search for books based on title, author, or genre",
"parameters": {
"type": "object",
"properties": {
"title": {
"type": "string",
"description": "The title of the book"
},
"author":... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"search_books\",\n \"description\": \"Search for books based on title, author, or genre\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\... |
You are a helpful assistant, with no access to external functions. | [
{
"from": "system",
"value": "You are a helpful assistant, with no access to external functions."
},
{
"from": "human",
"value": "How does the endocannabinoid system affect the immune system?"
},
{
"from": "gpt",
"value": "The endocannabinoid system (ECS) plays an essential role in r... | |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "generate_password",
"description": "Generate a random password",
"parameters": {
"type": "object",
"properties": {
"length": {
"type": "integer",
"description": "The length of the password"
},
"include_numbers": {... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"generate_password\",\n \"description\": \"Generate a random password\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\n ... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "convert_currency",
"description": "Convert currency from one unit to another",
"parameters": {
"type": "object",
"properties": {
"amount": {
"type": "number",
"description": "The amount to be converted"
},
"from_c... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"convert_currency\",\n \"description\": \"Convert currency from one unit to another\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "calculate_distance",
"description": "Calculate the distance between two points",
"parameters": {
"type": "object",
"properties": {
"lat1": {
"type": "number",
"description": "The latitude of point 1"
},
"lon1": {
... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"calculate_distance\",\n \"description\": \"Calculate the distance between two points\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\":... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "get_lyrics",
"description": "Get the lyrics of a song",
"parameters": {
"type": "object",
"properties": {
"song": {
"type": "string",
"description": "The name of the song"
},
"artist": {
"type": "s... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"get_lyrics\",\n \"description\": \"Get the lyrics of a song\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\n \"song\":... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "generate_random_number",
"description": "Generate a random number within a specified range",
"parameters": {
"type": "object",
"properties": {
"min": {
"type": "integer",
"description": "The minimum value of the range"
},
... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"generate_random_number\",\n \"description\": \"Generate a random number within a specified range\",\n \"parameters\": {\n \"type\": \"object\",\n \"p... |
You are a helpful assistant, with no access to external functions. | [
{
"from": "system",
"value": "You are a helpful assistant, with no access to external functions."
},
{
"from": "human",
"value": "As a manager of a sales team, you want to increase the motivation of your sales representatives to meet the sales target. To achieve this, you have implemented five d... | |
You are a helpful assistant, with no access to external functions. | [
{
"from": "system",
"value": "You are a helpful assistant, with no access to external functions."
},
{
"from": "human",
"value": "Provide a list of three commonly used websites that are popular amongst internet users worldwide. This list should include websites that are frequently visited for a ... | |
You are a helpful assistant, with no access to external functions. | [
{
"from": "system",
"value": "You are a helpful assistant, with no access to external functions."
},
{
"from": "human",
"value": "Can you create a series of clues that will lead to the main points of a speech on green energy? Each clue should give a hint towards one of the main points, and when ... | |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "search_book",
"description": "Search for books based on user preferences",
"parameters": {
"type": "object",
"properties": {
"author": {
"type": "string",
"description": "The author of the book"
},
"genre": {
... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"search_book\",\n \"description\": \"Search for books based on user preferences\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\n ... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "get_movie_details",
"description": "Get details of a movie",
"parameters": {
"type": "object",
"properties": {
"title": {
"type": "string",
"description": "The title of the movie"
},
"year": {
"typ... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"get_movie_details\",\n \"description\": \"Get details of a movie\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\n \"ti... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "search_books",
"description": "Search for books based on title or author",
"parameters": {
"type": "object",
"properties": {
"query": {
"type": "string",
"description": "The title or author to search for"
}
},
... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"search_books\",\n \"description\": \"Search for books based on title or author\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\n ... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "search_movies",
"description": "Search for movies based on specified criteria",
"parameters": {
"type": "object",
"properties": {
"genre": {
"type": "string",
"description": "The genre of the movie"
},
"year": {
... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"search_movies\",\n \"description\": \"Search for movies based on specified criteria\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": ... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "calculate_bmi",
"description": "Calculate the BMI (Body Mass Index)",
"parameters": {
"type": "object",
"properties": {
"weight": {
"type": "number",
"description": "The weight of the person in kilograms"
},
"heig... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"calculate_bmi\",\n \"description\": \"Calculate the BMI (Body Mass Index)\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\n ... |
You are a helpful assistant, with no access to external functions. | [
{
"from": "system",
"value": "You are a helpful assistant, with no access to external functions."
},
{
"from": "human",
"value": "In the context of online shopping, what are the most significant challenges that customers face, and how do these challenges impact their overall shopping experience?... | |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "search_news",
"description": "Search for news articles based on keywords",
"parameters": {
"type": "object",
"properties": {
"keywords": {
"type": "array",
"items": {
"type": "string"
},
... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"search_news\",\n \"description\": \"Search for news articles based on keywords\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\n ... |
You are a helpful assistant, with no access to external functions. | [
{
"from": "system",
"value": "You are a helpful assistant, with no access to external functions."
},
{
"from": "human",
"value": "Which R code can be used to identify scientific research institutes in France for a biotech-related task?\nHere's a sample R code that uses the \"europe\" dataset to ... | |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "calculate_loan_payment",
"description": "Calculate the monthly loan payment",
"parameters": {
"type": "object",
"properties": {
"loan_amount": {
"type": "number",
"description": "The total loan amount"
},
"interes... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"calculate_loan_payment\",\n \"description\": \"Calculate the monthly loan payment\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "check_email_availability",
"description": "Check if an email address is available or already taken",
"parameters": {
"type": "object",
"properties": {
"email": {
"type": "string",
"description": "The email address to be checked"
... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"check_email_availability\",\n \"description\": \"Check if an email address is available or already taken\",\n \"parameters\": {\n \"type\": \"object\",\n ... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "search_movies",
"description": "Search for movies based on title or genre",
"parameters": {
"type": "object",
"properties": {
"keyword": {
"type": "string",
"description": "The keyword to search for"
},
"genre": {... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"search_movies\",\n \"description\": \"Search for movies based on title or genre\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\n ... |
You are a helpful assistant, with no access to external functions. | [
{
"from": "system",
"value": "You are a helpful assistant, with no access to external functions."
},
{
"from": "human",
"value": "Can you write a shell command to count the number of letters in each word of a given sentence and add them up to get a total number? Then use that number as a clue to... | |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "search_restaurants",
"description": "Search for restaurants based on the given criteria",
"parameters": {
"type": "object",
"properties": {
"cuisine": {
"type": "string",
"description": "The cuisine type"
},
"loca... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"search_restaurants\",\n \"description\": \"Search for restaurants based on the given criteria\",\n \"parameters\": {\n \"type\": \"object\",\n \"prop... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "generate_password",
"description": "Generate a random password",
"parameters": {
"type": "object",
"properties": {
"length": {
"type": "integer",
"description": "The length of the password"
},
"include_numbers": {... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"generate_password\",\n \"description\": \"Generate a random password\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\n ... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "calculate_age",
"description": "Calculate the age based on date of birth",
"parameters": {
"type": "object",
"properties": {
"date_of_birth": {
"type": "string",
"description": "The date of birth"
}
},
"requir... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"calculate_age\",\n \"description\": \"Calculate the age based on date of birth\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\n ... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "create_calendar_event",
"description": "Create a new calendar event",
"parameters": {
"type": "object",
"properties": {
"title": {
"type": "string",
"description": "The title of the event"
},
"start_time": {
... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"create_calendar_event\",\n \"description\": \"Create a new calendar event\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\n ... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "calculate_discount",
"description": "Calculate the discounted price of a product",
"parameters": {
"type": "object",
"properties": {
"original_price": {
"type": "number",
"description": "The original price of the product"
},
... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"calculate_discount\",\n \"description\": \"Calculate the discounted price of a product\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\... |
You are a helpful assistant, with no access to external functions. | [
{
"from": "system",
"value": "You are a helpful assistant, with no access to external functions."
},
{
"from": "human",
"value": "Can you create a new magical creature struct in Go with the following attributes: name (string), element (string), abilities (slice of strings), and description (stri... | |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "get_movie_info",
"description": "Get detailed information about a movie",
"parameters": {
"type": "object",
"properties": {
"title": {
"type": "string",
"description": "The title of the movie"
},
"year": {
... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"get_movie_info\",\n \"description\": \"Get detailed information about a movie\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\n ... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "search_recipe",
"description": "Search for a recipe based on ingredients",
"parameters": {
"type": "object",
"properties": {
"ingredients": {
"type": "array",
"items": {
"type": "string"
},
... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"search_recipe\",\n \"description\": \"Search for a recipe based on ingredients\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\n ... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "search_movies",
"description": "Search for movies based on title, actor, or genre",
"parameters": {
"type": "object",
"properties": {
"search_query": {
"type": "string",
"description": "The search query for movies"
}
... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"search_movies\",\n \"description\": \"Search for movies based on title, actor, or genre\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties... |
You are a helpful assistant with access to the following functions. Use them if required - | {
"name": "get_definition",
"description": "Get the definition of a word",
"parameters": {
"type": "object",
"properties": {
"word": {
"type": "string",
"description": "The word to get the definition of"
}
},
"required":... | [
{
"from": "system",
"value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"get_definition\",\n \"description\": \"Get the definition of a word\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\n \... |
You are a helpful assistant, with no access to external functions. | [
{
"from": "system",
"value": "You are a helpful assistant, with no access to external functions."
},
{
"from": "human",
"value": "Your task is to create a web page that displays a summary of a famous scientist's life and achievements. The information to include is:\n- The scientist was a British... | |
You are a helpful assistant, with no access to external functions. | [
{
"from": "system",
"value": "You are a helpful assistant, with no access to external functions."
},
{
"from": "human",
"value": "A small business sells handcrafted goods. They have a collection of 10 unique items. The price of each item is a prime number ranging from 2 to 29 dollars. The sum of... |

Converted glaiveai/Glaive-function-calling-v2 to chatml format.

```
[ { "from": "system", "value": "You are a helpful assistant with access to the following functions. Use them if required -{\n \"name\": \"create_contact\",\n \"description\": \"Create a new contact\",\n \"parameters\": {\n \"type\": \"object\",\n \"properties\": {\n \"name\": {\n \"type\": \"string\",\n \"description\": \"The name of the contact\"\n },\n \"email\": {\n \"type\": \"string\",\n \"description\": \"The email address of the contact\"\n }\n },\n \"required\": [\n \"name\",\n \"email\"\n ]\n }\n}" }, { "from": "human", "value": "I need to create a new contact for my friend John Doe. His email is johndoe@example.com." }, { "from": "function-call", "value": "{\"name\": \"create_contact\", \"arguments\": '{\"name\": \"John Doe\", \"email\": \"johndoe@example.com\"}'}" }, { "from": "function-response", "value": "{\"status\": \"success\", \"message\": \"Contact for John Doe with email johndoe@example.com has been created successfully.\"}" }, { "from": "gpt", "value": "I have successfully created a new contact for your friend John Doe with the email johndoe@example.com." } ]
```
