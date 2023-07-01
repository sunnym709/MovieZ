import requests


def tmdb(Id,type="movies"):
    category = "movie" if type == "movies" else "tv"
    title = "title" if type == "movies" else "name"
    date = "release_date" if type == "movies" else "first_air_date"
    url = f"https://api.themoviedb.org/3/{category}/{Id}?append_to_response=credits&language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmZTFhOWNiYTI2OTY2MGRiNjA2NmY5MzAzMTNlMjY0YiIsInN1YiI6IjYyMDIzMWM3NDM5YmUxMDA2OWY1YjE1MSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.u2MqKw9YOmerApKFZD4Pa8EnbQJi9_kUVkbg4cNymus"
    }
    data = requests.get(url, headers=headers).json()
    return {"title":data[title],"genres":", " .join([x["name"] for x in data["genres"]]),"poster":data["poster_path"],"date":data[date],"cast":"," .join([x["name"]+x["profile_path"] for x in data["credits"].get("cast") if x["profile_path"]]),"rating":str(data["vote_average"])[:-2],"type":type,"overview":data["overview"]}

