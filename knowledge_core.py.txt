import pdfplumber

# ===================== 配置区（已经填好偏移！） =====================
PDF_PATH = "textbook.pdf"  # pdf放在项目根目录
PAGE_OFFSET = 2
# ======================================================================

def load_pdf_index():
    """预加载pdf，返回列表：[{pdf_page: 1, text: "页面文字"}, ...]"""
    page_list = []
    with pdfplumber.open(PDF_PATH) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            page_list.append({
                "pdf_page": page.page_number,
                "text": txt
            })
    return page_list

def test_print_pages():
    """校准测试函数，可单独运行查看每页预览"""
    pages = load_pdf_index()
    for p in pages:
        preview = p["text"][:80].replace("\n", "")
        real_page = p["pdf_page"] - PAGE_OFFSET
        print(f"【PDF物理页：{p['pdf_page']} | 实体课本页：{real_page}】 内容预览：{preview}\n")

def search_knowledge_page(keyword: str) -> str:
    """关键词检索pdf，返回实体页码+原文，方案1核心函数"""
    pages = load_pdf_index()
    hit_list = []
    for p in pages:
        if keyword in p["text"]:
            real_book_page = p["pdf_page"] - PAGE_OFFSET
            hit_list.append(f"✅ 实体课本第{real_book_page}页\n片段：{p['text'][:200]}...")
    if hit_list:
        return "\n\n".join(hit_list)
    else:
        return "❌ 在教材中未检索到该知识点，请核对关键词"

if __name__ == "__main__":
    test_print_pages()