import time

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

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
    
    def get_element_by_(self, resource_id=None, text=None, xpath=None, is_clickable=False, timeout=10, raise_error=True):
        """ Find and retrieve element and it's properties

        :param resource_id: resource ID of element, can be found in xml page data
        :param text: If an element has a text attribute it makes sure to find the element with the specified text
        :param xpath: specify the xpath.
        :param is_clickable: if True, it checks for the 'clickable' attribute to be True for the specified element.
        :param timeout: time limit to look for an element, raise a TimeoutException if not found in time limit.
        :param raise_error: if True, an error will be raised, otherwise it ignores the error.

        :return: found webdriver element
        """
        try:
            if xpath:
                path = xpath
            elif resource_id and text:
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
            return None

    def get_all_element_by_(self, resource_id=None, text=None, timeout=10, raise_error=True):
        """ Find and retrieve element and it's properties

        :param resource_id: resource ID of elements, can be found in xml page data
        :param text: If the elements have text attribute it makes sure to find all the elements with the specified text
        :param timeout: time limit to look for elements, raise a TimeoutException if not found in time limit.
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
            elements = WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(("xpath", path)))

            return elements
        except TimeoutException as err:
            print(f"Error: Could not find element at '{path}'.")
            if raise_error:
                raise err

    @property
    def get_page_title(self) -> str:
        """ get page title """
        current_window = self.driver.current_package
        if 'com.fivemobile.thescore' in current_window:
            title = self.get_element_by_(resource_id="com.fivemobile.thescore:id/titleTextView")
            return title.text
        return current_window

    def click_by_(self, resource_id=None, text=None, raise_error=False, xpath=None) -> None:
        """ finds and click element

        :param resource_id: resource ID of element, can be found in xml page data
        :param text: If an element has a text attribute it makes sure to find the element with the specified text
        :param xpath: specify the xpath.
        :param raise_error: if True, an error will be raised, otherwise it ignores the error.

        :return: None
        """
        element = self.get_element_by_(resource_id=resource_id, text=text, xpath=xpath, raise_error=raise_error)
        element.click()

    def is_selected_(self, resource_id: str = None, text: str = None) -> bool:
        """ Checks to see if a specific element is already selected or not

        :param (str or list) resource_id: resource ID of element to look for.
        :param (str) text: string attribute of element to look for.

        :return: (bool) True if 'selected' attribute of element is true, else False
        """
        element = self.get_element_by_(resource_id=resource_id, text=text)
        return element.get_attribute('selected') == 'true' if element else False

    def check_for_league_teams(self, teams: str or list):
        """ Confirms if team name(s) is present on page

        :param (list or str) teams: team / teams to look for on the visible page
        :return (bool) if team(s) is present return True, else False
        """
        elements = self.get_all_element_by_(resource_id="com.fivemobile.thescore:id/txt_name")
        element_list = [element.text for element in elements]
        try:
            element_list = str(element_list)
            if type(teams) is list:
                for team in teams:
                    assert team in element_list
            else:
                assert teams in element_list
        except AssertionError:
            return False
        return True

    def confirm_page(self, title: str) -> None:
        """ Checks if the page has the specified title using the titleTextView ID

        :param (str) title: title to look for
        :return (bool): True if found, else False
        """
        title_text = self.get_element_by_("com.fivemobile.thescore:id/titleTextView").text
        assert title_text == title

    def run(self):
        """ Basic run for setting up a new app.
            Steps:
            - Page:     Getting started
            - Page:     Choose your favorite leagues
            - Popup:    Allow location
            - Page:     Choose your favorite teams
            - Page:     Never miss a game
            - Popup:    Allow Notifications
            - Page:     Leagues Page
            - Page:     Go to specific League (NBA, NFL, NHL, ...)
            - Tabs:     Go to STANDINGS -> OVERALL tabs
            - Check to make sure teams reflect the League
            - Page:     Go back and make sure it's the League page
        """
        # Checks to see if current window has 'GrantPermissionsActivity' which is for android dialogue
        # if so select Allow
        current_window = self.driver.current_activity
        if 'GrantPermissionsActivity' in current_window:
            self.click_by_(text="Allow")
        self.click_by_(resource_id="com.fivemobile.thescore:id/btn_primary", raise_error=True)

        # Select Leagues
        fav_leagues = {
            "NHL Hockey": "com.fivemobile.thescore:id/txt_name",
            "NBA Basketball": "com.fivemobile.thescore:id/txt_name",
            "NFL Football": "com.fivemobile.thescore:id/txt_name",
            "Continue": "com.fivemobile.thescore:id/action_button_text"
        }
        league_teams = {
            "NBA": ["BOS Celtics", "CLE Cavaliers", "MIL Bucks", "LA Clippers", "NY Nicks"],
            "NFL": ["DAL Cowboys", "SF 49ers", "DET Lions", "BUF Bills", "CLE Browns"]
        }
        league_selected = "NBA"

        for league, resource_id in fav_leagues.items():
            self.click_by_(resource_id=resource_id, text=league)

        # Allow location
        self.click_by_(resource_id="com.fivemobile.thescore:id/btn_allow")

        self.click_by_(text="While using the app")

        for team in ["Toronto Raptors", "Toronto Maple Leafs", "Cleveland Cavaliers", "Golden State Warriors",
                     "Continue", "Done"]:
            try:
                self.click_by_(text=team)
            except Exception as ex:
                print(f"Could not find '{team}' in page.\n{ex}")

        # Allow for notification
        self.click_by_(text="Allow")

        # check for the dialog box and closes it if it's present
        self.click_by_(resource_id="com.fivemobile.thescore:id/dismiss_modal")

        self.click_by_(text="Leagues")
        self.confirm_page(title="Leagues")

        # This step is to get rid of the little dialog box, I can't seem to find the source code for it.
        self.click_by_(resource_id="com.fivemobile.thescore:id/header_right_text", text="Edit")
        time.sleep(1)
        self.click_by_(resource_id="com.fivemobile.thescore:id/header_right_text", text="Done")

        # Step 1: Open a league, team, or player page of your choice (bonus points for
        #         using a data-driven or parameterized approach).
        # Go to league page and confirm the title
        self.click_by_(resource_id="com.fivemobile.thescore:id/league_name_text", text=league_selected)
        # Step 2: Verify that the expected page opens correctly.
        self.confirm_page(title=league_selected)

        # Step 3: Tap on a sub-tab of your choice, eg: league table / standings / leaders, or
        #         stats tab of the league, team, or player.
        # Select the STANDINGS tab and OVERALL sub-tab
        self.click_by_(text="STANDINGS")
        # Step 4: Verify that you are on the correct tab and that the data is displayed
        #         correctly and corresponds to the league, team, or player from step 1.
        self.is_selected_(text="STANDINGS")
        self.click_by_(text="OVERALL")
        self.is_selected_(text="OVERALL")
        # Confirm the teams associated with the league are present on the page
        self.check_for_league_teams(teams=league_teams[league_selected])

        # Step 5: Verify that back navigation returns you to the previous page correctly.
        self.click_by_(xpath="//*[@content-desc=\"Navigate up\"]")
        assert self.get_page_title == "Leagues"

        # Close the driver session
        self.driver.quit()



if __name__ == "__main__":
    score = TheScoreAppAutomation()
    score.run()

