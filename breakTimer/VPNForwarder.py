from mitmproxy import http
from mitmproxy import ctx
from threading import Timer
import json

fix_domains = ['madou.club', 'e-hentai.org', 'exhentai.org']
stream_domans = ['liaobots']


class VPNForwarder:
    def __init__(self):
        self.update_()
    def request(self, flow):
        ctx.log.info(f'{ctx}')
        response_body = "滚去学习".encode('utf-8')  # 使用 utf-8 编码
        if any(domain in flow.request.pretty_host for domain in self.filtered_domains):
            ctx.log.info(f'成功阻止网站:{self.filtered_domains}')
            flow.response = http.Response.make(
                403,  # 状态码
                #b"forbidden, go to study, be a person",  # 响应体
                response_body,
                {"Content-Type": "text/html; charset=utf-8"}  # 头部
            )
        # if any(domain in flow.request.pretty_host for domain in stream_domans):
        #     flow.request.stream = True
        #     ctx.log.info(f"启用流式代理: {flow.request.pretty_host}")
        # 其他请求会自动通过上游代理，无需在这里指定
    def update_(self, *args, **kwargs):
        try:
            with open('temp.txt', 'r') as file:
                filtered_domains = json.load(file)
            self.filtered_domains = list(set(filtered_domains + fix_domains))
        except Exception as e:
            print(e)
            self.filtered_domains = []
        Timer(30, self.update_).start()

addons = [
    VPNForwarder()
]