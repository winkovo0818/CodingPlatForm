import json


def print_api_debug(title: str, res, expected_status=None):
    try:
        body = res.request.body.decode("utf-8") if res.request.body else ""
    except:
        body = str(res.request.body)

    print(f"\n" + "┌" + f"─[ {title} ]".center(60, "─") + "┐")
    print(f"│ 请求 URL     : {res.request.url}")
    print(f"│ 请求 Method  : {res.request.method}")
    print(f"│ 请求 Headers  : {res.request.headers}")
    print(f"│ 请求 Body    : {body}")

    if expected_status and res.status_code != expected_status:
        status_line = f"❌ {res.status_code}（期望: {expected_status}）"
    else:
        status_line = f"✅ {res.status_code}"

    print(f"│ 响应 Status  : {status_line}")
    print(f"│ 响应 Headers : {res.headers}")
    try:
        content = json.dumps(res.json(), ensure_ascii=False)
    except:
        content = res.text
    print(f"│ 响应内容     : {content}")
    print("└" + "─" * 60 + "┘\n")
