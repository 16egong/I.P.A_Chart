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
    if place == 'bilabial':
        if manner == 'plosive':
            url = 'https://s3.amazonaws.com/ipa-chart-sounds/Voiced_bilabial_plosive.mp3'
    if place == 'alveolar':
        if manner == 'plosive':
            url = 'https://s3.amazonaws.com/ipa-chart-sounds/Voiced_alveolar_plosive.mp3'
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