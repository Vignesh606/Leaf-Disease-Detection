import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

ASSETS_DIR = r"c:\Users\vigne\antigravity-google\epics_review1\assets"
OUT_PPTX = r"c:\Users\vigne\antigravity-google\epics_review1\AgroVision_Review1_Presentation.pptx"

NAVY = RGBColor(0x0F, 0x17, 0x2A)
BLUE = RGBColor(0x1D, 0x4E, 0xD8)
TEAL = RGBColor(0x0D, 0x94, 0x88)
SLATE = RGBColor(0x33, 0x41, 0x55)
LIGHT_BG = RGBColor(0xF8, 0xFA, 0xFC)


def set_bg(slide, color=LIGHT_BG):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_title_bar(slide, title_text, subtitle_text=None):
    tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12.1), Inches(0.85))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Calibri"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = NAVY

    if subtitle_text:
        p2 = tf.add_paragraph()
        p2.text = subtitle_text
        p2.font.name = "Calibri"
        p2.font.size = Pt(14)
        p2.font.color.rgb = BLUE


def add_bullets(slide, items, left=0.7, top=1.35, width=11.8, height=5.5, font_size=17):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    for idx, item in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.space_after = Pt(10)
        if isinstance(item, tuple):
            head, body = item
            r1 = p.add_run()
            r1.text = "• " + head + ": "
            r1.font.name = "Calibri"
            r1.font.size = Pt(font_size)
            r1.font.bold = True
            r1.font.color.rgb = NAVY
            r2 = p.add_run()
            r2.text = body
            r2.font.name = "Calibri"
            r2.font.size = Pt(font_size)
            r2.font.color.rgb = SLATE
        else:
            p.text = "• " + item
            p.font.name = "Calibri"
            p.font.size = Pt(font_size)
            p.font.color.rgb = SLATE


def build():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # Slide 1: Title
    s1 = prs.slides.add_slide(blank)
    set_bg(s1, RGBColor(0xEF, 0xF6, 0xFF))
    tb = s1.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(1.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "Advanced Leaf Disease Analytic Detection (AgroVision)"
    p.font.size = Pt(34)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.text = "DSN3099 – Engineering Projects in Community Service | PROJECT REVIEW I"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = BLUE

    tb2 = s1.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(6.5), Inches(3.8))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    hdr = tf2.paragraphs[0]
    hdr.text = "TEAM MEMBERS"
    hdr.font.size = Pt(16)
    hdr.font.bold = True
    hdr.font.color.rgb = NAVY
    members = [
        "1. Puli Sai Chaithanya Kumar – 24MEI10002",
        "2. Addepalli Sai Krishnam Raju – 24BEC10165",
        "3. Atla Dhatri Sai – 24BCY10362",
        "4. Pragada Sharmila – 24BEC10071",
        "5. Madineni Vignesh – 24BCY10002",
        "6. K Bala Yaswanth – 24MIM10243",
    ]
    for m in members:
        pm = tf2.add_paragraph()
        pm.text = m
        pm.font.size = Pt(15)
        pm.font.color.rgb = SLATE
        pm.space_after = Pt(4)

    tb3 = s1.shapes.add_textbox(Inches(8.0), Inches(2.5), Inches(4.5), Inches(3.5))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    for k, v in [
        ("SUPERVISOR", "Dr. Mostaid Ahmed"),
        ("REVIEWER 1", "Ms. Mamta Patankar"),
        ("REVIEWER 2", "Mr. Ajeet Singh"),
        ("INSTITUTION", "VIT Bhopal University (Nov 2026)"),
    ]:
        pk = tf3.add_paragraph()
        pk.text = k
        pk.font.size = Pt(13)
        pk.font.bold = True
        pk.font.color.rgb = BLUE
        pv = tf3.add_paragraph()
        pv.text = v
        pv.font.size = Pt(16)
        pv.font.bold = True
        pv.font.color.rgb = NAVY
        pv.space_after = Pt(10)

    # Slide 2: Problem & Field Visit
    s2 = prs.slides.add_slide(blank)
    set_bg(s2)
    add_title_bar(s2, "Problem Identification & Community Field Visit", "Grounded in local agricultural needs within 100 km of VIT Bhopal")
    add_bullets(s2, [
        ("Agricultural Impact", "Fungal, bacterial, and viral leaf diseases (spots, lesions, discoloration, blight) severely reduce crop yield."),
        ("Limitations of Manual Inspection", "Visual diagnosis by farmers is slow, subjective, and often misclassifies overlapping symptoms."),
        ("Field Visit Findings (< 100 km)", "Visited farming belt near Kothri Kalan / Sehore; farmers need an easy, smartphone-friendly screening tool."),
        ("Real-World Constraints", "Field photos suffer from daylight glare, shadows, cluttered soil backgrounds, and varied leaf angles."),
    ])

    # Slide 3: Literature Review & Gap
    s3 = prs.slides.add_slide(blank)
    set_bg(s3)
    add_title_bar(s3, "Literature Review & Identified Research Gap", "Synthesis of 30+ peer-reviewed studies")
    add_bullets(s3, [
        ("Sladojevic et al. (2016) & Mohanty et al. (2016)", "High benchmark accuracy (up to 99.35% on PlantVillage), but sharp drop on uncontrolled field images."),
        ("Brahimi et al. (2017) & Ferentinos (2018)", "Strong crop/disease classification, but limited crop scope or heavy compute requirements."),
        ("Geetharamani & Pandian (2019)", "9-layer CNN with augmentation improved efficiency, yet real-world background generalization remains open."),
        ("AgroVision Research Gap", "Need for a practical, lightweight crop disease detector hardened against lighting, orientation, and background noise."),
    ])

    # Slide 4: Objectives & Proposed System
    s4 = prs.slides.add_slide(blank)
    set_bg(s4)
    add_title_bar(s4, "Objectives & Proposed System: AgroVision", "From raw leaf photo to fast, reliable disease prediction")
    add_bullets(s4, [
        ("Multi-Source Data Consolidation", "Aggregate and standardize 4 Kaggle plant disease datasets to reduce single-source bias."),
        ("Robustness-First Preprocessing", "224×224 RGB normalization + geometric & photometric augmentations simulating real field conditions."),
        ("Efficient CNN Classifier", "4-block CNN with Batch Normalization, Global Average Pooling, and Dropout (p = 0.5)."),
        ("Accessible Deployment (Phase II)", "Simple farmer-friendly interface delivering instant disease class, confidence, and guidance."),
    ])

    # Slide 5: 4 Kaggle Datasets
    s5 = prs.slides.add_slide(blank)
    set_bg(s5)
    add_title_bar(s5, "Multi-Source Dataset Curation (4 Kaggle Datasets)", "Unified taxonomy & stratified 70 / 15 / 15 split")
    add_bullets(s5, [
        ("1. faysal05/plant-diseases-dataset", "Core multi-crop diseased and healthy leaf repository."),
        ("2. smokeyscraper/plant-diseases-dataset", "Supplementary categories for class balancing and resolution diversity."),
        ("3. nirmalsankalana/plant-diseases-training-dataset", "Structured training-ready leaf disease splits for baseline benchmarking."),
        ("4. vaibhavgovindwar/plant-diseases-dataset", "Additional symptom severities for cross-dataset generalization validation."),
        ("Curation Steps Completed", "Corrupt-file filtering, hash deduplication, label standardization, and 70/15/15 stratified split."),
        ("Open-Source Code References", "github.com/shukur-alom/leaf-diseases-detect & github.com/AkshayRP07/Plant-Desease-Detection"),
    ], font_size=15)

    # Slide 6: Architecture
    s6 = prs.slides.add_slide(blank)
    set_bg(s6)
    add_title_bar(s6, "AgroVision End-to-End System Architecture", "Modular 8-stage pipeline from dataset curation to field advisory")
    s6.shapes.add_picture(os.path.join(ASSETS_DIR, "fig1_architecture.png"), Inches(0.8), Inches(1.4), width=Inches(11.7))

    # Slide 7: Preprocessing & Augmentation
    s7 = prs.slides.add_slide(blank)
    set_bg(s7)
    add_title_bar(s7, "Preprocessing & Real-World Augmentation", "Improving invariance to lighting, angle, and field noise")
    s7.shapes.add_picture(os.path.join(ASSETS_DIR, "fig2_preprocessing.png"), Inches(0.7), Inches(1.3), width=Inches(11.9))
    s7.shapes.add_picture(os.path.join(ASSETS_DIR, "fig5_dataset_aug.png"), Inches(2.2), Inches(4.1), width=Inches(8.9))

    # Slide 8: CNN Architecture
    s8 = prs.slides.add_slide(blank)
    set_bg(s8)
    add_title_bar(s8, "CNN Classification Methodology", "4 Convolutional Blocks + BatchNorm + GlobalAvgPool + Softmax")
    s8.shapes.add_picture(os.path.join(ASSETS_DIR, "fig3_cnn.png"), Inches(0.8), Inches(1.5), width=Inches(11.7))
    add_bullets(s8, [
        ("Optimization", "Adam optimizer (lr = 0.001) with Categorical Cross-Entropy loss over 20 baseline epochs."),
        ("Regularization", "Batch Normalization + Dropout (0.5) + Global Average Pooling to prevent overfitting."),
    ], top=5.3, height=1.6, font_size=16)

    # Slide 9: Preliminary Results
    s9 = prs.slides.add_slide(blank)
    set_bg(s9)
    add_title_bar(s9, "Phase-I Preliminary Results & Discussion", "Augmentation improves validation accuracy from 85.4% to 89.2%")
    s9.shapes.add_picture(os.path.join(ASSETS_DIR, "fig6_training_curves.png"), Inches(0.8), Inches(1.35), width=Inches(11.5))
    add_bullets(s9, [
        ("Key Finding", "AgroVision augmentation reduced validation loss from 0.41 to 0.28 and boosted Macro F1-Score from 84.5% to 88.6%."),
    ], top=5.8, height=1.1, font_size=16)

    # Slide 10: Time Plan & Progress
    s10 = prs.slides.add_slide(blank)
    set_bg(s10)
    add_title_bar(s10, "Time Plan & Phase-I Progress (45% Completed)", "Exceeding the ≥ 40% Phase-I completion & ≥ 6 hrs/week requirement")
    s10.shapes.add_picture(os.path.join(ASSETS_DIR, "fig4_gantt.png"), Inches(1.1), Inches(1.35), width=Inches(11.1))

    # Slide 11: Phase II Roadmap & Thank You
    s11 = prs.slides.add_slide(blank)
    set_bg(s11, RGBColor(0xEF, 0xF6, 0xFF))
    add_title_bar(s11, "Phase-II Roadmap & Thank You", "Next steps toward community deployment")
    add_bullets(s11, [
        ("Weeks 9–11 (Model Optimization)", "Benchmark MobileNetV2 & EfficientNet-B0 transfer learning backbones for mobile efficiency."),
        ("Weeks 12–13 (User Interface)", "Build intuitive web/mobile leaf-upload interface with disease & remedy summary."),
        ("Weeks 14–16 (Field Validation)", "Test with local farmers on real smartphone captures & finalize DSN3099 Phase-II submission."),
    ], top=1.6, height=3.6, font_size=18)

    tb_ty = s11.shapes.add_textbox(Inches(0.8), Inches(5.4), Inches(11.7), Inches(1.2))
    p_ty = tb_ty.text_frame.paragraphs[0]
    p_ty.alignment = PP_ALIGN.CENTER
    p_ty.text = "THANK YOU — QUESTIONS & FEEDBACK"
    p_ty.font.size = Pt(28)
    p_ty.font.bold = True
    p_ty.font.color.rgb = BLUE

    prs.save(OUT_PPTX)
    print(f"Saved presentation to {OUT_PPTX}")


if __name__ == "__main__":
    build()
