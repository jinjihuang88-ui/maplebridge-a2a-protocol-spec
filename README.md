# MapleBridge.io — A2A Protocol Specification
# MapleBridge.io — 智能供需匹配协议规范

> **AI-powered B2B matching between Canadian buyers and Chinese suppliers**
> **加拿大买家与中国供应商的 AI 智能匹配协议**

[![Platform](https://img.shields.io/badge/Platform-maplebridge.io-green)](https://maplebridge.io)
[![Status](https://img.shields.io/badge/Status-Live-brightgreen)](https://maplebridge.io/app)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

---

## What is MapleBridge? / 什么是 MapleBridge？

**MapleBridge.io** is a Canada-China B2B supply-demand matching platform. Canadian importers post procurement needs in natural language; the system automatically finds and introduces the best-fit Chinese manufacturers — no middleman, no manual searching.

**MapleBridge.io** 是专为加拿大与中国企业打造的 B2B 供需匹配平台。买家用自然语言发布采购需求，系统自动搜索并匹配最优中国供应商，直接邮件引荐双方，无需中间人。

---

## How the A2A Protocol Works / 协议运作原理

```
Buyer posts need (EN/ZH)
        ↓
Intent Parser — LLM extracts: product, quantity, budget, spec
        ↓
SearXNG Search — TradeKey · Made-in-China · Global Sources
        ↓
Semantic Matcher — GPT-4o-mini (EN) / Qwen-Plus (ZH)
        ↓
Supplier scored & ranked by relevance
        ↓
Email introduction sent to both buyer and supplier
```

### Agent Roles / 智能体角色

| Agent | Role | Description |
|-------|------|-------------|
| `BUYER_BOT` | Demand intake | Parses buyer procurement intent |
| `MANUS_BOT` | Orchestrator | Triggers search + match pipeline |
| `BOT_SCRAPED` | Supply sourcing | Stores crawler-found suppliers |
| `SUPPLIER_AGENT` | Notification | Emails matched suppliers |

---

## API Endpoints / 接口文档

### Post a Procurement Need / 发布采购需求

```http
POST /api/webhook/manus
Content-Type: application/json

{
  "buyer_email": "buyer@example.com",
  "demand_description": "Looking for PCB manufacturer, 10,000 units/month, IPC Class 2",
  "product_category": "electronics",
  "budget_cad": 50000
}
```

### Query Matched Suppliers / 查询匹配供应商

```http
GET /api/intents?type=supply&status=matched
```

### Post Supply Intent / 发布供应意向

```http
POST /api/intents
Content-Type: application/json

{
  "issuer": "supplier@factory.cn",
  "type": "supply",
  "description": "Professional PCB manufacturer, ISO 9001, 15 years export experience"
}
```

---

## Matching Logic / 匹配逻辑

**Semantic Matching (not keyword matching)**

Traditional B2B directories match on keywords. MapleBridge uses LLM semantic understanding:

- A buyer searching *"injection molded plastic parts"* matches suppliers who describe themselves as *"precision plastic components manufacturer"*
- Bilingual understanding: Chinese-language supplier profiles are matched against English buyer needs

**Language Routing / 语言路由**

| Context | Model | Reason |
|---------|-------|--------|
| English procurement | GPT-4o-mini | North American B2B terminology |
| Chinese procurement | Qwen-Plus | Chinese business context + lower latency |

---

## Tech Stack / 技术架构

```
Frontend:    Streamlit (maplebridge.io/app)
Backend:     FastAPI (Python 3.11)
Database:    SQLite (intents, matched_pairs, crawled_leads)
Search:      SearXNG (self-hosted, multi-engine)
AI:          OpenAI GPT-4o-mini + Alibaba Qwen-Plus
Email:       Resend API
Infra:       Docker Compose on Alibaba Cloud ECS
Proxy:       Nginx (static landing + API routing)
```

---

## Product Categories Supported / 支持品类

- Electronics & PCB / 电子元器件
- Textiles & Apparel / 纺织服装
- Industrial Machinery / 工业机械
- Furniture & Home Goods / 家具家居
- Medical Devices / 医疗器械
- Food & Agriculture / 食品农业
- Building Materials / 建筑材料
- Packaging / 包装材料

---

## Use the Platform / 使用平台

**For Canadian Buyers / 加拿大买家：**
1. Visit [maplebridge.io/app](https://maplebridge.io/app)
2. Post your procurement need in English or Chinese
3. Receive matched supplier introductions by email within minutes

**For Chinese Suppliers / 中国供应商：**
1. Visit [maplebridge.io/app](https://maplebridge.io/app)
2. Post your supply capability
3. Get automatically matched with Canadian buyers

---

## Links / 相关链接

- 🌐 Platform: [maplebridge.io/app](https://maplebridge.io/app)
- 📄 Landing Page: [maplebridge.io](https://maplebridge.io)
- 📊 Dataset: [maplebridge-a2a-trade-logic-dataset](https://github.com/jinjihuang88-ui/maplebridge-a2a-trade-logic-dataset)

---

## License

MIT © 2026 MapleBridge.io
