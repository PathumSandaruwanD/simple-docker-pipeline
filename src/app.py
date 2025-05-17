from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = None
    if request.method == 'POST':
        try:
            num1 = float(request.form['num1'])
            num2 = float(request.form['num2'])
            operation = request.form['operation']
            
            if operation == 'add':
                result = f"{num1} + {num2} = {num1 + num2}"
            elif operation == 'subtract':
                result = f"{num1} - {num2} = {num1 - num2}"
            elif operation == 'multiply':
                result = f"{num1} × {num2} = {num1 * num2}"
            elif operation == 'divide':
                result = f"{num1} ÷ {num2} = {num1 / num2}" if num2 != 0 else "Error: Division by zero"
                
        except ValueError:
            result = "Error: Please enter valid numbers"
        except Exception as e:
            result = f"Error: {str(e)}"
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)