from DrissionPage import ChromiumPage
from DrissionPage.common import *
import time
# 实现单个课程的刷课逻辑
'''
接受一个课程id,执行刷课
1. 跳转到对应课程页面
2. 进入相应的课程界面
3. 循环检验课程是否完成
4. 完成当前课程后退出
'''
def one_course(cid:str,ctype:str,crate:int):
    # 接管浏览器
    cur_page = ChromiumPage()
    # 判定课程类别
    if ctype == '必修':
        cur_page.ele('@value=1').click()
    elif ctype == '选修':
        cur_page.ele('@value=2').click()
    elif ctype == '专题':
        cur_page.ele('@value=4').click()
    elif ctype == '培训':
        cur_page.ele('@value=5').click()
    time.sleep(1)
    # 利用课程序号定位，跳转到视频页面
    trs = cur_page.ele('#tbody').eles('tag:tr')
    for tr in trs:
        # 鉴别课程序号
        if tr.ele('tag:td').text.split('\t')[0] == cid:
            # 进入视频页面
            tr.ele('tag:button@@text():进入学习').click()
            cur_page.wait.new_tab(timeout=3) # 等待新标签页出现
            tab = cur_page.get_tab(cur_page.latest_tab) # 获取新标签页
            time.sleep(1)
            if crate == 100:
                print('当前课程已完成')
                cur_page.close_tabs(tabs_or_ids=[tab])
            # 进入后，获得当前视频的完成率
            try:
                if tab.ele('tag:a@@text():继续学习'):
                    tab.ele('tag:a@@text():继续学习').click()
            except BaseException:
                tab.ele('c:#normalModel_video > xg-start > div.xgplayer-icon-play > svg > path').click()
            # 建立循环，检测当前视频是否完播
            '''
            <div id="normalModel_nodeList" style="max-height:550px;overflow:auto;">
 			<div class="item-title selected" id="node_27817"><div class="courseName" title="活的马克思主义(上)" style="font-size:13px;">活的马克思主义(上)</div><span class="progressBar progress" style="font-size:12px;" id="progress_27817"><img id="progress_27817_percentImage" src="/js/axsProgress/images/percentImage.png" alt="100" style="width: 70px;height:12px;background-position: -50px 50%;background-image: url(/js/axsProgress/images/percentImage_back1.png);padding: 0;margin: 0;" class="percentImage" title="100%"> <span id="progress_27817_percentText" class="percentText" style="font-size:13px;">100%</span></span></div><div class="item-title" id="node_27821"><div class="courseName" title="活的马克思主义(下)" style="font-size:13px;">活的马克思主义(下)</div><span class="progressBar progress" style="font-size:12px;" id="progress_27821"><img id="progress_27821_percentImage" src="/js/axsProgress/images/percentImage.png" alt="100" style="width: 70px;height:12px;background-position: -50px 50%;background-image: url(/js/axsProgress/images/percentImage_back1.png);padding: 0;margin: 0;" class="percentImage" title="100%"> <span id="progress_27821_percentText" class="percentText" style="font-size:13px;">100%</span></span></div></div>
            '''
            l = []
            while 1:
                # 想要加一个定时刷新的功能方便释放内存
                watch_rates = tab.ele('#normalModel_nodeList').eles('tag:span')
                for watch_rate in watch_rates:
                    l.append(int(watch_rate.text[:-1]))
                # 取偶数索引
                l = l[::2]
                n = len(l)
                if l == [100]*len(l):
                    # 关闭当前标签页
                    cur_page.close_tabs(tabs_or_ids=[tab])
                time.sleep(5)
            break
if __name__ == '__main__':
    one_course('6992','培训',68)