from flask import Flask, render_template, request, jsonify
import requests
import yt_dlp

app = Flask(__name__)

def get_tiktok_video(url):
    # Usando a mesma lógica do seu bot com a TikWM
    api_url = f"https://www.tikwm.com/api/?url={url}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(api_url, headers=headers).json()
    if res.get('code') == 0:
        return res['data'].get('play')
    return None

def get_ytdlp_video(url):
    ydl_opts = {'format': 'best', 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info['url']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/baixar', methods=['POST'])
def baixar():
    url = request.form.get('url')
    if not url:
        return jsonify({'erro': 'Manda o link, doido!'})

    try:
        if 'tiktok.com' in url:
            video_link = get_tiktok_video(url)
            if not video_link:
                video_link = get_ytdlp_video(url) # fallback
        else:
            video_link = get_ytdlp_video(url)
            
        return jsonify({'sucesso': True, 'link': video_link})
    except Exception as e:
        return jsonify({'erro': str(e)})

if __name__ == '__main__':
    # O Gunicorn vai rodar isso na Discloud, mas pra testar no PC usa a porta 8080
    app.run(host='0.0.0.0', port=8080)
