def build_wrapper_svg(master_src):
    """تعديل مرن يقبل ملف الشعار الجديد دون اشتراط وجود وسم defs"""
    # استخراج محتوى الـ SVG الداخلي وتجريده من أوسمة البداية والنهاية
    inner_content = re.sub(r'<\?xml[^>]*\?>', '', master_src) # حذف وسم الـ xml إن وجد
    inner_content = re.sub(r'<svg[^>]*>', '', inner_content)    # حذف وسم فتح الـ svg
    inner_content = inner_content.replace('</svg>', '').strip() # حذف وسم إغلاق الـ svg

    # استخراج الـ defs القديمة لو وجدت، أو وضعها فارغة
    defs_match = re.search(r"<defs>(.*?)</defs>", master_src, re.S)
    defs_content = defs_match.group(1).strip() if defs_match else ""

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {vb} {vb}">\n'
        "  <defs>\n"
        "{bg}\n"
        "{defs}\n"
        "  </defs>\n"
        '  <rect width="{vb}" height="{vb}" fill="url(#wkalBg)"/>\n'
        '  <g transform="translate({t} {t}) scale({s})">\n'
        "{art}\n"
        "  </g>\n"
        "</svg>\n"
    ).format(
        vb=VIEWBOX,
        bg=BG_GRADIENT,
        defs=defs_content,
        art=inner_content,
        t=round(TRANSLATE, 3),
        s=round(SCALE, 6),
    )
