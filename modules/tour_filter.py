import modules

def tour_filter(tour_list):
    if(type(tour_list)==type([])):
        filtered_data=[]

        for i in tour_list:
            if(i['lclsSystm1']=='AC'): #숙소
                continue
            elif(i['lclsSystm1']=='FD'): #음식점
                continue
            elif(i['lclsSystm2']=='SH04'): #마트
                continue
            elif(i['lclsSystm3']=='NA020600'): #염전 NA020600
                continue
            elif(i['lclsSystm3']=='C0117000'): #맛코스 C0117000
                continue
            elif(i['lclsSystm3']=='VE060200'): #영화관 VE060200
                continue
            elif(i['lclsSystm3']=='VE090600'): #학교 VE090600
                continue
            elif(i['lclsSystm3']=='SH030100'): #대형마트 SH030100
                continue
            elif(i['lclsSystm3']=='SH050200'): #안경점
                continue
            else:
                filtered_data.append(i)
        return filtered_data

    elif(type(tour_list)==type({1:1})):
        filtered_data={'totalCount':0, 'items':[]}

        for i in tour_list['items']: # type: ignore
            if(i['lclsSystm1']=='AC'): #숙소
                continue
            elif(i['lclsSystm1']=='FD'): #식당
                continue
            elif(i['lclsSystm2']=='SH04'): #마트
                continue
            elif(i['lclsSystm3']=='NA020600'): #염전 NA020600
                continue
            elif(i['lclsSystm3']=='C0117000'): #맛코스 C0117000
                continue
            elif(i['lclsSystm3']=='VE060200'): #영화관 VE060200
                continue
            elif(i['lclsSystm3']=='VE090600'): #학교 VE090600
                continue
            elif(i['lclsSystm3']=='SH030100'): #대형마트 SH030100
                continue
            elif(i['lclsSystm3']=='SH050200'): #안경점
                continue
            else:
                filtered_data['items'].append(i)
        
        filtered_data['totalCount']=len(filtered_data['items'])
        return filtered_data