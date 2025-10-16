import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0',
    # cookie 需要每次替换为最新的
    'Cookie': "_tea_utm_cache_2608={%22utm_source%22:%22infinitynewtab.com%22}; s_v_web_id=verify_mex1lzhx_9708ROtC_m7DX_4MzZ_9A3S_oUH2lGev9Hbj; __tea_cookie_tokens_2608=%257B%2522web_id%2522%253A%25227544044080973465115%2522%252C%2522user_unique_id%2522%253A%25227544044080973465115%2522%252C%2522timestamp%2522%253A1756484652099%257D; _tea_utm_cache_2018={%22utm_source%22:%22infinitynewtab.com%22}; passport_csrf_token=e28a05c08242a03e00224bd8ea33e591; passport_csrf_token_default=e28a05c08242a03e00224bd8ea33e591; n_mh=NRfqMAJbemDr4WPjDFXqEYZO1C7tJ2T3hcnnfQVplPk; is_staff_user=false; sid_guard=8e27ecb702b03a23c0b8e873e9c64ce9%7C1760616195%7C31536000%7CFri%2C+16-Oct-2026+12%3A03%3A15+GMT; uid_tt=da6ff3d3a68b3b194282a9d86a629b71; uid_tt_ss=da6ff3d3a68b3b194282a9d86a629b71; sid_tt=8e27ecb702b03a23c0b8e873e9c64ce9; sessionid=8e27ecb702b03a23c0b8e873e9c64ce9; sessionid_ss=8e27ecb702b03a23c0b8e873e9c64ce9; session_tlb_tag=sttt%7C17%7CjifstwKwOiPAuOhz6cZM6f_________2_ofVN-loKvOpjp2Y-ZMfQnbY9ny3grZ0lah_LeyatPs%3D; sid_ucp_v1=1.0.0-KDdjOGU5NzFhZGI4NTljYjdlNGQ1OTYwNjU5ODFlYTU1NDY4ZWU2NjMKFwipoZCT9MzeARCDvsPHBhiwFDgCQO8HGgJscSIgOGUyN2VjYjcwMmIwM2EyM2MwYjhlODczZTljNjRjZTk; ssid_ucp_v1=1.0.0-KDdjOGU5NzFhZGI4NTljYjdlNGQ1OTYwNjU5ODFlYTU1NDY4ZWU2NjMKFwipoZCT9MzeARCDvsPHBhiwFDgCQO8HGgJscSIgOGUyN2VjYjcwMmIwM2EyM2MwYjhlODczZTljNjRjZTk"
    }
session = requests.Session()
response = session.get('https://juejin.cn/', headers=headers)
print(response.text)
