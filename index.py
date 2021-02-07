# Fake 
from fun import fallback, make_only_response
from person import person
import intro
from navigation import navigation
from fun import big_image
import phrases as ph 

def handler(event, context):

    # session
    new_session = event['session']['new']
    user_location = event['session'].get('location')
    appId = event['session']['application'].get('application_id', None)
    print('>>>event: ', event, appId)

    # state
    appState = event['state']['application']
    sessionState = event['state']['session']
    print('>>>sessionState: ', sessionState, appId)
    print('>>>appState: ', appState, appId)

    # request
    request = event['request']
    print('>>>request: ', request, appId)

    # skill logic
    def worker(request, sessionState, appState, event):
        intents = request.get('nlu',{}).get('intents', {})
        command = request.get('command')
        context = sessionState.get('context')
        geo_asked = sessionState.get('geo_asked', False)
        story_mode = sessionState.get('story_mode')

        if new_session==True: 
            if appState.get('place_seen')!='null' and appState.get('place_seen') is not None:
                return intro.continue_game(sessionState)
            else:
                return intro.welcome(state=sessionState)

        elif context=='continue_game':
            if 'answer_da' in intents or 'YANDEX.CONFIRM' in intents:
                return person(event=event, step=0, place=appState['place_seen'], status=appState.get('status')) #?
            if 'net' in intents or 'YANDEX.REJECT' in intents:
                return intro.welcome(state=sessionState, appStateClear=True, appState=appState)      

        elif context=='welcome':
            if 'answer_da' in intents or 'YANDEX.CONFIRM' in intents:
                # запрос геолокации
                if user_location is None and geo_asked==False:
                    return intro.ask_geo(state=sessionState,card=True)
                elif user_location is not None and geo_asked==True:
                    return intro.how_far_from_kremlin(sessionState=sessionState, appState=appState, user_location=user_location)
                elif geo_asked==False:
                    return intro.ask_geo(state=sessionState,card=True)
            elif 'povtor'in intents or "YANDEX.REPEAT" in intents:
                return intro.welcome(state=sessionState)
            if 'net' in intents or 'YANDEX.REJECT' in intents:
                    return intro.bye('Возвращайся, когда будешь готов. Я и Садко будем ждать тебя')
            else:
                return intro.ask_geo(state=sessionState,card=True)
            return intro.ask_geo(state=sessionState,card=True)

        # начало. где находится пользоваетль
        elif context=='ask_geo':
            return intro.how_far_from_kremlin(sessionState=sessionState, appState=appState, user_location=user_location)

        elif context=='within_kremlin':
            if 'answer_da' in intents or 'YANDEX.CONFIRM' in intents:
                sessionState['context'] = 'within_kremlin_next'
                text='''Нажми "Да" для того, чтобы продолжить путь''',
                tts='''Первое летописное упоминание о Новгородском кремле, или как еще его называют дет+инце, относится к тысяча сорок четвертому г+оду. Является памятником архитектуры федерального значения,а также как часть исторического центра Великого Новгорода входит в список всемирного наследия ЮНЕСКО.
Дет+инцем называется центральная часть кремлевского ансамбля, в которой, в случае военных действий, могло укрыться население города. 
До наших дней сохранились несколько древних церквей, в том числе один из древнейших храмов на территории России - Софийский собор, звонница и девять боевых башен.
А теперь нам пора. Продолжим?'''
                card=big_image(image_ids='''213044/7bb6cdba1162dd5a78d7''',description=text)
                return make_only_response(    
            text = text,
            tts = tts,
            card=card,
            directives = True,
            buttons=ph.hi['buttons']
                )
            else:
                return navigation(appState, sessionState, intents, user_location)
#      После истории про Кремль
        elif context=='within_kremlin_next':
            if 'answer_da' in intents or 'YANDEX.CONFIRM' in intents: #???
                return navigation(appState, sessionState, intents, user_location)#???
            elif 'povtor'in intents or "YANDEX.REPEAT" in intents:
                return intro.how_far_from_kremlin(sessionState=sessionState, appState=appState, user_location=user_location)
            else:
                return intro.bye()

        elif context=='around_kremlin':
            if 'answer_da' in intents or 'YANDEX.CONFIRM' in intents or 'im_ready' in intents:#???
                return intro.how_far_from_kremlin(sessionState=sessionState, appState=appState, user_location=user_location)#???
            elif 'povtor'in intents or "YANDEX.REPEAT" in intents:
                return intro.how_far_from_kremlin(sessionState=sessionState, appState=appState, user_location=user_location)
            else:
                return intro.bye()

        elif context=='somewhere':
            if 'answer_da' in intents or 'YANDEX.CONFIRM' in intents:
                return navigation(appState, sessionState, intents, user_location)
            elif 'net' in intents or 'YANDEX.REJECT' in intents:
                return intro.bye()
            elif 'povtor'in intents or "YANDEX.REPEAT" in intents:
                return intro.how_far_from_kremlin(sessionState=sessionState, appState=appState, user_location=user_location)
            else:
                return fallback()
        
        elif context=='quest':
            return person(event=event, step=appState['step'], place=appState['place_seen'], status=appState.get('status'))

        elif context=='navigation':
            return navigation(appState, sessionState, intents, user_location, event)



        # запрос геолокации
        if user_location is None and geo_asked==False and context!='quest':
            return intro.ask_geo(state=sessionState)
        
        if 'im_ready' in intents:
            return navigation(appState, sessionState, intents, user_location, event)
        if 'help' in intents:
            return intro.say_help()

        return intro.fallback(command)

    # skill answer
    response = worker(request, sessionState, appState, event)

    webhook_response={
        'response': response,
        'session_state': sessionState,
        'application_state': appState,
        'version': event['version']
    }
    print('>>>webhook_response: ', webhook_response, appId)

    return webhook_response
