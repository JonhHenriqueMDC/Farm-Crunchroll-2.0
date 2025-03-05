from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from twocaptcha import TwoCaptcha
from faker import Faker
from webdriver_manager.chrome import ChromeDriverManager
import time

solver = TwoCaptcha('') # aqui voce colcoa a API da sua conta da 2Captcha

chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

stealth(driver,
        languages=["pt-BR", "pt"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        run_on_insecure_origins=True,
        )

fake = Faker()

first_name = fake.first_name()
last_name = fake.last_name()
email = f"{first_name}{last_name}@hotmail.com".lower()
senha = "" # a senha da conta do  crunchroll

################################
# Na parte de Baixo voce tem que colcoar os dados de um cartao para fazer a ativacao
# Nao recomendamos usar o cartao fisico ou o cartao  digital para essa automacao use 
# Um cartao temporario que certos bancos possuem que voce pode apagar ele ou ele se
# auto apaga depois de  24 horas.
################################

nomecartao = ""
numerocartao = ""
cvv = ""
cpf = ""
validade_mes = ""
validade_ano = ""

driver.get("https://www.crunchyroll.com/pt-br/premium?referrer=newweb_organic_header&return_url=https%3A%2F%2Fwww.crunchyroll.com%2Fpt-br%2F%3Fsrsltid%3DAfmBOoq31Tkmm7-fSJPHHPNDMgZPJz1pUGa4H-gLzAYBaf-jL3f1Nz7g#plans")

time.sleep(5)

try:
    botao_testar = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'product-button-best-deal')]//span[contains(text(), 'Comece um teste grátis de 7 dias')]"))
    )
    actions = ActionChains(driver)
    actions.move_to_element(botao_testar).pause(1).click().perform()
except Exception as e:
    print("Erro ao clicar no botão 'Comece um teste grátis de 7 dias':", e)
    driver.quit()
    exit()

try:
    campo_email = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "login"))
    )
    for char in email:
        campo_email.send_keys(char)
        time.sleep(0.1)
    campo_email.send_keys(Keys.RETURN)
except Exception as e:
    print("Erro ao preencher o email:", e)
    driver.quit()
    exit()

try:
    campo_senha = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    for char in senha:
        campo_senha.send_keys(char)
        time.sleep(0.1)
    campo_senha.send_keys(Keys.RETURN)
except Exception as e:
    print("Erro ao preencher a senha:", e)
    driver.quit()
    exit()

time.sleep(15)

try:
    result = solver.hcaptcha(
        sitekey='0x4AAAAAAADnPIDROrmt1Wwj', # coloque o Site-Key do captchar
        url=driver.current_url
    )
    captcha_code = result['code']
    print("Captcha resolvido:", captcha_code)
    driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{captcha_code}";')
except Exception as e:
    print("Erro ao resolver o captcha:", e)

try:
    campo_nome_cartao = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "credit_card[full_name]"))
    )
    campo_nome_cartao.send_keys(nomecartao)

    campo_numero_cartao = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "credit_card[card_number]"))
    )
    campo_numero_cartao.send_keys(numerocartao)

    select_mes = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "credit_card[expiration_month]"))
    )
    Select(select_mes).select_by_value(validade_mes)

    select_ano = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "credit_card[expiration_year]"))
    )
    Select(select_ano).select_by_value(validade_ano)

    campo_cvv = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "credit_card[cvv2]"))
    )
    campo_cvv.send_keys(cvv)

    campo_cpf = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "credit_card[document]"))
    )
    campo_cpf.send_keys(cpf)
except Exception as e:
    print("Erro ao preencher os dados do cartão:", e)
    driver.quit()
    exit()

time.sleep(5)

try:
    botao_testar = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Iniciar Teste Gratuito')]"))
    )
    actions = ActionChains(driver)
    actions.move_to_element(botao_testar).pause(1).click().perform()
except Exception as e:
    print("Erro ao clicar no botão 'Iniciar Teste Gratuito':", e)
    driver.quit()
    exit()

time.sleep(5)

login_content = f"login: {email}\nsenha: {senha}"
with open("login_Crunch.txt", "w") as file:
    file.write(login_content)

time.sleep(2)
driver.quit()