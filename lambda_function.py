import json

def lambda_handler(event, context):
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.ask.skill.987654321"):
    #     raise ValueError("Invalid Application ID")
    
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
        
    if event['request']['type'] == 'LaunchRequest':
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == 'IntentRequest':
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def on_launch(intent_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    title = 'Welcome to I.P.A. Chart'
    body = 'Please ask for a place and a manner.'
    should_end_session = False
    speechlet_response = build_speechlet_response(title, body, 'phrase', should_end_session)

    return build_response(speechlet_response)
    
def on_intent(intent_request, session):
    
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    
    if intent_name == 'PhoneticSoundIntent':
        return phonetic_sound_intent(intent, session)
    elif intent_name == 'AMAZON.CancelIntent':
        return cancel_intent()
    elif intent_name == 'AMAZON.HelpIntent':
        return help_intent()
    elif intent_name == 'AMAZON.StopIntent':
        return stop_intent()
    elif intent_name == 'AMAZON.PauseIntent':
        return pause_intent(intent, session)
    elif intent_name == 'AMAZON.ResumeIntent':
        return resume_intent()
    else:
        raise ValueError("Invalid intent")


def add_ssml_pause(duration):
    """Turns a duration into an SSML tag."""
    if duration:
        return '<break time="%s"/> ' % (duration)
    else:
        return ''

def persist_attributes(session):
    if 'attributes' in session.keys():
        return session['attributes']
    else:
        return {}

def pause_intent(intent, session):
    """
    Pause instructions until resume is called for
    """
    sesh_attr = persist_attributes(session)
    
    speechlet_response = build_speechlet_response("Waiting...", add_ssml_pause("10s"), should_end_session=True)
    return build_response(sesh_attr, speechlet_response)
    

def phonetic_sound_intent(intent, session):
    place = intent['slots']['place']['value']
    manner = intent['slots']['manner']['value']
    
    url = get_sound(place, manner)
    title = "I.P.A. Chart: " + place + ' ' + manner
    should_end_session = True
    speechlet_response = build_speechlet_response(title, url, 'sound', should_end_session)
    return build_response(speechlet_response)

def get_sound(place, manner):
    url_chart = [[None for col in range(12)] for row in range(8)]
    
    places = {}
    places['bilabial'] = 0
    places['labiodental'] = 1
    places['dental'] = 2
    places['alveolar'] = 3
    places['postalveolar'] = 4
    places['retroflex'] = 5
    places['palatal'] = 6
    places['velar'] = 7
    places['uvular'] = 8
    places['pharyngeal'] = 9
    places['glottal'] = 10
    
    manners = {}
    manners['plosive'] = 0
    manners['nasal'] = 1
    manners['trill'] = 2
    manners['tap'] = 3
    manners['fricative'] = 4
    manners['lateral fricative'] = 5
    manners['approximant'] = 6
    manners['lateral approximant'] = 7
    
    url_chart[0][0] = 'https://s3.amazonaws.com/ipa-chart-sounds/Voiced_bilabial_plosive.mp3'
    url_chart[0][3] = 'https://s3.amazonaws.com/ipa-chart-sounds/Voiced_alveolar_plosive.mp3'
    url_chart[0][5] = 'https://s3.amazonaws.com/ipa-chart-sounds/Voiced_retroflex_plosive.mp3'
    url_chart[0][6] = 'https://s3.amazonaws.com/ipa-chart-sounds/Voiced_palatal_plosive.mp3'
    url_chart[0][7] = 'https://s3.amazonaws.com/ipa-chart-sounds/Voiced_velar_plosive.mp3'
    url_chart[0][8] = 'https://s3.amazonaws.com/ipa-chart-sounds/Voiced_uvular_plosive.mp3'
    url_chart[0][10] = 'https://s3.amazonaws.com/ipa-chart-sounds/Glottal_stop.mp3'
    
    url_chart[1][0] = 'https://s3.amazonaws.com/ipa-chart-sounds/Bilabial_nasal.mp3'
    url_chart[1][1] = 'https://s3.amazonaws.com/ipa-chart-sounds/Labiodental_nasal.mp3'
    url_chart[1][3] = 'https://s3.amazonaws.com/ipa-chart-sounds/Alveolar_nasal.mp3'
    url_chart[1][5] = 'https://s3.amazonaws.com/ipa-chart-sounds/Retroflex_nasal.mp3'
    url_chart[1][6] = 'https://s3.amazonaws.com/ipa-chart-sounds/Palatal_nasal.mp3'
    url_chart[1][7] = 'https://s3.amazonaws.com/ipa-chart-sounds/Velar_nasal.mp3'
    url_chart[1][8] = 'https://s3.amazonaws.com/ipa-chart-sounds/Uvular_nasal.mp3'
    url_chart[2][3] = 'https://s3.amazonaws.com/ipa-chart-sounds/Alveolar_trill.mp3'
    url_chart[3][3] = 'https://s3.amazonaws.com/ipa-chart-sounds/Alveolar_lateral_flap.mp3'
    url_chart[4][0] = 'https://s3.amazonaws.com/ipa-chart-sounds/Voiced_bilabial_fricative.mp3'
    url_chart[4][1] = 'https://s3.amazonaws.com/ipa-chart-sounds/Voiced_labiodental_fricative.mp3'
    url_chart[4][2] = 'https://s3.amazonaws.com/ipa-chart-sounds/Voiced_dental_fricative.mp3'
    url_chart[4][3] = 'https://s3.amazonaws.com/ipa-chart-sounds/Voiced_alveolar_fricative.mp3'
    url_chart[4][4] = 'https://s3.amazonaws.com/ipa-chart-sounds/Voiced_postalveolar_fricative.mp3'
    url_chart[4][5] = 'https://s3.amazonaws.com/ipa-chart-sounds/Voiced_retroflex_fricative.mp3'
    url_chart[4][6] = 'https://s3.amazonaws.com/ipa-chart-sounds/Voiced_palatal_fricative.mp3'
    url_chart[4][7] = 'https://s3.amazonaws.com/ipa-chart-sounds/Voiced_velar_fricative.mp3'
    url_chart[4][8] = 'https://s3.amazonaws.com/ipa-chart-sounds/Voiced_uvular_fricative.mp3'
    url_chart[4][9] = 'https://s3.amazonaws.com/ipa-chart-sounds/Voiced_pharyngeal_fricative.mp3'
    url_chart[4][10] = 'https://s3.amazonaws.com/ipa-chart-sounds/Voiced_glottal_fricative.mp3'
    
    return url_chart[places[place]][manners[manner]]
    return url
    
# Built In Intents
def cancel_intent():
    should_end_session = True
    speechlet_response = build_speechlet_response("Cancel this I.P.A Chart", "Cancelled", 'phrase', should_end_session)
    return build_response(speechlet_response)
    
def help_intent():
    should_end_session = False
    speechlet_response =  build_speechlet_response("Help with I.P.A. Chart", "Please state a place and a manner", 'phrase', should_end_session)
    return build_response(speechlet_response)
    
def stop_intent():
    should_end_session = True
    speechlet_response = build_speechlet_response("Stop I.P.A. Chart", "Done", 'phrase', should_end_session)
    return build_response(speechlet_response)

# --------------- Helpers that build all of the responses ----------------------
# modified: 
# https://console.aws.amazon.com/lambda/home?region=us-east-1#/create/new?bp=alexa-skills-kit-color-expert-python
def build_response(speechlet_response, session_attributes={}):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

def build_speechlet_response(title, output, typeIs, should_end_session):
    if typeIs == 'phrase':
        return {
            'outputSpeech': {
                'type': 'PlainText',
                'text': output
            },
            'card': {
                'type': 'Simple',
                'title': "SessionSpeechlet - " + title,
                'content': "SessionSpeechlet - " + output
            },
            'shouldEndSession': should_end_session
        }
    elif typeIs == 'sound':
        return {
            'directives': [
                {
                    'type': 'AudioPlayer.Play',
                    'playBehavior': 'REPLACE_ALL',
                    'audioItem': {
                        'stream': {
                            'token': '12345',
                            'url': output,
                            'offsetInMilliseconds': 0
                        }
                    }
                }
            ],
            'card': {
                'type': 'Simple',
                'title': "SessionSpeechlet - " + title,
                'content': "SessionSpeechlet - " + output
            },
            'shouldEndSession': should_end_session
        }