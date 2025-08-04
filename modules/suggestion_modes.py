def Count_model(item, local_data):
    from collections import Counter
    
    user_preference_counts = Counter(tour["lclsSystm3"] for tour in item.tours)

    # 2. data의 관광지 코드를 기반으로 점수 계산
    scored_places = []
    for place in local_data["items"]:
        place_code = place["lclsSystm3"]
        # 사용자의 선호 코드가 data에 있으면 해당 빈도수를 점수로 추가, 없으면 0점
        score = user_preference_counts.get(place_code, 0)
        scored_places.append((place, score))

    # 3. 점수가 높은 순으로 정렬
    scored_places.sort(key=lambda x: x[1], reverse=True)

    # 4. 상위 5개 출력
    top_5_places = [place[0] for place in scored_places[:5]]

    # 결과 출력
    # print("사용자가 선호할 것 같은 관광지 상위 5개:")
    # for place in top_5_places:
    #     print(f"  - {place[1]} (분류코드: {place[2]}, 점수: {user_preference_counts.get(place[2], 0)})")

    return scored_places

