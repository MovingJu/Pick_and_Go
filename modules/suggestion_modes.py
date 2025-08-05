
def Count_model(item, local_data):
    from collections import Counter
    
    user_preference_counts = Counter(tour["lclsSystm3"] for tour in item.tours)

    scored_places = []
    for place in local_data["items"]:
        place_code = place["lclsSystm3"]
        score = user_preference_counts.get(place_code, 0)
        scored_places.append((place, score))

    scored_places.sort(key=lambda x: x[1], reverse=True)

    top_5_places = [place[0] for place in scored_places[:5]]

    return top_5_places