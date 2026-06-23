# 前端模型配置说明

本版本已经把模型 API 配置放到网页前端。

## 使用方式

1. 启动项目后打开 `http://localhost:5173`。
2. 左侧进入「模型配置」。
3. 填写或编辑模型配置：
   - 显示名称
   - base_url
   - model_name
   - api_key_env
   - 用途
4. 点击「保存配置」。
5. 在模型卡片里粘贴 API Key，点击「保存密钥」。
6. 点击「测试连接」。

## 密钥保存位置

API Key 会保存在本地：

```text
backend/data/model_keys.json
```

`backend/data/` 已经在 `.gitignore` 中忽略，不会提交到 GitHub。

## 常见 base_url

```text
OpenAI: https://api.openai.com/v1
Grok / xAI: https://api.x.ai/v1
SiliconFlow: https://api.siliconflow.cn/v1
DeepSeek: https://api.deepseek.com/v1
OpenRouter: https://openrouter.ai/api/v1
```

模型名以服务商后台为准，别靠感觉猜。感觉这东西已经害人类写出太多烂配置了。
