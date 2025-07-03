from common.request_handler import RequestHandler


class ArticleAPI:
    def __init__(self, base_url, token=None):
        default_headers = {"Authorization": f"{token}"} if token else {}
        self.client = RequestHandler(base_url, default_headers)

    def get_article_list(self, data):
        return self.client.request("post", "/article/list", json=data)

    def get_article_detail(self, articleId):
        return self.client.request("get", f"/article/detail/{articleId}")
