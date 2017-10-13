from selenium import webdriver
from time import sleep

browser = webdriver.Firefox()
browser.get('https://www.amazon.cn/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=cnflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.cn%2Fref%3Dnav_signin%3Ftag%3Dzcn0e-23&switch_account=')

sleep(5)

(browser.find_element_by_id("ap_email")).send_keys("yamieborn@hotmail.com")
password = input('password:')
(browser.find_element_by_id("ap_password")).send_keys(password)
(browser.find_element_by_id("signInSubmit")).click()


browser.get('https://www.amazon.cn/mn/dcw/myx.html/ref=kinw_myk_redirect#/home/content/pdocs/dateDsc/%E7%AC%AC')
input('搜索好了？：')


num9 = 9
while num9 == 9:
    dels = browser.find_elements_by_xpath("//label[@class='listViewIconPosition_myx grayGradient_myx']")
    for e in dels:
        e.click()
        num9 = num9-1
        if num9 <= 0:
            num9 = 9
            break
    if len(dels) == 0:
        break
    browser.find_element_by_xpath("//*[@id='contentAction_delete_myx']/div/a/span/button").click()
    sleep(2)
    browser.find_element_by_xpath("//*[@id='dialogButton_ok_myx']/span/button").click()
    sleep(10)
    browser.find_element_by_xpath("//*[@id='dialogButton_ok_myx']/span/button").click()
    sleep(2)