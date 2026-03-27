import React, { useState } from 'react';
import { Card, Row, Col, Progress, Button, Form, Radio, Space, Result } from 'antd';
import { SmileOutlined } from '@ant-design/icons';

const PsychologyAssessment: React.FC = () => {
  const [showResult, setShowResult] = useState(false);
  const [form] = Form.useForm();

  const questions = [
    { id: 1, text: '当持仓下跌 10% 时，我会感到焦虑并考虑卖出' },
    { id: 2, text: '我经常因为害怕错过机会而追高买入' },
    { id: 3, text: '我会因为一次成功交易而过度自信' },
    { id: 4, text: '亏损后我会急于翻本，增加交易频率' },
    { id: 5, text: '我能严格执行止损纪律' },
    { id: 6, text: '我会因为市场噪音而改变原有计划' },
    { id: 7, text: '我能客观分析自己的交易错误' },
    { id: 8, text: '持仓波动会影响我的睡眠和心情' },
  ];

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">交易心理诊断</h1>

      {!showResult ? (
        <Card title="心理状态评估问卷">
          <Form form={form} layout="vertical">
            {questions.map((q, index) => (
              <Form.Item
                key={q.id}
                name={`q${q.id}`}
                label={`${index + 1}. ${q.text}`}
                rules={[{ required: true, message: '请选择' }]}
              >
                <Radio.Group>
                  <Radio value={1}>非常不同意</Radio>
                  <Radio value={2}>不同意</Radio>
                  <Radio value={3}>中立</Radio>
                  <Radio value={4}>同意</Radio>
                  <Radio value={5}>非常同意</Radio>
                </Radio.Group>
              </Form.Item>
            ))}
            <Form.Item>
              <Space>
                <Button type="primary" htmlType="submit" onClick={() => setShowResult(true)}>
                  提交评估
                </Button>
                <Button htmlType="reset">重置</Button>
              </Space>
            </Form.Item>
          </Form>
        </Card>
      ) : (
        <>
          <Row gutter={16} className="mb-6">
            <Col span={8}>
              <Card>
                <Result
                  icon={<SmileOutlined style={{ color: '#52c41a' }} />}
                  title="心理评分：72 分"
                  subTitle="整体状态良好，情绪管理有待提升"
                  status="success"
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card title="贪婪指数">
                <Progress percent={65} strokeColor={{ '0%': '#52c41a', '100%': '#faad14' }} />
                <div className="text-center mt-2">
                  {65 < 50 ? '😌 冷静' : 65 < 80 ? '😐 适度' : '😰 警惕'}
                </div>
              </Card>
            </Col>
            <Col span={8}>
              <Card title="恐惧指数">
                <Progress percent={45} strokeColor={{ '0%': '#1890ff', '100%': '#ff4d4f' }} />
                <div className="text-center mt-2">
                  {45 < 50 ? '😌 冷静' : 45 < 80 ? '😐 适度' : '😰 警惕'}
                </div>
              </Card>
            </Col>
          </Row>

          <Card title="心理维度分析" className="mb-6">
            <div className="h-64 flex items-center justify-center bg-gray-100 rounded">
              <p className="text-gray-500">雷达图组件 - 显示五维心理指标</p>
            </div>
          </Card>

          <Card title="改进建议">
            <ul className="list-disc list-inside space-y-2">
              <li><strong>情绪管理：</strong>建议建立交易前冷静仪式，避免情绪化交易</li>
              <li><strong>纪律性：</strong>保持优秀的止损纪律，继续严格执行交易计划</li>
              <li><strong>客观性：</strong>定期复盘交易记录，减少主观偏见</li>
              <li><strong>建议练习：</strong>每天记录交易情绪日记，提升自我觉察</li>
            </ul>
          </Card>
        </>
      )}
    </div>
  );
};

export default PsychologyAssessment;
