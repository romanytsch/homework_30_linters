import requests

URL = "http://127.0.0.1:5000/api"


def call(method: str, **params):
    """Универсальный вызов JSON‑RPC метода."""
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1,
    }
    resp = requests.post(URL, json=data)
    result = resp.json()
    if "error" in result:
        raise Exception(f"JSON‑RPC error: {result['error']}")
    return result["result"]


if __name__ == "__main__":
    print(call("calc.add", a=7.8, b=5.3))        # 13.1
    print(call("calc.subtract", a=10.0, b=3.5))  # 6.5
    print(call("calc.multiply", a=4.2, b=3.0))   # 12.6
    print(call("calc.divide", a=10.0, b=2.0))    # 5.0
