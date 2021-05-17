# Import stand libraries
import sys
import random
from datetime import datetime

# Import third party libraries
import requests


# Dictionaries with city coordinates
COORDS = {
    "curitiba": {"lat": -25.432604988726364, "lon": -49.26458705752047}, 
    "floripa": {"lat": -27.597482393445432, "lon": -48.50448698061411}, 
    "poa": {"lat": -30.020939148991644, "lon": -51.1669258420802}, 
}

CITACOES = [
    {"frase":"Como a literatura, o amor e a dor, as viagens são uma bela ocasião para nos encontramos com nós próprios", "autor":"Marguerite Yourcenar"},
    {"frase":"Viajar é aprender Geografia num mapa 1:1", "autor":"Eno Wanke"},
    {"frase":"O mundo é como um livro, e quem não viaja lê somente a primeira página", "autor":"Santo Agostinho"},
    {"frase":"Onde quer que vá, vá com todo seu coração", "autor":"Confúcio"},
    {"frase":"As pessoas não fazem as viagens, as viagens é que fazem as pessoas", "autor":"John Steinbeck"},
    {"frase":"Viajar é trocar a roupa da alma", "autor":"Mario Quintana"},
    {"frase":"A vida é o que fazemos dela. As viagens são os viajantes. O que vemos não é o que vemos, senão o que somos", "autor":"Fernando Pessoa"},
    {"frase":"Se não escalar a montanha, você nunca poderá apreciar a vista", "autor":"Pablo Neruda"},
    {"frase":"Porque metade de mim é partida, mas a outra metade é saudade", "autor":"Oswaldo Montenegro"},
    {"frase":"Se você der um passo em direção à liberdade, ela dará dois passos em direção a você", "autor":"Tom Morello"},
    {"frase":"Não viajamos para fugir da vida, mas para que a vida não fuja de nós", "autor":"Desconhecido"},
    {"frase":"Entre todos os livros do mundo, as melhores histórias estão entre as páginas de um passaporte", "autor":"Desconhecido"},
    {"frase":"Viajar. A melhor forma de se perder e de se encontrar ao mesmo tempo", "autor":"Brenna Smith"},
    {"frase":"Às vezes nem é o desejo de chegar. É só de ir", "autor":"Pe. Fábio de Melo"},
    {"frase":"Pior que não terminar uma viagem é nunca partir", "autor":"Amyr Klink"},
    {"frase":"Viajar é sentir a vida em constante movimento", "autor":"Valeria de Almeida"}
]

# API Key
KEY = "*********" # Insert API key here


def get_weather(city:str) -> dict:
    """Get 7-day weather forecast to a given city using the OpenWeather API
    (https://openweathermap.org/)
    
    > Arguments:
        - city (str): key to the coordinates dict.
    
    > Output:
        - (dict): dictionary with 7-day weather forecast.
    """
    
    # Base URL to OneCall OpenWeather API call
    base_url = "https://api.openweathermap.org/data/2.5/onecall"
    
    # Build API call
    base_url += f"?lat={COORDS[city]['lat']}&lon={COORDS[city]['lon']}"
    base_url += "&exclude=current,hourly,minutely&units=metric"
    base_url += f"&appid={KEY}"
    
    # Make the API call
    response = requests.get(url = base_url, params = {}).json()
     
    # Get only date, mean temp and rain
    timezone_offset = response['timezone_offset']
    
    # Iterate over daily forecasts
    day_strings = []
    for d in response['daily']:
        
        # Get info of interest
        utc_date = d['dt'] + timezone_offset
        temp = d['temp']['day']
        if "rain" in d.keys():
            rain = d['rain']
        else:
            rain = 0
        
        # Format date
        date = datetime.utcfromtimestamp(utc_date).strftime('%d/%m/%y')
        
        # Format day string and append it to list
        day_strings.append(f"<strong>{date}</strong>: {temp:.1f}°C ({rain:.1f}mm)")
    
    # Return results
    keys = ["a", "b", "c","d", "e", "f", "g"]
    return {"forecasts": {k:v for k,v in zip(keys, day_strings)}}


def main(dict):
    
    # Recognize action
    if dict['action'] == "previsao_curitiba":
        res = get_weather("curitiba")
        
    elif dict['action'] == "previsao_floripa":
        res = get_weather("floripa")
        
    elif dict['action'] == "previsao_poa":
        res = get_weather("poa")
    
    elif dict['action'] == "quote":
        res = random.choice(CITACOES)
    
    else:
        raise("Action not implemented!")
    
    # Return results
    return res
