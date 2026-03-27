# API 规范文档

**规范**: OpenAPI 3.0.3  
**基础路径**: `/api/v1`  
**认证方式**: JWT Bearer Token

---

## 1. 认证模块 (Authentication)

### 1.1 用户注册

```yaml
post /auth/register:
  summary: 用户注册
  tags: [Authentication]
  requestBody:
    required: true
    content:
      application/json:
        schema:
          type: object
          required: [email, username, password]
          properties:
            email:
              type: string
              format: email
            username:
              type: string
              minLength: 3
              maxLength: 50
            password:
              type: string
              minLength: 8
            full_name:
              type: string
  responses:
    '201':
      description: 注册成功
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/User'
    '400':
      description: 请求参数错误
    '409':
      description: 邮箱或用户名已存在
```

### 1.2 用户登录

```yaml
post /auth/login:
  summary: 用户登录
  tags: [Authentication]
  requestBody:
    required: true
    content:
      application/json:
        schema:
          type: object
          required: [email, password]
          properties:
            email:
              type: string
              format: email
            password:
              type: string
  responses:
    '200':
      description: 登录成功
      content:
        application/json:
          schema:
            type: object
            properties:
              access_token:
                type: string
              refresh_token:
                type: string
              token_type:
                type: string
                enum: [Bearer]
              expires_in:
                type: integer
    '401':
      description: 凭证错误
```

### 1.3 刷新 Token

```yaml
post /auth/refresh:
  summary: 刷新访问令牌
  tags: [Authentication]
  security:
    - refresh_token: []
  responses:
    '200':
      description: 刷新成功
      content:
        application/json:
          schema:
            type: object
            properties:
              access_token:
                type: string
              expires_in:
                type: integer
```

### 1.4 获取当前用户

```yaml
get /auth/me:
  summary: 获取当前登录用户信息
  tags: [Authentication]
  security:
    - bearerAuth: []
  responses:
    '200':
      description: 成功
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/User'
    '401':
      description: 未授权
```

---

## 2. 资产管理模块 (Assets)

### 2.1 获取资产列表

```yaml
get /assets:
  summary: 获取用户资产列表
  tags: [Assets]
  security:
    - bearerAuth: []
  parameters:
    - name: asset_type
      in: query
      schema:
        type: string
        enum: [STOCK, FUND, CASH, CRYPTO, OTHER]
    - name: is_active
      in: query
      schema:
        type: boolean
        default: true
    - name: page
      in: query
      schema:
        type: integer
        default: 1
    - name: page_size
      in: query
      schema:
        type: integer
        default: 20
  responses:
    '200':
      description: 成功
      content:
        application/json:
          schema:
            type: object
            properties:
              items:
                type: array
                items:
                  $ref: '#/components/schemas/Asset'
              total:
                type: integer
              page:
                type: integer
              page_size:
                type: integer
```

### 2.2 创建资产

```yaml
post /assets:
  summary: 添加新资产
  tags: [Assets]
  security:
    - bearerAuth: []
  requestBody:
    required: true
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/AssetCreate'
  responses:
    '201':
      description: 创建成功
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Asset'
    '400':
      description: 请求参数错误
    '409':
      description: 资产已存在
```

### 2.3 获取资产详情

```yaml
get /assets/{asset_id}:
  summary: 获取资产详情
  tags: [Assets]
  security:
    - bearerAuth: []
  parameters:
    - name: asset_id
      in: path
      required: true
      schema:
        type: string
        format: uuid
  responses:
    '200':
      description: 成功
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Asset'
    '404':
      description: 资产不存在
```

### 2.4 更新资产

```yaml
put /assets/{asset_id}:
  summary: 更新资产信息
  tags: [Assets]
  security:
    - bearerAuth: []
  parameters:
    - name: asset_id
      in: path
      required: true
      schema:
        type: string
        format: uuid
  requestBody:
    required: true
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/AssetUpdate'
  responses:
    '200':
      description: 更新成功
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Asset'
    '404':
      description: 资产不存在
```

### 2.5 删除资产

```yaml
delete /assets/{asset_id}:
  summary: 删除资产（软删除）
  tags: [Assets]
  security:
    - bearerAuth: []
  parameters:
    - name: asset_id
      in: path
      required: true
      schema:
        type: string
        format: uuid
  responses:
    '204':
      description: 删除成功
    '404':
      description: 资产不存在
```

### 2.6 同步资产价格

```yaml
post /assets/{asset_id}/sync:
  summary: 同步资产最新价格
  tags: [Assets]
  security:
    - bearerAuth: []
  parameters:
    - name: asset_id
      in: path
      required: true
      schema:
        type: string
        format: uuid
  responses:
    '200':
      description: 同步成功
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Asset'
    '404':
      description: 资产不存在
```

---

## 3. 交易记录模块 (Transactions)

### 3.1 获取交易列表

```yaml
get /transactions:
  summary: 获取交易记录列表
  tags: [Transactions]
  security:
    - bearerAuth: []
  parameters:
    - name: asset_id
      in: query
      schema:
        type: string
        format: uuid
    - name: tx_type
      in: query
      schema:
        type: string
        enum: [BUY, SELL, DIVIDEND, TRANSFER, FEE]
    - name: start_date
      in: query
      schema:
        type: string
        format: date
    - name: end_date
      in: query
      schema:
        type: string
        format: date
    - name: page
      in: query
      schema:
        type: integer
        default: 1
    - name: page_size
      in: query
      schema:
        type: integer
        default: 20
  responses:
    '200':
      description: 成功
      content:
        application/json:
          schema:
            type: object
            properties:
              items:
                type: array
                items:
                  $ref: '#/components/schemas/Transaction'
              total:
                type: integer
```

### 3.2 创建交易记录

```yaml
post /transactions:
  summary: 添加交易记录
  tags: [Transactions]
  security:
    - bearerAuth: []
  requestBody:
    required: true
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/TransactionCreate'
  responses:
    '201':
      description: 创建成功
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Transaction'
    '400':
      description: 请求参数错误
```

### 3.3 获取交易详情

```yaml
get /transactions/{tx_id}:
  summary: 获取交易详情
  tags: [Transactions]
  security:
    - bearerAuth: []
  parameters:
    - name: tx_id
      in: path
      required: true
      schema:
        type: string
        format: uuid
  responses:
    '200':
      description: 成功
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Transaction'
    '404':
      description: 交易不存在
```

### 3.4 更新交易记录

```yaml
put /transactions/{tx_id}:
  summary: 更新交易记录
  tags: [Transactions]
  security:
    - bearerAuth: []
  parameters:
    - name: tx_id
      in: path
      required: true
      schema:
        type: string
        format: uuid
  requestBody:
    required: true
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/TransactionUpdate'
  responses:
    '200':
      description: 更新成功
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Transaction'
    '404':
      description: 交易不存在
```

### 3.5 删除交易记录

```yaml
delete /transactions/{tx_id}:
  summary: 删除交易记录
  tags: [Transactions]
  security:
    - bearerAuth: []
  parameters:
    - name: tx_id
      in: path
      required: true
      schema:
        type: string
        format: uuid
  responses:
    '204':
      description: 删除成功
    '404':
      description: 交易不存在
```

---

## 4. 投资日记模块 (Diaries)

### 4.1 获取日记列表

```yaml
get /diaries:
  summary: 获取投资日记列表
  tags: [Diaries]
  security:
    - bearerAuth: []
  parameters:
    - name: diary_type
      in: query
      schema:
        type: string
        enum: [REFLECTION, ANALYSIS, PLAN, SUMMARY]
    - name: tags
      in: query
      schema:
        type: array
        items:
          type: string
    - name: start_date
      in: query
      schema:
        type: string
        format: date
    - name: end_date
      in: query
      schema:
        type: string
        format: date
    - name: page
      in: query
      schema:
        type: integer
        default: 1
    - name: page_size
      in: query
      schema:
        type: integer
        default: 20
  responses:
    '200':
      description: 成功
      content:
        application/json:
          schema:
            type: object
            properties:
              items:
                type: array
                items:
                  $ref: '#/components/schemas/Diary'
              total:
                type: integer
```

### 4.2 创建日记

```yaml
post /diaries:
  summary: 创建投资日记
  tags: [Diaries]
  security:
    - bearerAuth: []
  requestBody:
    required: true
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/DiaryCreate'
  responses:
    '201':
      description: 创建成功
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Diary'
    '400':
      description: 请求参数错误
```

### 4.3 获取日记详情

```yaml
get /diaries/{diary_id}:
  summary: 获取日记详情
  tags: [Diaries]
  security:
    - bearerAuth: []
  parameters:
    - name: diary_id
      in: path
      required: true
      schema:
        type: string
        format: uuid
  responses:
    '200':
      description: 成功
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Diary'
    '404':
      description: 日记不存在
```

### 4.4 更新日记

```yaml
put /diaries/{diary_id}:
  summary: 更新日记
  tags: [Diaries]
  security:
    - bearerAuth: []
  parameters:
    - name: diary_id
      in: path
      required: true
      schema:
        type: string
        format: uuid
  requestBody:
    required: true
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/DiaryUpdate'
  responses:
    '200':
      description: 更新成功
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Diary'
    '404':
      description: 日记不存在
```

### 4.5 删除日记

```yaml
delete /diaries/{diary_id}:
  summary: 删除日记
  tags: [Diaries]
  security:
    - bearerAuth: []
  parameters:
    - name: diary_id
      in: path
      required: true
      schema:
        type: string
        format: uuid
  responses:
    '204':
      description: 删除成功
    '404':
      description: 日记不存在
```

---

## 5. 分析统计模块 (Analytics)

### 5.1 获取投资组合概览

```yaml
get /analytics/portfolio:
  summary: 获取投资组合概览
  tags: [Analytics]
  security:
    - bearerAuth: []
  responses:
    '200':
      description: 成功
      content:
        application/json:
          schema:
            type: object
            properties:
              total_market_value:
                type: number
              total_cost:
                type: number
              total_pnl:
                type: number
              total_pnl_pct:
                type: number
              asset_allocation:
                type: object
                properties:
                  STOCK:
                    type: number
                  FUND:
                    type: number
                  CASH:
                    type: number
                  CRYPTO:
                    type: number
              top_holdings:
                type: array
                items:
                  $ref: '#/components/schemas/Asset'
```

### 5.2 获取收益趋势

```yaml
get /analytics/performance:
  summary: 获取收益趋势数据
  tags: [Analytics]
  security:
    - bearerAuth: []
  parameters:
    - name: period
      in: query
      schema:
        type: string
        enum: [7D, 1M, 3M, 6M, 1Y, ALL]
        default: 1Y
  responses:
    '200':
      description: 成功
      content:
        application/json:
          schema:
            type: object
            properties:
              labels:
                type: array
                items:
                  type: string
              portfolio_value:
                type: array
                items:
                  type: number
              benchmark_value:
                type: array
                items:
                  type: number
```

### 5.3 获取交易统计

```yaml
get /analytics/trading-stats:
  summary: 获取交易统计数据
  tags: [Analytics]
  security:
    - bearerAuth: []
  parameters:
    - name: start_date
      in: query
      schema:
        type: string
        format: date
    - name: end_date
      in: query
      schema:
        type: string
        format: date
  responses:
    '200':
      description: 成功
      content:
        application/json:
          schema:
            type: object
            properties:
              total_trades:
                type: integer
              buy_count:
                type: integer
              sell_count:
                type: integer
              total_fees:
                type: number
              win_rate:
                type: number
              avg_profit:
                type: number
              avg_loss:
                type: number
```

---

## 6. 系统模块 (System)

### 6.1 健康检查

```yaml
get /health:
  summary: 健康检查
  tags: [System]
  responses:
    '200':
      description: 服务正常
      content:
        application/json:
          schema:
            type: object
            properties:
              status:
                type: string
                enum: [healthy, unhealthy]
              version:
                type: string
              database:
                type: string
              uptime:
                type: integer
```

### 6.2 获取 API 版本

```yaml
get /version:
  summary: 获取 API 版本信息
  tags: [System]
  responses:
    '200':
      description: 成功
      content:
        application/json:
          schema:
            type: object
            properties:
              version:
                type: string
              build_date:
                type: string
              git_commit:
                type: string
```

---

## 组件 Schemas

```yaml
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        username:
          type: string
        full_name:
          type: string
        avatar_url:
          type: string
        base_currency:
          type: string
        is_active:
          type: boolean
        created_at:
          type: string
          format: date-time

    Asset:
      type: object
      properties:
        id:
          type: string
          format: uuid
        user_id:
          type: string
          format: uuid
        asset_type:
          type: string
          enum: [STOCK, FUND, CASH, CRYPTO, OTHER]
        symbol:
          type: string
        name:
          type: string
        market:
          type: string
        quantity:
          type: number
        avg_cost:
          type: number
        current_price:
          type: number
        market_value:
          type: number
        unrealized_pnl:
          type: number
        unrealized_pnl_pct:
          type: number
        realized_pnl:
          type: number
        is_active:
          type: boolean
        created_at:
          type: string
          format: date-time

    AssetCreate:
      type: object
      required: [asset_type, symbol, name]
      properties:
        asset_type:
          type: string
          enum: [STOCK, FUND, CASH, CRYPTO, OTHER]
        symbol:
          type: string
        name:
          type: string
        market:
          type: string
        quantity:
          type: number
          default: 0
        avg_cost:
          type: number
          default: 0

    AssetUpdate:
      type: object
      properties:
        name:
          type: string
        quantity:
          type: number
        avg_cost:
          type: number
        is_hidden:
          type: boolean

    Transaction:
      type: object
      properties:
        id:
          type: string
          format: uuid
        user_id:
          type: string
          format: uuid
        asset_id:
          type: string
          format: uuid
        tx_type:
          type: string
          enum: [BUY, SELL, DIVIDEND, TRANSFER, FEE]
        tx_date:
          type: string
          format: date
        quantity:
          type: number
        price:
          type: number
        amount:
          type: number
        fee:
          type: number
        currency:
          type: string
        broker:
          type: string
        order_id:
          type: string
        notes:
          type: string
        created_at:
          type: string
          format: date-time

    TransactionCreate:
      type: object
      required: [asset_id, tx_type, tx_date, quantity, price, amount]
      properties:
        asset_id:
          type: string
          format: uuid
        tx_type:
          type: string
          enum: [BUY, SELL, DIVIDEND, TRANSFER, FEE]
        tx_date:
          type: string
          format: date
        tx_time:
          type: string
          format: time
        quantity:
          type: number
        price:
          type: number
        amount:
          type: number
        fee:
          type: number
          default: 0
        currency:
          type: string
          default: CNY
        broker:
          type: string
        order_id:
          type: string
        notes:
          type: string

    TransactionUpdate:
      type: object
      properties:
        quantity:
          type: number
        price:
          type: number
        amount:
          type: number
        fee:
          type: number
        notes:
          type: string

    Diary:
      type: object
      properties:
        id:
          type: string
          format: uuid
        user_id:
          type: string
          format: uuid
        title:
          type: string
        content:
          type: string
        diary_type:
          type: string
          enum: [REFLECTION, ANALYSIS, PLAN, SUMMARY]
        related_assets:
          type: array
          items:
            type: string
            format: uuid
        tags:
          type: array
          items:
            type: string
        sentiment:
          type: string
          enum: [POSITIVE, NEUTRAL, NEGATIVE]
        confidence_score:
          type: integer
          minimum: 1
          maximum: 10
        is_private:
          type: boolean
        is_pinned:
          type: boolean
        diary_date:
          type: string
          format: date
        created_at:
          type: string
          format: date-time

    DiaryCreate:
      type: object
      required: [title, content]
      properties:
        title:
          type: string
        content:
          type: string
        diary_type:
          type: string
          enum: [REFLECTION, ANALYSIS, PLAN, SUMMARY]
        related_assets:
          type: array
          items:
            type: string
            format: uuid
        tags:
          type: array
          items:
            type: string
        sentiment:
          type: string
        confidence_score:
          type: integer
        is_private:
          type: boolean
          default: true

    DiaryUpdate:
      type: object
      properties:
        title:
          type: string
        content:
          type: string
        diary_type:
          type: string
        tags:
          type: array
          items:
            type: string
        sentiment:
          type: string
        confidence_score:
          type: integer
        is_pinned:
          type: boolean

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
    refresh_token:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

---

## 错误响应格式

```yaml
Error:
  type: object
  properties:
    error:
      type: object
      properties:
        code:
          type: string
        message:
          type: string
        details:
          type: object
```

### 常见错误码

| 错误码 | 说明 |
|--------|------|
| `INVALID_REQUEST` | 请求参数错误 |
| `UNAUTHORIZED` | 未授权 |
| `FORBIDDEN` | 禁止访问 |
| `NOT_FOUND` | 资源不存在 |
| `CONFLICT` | 资源冲突 |
| `INTERNAL_ERROR` | 服务器内部错误 |

---

## 分页格式

所有列表接口统一使用以下分页格式：

```json
{
  "items": [],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "total_pages": 5
}
```
