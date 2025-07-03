from common.yaml_util import read_yaml


def load_test_data(path, key):
    data = read_yaml(path)
    return [(case["title"], case.get("request_data", case.get("data")), case.get("validators", [{"code": case.get("expected_code"), "status": case.get("expected_status")}])) for case in data[key]]
