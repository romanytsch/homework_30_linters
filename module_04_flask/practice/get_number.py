from flask import Flask, request, abort

app = Flask(__name__)

@app.route("/number", methods=["GET"])
def number():
    number_str = request.args.getlist("number")

    if not number_str:
        abort(400, "Значение number обязательное!")

    try:
        numbers = [float(num) for num in number_str]
    except ValueError:
        abort(400, description="Значение number должно быть числом!")

    total_sum = sum(numbers)
    product = 1

    for num in numbers:
        product *= num

    return f'Сумма чисел = {total_sum}, произведение чисел = {product}'

if __name__ == "__main__":
    app.run(debug=True)