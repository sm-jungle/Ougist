#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从阿里云 OSS 同步文件到本地（用于 GitHub Actions）
"""

import oss2
import os
from pathlib import Path

# OSS 配置（从环境变量读取）
BUCKET = os.getenv('OSS_BUCKET', 'ougist-marketing')
ENDPOINT = os.getenv('OSS_ENDPOINT', 'oss-cn-hangzhou.aliyuncs.com')
ACCESS_KEY_ID = os.getenv('OSS_ACCESS_KEY_ID')
ACCESS_KEY_SECRET = os.getenv('OSS_ACCESS_KEY_SECRET')

# 本地目录（GitHub 仓库根目录）
LOCAL_DIR = Path('.')

# OSS 路径
OSS_PATH = 'marketing'

def sync_from_oss():
    """从 OSS 同步文件到本地"""
    
    print("=" * 50)
    print("OUGIST Marketing 文件从 OSS 同步到 GitHub")
    print("=" * 50)
    
    # 认证
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ENDPOINT, BUCKET)
    
    # 检查 Bucket 是否存在
    try:
        bucket.get_bucket_info()
        print(f"✓ Bucket: {BUCKET}")
    except Exception as e:
        print(f"✗ 无法访问 Bucket: {e}")
        return False
    
    # 列出并下载所有文件
    print(f"\nOSS 路径：oss://{BUCKET}/{OSS_PATH}/\n")
    
    downloaded = 0
    failed = 0
    
    for obj in oss2.ObjectIterator(bucket, prefix=OSS_PATH + '/'):
        # 跳过目录
        if obj.key.endswith('/'):
            continue
        
        # 本地文件路径
        relative_path = obj.key[len(OSS_PATH)+1:]
        local_path = LOCAL_DIR / relative_path
        
        # 创建目录
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 下载文件
        try:
            bucket.get_object_to_file(obj.key, str(local_path))
            print(f"✓ 下载：{relative_path}")
            downloaded += 1
        except Exception as e:
            print(f"✗ 失败：{relative_path} - {e}")
            failed += 1
    
    # 总结
    print("\n" + "=" * 50)
    print(f"同步完成！")
    print(f"✓ 成功：{downloaded} 个文件")
    print(f"✗ 失败：{failed} 个文件")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    sync_from_oss()
