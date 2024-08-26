# ----- Importações -----
# ------ 'musica' ------
import spotipy
import webbrowser
# ------ 'encontrar_rota' ------
import folium
import requests
import polyline
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import time
import pyautogui
import os
import google.generativeai as genai
# ------ 'musica'/'encontrar_rota'/'ligacao' ------
from PIL import Image, ImageDraw
from deep_translator import GoogleTranslator

# ----- Funções ------


def musica(nome: str, banda: str = '') -> str:
    """
    Essa função é responsável por se conectar com o spotify e reproduzir uma música na tela do carro.
    :param nome: Uma string que representa o nome de uma música que o usuário deseja ouvir
    :param banda: Uma string que representa o nome da banda que fez a música que o usuário deseja ouvir
    :return: None
    """

    musica = f"{nome}, {banda} "

    # ----- Variáveis -----
    clientID = "Coloque seu Client ID do Spotify aqui"
    clientSecret = "Coloque seu Cliente Secret do Spotify aqui"
    redirect_uri = 'http://google.com/callback/'

    # Acessa a Api do spotfy e cria um objeto chamado spotfy autenticado para fazer solicitações à API em nome do utilizador.
    oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri)
    token_dict = oauth_object.get_access_token()
    token = token_dict['access_token']
    spotifyObject = spotipy.Spotify(auth=token)

    # Busca uma música no Spotify, extrai o link para ouvir essa música no Spotify e abre o link no navegador da web.
    results = spotifyObject.search(musica, 1, 0, "track")
    songs_dict = results['tracks']
    song_items = songs_dict['items']
    song = song_items[0]['external_urls']['spotify']
    webbrowser.open(song)

    # ---------------------------------------------------------
    imagem = Image.open("telas_backup/spotify.png")

    # Cria um objeto ImageDraw
    desenho = ImageDraw.Draw(imagem)

    # Define o ponto onde você quer escrever a palavra
    ponto = (201, 70)
    desenho.text(ponto, musica.capitalize(), fill="white", font_size=38)
    imagem.save("telas/spotify.png")


def encontrar_rota(destino: str) -> None:
    """
    Essa função recebe como parametro o destino do usuário e retorna o caminho de gps até ele.
    :param destino: Uma string que representa o endereço do destino para o qual deseja-se traçar a rota.
    :return: None.
    """

    def obter_coordenadas(destino: str) -> dict or None:
        """
        Essa função é reponsável por obter as coordenadas do destino fornecido pelo usuário.
        :param destino: Uma string que representa o endereço do destino para o qual deseja-se traçar a rota.
        :return: None se o endereço não puder ser geocodificado ou as coordenadas não estiverem disponíveis.
        """
        geolocalizador = Nominatim(user_agent="my_geocoder")
        localizacao = geolocalizador.geocode(destino)
        if localizacao:
            return localizacao.latitude, localizacao.longitude
        else:
            return None

    # Função para obter a rota entre dois pontos usando a API do OpenStreetMap
    def obter_rota(ponto_inicial: dict, ponto_final: dict) -> str:
        """
        Essa função, a partir das coordenadas do ponto inicial e do ponto final, obtém uma rota que pode ser seguida com um carro.
        :param ponto_inicial: Dicionario de dois elementos que representam a latitude e a longitude do ponto inicial.
        :param ponto_final: Dicionario de dois elementos que representam a latitude e a longitude do ponto final.
        :return: Uma string representa a rota que o carro percorrerá.
        """
        url = f"http://router.project-osrm.org/route/v1/driving/{ponto_inicial[1]},{ponto_inicial[0]};{ponto_final[1]},{ponto_final[0]}"
        resposta = requests.get(url)
        dados = resposta.json()
        rota = dados['routes'][0]['geometry']
        return rota

    def salvar_mapa_como_png(mapa, nome_arquivo: str, largura: int = 650, altura: int = 350) -> None:
        """
        Essa função salva um print do mapa com as proporções de largura e altura desejadas
        :param mapa: Mapar de que será tirado a print
        :param nome_arquivo: Nome do arquivo em que a Print será salva
        :param largura: Largura da imagem
        :param altura: Altura da image
        :return: None
        """
        arquivo_temporario = f"{nome_arquivo}.html"
        mapa.save(arquivo_temporario)

        # Abre o arquivo temporario no navegador
        os.system(f"start {arquivo_temporario}")
        time.sleep(2)

        # Descobre dimensões da tela
        largura_tela, altura_tela = pyautogui.size()

        # Calcula as coordenadas do canto superior esquerdo do retângulo
        x_esquerda = (largura_tela - largura) // 2
        y_superior = (altura_tela - altura) // 2

        # Tira um screenshot da área desejada (com o centro do mapa no centro da tela)
        screenshot = pyautogui.screenshot(region=(x_esquerda, y_superior, largura, altura))
        screenshot.save(f"telas/{nome_arquivo}.png")

        # Remove o arquivo temporário HTML
        os.remove(arquivo_temporario)

    # -----------------------------------------------------------------------
    # Coordenadas dos pontos de partida e destino
    ponto_partida = [-23.5741147, -46.6231701]
    ponto_final = obter_coordenadas(destino)

    # Calcular o ponto médio entre o ponto de partida e o ponto de destino
    meio_trajeto = [(ponto_partida[0] + ponto_final[0]) / 2, (ponto_partida[1] + ponto_final[1]) / 2]

    rota = obter_rota(ponto_partida, ponto_final)
    rota_decodificada = polyline.decode(rota)

    # Calcular a distância entre os pontos de partida e destino
    distancia = geodesic(ponto_partida, ponto_final).kilometers

    # Determinar o nível de ‘zoom’ com base na distância
    # Você pode ajustar esses valores conforme a sua preferência
    if distancia < 1:
        nivel_zoom = 14
    elif distancia < 5:
        nivel_zoom = 13
    elif distancia < 10:
        nivel_zoom = 12
    else:
        nivel_zoom = 10.2

    # Criar um mapa
    mapa = folium.Map(location=meio_trajeto, zoom_start=nivel_zoom)
    folium.PolyLine(locations=rota_decodificada, color='red').add_to(mapa)

    # Adicionar marcadores para os pontos de partida e destino
    folium.Marker(ponto_partida, popup='Ponto de Partida', icon=folium.Icon(color='red')).add_to(mapa)
    folium.Marker(ponto_final, popup='Destino', icon=folium.Icon(color='black', icon='flag')).add_to(mapa)

    # Salvar o mapa como um arquivo PNG
    salvar_mapa_como_png(mapa, "mapa")


def ligacao(contato: str) -> None:
    """
    Edita a imagem 'ligação.png' para que o nome do contato esteja escrito na imagem
    :param contato: Nome do contato
    :return: None
    """
    # Carregua a imagem
    imagem = Image.open("telas_backup/ligação.png")

    # Cria um objeto ImageDraw
    desenho = ImageDraw.Draw(imagem)

    # Escreve a palavra na tela
    ponto = (273, 175)
    desenho.text(ponto, contato.capitalize(), fill="white", font_size=38)
    imagem.save("telas/ligação.png")


def informacoes_veiculo() -> None:
    """
    Exibe as informações do veículo
    :return: None
    """
    return "O veículo está em bom estado."
    
# Exemplo usando uma biblioteca de tradução, como `googletrans`.
def traduzir_para_portugues(texto: str) -> str:
    """
    Traduza o texto fornecido para o português usando a deep-translator.
    :param texto: Texto em qualquer idioma a ser traduzido.
    :return: Texto traduzido para o português.
    """
    try:
        traducao = GoogleTranslator(source='auto', target='pt').translate(texto)
        return traducao
    except Exception as e:
        return f"Erro ao traduzir o texto: {str(e)}"
 