import os
import requests
import pandas as pd
from datetime import datetime
from douyin import get_douyin_all_comment


def process_comments(comments):
    """
    Process comments into a DataFrame.
    :param comments: List of comments.
    :return: DataFrame of comments.
    """
    data = [{
        "用户昵称": c['user']['nickname'],
        "评论内容": c['text'],
        "点赞数": c['digg_count'],
        "评论时间": datetime.fromtimestamp(c['create_time']).strftime('%Y-%m-%d %H:%M:%S'),
        "ip地址": c['ip_label'],
        "评论等级": "一级评论",
    } for c in comments]
    return pd.DataFrame(data)


def save(data: pd.DataFrame, filename):
    """
    Save DataFrame to a CSV file.
    :param data: DataFrame to save.
    :param filename: Name of the CSV file.
    """
    data.to_csv(filename, index=False, encoding="utf-8-sig")


def share_url_to_aweme_id(share_url: str) -> str:
    """
    Extract aweme_id from a share URL.
    :param share_url: Share URL of the video.
    :return: aweme_id of the video.
    """
    res = requests.get(share_url, allow_redirects=False)
    return res.headers['Location'].split('/')[5]


def main(share_url=None):
    """
    Main function to fetch and save comments and replies.
    """
    if not share_url:
        share_url = input("Enter the share URL: ")
    aweme_id = share_url_to_aweme_id(share_url)

    # Fetch comments
    if not os.path.exists(f"data\comments_{aweme_id}.csv"):
        comment_list = get_douyin_all_comment(aweme_id)
        all_comments_ = process_comments(comment_list)
        print(f"Found {len(comment_list)} comments")
        save(all_comments_, f"data\comments_{aweme_id}.csv")
        print(f"Saved comments to comments_{aweme_id}.csv")
    else:
        comment_list = pd.read_csv(f"data\comments_{aweme_id}.csv")
        print(f"Found exist {len(comment_list)} comments")


if __name__ == '__main__':
    # main("https://v.douyin.com/irKCtpks/")
    # main("https://v.douyin.com/irKXFQ6e/")
    # main("https://v.douyin.com/irKXBV8D/")
    # main("https://v.douyin.com/irKXhM7Y/")
    # main("https://v.douyin.com/irKXhaYH/")
    # main("https://v.douyin.com/irKXPEM4/")
    # main("https://v.douyin.com/irKXnR7a/")
    # main("https://v.douyin.com/irKX3SA2/")
    # main("https://v.douyin.com/irKXVrG1/")
    # main("https://v.douyin.com/irKXX4sb/")
    # main("https://v.douyin.com/irKXWHkS/")
    # main("https://v.douyin.com/irKVSTHn/")
    # main("https://v.douyin.com/irKVSpMF/")
    main("https://v.douyin.com/ihREfNvj/")
