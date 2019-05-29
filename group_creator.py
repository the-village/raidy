import vk_requests
import json
import time
import random
import settings
from selenium import webdriver
import webbrowser
new = 2


token_status = 1
api = vk_requests.create_api(service_token=settings.service_token, interactive=True)
for i in range(1):
    group_id = api.groups.create(title='O' + str(random.randint(100000, 999999)) + '.' + str(i), type='group')['id']
    api.groups.edit(group_id=group_id, access=2, messages=1)
    try:
        vk = webdriver.Chrome()
    except:
        vk = webdriver.Firefox()
    vk.get('http://www.vk.com')
    login = vk.find_element_by_css_selector('#index_email')
    login.send_keys(settings.login)
    password = vk.find_element_by_css_selector('#index_pass')
    password.send_keys(settings.password)
    submit=vk.find_element_by_css_selector('#index_login_button')
    submit.click()
    vk.get(f'https://oauth.vk.com/authorize?client_id=3116505&scope=messages,manage,photos,docs,wall,stories&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&group_ids={group_id}')
    time.sleep(5)
    element = vk.find_element_by_css_selector('button.flat_button.fl_r.button_indent')
    element.click()
    url = vk.current_url
    url = url.split("=")
    token = url[2]
    api.groups.setLongPollSettings(group_id=group_id, enabled=1, api_version="5.92", message_new=1)
    vk.get(f"https://vk.com/club{group_id}?act=messages&tab=bots")
    element = vk.find_element_by_css_selector('div.idd_selected_value')
    element.click()
    time.sleep(10)
    new_group = {group_id: str(token)}
    webbrowser.get(using='google-chrome').open(f"https://vk.com/club{group_id}",new=new)
    print(f"token{token_status}: ")
    print(new_group)
    token_status += 1
print("")
print("")
print("add tokens to <settings.py> and run bot.py and invite bots")
