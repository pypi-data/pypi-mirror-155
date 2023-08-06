import os
import time
from PIL import ImageGrab  # pip install Pillow -i https://mirrors.aliyun.com/pypi/simple
from selenium import webdriver  # pip install selenium -i https://mirrors.aliyun.com/pypi/simple
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class get_selenium:
    selenium_object = {
        'url': '',
        'title': '',
        'page_content': '',
    }

    @staticmethod
    def selenium_screenshot2pic(url, pic_name, size=(1920, 1080), pic_savepath=fr'pics', isMobile=False, showPosition=(0, 0), delay=3, log=False, chromedriverPath=r'./chromedriver.exe'):
        """
        selenium 浏览器截图
        :param url: 截图地址
        :param pic_name: 截图名称
        :param size: 截图大小
        :param pic_savepath: 截图保存路径
        :param isMobile: 是否手机模式访问
        :param showPosition: selenium显示位置
        :param delay: 延时截图
        :param log: 显示日志
        :param chromedriverPath: chromedriver路径
        :return:
        """
        if not chromedriverPath:
            print('Please download chromedriver: https://registry.npmmirror.com/binary.html?path=chromedriver/')
            exit()
        if not os.path.exists(pic_savepath):
            os.mkdir(pic_savepath)

        printer = lambda *args, **kwargs: print(*args, **kwargs) if log else False

        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面

        if isMobile:
            mobile_emulation = {
                "deviceMetrics": {"width": size[0], "height": size[1], "pixelRatio": 3.0},  # 定义设备高宽，像素比
                "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"  # 通过UA来模拟
            }
            chrome_options.add_experimental_option('mobileEmulation', mobile_emulation)

            # chrome_options.add_experimental_option("mobileEmulation", {"deviceName": "iPhone 6"})

        driver = webdriver.Chrome(options=chrome_options, service=Service(chromedriverPath))  # python新版本
        # driver = webdriver.Chrome(options=chrome_options, executable_path='../../self/20191014_selenium_getTitle/chromedriver_win32/chromedriver.exe')  # python旧版本
        driver.set_window_rect(showPosition[0], showPosition[1], size[0], size[1])  # 设置摆放位置
        # driver.maximize_window()  # 最大化浏览器
        driver.implicitly_wait(10)
        try:
            driver.get(url)
            time.sleep(delay)
            printer('selenium visiting URL ==>', url)

            # region 补充selenium_object
            try:
                get_selenium.selenium_object['url'] = driver.current_url
            except Exception as e:
                printer('url -> error:', e)
            try:
                get_selenium.selenium_object['title'] = driver.title
            except Exception as e:
                printer('title -> error:', e)
            try:
                get_selenium.selenium_object['page_content'] = driver.page_source
            except Exception as e:
                printer('page_content -> error:', e)
            # endregion

            im = ImageGrab.grab((showPosition[0] + 10, showPosition[1], size[0], size[1]))
            im.save(fr'{pic_savepath}/{pic_name}.jpg', 'png')
        except Exception as e:
            printer('error', e)
            pass
        finally:
            driver.quit()
        return get_selenium.selenium_object

    @staticmethod
    def selenium_content(url, isMobile=False, log=False, chromedriverPath=r'./chromedriver.exe'):
        """
        selenium 获取内容
        :param url: 访问的url
        :param isMobile: 是否手机模式访问
        :param log: 显示日志
        :param chromedriverPath:  chromedriver路径
        :return:
        """
        if not chromedriverPath:
            print('Please download chromedriver: https://registry.npmmirror.com/binary.html?path=chromedriver/')
            exit()

        printer = lambda *args, **kwargs: print(*args, **kwargs) if log else False

        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面

        if isMobile:
            mobile_emulation = {
                "deviceMetrics": {"width": 192, "height": 108, "pixelRatio": 3.0},  # 定义设备高宽，像素比
                "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"  # 通过UA来模拟
            }
            chrome_options.add_experimental_option('mobileEmulation', mobile_emulation)

            # chrome_options.add_experimental_option("mobileEmulation", {"deviceName": "iPhone 6"})

        driver = webdriver.Chrome(options=chrome_options, service=Service(chromedriverPath))  # python新版本
        # driver = webdriver.Chrome(options=chrome_options, executable_path='../../self/20191014_selenium_getTitle/chromedriver_win32/chromedriver.exe')  # python旧版本
        driver.set_window_rect(0, 0, 192, 108)  # setting position
        # driver.maximize_window()  # browser maximum
        driver.implicitly_wait(10)
        try:
            driver.get(url)
            printer('selenium visiting URL ==>', url)

            # region fill selenium_object
            try:
                get_selenium.selenium_object['url'] = driver.current_url
            except Exception as e:
                printer('url -> error:', e)
            try:
                get_selenium.selenium_object['title'] = driver.title
            except Exception as e:
                printer('title -> error:', e)
            try:
                get_selenium.selenium_object['page_content'] = driver.page_source
            except Exception as e:
                printer('page_content -> error:', e)
            # endregion

        except Exception as e:
            print('error', e)
            pass
        finally:
            driver.quit()
        return get_selenium.selenium_object


if __name__ == '__main__':
    # r = get_selenium.selenium_screenshot2pic(url='http://www.baidu.com', pic_name='www.baidu.com', isMobile=True)  # http://lqfbwvhz.vftg.vip/index.php http://rljwt.kityc.xyz/#/no_password
    # r = get_selenium.selenium_content('http://www.baidu.com')
    # print(r)
    pass
