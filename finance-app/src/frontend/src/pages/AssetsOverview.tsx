import React from 'react';
import { Card, Row, Col, Table, Progress, Tag, Statistic, Tree } from 'antd';
import type { ColumnsType } from 'antd/es/table';

interface AssetItem {
  key: string;
  name: string;
  category: string;
  value: number;
  change: number;
  percent: number;
}

const AssetsOverview: React.FC = () => {
  const columns: ColumnsType<AssetItem> = [
    {
      title: '资产名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '类别',
      dataIndex: 'category',
      key: 'category',
      render: (category: string) => {
        const colorMap: Record<string, string> = {
          '房产': 'blue',
          '股票': 'green',
          '基金': 'cyan',
          '现金': 'gold',
          '其他': 'default',
        };
        return <Tag color={colorMap[category] || 'default'}>{category}</Tag>;
      },
    },
    {
      title: '当前价值',
      dataIndex: 'value',
      key: 'value',
      render: (value: number) => `¥${(value / 10000).toFixed(2)}万`,
    },
    {
      title: '占比',
      dataIndex: 'percent',
      key: 'percent',
      render: (percent: number) => <Progress percent={percent} size="small" />,
    },
    {
      title: '今日涨跌',
      dataIndex: 'change',
      key: 'change',
      render: (change: number, record: AssetItem) => (
        <span style={{ color: change >= 0 ? '#52c41a' : '#ff4d4f' }}>
          {change >= 0 ? '+' : ''}{change.toFixed(2)} ({record.percent >= 0 ? '+' : ''}{record.percent.toFixed(2)}%)
        </span>
      ),
    },
  ];

  const data: AssetItem[] = [
    { key: '1', name: '贵州茅台', category: '股票', value: 335700, change: 2340, percent: 26.8 },
    { key: '2', name: '腾讯控股', category: '股票', value: 256000, change: -1280, percent: 20.5 },
    { key: '3', name: '沪深 300ETF', category: '基金', value: 180000, change: 540, percent: 14.4 },
    { key: '4', name: '北京房产', category: '房产', value: 4500000, change: 0, percent: 36.0 },
    { key: '5', name: '银行存款', category: '现金', value: 280000, change: 35, percent: 2.2 },
  ];

  const totalAssets = 5551700;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">资产视图</h1>

      {/* 总资产概览 */}
      <Row gutter={16} className="mb-6">
        <Col span={6}>
          <Card>
            <Statistic
              title="总资产"
              value={totalAssets}
              prefix="¥"
              precision={2}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="今日盈亏"
              value={1635}
              prefix="¥"
              precision={2}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="本月收益"
              value={45280}
              prefix="¥"
              precision={2}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="本年收益"
              value={186500}
              prefix="¥"
              precision={2}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
      </Row>

      {/* 资产配置饼图占位 */}
      <Row gutter={16} className="mb-6">
        <Col span={12}>
          <Card title="资产配置">
            <div className="h-64 flex items-center justify-center bg-gray-100 rounded">
              <p className="text-gray-500">饼图 - 显示各类资产占比</p>
            </div>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="资产分类">
            <Tree
              treeData={[
                {
                  title: '📈 金融资产 ¥5,271,700',
                  key: '1',
                  children: [
                    { title: '🏠 房产 ¥4,500,000 (81.0%)', key: '1-1' },
                    {
                      title: '💹 股票 ¥591,700 (10.7%)',
                      key: '1-2',
                      children: [
                        { title: '贵州茅台 ¥335,700', key: '1-2-1' },
                        { title: '腾讯控股 ¥256,000', key: '1-2-2' },
                      ],
                    },
                    { title: '📊 基金 ¥180,000 (3.2%)', key: '1-3' },
                    { title: '💰 现金 ¥280,000 (5.0%)', key: '1-4' },
                  ],
                },
              ]}
            />
          </Card>
        </Col>
      </Row>

      {/* 资产明细表 */}
      <Card title="资产明细">
        <Table columns={columns} dataSource={data} pagination={false} />
      </Card>
    </div>
  );
};

export default AssetsOverview;
