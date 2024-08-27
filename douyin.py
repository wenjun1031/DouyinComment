import os
from time import sleep

import requests
import subprocess
from functools import partial
from tqdm import tqdm
subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')  #这三行代码需要放在导入execjs之前

import execjs
import urllib.parse

import execjs._runner_sources as _runner_sources

# 创建 JavaScript 运行时 对象
# 参数中的 command 并不重要，传入空字符串即可
local_node_runtime = execjs.ExternalRuntime(
    name="Node.js (V8) local",
    command='',
    encoding='UTF-8',
    runner_source=_runner_sources.Node
)
# 这里是重点，需要强制性修改
local_node_runtime._binary_cache = ['./nodejs/node.exe']
local_node_runtime._available = True
# 将刚创建好的 JavaScript 运行时 注册至 PyExecJS 中
execjs.register('local_node', local_node_runtime)

# print("execjs", execjs.get('local_node').name)

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
    'cache-control': 'no-cache',
    'cookie': 'dy_swidth=1829; dy_sheight=1143; csrf_session_id=ff341765530bc6404a43a79750bcd947; fpk1=U2FsdGVkX19nv6LdqzUt0VaBjPqe6f+KaDjEg4Iso/Qjb0M7BNx3b2Xmf5HUzRPIlG6Ii6VJ2cmKsztb7xqnTA==; fpk2=a565ccc5e7018c4ec7bec64e38db2966; s_v_web_id=verify_m0az5ous_761ae85e_c264_ab83_0cb5_4f31afff748c; passport_mfa_token=CjczM3JZvGT3SZgHQ4Xwd%2F8S0dC8gwUU0XlpMG20apXsptceY2%2Fs92jINkzCa9rERNjIwWltxT2KGkoKPCbZ5jfh0fH%2B%2BIQ4rwNMElVlnVeuPVNeNFHbIypd%2FxWCQNeOvi93XbQvllY33DqGSxVbb%2FP8ExXriKR9QRDuttoNGPax0WwgAiIBA0XXrZA%3D; __ac_nonce=066cc7ca2003bbb0f853e; __ac_signature=_02B4Z6wo00f01Dpee3AAAIDADXq.LU3r4bA6fn.AAGhiea; xgplayer_device_id=34264322324; xgplayer_user_id=502971258475; device_web_cpu_core=16; device_web_memory_size=8; architecture=amd64; passport_csrf_token=77e72cf4821866bd988e813c1d085b03; passport_csrf_token_default=77e72cf4821866bd988e813c1d085b03; ttwid=1%7Ck_0pzwbcfrSJbJwaPyDK5xKIv56VG3oL8c4lxlQvN_s%7C1724677703%7C38d40b9f5b7df247a7e6250bd30e40b98ceaf808e3b73bd25a38454a429d3fed; UIFID=c3109cf8eab4507640f022360c5ce002c7035d0857c7085fdeb180d1661fca19a5d3d6d13f5ca07e950fb768e18a0d6986d56271a7b9bbc8bdf6513d5cebda69a5d7c6d05ba08b5842ee58a5567f4913db6bfe9e5949ba2ece38995012ece1e1b41743307bf8d6c3cbe31baba027ca12d61416abb2f33b945b8c80aebc41efefea8abd6d2c2dc7538a115e70d24dd0c82114f559c7a970f8dbebb696b77701c4b31330ce299006fa16be8822f1fe0cdde01b485f064254e91da057572b6ef6ab; douyin.com; hevc_supported=true; strategyABtestKey=%221724677703.085%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.5%7D; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; bd_ticket_guard_client_web_domain=2; biz_trace_id=c3b8ca85; passport_assist_user=Cjx1Dt7DZJCvqwLUOvjiTJiaSZPJVRtDU8zi8rXC_mf0gVZeOAfS3F7mi5iCUZH_LcuZOKmsK4J_6nAB72kaSgo8rirj-Ccbk17k5kEK0d05N6ExU08mKxfL_FblCEr5mxuLH4IFk4eXtau22L2_dL4yqtKB930dYBPQCEGDEJe12g0Yia_WVCABIgEDDVAMmw%3D%3D; n_mh=XNuAU-Vt8SXxc6tpKVaVKpXnXVZvz8Bo2tmZfOJMJL8; sso_uid_tt=acba70d9b530776f1255e98be9e16675; sso_uid_tt_ss=acba70d9b530776f1255e98be9e16675; toutiao_sso_user=ca998ac3fe68d613a2e67364e69dc67a; toutiao_sso_user_ss=ca998ac3fe68d613a2e67364e69dc67a; sid_ucp_sso_v1=1.0.0-KGRkYWVlYmY4MDJjZDgxMjhiZWU5MmI4MDBlOTc3NGNlMGFhN2VhZmIKHwjHhorE6wEQ2_yxtgYY7zEgDDCMuYjLBTgGQPQHSAYaAmhsIiBjYTk5OGFjM2ZlNjhkNjEzYTJlNjczNjRlNjlkYzY3YQ; ssid_ucp_sso_v1=1.0.0-KGRkYWVlYmY4MDJjZDgxMjhiZWU5MmI4MDBlOTc3NGNlMGFhN2VhZmIKHwjHhorE6wEQ2_yxtgYY7zEgDDCMuYjLBTgGQPQHSAYaAmhsIiBjYTk5OGFjM2ZlNjhkNjEzYTJlNjczNjRlNjlkYzY3YQ; passport_auth_status=d5416b021544275a26f2b9e5ac2e3027%2C; passport_auth_status_ss=d5416b021544275a26f2b9e5ac2e3027%2C; uid_tt=daa87580fb859c7bc23dd21944768ad7; uid_tt_ss=daa87580fb859c7bc23dd21944768ad7; sid_tt=17aaa0c1bd9bc8f4f6e6ca57b67a142a; sessionid=17aaa0c1bd9bc8f4f6e6ca57b67a142a; sessionid_ss=17aaa0c1bd9bc8f4f6e6ca57b67a142a; is_staff_user=false; publish_badge_show_info=%220%2C0%2C0%2C1724677728918%22; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=731d51b1e0b54a677a98d5a202ce61ea; __security_server_data_status=1; sid_guard=17aaa0c1bd9bc8f4f6e6ca57b67a142a%7C1724677733%7C5183992%7CFri%2C+25-Oct-2024+13%3A08%3A45+GMT; sid_ucp_v1=1.0.0-KGM2ZTE2ZThjODVhODMxOTQxM2NhODdhZTRiZDBiZDk4OTU3ZWNkMWQKGQjHhorE6wEQ5fyxtgYY7zEgDDgGQPQHSAQaAmxmIiAxN2FhYTBjMWJkOWJjOGY0ZjZlNmNhNTdiNjdhMTQyYQ; ssid_ucp_v1=1.0.0-KGM2ZTE2ZThjODVhODMxOTQxM2NhODdhZTRiZDBiZDk4OTU3ZWNkMWQKGQjHhorE6wEQ5fyxtgYY7zEgDDgGQPQHSAQaAmxmIiAxN2FhYTBjMWJkOWJjOGY0ZjZlNmNhNTdiNjdhMTQyYQ; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAA9tMte4MUQsxe2VSUAR5WoQtPnPWAfXdaHHkctN7YJFA%2F1724688000000%2F0%2F0%2F1724678822877%22; xg_device_score=7.90435294117647; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1829%2C%5C%22screen_height%5C%22%3A1143%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A16%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAA9tMte4MUQsxe2VSUAR5WoQtPnPWAfXdaHHkctN7YJFA%2F1724688000000%2F0%2F1724678339647%2F0%22; IsDouyinActive=true; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A1%7D%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCQUVkaU4wVm5YNmlWYWZPbkg0ZmZmSlp0RkV0K2cwZmtDemJ1c2k4ODJwaHJ5QU9XK0RJVXA1b2tNWWJpQXFuSXB0bEhhVE0rRVg5cURqaytnN0lOSkk9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; passport_fe_beating_status=true; home_can_add_dy_2_desktop=%221%22; odin_tt=27a083083020c110414288988d9e8bfb4f7bf9d8ec03f3706662670a199bdd04651d9cdab247847dd135060d30766b24',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.douyin.com/user/MS4wLjABAAAAcdLig2KyRygH2j4SHpzwahXj7Cin6PDnFhOU4HwIHVx7UU65LAeOfQO267BxUdAZ',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}

params = {
    'device_platform': 'webapp',
    'aid': '6383',
    'channel': 'channel_pc_web',
    'item_type': '0',
    'locate_query': 'false',
    'show_live_replay_strategy': '1',
    'need_time_list': '1',
    'time_list_query': '0',
    'whale_cut_token': '',
    'cut_version': '1',
    'publish_video_strategy_type': '2',
    'update_version_code': '170400',
    'pc_client_type': '1',
    'version_code': '290100',
    'version_name': '29.1.0',
    'cookie_enabled': 'true',
    'screen_width': '1847',
    'screen_height': '1039',
    'browser_language': 'zh-CN',
    'browser_platform': 'Win32',
    'browser_name': 'Chrome',
    'browser_version': '125.0.0.0',
    'browser_online': 'true',
    'engine_name': 'Blink',
    'engine_version': '125.0.0.0',
    'os_name': 'Windows',
    'os_version': '10',
    'cpu_core_num': '8',
    'device_memory': '8',
    'platform': 'PC',
    'downlink': '10',
    'effective_type': '4g',
    'round_trip_time': '100',
    'webid': '7373962654656054793',
    'msToken': '_oAmCBg7EMDOt3T-1POfW1n6--0o-ASOEdZTCHgmLXSXk0HXBgM6rhfeUL7gQJFKgYt65DHDHpMzBx7IXRNj8sROdxFESJVCc_jDEcVIG1Pje7cJv29tel5uzx5GgFM=',
    'verifyFp': 'verify_lwq4p1rd_x9KHBYiK_SAe5_4qyC_B58o_crG0hp49CNTn',
    'fp': 'verify_lwq4p1rd_x9KHBYiK_SAe5_4qyC_B58o_crG0hp49CNTn',
}


def get_douyin_comment(aweme_id, cursor="0", count="20"):
    with open('cookie.txt', 'r') as f:
        headers['cookie'] = f.read()
    _params = params.copy()
    _params['aweme_id'] = aweme_id
    _params['cursor'] = cursor
    _params['count'] = count
    params_str = urllib.parse.urlencode(_params)
    a_bogus = execjs.get('local_node').compile(open('douyin.js').read()).call('get_a_bogus', params_str)
    _params['a_bogus'] = a_bogus
    response = requests.get('https://www.douyin.com/aweme/v1/web/comment/list/', params=_params, headers=headers)
    sleep(10)
    return response.json()


def get_douyin_all_comment(aweme_id):
    cursor = 0
    all_comments = []
    has_more = 1
    with tqdm(desc="Fetching comments", unit="comment") as pbar:
        while has_more:
            try:
                response = get_douyin_comment(aweme_id, cursor=str(cursor))
                comments = response.get("comments", [])
                if isinstance(comments, list):
                    all_comments.extend(comments)
                    pbar.update(len(comments))
                has_more = response.get("has_more", 0)
                if has_more:
                    cursor = response.get("cursor", 0)
            except Exception as e:
                print(f"Failed to fetch comments, error: {e}")
                cursor += 20
                continue
    return all_comments


if __name__ == '__main__':
    aweme_id = '7345429999001947404'
    comments = get_douyin_all_comment(aweme_id)
    # print(get_douyin_comment('7345429999001947404', cursor='20'))
    # print(get_douyin_comment('7345429999001947404', cursor='40'))