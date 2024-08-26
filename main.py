# ----- Importações -----
from tkinter import *
from Copilot_AI_v1 import enviar_mensagem
from PIL import Image, ImageTk
import speech_recognition as sr
import pyttsx3
import os
import shutil

# ----- Janela principal -----
janela_principal = Tk()
janela_principal.title("Copilot")
janela_principal.geometry("650x490")
janela_principal.resizable(False, False)
janela_principal.config(background="#565863")

# Cria uma tela preta que receberá as imagens
canvas = Canvas(janela_principal, width=650, height=350, bd=0, highlightthickness=0)
canvas.place(x=0, y=0)
canvas.create_rectangle(0, 0, 650, 350, fill="black")

# ------ Restaura as imagens da pasta 'telas' ------
caminho = "telas"
pasta = os.listdir(caminho)
for arquivo in pasta:
    if arquivo != "informações.png":
        os.remove(f"{caminho}/{arquivo}")

caminho = "telas_backup"
pasta = os.listdir(caminho)
for arquivo in pasta:
    shutil.copyfile(f"{caminho}/{arquivo}", f"telas/{arquivo}")


# -------- Funções para ações dos botões ------
def funcao_botao1() -> None:
    """
    Exibe a imagem 'spotify.png' no canvas criado.
    :return: None
    """
    global canvas
    canvas.delete("all")

    # Carrega a imagem e axibe no canvas
    imagem = Image.open("telas/spotify.png")
    imagem_tk = ImageTk.PhotoImage(imagem)
    canvas.create_image(0, 0, anchor=NW, image=imagem_tk)
    canvas.image = imagem_tk


def funcao_botao2() -> None:
    """
    Exibe a imagem 'mapa.png' no canvas criado.
    :return: None
    """
    global canvas
    canvas.delete("all")

    # Carrega a imagem e axibe no canvas
    imagem = Image.open("telas/mapa.png")
    imagem_tk = ImageTk.PhotoImage(imagem)
    canvas.create_image(0, 0, anchor=NW, image=imagem_tk)
    canvas.image = imagem_tk


def funcao_botao3() -> None:
    """
    Exibe a imagem 'ligação.png' no canvas criado
    :return: None
    """
    global canvas
    canvas.delete("all")

    # Carrega a imagem e axibe no canvas
    imagem = Image.open("telas/ligação.png")
    imagem_tk = ImageTk.PhotoImage(imagem)
    canvas.create_image(0, 0, anchor=NW, image=imagem_tk)
    canvas.image = imagem_tk


def funcao_botao4() -> None:
    """
    Exibe a imagem 'informações.png' no canvas criado
    :return: None
    """
    global canvas
    canvas.delete("all")

    # Carrega a imagem e axibe no canvas
    imagem = Image.open("telas/informações.png")
    imagem_tk = ImageTk.PhotoImage(imagem)
    canvas.create_image(0, 0, anchor=NW, image=imagem_tk)
    canvas.image = imagem_tk


def falar(resposta: str) -> None:
    """
    Recebe uma frase e configura a voz que falará a frase
    :param resposta: Uma string que a IA falará
    :return: None
    """
    if "tocando" in resposta.lower():
        funcao_botao1()
    elif "rota" in resposta.lower():
        funcao_botao2()
    elif "ligando" in resposta.lower():
        funcao_botao3()
    elif "veículo" in resposta.lower():
        funcao_botao4()

    # Configura a voz
    engine = pyttsx3.init()
    engine.setProperty('rate', 250)

    # Define a voz ser usar
    voz = engine.getProperty('voices')
    engine.setProperty('voice', voz[0].id)

    # Converte texto em fala e executa a síntese de voz
    engine.say(resposta)
    engine.runAndWait()


# ------ Função para ação da barra de espaço ------
def espaco_apertado(event) -> None:
    """
    Ativa o microfone, permitindo o usuário de conversar com a IA
    :param event: Evento, que no caso é a 'barra de espaço' ser precionado
    :return: None
    """
    r = sr.Recognizer()

    # Usa o microfone como fonte de áudio
    with sr.Microphone() as fonte:
        print("Fale alguma coisa...")
        audio = r.listen(fonte)

        try:
            falar(enviar_mensagem(r.recognize_google(audio, language='pt-BR').lower()))
            print(r.recognize_google(audio, language='pt-BR').lower())
        except sr.UnknownValueError:
            print("Não foi possível entender a fala")


# ------ Função para carregar e redimensionar as imagens dos ícones ------
def carregar_e_redimensionar_imagem(caminho_imagem, largura, altura) -> None:
    """
    Carerga e redimensiona as imagens da pasta ícone nos respectivos botões
    :param caminho_imagem: Uma string que representa o caminho para as imagens
    :param largura: A largura do botão
    :param altura: A altura do botão
    :return: None
    """
    imagem = Image.open(caminho_imagem)
    imagem_redimensionada = imagem.resize((largura, altura))
    return ImageTk.PhotoImage(imagem_redimensionada)


# ------ Criação dos botões ------
tamanho_botao = 80
espaco_entre_botoes = (650 - 4 * tamanho_botao) / 5

botoes = [funcao_botao1, funcao_botao2, funcao_botao3, funcao_botao4]
icones = ["ícones/Spotify.png", "ícones/Mapa.png", "ícones/Whats.png", "ícones/Engrenagem.png"]

for i in range(4):
    botao = Button(janela_principal, width=90, height=90, command=botoes[i])
    botao.place(x=(i + 1) * espaco_entre_botoes + i * tamanho_botao, y=370)

    # Carregar e redimensionar o ícone
    icone = carregar_e_redimensionar_imagem(icones[i], 100, 100)
    botao.config(image=icone, compound=TOP)
    botao.image = icone  # Manter uma referência para evitar a coleta de lixo

# ------ Vincula evento de teclado para a barra de espaço ------
janela_principal.bind("<space>", espaco_apertado)

janela_principal.mainloop()
