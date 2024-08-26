from funcoes_carplay import *
import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyCIB3tPjLXhZmPh2BuPqdBY2bGMUm0z3BQ"
genai.configure(api_key=GOOGLE_API_KEY)

# Configuração do modelo
generation_config = {
    "temperature": 1,
    "max_output_tokens": 8192,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

# Função para definir a personalidade
def definir_personalidade(tipo_personalidade):
    if tipo_personalidade == "agressivo":
        return (
            "Haja de maneira direta e assertiva. Não seja muito educado, "
            "e mantenha suas respostas curtas e claras."
        )
    elif tipo_personalidade == "amigável":
        return (
            "Seja muito simpático e educado, use muitas palavras de carinho e "
            "encoraje o usuário sempre que possível."
        )
    elif tipo_personalidade == "mais maduro":
        return (
            "Adote um tom sério e formal, fornecendo informações detalhadas e "
            "mantendo uma postura mais reservada e tranquila."
        )
    elif tipo_personalidade == "mais criança":
        return (
            "Responda de maneira divertida e infantil, usando frases curtas, "
            "emoticons e um tom de voz animado."
        )
    elif tipo_personalidade == "passivo-agressivo":
        return (
            "Seja sutilmente sarcástico e irônico em suas respostas, "
            "mas ainda forneça as informações solicitadas."
        )
    else:
        return (
            "Haja de maneira neutra e profissional, fornecendo respostas claras "
            "e úteis sem demonstrar emoções específicas."
        )

# Perguntar ao usuário qual personalidade deseja
def escolher_personalidade():
    print("Escolha a personalidade do assistente:")
    print("1. Agressivo")
    print("2. Amigável")
    print("3. Mais maduro")
    print("4. Mais criança")
    print("5. Passivo-agressivo")
    
    escolha = input("Digite o número correspondente à personalidade desejada: ")
    
    if escolha == "1":
        return "agressivo"
    elif escolha == "2":
        return "amigável"
    elif escolha == "3":
        return "mais maduro"
    elif escolha == "4":
        return "mais criança"
    elif escolha == "5":
        return "passivo-agressivo"
    else:
        print("Escolha inválida, personalidade neutra selecionada.")
        return "neutro"

# Definir a personalidade escolhida
personalidade_escolhida = escolher_personalidade()
prompt_base = definir_personalidade(personalidade_escolhida)

# Prompt inicial baseado na personalidade escolhida
promt = (
    prompt_base +
    " Se o usuário digitar seu nome, responda apenas com 'Sim'. "
    "Exemplo ao pedir uma música: 'Toque [Nome da música]' ou 'Toque [Nome da música] da banda [Nome da banda]'. "
    "Exemplo ao pedir rota: 'Trace a rota para [Destino]' ou 'Leve-me para [Destino]', nesse caso responda 'Traçando rota para [Destino].' "
    "Exemplo ao pedir uma ligação: 'Ligue para [Nome da pessoa]', nesse caso responda 'Ligando para [Nome da pessoa]'. "
    "Exemplo ao pedir uma tradução: 'Traduza essa [Frase pedida] da ['Lingua pedida']' neste caso responda ' A frase traduzida ficaria [Frase traduzida para a lingua]"
    "Se você receber a palavra 'Oi', e apenas essa palavra, responda com 'Olá. Sou seu Copilot na viagem de hoje. Caso queira ouvir uma música, fazer uma ligação ou ver informações do veículo, é só me pedir.'"
)

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
    tools=[musica, encontrar_rota, ligacao, informacoes_veiculo]
)

chat = model.start_chat(enable_automatic_function_calling=True, history=[])

# Função para enviar mensagem e gerar resposta
def enviar_mensagem(mensagem: str) -> str:
    """
    Recebe o prompt falado pelo usuário e gera a resposta da IA.
    :param mensagem: Uma string que representa o prompt do usuário.
    :return: Uma string que representa a resposta da IA.
    """
    print(f"Mensagem enviada: {mensagem}")
    resposta = chat.send_message(mensagem)
    print(f"Resposta gerada: {resposta.text}")
    return resposta.text
