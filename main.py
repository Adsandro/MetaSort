import os
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
import shutil
from datetime import datetime
from pymediainfo import MediaInfo

# Função para extrair a data da foto a partir dos metadados
def extrair_data_foto(caminho_foto):
    try:
        image = Image.open(caminho_foto)
        exif_data = image._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                if TAGS.get(tag) == 'DateTimeOriginal':
                    # Converte a data para o formato YYYY-MM-DD
                    data_str = value.split(" ")[0].replace(":", "-")
                    return data_str
    except Exception as e:
        print(f"Erro ao extrair data de {caminho_foto}: {e}")
    return None

def extrair_data_video(caminho_video):
        video = MediaInfo.parse(caminho_video)
        for track in video.tracks:
            if track.track_type == 'General':

                encoded = str(track.encoded_date)[:10].split(" ")[0].replace(":", "-")
                targget = str(track.targget_date)[:10].split(" ")[0].replace(":", "-")
                return encoded or targget

def main(pasta_principal, pasta_destino):
    Path(pasta_destino).mkdir(parents=True, exist_ok=True)

    # Extensões de arquivos que queremos processar (fotos)
    extensoes_fotos = ['.jpg', '.jpeg', '.png', '.heic']
    extensoes_videos = ['.mp4']

    # Percorrer todas as subpastas e arquivos
    for root, dirs, files in os.walk(pasta_principal):
        for arquivo in files:
            # Verifica se o arquivo é uma foto
            if any(arquivo.lower().endswith(ext) for ext in extensoes_fotos):
                caminho_arquivo = os.path.join(root, arquivo)
                # if extensoes_videos:
                #     data_foto = extrair_data_video(caminho_arquivo)
                #     print('video')

                if extensoes_fotos:
                # Extrair a data da foto
                    data_foto = extrair_data_foto(caminho_arquivo)
                

                if data_foto:
                    # Cria o diretório de destino baseado na data da foto
                    pasta_data = os.path.join(pasta_destino, data_foto)
                    Path(pasta_data).mkdir(parents=True, exist_ok=True)
                    
                    # Move a foto para o diretório da data correspondente
                    shutil.move(caminho_arquivo, os.path.join(pasta_data, arquivo))
                    print(f"Movido: {caminho_arquivo} -> {os.path.join(pasta_data, arquivo)}")
                else:
                    contador +=1
                    print(f"Data não encontrada para: {caminho_arquivo}")