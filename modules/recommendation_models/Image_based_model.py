from io import BytesIO
import numpy as np

import modules

@modules.tools.timer
async def Image_based_model(item: modules.schema.ServerData, local_data):
    
    img_tool = modules.Image_comparison()

    user_sigungu_image=[] #(len(local_data["items"]),2048)
    for i in local_data["items"]:
        user_sigungu_image.append(i["firstimage"])
    user_sigungu_image = await img_tool.extract_features_list(user_sigungu_image)

    user_liked_image=[] #(len(item.tours),2048)
    for i in item.interTour.list:
        user_liked_image.append(i.firstimage)
    user_liked_image = await img_tool.extract_features_list(user_liked_image)
    
    X=[]
    for i in user_sigungu_image:
        iter_list=[]
        for j in user_liked_image:
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
        for j in item.interTour.list:
            if(i["firstimage"]==j.firstimage):
                score+=5
            elif(i["firstimage"][:-4]==j.firstimage[:-4]):
                score+=3
            elif(i["firstimage"][:-6]==j.firstimage[:-6]):
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

