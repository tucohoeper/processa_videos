import os
import subprocess

def create_output_directory(path):
    """Cria o diretório de saída se ele não existir."""
    output_dir = os.path.join(path, "output")
    if not os.path.exists(output_dir):
        print(f"Criando diretório de saída em: {output_dir}")
        os.makedirs(output_dir)
    return output_dir

def process_videos_in_folder(folder_path):
    """
    Encontra todos os vídeos .mp4 em uma pasta e insere a imagem .png de mesmo nome
    nos primeiros 5 quadros de cada vídeo usando ffmpeg.
    """
    if not os.path.isdir(folder_path):
        print(f"Erro: O caminho '{folder_path}' não é um diretório válido.")
        return

    output_dir = create_output_directory(folder_path)
    
    files_in_folder = os.listdir(folder_path)
    video_files = [f for f in files_in_folder if f.lower().endswith(".mp4")]

    if not video_files:
        print("Nenhum arquivo de vídeo .mp4 encontrado no diretório.")
        return

    print(f"Encontrados {len(video_files)} arquivos de vídeo. Iniciando o processo...")

    for video_file in video_files:
        base_name, _ = os.path.splitext(video_file)
        image_file = f"{base_name}.png"
        
        video_path = os.path.join(folder_path, video_file)
        image_path = os.path.join(folder_path, image_file)
        output_path = os.path.join(output_dir, f"{base_name}_modified.mp4")

        if os.path.exists(image_path):
            print(f"Processando '{video_file}' com a imagem '{image_file}'...")

            try:
                # 1. Obter as dimensões do vídeo com ffprobe
                ffprobe_command = [
                    "ffprobe",
                    "-v", "error",
                    "-select_streams", "v:0",
                    "-show_entries", "stream=width,height",
                    "-of", "csv=s=x:p=0",
                    video_path,
                ]
                probe_result = subprocess.run(ffprobe_command, check=True, capture_output=True, text=True)
                video_width, video_height = probe_result.stdout.strip().split('x')

                # 2. Construir e executar o comando ffmpeg
                #   - [1:v]scale=...[scaled_img]: Pega a imagem e a redimensiona para caber no vídeo
                #     mantendo a proporção (force_original_aspect_ratio=decrease).
                #   - [0:v][scaled_img]overlay=...: Pega o vídeo principal e sobrepõe a imagem redimensionada.
                #   - x=(main_w-overlay_w)/2:y=(main_h-overlay_h)/2 : Centraliza a imagem na tela.
                #   - enable='lte(n,4)': Ativa a sobreposição apenas para os 5 primeiros quadros.
                filter_str = (
                    f"[1:v]scale={video_width}:{video_height}:force_original_aspect_ratio=decrease[scaled_img];"
                    f"[0:v][scaled_img]overlay=x=(main_w-overlay_w)/2:y=(main_h-overlay_h)/2:enable='lte(n,4)'"
                )
                
                command = [
                    "ffmpeg",
                    "-i", video_path,
                    "-i", image_path,
                    "-filter_complex", filter_str,
                    "-map", "0:a?",
                    "-c:a", "copy",
                    "-y", # Sobrescreve o arquivo de saída se ele já existir
                    output_path,
                ]
                
                result = subprocess.run(command, check=True, capture_output=True, text=True)
                print(f"SUCESSO: Vídeo '{output_path}' gerado.")

            except subprocess.CalledProcessError as e:
                print(f"ERRO ao processar '{video_file}':")
                # Se o erro for do ffprobe, e.stderr pode não estar populado da mesma forma
                error_output = e.stderr or e.stdout
                print(f"Output do comando: {error_output}")
            except FileNotFoundError:
                print("ERRO: ffmpeg ou ffprobe não encontrado. Verifique se eles estão instalados e no PATH do seu sistema.")
                return # Interrompe o script se o ffmpeg/ffprobe não for encontrado
            except Exception as e:
                print(f"Um erro inesperado ocorreu ao processar '{video_file}': {e}")

        else:
            print(f"AVISO: Imagem '{image_file}' não encontrada para o vídeo '{video_file}'. Pulando.")

    print("\nProcesso concluído.")

if __name__ == "__main__":
    target_folder = input("Por favor, arraste ou cole o caminho da pasta com seus vídeos e imagens e pressione Enter: ").strip()
    # Remove aspas que podem ser adicionadas ao arrastar e soltar pastas em alguns terminais
    if target_folder.startswith("'") and target_folder.endswith("'"):
        target_folder = target_folder[1:-1]
        
    process_videos_in_folder(target_folder)
