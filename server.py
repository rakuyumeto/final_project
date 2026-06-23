"""
Web server for emotion detection using Flask.
Provides a simple web endpoint that returns emotion scores.
"""

from typing import Dict, Any, Optional

from flask import Flask, render_template, request  # pylint: disable=import-error

# Import from package — when running from repo root use: from final_project import emotion_detector
from final_project.emotion_detection import emotion_detector  # type: ignore

app = Flask(__name__)


@app.route("/")
def render_index_page() -> str:
    """Render the main index page with the input form."""
    return render_template("index.html")


@app.route("/emotionDetector")
def sent_analyzer() -> str:
    """Analyze text from the query string and return emotion scores."""
    text_to_analyze: Optional[str] = request.args.get("textToAnalyze")

    if not text_to_analyze:
        return "Invalid text! Please provide a non-empty textToAnalyze parameter."

    response: Dict[str, Any] = emotion_detector(text_to_analyze)

    # If the emotion detector could not process the text, return a friendly message.
    if response.get("dominant_emotion") is None:
        return "Invalid text! Please try again!"

    return (
        f"For the given statement, the system response is "
        f"'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, "
        f"'joy': {response['joy']}, "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )


if __name__ == "__main__":
    # Bind to localhost; in production use a WSGI server.
    app.run(host="127.0.0.1", port=5000)
