from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import xlwt
import time


# 保持浏览器窗口不关闭
# options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)
# browser = webdriver.Chrome(options=options)

browser = webdriver.Chrome()
WAIT = WebDriverWait(browser, 10) # 最多等待10秒
browser.set_window_size(1400, 900) # 设置浏览器窗口大小

book = xlwt.Workbook(encoding="utf-8", style_compression=0)
sheet = book.add_sheet('蔡徐坤篮球', cell_overwrite_ok=True)
sheet.write(0, 0, '视频标题')
sheet.write(0, 1, '视频链接')
sheet.write(0, 2, '视频时长')
sheet.write(0, 3, '播放量')
sheet.write(0, 4, '弹幕数')
sheet.write(0, 5, '发布时间')

n = 1

def save_to_excel(soup):
    list = soup.find(class_='search-layout clearfix').find_all(class_='bili-video-card')
    for item in list:
        item_title = item.find('h3').get('title')
        print('正在爬取:', item_title)
        item_link = item.find('a').get('href')
        print("链接:", item_link)
        item_dura = item.find(class_='bili-video-card__stats__duration').text
        print("时长:", item_dura)
        # 使用 find 方法的 class_ 参数来查找元素
        stats_left = item.find(class_='bili-video-card__stats--left')            
        item_view = stats_left.find_all('span')[0].text
        print("播放量:", item_view)
        item_biubiu = stats_left.find_all('span')[3].text
        print("弹幕数:", item_biubiu)
        item_date = item.find(class_='bili-video-card__info--date').text
        print("发布时间:", item_date)

        print(item_title, "爬取完成")

        global n
        sheet.write(n, 0, item_title)
        sheet.write(n, 1, item_link)
        sheet.write(n, 2, item_dura)
        sheet.write(n, 3, item_view)
        sheet.write(n, 4, item_biubiu)
        sheet.write(n, 5, item_date)
        n += 1

def get_source():
    print("正在获取页面信息...")
    try:
        # 等待搜索结果容器出现
        WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.search-content > div.search-page-wrapper')))
        # 等待视频卡片加载完成
        WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.bili-video-card')))
        
        # 确保页面完全加载
        time.sleep(1)
        
        html = browser.page_source
        soup = BeautifulSoup(html, "lxml")
        
        save_to_excel(soup)
    except TimeoutException as e:
        print(f"页面加载超时: {str(e)}")
        browser.refresh()
        time.sleep(2)
        get_source()
    except Exception as e:
        print(f"获取数据时出错: {str(e)}")
        browser.refresh()
        time.sleep(2)
        get_source()

def search():
    try:
        print("开始访问bilibili...")
        browser.get("https://www.bilibili.com/")

        input = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".nav-search-input")))
        input.send_keys('蔡徐坤 篮球')

        submit = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.nav-search-btn')))
        submit.click()

        print("跳转到搜索结果页面...")
        all_h = browser.window_handles # 获取所有窗口句柄
        browser.switch_to.window(all_h[1]) # 切换到新打开的窗口
        get_source()

        total_pages = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.vui_pagenation > div.vui_pagenation--btns > button:nth-last-child(2)'))) # button:nth-last-child(2)选择倒数第二个按钮，即总页数
        print(f"总页数: {int(total_pages.text)}")
        return int(total_pages.text)
    except TimeoutException:
        return search()

def next_page(page_num):
    try:
        print(f'开始获取第{page_num}页数据...')
        # 等待页面完全加载
        WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.vui_pagenation')))
        
        # 确保元素可见和可点击
        next_btn = WAIT.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.vui_pagenation > div.vui_pagenation--btns > button:last-child')))
        
        # 使用JavaScript点击按钮，这样更可靠
        browser.execute_script("arguments[0].click();", next_btn)
        
        # 等待新页面加载完成
        WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.search-content')))
        WAIT.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '.vui_pagenation > div.vui_pagenation--btns > button.vui_button--active'), 
            str(page_num)))
        
        # 短暂等待确保页面稳定
        time.sleep(1)
        
        get_source()

    except TimeoutException as e:
        print(f"超时错误: {str(e)}")
        browser.refresh()
        time.sleep(2)  # 刷新后等待页面加载
        return next_page(page_num)
    except Exception as e:
        print(f"发生错误: {str(e)}")
        browser.refresh()
        time.sleep(2)
        return next_page(page_num)

def main():
    try:
        total = search()
        print('搜索结果总页数为:', total)
        for i in range(2, int(total + 1)):
            next_page(i)
    finally:
        browser.quit()

if __name__ == "__main__":
    try:
        main()
        book.save('蔡徐坤篮球.xls') # 保存到本地
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序发生错误: {str(e)}")
    finally:
        print("程序结束")