import React from 'react';

export default function Settings() {
  return (
    <div className="space-y-6 animate-fade-in-up">
      {/* 页面标题 */}
      <div>
        <h2 className="text-4xl font-bold gradient-text">设置</h2>
        <p className="text-white/60 mt-1">管理你的账户和偏好设置</p>
      </div>

      {/* 账户信息 */}
      <div className="glass-strong rounded-2xl p-6 card-hover">
        <h3 className="text-xl font-bold gradient-text mb-6 flex items-center">
          <span className="mr-3">👤</span>
          账户信息
        </h3>
        <div className="space-y-4">
          <div className="flex justify-between items-center py-3 border-b border-white/10">
            <span className="text-white/60">登录状态</span>
            <span className="text-green-400 font-medium flex items-center">
              <span className="w-2 h-2 bg-green-400 rounded-full mr-2"></span>
              演示模式
            </span>
          </div>
          <div className="flex justify-between items-center py-3 border-b border-white/10">
            <span className="text-white/60">邮箱</span>
            <span className="text-white/80">未登录</span>
          </div>
          <div className="flex justify-between items-center py-3 border-b border-white/10">
            <span className="text-white/60">用户名</span>
            <span className="text-white/80">未登录</span>
          </div>
        </div>
        <div className="mt-6">
          <a href="/login" className="btn-primary w-full block text-center">
            登录/注册
          </a>
        </div>
      </div>

      {/* 财务目标 */}
      <div className="glass-strong rounded-2xl p-6 card-hover">
        <h3 className="text-xl font-bold gradient-text mb-6 flex items-center">
          <span className="mr-3">🎯</span>
          财务目标
        </h3>
        <div className="space-y-5">
          <div>
            <label className="text-white/70 text-sm font-medium block mb-2">
              目标金额
            </label>
            <input
              type="text"
              placeholder="¥10,000,000"
              className="input-glass w-full"
            />
            <p className="text-white/40 text-xs mt-2">
              你希望的财务自由目标金额
            </p>
          </div>
          <div>
            <label className="text-white/70 text-sm font-medium block mb-2">
              期望达成日期
            </label>
            <input
              type="date"
              className="input-glass w-full"
            />
          </div>
          <div>
            <label className="text-white/70 text-sm font-medium block mb-2">
              每月储蓄目标
            </label>
            <input
              type="text"
              placeholder="¥10,000"
              className="input-glass w-full"
            />
          </div>
        </div>
        <button className="btn-primary w-full mt-6">
          保存目标
        </button>
      </div>

      {/* 投资偏好 */}
      <div className="glass-strong rounded-2xl p-6 card-hover">
        <h3 className="text-xl font-bold gradient-text mb-6 flex items-center">
          <span className="mr-3">⚙️</span>
          投资偏好
        </h3>
        <div className="space-y-4">
          <div>
            <label className="text-white/70 text-sm font-medium block mb-2">
              风险承受能力
            </label>
            <select className="input-glass w-full">
              <option value="">请选择</option>
              <option value="conservative">保守型 - 保本为主</option>
              <option value="moderate">稳健型 - 平衡风险</option>
              <option value="aggressive">进取型 - 追求高收益</option>
            </select>
          </div>
          <div>
            <label className="text-white/70 text-sm font-medium block mb-2">
              主要投资市场
            </label>
            <div className="flex flex-wrap gap-2">
              {['A 股', '港股', '美股', '基金', '加密货币'].map((market) => (
                <label key={market} className="flex items-center space-x-2 glass-light px-4 py-2 rounded-lg cursor-pointer hover:bg-white/10 transition-colors">
                  <input type="checkbox" className="rounded" />
                  <span className="text-white/80 text-sm">{market}</span>
                </label>
              ))}
            </div>
          </div>
        </div>
        <button className="btn-primary w-full mt-6">
          保存偏好
        </button>
      </div>

      {/* 关于 */}
      <div className="glass-light rounded-2xl p-6">
        <h3 className="text-xl font-bold gradient-text mb-4 flex items-center">
          <span className="mr-3">ℹ️</span>
          关于
        </h3>
        <div className="space-y-2 text-sm text-white/60">
          <p>版本：1.0.0</p>
          <p>UI/UX: Optimized by UI/UX Pro Max</p>
          <p>© 2026 财务自由之路 · Made with AI</p>
        </div>
      </div>
    </div>
  );
}
