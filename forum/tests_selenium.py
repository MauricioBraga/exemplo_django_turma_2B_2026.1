from os import link

from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

import time



class BaseTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        opts = Options()
        # opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--window-size=1280,800")

        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service, options=opts)

        cls.wait = WebDriverWait(cls.driver, 10)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "driver"):
            cls.driver.quit()
        super().tearDownClass()



class TestePaginaInicial(BaseTestCase):

    def test_deve_carregar_pagina_inicial(self):
        print("Testando carregamento da página inicial...")
        self.driver.get(f"{self.live_server_url}/forum/")

        body = self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        self.assertIn("Exemplo StackOverflow", self.driver.title)
        
        time.sleep(3)  # Apenas para visualizar o teste, pode ser removido
        




class TesteCriacaoPergunta(BaseTestCase):

    def test_deve_criar_pergunta(self):
        print("Testando criação de pergunta...")
        
        self.driver.get(f"{self.live_server_url}/forum/inserir/")
        
        # acessa os campos do formulário de criação de pergunta
        titulo = self.wait.until(
            EC.presence_of_element_located((By.NAME, "titulo"))
        )
        detalhe = self.wait.until(
            EC.presence_of_element_located((By.NAME, "detalhe"))
        )

        tentativa = self.wait.until(
            EC.presence_of_element_located((By.NAME, "tentativa"))
        )

        # preenche os dados da pergunta.
        titulo.send_keys("Como usar o Selenium com Django?")

        time.sleep(1)  # Apenas para visualizar o teste, pode ser removido

        detalhe.send_keys("Podem me indicar tutoriais ou exemplos de uso do Selenium para testes em Django?")

        time.sleep(1)  # Apenas para visualizar o teste, pode ser removido

        tentativa.send_keys("Não tentei nada ainda.")

        time.sleep(3)  # Apenas para visualizar o teste, pode ser removido
        
        # clica no botão de submit do formulário
        self.driver.find_element(By.TAG_NAME, "form").submit()

        # espera a página recarregar e exibir conteúdo
        body = self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # verifica se o título da pergunta criada aparece na página
        self.assertIn("Como usar o Selenium com Django?", body.text)
        
        time.sleep(3)  # Apenas para visualizar o teste, pode ser removido



class TesteCriacaoPerguntaComAcessoPelaPaginaPrincipal(BaseTestCase):

    def test_deve_acessar_pergunta_criada_pela_pagina_principal_e_exibir_detalhes_pergunta(self):
        print("Testando criação de pergunta e acesso pela página principal...")
        # cria pergunta
        self.driver.get(f"{self.live_server_url}/forum/inserir/")

        titulo = self.wait.until(
            EC.presence_of_element_located((By.NAME, "titulo"))
        )
        detalhe = self.wait.until(
            EC.presence_of_element_located((By.NAME, "detalhe"))
        )

        titulo.send_keys("Como criar jogos no Unity?")

        time.sleep(1)  # Apenas para visualizar o teste, pode ser removido

        detalhe.send_keys("Podem me ajudar por favor?")

        time.sleep(1)  # Apenas para visualizar o teste, pode ser removido

        # grava a pergunta
        self.driver.find_element(By.TAG_NAME, "form").submit()

        # espera redirecionamento/listagem
        self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        time.sleep(1)  # Apenas para visualizar o teste, pode ser removido

        # vai para página inicial
        self.driver.get(f"{self.live_server_url}/forum/")

        # clica no link da pergunta criada para acessar detalhes
        link = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Como criar jogos no Unity?"))
        )

        time.sleep(1)  # Apenas para visualizar o teste, pode ser removido

        link.click()

        body = self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        time.sleep(3)  # Apenas para visualizar o teste, pode ser removido

        self.assertIn("Podem me ajudar por favor?", body.text)



class TesteResposta(BaseTestCase):

    def test_responder_pergunta(self):
        print("Testando resposta a pergunta...")
        # acessa a página de criação de pergunta
        self.driver.get(f"{self.live_server_url}/forum/inserir/")

        # pega os campos do formulário para criar a pergunta
        titulo = self.wait.until(
            EC.presence_of_element_located((By.NAME, "titulo"))
        )
        detalhe = self.wait.until(
            EC.presence_of_element_located((By.NAME, "detalhe"))
        )

        # envia os dados da pergunta
        titulo.send_keys("Pergunta resposta")
        detalhe.send_keys("Conteúdo resposta")

        time.sleep(1)  # Apenas para visualizar o teste, pode ser removido

        # grava a pergunta
        self.driver.find_element(By.TAG_NAME, "form").submit()

        # espera página atualizar
        self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # acessa listagem de perguntas na página inicial
        self.driver.get(f"{self.live_server_url}/forum/")

        self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # clica no link da pergunta criada para acessar os detalhes dela
        self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Pergunta resposta"))
        ).click()

        # pega o botão de nova resposta e clica nele
        botao = self.driver.find_element(By.NAME, "nova_resposta")
        botao.click()


        self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # responde a pergunta
        resposta = self.wait.until(
            EC.presence_of_element_located((By.NAME, "texto_resposta"))
        )

        time.sleep(3)  # Apenas para visualizar o teste, pode ser removido

        resposta.send_keys("Minha resposta")

        time.sleep(3)  # Apenas para visualizar o teste, pode ser removido

        # grava a resposta
        # self.driver.find_element(By.TAG_NAME, "form").submit()

        botao_resposta = self.driver.find_element(By.NAME, "salvar_resposta")
        botao_resposta.click()

        

        body = self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        time.sleep(3)  # Apenas para visualizar o teste, pode ser removido

        self.assertIn("Minha resposta", body.text)