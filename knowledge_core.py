import fitz
import easyocr
import re
import streamlit as st

# ===================== 配置区 =====================
PDF_PATH = "textbook.pdf"
PAGE_OFFSET = 2
OCR_DPI = 100  # 降低分辨率，大幅提速
# ==================================================

# 缓存OCR模型（全局只初始化1次）
@st.cache_resource
def get_ocr_reader():
    return easyocr.Reader(['ch_sim','en'])

# 缓存PDF全文索引，一次构建，反复查询
@st.cache_resource
def load_pdf_index():
    reader = get_ocr_reader()
    page_list = []
    doc = fitz.open(PDF_PATH)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        txt = page.get_text()
        # 原生文字为空才执行OCR
        if not txt.strip():
            pix = page.get_pixmap(dpi=OCR_DPI)
            img_bytes = pix.tobytes("png")
            ocr_result = reader.readtext(img_bytes, detail=0, min_size=8)
            txt = "".join(ocr_result)
        
        page_list.append({
            "pdf_page": page_num + 1,
            "text": txt,
            "text_clean": re.sub(r'\s+', '', txt)
        })
    doc.close()
    return page_list


def search_knowledge_page(keyword: str) -> str:
    try:
        pages = load_pdf_index()
    except FileNotFoundError:
        return "❌ 错误：未找到 textbook.pdf，请确认PDF文件上传到仓库根目录"
    
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
    pages = load_pdf_index()
    for i, p in enumerate(pages[:3]):
        preview = p["text"][:100].replace("\n", " ")
        print(f"第{p['pdf_page']}页: {preview}\n")
