from pypdf import PdfReader, PdfWriter
import os
#根目录
dir_path = "xxxxxx"
def merge_pdf(pdf_files, i):
    # 要合并的文件列表
    writer = PdfWriter()
    for fn in pdf_files:
        # 合并多个PDF文件
        reader = PdfReader(fn)
        for page in reader.pages:
            writer.add_page(page)
    # 输出合并后的PDF
    with open(f"new_{i}.pdf", "wb") as output_pdf:
        writer.write(output_pdf)
    output_pdf.close()


if __name__ == "__main__":
    pdf_files = []
    for fn in os.listdir(dir_path):
        if fn.endswith(".pdf"):
            pdf_files.append(dir_path + fn)
    print(pdf_files)
    pages = 0
    pages_start = 0
    idx = 0
    for i in range(0, len(pdf_files)):
        reader = PdfReader(pdf_files[i])
        if pages + len(reader.pages) > 300 or i == len(pdf_files) - 1:
            merge_pdf_files = pdf_files[pages_start : i - 1]
            print(f"合并 {merge_pdf_files} 中")
            merge_pdf(merge_pdf_files, idx)
            print(f"合并 {merge_pdf_files} 成功")
            pages = 0
            idx = idx + 1
            pages_start = i
    print("全部合并完毕！")
