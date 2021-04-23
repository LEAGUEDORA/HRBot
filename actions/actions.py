#Author: Boyinapalli Sandeep Dora, Aremanda Abhijeeth



"""Importing necessary packages"""
import json
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.types import DomainDict
import random
import requests



"""URL to connect to connect to database"""
url = "https://3e80363e678f.ngrok.io/"    #Don't forget to add / after io 
# latest = None


class ButtonsFactory:

    @classmethod
    def createButtons(cls, list_of_possibles: list, intent: str, slot_name: str):
        lst = []
        for i in list_of_possibles:
            d = {}
            d['title'] = i
            d['payload'] = "/" + intent + "{\"" + slot_name + "\":\" "+i+" \"}"
            lst.append(d)
        return lst
 
##########################################################################################

class ActionLeaveBalance(Action):

    def name(self) -> Text:
        return "action_leave_balance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        authenticate = tracker.get_slot("authenticate")
        if authenticate is None:
            # latest = "action_leave_balance"
            dispatcher.utter_message(text = f"you have not logged in. Please login and try again", buttons = ButtonsFactory.createButtons(list_of_possibles = ['Login'], intent = "greet", slot_name = "dummy"))
        else:
            id = tracker.get_slot("id")
            data = {"id": int(id)}
            with open("data.json", "w") as f:
                json.dump(data, f)
            response = requests.post(url = url+"leavebalance", params = data)
            dispatcher.utter_message(text=f"Your remaining leaves {response.text}")
        return [SlotSet("latest","action_leave_balance")]


#################################################################################################


class ActionLogin(FormValidationAction):

    def name(self) -> Text:
        return "validate_greet"
    
    def validate_password(self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        id = tracker.get_slot("id")
        password = tracker.get_slot("password")
        data = {
            "id" : int(id),
            "signuppswd" : password
        }
        with open("data.json", "w") as f:
            json.dump(data, f)
        print(data)
        response = requests.post(url = url, params = data)
        print(response.text)
        if response.text == "OK":
            d = {}
            d['id'] = id
            d['password'] = password
            d['authenticate'] = 1
            dispatcher.utter_message(text="YOU HAVE LOGGED IN SUCCESSFULLY")
            return d
        else:
            d = {}
            d['id'] = None
            d['password'] = None
            dispatcher.utter_message(text = "Please check your ID and Password")
        return d


##########################################################################################################

class ActionSalaryIssue(FormValidationAction):

    def name(self) -> Text:
        return "validate_salary_issue"

    def validate_SALARY_ISSUE(self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,) -> Dict[Text, Any]:
        # print(1)
        # global latest
        authenticate = tracker.get_slot("authenticate")
        if authenticate is None:
            print("sending to authenticate")
            latest = "salary_issue"
            dispatcher.utter_message(text = f"you have not logged in. Please login and try again", buttons = ButtonsFactory.createButtons(list_of_possibles = ["Login"], intent = "greet", slot_name = "dummy"))
            d = {"latest" : latest}
            return d
        else:
            id = tracker.get_slot("id")
            issue = tracker.get_slot("SALARY_ISSUE")
            data = {"id": int(id),
                    "salaryissue": str(issue) }
            with open("data.json", "w") as f:
                json.dump(data, f)
            response = requests.post(url = url+"salaryissue", params = data)
            
            dispatcher.utter_message(text=f"{response.text}")
            print(issue)
        return []


##############################################################################################################################

class ActionHarrasment(FormValidationAction):

    def name(self) -> Text:
        return "validate_harrasment"
    
    def validate_NAME_ACCUSED(self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,) -> Dict[Text, Any]:
        # global latest
        latest = "harrasment"
        d = {"latest" : latest}
        return d

    def validate_ISSUE_DISCRIPTION(self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,) -> Dict[Text, Any]:
        authenticate = tracker.get_slot("authenticate")
        id = tracker.get_slot("id")
        issue = tracker.get_slot("ISSUE_DISCRIPTION")
        accused = tracker.get_slot("NAME_ACCUSED")
        if authenticate is None:
            latest = "harrasment"
            dispatcher.utter_message(text = f"you have not logged in. Please login and try again" , buttons = ButtonsFactory.createButtons(list_of_possibles = ["Login"], intent = "greet", slot_name = "dummy"))
            return [FollowupAction("greet")]
        else:
            data = {
                "id1" : int(id),
                "case" : issue,
                "id2" : accused
            }
            with open("data.json", "w") as f:
                    json.dump(data, f)
            response = requests.post(url = url+"harassment", params = data)
                
            dispatcher.utter_message(text=f"{response.text}")
        return [SlotSet("latest","harrasment")]



#############################################################################################################

class ActionResignation(FormValidationAction):

    def name(self) -> Text:
        return "validate_resign"


    def validate_WHY_DO_YOU_WANT_TO_LEAVE(self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,) -> Dict[Text, Any]:
        # global latest
        latest = "resign"
        d = {"latest" : latest}
        return d

    def validate_IS_THERE_ANYTHING_WE_CAN_SO_THAT_YOU_STAY(self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,) -> Dict[Text, Any]:
        id = tracker.get_slot("id")
        issue = tracker.get_slot("WHY_DO_YOU_WANT_TO_LEAVE")
        korika = tracker.get_slot("IS_THERE_ANYTHING_WE_CAN_SO_THAT_YOU_STAY")
        authenticate = tracker.get_slot("authenticate")
        if authenticate is None:

            dispatcher.utter_message(text = f"you have not logged in. Please login and try again", buttons = ButtonsFactory.createButtons(list_of_possibles = ["Login"], intent = "greet", slot_name = "dummy"))
            return [FollowupAction("greet")]
        else:
            data = {
                "id1" : int(id),
                "resignissue" : issue,
                "block" : korika
            }
            with open("data.json", "w") as f:
                    json.dump(data, f)
            response = requests.post(url = url+"resignation", params = data)
                
            dispatcher.utter_message(text=f"{response.text}")

#################################################################################################


class ActionSollu(Action):

    def name(self) -> Text:
        return "action_sollu"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent_ = tracker.get_intent_of_latest_message()
        dispatcher.utter_message(template = f"utter_{intent_}")

        return []

#####################################################################################


class ActionTakeUp(Action):

    def name(self) -> Text:
        return "action_takeup"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest = tracker.get_slot("latest")
        if  latest is not  None:
            print("lstest issue", latest)
            return [FollowupAction(latest)]
