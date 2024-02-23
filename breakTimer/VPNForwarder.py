from mitmproxy import http
from mitmproxy import ctx
import json

fix_domains = ['madou.club', 'e-hentai.org', 'exhentai.org']

class VPNForwarder:

    def request(self, flow):
        with open('temp.txt', 'r') as file:
            filtered_domains = json.load(file)
        filtered_domains = list(set(filtered_domains + fix_domains))

        ctx.log.info(f'{ctx}')
        # ctx.log.info(f'当前阻止网站: {filtered_domains}')
        # 对特定域名请求不进行转发
        response_body = "滚去学习".encode('utf-8')  # 使用 utf-8 编码
        if any(domain in flow.request.pretty_host for domain in filtered_domains):
            ctx.log.info(f'成功阻止网站:{filtered_domains}')

            flow.response = http.Response.make(
                403,  # 状态码
                #b"forbidden, go to study, be a person",  # 响应体
                response_body,
                {"Content-Type": "text/html; charset=utf-8"}  # 头部
            )
        # 其他请求会自动通过上游代理，无需在这里指定

addons = [
    VPNForwarder()
]