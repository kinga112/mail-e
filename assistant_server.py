from aiohttp import web
import asyncio
import socketio
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
# from selenium.common.exceptions import StaleElementReferenceException

def start():
    """
    Start socket io server, which hosts chat-gpt selenium bot that forwards responds to front end application.
    Hosted on localhost:8999
    """
    sio = socketio.AsyncServer(async_mode='aiohttp', async_handlers=True, cors_allowed_origins="*")
    app = web.Application()
    sio.attach(app)

    print('Setting up Assistant...')
    options = Options()
    options.add_argument('--headless')
    # firefox must be updated/installed
    driver = webdriver.Firefox(options=options)
    driver.get('https://chatgpt.com/')

    # close login modal if needed
    try:
        close_modal = WebDriverWait(driver, 3).until(
            # continue with no login - web element
            EC.presence_of_element_located((By.XPATH, '//*[@id="radix-:r7:"]/div/div/a'))
        )
        close_modal.click()
    except Exception as e:
        pass

    print('Finished setting up Assistant')

    @sio.event
    async def connect(sid, environ):
        """
        Outputs ID from client on connect
        """
        print('[INFO] Connected to client:', sid)

    @sio.event
    async def disconnect(sid):
        """
        Outputs ID from client on disconnect. Occures when user closes application.
        """
        print('[INFO] Client disconnected:', sid)
        driver.close()
        await app.shutdown()
        await app.cleanup()

    @sio.event
    async def ask_eve(sid, prompt, index):
        """
        Give assistant prompt and get an async response stream emitted to socket.
        :param prompt: question to ask assistant.
        :param index: the count for how many questions have been sent. Needs index to fetch correct html element with selenium.
        """
        print('Prompt: ', prompt)
        # text area for prompt - web element
        # input = driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[1]/div/form/div/div[2]/div/textarea')
        input = WebDriverWait(driver, 10).until(
            # text area for prompt - web element
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[1]/div/form/div/div[2]/div/textarea'))
        )
        driver.execute_script(f'arguments[0].value=`{prompt}`;', input)

        # add to end of prompt to know when answer is complete
        input.send_keys('Send "DONE" all capitals when you are finished sending information')

        button = WebDriverWait(driver, 10).until(
            # Submit prompt button - web element
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/div[1]/div/form/div/div[2]/div/button'))
        )
        button.click()

        while True:
            await asyncio.sleep(0.1)
            try:
                # list of chat-gpt responses
                elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-message-author-role=assistant]')
                # select response by index
                element = elements[index]
                if 'DONE' in element.text:
                    final = element.text.replace('DONE', '')
                    await sio.emit(event='ask_response', data={'response': final})
                    break
                else:
                    await sio.emit(event='ask_response', data={'response': element.text})
            except:
                pass

    web.run_app(app, host='localhost', port=8999)
