import numpy as np

import modules

@modules.tools.timer
async def Image_based_model(item: modules.schema.ServerData, local_data):
    
    img_tool = modules.Image_comparison()

    user_sigungu_image=[] #(len(local_data["items"]),2048)
    for i in local_data["items"]:
        user_sigungu_image.append(i["firstimage"])
    user_sigungu_image = np.array(await img_tool.extract_features_list(user_sigungu_image))
    row_sums = user_sigungu_image.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    user_sigungu_image = user_sigungu_image / row_sums

    user_liked_image=[] #(len(item.tours),2048)
    for i in item.interTour.items:
        user_liked_image.append(i.firstimage)
    user_liked_image = np.array(await img_tool.extract_features_list(user_liked_image))
    row_sums = user_liked_image.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    user_liked_image = user_liked_image / row_sums
    
    init=[]
    for i in local_data["items"]:
        score=0
        for j in item.interTour.items:
            if(i["lclsSystm3"]==j.lclsSystm3):
                score+=5
            elif(i["lclsSystm2"]==j.lclsSystm2):
                score+=3
            elif(i["lclsSystm1"]==j.lclsSystm1):
                score+=1
        init.append(score)
    init=np.array(init)
    column_sums = init.sum(axis=0, keepdims=True)
    column_sums[column_sums == 0] = 1
    init = init / column_sums


    X = user_sigungu_image @ user_liked_image.T
    X=X@X.T
    

    for i in range(50):
        init=X@init
        column_sums = init.sum(axis=0, keepdims=True)
        column_sums[column_sums == 0] = 1
        init = init / column_sums

    sorted_indices = np.argsort(init)
    top_5_indices = sorted_indices[::-1][:5]

    top_5 = []
    for i in top_5_indices:
        top_5.append(local_data["items"][i])
        # print(local_data["items"][i])

    return top_5

