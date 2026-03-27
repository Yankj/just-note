import React, { useState } from 'react';
import { Card, Table, Button, Tag, Modal, Form, Input, DatePicker, Select, Space, Row, Col, InputNumber } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';

interface DiaryEntry {
  key: string;
  date: string;
  type: string;
  stock: string;
  action: string;
  price: number;
  amount: number;
  reason: string;
  emotion: string;
}

const InvestmentDiary: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [form] = Form.useForm();

  const columns: ColumnsType<DiaryEntry> = [
    {
      title: '日期',
      dataIndex: 'date',
      key: 'date',
      width: 120,
    },
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
      width: 100,
      render: (type: string) => {
        const color = type === '买入' ? 'green' : type === '卖出' ? 'red' : 'blue';
        return <Tag color={color}>{type}</Tag>;
      },
    },
    {
      title: '股票',
      dataIndex: 'stock',
      key: 'stock',
      width: 120,
    },
    {
      title: '操作',
      dataIndex: 'action',
      key: 'action',
      width: 100,
    },
    {
      title: '价格',
      dataIndex: 'price',
      key: 'price',
      width: 100,
      render: (price: number) => `¥${price.toFixed(2)}`,
    },
    {
      title: '数量',
      dataIndex: 'amount',
      key: 'amount',
      width: 100,
    },
    {
      title: '情绪',
      dataIndex: 'emotion',
      key: 'emotion',
      width: 100,
      render: (emotion: string) => {
        const color = emotion === '贪婪' ? 'red' : emotion === '恐惧' ? 'orange' : 'default';
        return <Tag color={color}>{emotion}</Tag>;
      },
    },
    {
      title: '原因',
      dataIndex: 'reason',
      key: 'reason',
      ellipsis: true,
    },
    {
      title: '操作',
      key: 'action',
      width: 100,
      render: () => (
        <Space size="small">
          <Button type="link" icon={<EditOutlined />} />
          <Button type="link" danger icon={<DeleteOutlined />} />
        </Space>
      ),
    },
  ];

  const data: DiaryEntry[] = [
    {
      key: '1',
      date: '2024-03-19',
      type: '买入',
      stock: '600519',
      action: '建仓',
      price: 1678.50,
      amount: 100,
      reason: '估值合理，长期看好',
      emotion: '冷静',
    },
    {
      key: '2',
      date: '2024-03-18',
      type: '卖出',
      stock: '00700',
      action: '止盈',
      price: 320.40,
      amount: 200,
      reason: '达到目标价位',
      emotion: '满足',
    },
  ];

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">投资日记</h1>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => setIsModalOpen(true)}>
          记录交易
        </Button>
      </div>

      <Card>
        <Table columns={columns} dataSource={data} pagination={{ pageSize: 10 }} />
      </Card>

      <Modal
        title="记录交易"
        open={isModalOpen}
        onOk={() => {
          form.submit();
          setIsModalOpen(false);
        }}
        onCancel={() => setIsModalOpen(false)}
        width={600}
      >
        <Form form={form} layout="vertical">
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="date" label="日期" rules={[{ required: true }]}>
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="type" label="类型" rules={[{ required: true }]}>
                <Select>
                  <Select.Option value="买入">买入</Select.Option>
                  <Select.Option value="卖出">卖出</Select.Option>
                  <Select.Option value="观察">观察</Select.Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="stock" label="股票代码" rules={[{ required: true }]}>
                <Input placeholder="如：600519" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="action" label="操作" rules={[{ required: true }]}>
                <Select>
                  <Select.Option value="建仓">建仓</Select.Option>
                  <Select.Option value="加仓">加仓</Select.Option>
                  <Select.Option value="减仓">减仓</Select.Option>
                  <Select.Option value="清仓">清仓</Select.Option>
                  <Select.Option value="止盈">止盈</Select.Option>
                  <Select.Option value="止损">止损</Select.Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="price" label="价格" rules={[{ required: true }]}>
                <InputNumber style={{ width: '100%' }} prefix="¥" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="amount" label="数量" rules={[{ required: true }]}>
                <InputNumber style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>
          <Form.Item name="reason" label="交易原因">
            <Input.TextArea rows={3} placeholder="记录你的交易逻辑..." />
          </Form.Item>
          <Form.Item name="emotion" label="当时情绪">
            <Select>
              <Select.Option value="冷静">冷静</Select.Option>
              <Select.Option value="贪婪">贪婪</Select.Option>
              <Select.Option value="恐惧">恐惧</Select.Option>
              <Select.Option value="兴奋">兴奋</Select.Option>
              <Select.Option value="焦虑">焦虑</Select.Option>
              <Select.Option value="满足">满足</Select.Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default InvestmentDiary;
