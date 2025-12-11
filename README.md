# Processador de Vídeos com FFmpeg

Este script Python automatiza o processo de sobreposição de uma imagem estática no início de múltiplos vídeos usando o FFmpeg. Ele foi projetado para ser simples, eficiente e fácil de usar.

## Funcionalidades

- **Processamento em Lote:** Percorre uma pasta e processa todos os vídeos com a extensão `.mp4`.
- **Correspondência Automática:** Para cada vídeo (ex: `meu_video.mp4`), o script procura por uma imagem com o mesmo nome base (ex: `meu_video.png`).
- **Sobreposição Inteligente:** Insere a imagem correspondente nos primeiros 5 quadros de cada vídeo.
- **Redimensionamento Automático:** A imagem é redimensionada para se ajustar às dimensões do vídeo, mantendo sua proporção original, e é centralizada na tela.
- **Saída Organizada:** Os vídeos processados são salvos em um subdiretório chamado `output`, mantendo a pasta original limpa.
- **Tratamento de Erros:** O script verifica se o `ffmpeg` e o `ffprobe` estão instalados e fornece feedback claro sobre arquivos ausentes ou erros durante o processamento.

## Requisitos

- **Python 3.x**
- **FFmpeg:** É necessário que o `ffmpeg` e o `ffprobe` estejam instalados e acessíveis no PATH do sistema. Você pode baixá-los no [site oficial do FFmpeg](https://ffmpeg.org/download.html).

## Como Usar

1.  **Prepare seus arquivos:**
    - Coloque todos os seus vídeos `.mp4` em uma única pasta.
    - Para cada vídeo, adicione a imagem `.png` que você deseja sobrepor na mesma pasta. A imagem deve ter o mesmo nome do vídeo.
    - Exemplo de estrutura de pasta:
      ```
      /minha_pasta/
      ├─── video1.mp4
      ├─── video1.png
      ├─── video2.mp4
      ├─── video2.png
      └─── outro_video.mp4  (Este será ignorado se 'outro_video.png' não existir)
      ```

2.  **Execute o script:**
    - Abra um terminal ou prompt de comando.
    - Navegue até o diretório onde o script `process_videos.py` está localizado.
    - Execute o seguinte comando:
      ```bash
      python process_videos.py
      ```

3.  **Forneça o caminho:**
    - O script solicitará que você forneça o caminho para a pasta que contém seus vídeos e imagens. Você pode arrastar e soltar a pasta no terminal ou colar o caminho manualmente e pressionar Enter.

4.  **Aguarde o processamento:**
    - O script irá processar cada vídeo e exibir o progresso no terminal.

5.  **Verifique a saída:**
    - Após a conclusão, uma nova pasta chamada `output` será criada dentro do diretório que você forneceu. Dentro dela, você encontrará os vídeos modificados (ex: `video1_modified.mp4`).

## Como Funciona

O script utiliza o `ffprobe` para obter as dimensões de cada vídeo e, em seguida, constrói um comando `ffmpeg` complexo para realizar a sobreposição. A lógica principal do `ffmpeg` é:

- `-filter_complex`: Permite o uso de múltiplos filtros.
- `[1:v]scale=...[scaled_img]`: Redimensiona a imagem de entrada (`[1:v]`) para caber no vídeo, mantendo a proporção.
- `[0:v][scaled_img]overlay=...`: Sobrepõe a imagem redimensionada (`[scaled_img]`) sobre o vídeo principal (`[0:v]`).
- `enable='lte(n,4)'`: Ativa a sobreposição apenas para os quadros de 0 a 4 (os primeiros 5 quadros).
- `-map 0:a? -c:a copy`: Mapeia e copia o áudio do vídeo original para o vídeo de saída sem re-codificação.
