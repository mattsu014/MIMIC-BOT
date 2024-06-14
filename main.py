import os
import speech_recognition as sr
import keyboard
import pyttsx3
import google.generativeai as genai

def reconhecer_fala(rec):
    with sr.Microphone() as mic:
        rec.adjust_for_ambient_noise(mic)
        print("Pressione 'r' para começar a escutar.")
        keyboard.wait('r')
        print("Escutando...")
        audio = rec.listen(mic)
        print("Parando a escuta...")
    try:
        return rec.recognize_google(audio, language="pt-BR")
    except sr.UnknownValueError:
        print("Não consegui entender o áudio")
    except sr.RequestError as e:
        print(f"Erro ao solicitar resultados do serviço de reconhecimento de fala: {e}")
    return None

def selecionar_voz(engine):
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 180)  # Velocidade da voz
    print("\nLista de Vozes - Verifique o número\n")
    for indice, voz in enumerate(voices):
        print(f"{indice}: {voz.name} ({voz.languages})")
    voz_indice = -1
    while not (0 <= voz_indice < len(voices)):
        try:
            voz_indice = int(input("Escolha o número da voz que deseja usar: "))
        except ValueError:
            print("Entrada inválida, por favor insira um número.")
    engine.setProperty('voice', voices[voz_indice].id)

def falar_resposta(engine, texto):
    engine.say(texto)
    engine.runAndWait()

def main():
    rec = sr.Recognizer()
    engine = pyttsx3.init()
    selecionar_voz(engine)

    caminho_arquivo_chave = os.path.join(os.path.dirname(__file__), "API_key.txt")
    os.environ['GOOGLE_API_KEY'] = open(caminho_arquivo_chave, 'r').read().strip()
    genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
    model = genai.GenerativeModel('gemini-pro')

    print("Digite o nome do personagem e a sua origem, por exemplo, Sasuke (Naruto)\n")
    personagem = input().strip()
    print("\n")
    historico = []

    while True:
        pergunta = reconhecer_fala(rec)
        if pergunta:
            print(f"Você disse: {pergunta}")
        else:
            continue
        if pergunta.lower() in ['sair', 'exit', 'quit']:
            print("Encerrando o programa.")
            break
        historico.append(f"Usuário: {pergunta}")
        contexto = "\n".join(historico)

        atuacao = f"Responda (em 1 paragrafo) como se fosse o {personagem}:\n{contexto}\n{personagem}: "
        response = model.generate_content(atuacao)
        resposta_texto = response.text.strip()
        historico.append(f"{personagem}: {resposta_texto}")

        print(resposta_texto)
        falar_resposta(engine, resposta_texto)
        print("\n")

if __name__ == "__main__":
    main()