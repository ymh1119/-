import json
import re
import streamlit as st

# ========= 和前面配置保持一致 =========
PDF_INDEX_FILE = "pdf_index.json"
PAGE_OFFSET = 2
# ======================================

@st.cache_resource
def load_index():
    """加载预生成的索引，只加载一次并缓存"""
    with open(PDF_INDEX_FILE,"r",encoding="utf-8") as f:
        return json.load(f)

def search_knowledge_page(keyword: str) -> str:
    try:
        pages = load_index()
    except Exception as e:
        return f"❌ 错误：索引文件加载失败 {e}"
    
    total_pages = len(pages)
    total_chars = sum(len(p["text"]) for p in pages)
    debug_info = f"🔍 调试信息：PDF共{total_pages}页，提取到总文字{total_chars}字符\n"
    keyword_clean = re.sub(r'\s+', '', keyword)
    hit_list = []
    for p in pages:
        if keyword in p["text"] or keyword_clean in p["text_clean"]:
            real_book_page = p["pdf_page"] - PAGE_OFFSET
            raw_text = p["text"].replace("\n", " ")
            hit_list.append(f"✅ 实体课本第{real_book_page}页\n片段：{raw_text[:300]}...")
    if hit_list:
        return debug_info + "\n\n".join(hit_list)
    else:
        return debug_info + "❌ 在教材中未检索到该知识点，请核对关键词"

if __name__ == "__main__":
    data = load_index()
    print(f"预加载索引共{len(data)}页")

