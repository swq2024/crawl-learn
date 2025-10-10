from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
driver.get("https://www.baidu.com")

WAIT = WebDriverWait(driver, 10) # 最多等待10秒

try:
    input_box = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#chat-textarea")))
    input_box.send_keys("Python")

    submit_button = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#chat-submit-button")))
    submit_button.click()

    # 操作完成后暂停，方便观察结果（按 Enter 退出）
    input("Press Enter to close the browser...")
finally:
    driver.quit()