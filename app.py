from flask import Flask, render_template, request
from duckduckgo_search import ddg

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        query = request.form.get('search')
        if query:
            # Get first 3 results from DuckDuckGo
            results = ddg(query, max_results=3)
    
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True) 