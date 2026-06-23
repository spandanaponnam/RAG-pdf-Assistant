from dotenv import load_dotenv
from openai import OpenAI
import json
import requests
import os

load_dotenv()
client = OpenAI(
    base_url='YOUR_API_BASE_URL',
    api_key="YOUR_API_KEY",  # required but ignored
)

def get_weather(city: str): #weather api calling logic
    url = f"OPEN_SOURCE_WEATHER_API_LINK" #open source weather api, we don't need to create apis for weather
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    
    return "Something went wrong"

def run_command(cmd: str): #executing system commands logic
    result = os.system(cmd)
    return result
def get_stock_data(symbol: str):
    if not symbol:
        return "Please provide a stock symbol like TSLA, AAPL, MSFT"

    symbol = str(symbol)


    api_key = os.getenv("API_KEY")

    url = (
        f"OPEN_SOURCE_STOCK_API_LINK"
        f"?function=GLOBAL_QUOTE"
        f"&symbol={symbol.upper()}"
        f"&apikey={api_key}"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return "Failed to fetch stock data"

    data = response.json()

    if "Global Quote" not in data:
        return f"No stock data found for {symbol}"

    quote = data["Global Quote"]

    return (
    f"Stock: {quote.get('01. symbol')}\n"
    f"Price: ${quote.get('05. price')}\n"
    f"Change: {quote.get('09. change')}\n"
    f"Percent Change: {quote.get('10. change percent')}"
    )

available_tools = {
    "get_weather": get_weather, #using get_weather function where we designed our weather api calling logic
    "run_command": run_command, #using run_commad function where we designed our running system commands logic.
    "get_stock_data": get_stock_data

}
SYSTEM_PROMPT = """
You are a helpful AI assistant.

You always reply ONLY valid JSON.

For every user query follow:

1. plan
2. action (only if tool needed)
3. observe
4. output


JSON formats:

Plan:
{
 "step":"plan",
 "content":"what you are planning"
}


Action:
{
 "step":"action",
 "function":"tool name",
 "input":"tool input"
}


Output:
{
 "step":"output",
 "content":"final answer"
}


Tools:

get_weather:
input = city name

get_stock_data:
input = stock symbol only

Examples:

User:
what is Tesla stock price?

You return:

{
 "step":"action",
 "function":"get_stock_data",
 "input":"TSLA"
}


For company names convert:

Infosys = INFY
Apple = AAPL
Tesla = TSLA
Microsoft = MSFT
"""
#agent-
# agent.py

def run_agent(prompt):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    for _ in range(10):

        response = client.chat.completions.create(
        model="MODEL_NAME",
        messages=messages,
        temperature=0,
        max_tokens=300
        )

        raw = response.choices[0].message.content

        print("MODEL RESPONSE:")
        print(raw)

        try:
            data = json.loads(raw)

        except Exception:
            return raw


        step = data.get("step")


        if step == "plan":

            messages.append(
                {
                    "role": "assistant",
                    "content": raw
                }
            )

            continue


        elif step == "action":

            function_name = data.get("function")
            tool_input = data.get("input")

    # normalize name
            function_name = function_name.lower()
            function_name = function_name.replace(" ", "_")

            print("Calling tool:", function_name)

            if function_name in available_tools:

                result = available_tools[function_name](tool_input)

            else:
                result = f"Tool {function_name} not found"


            messages.append(
            {
                "role":"assistant",
                "content":raw
            }
            )

            messages.append(
            {
                "role":"user",
                "content":json.dumps({
                "step":"observe",
                "content":result
            })
            }
            )

            continue

        elif step == "output":

            return data.get("content")


    return "Agent reached maximum steps"
