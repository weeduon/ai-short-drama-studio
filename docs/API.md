# API 摘要

## Health

`GET /health`

## Roles

`GET /api/roles`

返回全部 Agent 角色。

## Projects

`POST /api/projects`

```json
{
  "title": "短剧名",
  "logline": "一句话故事",
  "genre": "豪门逆袭 / 抽象爽剧",
  "audience": "目标受众",
  "platform": "9:16 竖屏短剧",
  "tone": "强设定、强反转、强情绪刺激"
}
```

`GET /api/projects`

`GET /api/projects/{project_id}`

`POST /api/projects/{project_id}/run`

```json
{
  "episode_count": 6,
  "target_minutes_per_episode": 1.2,
  "use_cross_review": true,
  "max_revision_rounds": 1
}
```

## Artifacts

`GET /api/projects/{project_id}/artifacts`

## Models

`GET /api/models`

`POST /api/models`

```json
{
  "name": "My OpenAI-Compatible API",
  "provider_type": "openai_compatible",
  "base_url": "https://api.example.com/v1",
  "api_key_env": "CUSTOM_API_KEY",
  "model_name": "my-model",
  "enabled": true,
  "is_default": false,
  "purpose": "writing"
}
```

## Review

`POST /api/review/cross`

```json
{
  "artifact_id": 1,
  "dimensions": ["钩子", "人设", "爽点", "反转", "台词", "可拍性", "合规"]
}
```

## Video Tasks

`POST /api/video-tasks`

```json
{
  "project_id": 1,
  "episode": 1,
  "scene_no": 1,
  "provider": "kling",
  "prompt": "竖屏9:16...",
  "negative_prompt": "blurry, watermark",
  "ref_assets": []
}
```

`GET /api/video-tasks?project_id=1`

`POST /api/video-tasks/{task_id}/run`
