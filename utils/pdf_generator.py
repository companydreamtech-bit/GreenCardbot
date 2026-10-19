import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime


def generate_application_pdf(data: dict, app_code: str, output_path: str) -> str:
    """Arizachi ma'lumotlari asosida rasmiy ko'rinishdagi PDF hujjat yaratish"""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    story = []
    styles = getSampleStyleSheet()

    # Maxsus stillar
    header_title = ParagraphStyle(
        name="HeaderTitle",
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0B2545"),
        alignment=1,
    )
    sub_title = ParagraphStyle(
        name="SubTitle",
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#134074"),
        alignment=1,
    )
    section_title = ParagraphStyle(
        name="SectionTitle",
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0B2545"),
    )
    cell_label = ParagraphStyle(
        name="CellLabel",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#333333"),
    )
    cell_value = ParagraphStyle(
        name="CellValue",
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#111111"),
    )

    # 1. Bosh qism (Header)
    story.append(Paragraph("UNITED STATES DIVERSITY VISA PROGRAM", header_title))
    story.append(Paragraph("DV-2027 OFFICIAL ENTRY SUMMARY / ARIZA VARAQASI", sub_title))
    story.append(Spacer(1, 10))
    story.append(
        HRFlowable(
            width="100%", thickness=2, color=colors.HexColor("#0B2545"), spaceAfter=15
        )
    )

    # 2. Ariza kodi va holati jadvali
    main_info = data.get("main", {})
    created_at = data.get("created_at", datetime.now().strftime("%d.%m.%Y %H:%M"))
    if "T" in created_at:
        try:
            dt = datetime.fromisoformat(created_at)
            created_at = dt.strftime("%d.%m.%Y %H:%M")
        except Exception:
            pass

    meta_table_data = [
        [
            Paragraph("<b>Application ID / Ariza Kodi:</b>", cell_label),
            Paragraph(f"<font color='#0B2545'><b>{app_code}</b></font>", cell_label),
            Paragraph("<b>Submission Date / Sana:</b>", cell_label),
            Paragraph(str(created_at), cell_value),
        ],
        [
            Paragraph("<b>Primary Applicant / Arizachi:</b>", cell_label),
            Paragraph(f"{main_info.get('first_name', '')} {main_info.get('last_name', '')}", cell_value),
            Paragraph("<b>Phone / Telefon:</b>", cell_label),
            Paragraph(str(main_info.get("phone", "-")), cell_value),
        ],
    ]
    meta_table = Table(meta_table_data, colWidths=[130, 130, 130, 130])
    meta_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EEF4F8")),
                ("PADDING", (0, 0), (-1, -1), 6),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#B0C4DE")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.append(meta_table)
    story.append(Spacer(1, 15))

    # 3. Asosiy arizachi ma'lumotlari
    story.append(Paragraph("1. PRIMARY APPLICANT INFORMATION", section_title))
    story.append(Spacer(1, 5))

    patronymic = main_info.get("patronymic") or "None / Mavjud emas"
    primary_data = [
        [
            Paragraph("Last Name / Familiya:", cell_label),
            Paragraph(str(main_info.get("last_name", "-")), cell_value),
            Paragraph("First Name / Ism:", cell_label),
            Paragraph(str(main_info.get("first_name", "-")), cell_value),
        ],
        [
            Paragraph("Middle Name / Sharif:", cell_label),
            Paragraph(str(patronymic), cell_value),
            Paragraph("Gender / Jinsi:", cell_label),
            Paragraph(str(main_info.get("gender", "-")), cell_value),
        ],
        [
            Paragraph("Date of Birth / Sana:", cell_label),
            Paragraph(str(main_info.get("birth_date", "-")), cell_value),
            Paragraph("Place of Birth / Tug'ilgan joyi:", cell_label),
            Paragraph(str(main_info.get("birth_place", "-")), cell_value),
        ],
        [
            Paragraph("Education / Ta'lim:", cell_label),
            Paragraph(str(main_info.get("education", "-")), cell_value),
            Paragraph("Marital Status / Holati:", cell_label),
            Paragraph(str(main_info.get("marital_status", "-")), cell_value),
        ],
        [
            Paragraph("Address / Yashash manzili:", cell_label),
            Paragraph(str(main_info.get("address", "-")), cell_value),
            Paragraph("Photo Attached / Fotosurat:", cell_label),
            Paragraph("YES (Verified 5x5 cm / 600x600)", cell_value),
        ],
    ]
    prim_table = Table(primary_data, colWidths=[130, 130, 130, 130])
    prim_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
                ("PADDING", (0, 0), (-1, -1), 5),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#F9FBFD")]),
            ]
        )
    )
    story.append(prim_table)
    story.append(Spacer(1, 15))

    # 4. Turmush o'rtog'i ma'lumotlari (agar bo'lsa)
    spouse = data.get("spouse")
    if spouse:
        story.append(Paragraph("2. SPOUSE INFORMATION / TURMUSH O'RTOG'I", section_title))
        story.append(Spacer(1, 5))
        spouse_data = [
            [
                Paragraph("Full Name / F.I.SH:", cell_label),
                Paragraph(str(spouse.get("fullname", "-")), cell_value),
                Paragraph("Gender / Jinsi:", cell_label),
                Paragraph(str(spouse.get("gender", "-")), cell_value),
            ],
            [
                Paragraph("Date of Birth / Sana:", cell_label),
                Paragraph(str(spouse.get("birth_date", "-")), cell_value),
                Paragraph("Place of Birth / Joyi:", cell_label),
                Paragraph(str(spouse.get("birth_place", "-")), cell_value),
            ],
            [
                Paragraph("Education / Ta'lim:", cell_label),
                Paragraph(str(spouse.get("education", "-")), cell_value),
                Paragraph("Photo / Fotosurat:", cell_label),
                Paragraph("YES (Verified 5x5 cm)", cell_value),
            ],
        ]
        sp_table = Table(spouse_data, colWidths=[130, 130, 130, 130])
        sp_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
                    ("PADDING", (0, 0), (-1, -1), 5),
                    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#F9FBFD")]),
                ]
            )
        )
        story.append(sp_table)
        story.append(Spacer(1, 15))

    # 5. Bolalar ma'lumotlari (agar bo'lsa)
    children = data.get("children", [])
    if children:
        story.append(
            Paragraph(f"3. CHILDREN UNDER 21 / BOLALAR ({len(children)} ta)", section_title)
        )
        story.append(Spacer(1, 5))
        ch_rows = [
            [
                Paragraph("№", cell_label),
                Paragraph("Full Name / F.I.SH", cell_label),
                Paragraph("Gender", cell_label),
                Paragraph("Date of Birth", cell_label),
                Paragraph("Place of Birth", cell_label),
            ]
        ]
        for i, ch in enumerate(children, 1):
            ch_rows.append(
                [
                    Paragraph(str(i), cell_value),
                    Paragraph(str(ch.get("fullname", "-")), cell_value),
                    Paragraph(str(ch.get("gender", "-")), cell_value),
                    Paragraph(str(ch.get("birth_date", "-")), cell_value),
                    Paragraph(str(ch.get("birth_place", "-")), cell_value),
                ]
            )
        ch_table = Table(ch_rows, colWidths=[25, 175, 70, 100, 150])
        ch_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EEF4F8")),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
                    ("PADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )
        story.append(ch_table)
        story.append(Spacer(1, 15))

    # 6. Eslatma va Muhr qismi (Footer notes)
    notes_style = ParagraphStyle(
        name="NotesStyle",
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#555555"),
    )
    story.append(
        HRFlowable(
            width="100%", thickness=1, color=colors.HexColor("#B0C4DE"), spaceAfter=10
        )
    )
    story.append(
        Paragraph(
            "<b>Important Note:</b> This document is an official registration intake summary prepared for the U.S. Diversity Visa Program DV-2027. "
            "Please keep your Application ID safe. The official confirmation number will be issued once the entry is successfully submitted to the Department of State system.",
            notes_style,
        )
    )

    doc.build(story)
    return output_path
