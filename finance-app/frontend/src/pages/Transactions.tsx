import React, { useState } from 'react';

export default function Transactions() {
  const [filter, setFilter] = useState('all');
  
  const filters = [
    { id: 'all', label: '全部', icon: '📋' },
    { id: 'buy', label: '买入', icon: '💰' },
    { id: 'sell', label: '卖出', icon: '💸' },
  ];

  return (
    <div className="space-y-6 animate-fade-in-up">
      {/* 页面标题 */}
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4">
        <div>
          <h2 className="text-4xl font-bold gradient-text">交易记录</h2>
          <p className="text-white/60 mt-1">追踪每一笔买卖操作，复盘交易决策</p>
        </div>
        <button className="btn-primary inline-flex items-center space-x-2">
          <span>➕</span>
          <span>记录交易</span>
        </button>
      </div>

      {/* 筛选器 */}
      <div className="glass rounded-xl p-2 flex flex-wrap gap-2">
        {filters.map((f) => (
          <button
            key={f.id}
            onClick={() => setFilter(f.id)}
            className={`px-4 py-2 rounded-lg transition-all duration-300 flex items-center space-x-2 ${
              filter === f.id 
                ? 'bg-white text-purple-600 shadow-lg' 
                : 'text-white/70 hover:bg-white/10 hover:text-white'
            }`}
          >
            <span>{f.icon}</span>
            <span className="font-medium">{f.label}</span>
          </button>
        ))}
      </div>

      {/* 空状态 */}
      <div className="glass rounded-3xl p-12 text-center card-hover">
        <div className="text-7xl mb-6">📝</div>
        <h3 className="text-2xl font-bold gradient-text mb-3">暂无交易记录</h3>
        <p className="text-white/60 text-lg mb-8 max-w-md mx-auto">
          添加资产后，开始记录你的第一笔交易。良好的交易记录是投资成功的基础。
        </p>
        <div className="flex flex-wrap justify-center gap-3">
          <button className="btn-primary">
            记录交易
          </button>
          <button className="btn-secondary">
            查看资产
          </button>
        </div>
      </div>

      {/* 交易提示 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="glass-light rounded-2xl p-6">
          <div className="flex items-start space-x-4">
            <span className="text-3xl">✅</span>
            <div>
              <h4 className="font-bold text-white mb-2">好的交易习惯</h4>
              <ul className="text-white/60 text-sm space-y-1">
                <li>• 记录每笔交易的买入理由</li>
                <li>• 设置明确的止盈止损点</li>
                <li>• 定期复盘交易决策</li>
                <li>• 避免情绪化交易</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="glass-light rounded-2xl p-6">
          <div className="flex items-start space-x-4">
            <span className="text-3xl">⚠️</span>
            <div>
              <h4 className="font-bold text-white mb-2">常见交易误区</h4>
              <ul className="text-white/60 text-sm space-y-1">
                <li>• 追涨杀跌，频繁交易</li>
                <li>• 不止损，扛单到底</li>
                <li>• 听消息炒股，没有自己的判断</li>
                <li>• 仓位过重，风险集中</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
