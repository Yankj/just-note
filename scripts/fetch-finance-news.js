#!/usr/bin/env node

/**
 * 财经新闻抓取脚本
 * 从多个源抓取可能影响股市的重要新闻
 */

const https = require('https');
const http = require('http');

// 新闻源配置
const NEWS_SOURCES = [
  {
    name: '财联社',
    url: 'https://www.cls.cn/telegraph',
    api: 'https://www.cls.cn/nodeapi/updateTelegraphList'
  },
  {
    name: '华尔街见闻',
    url: 'https://wallstreetcn.com/live',
    api: 'https://api-one.wallstreetcn.com/apigateway/live/rolling'
  },
  {
    name: '新浪财经',
    url: 'https://finance.sina.com.cn/7x24',
    api: 'https://finance.sina.com.cn/7x24/api'
  }
];

// 关键词过滤
const KEYWORDS = {
  important: [
    'GDP', 'CPI', 'PMI', '央行', '利率', '降准', '降息',
    '财政', '货币', '通胀', '失业', '经济', '贸易',
    '财报', '盈利', '亏损', '重组', '并购', 'IPO',
    '监管', '政策', '法规', '税收', '补贴',
    '战争', '冲突', '选举', '制裁', '协议',
    '原油', '黄金', '美元', '汇率', '人民币',
    '科创板', '创业板', '牛市', '熊市', '崩盘', '暴涨', '暴跌'
  ],
  negative: [
    '下跌', '暴跌', '亏损', '衰退', '危机', '风险',
    '制裁', '调查', '处罚', '诉讼', '违约', '破产',
    '战争', '冲突', '疫情', '灾难', '事故'
  ],
  positive: [
    '上涨', '暴涨', '盈利', '增长', '突破', '利好',
    '合作', '签约', '获批', '创新', '领先', '复苏',
    '协议', '和解', '奖励', '支持', '鼓励'
  ]
};

/**
 * 判断新闻是否重要
 */
function isImportantNews(title, content) {
  const text = (title + ' ' + content).toLowerCase();
  
  // 检查是否包含重要关键词
  for (const keyword of KEYWORDS.important) {
    if (text.includes(keyword.toLowerCase())) {
      return true;
    }
  }
  
  return false;
}

/**
 * 判断新闻情感
 */
function analyzeSentiment(title, content) {
  const text = (title + ' ' + content).toLowerCase();
  
  let positiveScore = 0;
  let negativeScore = 0;
  
  for (const word of KEYWORDS.positive) {
    if (text.includes(word.toLowerCase())) {
      positiveScore++;
    }
  }
  
  for (const word of KEYWORDS.negative) {
    if (text.includes(word.toLowerCase())) {
      negativeScore++;
    }
  }
  
  if (negativeScore > positiveScore) {
    return 'negative';
  } else if (positiveScore > negativeScore) {
    return 'positive';
  } else {
    return 'neutral';
  }
}

/**
 * 抓取新闻
 */
function fetchNews(source) {
  return new Promise((resolve, reject) => {
    const client = source.api.startsWith('https') ? https : http;
    
    client.get(source.api, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
      }
    }, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve({ source: source.name, data: json });
        } catch (e) {
          resolve({ source: source.name, error: e.message });
        }
      });
    }).on('error', (e) => {
      resolve({ source: source.name, error: e.message });
    });
  });
}

/**
 * 格式化新闻
 */
function formatNews(news) {
  const sentiment = news.sentiment;
  const emoji = sentiment === 'positive' ? '📈' : sentiment === 'negative' ? '📉' : '⚠️';
  
  return `${emoji} [${news.source}] ${news.title}\n   ${news.content.substring(0, 100)}${news.content.length > 100 ? '...' : ''}\n   ${news.time}`;
}

/**
 * 主函数
 */
async function main() {
  console.log(`[${new Date().toISOString()}] 开始抓取财经新闻...`);
  
  const allNews = [];
  
  // 并行抓取所有新闻源
  const results = await Promise.all(NEWS_SOURCES.map(fetchNews));
  
  for (const result of results) {
    if (result.error) {
      console.log(`❌ ${result.source}: ${result.error}`);
      continue;
    }
    
    console.log(`✅ ${result.source}: 获取成功`);
    // 这里需要解析实际的 API 响应格式
    // 由于不同源的 API 格式不同，需要分别处理
  }
  
  // 筛选重要新闻
  const importantNews = allNews.filter(news => isImportantNews(news.title, news.content));
  
  // 按情感分类
  const positive = importantNews.filter(n => n.sentiment === 'positive');
  const negative = importantNews.filter(n => n.sentiment === 'negative');
  const neutral = importantNews.filter(n => n.sentiment === 'neutral');
  
  // 生成推送内容
  const now = new Date();
  const message = [
    `【股市快讯】${now.toISOString().slice(0, 16).replace('T', ' ')}`,
    '',
    `📈 重要利好 (${positive.length}):`,
    ...positive.map(formatNews),
    '',
    `📉 重要利空 (${negative.length}):`,
    ...negative.map(formatNews),
    '',
    `⚠️ 需要关注 (${neutral.length}):`,
    ...neutral.map(formatNews),
    '',
    '---',
    `下次推送：${new Date(now.getTime() + 2 * 60 * 60 * 1000).toLocaleTimeString('zh-CN', {hour: '2-digit', minute:'2-digit'})}`
  ].filter(line => line !== '').join('\n');
  
  console.log('\n' + message);
  
  // 输出到文件，供 cron 调用
  const fs = require('fs');
  const outputPath = '/home/admin/openclaw/workspace/temp/latest-finance-news.md';
  fs.writeFileSync(outputPath, message);
  console.log(`\n📁 已保存到：${outputPath}`);
}

main().catch(console.error);
