import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
import instaloader

application = Flask(__name__)
application.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this to a secure secret key

# Directory to store downloaded videos
DOWNLOADS_DIR = 'downloads'
if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)


def download_instagram_post(url):
    try:
        L = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(L.context, url.rsplit('/', 2)[-2])
        filename = f"{post.owner_username}{post.date_utc.strftime('%Y%m%d%H%M%S')}"
        session['user'] = filename
        print("Hii",filename,"bye")
        filepath = os.path.join(DOWNLOADS_DIR, filename)
        L.download_post(post, target=filepath)
        return filepath
    except Exception as e:
        return render_template('index.html')


@application.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            post_url = request.form['post_url']
            filepath = download_instagram_post(post_url)
            if filepath:
                flash(f"Downloaded video as {filepath}", 'success')
                return redirect(url_for('download_file', filename=filepath))
            else:
                flash("Failed to download video. Please check the URL.", 'danger')
        return render_template('index.html')
    except:
        return render_template('index.html')


@application.route('/download_file')
def download_file():
    username = session['user']
     # Replace with the path to your file

    file_names = os.listdir('downloads﹨'+username)
    file_names = [file_name for file_name in file_names if os.path.isfile(os.path.join('downloads﹨' + username, file_name))]
    file_path = 'downloads﹨' + username + '\\' + file_names[2]
    print(file_path)

    # Filter out directories (if needed)


    # Use send_file to send the file for download
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    application.run(debug=True)