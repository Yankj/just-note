import React from 'react';

export default function Analytics() {
  return (
    <div className="space-y-6 animate-fade-in-up">
      {/* 页面标题 */}
      <div>
        <h2 className="text-4xl font-bold gradient-text">数据分析</h2>
        <p className="text-white/60 mt-1">可视化你的投资表现，洞察财富趋势</p>
      </div>

      {/* 空状态 */}
      <div className="glass rounded-3xl p-12 text-center card-hover">
        <div className="text-7xl mb-6">📈</div>
        <h3 className="text-2xl font-bold gradient-text mb-3">暂无数据</h3>
        <p className="text-white/60 text-lg mb-8 max-w-md mx-auto">
          添加资产和交易记录后，这里会显示丰富的分析图表，包括：
          资产分布、收益趋势、盈亏分析等。
        </p>
        <div className="flex flex-wrap justify-center gap-3">
          <a href="/assets" className="btn-primary">
            添加资产
          </a>
          <a href="/transactions" className="btn-secondary">
            记录交易
          </a>
        </div>
      </div>

      {/* 将来会有的分析功能预览 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="glass-light rounded-2xl p-6 card-hover opacity-60">
          <div className="text-4xl mb-4">🥧</div>
          <h4 className="text-xl font-bold gradient-text mb-3">资产分布</h4>
          <p className="text-white/60 text-sm">
            饼图展示各类资产占比，帮助你了解资产配置是否合理。
          </p>
        </div>

        <div className="glass-light rounded-2xl p-6 card-hover opacity-60">
          <div className="text-4xl mb-4">📊</div>
          <h4 className="text-xl font-bold gradient-text mb-3">收益趋势</h4>
          <p className="text-white/60 text-sm">
            折线图展示总资产和收益率的变化趋势，追踪财富增长速度。
          </p>
        </div>

        <div className="glass-light rounded-2xl p-6 card-hover opacity-60">
          <div className="text-4xl mb-4">🎯</div>
          <h4 className="text-xl font-bold gradient-text mb-3">盈亏分析</h4>
          <p className="text-white/60 text-sm">
            分析各资产的盈亏贡献，找出你的"现金牛"和"拖油瓶"。
          </p>
        </div>

        <div className="glass-light rounded-2xl p-6 card-hover opacity-60">
          <div className="text-4xl mb-4">📅</div>
          <h4 className="text-xl font-bold gradient-text mb-3">交易日历</h4>
          <p className="text-white/60 text-sm">
            日历热力图展示交易频率，帮助你发现交易习惯。
          </p>
        </div>

        <div className="glass-light rounded-2xl p-6 card-hover opacity-60">
          <div className="text-4xl mb-4">🏆</div>
          <h4 className="text-xl font-bold gradient-text mb-3">最佳投资</h4>
          <p className="text-white/60 text-sm">
            排行榜展示收益率最高的投资，总结成功经验。
          </p>
        </div>

        <div className="glass-light rounded-2xl p-6 card-hover opacity-60">
          <div className="text-4xl mb-4">⚠️</div>
          <h4 className="text-xl font-bold gradient-text mb-3">风险指标</h4>
          <p className="text-white/60 text-sm">
            波动率、最大回撤等风险指标，评估投资组合风险水平。
          </p>
        </div>
      </div>
    </div>
  );
}
