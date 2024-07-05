from flask import Flask, render_template, make_response, request, session, jsonify

from video import Video

app = Flask(__name__, template_folder="view", static_folder="static")


@app.route("/")
def main_index():
    return render_template("video.html")


@app.route("/get-video", methods=["POST"])
def get_video():
    title = request.form.get("title")
    target_url = f"https://www.google.com/search?q={title}&tbm=vid"
    html = Video().extract_text_from_xpath(Video().get_html_from_url(target_url))
    return jsonify({"html": html})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
