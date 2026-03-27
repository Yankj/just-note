import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider, Layout, Menu, theme } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import {
  FundOutlined,
  BookOutlined,
  SmileOutlined,
  WalletOutlined,
  DollarOutlined,
  RobotOutlined,
} from '@ant-design/icons';
import type { MenuProps } from 'antd';

import FinancialPlanning from './pages/FinancialPlanning';
import InvestmentDiary from './pages/InvestmentDiary';
import PsychologyAssessment from './pages/PsychologyAssessment';
import AssetsOverview from './pages/AssetsOverview';
import PassiveIncome from './pages/PassiveIncome';
import AIChat from './pages/AIChat';

const { Header, Sider, Content } = Layout;

type MenuItem = Required<MenuProps>['items'][number];

const menuItems: MenuItem[] = [
  {
    key: '/planning',
    icon: <FundOutlined />,
    label: '财务自由规划',
  },
  {
    key: '/diary',
    icon: <BookOutlined />,
    label: '投资日记',
  },
  {
    key: '/psychology',
    icon: <SmileOutlined />,
    label: '心理诊断',
  },
  {
    key: '/assets',
    icon: <WalletOutlined />,
    label: '资产视图',
  },
  {
    key: '/passive-income',
    icon: <DollarOutlined />,
    label: '被动收入',
  },
  {
    key: '/chat',
    icon: <RobotOutlined />,
    label: 'AI 对话',
  },
];

const App: React.FC = () => {
  const [collapsed, setCollapsed] = React.useState(false);

  return (
    <ConfigProvider locale={zhCN} theme={{ algorithm: theme.defaultAlgorithm }}>
      <BrowserRouter>
        <Layout style={{ minHeight: '100vh' }}>
          <Sider collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)}>
            <div className="h-16 flex items-center justify-center">
              <h1 className={`text-white font-bold ${collapsed ? 'text-lg' : 'text-xl'}`}>
                {collapsed ? '💰' : '财务自由助手'}
              </h1>
            </div>
            <Menu
              theme="dark"
              mode="inline"
              defaultSelectedKeys={['/planning']}
              items={menuItems}
              onClick={({ key }) => {
                window.location.href = key;
              }}
            />
          </Sider>
          <Layout>
            <Header style={{ padding: '0 24px', background: '#fff' }}>
              <h2 className="text-xl font-semibold m-0">财务自由管理系统</h2>
            </Header>
            <Content style={{ margin: '24px 16px', padding: 24, background: '#fff' }}>
              <Routes>
                <Route path="/" element={<Navigate to="/planning" replace />} />
                <Route path="/planning" element={<FinancialPlanning />} />
                <Route path="/diary" element={<InvestmentDiary />} />
                <Route path="/psychology" element={<PsychologyAssessment />} />
                <Route path="/assets" element={<AssetsOverview />} />
                <Route path="/passive-income" element={<PassiveIncome />} />
                <Route path="/chat" element={<AIChat />} />
              </Routes>
            </Content>
          </Layout>
        </Layout>
      </BrowserRouter>
    </ConfigProvider>
  );
};

export default App;
