from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.mobileby import MobileBy

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json


class TheScoreAppAutomation:
    def __init__(self):
        config = self.get_json_data("config.json")
        self.driver = webdriver.Remote(config["server_uri"], desired_capabilities=config["desired_caps"])
        
    @staticmethod
    def get_json_data(filename) -> dict:
        """ Get json data from specified file
        :param (str) filename: name of .json file to get data from
        :return file data in a dictionary format
        """
        try:
            with open(filename, "r") as f:
                data = json.loads(f.read())
            return data
        except FileNotFoundError:
            print(f"{filename} doesn't seem to exist, please make sure the path to the file is correct")
            raise 
        except json.decoder.JSONDecodeError as err:
            print(f"Json data seems to be corrupt or not in the right format.\n{err}")
    
    def get_element_by_(self, resource_id=None, text=None, is_clickable=False, timeout=10, raise_error=True):
        """ Find and retrieve element and it's properties

        :param resource_id: resource ID of element, can be found in xml page data
        :param text: If an element has a text attribute it makes sure to find the element with the specified text
        :param is_clickable: if True, it checks for the 'clickable' attribute to be True for the specified element.
        :param timeout: time limit to look for an element, raise a TimeoutException if not found in time limit.
        :param raise_error: if True, an error will be raised, otherwise it ignores the error.

        :return: found webdriver element
        """
        try:
            if resource_id and text:
                path = f"//*[@resource-id=\"{resource_id}\" and @text=\"{text}\"]"
            elif resource_id:
                path = f"//*[@resource-id=\"{resource_id}\"]"
            elif text:
                path = f"//*[@text=\"{text}\"]"
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(("xpath", path)))

            if is_clickable:
                element = element.find_element("xpath", ".//*[@clickable='true']")

            return element
        except TimeoutException as err:
            print(f"Error: Could not find element at '{path}'.")
            if raise_error:
                raise err

    @property
    def get_page_title(self) -> str:
        """ get page title """
        current_window = self.driver.current_activity
        if 'com.fivemobile.thescore' in current_window:
            title = self.get_element_by_(resource_id="com.fivemobile.thescore:id/titleTextView")
            return title.text
        return current_window
    
    def run(self):
        current_window = self.driver.current_activity
        if 'GrantPermissionsActivity' in current_window:
            self.get_element_by_(text="Allow").click()
        get_started_btn = "com.fivemobile.thescore:id/btn_primary"
        self.get_element_by_(resource_id=get_started_btn).click()

        # Select Leagues
        fav_leagues = {
            "NHL Hockey": "com.fivemobile.thescore:id/txt_name",
            "NBA Basketball": "com.fivemobile.thescore:id/txt_name",
            "NFL Football": "com.fivemobile.thescore:id/txt_name",
            "Continue": "com.fivemobile.thescore:id/action_button_text"
        }

        for key, value in fav_leagues.items():
            element = self.get_element_by_(resource_id=value, text=key)
            element.click()

        # Allow location
        self.get_element_by_("com.fivemobile.thescore:id/btn_allow").click()

        self.get_element_by_(text="While using the app").click()

        for vals in ["Toronto Raptors", "Toronto Maple Leafs", "Cleveland Cavaliers", "Golden State Warriors",
                     "Continue", "Done"]:
            try:
                self.get_element_by_(text=vals).click()
            except Exception as ex:
                print(f"Could not find '{vals}' in page.")

        self.get_element_by_("com.fivemobile.thescore:id/dismiss_modal", raise_error=False).click()

        # current_window = self.driver.current_activity
        # if 'permissioncontroller' in current_window:
        #     self.get_element_by_("com.android.permissioncontroller:id/permission_allow_foreground_only_button").click()

        self.get_element_by_(text="Leagues").click()

        league = "NHL"
        element = self.get_element_by_("com.fivemobile.thescore:id/league_name_text", text=league)
        element.click()

        title = self.get_element_by_("com.fivemobile.thescore:id/titleTextView").text
        assert title == league

        source = self.driver.page_source
        print(source)

        # Example: Perform swipe action
        action = TouchAction(self.driver)
        action.press(x=500, y=1000).move_to(x=500, y=500).release().perform()

        # You can add more actions as per your requirement

        # Close the driver session
        self.driver.quit()

    def is_home(self):
        element = self.get_element_by_(
            resource_id="com.fivemobile.thescore:id/navigation_bar_item_large_label_view",
            text="Favorites"
        )
        return element.selected == True

    
steps = {
    "title": "",
    "dialog_container": "com.fivemobile.thescore:id/dialog_container",
    "dismiss_dialog": ["com.fivemobile.thescore:id/dismiss_modal", "//android.widget.ImageView[@resource-id=\"com.fivemobile.thescore:id/dismiss_modal\"]"],
}

score = TheScoreAppAutomation()
score.run()






