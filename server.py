from flask import Flask
from flask import request
import openai
openai.api_key="YOUR API KEY HERE"
app = Flask(__name__)

def predict(query):
    ft_model ="YOUR MODEL"#EXAMPLE ada:ft-personal-2022-06-02-09-26-26
    res = openai.Completion.create(model=ft_model, prompt= query, max_tokens=1, temperature=0)
    return res.choices[0].text

@app.route('/query', methods=['GET', 'POST'])
def index():
    #read paramerters from the url
    query = request.args.get('query')
    #call the function to get the response
    response = predict(query)
    return response
    
if __name__ == '__main__':
    app.run(debug=True)