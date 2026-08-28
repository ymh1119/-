import pdfplumber
import re

# ===================== 配置区 =====================
PDF_PATH = "textbook.pdf"
PAGE_OFFSET = 2
# ==================================================

_pdf_index_cache = None

def load_pdf_index():
    """预加载pdf，返回每页文本"""
    global _pdf_index_cache
    if _pdf_index_cache is not None:
        return _pdf_index_cache
    
    page_list = []
    with pdfplumber.open(PDF_PATH) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            page_list.append({
                "pdf_page": page.page_number,
                "text": txt,
                "text_clean": re.sub(r'\s+', '', txt)  # 去除所有空格换行，用于宽松匹配
            })
    _pdf_index_cache = page_list
    return page_list


def search_knowledge_page(keyword: str) -> str:
    """核心接口：输入知识点关键词，返回实体课本页码+文本片段"""
    try:
        pages = load_pdf_index()
    except FileNotFoundError:
        return "❌ 错误：未找到 textbook.pdf，请确认PDF文件上传到仓库根目录"
    
    # 调试信息（先显示PDF基本情况，方便排查）
    total_pages = len(pages)
    total_chars = sum(len(p["text"]) for p in pages)
    debug_info = f"🔍 调试信息：PDF共{total_pages}页，提取到总文字{total_chars}字符\n"
    
    # 关键词也去除空格换行，宽松匹配
    keyword_clean = re.sub(r'\s+', '', keyword)
    
    hit_list = []
    for p in pages:
        # 同时尝试：原文匹配 + 去空格宽松匹配
        if keyword in p["text"] or keyword_clean in p["text_clean"]:
            real_book_page = p["pdf_page"] - PAGE_OFFSET
            # 提取关键词前后的上下文片段
            raw_text = p["text"].replace("\n", " ")
            hit_list.append(f"✅ 实体课本第{real_book_page}页\n片段：{raw_text[:300]}...")
    
    if hit_list:
        return debug_info + "\n\n".join(hit_list)
    else:
        return debug_info + "❌ 在教材中未检索到该知识点，请核对关键词（可尝试输入PDF里一整句原文测试）"


if __name__ == "__main__":
    # 本地测试：打印前5页内容预览
    pages = load_pdf_index()
    for i, p in enumerate(pages[:5]):
        preview = p["text"][:100].replace("\n", " ")
        print(f"第{p['pdf_page']}页: {preview}\n")
