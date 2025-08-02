from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_choice = request.form['format']
    filename = str(uuid.uuid4())

    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/{filename}.%(ext)s',
    }

    if format_choice == 'mp3':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'merge_output_format': 'mp4'
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    file_ext = 'mp3' if format_choice == 'mp3' else 'mp4'
    filepath = f"{DOWNLOAD_FOLDER}/{filename}.{file_ext}"
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
