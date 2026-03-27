import React from 'react';
import { Card, Row, Col, Progress, Statistic, Button, Form, InputNumber, Select } from 'antd';
import { DollarOutlined, RiseOutlined, AimOutlined } from '@ant-design/icons';

const { Option } = Select;

const FinancialPlanning: React.FC = () => {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">财务自由规划</h1>
      
      {/* 核心指标卡片 */}
      <Row gutter={16} className="mb-6">
        <Col span={8}>
          <Card>
            <Statistic
              title="财务自由进度"
              value={45}
              suffix="%"
              prefix={<AimOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
            <Progress percent={45} className="mt-4" />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="当前净资产"
              value={1250000}
              prefix={<DollarOutlined />}
              precision={2}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="被动收入占比"
              value={32}
              suffix="%"
              prefix={<RiseOutlined />}
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>
      </Row>

      {/* 规划计算器 */}
      <Card title="财务自由计算器" className="mb-6">
        <Form layout="inline">
          <Form.Item label="当前年龄">
            <InputNumber defaultValue={30} />
          </Form.Item>
          <Form.Item label="退休年龄">
            <InputNumber defaultValue={60} />
          </Form.Item>
          <Form.Item label="目标资产">
            <InputNumber defaultValue={5000000} formatter={(value) => `¥ ${value}`} />
          </Form.Item>
          <Form.Item label="预期年化收益率">
            <Select defaultValue="8" style={{ width: 120 }}>
              <Option value="5">5%</Option>
              <Option value="8">8%</Option>
              <Option value="10">10%</Option>
              <Option value="12">12%</Option>
            </Select>
          </Form.Item>
          <Form.Item>
            <Button type="primary">计算</Button>
          </Form.Item>
        </Form>
      </Card>

      {/* 里程碑 */}
      <Card title="财务自由里程碑">
        <Row gutter={16}>
          <Col span={6}>
            <Card size="small" className="text-center">
              <div className="text-3xl mb-2">🎯</div>
              <div className="font-bold">应急基金</div>
              <div className="text-green-500">已完成</div>
            </Card>
          </Col>
          <Col span={6}>
            <Card size="small" className="text-center">
              <div className="text-3xl mb-2">💰</div>
              <div className="font-bold">首套房</div>
              <div className="text-green-500">已完成</div>
            </Card>
          </Col>
          <Col span={6}>
            <Card size="small" className="text-center">
              <div className="text-3xl mb-2">📈</div>
              <div className="font-bold">100 万资产</div>
              <div className="text-blue-500">进行中</div>
            </Card>
          </Col>
          <Col span={6}>
            <Card size="small" className="text-center">
              <div className="text-3xl mb-2">🏆</div>
              <div className="font-bold">财务自由</div>
              <div className="text-gray-400">未开始</div>
            </Card>
          </Col>
        </Row>
      </Card>
    </div>
  );
};

export default FinancialPlanning;
