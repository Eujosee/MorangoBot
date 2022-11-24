import time
from tkinter import *
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# criamos um array vazio para cada item
contatos = []
mensagem = []
imagem = []

#função para adicionar um contato a lista de
def addContato():
          contatos.append(buscarContatos.get()) #pega os contatos do input tkinter
          buscarContatos.delete(0, 'end')

def addMensagem():
          mensagem.append(buscarMensagem.get("1.0", "end-1c"))
          buscarMensagem.delete("1.0", 'end-1c')
          
          
def addImagem():
          imagens = filedialog.askopenfilename(initialdir="/", title="Selecione um arquivo", 
          filetype=(("Image Files", [".jpg", ".png", ".jpeg"]), ("all files", ".")))
          imagem.append(imagens)
          print(imagem)

#função para resetar os valores dos inputs(para que não haja a necessidade de fechar a janela)
def reiniciar():
          contatos.clear()
          mensagem.clear()
          imagem.clear()

          
def iniciar():
          
          driver = webdriver.Chrome(ChromeDriverManager().install())
          driver.get('https://web.whatsapp.com/')
          time.sleep(60)

          #função para buscar os contatos
          def cade_contato(contato):
                    achar_contato = driver.find_element(By.XPATH, '//div[contains(@class, "copyable-text")]') #seleciona a div onde é feita a pesquisa do contato
                    time.sleep(2)
                    achar_contato.click()
                    achar_contato.send_keys(contato) #digita o contato passado como parametro e em seguida da enter
                    achar_contato.send_keys(Keys.ENTER) 
                    time.sleep(1)
    
          #função para enviar as mensagens
          def enviar_mensagem(mensagens):
                    for mensagem in mensagens:
                              mensagemFormatada = mensagem.split('\n') #para evitar que as mensagens sejam enviadas "coladas", é feita a divisão 
                              enviar_mensagem = driver.find_element(By.XPATH, '//p[contains(@class, "selectable-text copyable-text")]') #seleciona a caixa de envio de mensagem
                              enviar_mensagem.click()
                              for msg in mensagemFormatada:          
                                        enviar_mensagem.send_keys(msg)
                                        enviar_mensagem.send_keys(Keys.SHIFT, Keys.ENTER)
                              enviar_mensagem.send_keys(Keys.ENTER)
                              time.sleep(1)
          
          #função para enviar as imagens
          def enviar_imagem(imagens):
                    for imagem in imagens:
                              driver.find_element(By.CSS_SELECTOR, 'span[data-icon="clip"]').click() 
                              attach = driver.find_element(By.CSS_SELECTOR, 'input[type=file') #seleciona o icone de envio de imagem
                              attach.send_keys(imagem)
                              time.sleep(1)
                              send = driver.find_element(
                                        By.XPATH, '//div[contains(@class, "_165_h _2HL9j")]')
                              send.click(1)
                              time.sleep(1)
          
          
          for contato in contatos: #loop para passar por todos os contatos do array
                    cade_contato(contato) #chama a função de buscar contato passando o item do array como parametro
                    if len(mensagem) > 0: #verifica se há mensagens no array 
                              enviar_mensagem(mensagem)
                    if len(imagem) > 0: #verifica se há imagens no array
                              enviar_imagem(imagem)
                    time.sleep(1)
          reiniciar() #após tudo isso, ele reinicia os valores dos arrays
          
janela = Tk()
janela.title("Morango Chatbot") #titulo da janela
janela.geometry("400x400") #tamanho da janela tkinter

#Pesquisa de contato/grupo
placeHolder = Label(janela, text="Para quais grupos/contatos deseja enviar? ")
placeHolder.grid(column=0, row=4)

buscarContatos = Entry(janela)
buscarContatos.grid(column=1, row=4)

btnPesquisar = Button(janela, text="Enviar", command=addContato)
btnPesquisar.grid(column=2, row=4)

#Mensagem
labelMsg = Label(janela, text="Mensagem:")
labelMsg.grid(column=0, row=5)

buscarMensagem = Text(janela, height= 5)
buscarMensagem.place(x= 150, y = 100, width= 100)

Button(janela, text="Adicionar mensagem", command=addMensagem).place(x= 200, y= 200, width= 100)

Button(janela, text="Enviar", command=iniciar).place(x= 200, y= 150, width= 100)



janela.mainloop()