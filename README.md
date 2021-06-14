# 美篇文章爬虫
## 项目简介
  该项目使用 python 语言的爬虫库 scrapy 以及动态渲染插件 selenium ，从 www.meipian.cn 网站
  上爬取用户的文章 标题、内容、配图、点赞数量，阅读数量，是否加精，发布时间等内容。并以 json 和 xlsx 两种
  格式存储了格式化的数据。 分析。。。。（）
  
## 流程说明

### 抓取数据
代码位置 meipianCrawler/spider/article_spider.py:ArticleSpider

执行逻辑：
1. 使用 selenium-python 模拟用户登录流程，在首页选择使用账号密码登录。
2. 在登录后，进入文章详情页面，模拟点击分享按钮生成分享链接 share_url ，每页总共有12个文章卡片，yield 生成12个SeleniumRequest。
3. 检查向后翻页按钮，若是 enable 状态，调用 javascript 点击翻页，重复步骤2、3，直到翻页按钮变成 disabled 状态。

设计说明：
使用 start_requests 方法返回 Request 对象生成器，后续 parser 中无须继续增加 Request，所以只需要返回 item

### 数据清洗
Response 数据主要经过 ArticleSpider.parse() 变成 ArticleItem 对象，在 parse 函数中使用了 itemLoader 对象简化数据提取工作，
ArticleItem 对象定义中使用 input_processor 去除空白字符，和 output_processor 将数据格式转化为字符串类型。然后 item 进入 pipeline 进行最终处理。
在 settings.py 文件中配置了 PrintXLSXPipeline PrintJsonPipeline 两个数据处理管道分别将 items 序列化输出到 items.json 和 items.xlsx 。其中对空白字符填充了默认值。