import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors

class ResumeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automotive Radar Resume Builder & PDF Generator")
        self.root.geometry("900x800")

        self.data = {}
        self.create_widgets()

    def create_widgets(self):
        # Top Action Bar
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill=tk.X)

        ttk.Button(top_frame, text="Load JSON", command=self.load_json).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Save JSON", command=self.save_json).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Generate PDF", command=self.generate_pdf).pack(side=tk.LEFT, padx=5)

        # Form Scrollable Area
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, padding=15)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def load_json(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not filepath:
            return

        with open(filepath, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # 1. Header Section
        ttk.Label(self.scrollable_frame, text="HEADER / CONTACT INFO", font=("Helvetica", 11, "bold")).pack(anchor="w", pady=(5, 5))
        hdr = self.data.get("header", {})
        self.hdr_entries = {}
        for key in ["name", "title", "location", "phone", "email", "linkedin"]:
            frame = ttk.Frame(self.scrollable_frame)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=f"{key.capitalize()}:", width=12).pack(side=tk.LEFT)
            ent = ttk.Entry(frame, width=80)
            ent.insert(0, hdr.get(key, ""))
            ent.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.hdr_entries[key] = ent

        # 2. Professional Summary
        ttk.Label(self.scrollable_frame, text="PROFESSIONAL SUMMARY", font=("Helvetica", 11, "bold")).pack(anchor="w", pady=(15, 5))
        self.summary_text = tk.Text(self.scrollable_frame, width=90, height=4)
        self.summary_text.insert("1.0", self.data.get("summary", ""))
        self.summary_text.pack(anchor="w")

        # 3. Core Competencies
        ttk.Label(self.scrollable_frame, text="CORE COMPETENCIES (One per line)", font=("Helvetica", 11, "bold")).pack(anchor="w", pady=(15, 5))
        self.comp_text = tk.Text(self.scrollable_frame, width=90, height=6)
        self.comp_text.insert("1.0", "\n".join(self.data.get("competencies", [])))
        self.comp_text.pack(anchor="w")

        # 4. Professional Experience
        ttk.Label(self.scrollable_frame, text="PROFESSIONAL EXPERIENCE", font=("Helvetica", 11, "bold")).pack(anchor="w", pady=(15, 5))
        self.exp_entries = []
        for job in self.data.get("experience", []):
            job_frame = ttk.LabelFrame(self.scrollable_frame, text=job.get("company", "Company"), padding=8)
            job_frame.pack(fill=tk.X, pady=5)

            row1 = ttk.Frame(job_frame)
            row1.pack(fill=tk.X, pady=2)
            ttk.Label(row1, text="Company:").pack(side=tk.LEFT)
            comp_e = ttk.Entry(row1, width=25)
            comp_e.insert(0, job.get("company", ""))
            comp_e.pack(side=tk.LEFT, padx=(5, 15))

            ttk.Label(row1, text="Role:").pack(side=tk.LEFT)
            role_e = ttk.Entry(row1, width=35)
            role_e.insert(0, job.get("role", ""))
            role_e.pack(side=tk.LEFT, padx=5)

            row2 = ttk.Frame(job_frame)
            row2.pack(fill=tk.X, pady=2)
            ttk.Label(row2, text="Dates:").pack(side=tk.LEFT)
            dates_e = ttk.Entry(row2, width=25)
            dates_e.insert(0, job.get("dates", ""))
            dates_e.pack(side=tk.LEFT, padx=(5, 15))

            ttk.Label(row2, text="Location:").pack(side=tk.LEFT)
            loc_e = ttk.Entry(row2, width=25)
            loc_e.insert(0, job.get("location", ""))
            loc_e.pack(side=tk.LEFT, padx=5)

            ttk.Label(job_frame, text="Bullets (One per line):").pack(anchor="w", pady=(4, 2))
            bullets_t = tk.Text(job_frame, width=85, height=5)
            bullets_t.insert("1.0", "\n".join(job.get("bullets", [])))
            bullets_t.pack(anchor="w")

            self.exp_entries.append({
                "company": comp_e, "role": role_e, "dates": dates_e, "location": loc_e, "bullets": bullets_t
            })

        # 5. Selected NXP Validation Experience
        ttk.Label(self.scrollable_frame, text="SELECTED SYSTEM VALIDATION EXPERIENCE (One per line)", font=("Helvetica", 11, "bold")).pack(anchor="w", pady=(15, 5))
        self.nxp_text = tk.Text(self.scrollable_frame, width=90, height=4)
        self.nxp_text.insert("1.0", "\n".join(self.data.get("selected_nxp_experience", [])))
        self.nxp_text.pack(anchor="w")

        # 6. Technical Skills
        ttk.Label(self.scrollable_frame, text="TECHNICAL SKILLS", font=("Helvetica", 11, "bold")).pack(anchor="w", pady=(15, 5))
        skills = self.data.get("technical_skills", {})
        self.skills_entries = {}
        for cat, val in skills.items():
            frame = ttk.Frame(self.scrollable_frame)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=f"{cat}:", width=20, font=("Helvetica", 9, "bold")).pack(side=tk.LEFT)
            ent = ttk.Entry(frame, width=70)
            ent.insert(0, val)
            ent.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.skills_entries[cat] = ent

        # 7. Education
        ttk.Label(self.scrollable_frame, text="EDUCATION (Degree | Institution | Year | Grade)", font=("Helvetica", 11, "bold")).pack(anchor="w", pady=(15, 5))
        self.edu_entries = []
        for edu in self.data.get("education", []):
            frame = ttk.Frame(self.scrollable_frame)
            frame.pack(fill=tk.X, pady=2)
            deg_e = ttk.Entry(frame, width=30); deg_e.insert(0, edu.get("degree", "")); deg_e.pack(side=tk.LEFT, padx=2)
            inst_e = ttk.Entry(frame, width=30); inst_e.insert(0, edu.get("institution", "")); inst_e.pack(side=tk.LEFT, padx=2)
            yr_e = ttk.Entry(frame, width=10); yr_e.insert(0, edu.get("year", "")); yr_e.pack(side=tk.LEFT, padx=2)
            grd_e = ttk.Entry(frame, width=15); grd_e.insert(0, edu.get("grade", "")); grd_e.pack(side=tk.LEFT, padx=2)
            self.edu_entries.append((deg_e, inst_e, yr_e, grd_e))

        # 8. Publications & Achievements
        ttk.Label(self.scrollable_frame, text="PUBLICATIONS & ACHIEVEMENTS (One per line)", font=("Helvetica", 11, "bold")).pack(anchor="w", pady=(15, 5))
        self.achieve_text = tk.Text(self.scrollable_frame, width=90, height=3)
        self.achieve_text.insert("1.0", "\n".join(self.data.get("publications_and_achievements", [])))
        self.achieve_text.pack(anchor="w")

        # 9. Languages
        ttk.Label(self.scrollable_frame, text="LANGUAGES (Comma Separated)", font=("Helvetica", 11, "bold")).pack(anchor="w", pady=(15, 5))
        self.lang_entry = ttk.Entry(self.scrollable_frame, width=90)
        self.lang_entry.insert(0, ", ".join(self.data.get("languages", [])))
        self.lang_entry.pack(anchor="w", pady=(0, 15))

        messagebox.showinfo("Loaded", "All sections extracted successfully from JSON!")

    def extract_form_data(self):
        return {
            "header": {key: entry.get().strip() for key, entry in self.hdr_entries.items()},
            "summary": self.summary_text.get("1.0", tk.END).strip(),
            "competencies": [line.strip() for line in self.comp_text.get("1.0", tk.END).strip().split("\n") if line.strip()],
            "experience": [
                {
                    "company": item["company"].get().strip(),
                    "role": item["role"].get().strip(),
                    "dates": item["dates"].get().strip(),
                    "location": item["location"].get().strip(),
                    "bullets": [b.strip() for b in item["bullets"].get("1.0", tk.END).strip().split("\n") if b.strip()]
                }
                for item in self.exp_entries
            ],
            "selected_nxp_experience": [line.strip() for line in self.nxp_text.get("1.0", tk.END).strip().split("\n") if line.strip()],
            "technical_skills": {cat: entry.get().strip() for cat, entry in self.skills_entries.items()},
            "education": [
                {
                    "degree": deg.get().strip(),
                    "institution": inst.get().strip(),
                    "year": yr.get().strip(),
                    "grade": grd.get().strip()
                }
                for deg, inst, yr, grd in self.edu_entries
            ],
            "publications_and_achievements": [line.strip() for line in self.achieve_text.get("1.0", tk.END).strip().split("\n") if line.strip()],
            "languages": [l.strip() for l in self.lang_entry.get().split(",") if l.strip()]
        }

    def save_json(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if not filepath:
            return

        current_data = self.extract_form_data()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(current_data, f, indent=2)

        messagebox.showinfo("Saved", "JSON saved successfully!")

    def generate_pdf(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not filepath:
            return

        data = self.extract_form_data()
        doc = SimpleDocTemplate(filepath, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        story = []

        # Styles
        styles = getSampleStyleSheet()
        
        name_style = ParagraphStyle('Name', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=16, leading=18, alignment=TA_CENTER)
        subhead_style = ParagraphStyle('SubHead', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=13, alignment=TA_CENTER, textColor=colors.HexColor('#1A2B4C'))
        contact_style = ParagraphStyle('Contact', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=11, alignment=TA_CENTER)
        
        sec_heading = ParagraphStyle('SecHeading', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5, leading=13, textColor=colors.HexColor('#1A2B4C'), spaceBefore=8, spaceAfter=2)
        
        job_title_style = ParagraphStyle('JobTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5, leading=12)
        job_sub_style = ParagraphStyle('JobSub', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8.5, leading=11, textColor=colors.HexColor('#333333'))
        
        body_style = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=11.5)
        bullet_style = ParagraphStyle('Bullet', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=11.5, leftIndent=10)

        def add_heading(title):
            story.append(Paragraph(title.upper(), sec_heading))
            story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#1A2B4C'), spaceBefore=1, spaceAfter=4))

        # --- HEADER ---
        hdr = data.get("header", {})
        story.append(Paragraph(hdr.get("name", ""), name_style))
        story.append(Spacer(1, 2))
        story.append(Paragraph(hdr.get("title", ""), subhead_style))
        story.append(Spacer(1, 2))
        
        c_info = f"{hdr.get('location', '')} | {hdr.get('phone', '')} | {hdr.get('email', '')} | {hdr.get('linkedin', '')}"
        story.append(Paragraph(c_info, contact_style))
        story.append(Spacer(1, 6))

        # --- SUMMARY ---
        if data.get("summary"):
            add_heading("Professional Summary")
            story.append(Paragraph(data["summary"], body_style))
            story.append(Spacer(1, 4))

        # --- COMPETENCIES ---
        if data.get("competencies"):
            add_heading("Core Competencies")
            for comp in data["competencies"]:
                story.append(Paragraph(f"• {comp}", bullet_style))
            story.append(Spacer(1, 4))

        # --- WORK EXPERIENCE ---
        if data.get("experience"):
            add_heading("Professional Experience")
            for job in data["experience"]:
                title_line = f"<b>{job.get('company', '')}</b> — {job.get('role', '')}"
                meta_line = f"{job.get('dates', '')} | {job.get('location', '')}"
                
                story.append(Paragraph(title_line, job_title_style))
                story.append(Paragraph(meta_line, job_sub_style))
                story.append(Spacer(1, 2))
                
                for b in job.get("bullets", []):
                    story.append(Paragraph(f"• {b}", bullet_style))
                story.append(Spacer(1, 4))

        # --- SELECTED NXP EXPERIENCE ---
        if data.get("selected_nxp_experience"):
            add_heading("Selected NXP System Validation Experience")
            for item in data["selected_nxp_experience"]:
                story.append(Paragraph(f"• {item}", bullet_style))
            story.append(Spacer(1, 4))

        # --- TECHNICAL SKILLS ---
        if data.get("technical_skills"):
            add_heading("Technical Skills")
            for cat, val in data["technical_skills"].items():
                story.append(Paragraph(f"<b>{cat}:</b> {val}", body_style))
                story.append(Spacer(1, 1.5))
            story.append(Spacer(1, 2))

        # --- EDUCATION ---
        if data.get("education"):
            add_heading("Education")
            for edu in data["education"]:
                edu_str = f"• <b>{edu.get('degree', '')}</b> — {edu.get('institution', '')}, {edu.get('year', '')} | {edu.get('grade', '')}"
                story.append(Paragraph(edu_str, body_style))
            story.append(Spacer(1, 4))

        # --- PUBLICATIONS & ACHIEVEMENTS ---
        if data.get("publications_and_achievements"):
            add_heading("Publications & Achievements")
            for ach in data["publications_and_achievements"]:
                story.append(Paragraph(f"• {ach}", bullet_style))
            story.append(Spacer(1, 4))

        # --- LANGUAGES ---
        if data.get("languages"):
            add_heading("Languages")
            story.append(Paragraph(" | ".join(data["languages"]), body_style))

        doc.build(story)
        messagebox.showinfo("Success", "Professional PDF generated successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeApp(root)
    root.mainloop()