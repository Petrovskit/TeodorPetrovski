import os
import unittest

from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class ShopTests(unittest.TestCase):
    driver = None
    global_username = "teodorpetrovski"
    global_password = "12345678"
    global_bug_name = "Infinum"

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("https://qaworkshop.netlify.app/")
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def wait_for_element(self, by, value, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located((by, value)))
            return element
        except Exception as e:
            raise e

    def wait_for_text_in_element(self, by, locator, text, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.text_to_be_present_in_element((by, locator), text))
            return element
        except Exception as e:
            raise e

    def login(self, username, password):
        username_input_field = self.wait_for_element(By.CSS_SELECTOR, "input[data-testid='store-name-input']")
        password_input_field = self.driver.find_element(By.CSS_SELECTOR, "input[data-testid='password-input']")

        username_input_field.clear()
        password_input_field.clear()

        username_input_field.send_keys(username)
        password_input_field.send_keys(password)

        login_btn = self.driver.find_element(By.NAME, "login")
        login_btn.click()

    def test_1_register(self):
        """
        With this test we are going to register a new user and check if a success message is displayed, and we are going
        to check if the text of the success message corresponds with the client requirements.
        """
        self.login(self.global_username, self.global_password)

        register_button = self.driver.find_element(By.NAME, "register")
        register_button.click()

        success_message = self.wait_for_element(By.CSS_SELECTOR, "p[data-testid='message']")
        self.assertEqual(success_message.text, "User registered")

        try:
            user_home_directory = os.path.expanduser("~")

            screenshot_file_path = os.path.join(user_home_directory, "Desktop", "Test 1 screenshot.png")

            self.driver.save_screenshot(screenshot_file_path)

            print(f"Screenshot saved to: {screenshot_file_path}")
        except Exception as e:
            print(f"Error saving screenshot: {str(e)}")

    def test_2_login(self):
        """
        With this test we are going to log in with the user that was created in the First test, and we are going to
        check if the user is navigated to the correct page. We are checking for the URL and if "Empty Order" button
        is displayed.
        """
        self.login(self.global_username, self.global_password)

        empty_order_btn = self.wait_for_element(By.CSS_SELECTOR, "button[data-testid='empty-order-button']")
        self.assertTrue(empty_order_btn.is_displayed())
        self.assertEqual(self.driver.current_url, f"https://qaworkshop.netlify.app/store/{self.global_username}")

        try:
            user_home_directory = os.path.expanduser("~")

            screenshot_file_path = os.path.join(user_home_directory, "Desktop", "Test 2 screenshot.png")

            self.driver.save_screenshot(screenshot_file_path)

            print(f"Screenshot saved to: {screenshot_file_path}")
        except Exception as e:
            print(f"Error saving screenshot: {str(e)}")

    def test_3_delete_user(self):
        """
        With this test we are going to navigate back to the Login page and delete the user that we created in the
        First test, and we are going to check if the text of the success message corresponds with the client
        requirements.
        """
        self.driver.back()

        username_input_field = self.driver.find_element(By.CSS_SELECTOR, "input[data-testid='store-name-input']")
        password_input_field = self.driver.find_element(By.CSS_SELECTOR, "input[data-testid='password-input']")

        username_input_field.clear()
        password_input_field.clear()

        username_input_field.send_keys(self.global_username)
        password_input_field.send_keys(self.global_password)

        delete_btn = self.driver.find_element(By.NAME, "delete")
        delete_btn.click()

        success_message = self.wait_for_element(By.CSS_SELECTOR, "p[data-testid='message']")
        self.assertEqual(success_message.text, "User deleted!")

        try:
            user_home_directory = os.path.expanduser("~")

            screenshot_file_path = os.path.join(user_home_directory, "Desktop", "Test 3 screenshot.png")

            self.driver.save_screenshot(screenshot_file_path)

            print(f"Screenshot saved to: {screenshot_file_path}")
        except Exception as e:
            print(f"Error saving screenshot: {str(e)}")

    def test_4_add_bug_to_cart(self):
        """
        With this test we are going to add a bug to the Cart, and we are going to check if the bug is displayed in
        the Cart.
        """
        self.driver.refresh()
        self.test_1_register()
        self.test_2_login()

        load_sample_bugs_btn = self.driver.find_element(By.CSS_SELECTOR,
                                                        "button[data-testid='load-sample-bugs-button']")
        load_sample_bugs_btn.click()

        products = self.driver.find_elements(By.CSS_SELECTOR, ".menu-fish")

        filtered_products = [product for product in products if
                             product.find_element(By.CSS_SELECTOR, "h3.fish-name").text == "Beetle\n$32.00"]

        if filtered_products:
            filtered_products[0].find_element(By.CSS_SELECTOR, ".menu-fish button").click()

        order_in_cart = self.wait_for_element(By.CSS_SELECTOR, "li.order-enter-done")
        self.assertTrue(order_in_cart.is_displayed())

        try:
            user_home_directory = os.path.expanduser("~")

            screenshot_file_path = os.path.join(user_home_directory, "Desktop", "Test 4 screenshot.png")

            self.driver.save_screenshot(screenshot_file_path)

            print(f"Screenshot saved to: {screenshot_file_path}")
        except Exception as e:
            print(f"Error saving screenshot: {str(e)}")

    def test_5_clear_inventory_add_new_bug_to_cart(self):
        """
        With this test we are going to clear the inventory, create a new bug, and add the newly created bug to the
        Cart. We are going to check if the bug is displayed in the shop and if the bug is displayed in the Cart.
        """
        clear_inventory = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='clear-inventory-button']")
        clear_inventory.click()

        bug_name = self.driver.find_element(By.NAME, "name")
        bug_name.send_keys(self.global_bug_name)

        bug_price = self.driver.find_element(By.NAME, "price")
        bug_price.send_keys(666)

        bug_description = self.driver.find_element(By.NAME, "desc")
        bug_description.send_keys("Python is so hard compared to JAVA !!! Cheers to brate Neven :)")

        add_new_bug_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        add_new_bug_btn.click()

        bug_added = self.driver.find_element(By.CSS_SELECTOR, ".menu-fish")
        add_to_order_btn = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='add-to-order-button']")

        self.assertTrue(bug_added.is_displayed())
        add_to_order_btn.click()

        item_displayed_in_cart = self.wait_for_element(By.CSS_SELECTOR, ".order-enter-done")
        self.assertTrue(item_displayed_in_cart.is_displayed())

        try:
            user_home_directory = os.path.expanduser("~")

            screenshot_file_path = os.path.join(user_home_directory, "Desktop", "Test 5 screenshot.png")

            self.driver.save_screenshot(screenshot_file_path)

            print(f"Screenshot saved to: {screenshot_file_path}")
        except Exception as e:
            print(f"Error saving screenshot: {str(e)}")

    def test_6_change_bug_status(self):
        """
        With this test we are going to change the status of the bug, and we are going to check if the status was
        successfully updated. Also, we are going to check if the Cart has been updated since the bug that was added
        to the cart is not available anymore.
        """
        status_drop_down = self.wait_for_element(By.NAME, "status")

        dropdown = Select(status_drop_down)
        dropdown.select_by_visible_text("Sold Out")

        sold_out_txt = self.wait_for_element(By.CSS_SELECTOR, "button[data-testid='add-to-order-button']")
        self.assertEqual(sold_out_txt.text.lower(), "sold out")

        cart_message = self.driver.find_element(By.CSS_SELECTOR, "li.order-enter-done")
        self.assertEqual(cart_message.text, f"Sorry {self.global_bug_name} is no longer available.")

        try:
            user_home_directory = os.path.expanduser("~")

            screenshot_file_path = os.path.join(user_home_directory, "Desktop", "Test 6 screenshot.png")

            self.driver.save_screenshot(screenshot_file_path)

            print(f"Screenshot saved to: {screenshot_file_path}")
        except Exception as e:
            print(f"Error saving screenshot: {str(e)}")

    def test_7_change_price(self):
        """
        With this test we are going to change the bug status to available again, and we are going to change the price
        of the bug. For the new price we are going to add alphabetical characters instead of digits, and we are going
        to check if the price is going to be displayed as NaN.
        """
        status_drop_down = self.wait_for_element(By.NAME, "status")

        dropdown = Select(status_drop_down)
        dropdown.select_by_visible_text("Fresh!")

        price_input_field = self.driver.find_element(By.NAME, "price")
        price_input_field.send_keys("price")

        cart_bug_price = self.wait_for_element(By.CSS_SELECTOR, ".price")
        self.assertEqual(cart_bug_price.text, "$NaN")

        shop_bug_price = self.driver.find_element(By.CSS_SELECTOR, "span[data-testid='bug-shop-price']")
        self.assertEqual(shop_bug_price.text, "$NaN")

        try:
            user_home_directory = os.path.expanduser("~")

            screenshot_file_path = os.path.join(user_home_directory, "Desktop", "Test 7 screenshot.png")

            self.driver.save_screenshot(screenshot_file_path)

            print(f"Screenshot saved to: {screenshot_file_path}")
        except Exception as e:
            print(f"Error saving screenshot: {str(e)}")

    def test_8_register_already_existing_user(self):
        """
        With this test we are going to try and register an already existing user. We are going to check for the
        validation message and after that we are going to delete the user that we have created(cleanup).
        """
        self.driver.back()

        username_input_field = self.wait_for_element(By.CSS_SELECTOR, "input[data-testid='store-name-input']")
        username_input_field.send_keys(self.global_username)

        password_input_field = self.driver.find_element(By.CSS_SELECTOR, "input[data-testid='password-input']")
        password_input_field.send_keys(self.global_password)

        register_btn = self.driver.find_element(By.NAME, "register")
        register_btn.click()

        validation_message1 = self.wait_for_element(By.CSS_SELECTOR, "p[data-testid='message']")
        self.assertEqual(validation_message1.text, "User already exists")

        delete_btn = self.driver.find_element(By.NAME, "delete")
        delete_btn.click()

        validation_message2 = self.wait_for_text_in_element(By.CSS_SELECTOR, "p[data-testid='message']",
                                                            text="User deleted!")
        self.assertTrue(validation_message2)

        try:
            user_home_directory = os.path.expanduser("~")

            screenshot_file_path = os.path.join(user_home_directory, "Desktop", "Test 8 screenshot.png")

            self.driver.save_screenshot(screenshot_file_path)

            print(f"Screenshot saved to: {screenshot_file_path}")
        except Exception as e:
            print(f"Error saving screenshot: {str(e)}")


if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()

    test_suite.addTest(ShopTests("test_1_register"))
    test_suite.addTest(ShopTests("test_2_login"))
    test_suite.addTest(ShopTests("test_3_delete_user"))
    test_suite.addTest(ShopTests("test_4_add_bug_to_cart"))
    test_suite.addTest(ShopTests("test_5_clear_inventory_add_new_bug_to_cart"))
    test_suite.addTest(ShopTests("test_6_change_bug_status"))
    test_suite.addTest(ShopTests("test_7_change_price"))
    test_suite.addTest(ShopTests("test_8_register_already_existing_user"))

    unittest.TextTestRunner(verbosity=2).run(test_suite)
