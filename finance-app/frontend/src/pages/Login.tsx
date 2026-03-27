import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authApi } from '../services/auth';

export default function Login() {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (isLogin) {
        const tokenData = await authApi.login({
          username: email,
          password,
        });
        localStorage.setItem('access_token', tokenData.access_token);
        localStorage.setItem('refresh_token', tokenData.refresh_token);
        navigate('/');
      } else {
        await authApi.register({
          email,
          username,
          password,
        });
        // 注册成功后自动登录
        const tokenData = await authApi.login({ username: email, password });
        localStorage.setItem('access_token', tokenData.access_token);
        localStorage.setItem('refresh_token', tokenData.refresh_token);
        navigate('/');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || '操作失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = () => {
    navigate('/');
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 animate-fade-in">
      {/* 登录卡片 */}
      <div className="glass-strong rounded-3xl p-8 w-full max-w-md card-hover">
        {/* Logo 和标题 */}
        <div className="text-center mb-8">
          <div className="text-6xl mb-4 animate-pulse">💎</div>
          <h1 className="text-4xl font-bold gradient-text mb-2">财务自由之路</h1>
          <p className="text-white/60">AI 原生财富管理助手</p>
        </div>

        {/* 登录/注册切换 */}
        <div className="flex mb-6 glass rounded-xl p-1">
          <button
            onClick={() => { setIsLogin(true); setError(''); }}
            className={`flex-1 py-3 rounded-lg transition-all duration-300 font-medium ${
              isLogin 
                ? 'bg-white text-purple-600 shadow-lg' 
                : 'text-white/60 hover:text-white'
            }`}
          >
            登录
          </button>
          <button
            onClick={() => { setIsLogin(false); setError(''); }}
            className={`flex-1 py-3 rounded-lg transition-all duration-300 font-medium ${
              !isLogin 
                ? 'bg-white text-purple-600 shadow-lg' 
                : 'text-white/60 hover:text-white'
            }`}
          >
            注册
          </button>
        </div>

        {/* 错误提示 */}
        {error && (
          <div className="mb-6 p-4 bg-red-500/20 border border-red-500/50 rounded-xl text-red-200 text-sm animate-fade-in">
            <div className="flex items-start">
              <span className="mr-2">⚠️</span>
              {error}
            </div>
          </div>
        )}

        {/* 登录表单 */}
        <form onSubmit={handleSubmit} className="space-y-5">
          {!isLogin && (
            <div className="animate-fade-in">
              <label className="block text-white/70 text-sm font-medium mb-2">
                用户名
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="input-glass w-full"
                placeholder="请输入用户名"
                required={!isLogin}
                autoComplete="username"
              />
            </div>
          )}
          
          <div>
            <label className="block text-white/70 text-sm font-medium mb-2">
              邮箱
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="input-glass w-full"
              placeholder="请输入邮箱"
              required
              autoComplete="email"
            />
          </div>
          
          <div>
            <label className="block text-white/70 text-sm font-medium mb-2">
              密码
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="input-glass w-full"
              placeholder="请输入密码"
              required
              minLength={8}
              autoComplete={isLogin ? 'current-password' : 'new-password'}
            />
          </div>
          
          <button
            type="submit"
            disabled={loading}
            className="btn-primary w-full py-4 text-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            {loading ? (
              <>
                <span className="loading-spinner mr-2"></span>
                处理中...
              </>
            ) : (
              isLogin ? '🔐 登录' : '✨ 注册'
            )}
          </button>
        </form>

        {/* 演示模式 */}
        <div className="mt-6 text-center">
          <button
            onClick={handleDemoLogin}
            className="text-white/50 hover:text-white text-sm transition-colors duration-300 flex items-center justify-center mx-auto"
          >
            <span className="mr-2">🎭</span>
            跳过登录，进入演示模式
          </button>
        </div>

        {/* 安全提示 */}
        <div className="mt-6 pt-6 border-t border-white/10">
          <p className="text-white/40 text-xs text-center">
            🔒 您的信息已加密保护 · 注册即同意服务条款
          </p>
        </div>
      </div>
    </div>
  );
}
