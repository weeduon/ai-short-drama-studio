import asyncio
from typing import Any
from sqlalchemy.orm import Session
from .providers import LLMConfig, call_openai_compatible, extract_json, get_enabled_configs
from ..workflows.prompts import REVIEW_PROMPT, SYSTEM_BASE


async def review_with_models(db: Session, artifact: dict[str, Any], dimensions: list[str]) -> dict[str, Any]:
    configs = [cfg for cfg in get_enabled_configs(db) if cfg.api_key]
    if not configs:
        mock = {
            "score": 82,
            "verdict": "needs_revision",
            "dimensions": [{"name": item, "score": 80} for item in dimensions],
            "strengths": ["结构完整", "短剧工业流程清晰", "有可拍摄拆分"],
            "issues": ["缺少真实播放数据", "部分反转还可以更狠"],
            "actions": ["强化前三秒钩子", "增加每集尾钩冲击", "给主角补一个更明确的身份秘密"],
            "_model": "local-review-mock",
        }
        return {"reviews": [mock], "average_score": mock["score"], "final_verdict": mock["verdict"]}

    async def one(cfg: LLMConfig):
        prompt = REVIEW_PROMPT.format(dimensions="、".join(dimensions))
        messages = [
            {"role": "system", "content": SYSTEM_BASE + "\n" + prompt},
            {"role": "user", "content": f"请评审以下短剧产物：\n{artifact}"},
        ]
        try:
            text = await call_openai_compatible(cfg, messages, temperature=0.2)
            data = extract_json(text)
            data["_model"] = cfg.name
            return data
        except Exception as exc:  # noqa: BLE001
            return {"score": 0, "verdict": "error", "issues": [str(exc)], "_model": cfg.name}

    reviews = await asyncio.gather(*(one(cfg) for cfg in configs[:5]))
    scores = [float(item.get("score", 0)) for item in reviews if item.get("verdict") != "error"]
    avg = round(sum(scores) / len(scores), 2) if scores else 0
    return {
        "reviews": reviews,
        "average_score": avg,
        "final_verdict": "pass" if avg >= 85 else "needs_revision",
    }
