import React from 'react';
import { Card, Row, Col, Table, Progress, Statistic, Tag, Button } from 'antd';
import { PlusOutlined, RiseOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';

interface IncomeStream {
  key: string;
  name: string;
  type: string;
  monthly: number;
  annual: number;
  growth: number;
  status: string;
}

const PassiveIncome: React.FC = () => {
  const columns: ColumnsType<IncomeStream> = [
    {
      title: '收入来源',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
      render: (type: string) => {
        const colorMap: Record<string, string> = {
          '股息': 'blue',
          '房租': 'green',
          '利息': 'gold',
          '版权': 'purple',
          '其他': 'default',
        };
        return <Tag color={colorMap[type] || 'default'}>{type}</Tag>;
      },
    },
    {
      title: '月收入',
      dataIndex: 'monthly',
      key: 'monthly',
      render: (monthly: number) => `¥${monthly.toFixed(2)}`,
    },
    {
      title: '年收入',
      dataIndex: 'annual',
      key: 'annual',
      render: (annual: number) => `¥${(annual / 10000).toFixed(2)}万`,
    },
    {
      title: '增长率',
      dataIndex: 'growth',
      key: 'growth',
      render: (growth: number) => (
        <span style={{ color: growth >= 0 ? '#52c41a' : '#ff4d4f' }}>
          <RiseOutlined rotate={growth < 0 ? 180 : 0} /> {growth.toFixed(1)}%
        </span>
      ),
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        const color = status === '稳定' ? 'green' : status === '增长' ? 'blue' : 'orange';
        return <Tag color={color}>{status}</Tag>;
      },
    },
  ];

  const data: IncomeStream[] = [
    { key: '1', name: '贵州茅台股息', type: '股息', monthly: 2800, annual: 33600, growth: 12.5, status: '增长' },
    { key: '2', name: '腾讯控股股息', type: '股息', monthly: 1600, annual: 19200, growth: 8.3, status: '增长' },
    { key: '3', name: '北京房产租金', type: '房租', monthly: 8500, annual: 102000, growth: 3.2, status: '稳定' },
    { key: '4', name: '银行理财利息', type: '利息', monthly: 980, annual: 11760, growth: -2.1, status: '下降' },
    { key: '5', name: '技术文章版权', type: '版权', monthly: 450, annual: 5400, growth: 25.0, status: '增长' },
  ];

  const totalMonthly = 14330;
  const totalAnnual = 171960;
  const targetMonthly = 30000;
  const progress = (totalMonthly / targetMonthly) * 100;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">被动收入</h1>
        <Button type="primary" icon={<PlusOutlined />}>
          添加收入来源
        </Button>
      </div>

      {/* 核心指标 */}
      <Row gutter={16} className="mb-6">
        <Col span={6}>
          <Card>
            <Statistic
              title="月被动收入"
              value={totalMonthly}
              prefix="¥"
              precision={2}
              valueStyle={{ color: '#52c41a' }}
            />
            <div className="mt-4">
              <div className="text-sm text-gray-500 mb-2">财务自由进度</div>
              <Progress percent={Math.round(progress)} strokeColor="#52c41a" />
              <div className="text-xs text-gray-400 mt-1">目标：¥{targetMonthly}/月</div>
            </div>
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="年被动收入"
              value={totalAnnual}
              prefix="¥"
              precision={2}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="收入来源数"
              value={5}
              suffix="个"
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="平均增长率"
              value={9.38}
              suffix="%"
              prefix={<RiseOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
      </Row>

      {/* 收入结构 */}
      <Row gutter={16} className="mb-6">
        <Col span={12}>
          <Card title="收入结构">
            <div className="space-y-4">
              <div>
                <div className="flex justify-between mb-1">
                  <span>股息收入</span>
                  <span>¥4,400/月 (30.7%)</span>
                </div>
                <Progress percent={30.7} strokeColor="#1890ff" size="small" />
              </div>
              <div>
                <div className="flex justify-between mb-1">
                  <span>房租收入</span>
                  <span>¥8,500/月 (59.3%)</span>
                </div>
                <Progress percent={59.3} strokeColor="#52c41a" size="small" />
              </div>
              <div>
                <div className="flex justify-between mb-1">
                  <span>利息收入</span>
                  <span>¥980/月 (6.8%)</span>
                </div>
                <Progress percent={6.8} strokeColor="#faad14" size="small" />
              </div>
              <div>
                <div className="flex justify-between mb-1">
                  <span>版权收入</span>
                  <span>¥450/月 (3.1%)</span>
                </div>
                <Progress percent={3.1} strokeColor="#722ed1" size="small" />
              </div>
            </div>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="增长趋势">
            <div className="h-48 flex items-center justify-center bg-gray-100 rounded">
              <p className="text-gray-500">折线图 - 显示月度被动收入增长趋势</p>
            </div>
          </Card>
        </Col>
      </Row>

      {/* 收入明细表 */}
      <Card title="收入来源明细">
        <Table columns={columns} dataSource={data} pagination={false} />
      </Card>
    </div>
  );
};

export default PassiveIncome;
