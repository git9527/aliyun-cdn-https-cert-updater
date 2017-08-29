基于阿里云CDN API手册python版本签名机制代码示例[点击下载](https://docs-aliyun.cn-hangzhou.oss.aliyun-inc.com/cn/cdn/0.1.99/assets/api/callmethod_sdk_python.zip?spm=5176.doc27149.2.1.eijrGE&file=callmethod_sdk_python.zip)

使用方法:

1. 确保python已安装Requests(http://docs.python-requests.org/en/master/user/install/#install)
2. 使用说明
    * 上传新的key文件和cert文件
    
        `python updater.py -i LTAI**** -s aBPGz3**** -d www.***.*** -p ./certs/*.key -c ./certs/fullchain.cer`
    * 使用已有cert name更新https设置
    
        `python updater.py -i LTAI**** -s aBPGz3**** -d www.***.*** -n some_name`

