# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import random
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

questions = [
    "Who's your favorite character in The Last Airbender?",
    "Which trait describes you?",
    "Which superpower would you want out of this list?",
    "What's your favorite animal in the Avatar universe?",
    "Who's your favorite character in Legend of Korra?",
    "Which activity sounds the most relaxing?",
    "who's your favorite villain in Legend of Korra?",
    "Which organization do you like better?", #white lotus vs red lotus
    "Who's your favorite non bender character?",
    "Which show do you like better?", #atla or lok
    "If given the choice where would you rather live: ", #spirit world, material world
    "Who do you think is the best avatar?"
]

answers = [
    "Aang, Toph, Zuko, Katara, or Sokka", #aang:air, #toph:earth, #katara:water, #sokka:non
    "brash, down to earth, calm, family oriented, or loyal", #brash:fire, down to earth: earth, calm:air, family oriented:water, loyal:non
    "flying, reading minds, super strength, shape shifting, or invisibility", #flying:air, super strength:earth, reading minds:fire, shape shifting:water, 
    "polar bear dog, flying lemur, dragon, the earth king's bear, or badgermole", #water, air, fire, non, earth
    "Mako, Bolin, Varrick, Jinora, or Asami", #mako:fire, bolin:earth, varrick:water, jinora:air, asami:non
    "reading, taking a bath, candlelit dinner, sleeping, or going on a hike", #air, water, fire, non, earth 
    "Amon, Zaheer, Tarlok, Kuvira, or Vaatu", #non air water earth fire
    "The White Lotus or The Red Lotus", #white: fire, air, #red: water, earth
    "Jet, Guru Prathik, Varrick, Mai, or Suki", #non air water fire earth
    "The Last Airbender or Legend of Korra", #atla: water, air, -  #lok: fire, earth, non
    "in the spirit world or in the material world", #spirit: water, non - air #material: fire, earth
    "Aang, Korra, Wan, Kyoshi, or Roku", #air, water, non, earth, fire
]

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hi! Welcome to What Bender Are You Quiz! Would you like to start the quiz and figure out what type of bender you are?"
        reprompt_text = "would you like to start the quiz and find out what bender you are?"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )
class NoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("NoIntent")(handler_input)
    def handle(self, handler_input):
        speak_output = "That's okay! Have a nice day!"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(True)
                .response
        )

class StartQuizIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("StartQuizIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Okay! fetching your questions right now! "
        
        attr = handler_input.attributes_manager.session_attributes
        attr["state"] = "QUIZ"
        attr["counter"] = 0
        attr['airScore'] = 0
        attr['waterScore'] = 0
        attr['earthScore'] = 0
        attr['fireScore'] = 0
        attr['nonbenderScore'] = 0
        
        speak_output += "Here's question number {}. {} {}".format(attr['counter'] + 1, questions[attr['counter']], answers[attr['counter']])
        attr['lastSpeech'] = answers[attr['counter']]
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(attr['lastSpeech'])
                .response
        )
class AnswerIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AnswerIntent")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        airSlot = slots["airSlot"].value
        waterSlot = slots['waterSlot'].value
        earthSlot = slots['earthSlot'].value
        fireSlot = slots['fireSlot'].value
        nonbenderSlot = slots['nonbender'].value
        fireAirNon = slots['fireAirNon'].value
        fireEarth = slots['fireEarth'].value
        fireEarthNon = slots['fireEarthNon'].value
        waterAir = slots['waterAir'].value
        waterAirNon = slots['waterAirNon'].value
        waterEarth = slots['waterEarth'].value
        
        attr = handler_input.attributes_manager.session_attributes
        
        if(airSlot != None and waterSlot == None and earthSlot == None and fireSlot == None and nonbenderSlot == None and fireAirNon == None 
            and fireEarth == None and fireEarthNon == None and waterAir == None and  waterAirNon == None and waterEarth == None):
            attr['airScore'] += 1
            
        elif(airSlot == None and waterSlot != None and earthSlot == None and fireSlot == None and nonbenderSlot == None and fireAirNon == None 
            and fireEarth == None and fireEarthNon == None and waterAir == None and  waterAirNon == None and waterEarth == None):
            attr['waterScore'] += 1
            
        elif(airSlot == None and waterSlot == None and earthSlot != None and fireSlot == None and nonbenderSlot == None and fireAirNon == None 
            and fireEarth == None and fireEarthNon == None and waterAir == None and  waterAirNon == None and waterEarth == None):
            attr['earthScore'] += 1
            
        elif(airSlot == None and waterSlot == None and earthSlot == None and fireSlot != None and nonbenderSlot == None and fireAirNon == None 
            and fireEarth == None and fireEarthNon == None and waterAir == None and  waterAirNon == None and waterEarth == None):
            attr['fireScore'] += 1
            
        elif(airSlot == None and waterSlot == None and earthSlot == None and fireSlot == None and nonbenderSlot != None and fireAirNon == None 
            and fireEarth == None and fireEarthNon == None and waterAir == None and  waterAirNon == None and waterEarth == None):
            attr['nonbenderScore'] += 1
            
        elif(airSlot == None and waterSlot == None and earthSlot == None and fireSlot == None and nonbenderSlot == None and fireAirNon != None 
            and fireEarth == None and fireEarthNon == None and waterAir == None and  waterAirNon == None and waterEarth == None):
            attr['fireScore'] += 1
            attr['airScore'] += 1
            attr['nonbenderScore'] += 1
            
        elif(airSlot == None and waterSlot == None and earthSlot == None and fireSlot == None and nonbenderSlot == None and fireAirNon == None 
            and fireEarth != None and fireEarthNon == None and waterAir == None and  waterAirNon == None and waterEarth == None):
            attr['fireScore'] += 1
            attr['earthScore'] += 1
            
        elif(airSlot == None and waterSlot == None and earthSlot == None and fireSlot == None and nonbenderSlot == None and fireAirNon == None 
            and fireEarth == None and fireEarthNon != None and waterAir == None and  waterAirNon == None and waterEarth == None):
            attr['fireScore'] += 1
            attr['earthScore'] += 1
            attr['nonbenderScore'] += 1
            
        elif(airSlot == None and waterSlot == None and earthSlot == None and fireSlot == None and nonbenderSlot == None and fireAirNon == None 
            and fireEarth == None and fireEarthNon == None and waterAir != None and  waterAirNon == None and waterEarth == None):
            attr['waterScore'] += 1
            attr['airScore'] += 1
            
        elif(airSlot == None and waterSlot == None and earthSlot == None and fireSlot == None and nonbenderSlot == None and fireAirNon == None 
            and fireEarth == None and fireEarthNon == None and waterAir == None and  waterAirNon != None and waterEarth == None):
            attr['waterScore'] += 1
            attr['airScore'] += 1
            attr['nonbenderScore'] += 1
            
        elif(airSlot == None and waterSlot == None and earthSlot == None and fireSlot == None and nonbenderSlot == None and fireAirNon == None 
            and fireEarth == None and fireEarthNon == None and waterAir == None and  waterAirNon == None and waterEarth != None):
            attr['waterScore'] += 1
            attr['earthScore'] += 1
        else: #review this
            speak_output = "i'm sorry i didn't get your answer can you repeat what you just said!"
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask(attr['lastSpeech'])
                    .response
            )

        attr['counter'] += 1
        
        if(attr['counter'] >= len(questions)):
            speak_output = "Thanks for playing! "
            air = {
            	"bending": "air bender",
            	"points": attr['airScore']
            }
            water = {
            	"bending": "water bender",
            	"points": attr['waterScore']
            }
            earth = {
            	"bending": "earth bender",
            	"points": attr['earthScore']
            }
            fire  = {
            	"bending": "fire bender",
            	"points": attr['fireScore']
            }
            non = {
                "bending": "non bender",
                "points" : attr['nonbenderScore']
            }
            listOfAllElements = [air,water,earth,fire, non]
            maximum = listOfAllElements[0] #arbitrarily set it as first element
            maxList = [maximum] #in case there is a tie choose randomly
            for item in listOfAllElements[1:]: #finds one maximum value
                if(item["points"] > maximum["points"]):
                    maxList.remove(maximum)
                    maximum = item
                    maxList.append(maximum)
            compPoints = maxList[0]["points"]
            for el in listOfAllElements:
                if(el not in maxList and el["points"] == compPoints):
                    maxList.append(el)
            
            index = random.randint(0, len(maxList) - 1) #randomly chooses an element in case of a tie
            bender = maxList[index]["bending"]
            
            determiner = 'a'
            if(bender == 'air bender' or bender == 'earth bender'):
                determiner+='n'
            description = ''
            if(bender == 'air bender'):
                description = "You are free-spirited, and easygoing. You like to maintain peace with your inner self and the world around you. As Uncle Iroh says \"air is the element of freedom.\""
            elif(bender == 'water bender'):
                description = "You are very balanced and go with the flow. You pride in your adaptability and are family oriented to the core. As Uncle Iroh says \"water is the element of change.\""
            elif(bender == 'earth bender'):
                description = "You are very headstrong and confrontational. You are described to be diverse, strong, and enduring and are meant to be a protector. As Uncle Iroh says \"Earth is the element of substance.\""
            elif(bender == 'fire bender'):
                description = "You are very powerful and aggressive. You are known to have an unflinching will to accomplish your tasks and desires. As Uncle Iroh says \"Fire is the element of power.\""
            else: #nonbender
                description = "Most of the time you are underestimated, but you will never let that stop you! You are known to be entrepreneurial, resourceful, loyal. You are the backbone and foundation of the world around you, and on top of that you have a heart of gold!"
            
            speak_output += "Based on your answers you are {} {}. {} Hope you had fun taking this quiz, feel free to take it again sometime!".format(determiner,bender, description)
            attr['lastSpeech'] = speak_output

            return (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(True)
                .response
            )
        else:    
            speak_output = "Question number {}. {} {}".format(attr['counter'] + 1, questions[attr['counter']], answers[attr['counter']])
            reprompt_text = "Sorry I didn't get that. Here's question number {} again: {} {}".format(attr['counter'] + 1, questions[attr['counter']], answers[attr['counter']])
            attr['lastSpeech'] = speak_output
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask(reprompt_text)
                    .response
            )
class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)
    def handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        speak_output = "I'm sorry I didn't quite catch what you just said I'll just repeat what I last spoke. "
        speak_output += attr["lastSpeech"] 
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
class RepeatIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        speak_output = attr["lastSpeech"] 
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(StartQuizIntentHandler())
sb.add_request_handler(AnswerIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(RepeatIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()