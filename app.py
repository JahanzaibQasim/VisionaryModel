from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Ensure this matches your actual template name

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/service-details')
def service_details():
    return render_template('service-details.html')

# Add more routes as needed
if __name__ == '__main__':
    app.run(debug=True)
