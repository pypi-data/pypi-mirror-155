import os
#winrar 路径
winrarpath = 'C:\Program Files\WinRAR\WinRAR.exe'

#压缩密码
# password = '123456zxc'

#分卷大小
fenjuansize = '2g -v4g'

#修复BUG的模式
fenjuansize_bug = 1024*1024*2
#输出模式 ，如果为1直接输出到文件的当前文件夹，为0则是outinput_path 的路径
outmethod = 1

#压缩完之后是否删除附件文件
yasuo_after_delet = True
#压缩文件输出路径
# outinput_path = None

#随机生成文件，防止压缩包md5相同
suijishu = False

#自解压选择
# zijieya_text = 'comment.txt'
zijieya_text = 'comment_card.txt'
zijieya_text = os.path.join(os.path.dirname(__file__),zijieya_text)
#要额外附加的宣传文件
# other_add_file = [
#     r'F:\python\pyqt5\tools\fujia\更多游戏下载.url',
#
# ]
other_add_file = [
    r'F:\python\pyqt5\tools\fujia\更多游戏MOD下载.url',
]

if __name__ == '__main__':
    import os
    print(os.path.dirname(other_add_file[0]))