import streamlit as st
from openai import OpenAI
import requests

# 设置页面布局
st.set_page_config(page_title="高考志愿填报助手", layout="wide")

def check_url(url: str) -> bool:
    try:
        response = requests.get(url, timeout=5)  # 设置超时时间为5秒
        return response.status_code == 200
    except requests.RequestException as e:
        st.sidebar.warning(f"无法访问 {url}，错误信息：{str(e)}")
        return False

def generate_content(score, preferred_major):
    base_url = 'https://api.deepseek.com'
    if not check_url(base_url):
        st.sidebar.warning("无法访问 DeepSeek API，可能是网页链接的合法性或网络连接问题。请检查链接或稍后重试。")
        return "请检查您的网络连接或 API 配置，并重试。"

    try:
        client = OpenAI(base_url=base_url, api_key=st.secrets['API_KEY'])
        response = client.chat.completions.create(
            model='deepseek-chat',
            temperature=0.2,
            frequency_penalty=0.5,
            max_tokens=512,
            messages=[
                {'role': 'system', 'content': sys_prompt},
                {'role': 'user', 'content': f"分数：{score.strip()}, 喜欢的专业：{preferred_major.strip()}"},
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"无法访问 API 或处理请求：{str(e)}")
        return "请检查您的网络连接或 API 配置，并重试。"

sys_prompt = '''你是一位精通高考大数据分析的高级规划师，需同时具备：
1) 全国各省各批次分数线实时查询能力 
2) 院校三维对比功能（学科实力/就业率/区位优势）
3) 智能志愿梯度生成技术 
4) 专业适配度测评。所有数据需注明来源年份，对预测性结论要提示‘仅供参考’。当考生提出‘冲稳保’策略请求时，必须结合近3年录取位次波动分析。
同时可根据用户喜好匹配相关专业和院校，可向用户展示该校基本情况和往年专业最低录取分数线，并分析该用户分数的录取风险情况并推荐该分数录取概率高的学校与专业。

目标：
帮助考生根据分数、位次和兴趣，科学制定“冲稳保”志愿填报方案，最大化录取概率。

技能：
政策解读：熟悉各省高考批次线划分规则、新老高考差异及特殊招生政策（如强基计划、民族班）。
数据分析：能快速查询并对比院校/专业历年分数线、位次趋势，提供量化建议。
策略制定：基于考生分数生成分层志愿推荐（冲/稳/保），并提示风险（如专业级差、退档风险）。

工作流：
信息收集：确认考生所在省份、科类（物理/历史/文理）、高考分数及位次。
需求匹配：询问考生兴趣专业或院校类型（如“优先城市还是学校排名？”）。

方案输出：
提供批次线解读 + 目标院校列表（附分数差和位次参考）。
强调关键注意事项（如“该专业单科成绩要求≥120分”）。

输出格式：
结构化分点回复，关键数据加粗或表格化，例如：
您的位次：2024年XX省理科第1.2万名（参考2023年对应分数：580分）。

推荐院校：
学校    最低分（2023）    您的分差
冲：A大学    585    +5
稳：B大学    575    -5
注意：B大学的计算机专业近年录取线高于校线15分，建议谨慎填报。

限制：
不承诺录取结果：仅提供概率分析，避免“100%能上”等绝对表述。
数据免责：需声明“仅供参考，以考试院最新公布为准”。
中立建议：不引导考生选择特定院校或专业，仅客观对比优劣。
'''

st.title('高考志愿填报助手')
col1, col2 = st.columns(2)
with col1:
    score = st.text_input(label='请输入分数', placeholder='例如：580')
    preferred_major = st.text_input(label='请输入喜欢的专业', placeholder='例如：计算机科学')
    button = st.button('确定', type='primary')
    placeholder = st.empty()
    if button and score.strip() and preferred_major.strip():
        content = generate_content(score, preferred_major)
        placeholder.markdown(content)