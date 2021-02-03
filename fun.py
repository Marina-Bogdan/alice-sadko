from resource import pers_help
def make_response(
    text="Текст ответа здесь",
    tts=None, 
    buttons=None,
    step=None, 
    place=None, 
    status=None, 
    card=None,
    directives=False,
    end_session=False,
    place_next=None,
    context=None,
    geo_asked=None
    ):
    response = {
            'text':text,
            'tts': tts if tts is not None else text,
            "end_session": end_session
        }
    if buttons is not None:
        response['buttons'] = buttons
    if card is not None:
        response['card']=card
    if place_next is not None:
        response['place_next']=place_next
    if directives is True:
        response['directives']={"request_geolocation": {}}

    webhook_response={
        'response': response,
        "application_state": {
            "step": step,
            "place_seen": place,
            "status": status,
        },
        'version':'1.0',
    }
    print(webhook_response)
    return  webhook_response
    
def fallback(event):
    text="Извините данный диалог в разработке"
    return make_response(text,end_session= True)

def button(title, payload=None, url=None, hide=False):
    button = {
        'title': title,
        'hide': hide,
    }
    if payload is not None:
        button['payload'] = payload
    if url is not None:
        button['url'] = url
    return button
def image_gallery(image_ids,description):
    return {
        'type':'BigImage',
        'image_id':image_ids,
        'description':description
    }
def end_session1(text=None,tts=None,step=None,place=None,status=None):
    if text is None:
        text='''Скоро сказка сказывается, да не скоро дело делается.\
         Я и Садко, будем ждать тебя. Возвращайся скорей!'''
        tts='''<speaker audio="dialogs-upload/ba73ad37-33af-4bea-8c8d-b6689c2febdd/7379f654-3b36-40ec-8909-970d66673535.opus">'''
    else:
        text=text
        tts=tts
    end_session11=True
    return make_response(text= text,\
    tts=tts , end_session=end_session11,step=step, place=place,status=status)

def text_to_resp(source,ind_1=None,ind_2=None,card=None,obj_3=None,obj_4=None):
    source=source
    if ind_2 is not None:
        text=source[ind_1][ind_2][0]
        tts=source[ind_1][ind_2][1]
        status=source[ind_1][ind_2][2]
        if card is not None:
            card=image_gallery(source[ind_1][ind_2][3],description=text)
        if obj_3 is not None:
            obj_3=source[ind_1][ind_2][3]
        if obj_4 is not None:
            obj_4=source[ind_1][ind_2][4]
    elif ind_1 is not None:
        text=source[ind_1][0]
        tts=source[ind_1][1]
        status=source[ind_1][2]
        if card is not None:
            card=image_gallery(source[ind_1][3],description=text)
        if obj_3 is not None:
            obj_3=source[ind_1][3]
        if obj_4 is not None:
            obj_4=source[ind_1][4]
    else:
        text=source[0]
        tts=source[1]
        status=source[2]
        if card is not None:
            card=image_gallery(source[3],description=text) 
        if obj_3 is not None:
            obj_3=source[3]
        if obj_4 is not None:
            obj_4=source[4]
    return (text,tts,status,card,obj_3,obj_4)

def help_4_zagadka (event,ind_1,povtor=None):
    place=event.get('state').get('application').get('place_seen')
    step=event.get('state').get('application').get('step')
    status=event.get('state').get('application').get('status')
    if povtor:
        if status=='help_not_end':
            status='zagadka'
        elif status=='help_end':
            status='help_not_end'
    if ind_1==999 and status!='help_not_end':
        buttons=[button('Да', hide=True),button('Нет', hide=True)]
        card_999=True
    elif ind_1==999 and status=='help_not_end':
        card_999=True
        buttons=[button('Да', hide=True)]
    else:
        buttons=[button('Повтори', hide=True),button('Я не знаю', hide=True),button('Я знаю', hide=True)]
        card_999=None

    if status=="zagadka" or status=='zag_not_end':
        param=text_to_resp(pers_help,ind_1,0,card=card_999)
        return make_response(text=param[0],tts=param[1], buttons=buttons,step=step, place=place,
                status=param[2], card=param[3])
    elif status=='help_not_end':
        param=text_to_resp(pers_help,ind_1,1,card=True)
        return make_response(text=param[0],tts=param[1], buttons=buttons,step=step, place=place,
        status=param[2], card=param[3])
    elif status=='help_end':
        param=text_to_resp(pers_help,ind_1,2)
        return end_session1(text=param[0],tts=param[1],step=0,place=place,status=param[2])
    else:
        return fallback(event)
