import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class TestAuthModule(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.base_url = "http://localhost/quiz-pengupil"

    def setUp(self):
        # Clear session sebelum tiap test
        self.driver.get(f"{self.base_url}/index.php?action=logout")
        time.sleep(0.5)
    def test_01_tc_reg_01_register_success(self):
        """TC-REG-01: Registrasi Berhasil"""
        driver = self.driver
        driver.get(f"{self.base_url}/register.php")
        
        driver.find_element(By.ID, "name").send_keys("User Tester Valid")
        driver.find_element(By.ID, "InputEmail").send_keys("valid@mail.com")
        driver.find_element(By.ID, "username").send_keys("uservalid123")
        driver.find_element(By.ID, "InputPassword").send_keys("password123")
        driver.find_element(By.ID, "InputRePassword").send_keys("password123")
        
        driver.find_element(By.NAME, "submit").click()
        time.sleep(1)
        
        self.assertIn("index.php", driver.current_url)

    def test_02_tc_reg_02_password_mismatch(self):
        driver = self.driver
        driver.get(f"{self.base_url}/register.php")
        
        driver.find_element(By.ID, "name").send_keys("User Mismatch")
        driver.find_element(By.ID, "InputEmail").send_keys("mismatch@mail.com")
        driver.find_element(By.ID, "username").send_keys("userbedapass")
        driver.find_element(By.ID, "InputPassword").send_keys("password123")
        driver.find_element(By.ID, "InputRePassword").send_keys("passwordBeda")
        
        driver.find_element(By.NAME, "submit").click()
        time.sleep(1)
        
        self.assertIn("Password tidak sama !!", driver.page_source)

    def test_03_tc_reg_03_empty_form(self):
        """TC-REG-03: Form Register Kosong"""
        driver = self.driver
        driver.get(f"{self.base_url}/register.php")
        
        driver.find_element(By.NAME, "submit").click()
        time.sleep(1)
        
        self.assertIn("Data tidak boleh kosong !!", driver.page_source)

    def test_04_tc_lgn_01_login_success(self):
        """TC-LGN-01: Login Berhasil (Memakai akun dari TC-REG-01)"""
        driver = self.driver
        driver.get(f"{self.base_url}/login.php")
        
        driver.find_element(By.ID, "username").send_keys("uservalid123")
        driver.find_element(By.ID, "InputPassword").send_keys("password123")
        
        driver.find_element(By.NAME, "submit").click()
        time.sleep(1)
        
        self.assertIn("index.php", driver.current_url)
        self.assertIn("uservalid123", driver.page_source)

    def test_05_tc_lgn_02_unregistered_user(self):
        """TC-LGN-02: Akun Tidak Terdaftar"""
        driver = self.driver
        driver.get(f"{self.base_url}/login.php")
        
        driver.find_element(By.ID, "username").send_keys("userGhoib999")
        driver.find_element(By.ID, "InputPassword").send_keys("sembarang123")
        
        driver.find_element(By.NAME, "submit").click()
        time.sleep(1)
        
        self.assertIn("Register User Gagal !!", driver.page_source)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()