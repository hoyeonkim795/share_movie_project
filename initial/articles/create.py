import sys
import requests
import json

jsondata = []
for i in range(1, 11):
    url = "https://api.themoviedb.org/3/movie/top_rated?api_key=7bfeda2276dd8eac6859724170d2ace6&language=ko-KR&page=" + str(i)
    results = requests.get(url).json()["results"]
    # print(results)
    for result in results:
        temp = {}
        temp['model'] = 'articles.movie'
        temp['id'] = result.pop('id')
        field = {}
        # 'genre_ids'추가 원해 
        modelfield = ['title', 'original_title', 'release_date', 'popularity', 'vote_count', 'vote_average', 'adult', 'overview', 'original_language', 'poster_path', 'backdrop_path', 'genre_ids']
        for key, value in result.items():
            if key in modelfield:
                field[key] = value
        # print(field)
            temp['fields'] = field
        # print()
        jsondata.append(temp)
    # print(jsondata)

with open('moviedata.json', 'w', encoding="UTF-8") as make_file:
    json.dump(jsondata, make_file, indent="\t")


jsondata = []
url = "https://api.themoviedb.org/3/genre/movie/list?api_key=7bfeda2276dd8eac6859724170d2ace6&language=ko-KR"
genres = requests.get(url).json()["genres"]
# print(genres)
for genre in genres:
    temp = {}
    temp['model'] = 'articles.genre'
    # temp['id'] = genre.pop('id')
    field = {}
    for key, value in genre.items():
        field[key] = value
        temp['fields'] = field
    jsondata.append(temp)
# print(jsondata)

with open('genre.json', 'w', encoding="UTF-8") as make_file:
    json.dump(jsondata, make_file, indent="\t")