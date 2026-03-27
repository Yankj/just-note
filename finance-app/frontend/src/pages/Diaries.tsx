import React from 'react';
import { Link } from 'react-router-dom';

export default function Diaries() {
  return (
    <div className="space-y-6 animate-fade-in-up">
      {/* 页面标题 */}
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4">
        <div>
          <h2 className="text-4xl font-bold gradient-text">投资日记</h2>
          <p className="text-white/60 mt-1">记录投资反思，复盘交易逻辑，持续成长</p>
        </div>
        <Link
          to="/diaries/new"
          className="btn-primary inline-flex items-center space-x-2"
        >
          <span>✏️</span>
          <span>写日记</span>
        </Link>
      </div>

      {/* 空状态 */}
      <div className="glass rounded-3xl p-12 text-center card-hover">
        <div className="text-7xl mb-6">📖</div>
        <h3 className="text-2xl font-bold gradient-text mb-3">还没有日记</h3>
        <p className="text-white/60 text-lg mb-8 max-w-md mx-auto">
          记录你的投资思考和复盘，这是成为优秀投资者的重要习惯。
          成功的投资者都有写投资日记的习惯。
        </p>
        <Link
          to="/diaries/new"
          className="btn-primary text-lg px-8 py-4"
        >
          开始写作
        </Link>
      </div>

      {/* 写日记的好处 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-light rounded-2xl p-6 card-hover">
          <div className="text-4xl mb-4">🎯</div>
          <h4 className="text-xl font-bold gradient-text mb-3">提升决策质量</h4>
          <p className="text-white/60 text-sm leading-relaxed">
            记录每次交易的思考过程，帮助你在未来遇到类似情况时做出更好的决策。
          </p>
        </div>

        <div className="glass-light rounded-2xl p-6 card-hover">
          <div className="text-4xl mb-4">📈</div>
          <h4 className="text-xl font-bold gradient-text mb-3">发现模式</h4>
          <p className="text-white/60 text-sm leading-relaxed">
            通过回顾历史日记，发现自己的投资模式和习惯，识别优势和改进空间。
          </p>
        </div>

        <div className="glass-light rounded-2xl p-6 card-hover">
          <div className="text-4xl mb-4">🧘</div>
          <h4 className="text-xl font-bold gradient-text mb-3">控制情绪</h4>
          <p className="text-white/60 text-sm leading-relaxed">
            写作是情绪管理的有效方式，帮助你在市场波动时保持冷静和理性。
          </p>
        </div>
      </div>

      {/* 投资日记模板 */}
      <div className="glass rounded-2xl p-8">
        <h3 className="text-2xl font-bold gradient-text mb-6 flex items-center">
          <span className="mr-3">📝</span>
          日记写作模板
        </h3>
        <div className="space-y-4">
          <div className="flex items-start space-x-4">
            <span className="text-white/40 font-mono text-sm mt-1">01</span>
            <div>
              <h4 className="font-bold text-white mb-1">今日市场观察</h4>
              <p className="text-white/60 text-sm">大盘走势如何？有哪些重要事件？</p>
            </div>
          </div>
          <div className="h-px bg-white/10"></div>
          
          <div className="flex items-start space-x-4">
            <span className="text-white/40 font-mono text-sm mt-1">02</span>
            <div>
              <h4 className="font-bold text-white mb-1">我的操作</h4>
              <p className="text-white/60 text-sm">今天做了什么交易？为什么？</p>
            </div>
          </div>
          <div className="h-px bg-white/10"></div>
          
          <div className="flex items-start space-x-4">
            <span className="text-white/40 font-mono text-sm mt-1">03</span>
            <div>
              <h4 className="font-bold text-white mb-1">反思与总结</h4>
              <p className="text-white/60 text-sm">哪些做对了？哪些可以改进？</p>
            </div>
          </div>
          <div className="h-px bg-white/10"></div>
          
          <div className="flex items-start space-x-4">
            <span className="text-white/40 font-mono text-sm mt-1">04</span>
            <div>
              <h4 className="font-bold text-white mb-1">明日计划</h4>
              <p className="text-white/60 text-sm">明天关注什么？有什么交易计划？</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
