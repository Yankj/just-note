import { Outlet, Link, useLocation } from 'react-router-dom';

export default function App() {
  const location = useLocation();

  const navItems = [
    { path: '/', label: '总览', icon: '🏠' },
    { path: '/assets', label: '资产', icon: '💼' },
    { path: '/transactions', label: '交易', icon: '📊' },
    { path: '/diaries', label: '日记', icon: '📝' },
    { path: '/analytics', label: '分析', icon: '📈' },
  ];

  return (
    <div className="min-h-screen">
      {/* 顶部导航 - 玻璃态 */}
      <header className="glass-strong sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-3 group">
              <span className="text-4xl group-hover:scale-110 transition-transform duration-300">💎</span>
              <div>
                <h1 className="text-2xl font-bold gradient-text">财务自由之路</h1>
                <p className="text-xs text-white/60 -mt-1">AI Wealth Manager</p>
              </div>
            </Link>

            {/* 导航菜单 - 桌面端 */}
            <nav className="hidden md:flex items-center space-x-2">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`px-4 py-2 rounded-xl transition-all duration-300 flex items-center space-x-2 ${
                    location.pathname === item.path
                      ? 'bg-white text-purple-600 shadow-lg scale-105'
                      : 'text-white/80 hover:bg-white/10 hover:text-white'
                  }`}
                >
                  <span className="text-lg">{item.icon}</span>
                  <span className="font-medium">{item.label}</span>
                </Link>
              ))}
            </nav>

            {/* 设置按钮 */}
            <Link
              to="/settings"
              className="glass-light px-4 py-2 rounded-xl text-white/80 hover:text-white transition-all duration-300 flex items-center space-x-2 hover:bg-white/15"
            >
              <span>⚙️</span>
              <span className="hidden sm:inline">设置</span>
            </Link>
          </div>
        </div>

        {/* 移动端导航 - 底部固定 */}
        <nav className="md:hidden fixed bottom-0 left-0 right-0 glass-strong safe-area-pb">
          <div className="flex justify-around items-center h-16 px-2">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`flex flex-col items-center justify-center w-full h-full space-y-1 ${
                  location.pathname === item.path
                    ? 'text-white'
                    : 'text-white/60'
                }`}
              >
                <span className={`text-2xl ${location.pathname === item.path ? 'scale-110' : ''} transition-transform`}>
                  {item.icon}
                </span>
                <span className="text-xs">{item.label}</span>
              </Link>
            ))}
          </div>
        </nav>
      </header>

      {/* 主内容区 */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pb-24 md:pb-8">
        <Outlet />
      </main>

      {/* 底部版权 */}
      <footer className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 hidden md:block">
        <p className="text-center text-white/40 text-sm">
          © 2026 财务自由之路 · Made with AI · <span className="text-white/60">UI/UX by Pro Max</span>
        </p>
      </footer>
    </div>
  );
}
