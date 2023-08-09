# from transformers import pipeline

# text_generation_pipeline = pipeline("text-generation")
# output = text_generation_pipeline(
#     "I love a girl, and she is gone.", max_length=1000)
# print("======================>>>", output[0]['generated_text'])


import csv
import pycountry
import pytz
import phonenumbers
from phonenumbers import geocoder

data = [["Country Code", "Country Name", "Timezones"]]


def create_csv():
    for country in pycountry.countries:
        timezones = pytz.country_timezones.get(country.alpha_2)
        if timezones:
            data.append([country.alpha_2, country.name, ', '.join(timezones)])

    with open('country_timezone.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def get_country(phone_number):
    parsed_number = phonenumbers.parse(phone_number, None)
    return geocoder.description_for_number(parsed_number, "en")


phone_number = input("Enter the phone number: ")
country = get_country(phone_number)
print(f"The phone number belongs to: {country}")
