import React, { useState } from 'react';

export default function Assets() {
  const [showAddModal, setShowAddModal] = useState(false);
  
  const assetTypes = [
    { name: 'A 股', icon: '🇨🇳', color: 'from-red-500 to-red-600', count: 0 },
    { name: '港股', icon: '🇭🇰', color: 'from-blue-500 to-blue-600', count: 0 },
    { name: '美股', icon: '🇺🇸', color: 'from-green-500 to-green-600', count: 0 },
    { name: '基金', icon: '📊', color: 'from-purple-500 to-purple-600', count: 0 },
    { name: '加密货币', icon: '₿', color: 'from-orange-500 to-orange-600', count: 0 },
    { name: '现金', icon: '💵', color: 'from-emerald-500 to-emerald-600', count: 0 },
  ];

  return (
    <div className="space-y-6 animate-fade-in-up">
      {/* 页面标题 */}
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4">
        <div>
          <h2 className="text-4xl font-bold gradient-text">资产管理</h2>
          <p className="text-white/60 mt-1">追踪你的全资产分布，掌控财富全局</p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="btn-primary inline-flex items-center justify-center space-x-2"
        >
          <span>➕</span>
          <span>添加资产</span>
        </button>
      </div>

      {/* 资产总览卡片 */}
      <div className="glass-strong rounded-3xl p-8 card-hover">
        <div className="flex items-center justify-between mb-6">
          <div>
            <p className="text-white/60 text-sm mb-1">总资产估值</p>
            <p className="text-5xl font-bold gradient-text">¥0.00</p>
          </div>
          <div className="text-right">
            <p className="text-white/60 text-sm mb-1">今日涨跌</p>
            <p className="text-2xl font-bold text-green-400">+¥0.00</p>
          </div>
        </div>
        
        {/* 进度条 */}
        <div className="space-y-3">
          <div className="flex justify-between text-sm">
            <span className="text-white/60">财务自由进度</span>
            <span className="text-white/80 font-medium">0%</span>
          </div>
          <div className="h-3 bg-white/10 rounded-full overflow-hidden">
            <div className="h-full bg-gradient-to-r from-purple-500 to-pink-500 w-0 transition-all duration-1000"></div>
          </div>
        </div>
      </div>

      {/* 空状态 */}
      <div className="glass rounded-3xl p-12 text-center card-hover">
        <div className="text-7xl mb-6">💼</div>
        <h3 className="text-2xl font-bold gradient-text mb-3">还没有资产</h3>
        <p className="text-white/60 text-lg mb-8 max-w-md mx-auto">
          添加你的第一个资产，开始财富管理之旅。支持股票、基金、加密货币等多种资产类型。
        </p>
        <button
          onClick={() => setShowAddModal(true)}
          className="btn-primary text-lg px-8 py-4"
        >
          添加资产
        </button>
      </div>

      {/* 资产类型网格 */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
        {assetTypes.map((type, index) => (
          <button
            key={type.name}
            className="glass rounded-2xl p-6 card-hover group"
            style={{ animationDelay: `${index * 0.05}s` }}
          >
            <div className={`text-5xl mb-4 bg-gradient-to-br ${type.color} w-20 h-20 rounded-2xl flex items-center justify-center mx-auto group-hover:scale-110 transition-transform duration-300`}>
              {type.icon}
            </div>
            <p className="text-white font-bold text-center mb-1">{type.name}</p>
            <p className="text-white/50 text-sm text-center">{type.count} 持仓</p>
          </button>
        ))}
      </div>

      {/* 投资知识提示 */}
      <div className="glass-light rounded-2xl p-6">
        <div className="flex items-start space-x-4">
          <span className="text-3xl">💡</span>
          <div>
            <h4 className="font-bold text-white mb-2">分散投资的重要性</h4>
            <p className="text-white/60 text-sm leading-relaxed">
              不要把鸡蛋放在一个篮子里。通过配置不同资产类别（股票、债券、现金等），
              可以有效降低风险，提高长期收益的稳定性。建议根据年龄、风险承受能力和投资目标来配置资产。
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
