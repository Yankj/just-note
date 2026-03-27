import React from 'react';
import { Link } from 'react-router-dom';

export default function Dashboard() {
  const stats = [
    { label: '总资产', value: '¥0.00', icon: '💰', change: '+0%', trend: 'neutral' },
    { label: '总盈亏', value: '+¥0.00', icon: '📈', change: '+0%', trend: 'positive' },
    { label: '持仓数', value: '0', icon: '📊', change: '0', trend: 'neutral' },
    { label: '今日盈亏', value: '¥0.00', icon: '📉', change: '+0%', trend: 'neutral' },
  ];

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'positive': return 'text-green-400';
      case 'negative': return 'text-red-400';
      default: return 'text-white/60';
    }
  };

  return (
    <div className="space-y-8 animate-fade-in-up">
      {/* 欢迎区域 - 主卡片 */}
      <div className="glass-strong rounded-3xl p-8 card-hover">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h2 className="text-4xl font-bold gradient-text mb-3">欢迎回来 👋</h2>
            <p className="text-lg text-white/70">开始管理你的资产，迈向财务自由</p>
          </div>
          <div className="flex gap-3">
            <Link
              to="/assets"
              className="btn-primary inline-flex items-center space-x-2"
            >
              <span>➕</span>
              <span>添加资产</span>
            </Link>
            <Link
              to="/transactions"
              className="btn-secondary inline-flex items-center space-x-2"
            >
              <span>📝</span>
              <span>记录交易</span>
            </Link>
          </div>
        </div>
      </div>

      {/* 统计卡片网格 */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <div
            key={index}
            className="glass rounded-2xl p-6 card-hover animate-fade-in"
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <div className="flex items-center justify-between mb-4">
              <span className="text-4xl">{stat.icon}</span>
              <span className={`text-sm font-medium px-2 py-1 rounded-full bg-white/10 ${getTrendColor(stat.trend)}`}>
                {stat.change}
              </span>
            </div>
            <p className="text-white/60 text-sm mb-1">{stat.label}</p>
            <p className="text-3xl font-bold gradient-text">{stat.value}</p>
          </div>
        ))}
      </div>

      {/* 快捷入口 - 功能卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Link to="/diaries" className="glass rounded-2xl p-6 card-hover group">
          <div className="flex items-start justify-between mb-4">
            <span className="text-5xl">📝</span>
            <span className="text-white/40 group-hover:text-white/80 transition-colors">→</span>
          </div>
          <h3 className="text-xl font-bold gradient-text mb-2">投资日记</h3>
          <p className="text-white/60 text-sm mb-4">记录投资反思，复盘交易逻辑</p>
          <div className="flex items-center text-sm">
            <span className="text-purple-300 group-hover:text-purple-200 transition-colors font-medium">
              开始写作 →
            </span>
          </div>
        </Link>

        <Link to="/analytics" className="glass rounded-2xl p-6 card-hover group">
          <div className="flex items-start justify-between mb-4">
            <span className="text-5xl">📊</span>
            <span className="text-white/40 group-hover:text-white/80 transition-colors">→</span>
          </div>
          <h3 className="text-xl font-bold gradient-text mb-2">数据分析</h3>
          <p className="text-white/60 text-sm mb-4">可视化资产分布，追踪收益趋势</p>
          <div className="flex items-center text-sm">
            <span className="text-purple-300 group-hover:text-purple-200 transition-colors font-medium">
              查看分析 →
            </span>
          </div>
        </Link>

        <Link to="/settings" className="glass rounded-2xl p-6 card-hover group">
          <div className="flex items-start justify-between mb-4">
            <span className="text-5xl">⚙️</span>
            <span className="text-white/40 group-hover:text-white/80 transition-colors">→</span>
          </div>
          <h3 className="text-xl font-bold gradient-text mb-2">财务目标</h3>
          <p className="text-white/60 text-sm mb-4">设定财务自由目标，追踪进度</p>
          <div className="flex items-center text-sm">
            <span className="text-purple-300 group-hover:text-purple-200 transition-colors font-medium">
              设置目标 →
            </span>
          </div>
        </Link>
      </div>

      {/* 投资理念 - 价值观展示 */}
      <div className="glass rounded-2xl p-8">
        <h3 className="text-2xl font-bold gradient-text mb-6 flex items-center">
          <span className="mr-3">💡</span>
          投资理念
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="space-y-3">
            <div className="flex items-center space-x-3">
              <span className="text-3xl">🎯</span>
              <h4 className="text-lg font-bold text-white">长期主义</h4>
            </div>
            <p className="text-white/60 text-sm leading-relaxed pl-12">
              做时间的朋友，享受复利的力量。不要试图预测市场，而是长期持有优质资产。
            </p>
          </div>
          <div className="space-y-3">
            <div className="flex items-center space-x-3">
              <span className="text-3xl">🛡️</span>
              <h4 className="text-lg font-bold text-white">风险控制</h4>
            </div>
            <p className="text-white/60 text-sm leading-relaxed pl-12">
              永远不要亏钱，这是第一条规则。分散投资，设置止损，保持安全边际。
            </p>
          </div>
          <div className="space-y-3">
            <div className="flex items-center space-x-3">
              <span className="text-3xl">📚</span>
              <h4 className="text-lg font-bold text-white">持续学习</h4>
            </div>
            <p className="text-white/60 text-sm leading-relaxed pl-12">
              市场永远在变，唯有学习不变。保持好奇心，不断更新认知体系。
            </p>
          </div>
        </div>
      </div>

      {/* 空状态提示 */}
      <div className="glass-light rounded-2xl p-8 text-center">
        <div className="text-6xl mb-4">🚀</div>
        <h3 className="text-xl font-bold gradient-text mb-2">开启你的财富之旅</h3>
        <p className="text-white/60 mb-6 max-w-md mx-auto">
          添加第一个资产，记录第一笔交易，开始你的财务自由之路
        </p>
        <div className="flex flex-wrap justify-center gap-3">
          <Link to="/assets" className="btn-primary">
            添加资产
          </Link>
          <Link to="/diaries" className="btn-secondary">
            写日记
          </Link>
        </div>
      </div>
    </div>
  );
}
