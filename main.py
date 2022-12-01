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


# função para adicionar um contato a lista de
def addContato():
    contatos.append(buscarContatos.get())  # pega os contatos do input tkinter
    buscarContatos.delete(0, 'end')
    contLabel["text"] = ', '.join(contatos)


def addMensagem():
    mensagem.append(buscarMensagem.get("1.0", "end-1c"))
    buscarMensagem.delete("1.0", 'end-1c')


def addImagem():
    imagens = filedialog.askopenfilename(initialdir="/", title="Selecione um arquivo",
                                         filetype=(("Image Files", [".jpg", ".png", ".jpeg"]), ("all files", ".")))
    imagem.append(imagens)
    ImgLabel["text"] = ', '.join(imagem)


def removerContatos():
    contatos.clear()
    contLabel["text"] = ''


def removerMensagem():
    mensagem.clear()


def removerImagem():
    imagem.clear()
    ImgLabel["text"] = ''


# função para resetar os valores dos inputs(para que não haja a necessidade de fechar a janela)
def reiniciar():
    contatos.clear()
    mensagem.clear()
    imagem.clear()


def iniciar():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://web.whatsapp.com/')
    time.sleep(25)

    # função para buscar os contatos
    def cade_contato(contato):
        achar_contato = driver.find_element(By.XPATH,
                                            '//div[contains(@class, "copyable-text")]')  # seleciona a div onde é feita a pesquisa do contato
        time.sleep(2)
        achar_contato.click()
        achar_contato.send_keys(contato)  # digita o contato passado como parametro e em seguida da enter
        achar_contato.send_keys(Keys.ENTER)
        time.sleep(1)

    # função para enviar as mensagens
    def enviar_mensagem(mensagens):
        for mensagem in mensagens:
            mensagemFormatada = mensagem.split(
                '\n')  # para evitar que as mensagens sejam enviadas "coladas", é feita a divisão
            enviar_mensagem = driver.find_element(By.XPATH,
                                                  '//p[contains(@class, "selectable-text copyable-text")]')  # seleciona a caixa de envio de mensagem
            enviar_mensagem.click()
            for msg in mensagemFormatada:
                enviar_mensagem.send_keys(msg)
                enviar_mensagem.send_keys(Keys.SHIFT, Keys.ENTER)
            enviar_mensagem.send_keys(Keys.ENTER)
            time.sleep(1)

    # função para enviar as imagens
    def enviar_imagem(imagens):
        for imagem in imagens:
            driver.find_element(By.CSS_SELECTOR, 'span[data-icon="clip"]').click()
            attach = driver.find_element(By.CSS_SELECTOR, 'input[type=file')  # seleciona o icone de envio de imagem
            attach.send_keys(imagem)
            time.sleep(1)
            send = driver.find_element(By.XPATH, "//div[contains(@class, '_165_h _2HL9j')]")
            send.click()
            time.sleep(1)

    for contato in contatos:  # loop para passar por todos os contatos do array
        cade_contato(contato)  # chama a função de buscar contato passando o item do array como parametro
        if len(mensagem) > 0:  # verifica se há mensagens no array
            enviar_mensagem(mensagem)
        if len(imagem) > 0:  # verifica se há imagens no array
            enviar_imagem(imagem)
        time.sleep(1)
    reiniciar()  # após tudo isso, ele reinicia os valores dos arrays


janela = Tk()
photo = PhotoImage(file='Morango.png')
janela.iconphoto(False, photo)
janela.title("Morango Chatbot")  # titulo da janela

# Redimensionamento da janela
janela.geometry("570x570")

#Mensagem de boas vindas
benvinde = Label(janela, text="Olá eu sou o ChatBot Morango!")
benvinde.grid(row=0,column=1,columnspan=6)
benvinde2 = Label(janela, text="O chatbot que vai te ajudar a enviar mensagens de forma automatizada")
benvinde2.grid(row=1,column=1,columnspan=6)

pularlinha = Label(janela, text="")
pularlinha.grid(row=2,column=1,columnspan=6)


# Pesquisa de contato/grupo
placeHolder = Label(janela, text="Nome do contato ou grupo: ")
placeHolder.grid(row=3,column=2,columnspan=2, padx=20, pady=5)

buscarContatos = Entry(font=('Century 12'), width=45)
buscarContatos.grid(row=4,column=3,columnspan=3, rowspan=1, padx=20, pady=5)
contLabel = Label(janela, text="")
contLabel.grid(row=5,column=3)

btnPesquisar = Button(janela, text="Adicionar a lista", command=addContato)
btnPesquisar.grid(row=4,column=6)

btnPesquisar = Button(janela, text="Remover contatos", command=removerContatos)
btnPesquisar.grid(row=5,column=6)

pularlinha2 = Label(janela, text="")
pularlinha2.grid(row=6,column=3)


# Mensagem
labelMsg = Label(janela, text="Mensagem:")
labelMsg.grid(row=7,column=2,columnspan=2)

buscarMensagem = Text(janela, height=8, width=50)
buscarMensagem.grid(row=8,column=3,columnspan=3, rowspan=1, padx=5, pady=5)
Button(janela, text="Adicionar mensagem", command=addMensagem).grid(row=9,column=4,columnspan=3)

btnPesquisar = Button(janela, text="Remover mensagem", command=removerMensagem)
btnPesquisar.grid(row=10,column=4, columnspan=4)

pularlinha3 = Label(janela, text="")
pularlinha3.grid(row=10,column=3)


# Imagem
labelImg = Label(janela, text="Adicionar imagem: ")
labelImg.grid(row=11,column=3)

ImgLabel = Label(janela, text="")
ImgLabel.grid(row=12,column=3,columnspan=3, rowspan=1, padx=5, pady=5)

imgBtn = Button(janela, text="Procurar", command=addImagem)
imgBtn.grid(row=12,column=6)
btnPesquisar = Button(janela, text="Remover imagens", command=removerImagem)
btnPesquisar.grid(row=13,column=6)

pularlinha4 = Label(janela, text="")
pularlinha4.grid(row=14,column=3)

btnEnviar = Button(janela, text="Enviar", command=iniciar,
                   height=2, width=15, foreground='red', font=('bold', 15, 'underline'))
btnEnviar.grid(row=15,column=1,columnspan=6)

janela.mainloop()