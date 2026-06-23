from dataclasses import dataclass


@dataclass(frozen=True)
class AgentRole:
    key: str
    name: str
    mission: str
    output: str
    quality_bar: str


ROLES: list[AgentRole] = [
    AgentRole("showrunner", "总导演 / Showrunner", "把控项目定位、受众、情绪曲线和统一风格。", "项目圣经、核心卖点、风格准则", "一句话能卖，前三秒有钩子，每集有尾钩。"),
    AgentRole("market_radar", "市场雷达专员", "扫描题材、平台偏好、受众情绪和近期爆点。", "趋势雷达、竞品方向、平台打法", "能直接指导剧情选择。"),
    AgentRole("hit_breakdown", "爆款拆解专员", "拆解同类爆款的钩子、爽点密度、反转节奏和封面标题套路。", "爆款结构表、可复用套路", "输出必须能转化成剧作模板。"),
    AgentRole("wild_idea", "脑洞策划专员", "负责强设定、抽象梗、极端处境和反常识冲突。", "高概念脑洞、主推设定、反转池", "荒诞但可理解，离谱但能拍。"),
    AgentRole("character_designer", "人设专员", "设计主角、反派、关系网、身份秘密、欲望和伤口。", "人物小传、关系冲突图、口头禅、视觉锚点", "人设要一眼能懂，动机能制造连续冲突。"),
    AgentRole("season_architect", "分集大纲专员", "把故事拆成短剧季结构，规划每集钩子、升级、反转、尾钩。", "分集大纲、情绪曲线、付费点建议", "集集有事，不能出现无效过渡集。"),
    AgentRole("screenwriter", "编剧", "写可拍摄剧本，控制场景、动作、对白、节奏和信息释放。", "分场剧本、对白、动作、场景说明", "短句、高冲突、少解释、多行动。"),
    AgentRole("dialogue_polisher", "台词嘴替专员", "把普通台词改成短剧口播感、网感和情绪爆点。", "台词润色版、金句、口播切片", "能截图当标题，能剪成预告。"),
    AgentRole("storyboard_director", "分镜导演", "把剧本拆成镜头、景别、运动、表演、转场和竖屏构图。", "镜头表、场景调度、竖屏构图方案", "每个镜头都能转成视频生成提示词。"),
    AgentRole("video_prompt_engineer", "视频提示词专员", "生成可用于视频生成工具的中英双语提示词。", "视频 Prompt、负面 Prompt、首帧图 Prompt、运镜参数", "提示词要具体到人物、表情、镜头、光线、动作和时长。"),
    AgentRole("art_consistency", "美术资产一致性专员", "维护角色脸、服装、场景、色彩、道具和世界观一致性。", "角色资产卡、场景资产卡、连续性检查表", "避免同一角色在不同镜头里变成不同人。"),
    AgentRole("compliance_auditor", "合规审核专员", "检查版权、平台规范、内容边界和发布风险。", "风险等级、修改建议、替代表达", "尽量保留戏剧张力，同时把风险拆掉。"),
    AgentRole("data_replay", "数据复盘专员", "根据播放、完播、互动、转化和评论反馈提出下一轮迭代方向。", "复盘指标、A/B 测试建议、下一集调整", "用数据改戏，不用玄学许愿。"),
]

ROLE_MAP = {role.key: role for role in ROLES}
