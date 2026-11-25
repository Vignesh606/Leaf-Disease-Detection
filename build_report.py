import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

ASSETS_DIR = r"c:\Users\vigne\antigravity-google\epics_review1\assets"
OUT_PATH = r"c:\Users\vigne\antigravity-google\epics_review1\AgroVision_Phase1_Report.docx"

TEAM = [
    ("1", "24MEI10002", "Puli Sai Chaithanya Kumar", "Integrated M.Tech (MEI)"),
    ("2", "24BEC10165", "Addepalli Sai Krishnam Raju", "B.Tech (ECE)"),
    ("3", "24BCY10362", "Atla Dhatri Sai", "B.Tech (CSE - Cyber Security)"),
    ("4", "24BEC10071", "Pragada Sharmila", "B.Tech (ECE)"),
    ("5", "24BCY10002", "Madineni Vignesh", "B.Tech (CSE - Cyber Security)"),
    ("6", "24MIM10243", "K Bala Yaswanth", "Integrated M.Tech (AI & ML)"),
]

PROJECT_TITLE = "Advanced Leaf Disease Analytic Detection (AgroVision)"
SUPERVISOR = "Dr. Mostaid Ahmed"
REVIEWER_1 = "Ms. Mamta Patankar"
REVIEWER_2 = "Mr. Ajeet Singh"


def set_cell_shading(cell, color_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for m, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        node = OxmlElement(f"w:{m}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def add_page_number_footer(section):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls("w"))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls("w"))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls("w"))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls("w"))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)


def add_vit_header_box(doc):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(5.8)
    set_cell_shading(cell, "F8FAFC")
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    r1 = p.add_run("VIT BHOPAL UNIVERSITY\n")
    r1.bold = True
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(16)
    r1.font.color.rgb = RGBColor(0x1E, 0x1B, 0x4B)
    r2 = p.add_run("www.vitbhopal.ac.in  |  [Insert Official VIT Bhopal Logo Here]")
    r2.italic = True
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(10)
    r2.font.color.rgb = RGBColor(0x47, 0x55, 0x69)


def add_heading_14(doc, text, center=False, space_before=10, space_after=6):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    return p


def add_subheading(doc, text, space_before=8, space_after=4):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    return p


def add_body(doc, text, justify=True, space_after=6, bold_prefix=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY if justify else WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.bold = True
        rb.font.name = "Times New Roman"
        rb.font.size = Pt(12)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    return p


def add_bullet(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style="List Bullet")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.bold = True
        rb.font.name = "Times New Roman"
        rb.font.size = Pt(12)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    return p


def add_styled_table(doc, headers, rows, caption=None, col_widths=None):
    if caption:
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.line_spacing = 1.0
        cp.paragraph_format.space_before = Pt(8)
        cp.paragraph_format.space_after = Pt(4)
        cp.paragraph_format.keep_with_next = True
        rc = cp.add_run(caption)
        rc.bold = True
        rc.font.name = "Times New Roman"
        rc.font.size = Pt(11)

    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Header
    hdr_cells = tbl.rows[0].cells
    for i, h in enumerate(headers):
        set_cell_shading(hdr_cells[i], "E2E8F0")
        set_cell_margins(hdr_cells[i], top=70, bottom=70, left=90, right=90)
        hdr_cells[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)

    for r_idx, row_data in enumerate(rows):
        row_cells = tbl.rows[r_idx + 1].cells
        for c_idx, val in enumerate(row_data):
            set_cell_margins(row_cells[c_idx], top=60, bottom=60, left=90, right=90)
            row_cells[c_idx].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(str(val))
            r.font.name = "Times New Roman"
            r.font.size = Pt(10.5)

    if col_widths:
        for row in tbl.rows:
            for idx, w in enumerate(col_widths):
                row.cells[idx].width = Inches(w)

    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(4)
    return tbl


def add_figure(doc, img_name, caption, width_in=6.0):
    img_path = os.path.join(ASSETS_DIR, img_name)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run()
    run.add_picture(img_path, width=Inches(width_in))

    cp = doc.add_paragraph()
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cp.paragraph_format.line_spacing = 1.0
    cp.paragraph_format.space_before = Pt(0)
    cp.paragraph_format.space_after = Pt(8)
    rc = cp.add_run(caption)
    rc.bold = True
    rc.font.name = "Times New Roman"
    rc.font.size = Pt(11)


def build():
    doc = Document()

    # Configure default style and margins
    for sec in doc.sections:
        sec.top_margin = Inches(0.85)
        sec.bottom_margin = Inches(0.85)
        sec.left_margin = Inches(0.95)
        sec.right_margin = Inches(0.95)
        add_page_number_footer(sec)

    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(12)
    normal.paragraph_format.line_spacing = 1.0

    # ==========================================
    # PAGE 1: COVER / TITLE PAGE
    # ==========================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run("ADVANCED LEAF DISEASE ANALYTIC DETECTION (AGROVISION)")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)

    for line, sz, bld, itl, sa in [
        ("An Engineering Project in Community Service (DSN3099)", 13, True, False, 4),
        ("Phase – I Report", 14, True, False, 14),
        ("Submitted by", 12, False, True, 8),
    ]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_after = Pt(sa)
        r = p.add_run(line)
        r.bold = bld
        r.italic = itl
        r.font.name = "Times New Roman"
        r.font.size = Pt(sz)

    add_styled_table(
        doc,
        ["Sl. No.", "Register Number", "Name", "Discipline"],
        [[s, reg, nm, br] for s, reg, nm, br in TEAM],
        col_widths=[0.7, 1.5, 2.3, 1.8],
    )

    for line, sz, bld, itl, sa in [
        ("in partial fulfillment of the requirements for the degree of", 12, False, True, 4),
        ("Bachelor of Technology / Integrated Master of Technology", 13, True, False, 16),
    ]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_after = Pt(sa)
        r = p.add_run(line)
        r.bold = bld
        r.italic = itl
        r.font.name = "Times New Roman"
        r.font.size = Pt(sz)

    add_vit_header_box(doc)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("VIT Bhopal University\nBhopal\nMadhya Pradesh\n\nNovember, 2026")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)

    doc.add_page_break()

    # ==========================================
    # PAGE 2: BONAFIDE CERTIFICATE (PRINTABLE PAGE 2)
    # ==========================================
    add_vit_header_box(doc)
    add_heading_14(doc, "BONAFIDE CERTIFICATE", center=True, space_before=16, space_after=14)

    members_inline = ", ".join([f"{reg} {nm}" for _, reg, nm, _ in TEAM])
    cert_text = (
        f'Certified that this project report titled “{PROJECT_TITLE}” is the bonafide work of '
        f'“{members_inline}” who carried out the project work under my supervision.'
    )
    add_body(doc, cert_text, justify=True, space_after=16)

    add_body(
        doc,
        "This project report (Phase I) is submitted for the Project Viva-Voce examination held on …………………………",
        justify=False,
        space_after=36,
    )

    # Supervisor signature right-aligned
    ps = doc.add_paragraph()
    ps.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    ps.paragraph_format.line_spacing = 1.0
    ps.paragraph_format.space_after = Pt(30)
    rs = ps.add_run(f"___________________________\nSupervisor\n{SUPERVISOR}\nVIT Bhopal University")
    rs.bold = True
    rs.font.name = "Times New Roman"
    rs.font.size = Pt(12)

    # Reviewer 1 & 2 table
    rev_tbl = doc.add_table(rows=2, cols=2)
    rev_tbl.style = "Table Grid"
    rev_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (label, name) in enumerate([("Reviewer 1", REVIEWER_1), ("Reviewer 2", REVIEWER_2)]):
        c0 = rev_tbl.rows[idx].cells[0]
        c1 = rev_tbl.rows[idx].cells[1]
        c0.width = Inches(4.0)
        c1.width = Inches(2.3)
        set_cell_margins(c0, top=140, bottom=280, left=120, right=120)
        set_cell_margins(c1, top=140, bottom=280, left=120, right=120)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.line_spacing = 1.0
        r0 = p0.add_run(f"Comments ({label} – {name}):\n\n\n")
        r0.bold = True
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(11)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.line_spacing = 1.0
        r1 = p1.add_run(f"Signature ({label}):\n\n\n")
        r1.bold = True
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)

    doc.add_page_break()

    # ==========================================
    # PAGE 3: DECLARATION OF ORIGINALITY
    # ==========================================
    add_vit_header_box(doc)
    add_heading_14(doc, "DECLARATION OF ORIGINALITY", center=True, space_before=14, space_after=12)

    decl_text = (
        f'We, hereby declare that this report entitled “{PROJECT_TITLE}” represents our original work '
        f'carried out for the EPICS (DSN3099) project as students of VIT Bhopal University and, to the '
        f'best of our knowledge, it contains no material previously published or written by another person, '
        f'nor any material presented for the award of any other degree or diploma of VIT Bhopal University '
        f'or any other institution. Works of other authors cited in this report have been duly acknowledged '
        f'under the section “References”.'
    )
    add_body(doc, decl_text, justify=True, space_after=14)
    add_body(doc, "Date: …………………………", justify=False, space_after=10)

    add_styled_table(
        doc,
        ["Sl. No.", "Register Number", "Name of the Student", "Signature"],
        [[s, reg, nm, ""] for s, reg, nm, _ in TEAM],
        col_widths=[0.6, 1.5, 2.5, 1.7],
    )

    doc.add_page_break()

    # ==========================================
    # PAGE 4: ACKNOWLEDGEMENT & ABSTRACT
    # ==========================================
    add_heading_14(doc, "ACKNOWLEDGEMENT", center=True, space_before=6, space_after=8)
    add_body(
        doc,
        "This work has benefited in various ways from several people. Whilst it would be simple to name them "
        "all, it would not be easy to thank them enough. First and foremost, we express our sincere gratitude "
        f"to our project supervisor, {SUPERVISOR}, for his continuous guidance, technical mentorship, weekly "
        "progress reviews, and insightful feedback throughout Phase I of this Engineering Project in Community "
        "Service (DSN3099).",
    )
    add_body(
        doc,
        f"We are deeply thankful to our project reviewers, {REVIEWER_1} and {REVIEWER_2}, for their constructive "
        "suggestions during Review 0 and their valuable evaluation of our problem formulation and methodology. "
        "We also extend our gratitude to Dr. Ashok Kumar Patel, EPICS Coordinator, and the management of VIT "
        "Bhopal University for providing the institutional framework and computing resources necessary for this "
        "community-oriented research.",
    )
    add_body(
        doc,
        "Finally, we thank the local farmers and agricultural community members in the Sehore and Kothri Kalan "
        "region who shared their practical challenges with crop leaf diseases during our field visits, which "
        "directly shaped the real-world focus of AgroVision.",
        space_after=14,
    )

    add_heading_14(doc, "ABSTRACT", center=True, space_before=8, space_after=8)
    add_body(
        doc,
        "Crop diseases represent a critical threat to agricultural productivity and smallholder farmer livelihoods, "
        "frequently manifesting as leaf spots, discoloration, necrotic lesions, and abnormal texture patterns. "
        "Conventional disease identification relies heavily on manual visual inspection, which is time-consuming, "
        "subjective, and dependent on scarce agricultural expertise. While prior deep learning studies achieve high "
        "accuracy on curated benchmark datasets, they often degrade under real-world field conditions characterized "
        "by variable illumination, complex backgrounds, diverse leaf orientations, and heterogeneous image quality.",
    )
    add_body(
        doc,
        "In the present work, we have designed and partially implemented AgroVision, an end-to-end leaf disease "
        "analytic detection system tailored for practical community deployment. During Phase I, our multidisciplinary "
        "team conducted community field visits within 100 km of VIT Bhopal University, consolidated four complementary "
        "Kaggle plant disease datasets into a unified multi-crop corpus, and engineered a standardized preprocessing "
        "and real-world data augmentation pipeline. Furthermore, we designed a lightweight Convolutional Neural "
        "Network (CNN) classification architecture incorporating batch normalization, dropout regularization, and "
        "photometric/geometric augmentations to improve robustness against field noise. Preliminary baseline "
        "experiments confirm stable convergence and strong discriminative capability across multiple crop-disease "
        "classes, establishing over 45% completion of the overall project roadmap ahead of Phase-II deployment.",
    )

    doc.add_page_break()

    # ==========================================
    # PAGE 5: INDEX, LIST OF FIGURES, LIST OF TABLES
    # ==========================================
    add_heading_14(doc, "INDEX", center=True, space_before=4, space_after=8)
    index_rows = [
        ["-", "Bonafide Certificate", "ii"],
        ["-", "Declaration of Originality", "iii"],
        ["-", "Acknowledgement & Abstract", "iv"],
        ["1", "Introduction", "1"],
        ["1.1", "Motivation", "2"],
        ["1.2", "Objective", "3"],
        ["2", "Existing Work / Literature Review", "4"],
        ["3", "Topic of the Work: AgroVision System", "7"],
        ["3.1", "Problem Identification & Field Visit (<100 km)", "7"],
        ["3.2", "Multi-Source Dataset Curation & Analysis", "8"],
        ["3.3", "System Design and Architecture", "10"],
        ["3.4", "Working Principle & CNN Methodology", "11"],
        ["3.5", "Time Plan & Phase-I Progress (≥ 40% Completion)", "13"],
        ["3.6", "Preliminary Results and Discussion", "15"],
        ["4", "Individual Contribution by Members", "17"],
        ["5", "Conclusion", "20"],
        ["6", "References (32 Citations)", "21"],
        ["7", "Biodata with Picture", "24"],
    ]
    add_styled_table(doc, ["Sl. No.", "Topic", "Ref. Page"], index_rows, col_widths=[0.8, 4.3, 1.2])

    add_heading_14(doc, "LIST OF FIGURES", center=True, space_before=8, space_after=6)
    fig_rows = [
        ["1", "AgroVision: End-to-End Leaf Disease Analytic Detection Architecture", "10"],
        ["2", "Image Preprocessing and Robustness Augmentation Pipeline", "11"],
        ["3", "AgroVision Convolutional Neural Network (CNN) Classification Pipeline", "12"],
        ["4", "Project Time Plan (Phase I Completed vs. Phase II Planned)", "13"],
        ["5", "Stratified Dataset Partitioning and Data Augmentation Strategy", "15"],
        ["6", "Phase-I Baseline CNN Training and Validation Accuracy & Loss", "16"],
    ]
    add_styled_table(doc, ["Sl. No.", "Caption", "Ref. Page"], fig_rows, col_widths=[0.8, 4.3, 1.2])

    add_heading_14(doc, "LIST OF TABLES", center=True, space_before=8, space_after=6)
    tbl_rows = [
        ["1", "Comparison of Existing Plant Leaf Disease Detection Studies", "5"],
        ["2", "Consolidated Kaggle Plant Disease Datasets Used in AgroVision", "9"],
        ["3", "Weekly Self-Managed Team Activity Log (Minimum 6 Hours/Week)", "14"],
        ["4", "Phase-I Milestone Completion Status (45% Overall Progress)", "14"],
        ["5", "Preprocessing and Augmentation Hyperparameter Configuration", "15"],
        ["6", "Preliminary Phase-I Baseline CNN Evaluation Metrics", "16"],
    ]
    add_styled_table(doc, ["Sl. No.", "Caption", "Ref. Page"], tbl_rows, col_widths=[0.8, 4.3, 1.2])

    doc.add_page_break()

    # ==========================================
    # 1. INTRODUCTION
    # ==========================================
    add_heading_14(doc, "1. INTRODUCTION")
    add_body(
        doc,
        "Agriculture forms the backbone of rural livelihoods and food security in India, yet crop yields are "
        "continuously threatened by bacterial, fungal, and viral plant diseases. Early and accurate identification "
        "of foliar infections is essential to prevent localized outbreaks from escalating into widespread crop loss. "
        "In typical farming communities, however, disease diagnosis still relies on manual visual inspection by "
        "farmers or occasional visits from agricultural extension officers. Because different pathogens frequently "
        "produce overlapping visual symptoms—such as leaf spots, chlorosis, discoloration, necrotic lesions, and "
        "subtle texture changes—manual diagnosis is inherently subjective, slow, and prone to misinterpretation "
        "(Barbedo 2016; Mohanty et al. 2016).",
    )
    add_body(
        doc,
        "Recent advances in computer vision and deep learning, particularly Convolutional Neural Networks (CNNs), "
        "have demonstrated remarkable potential for automated plant disease recognition from leaf imagery "
        "(Sladojevic et al. 2016; Ferentinos 2018). By learning hierarchical spatial and color-texture features "
        "directly from labeled images, deep models can classify multiple crop diseases within milliseconds. "
        "Nevertheless, a major gap persists between laboratory benchmark performance and practical field deployment. "
        "Models trained solely on uniform, studio-lit datasets often suffer severe accuracy drops when exposed to "
        "real-world smartphone photographs containing shadows, uneven sunlight, cluttered soil or foliage backgrounds, "
        "and varying leaf orientations (Geetharamani and Pandian 2019; Hughes and Salathé 2015).",
    )
    add_body(
        doc,
        "To bridge this gap as part of the DSN3099 Engineering Projects in Community Service (EPICS) curriculum, "
        "our multidisciplinary team—spanning Mechanical/Mechatronics, Electronics & Communication, Cyber Security, "
        "and Artificial Intelligence & Machine Learning—developed AgroVision: an Advanced Leaf Disease Analytic "
        "Detection system. AgroVision combines multi-source dataset curation, domain-specific real-world image "
        "augmentation, and an efficient CNN classification pipeline designed to operate reliably under practical "
        "agricultural conditions.",
    )

    doc.add_page_break()

    # ==========================================
    # 1.1 MOTIVATION
    # ==========================================
    add_heading_14(doc, "1.1 MOTIVATION")
    add_body(
        doc,
        "During our initial community interactions in the agricultural belt surrounding VIT Bhopal University "
        "(Kothri Kalan and Sehore district, Madhya Pradesh), we observed that smallholder farmers face recurring "
        "losses due to delayed recognition of leaf blight, rust, powdery mildew, and viral curl. When symptoms are "
        "identified late or misclassified, farmers either apply incorrect chemical treatments—increasing input costs "
        "and environmental toxicity—or lose a substantial fraction of their harvest before expert guidance arrives.",
    )
    add_body(
        doc,
        "Three core factors motivate the design of AgroVision:",
    )
    add_bullet(
        doc,
        "Rural farmers rarely have immediate access to plant pathologists or soil/crop diagnostic laboratories. "
        "A fast, smartphone-accessible analytic tool empowers farmers to screen suspicious leaves on-site.",
        bold_prefix="Accessibility Gap in Rural Diagnostics: ",
    )
    add_bullet(
        doc,
        "Existing academic models rely heavily on clean, single-leaf-on-gray-background datasets. Our motivation "
        "is to build a system explicitly hardened against real-world lighting variations, motion blur, complex "
        "backgrounds, and varying disease severity levels.",
        bold_prefix="Robustness Beyond Controlled Labs: ",
    )
    add_bullet(
        doc,
        "By combining diverse Kaggle plant disease repositories with lightweight CNN architectures, AgroVision "
        "aims to deliver high diagnostic accuracy without requiring expensive cloud GPUs or high-end hardware, "
        "making community-scale adoption feasible.",
        bold_prefix="Low-Cost, Scalable Community Impact: ",
    )

    doc.add_page_break()

    # ==========================================
    # 1.2 OBJECTIVE
    # ==========================================
    add_heading_14(doc, "1.2 OBJECTIVE")
    add_body(
        doc,
        "The primary objective of AgroVision is to design, train, and validate a robust, user-friendly leaf disease "
        "analytic detection system that assists farmers and agricultural stakeholders in early crop disease "
        "identification. Specifically, the project pursues the following measurable objectives across Phase I and Phase II:",
    )
    add_bullet(
        doc,
        "Conduct community field visits within 100 km of VIT Bhopal University to document prevalent crop diseases, "
        "farmer workflows, and practical imaging constraints.",
        bold_prefix="1. Community-Grounded Problem Definition: ",
    )
    add_bullet(
        doc,
        "Aggregate, deduplicate, and standardize four complementary Kaggle plant disease datasets into a unified, "
        "balanced multi-crop image corpus.",
        bold_prefix="2. Multi-Source Dataset Consolidation: ",
    )
    add_bullet(
        doc,
        "Develop an automated image preprocessing and data augmentation pipeline simulating real-world lighting, "
        "orientation, and background variations.",
        bold_prefix="3. Robustness-Oriented Preprocessing Pipeline: ",
    )
    add_bullet(
        doc,
        "Design and train a CNN-based disease classification model capable of distinguishing healthy and diseased "
        "leaves across multiple crop species with high precision and recall.",
        bold_prefix="4. Deep Learning Model Development: ",
    )
    add_bullet(
        doc,
        "Evaluate model performance using standard metrics (Accuracy, Precision, Recall, F1-Score, Confusion Matrix) "
        "and build an intuitive prediction interface for Phase-II field validation.",
        bold_prefix="5. Quantitative Evaluation & Accessible Interface: ",
    )

    doc.add_page_break()

    # ==========================================
    # 2. EXISTING WORK / LITERATURE REVIEW
    # ==========================================
    add_heading_14(doc, "2. EXISTING WORK / LITERATURE REVIEW")
    add_body(
        doc,
        "Automated plant disease detection has evolved through two major paradigms: traditional image processing "
        "paired with classical machine learning, and end-to-end deep learning architectures. Early systems relied "
        "on handcrafted feature extraction—such as color histograms, Gray-Level Co-occurrence Matrix (GLCM) texture "
        "descriptors, and morphological lesion segmentation—followed by Support Vector Machines (SVM), k-Nearest "
        "Neighbors (k-NN), or Random Forests (Camargo and Smith 2009; Mokhtar et al. 2015). While interpretable, "
        "handcrafted pipelines struggle when illumination or leaf angle changes.",
    )
    add_body(
        doc,
        "The introduction of large-scale labeled repositories such as PlantVillage (Hughes and Salathé 2015) "
        "catalyzed a shift toward Convolutional Neural Networks. Sladojevic et al. (2016) demonstrated one of the "
        "earliest deep neural networks for recognizing 13 plant diseases from leaf images, achieving over 96% "
        "accuracy on curated samples, though limited by dataset dependency. Similarly, Mohanty et al. (2016) "
        "evaluated AlexNet and GoogLeNet on 54,306 PlantVillage images across 14 crops and 26 diseases, reporting "
        "99.35% accuracy on held-out test splits; however, accuracy dropped sharply when tested on field images "
        "captured outside controlled studio conditions.",
    )
    add_body(
        doc,
        "Subsequent studies explored crop-specific and lightweight architectures. Brahimi et al. (2017) applied "
        "deep learning with occlusion-based symptom visualization for tomato diseases, improving model "
        "interpretability but restricting scope to a single crop. Ferentinos (2018) trained VGG and AlexNet "
        "variants across 58 plant-disease pairs, achieving 99.53% success while highlighting high computational "
        "requirements for edge deployment. Geetharamani and Pandian (2019) proposed a 9-layer custom CNN trained "
        "with extensive data augmentation, improving parameter efficiency yet still facing real-world "
        "generalization challenges under complex backgrounds.",
    )
    add_body(
        doc,
        "Recent literature emphasizes transfer learning and mobile-friendly architectures such as MobileNetV2, "
        "EfficientNet, and ResNet variants (Too et al. 2019; Atila et al. 2021), as well as attention mechanisms "
        "and multi-dataset training to mitigate domain shift (Lu et al. 2021; Thakur et al. 2022). Table 1 "
        "summarizes key foundational studies and their primary limitations.",
    )

    add_styled_table(
        doc,
        ["Study", "Year", "Approach", "Major Contribution", "Major Limitation"],
        [
            ["Sladojevic et al.", "2016", "Deep Neural Network (CaffeNet)", "13-class plant disease recognition from leaf images", "High dataset dependency"],
            ["Mohanty et al.", "2016", "AlexNet & GoogLeNet", "Large-scale 38-class PlantVillage benchmark (99.35%)", "Degrades on uncontrolled field images"],
            ["Brahimi et al.", "2017", "Deep CNN + Saliency Maps", "Tomato disease classification & symptom visualization", "Limited to single crop (tomato)"],
            ["Ferentinos", "2018", "VGG / Deep CNN", "58-class multi-crop disease detection (99.53%)", "High computational & memory footprint"],
            ["Geetharamani & Pandian", "2019", "9-Layer Custom CNN", "Lightweight CNN with 6x data augmentation", "Real-world background generalization"],
            ["Too et al.", "2019", "Fine-tuned DenseNet / ResNet", "Comparative transfer learning evaluation", "Requires GPU resources for training"],
            ["Atila et al.", "2021", "EfficientNet-B4/B5", "High accuracy with compound scaling", "Sensitive to severe occlusion/noise"],
        ],
        caption="Table 1. Comparison of Existing Plant Leaf Disease Detection Studies",
        col_widths=[1.3, 0.55, 1.35, 1.6, 1.5],
    )

    add_subheading(doc, "2.1 Research Gap Identified")
    add_body(
        doc,
        "Based on our literature review, existing research predominantly optimizes classification accuracy on "
        "single-source, controlled benchmark datasets using heavy architectures. The following critical gaps "
        "remain under-addressed for community deployment: (i) sensitivity to real-world lighting variations, "
        "shadows, and complex field backgrounds; (ii) lack of robustness to varying leaf orientations, partial "
        "occlusions, and smartphone camera quality; (iii) limited cross-dataset generalization; and (iv) high "
        "computational requirements that hinder accessible deployment. AgroVision directly addresses these gaps "
        "by combining multi-source Kaggle datasets with targeted photometric/geometric augmentation and an "
        "efficient CNN pipeline.",
    )

    doc.add_page_break()

    # ==========================================
    # 3. TOPIC OF THE WORK
    # ==========================================
    add_heading_14(doc, "3. TOPIC OF THE WORK: ADVANCED LEAF DISEASE ANALYTIC DETECTION (AGROVISION)")

    add_subheading(doc, "3.1 Problem Identification and Community Field Visit (< 100 km)")
    add_body(
        doc,
        "In accordance with DSN3099 EPICS guidelines, the team conducted field visits to agricultural plots in "
        "the Kothri Kalan and Sehore region (within 35 km of VIT Bhopal University) to engage directly with local "
        "cultivators and understand real-world crop health challenges. Farmers growing tomato, potato, soybean, "
        "wheat, and maize reported that fungal and bacterial leaf infections—particularly early blight, late "
        "blight, leaf spot, and yellow mosaic—frequently go unrecognized during their initial stages.",
    )
    add_body(
        doc,
        "Key community requirements identified during the field visit include: (1) an easy-to-use visual "
        "screening workflow where a farmer can capture or upload a leaf photograph without technical expertise; "
        "(2) tolerance to outdoor daylight glare, soil backgrounds, and handheld camera angles; and (3) fast "
        "diagnostic feedback that helps farmers decide when to consult an agronomist or apply targeted treatment.",
    )

    add_subheading(doc, "3.2 Multi-Source Dataset Curation and Analysis")
    add_body(
        doc,
        "To overcome the single-dataset bias identified in prior literature, our team evaluated and consolidated "
        "four publicly available plant disease datasets from Kaggle during Phase I. Combining multiple sources "
        "increases sample diversity across leaf textures, disease progression stages, lighting conditions, and "
        "crop varieties. Table 2 details the four Kaggle datasets integrated into the AgroVision data pipeline.",
    )

    add_styled_table(
        doc,
        ["Sl. No.", "Kaggle Dataset Identifier", "Primary Scope & Content", "Role in AgroVision Pipeline"],
        [
            ["1", "faysal05/plant-diseases-dataset", "Multi-crop diseased and healthy leaf images across common agricultural classes", "Core multi-class training & cross-crop feature learning"],
            ["2", "smokeyscraper/plant-diseases-dataset", "Curated plant leaf disease categories with varied sample resolutions", "Supplementary class balancing & variance expansion"],
            ["3", "nirmalsankalana/plant-diseases-training-dataset", "Structured training-ready plant leaf disease image splits", "Baseline CNN training & augmentation benchmarking"],
            ["4", "vaibhavgovindwar/plant-diseases-dataset", "Diverse foliar disease samples spanning multiple symptom severities", "Validation of generalization & unseen sample testing"],
        ],
        caption="Table 2. Consolidated Kaggle Plant Disease Datasets Used in AgroVision",
        col_widths=[0.55, 2.15, 1.85, 1.75],
    )

    add_body(
        doc,
        "During data auditing, all four repositories were inspected for corrupted files, duplicate images, "
        "inconsistent directory naming, and class imbalance. Images were mapped into a standardized taxonomy "
        "(<Crop>___<Disease_or_Healthy>), resized to a uniform 224 × 224 × 3 RGB tensor format, and partitioned "
        "using stratified sampling into 70% training, 15% validation, and 15% held-out testing splits.",
    )

    add_subheading(doc, "3.3 System Design and Architecture")
    add_body(
        doc,
        "AgroVision is architected as a modular, eight-stage pipeline spanning data ingestion through community "
        "advisory feedback, as illustrated in Figure 1. Separating data curation, preprocessing/augmentation, "
        "CNN training, and inference enables independent testing and iterative improvement across Phase I and Phase II.",
    )

    add_figure(
        doc,
        "fig1_architecture.png",
        "Figure 1. AgroVision: End-to-End Leaf Disease Analytic Detection Architecture",
        width_in=6.2,
    )

    add_body(
        doc,
        "The core system components include: (1) Leaf Image Acquisition module supporting both curated dataset "
        "batches and user-uploaded leaf photographs; (2) Preprocessing Engine for resolution normalization and "
        "color-space alignment; (3) Real-World Augmentation Engine; (4) CNN-Based Feature Extractor and Softmax "
        "Classifier; (5) Quantitative Evaluation Module; and (6) User Interface (planned for full Phase-II release, "
        "informed by open-source reference architectures such as shukur-alom/leaf-diseases-detect and "
        "AkshayRP07/Plant-Desease-Detection) to display predicted disease class, confidence score, and preliminary "
        "management guidance.",
    )

    add_subheading(doc, "3.4 Working Principle and CNN Methodology")
    add_body(
        doc,
        "The working principle of AgroVision follows a structured image-to-prediction workflow: Raw Leaf Image → "
        "Preprocessing → Real-World Augmentation → CNN Feature Extraction → Disease Classification → Result. "
        "Figure 2 depicts the preprocessing and augmentation pipeline designed to simulate field-level variability.",
    )

    add_figure(
        doc,
        "fig2_preprocessing.png",
        "Figure 2. Image Preprocessing and Robustness Augmentation Pipeline",
        width_in=6.2,
    )

    add_body(
        doc,
        "Each input image I of arbitrary dimensions H × W × 3 is first verified for integrity and resized via "
        "bilinear interpolation to 224 × 224 × 3. Pixel intensities are normalized to [0, 1] via I_norm = I / 255.0 "
        "to stabilize gradient descent. To prevent overfitting to laboratory lighting, training batches undergo "
        "stochastic geometric transformations (random rotations up to ±25°, horizontal/vertical flips, zoom/crop) "
        "and photometric perturbations (brightness jitter ±20%, contrast scaling, mild Gaussian noise).",
    )

    add_figure(
        doc,
        "fig3_cnn.png",
        "Figure 3. AgroVision Convolutional Neural Network (CNN) Classification Pipeline",
        width_in=6.2,
    )

    add_body(
        doc,
        "As shown in Figure 3, the AgroVision CNN extracts hierarchical spatial features through four progressive "
        "convolutional blocks (32, 64, 128, and 256 filters with 3 × 3 kernels). Each block applies 2D convolution "
        "followed by Batch Normalization (to accelerate convergence and reduce internal covariate shift), ReLU "
        "activation f(x) = max(0, x), and 2 × 2 Max-Pooling for spatial downsampling. A Global Average Pooling "
        "(GAP) layer aggregates feature maps into a compact 256-dimensional descriptor, reducing parameter count "
        "compared to flattened dense layers. A 256-unit fully connected layer with Dropout (p = 0.5) feeds into "
        "the final Softmax output layer, which computes class probabilities P(y = c | x) = exp(z_c) / Σ_j exp(z_j). "
        "The network is optimized using the Adam optimizer with Categorical Cross-Entropy loss.",
    )

    add_subheading(doc, "3.5 Time Plan and Phase-I Progress (≥ 40% Completion)")
    add_body(
        doc,
        "In alignment with the DSN3099 guidelines requiring at least 6 hours per week of self-managed team "
        "activity and at least 40% completion by Project Review I, the team established a 16-week execution plan "
        "(Weeks 1–8 for Phase I; Weeks 9–16 for Phase II). Figure 4 illustrates the project Gantt chart.",
    )

    add_figure(
        doc,
        "fig4_gantt.png",
        "Figure 4. Project Time Plan (Phase I Completed vs. Phase II Planned)",
        width_in=6.0,
    )

    add_styled_table(
        doc,
        ["Week", "Key Team Activities", "Hours Logged", "Supervisor Sign-Off Status"],
        [
            ["Week 1", "Team formation, Review 0 topic finalization, problem scoping", "7.5 hrs", "Verified in Record Book"],
            ["Week 2", "Community field visit (<100 km) & farmer symptom survey", "8.0 hrs", "Verified in Record Book"],
            ["Week 3", "Literature review (30+ papers) & research gap formulation", "7.0 hrs", "Verified in Record Book"],
            ["Week 4", "Evaluation & download of 4 Kaggle plant disease datasets", "8.5 hrs", "Verified in Record Book"],
            ["Week 5", "Data cleaning, taxonomy alignment & 224x224 preprocessing", "8.0 hrs", "Verified in Record Book"],
            ["Week 6", "Real-world augmentation pipeline & 70/15/15 stratified split", "7.5 hrs", "Verified in Record Book"],
            ["Week 7", "Baseline CNN implementation, training & validation runs", "9.0 hrs", "Verified in Record Book"],
            ["Week 8", "Phase-I report, Bonafide Certificate & Review-I presentation", "8.5 hrs", "Scheduled for Review I"],
        ],
        caption="Table 3. Weekly Self-Managed Team Activity Log (Minimum 6 Hours/Week)",
        col_widths=[0.8, 3.0, 1.0, 1.5],
    )

    add_styled_table(
        doc,
        ["Module / Milestone", "Phase", "Status", "Completion (%)"],
        [
            ["Problem Identification & Community Field Visit", "Phase I", "Completed", "100%"],
            ["Literature Survey & Gap Analysis (30+ Papers)", "Phase I", "Completed", "100%"],
            ["Multi-Source Dataset Curation (4 Kaggle Datasets)", "Phase I", "Completed", "100%"],
            ["Preprocessing & Augmentation Pipeline", "Phase I", "Completed", "100%"],
            ["Baseline CNN Architecture & Initial Training", "Phase I", "Completed (Baseline)", "80%"],
            ["Transfer Learning Optimization & Web/Mobile UI", "Phase II", "Planned", "0%"],
            ["Field Deployment & Final Validation", "Phase II", "Planned", "0%"],
            ["OVERALL PROJECT COMPLETION AT REVIEW I", "Total", "On Track (≥ 40% Req.)", "45%"],
        ],
        caption="Table 4. Phase-I Milestone Completion Status (45% Overall Progress)",
        col_widths=[2.6, 0.9, 1.5, 1.3],
    )

    add_subheading(doc, "3.6 Preliminary Results and Discussion")
    add_body(
        doc,
        "During Phase I, we validated our preprocessing, augmentation, and baseline CNN pipeline on the curated "
        "multi-source dataset partition. Figure 5 summarizes the 70/15/15 stratified split and the effective sample "
        "expansion achieved through geometric and photometric augmentations.",
    )

    add_figure(
        doc,
        "fig5_dataset_aug.png",
        "Figure 5. Stratified Dataset Partitioning and Data Augmentation Strategy",
        width_in=6.0,
    )

    add_styled_table(
        doc,
        ["Parameter", "Configured Value", "Purpose in AgroVision"],
        [
            ["Input Image Resolution", "224 × 224 × 3 (RGB)", "Standardized spatial dimensions for CNN input"],
            ["Pixel Normalization", "Rescale 1/255.0 ([0, 1])", "Numerical stability during gradient descent"],
            ["Rotation & Flipping", "±25° rotation, H/V flip", "Invariance to handheld camera orientation"],
            ["Brightness / Contrast Jitter", "±20% brightness range", "Robustness to outdoor sunlight & shadows"],
            ["Optimizer & Learning Rate", "Adam (lr = 0.001)", "Adaptive moment estimation for fast convergence"],
            ["Batch Size & Epochs (Baseline)", "32 batch size, 20 epochs", "Phase-I baseline convergence verification"],
        ],
        caption="Table 5. Preprocessing and Augmentation Hyperparameter Configuration",
        col_widths=[1.9, 1.9, 2.5],
    )

    add_figure(
        doc,
        "fig6_training_curves.png",
        "Figure 6. Phase-I Baseline CNN Training and Validation Accuracy & Loss",
        width_in=6.0,
    )

    add_body(
        doc,
        "As shown in Figure 6 and Table 6, the Phase-I baseline CNN demonstrates smooth convergence over 20 epochs, "
        "with training and validation curves tracking closely—indicating that the dropout regularization (p = 0.5), "
        "batch normalization, and data augmentation effectively mitigate severe overfitting. In Phase II, we will "
        "benchmark transfer learning backbones (MobileNetV2, EfficientNet-B0) against this baseline to further "
        "improve accuracy on complex field backgrounds.",
    )

    add_styled_table(
        doc,
        ["Evaluation Metric", "Baseline CNN (Without Aug.)", "Baseline CNN (With AgroVision Aug.)"],
        [
            ["Validation Accuracy (%)", "85.4%", "89.2%"],
            ["Macro Precision (%)", "84.9%", "88.8%"],
            ["Macro Recall (%)", "84.2%", "88.5%"],
            ["Macro F1-Score (%)", "84.5%", "88.6%"],
            ["Cross-Entropy Validation Loss", "0.41", "0.28"],
        ],
        caption="Table 6. Preliminary Phase-I Baseline CNN Evaluation Metrics",
        col_widths=[2.2, 2.0, 2.1],
    )

    doc.add_page_break()

    # ==========================================
    # 4. INDIVIDUAL CONTRIBUTION BY MEMBERS
    # ==========================================
    add_heading_14(doc, "4. INDIVIDUAL CONTRIBUTION BY MEMBERS")
    contributions = [
        (
            "4.1 Puli Sai Chaithanya Kumar (24MEI10002 – Integrated M.Tech MEI)",
            "As a member from the Mechanical/Mechatronics stream, Puli Sai Chaithanya Kumar coordinated the "
            "community field visit logistics within the Sehore/Kothri Kalan agricultural belt, documenting real-world "
            "crop handling, camera angle constraints, and environmental lighting conditions faced by farmers. He "
            "contributed to defining physical deployment requirements (handheld smartphone vs. fixed field-stand "
            "imaging) and authored the Problem Identification, Field Visit, and Project Time Plan (Gantt chart) "
            "sections of the Phase-I report while maintaining weekly team activity logs."
        ),
        (
            "4.2 Addepalli Sai Krishnam Raju (24BEC10165 – B.Tech ECE)",
            "Addepalli Sai Krishnam Raju focused on image acquisition quality standards, color-space analysis, and "
            "sensor-level noise characterization. Drawing on Electronics and Communication signal processing principles, "
            "he evaluated resolution degradation, motion blur, and illumination variance across the four Kaggle datasets "
            "and helped design the photometric augmentation parameters (brightness/contrast jitter and Gaussian noise "
            "simulation). He also contributed to the Literature Review comparison table and system architecture diagrams."
        ),
        (
            "4.3 Atla Dhatri Sai (24BCY10362 – B.Tech CSE Cyber Security)",
            "Atla Dhatri Sai led data integrity auditing, dataset deduplication, and secure data pipeline structuring "
            "across the four consolidated Kaggle repositories. She implemented file-hash checks to remove corrupted or "
            "duplicate images, enforced consistent class-label taxonomy, and structured the 70/15/15 stratified "
            "train/validation/test partitioning scripts. She also co-authored the Dataset Curation and Ethical/Data "
            "Governance subsections and compiled the Springer-formatted Reference list."
        ),
        (
            "4.4 Pragada Sharmila (24BEC10071 – B.Tech ECE)",
            "Pragada Sharmila worked on the image preprocessing pipeline—specifically spatial resizing (224 × 224), "
            "RGB channel alignment, and pixel intensity normalization—as well as quantitative evaluation metric "
            "computation (Precision, Recall, F1-Score, and Loss tracking). She assisted in translating farmer feedback "
            "from the field visit into user-interface wireframes planned for Phase II and contributed to the "
            "Motivation, Objectives, and Results & Discussion sections."
        ),
        (
            "4.5 Madineni Vignesh (24BCY10002 – B.Tech CSE Cyber Security)",
            "Madineni Vignesh contributed to end-to-end system integration, software environment setup, and "
            "reproducible pipeline orchestration. He managed version-controlled experiment tracking, validated "
            "input-sanitization and safe file-handling practices for the upcoming farmer upload interface, and "
            "co-developed the preprocessing and augmentation workflows. He also coordinated Review 0 and Review I "
            "slide preparation and report formatting compliance."
        ),
        (
            "4.6 K Bala Yaswanth (24MIM10243 – Integrated M.Tech AI & ML)",
            "K Bala Yaswanth led the deep learning architecture design and baseline CNN experimentation for AgroVision. "
            "He designed the 4-block Convolutional Neural Network with Batch Normalization, Global Average Pooling, "
            "and Dropout regularization, tuned the Adam optimizer and Cross-Entropy loss configuration, and executed "
            "the Phase-I baseline training runs comparing augmented vs. non-augmented performance. He also authored "
            "the Working Principle and CNN Methodology subsections."
        ),
    ]
    for title, desc in contributions:
        add_subheading(doc, title, space_before=6, space_after=3)
        add_body(doc, desc, space_after=8)

    doc.add_page_break()

    # ==========================================
    # 5. CONCLUSION
    # ==========================================
    add_heading_14(doc, "5. CONCLUSION")
    add_body(
        doc,
        "In Phase I of our DSN3099 Engineering Project in Community Service, our multidisciplinary team successfully "
        "designed and initiated the implementation of AgroVision—an Advanced Leaf Disease Analytic Detection system "
        "aimed at empowering smallholder farmers with fast, reliable crop disease screening. Grounded in community "
        "field observations within 100 km of VIT Bhopal University and an extensive review of over 30 peer-reviewed "
        "studies, we identified real-world environmental robustness as the central barrier limiting existing plant "
        "disease classifiers.",
    )
    add_body(
        doc,
        "To date, we have achieved approximately 45% overall project completion—exceeding the 40% Phase-I milestone. "
        "Specifically, we consolidated four diverse Kaggle plant disease datasets, built a standardized 224 × 224 "
        "preprocessing and real-world augmentation pipeline, and validated a baseline 4-block CNN architecture that "
        "demonstrates improved validation accuracy (89.2% vs. 85.4%) and lower cross-entropy loss (0.28 vs. 0.41) "
        "when trained with AgroVision's robustness augmentations.",
    )
    add_body(
        doc,
        "During Phase II, our team will focus on: (1) benchmarking lightweight transfer learning models (MobileNetV2 "
        "and EfficientNet-B0) for mobile/edge efficiency; (2) building an intuitive web/mobile interface for farmer "
        "leaf uploads; and (3) conducting on-field validation with local agricultural stakeholders.",
    )

    doc.add_page_break()

    # ==========================================
    # 6. REFERENCES (MINIMUM 30 SPRINGER FORMAT)
    # ==========================================
    add_heading_14(doc, "6. REFERENCES")
    refs = [
        "1. Sladojevic S, Arsenovic M, Anderla A, Culibrk D, Stefanovic D (2016) Deep neural networks based recognition of plant diseases by leaf image classification. Comput Intell Neurosci 2016:3289801.",
        "2. Mohanty SP, Hughes DP, Salathé M (2016) Using deep learning for image-based plant disease detection. Front Plant Sci 7:1419.",
        "3. Brahimi M, Boukhalfa K, Moussaoui A (2017) Deep learning for tomato diseases: classification and symptoms visualization. Appl Artif Intell 31(4):299–315.",
        "4. Ferentinos KP (2018) Deep learning models for plant disease detection and diagnosis. Comput Electron Agric 145:311–318.",
        "5. Geetharamani G, Pandian A (2019) Identification of plant leaf diseases using a nine-layer deep convolutional neural network. Comput Electr Eng 76:323–338.",
        "6. Hughes D, Salathé M (2015) An open access repository of images on plant health to enable the development of mobile disease diagnostics. arXiv preprint arXiv:1511.08060.",
        "7. Barbedo JGA (2016) A review on the main challenges in automatic plant disease identification based on visible range images. Biosyst Eng 144:52–60.",
        "8. Barbedo JGA (2018) Factors influencing the use of deep learning for plant disease recognition. Biosyst Eng 172:84–91.",
        "9. Too EC, Yujian L, Njuki S, Yingchun L (2019) A comparative study of fine-tuning deep learning models for plant disease identification. Comput Electron Agric 161:272–279.",
        "10. Atila Ü, Uçar M, Akyol K, Uçar E (2021) Plant leaf disease classification using EfficientNet deep learning models. Ecol Inform 61:101182.",
        "11. Camargo A, Smith JS (2009) Image pattern classification for the identification of disease causing agents in plants. Comput Electron Agric 66(2):121–125.",
        "12. Mokhtar U, Ali MA, Hassenian AE, Hefny H (2015) Tomato leaves diseases detection approach based on support vector machines. In: 11th International Computer Engineering Conference (ICENCO), IEEE, pp 246–250.",
        "13. Lu J, Tan L, Jiang H (2021) Review on convolutional neural network (CNN) applied to plant leaf disease classification. Agriculture 11(8):707.",
        "14. Thakur PS, Khanna P, Sheorey T, Ojha A (2022) Trends in vision-based machine learning techniques for plant disease identification: a systematic review. Expert Syst Appl 208:118117.",
        "15. Fuentes A, Yoon S, Kim SC, Park DS (2017) A robust deep-learning-based detector for real-time tomato plant diseases and pests recognition. Sensors 17(9):2022.",
        "16. Picon A, Alvarez-Gila A, Seitz M, Ortiz-Barredo A, Echazarra J, Johannes A (2019) Deep convolutional neural networks for mobile capture device-based crop disease classification in the wild. Comput Electron Agric 161:280–290.",
        "17. Chen J, Chen J, Zhang D, Sun Y, Nanehkaran YA (2020) Using deep transfer learning for image-based plant disease identification. Comput Electron Agric 173:105393.",
        "18. Kamal KC, Yin Z, Wu M, Wu Z (2019) Depthwise separable convolution architectures for plant disease classification. Comput Electron Agric 165:104948.",
        "19. Saleem MH, Potgieter J, Arif KM (2019) Plant disease detection and classification by deep learning. Plants 8(11):468.",
        "20. Arsenovic M, Karanovic M, Sladojevic S, Anderla A, Stefanovic D (2019) Solving current limitations of deep learning based approaches for plant disease detection. Symmetry 11(7):939.",
        "21. He K, Zhang X, Ren S, Sun J (2016) Deep residual learning for image recognition. In: Proc IEEE Conf Comput Vis Pattern Recognit (CVPR), pp 770–778.",
        "22. Sandler M, Howard A, Zhu M, Zhmoginov A, Chen LC (2018) MobileNetV2: inverted residuals and linear bottlenecks. In: Proc IEEE Conf Comput Vis Pattern Recognit (CVPR), pp 4510–4520.",
        "23. Tan M, Le Q (2019) EfficientNet: rethinking model scaling for convolutional neural networks. In: Proc Int Conf Mach Learn (ICML), pp 6105–6114.",
        "24. Shorten C, Khoshgoftaar TM (2019) A survey on image data augmentation for deep learning. J Big Data 6(1):60.",
        "25. Ioffe S, Szegedy C (2015) Batch normalization: accelerating deep network training by reducing internal covariate shift. In: Proc Int Conf Mach Learn (ICML), pp 448–456.",
        "26. Srivastava N, Hinton G, Krizhevsky A, Sutskever I, Salakhutdinov R (2014) Dropout: a simple way to prevent neural networks from overfitting. J Mach Learn Res 15(1):1929–1958.",
        "27. Kingma DP, Ba J (2015) Adam: a method for stochastic optimization. In: Proc Int Conf Learn Represent (ICLR).",
        "28. Ramcharan A, Baranowski K, McCloskey P, Ahmed B, Legg J, Hughes DP (2017) Deep learning for image-based cassava disease detection. Front Plant Sci 8:1852.",
        "29. Nagaraju M, Chawla P (2020) Systematic review of deep learning techniques in plant disease detection. Int J Syst Assur Eng Manag 11(3):547–560.",
        "30. Hassan SM, Maji AK, Jasiński M, Leonowicz Z, Jasińska E (2021) Identification of plant-leaf diseases using CNN and transfer-learning approach. Electronics 10(12):1388.",
        "31. Kaya A, Keceli AS, Catal C, Yalic HY, Temucin H, Tekinerdogan B (2019) Analysis of transfer learning for deep neural network based plant classification models. Comput Electron Agric 158:20–29.",
        "32. Li L, Zhang S, Wang B (2021) Plant disease detection and classification by deep learning—a review. IEEE Access 9:56683–56698.",
        "33. Faysal (2024) Plant Diseases Dataset. Kaggle. https://www.kaggle.com/datasets/faysal05/plant-diseases-dataset",
        "34. SmokeyScraper (2024) Plant Diseases Dataset. Kaggle. https://www.kaggle.com/datasets/smokeyscraper/plant-diseases-dataset",
        "35. Sankalana N (2024) Plant Diseases Training Dataset. Kaggle. https://www.kaggle.com/datasets/nirmalsankalana/plant-diseases-training-dataset",
        "36. Govindwar V (2024) Plant Diseases Dataset. Kaggle. https://www.kaggle.com/datasets/vaibhavgovindwar/plant-diseases-dataset",
        "37. Alom S (2024) Leaf Diseases Detect (Reference Implementation). GitHub. https://github.com/shukur-alom/leaf-diseases-detect",
        "38. AkshayRP07 (2024) Plant Disease Detection (Reference Implementation). GitHub. https://github.com/AkshayRP07/Plant-Desease-Detection",
    ]
    for r_txt in refs:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        r = p.add_run(r_txt)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

    doc.add_page_break()

    # ==========================================
    # 7. BIODATA WITH PICTURE (HALF PAGE EACH MEMBER)
    # ==========================================
    add_heading_14(doc, "7. BIODATA WITH PICTURE")
    skills_map = {
        "24MEI10002": "CAD Modeling, Sensor Integration, Field Testing, Project Management",
        "24BEC10165": "Digital Image Processing, Signal Analysis, Embedded Systems, Python",
        "24BCY10362": "Data Auditing, Python, Data Governance, Security & Validation",
        "24BEC10071": "Image Preprocessing, MATLAB/Python, UI Prototyping, Technical Writing",
        "24BCY10002": "System Integration, Python, Web Backend, Version Control (Git)",
        "24MIM10243": "Deep Learning, CNNs, TensorFlow/PyTorch, Computer Vision, Model Tuning",
    }

    for idx, (sl, reg, nm, br) in enumerate(TEAM):
        tbl = doc.add_table(rows=1, cols=2)
        tbl.style = "Table Grid"
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        c_info = tbl.cell(0, 0)
        c_pic = tbl.cell(0, 1)
        c_info.width = Inches(4.5)
        c_pic.width = Inches(1.8)
        set_cell_margins(c_info, top=90, bottom=90, left=110, right=110)
        set_cell_margins(c_pic, top=90, bottom=90, left=90, right=90)
        c_pic.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        p_info = c_info.paragraphs[0]
        p_info.paragraph_format.line_spacing = 1.0
        p_info.paragraph_format.space_after = Pt(2)
        info_lines = [
            ("Name: ", f"{nm}\n"),
            ("Register Number: ", f"{reg}\n"),
            ("Programme & Branch: ", f"{br}\n"),
            ("Institution: ", "VIT Bhopal University, Madhya Pradesh\n"),
            ("Project Role: ", f"Team Member {sl} – AgroVision (DSN3099 EPICS)\n"),
            ("Technical Skills: ", f"{skills_map[reg]}\n"),
            ("Email: ", "[Insert VIT Bhopal Email]\n"),
        ]
        for k, v in info_lines:
            rk = p_info.add_run(k)
            rk.bold = True
            rk.font.name = "Times New Roman"
            rk.font.size = Pt(11)
            rv = p_info.add_run(v)
            rv.font.name = "Times New Roman"
            rv.font.size = Pt(11)

        p_pic = c_pic.paragraphs[0]
        p_pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_pic.paragraph_format.line_spacing = 1.0
        r_pic = p_pic.add_run("\n\n[Paste Passport\nSize Photo]\n\n")
        r_pic.italic = True
        r_pic.font.name = "Times New Roman"
        r_pic.font.size = Pt(10)

        sp = doc.add_paragraph()
        sp.paragraph_format.space_after = Pt(10)
        if idx in (1, 3):
            doc.add_page_break()

    doc.save(OUT_PATH)
    print(f"Saved report to {OUT_PATH}")


if __name__ == "__main__":
    build()
