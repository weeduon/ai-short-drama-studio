import json
from typing import Any
from sqlalchemy.orm import Session
from ..llm.providers import complete_json
from ..models import Artifact, Project
from .prompts import STAGE_PROMPTS, SYSTEM_BASE
from .roles import ROLE_MAP


def _fallback(stage: str, project: Project, context: dict[str, Any], episode_count: int) -> dict[str, Any]:
    base = {
        "project_title": project.title,
        "logline": project.logline,
        "stage": stage,
        "note": "本地演示样稿。配置 API Key 后会调用真实大模型生成。",
    }
    samples: dict[str, dict[str, Any]] = {
        "showrunner": {**base, "core_selling_point": "强设定开场、清晰目标、连续反转、集集尾钩。", "style": project.tone},
        "market_radar": {**base, "audience_needs": ["快速进入剧情", "人物关系清楚", "反转容易传播"], "cover_titles": [f"《{project.title}》开局反转", "三秒进入核心冲突"]},
        "hit_breakdown": {**base, "templates": ["高概念设定", "公开冲突", "关键身份信息", "尾钩升级"]},
        "wild_idea": {**base, "ideas": [{"title": "AI 档案重新排序家族关系", "emotion": 90, "shootability": 82}, {"title": "旧手机收到未来剧本提醒", "emotion": 86, "shootability": 78}]},
        "character_designer": {**base, "characters": [{"name": "沈逆", "tag": "隐藏价值的主角", "goal": "拿回被忽视的机会", "visual_anchor": "黑风衣、旧手机"}, {"name": "林栀", "tag": "冷静盟友", "goal": "补上过去的信息差", "visual_anchor": "白衬衫、银色耳钉"}]},
        "season_architect": {**base, "episodes": [{"episode": i, "hook": f"第 {i} 集开场给出新信息", "conflict": "目标受阻", "twist": "信息差反转", "cliffhanger": "新线索出现"} for i in range(1, episode_count + 1)]},
        "screenwriter": {**base, "episodes": [{"episode": 1, "scenes": [{"scene": 1, "location": "会议厅", "action": "众人讨论主角资格", "dialogue": ["你确定要现在公布？", "越早越好。"]}, {"scene": 2, "location": "走廊", "action": "旧手机弹出认证信息", "dialogue": ["认证完成。"]}]}]},
        "dialogue_polisher": {**base, "golden_lines": ["现在开始，规则换人写。", "你看到的是结尾，我看到的是开局。", "别急，真正的信息还没公开。"]},
        "storyboard_director": {**base, "shots": [{"shot": 1, "duration": "3s", "size": "特写", "camera": "缓慢推近", "action": "手机亮屏", "vertical_composition": "手机位于画面中心"}]},
        "video_prompt_engineer": {**base, "video_prompts": [{"episode": 1, "scene": 1, "zh": "竖屏9:16，现代会议厅，冷色电影光，主角穿黑风衣，镜头缓慢推近，紧张氛围", "en": "Vertical 9:16, modern meeting room, cold cinematic light, protagonist in a black trench coat, slow push-in, tense atmosphere", "negative_prompt": "blurry, watermark, distorted face"}]},
        "art_consistency": {**base, "character_cards": [{"name": "沈逆", "face": "清瘦、眼神锋利", "costume": "黑风衣", "do_not_change": ["发型", "外套", "手机"]}]},
        "compliance_auditor": {**base, "risk_level": "low", "risks": ["避免映射真实个人和机构"], "fixes": ["使用虚构名称", "保持架空设定"]},
        "data_replay": {**base, "metrics": ["3秒留存", "完播率", "评论率", "追更率"], "ab_tests": ["身份信息早露出 vs 晚露出", "主线强化 vs 情感线强化"]},
    }
    return samples.get(stage, base)


async def run_workflow(db: Session, project: Project, episode_count: int = 3) -> list[Artifact]:
    context: dict[str, Any] = {"project": {"title": project.title, "logline": project.logline, "genre": project.genre, "audience": project.audience, "platform": project.platform, "tone": project.tone}}
    artifacts: list[Artifact] = []

    for stage in STAGE_PROMPTS.keys():
        role = ROLE_MAP[stage]
        fallback = _fallback(stage, project, context, episode_count)
        messages = [
            {"role": "system", "content": SYSTEM_BASE + f"\n你的角色：{role.name}\n任务：{role.mission}\n质量标准：{role.quality_bar}"},
            {"role": "user", "content": json.dumps({"stage_instruction": STAGE_PROMPTS[stage], "episode_count": episode_count, "context": context}, ensure_ascii=False)},
        ]
        result = await complete_json(messages, db=db, fallback=fallback)
        artifact = Artifact(project_id=project.id, stage=stage, role=role.name, title=f"{project.title} - {role.name}", content_json=json.dumps(result, ensure_ascii=False))
        db.add(artifact)
        db.flush()
        artifacts.append(artifact)
        context[stage] = result

    project.status = "workflow_done"
    db.commit()
    return artifacts
