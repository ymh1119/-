import pdfplumber

# ===================== 配置区（根据你的PDF页码偏移调整）=====================
PDF_PATH = "textbook.pdf"
PAGE_OFFSET = 2  # PDF页码和实体课本页码差值，后续可以自行微调
# =================================================================

# 全局缓存，只加载1次PDF，避免每次查询重复读取，防止streamlit超时
_pdf_index_cache = None

def load_pdf_index():
    """预加载pdf，返回列表：[{pdf_page: 1, text: "页面文字"}, ...]"""
    global _pdf_index_cache
    if _pdf_index_cache is not None:
        return _pdf_index_cache
    
    page_list = []
    with pdfplumber.open(PDF_PATH) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            page_list.append({
                "pdf_page": page.page_number,
                "text": txt
            })
    _pdf_index_cache = page_list
    return page_list

def test_print_pages():
    """校准测试函数，本地运行可以核对页码是否准确"""
    pages = load_pdf_index()
    for p in pages:
        preview = p["text"][:80].replace("\n", " ")
        real_page = p["pdf_page"] - PAGE_OFFSET
        print(f"【PDF物理页: {p['pdf_page']} | 实体课本页: {real_page}】内容预览: {preview}\n")

def search_knowledge_page(keyword: str) -> str:
    """核心接口：输入知识点关键词，返回实体课本页码+文本片段"""
    try:
        pages = load_pdf_index()
    except FileNotFoundError:
        return "❌ 错误：未找到 textbook.pdf，请确认PDF文件上传到仓库根目录"
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