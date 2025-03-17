import os
import speech_recognition as sr
import pygame
import argparse
import threading
from deep_translator import GoogleTranslator

global args
parser = argparse.ArgumentParser(description='PNGtuber configuration')
parser.add_argument('--translate', type=str, default='es', help='Translate to language (e.g., en for English)')
args = parser.parse_args()


# Inicializar pygame para la reproducción de audio y la ventana de subtítulos
pygame.init()
pygame.mixer.init()

# Configuración de la ventana para subtítulos
WIDTH, HEIGHT = 1200, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Subtítulos")
font = pygame.font.Font(None, 48)
clock = pygame.time.Clock()

def listen_to_voice_async(result_container):
    """Captura el audio del micrófono y lo convierte en texto en un hilo separado"""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("*Se queda escuchando*")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language='en-EN')
        os.system("cls")
        print(f"Has dicho: {text}")
        result_container["text"] = text
    except sr.UnknownValueError:
        print("*No lo entiende*")
    except sr.RequestError as e:
        print(f"Error al solicitar resultados de reconocimiento; {e}")
    result_container["done"] = True
    
def translate_text(text, target_language):
    try:
        return GoogleTranslator(source='auto', target=target_language).translate(text)
    except Exception as e:
        print(f"Error en la traducción: {e}")
        return "[Error en traducción]"

def display_subtitles(text):
    """Muestra los subtítulos en la pantalla"""
    if args.translate:
        text = translate_text(text, args.translate)
        print(f"Traducción: {text}")
    screen.fill((0, 0, 0))  # Fondo negro
    subtitle_text = font.render(text, True, (255, 255, 255))
    text_rect = subtitle_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(subtitle_text, text_rect)
    pygame.display.flip()

def clean_text():
    print("Limpiando texto...")

if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        # Escuchar en un hilo separado
        result = {"text": "", "done": False}
        listener_thread = threading.Thread(target=listen_to_voice_async, args=(result,))
        listener_thread.start()
        
        while not result["done"]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            clock.tick(30)
        
        message = result["text"]
        if message.lower() == "salir":
            break
        display_subtitles(message)
    
    pygame.quit()
