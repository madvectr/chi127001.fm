#! /usr/bin/env python
import datetime
from meta_ai_api import MetaAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI  
from langchain.output_parsers.json import SimpleJsonOutputParser
import json
from dotenv import load_dotenv

load_dotenv()

# Initialize the MetaAI model
meta_ai = MetaAI()
# Initialize the OpenAI model
chat = ChatOpenAI(  # Updated class
    model_name='gpt-4o',
    model_kwargs={"response_format": {"type": "json_object"}}
  )

# Load the template


def get_weather_report(city, date) -> dict:
    with open('prompts/morning_weather_report_template.txt', 'r') as file:
        template_morning_weather_report = file.read()
    response_morning_weather_report: dict = meta_ai.prompt(template_morning_weather_report.format(city=city, date=date))
    response_morning_weather_report = json.loads(response_morning_weather_report['message'])
    # Message already extracted from the response
    return response_morning_weather_report

def create_song(weather_report: dict) -> dict:
    with open('prompts/create_a_song_template.txt', 'r') as file:
        template_create_a_song = file.read()

    songs = {}
    for time, description in weather_report.items():
        prompt_template = ChatPromptTemplate.from_template(template_create_a_song)
        chain = prompt_template | chat | SimpleJsonOutputParser()
        response_create_a_song = chain.invoke({
            "time": time,
            "weather_description": description
        })
        songs[time] = response_create_a_song
    return songs


if __name__ == "__main__":
    weather_report = get_weather_report("Chicago", datetime.datetime.now().strftime("%Y-%m-%d"))
    songs = create_song(weather_report)
    for time, song in songs.items():
        print(f'{time}\n\n')
        print(f'{song["title"]}\n\n')
        print(f'{song["song"]}\n\n')
        print(f'{song["reasoning"]}\n\n')
        print(f'{song["rhythm"]}\n\n')
        print(f'{song["genre"]}\n\n')
        print("--------------------------------")
