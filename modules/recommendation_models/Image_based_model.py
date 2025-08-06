from io import BytesIO
import numpy as np

import modules

@modules.tools.timer
def Image_based_model(item, local_data):
    
    data_url_feature=[] #(len(local_data["items"]),2048)
    for i in local_data["items"]:
        data_url_feature.append(modules.Image_comparison.extract_features(i["firstimage"]))

    user_input_url_feature=[] #(len(item.tours),2048)
    for i in item.tours:
        user_input_url_feature.append(modules.Image_comparison.extract_features(i["firstimage"]))
    
    X=[]
    for i in data_url_feature:
        iter_list=[]
        for j in user_input_url_feature:
            iter_list.append(modules.Image_comparison.cosine_similarity(i, j))
        X.append(iter_list)

    X=np.array(X) #(112, 7)
    X=X@X.T #(112, 112)

    column_sums = X.sum(axis=0, keepdims=True)
    num_rows = X.shape[0]
    column_sums[column_sums == 0] = 1
    X = X / column_sums

    init=[]
    for i in local_data["items"]:
        score=0
        for j in item.tours:
            if(i["firstimage"]==j["firstimage"]):
                score+=5
            elif(i["firstimage"][:-4]==j["firstimage"][:-4]):
                score+=3
            elif(i["firstimage"][:-6]==j["firstimage"][:-6]):
                score+=1
        init.append(score)
    init=np.array(init)

    while(init.all()!=(X@init).all()):
        init=X@init

    sorted_indices = np.argsort(init)
    top_5_indices = sorted_indices[::-1][:5]

    top_5 = []
    for i in top_5_indices:
        top_5.append(local_data["items"][i])
        print(local_data["items"][i])

    return top_5


if __name__ == "__main__":

    features = modules.Image_comparison.extract_features(
        "http://tong.visitkorea.or.kr/cms/resource/21/3497121_image3_1.jpg"
    )
    features1 = modules.Image_comparison.extract_features(
        "http://tong.visitkorea.or.kr/cms/resource/88/3082988_image2_1.jpg"
    )
    print(
        modules.Image_comparison.cosine_similarity(
            features, features1
        )
    )