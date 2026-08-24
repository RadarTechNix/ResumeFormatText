import io
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from pypdf import PdfReader
from PIL import Image, ImageTk
import pymupdf as fitz  # PyMuPDF (use recommended import to avoid deprecation warning)

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

INITIAL_DATA = {
  "header": {
    "name": "Nikhil Ganpat Navghade",
    "location": "Munich, Germany",
    "phone": "+49 163 5454172",
    "email": "nikhil.nawaghadej@gmail.com",
    "linkedin": "linkedin.com/in/nikhil-navghade/",
    "title": "SYSTEM APPLICATIONS ENGINEER | RF & SEMICONDUCTOR SYSTEMS | CUSTOMER ENGINEERING"
  },
  "summary": "System Applications / RF Engineer with 12+ years of experience across semiconductor products, RF systems, radar SoCs, embedded systems, DSP, system integration, validation, and customer-facing engineering.\nExperienced in translating customer and system requirements into technical solutions, supporting semiconductor product evaluation and integration, performing system bring-up and laboratory validation, and troubleshooting complex interactions across RF, mixed-signal, hardware, software, and DSP domains.\nStrong background in RF signal chains, radar SoCs, ADC/DAC architectures, MATLAB/Simulink, Python, Embedded C, automated validation, RF characterization, and laboratory debugging. Proven experience collaborating with customers, applications, R&D, product, and marketing teams.",
  "competencies": [
    "System Applications & Customer Engineering: System architecture | Customer requirements | Product evaluation | Integration & bring-up | Validation | Technical support | Root-cause analysis",
    "RF & Semiconductor Systems: Radar SoCs | RF TX/RX chains | ADC/DAC | RF characterization | Gain/noise/dynamic range | Linearity & spurious analysis",
    "Software & Tools: Python | MATLAB/Simulink | Embedded C | Java | C++ (basic) | Git | Automated validation | Test frameworks",
    "Signal Processing: FMCW & pulsed radar | FFT | Digital filtering | Doppler | MIMO | Beamforming | CFAR | Detection | Angle estimation",
    "Laboratory: Oscilloscopes | Signal generators | Spectrum analyzers | Power meters | Attenuators | Frequency multipliers"
  ],
  "experience": [
    {
      "company": "NXP Semiconductors",
      "role": "System Integration & Validation Engineer",
      "meta": "via ACONEXT / Hays | Munich, Germany | 2026 – Present",
      "bullets": [
        "Perform system- and board-level validation of semiconductor radar products, from laboratory characterization through system qualification.",
        "Translate product requirements into validation strategies, automated test cases, measurement procedures, and performance metrics.",
        "Develop Python and Java automation frameworks covering 100+ validation scenarios, improving repeatability and efficiency.",
        "Integrate signal generators, attenuators, frequency multipliers, power meters, and other laboratory equipment into automated validation environments.",
        "Perform RF and system characterization using laboratory measurements and MATLAB-based analysis.",
        "Diagnose RF and system-level anomalies by correlating device behavior, requirements, measurements, and software analysis.",
        "Perform hardware/software integration and system debugging and communicate findings to cross-functional engineering teams."
      ]
    },
    {
      "company": "Calterah GmbH",
      "role": "FAE & Technical Sales",
      "meta": "Munich, Germany | Sept 2024 – Feb 2026",
      "bullets": [
        "Acted as a technical advisor to customers throughout the radar SoC lifecycle, from architecture and product selection through integration, validation, troubleshooting, and deployment.",
        "Supported customer architecture decisions involving RF front-end behavior, ADC sampling, DSP processing, interfaces, and end-to-end system performance.",
        "Gathered customer requirements, evaluated technical solutions, and guided successful semiconductor product integration.",
        "Diagnosed complex RF, mixed-signal, hardware/software, and DSP interaction issues, coordinating investigations between customers and internal R&D.",
        "Supported customer system bring-up, integration, validation, and performance optimization.",
        "Led root-cause analysis of issues involving secure boot, OTP programming, functional-safety configuration, and Ethernet interfaces.",
        "Delivered technical workshops, product demonstrations, and customer presentations, including at Electronica 2024.",
        "Collaborated with applications, marketing, product, and R&D teams to convert field requirements and issues into product feedback and improvements."
      ]
    },
    {
      "company": "Fusionride GmbH",
      "role": "Senior Radar Signal Processing Engineer",
      "meta": "Munich, Germany / India | Feb 2022 – Sept 2024",
      "bullets": [
        "Architected complete 1D–4D radar processing chains, including FFT, MIMO, beamforming, detection, and signal-processing modules using MATLAB/Simulink.",
        "Designed multi-core system architecture with focus on memory mapping, computational efficiency, runtime performance, and system integration.",
        "Developed antenna evaluation tools covering beam patterns, sidelobes, and virtual-array analysis, reducing analysis time from ~1 week to 1 day.",
        "Delivered the first 4×4 corner radar prototype with real-time detections within one year and contributed to 6×8 front-radar development.",
        "Led technical decisions covering algorithm architecture, system integration, validation, and performance optimization."
      ]
    },
    {
      "company": "Continental Automotive",
      "role": "Technical Specialist, Radar",
      "meta": "Bengaluru, India | Jul 2018 – Feb 2022",
      "bullets": [
        "Developed and validated radar signal-processing modules for automotive FMCW radar systems, achieving 99.92% functional coverage for Gen5 radar validation.",
        "Implemented and optimized CFAR, elevation MIMO, sidelobe suppression, and noise-estimation algorithms.",
        "Developed MATLAB and Embedded C modules for radar signal-processing pipelines and embedded implementation.",
        "Modelled and validated pulsed-Doppler radar systems and performed system-level performance analysis and debugging."
      ]
    },
    {
      "company": "Wavelet Technologies",
      "role": "Project Engineer",
      "meta": "Pune, India | Jul 2015 – Jul 2018",
      "bullets": [
        "Developed embedded firmware and signal-processing functionality for pulse wind-profile radar receiver systems.",
        "Participated in algorithm implementation, embedded development, laboratory testing, debugging, and system integration."
      ]
    }
  ],
  "education": [
    "M.E. — Embedded Systems & VLSI | Pune University | 2016 | CGPA: 8.54/10",
    "B.E. — Electronics & Telecommunication | Pune University | 2013 | CGPA: 8.43/10"
  ],
  "publications_and_achievements": [
    "IEEE Conference Paper: Comparative study and implementation of wind-profiler radar, 2017.",
    "Pioneered introduction of the first 4×4 corner radar product with real-time detections within one year at Fusionride.",
    "Received a monetary award for developing an engineering tool that significantly accelerated initial radar signal-processing bring-up and analysis."
  ],
  "languages": ["English", "German", "Hindi", "Marathi"]
}

class ResumeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automotive Radar Resume Editor & Live PDF Preview")
        self.root.geometry("1400x900")

        self.data = INITIAL_DATA
        self.preview_images = []
        self.preview_scale = 1.0  # zoom multiplier for PDF preview

        self.create_widgets()
        self.populate_form()

    def create_widgets(self):
        # Top Bar
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill=tk.X)

        ttk.Button(top_frame, text="Load JSON", command=self.load_json).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Save JSON", command=self.save_json).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(top_frame, text="Update Live Preview", command=self.update_live_preview).pack(side=tk.LEFT, padx=15)
        # Zoom controls for PDF preview
        ttk.Label(top_frame, text="   Zoom:").pack(side=tk.LEFT)
        ttk.Button(top_frame, text="-", width=3, command=self._zoom_out).pack(side=tk.LEFT)
        self.zoom_label = ttk.Label(top_frame, text="100%")
        self.zoom_label.pack(side=tk.LEFT, padx=4)
        ttk.Button(top_frame, text="+", width=3, command=self._zoom_in).pack(side=tk.LEFT)
        ttk.Button(top_frame, text="Reset", command=self._zoom_reset).pack(side=tk.LEFT, padx=(4,12))
        self.page_label = ttk.Label(top_frame, text="Total Pages: --", font=("Helvetica", 10, "bold"), foreground="navy")
        self.page_label.pack(side=tk.LEFT, padx=5)

        ttk.Button(top_frame, text="Export PDF", command=self.generate_pdf).pack(side=tk.RIGHT, padx=5)
        # Filename entry for export
        ttk.Label(top_frame, text="  File name:").pack(side=tk.RIGHT)
        self.filename_entry = tk.Entry(top_frame, width=30)
        self.filename_entry.pack(side=tk.RIGHT, padx=(0,8))

        # PanedWindow: Split Left (Form Editor) and Right (PDF Preview)
        paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        # --- LEFT PANE (Editor + JSON tab) ---
        left_container = ttk.Frame(paned)
        paned.add(left_container, weight=1)

        # Header for left pane with label and a side button to show JSON tab
        left_header = ttk.Frame(left_container)
        left_header.pack(fill=tk.X)
        self.left_tab_label = ttk.Label(left_header, text="Main Tab", font=("Helvetica", 10, "bold"))
        self.left_tab_label.pack(side=tk.LEFT, padx=6, pady=4)
        ttk.Button(left_header, text="Show JSON", command=lambda: self._show_json_tab()).pack(side=tk.RIGHT, padx=6)

        # Notebook containing main form and JSON diff/editor
        self.left_notebook = ttk.Notebook(left_container)
        self.main_tab = ttk.Frame(self.left_notebook)
        self.json_tab = ttk.Frame(self.left_notebook)
        self.left_notebook.add(self.main_tab, text="Main")
        self.left_notebook.add(self.json_tab, text="JSON")
        self.left_notebook.pack(fill=tk.BOTH, expand=True)

        # --- Main form canvas inside the notebook ---
        self.editor_canvas = tk.Canvas(self.main_tab)
        self.editor_scrollbar = ttk.Scrollbar(self.main_tab, orient="vertical", command=self.editor_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.editor_canvas, padding=15)

        self.scrollable_frame.bind("<Configure>", lambda e: self.editor_canvas.configure(scrollregion=self.editor_canvas.bbox("all")))
        self.editor_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.editor_canvas.configure(yscrollcommand=self.editor_scrollbar.set)

        self.editor_canvas.pack(side="left", fill="both", expand=True)
        self.editor_scrollbar.pack(side="right", fill="y")

        # --- JSON tab contents ---
        # smaller inline JSON viewer per user request
        self.json_text = tk.Text(self.json_tab, wrap=tk.NONE, width=60, height=18)
        j_v = ttk.Scrollbar(self.json_tab, orient=tk.VERTICAL, command=self.json_text.yview)
        j_h = ttk.Scrollbar(self.json_tab, orient=tk.HORIZONTAL, command=self.json_text.xview)
        self.json_text.configure(yscrollcommand=j_v.set, xscrollcommand=j_h.set)
        j_v.pack(side=tk.RIGHT, fill=tk.Y)
        j_h.pack(side=tk.BOTTOM, fill=tk.X)
        self.json_text.pack(fill=tk.BOTH, expand=True)

        json_btn_frame = ttk.Frame(self.json_tab)
        json_btn_frame.pack(fill=tk.X)
        ttk.Button(json_btn_frame, text="Apply JSON to Form", command=self._apply_json_from_tab).pack(side=tk.LEFT, padx=6, pady=6)
        ttk.Button(json_btn_frame, text="Save JSON to file", command=lambda: self._save_text_to_file(self.json_text)).pack(side=tk.LEFT, padx=6, pady=6)
        ttk.Button(json_btn_frame, text="Back to Main", command=lambda: self.left_notebook.select(self.main_tab)).pack(side=tk.RIGHT, padx=6, pady=6)
        # PDF-only window handle and image cache
        self.pdf_only_win = None
        self.pdf_only_images = []
        # Add Open PDF Only button to top bar
        ttk.Button(top_frame, text="Open PDF Only", command=self._open_pdf_only_window).pack(side=tk.RIGHT, padx=6)

        # --- RIGHT PANE (Live PDF Preview) ---
        right_container = ttk.Frame(paned)
        # give the preview pane more space (weight 3)
        paned.add(right_container, weight=3)

        preview_header = ttk.Label(right_container, text="LIVE PDF PREVIEW", font=("Helvetica", 11, "bold"), padding=5)
        preview_header.pack(anchor="nw")

        self.preview_canvas = tk.Canvas(right_container, bg="#525659")
        self.preview_scrollbar = ttk.Scrollbar(right_container, orient="vertical", command=self.preview_canvas.yview)
        self.preview_frame = tk.Frame(self.preview_canvas, bg="#525659", padx=10, pady=10)

        self.preview_frame.bind("<Configure>", lambda e: self.preview_canvas.configure(scrollregion=self.preview_canvas.bbox("all")))
        self.preview_canvas.create_window((0, 0), window=self.preview_frame, anchor="nw")
        self.preview_canvas.configure(yscrollcommand=self.preview_scrollbar.set)

        self.preview_canvas.pack(side="left", fill="both", expand=True)
        self.preview_scrollbar.pack(side="right", fill="y")

        # Mouse wheel bindings for smooth scrolling when cursor is over a pane
        self.preview_frame.bind("<Enter>", lambda e: self.preview_canvas.bind_all("<MouseWheel>", self._on_preview_mousewheel))
        self.preview_frame.bind("<Leave>", lambda e: self.preview_canvas.unbind_all("<MouseWheel>"))
        self.scrollable_frame.bind("<Enter>", lambda e: self.editor_canvas.bind_all("<MouseWheel>", self._on_editor_mousewheel))
        self.scrollable_frame.bind("<Leave>", lambda e: self.editor_canvas.unbind_all("<MouseWheel>"))
        # Ctrl+Wheel zoom on preview when cursor over preview
        self.preview_frame.bind("<Enter>", lambda e: self.preview_canvas.bind_all("<Control-MouseWheel>", self._on_ctrl_wheel_preview))
        self.preview_frame.bind("<Leave>", lambda e: self.preview_canvas.unbind_all("<Control-MouseWheel>"))

        # Global undo/redo bindings (Text and Entry widgets)
        self.root.bind_all("<Control-z>", self._global_undo)
        self.root.bind_all("<Control-y>", self._global_redo)
        # Ctrl+S to save JSON quickly
        self.root.bind_all("<Control-s>", self._global_save_json)

    def populate_form(self):
        for w in self.scrollable_frame.winfo_children():
            w.destroy()

        # Header
        self._add_section_header(self.scrollable_frame, "HEADER INFO", lambda: self._open_header_editor())
        hdr = self.data.get("header", {})
        self.hdr_entries = {}
        for key in ["name", "title", "location", "phone", "email", "linkedin"]:
            f = ttk.Frame(self.scrollable_frame)
            f.pack(fill=tk.X, pady=2)
            ttk.Label(f, text=f"{key.capitalize()}:", width=12).pack(side=tk.LEFT)
            ent = tk.Entry(f, width=60)
            ent.insert(0, hdr.get(key, ""))
            ent.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.hdr_entries[key] = ent

        # Summary
        self._add_section_header(self.scrollable_frame, "PROFESSIONAL SUMMARY", lambda: self._open_text_editor("summary", "Professional Summary"))
        self.summary_text = tk.Text(self.scrollable_frame, width=70, height=5, undo=True)
        self.summary_text.insert("1.0", self.data.get("summary", ""))
        self.summary_text.pack(anchor="w")

        # Core Competencies (One bullet per line for fast AI paste)
        self._add_section_header(self.scrollable_frame, "CORE COMPETENCIES (One bullet point per line)", lambda: self._open_text_editor("competencies", "Core Competencies"))
        self.comp_text = tk.Text(self.scrollable_frame, width=70, height=6, undo=True)
        self.comp_text.insert("1.0", "\n".join(self.data.get("competencies", [])))
        self.comp_text.pack(anchor="w")

        # Work Experience
        self._add_section_header(self.scrollable_frame, "PROFESSIONAL EXPERIENCE", lambda: messagebox.showinfo("Info", "Use the Open button on each job to maximize."))
        self.work_entries = []
        for job in self.data.get("experience", []):
            jf = ttk.LabelFrame(self.scrollable_frame, text=job.get("company", "Company"), padding=8)
            jf.pack(fill=tk.X, pady=5)

            # Open (maximize) button for this job section
            btn_frame = ttk.Frame(jf)
            btn_frame.pack(fill=tk.X)
            ttk.Button(btn_frame, text="Open", width=6, command=lambda j=job, jf=jf: self._open_job_editor(j, jf)).pack(side=tk.RIGHT)

            r1 = ttk.Frame(jf); r1.pack(fill=tk.X, pady=2)
            ttk.Label(r1, text="Company:").pack(side=tk.LEFT)
            c_e = tk.Entry(r1, width=20); c_e.insert(0, job.get("company", "")); c_e.pack(side=tk.LEFT, padx=(5,10))
            ttk.Label(r1, text="Role:").pack(side=tk.LEFT)
            r_e = tk.Entry(r1, width=25); r_e.insert(0, job.get("role", "")); r_e.pack(side=tk.LEFT, padx=5)

            r2 = ttk.Frame(jf); r2.pack(fill=tk.X, pady=2)
            ttk.Label(r2, text="Meta/Location:").pack(side=tk.LEFT)
            m_e = tk.Entry(r2, width=50); m_e.insert(0, job.get("meta", "")); m_e.pack(side=tk.LEFT, padx=5)

            ttk.Label(jf, text="Bullets (One per line):").pack(anchor="w", pady=(4, 2))
            b_t = tk.Text(jf, width=65, height=5, undo=True)
            b_t.insert("1.0", "\n".join(job.get("bullets", [])))
            b_t.pack(anchor="w")

            self.work_entries.append({"company": c_e, "role": r_e, "meta": m_e, "bullets": b_t})

        # Education
        self._add_section_header(self.scrollable_frame, "EDUCATION (One line per entry)", lambda: self._open_text_editor("education", "Education"))
        self.edu_text = tk.Text(self.scrollable_frame, width=70, height=3, undo=True)
        self.edu_text.insert("1.0", "\n".join(self.data.get("education", [])))
        self.edu_text.pack(anchor="w")

        # Publications
        self._add_section_header(self.scrollable_frame, "PUBLICATIONS & ACHIEVEMENTS", lambda: self._open_text_editor("publications_and_achievements", "Publications & Achievements"))
        self.achieve_text = tk.Text(self.scrollable_frame, width=70, height=3, undo=True)
        self.achieve_text.insert("1.0", "\n".join(self.data.get("publications_and_achievements", [])))
        self.achieve_text.pack(anchor="w")

        # Languages
        self._add_section_header(self.scrollable_frame, "LANGUAGES", lambda: self._open_text_editor("languages", "Languages"))
        self.lang_entry = tk.Entry(self.scrollable_frame, width=70)
        self.lang_entry.insert(0, " | ".join(self.data.get("languages", [])))
        self.lang_entry.pack(anchor="w", pady=(0, 15))

        self.update_live_preview()

    def extract_form_data(self):
        return {
            "header": {k: ent.get().strip() for k, ent in self.hdr_entries.items()},
            "summary": self.summary_text.get("1.0", tk.END).strip(),
            "competencies": [line.strip() for line in self.comp_text.get("1.0", tk.END).strip().split("\n") if line.strip()],
            "experience": [
                {
                    "company": item["company"].get().strip(),
                    "role": item["role"].get().strip(),
                    "meta": item["meta"].get().strip(),
                    "bullets": [b.strip() for b in item["bullets"].get("1.0", tk.END).strip().split("\n") if b.strip()]
                }
                for item in self.work_entries
            ],
            "education": [line.strip() for line in self.edu_text.get("1.0", tk.END).strip().split("\n") if line.strip()],
            "publications_and_achievements": [line.strip() for line in self.achieve_text.get("1.0", tk.END).strip().split("\n") if line.strip()],
            "languages": [l.strip() for l in self.lang_entry.get().split("|") if l.strip()]
        }

    def build_pdf_bytes(self):
        data = self.extract_form_data()
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        story = []

        styles = getSampleStyleSheet()
        name_style = ParagraphStyle('Name', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=15, leading=17, alignment=TA_CENTER)
        subhead_style = ParagraphStyle('SubHead', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=12, alignment=TA_CENTER, textColor=colors.HexColor('#1A2B4C'))
        contact_style = ParagraphStyle('Contact', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=11, alignment=TA_CENTER)
        sec_heading = ParagraphStyle('SecHeading', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=colors.HexColor('#1A2B4C'), spaceBefore=6, spaceAfter=2)
        job_title_style = ParagraphStyle('JobTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=11)
        job_sub_style = ParagraphStyle('JobSub', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8, leading=10, textColor=colors.HexColor('#444444'))
        body_style = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=11)
        bullet_style = ParagraphStyle('Bullet', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=11, leftIndent=10)

        def add_heading(title):
            story.append(Paragraph(title.upper(), sec_heading))
            story.append(HRFlowable(width="100%", thickness=0.7, color=colors.HexColor('#1A2B4C'), spaceBefore=1, spaceAfter=3))

        # Header
        hdr = data.get("header", {})
        story.append(Paragraph(hdr.get("name", ""), name_style))
        story.append(Spacer(1, 2))
        story.append(Paragraph(hdr.get("title", ""), subhead_style))
        story.append(Spacer(1, 2))
        c_info = f"{hdr.get('location', '')} | {hdr.get('phone', '')} | {hdr.get('email', '')} | {hdr.get('linkedin', '')}"
        story.append(Paragraph(c_info, contact_style))
        story.append(Spacer(1, 4))

        # Summary
        if data.get("summary"):
            add_heading("Professional Summary")
            story.append(Paragraph(data["summary"].replace("\n", "<br/>"), body_style))

        # Competencies
        if data.get("competencies"):
            add_heading("Core Competencies")
            for comp in data["competencies"]:
                story.append(Paragraph(f"• {comp}", bullet_style))

        # Experience
        if data.get("experience"):
            add_heading("Professional Experience")
            for job in data["experience"]:
                story.append(Paragraph(f"<b>{job.get('company', '')}</b> — {job.get('role', '')}", job_title_style))
                story.append(Paragraph(job.get('meta', ''), job_sub_style))
                for b in job.get("bullets", []):
                    story.append(Paragraph(f"• {b}", bullet_style))
                story.append(Spacer(1, 3))

        # Education
        if data.get("education"):
            add_heading("Education")
            for edu in data["education"]:
                story.append(Paragraph(f"• {edu}", body_style))

        # Achievements
        if data.get("publications_and_achievements"):
            add_heading("Publications & Achievements")
            for ach in data["publications_and_achievements"]:
                story.append(Paragraph(f"• {ach}", bullet_style))

        # Languages
        if data.get("languages"):
            add_heading("Languages")
            story.append(Paragraph(" | ".join(data["languages"]), body_style))

        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

    def update_live_preview(self):
        try:
            # Update JSON tab content without switching tabs
            if hasattr(self, 'json_text'):
                try:
                    self.json_text.delete("1.0", tk.END)
                    self.json_text.insert("1.0", json.dumps(self.extract_form_data(), indent=2, ensure_ascii=False))
                except Exception:
                    pass

            pdf_bytes = self.build_pdf_bytes()

            # Render PDF pages to images and show in preview frame
            pdf_doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            num_pages = len(pdf_doc)
            self.page_label.config(text=f"Total Pages: {num_pages}")

            # Clear previous preview
            for w in self.preview_frame.winfo_children():
                w.destroy()
            self.preview_images = []

            for idx in range(num_pages):
                page = pdf_doc.load_page(idx)
                base = 1.5
                scale = base * self.preview_scale
                pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                # Resize for display while preserving aspect
                max_w = int(850 * self.preview_scale)
                max_h = int(1200 * self.preview_scale)
                img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.preview_images.append(photo)

                p_label = tk.Label(self.preview_frame, text=f"Page {idx + 1} of {num_pages}", font=("Helvetica", 9, "bold"), bg="#525659", fg="white")
                p_label.pack(anchor="center", pady=(10, 2))

                img_label = tk.Label(self.preview_frame, image=photo, bg="#525659")
                img_label.pack(anchor="center", pady=(0, 10))

            pdf_doc.close()

            # Update PDF-only window if open
            if self.pdf_only_win is not None:
                try:
                    self._update_pdf_only_window(pdf_bytes)
                except Exception:
                    pass

        except Exception as e:
            self.page_label.config(text=f"Total Pages: Error ({e})")

    def _show_json_tab(self):
        # Alias for button
        self._open_json_editor()

    def _apply_json_from_tab(self):
        raw = self.json_text.get("1.0", tk.END).strip()
        if not raw:
            messagebox.showwarning("Empty", "JSON text is empty.")
            return
        try:
            parsed = json.loads(raw)
        except Exception as e:
            messagebox.showerror("JSON Error", f"Failed to parse JSON: {e}")
            return
        if not isinstance(parsed, dict):
            messagebox.showerror("JSON Error", "Top-level JSON must be an object/dictionary.")
            return
        self.data = parsed
        self.populate_form()
        self.update_live_preview()
        messagebox.showinfo("Applied", "JSON applied to form successfully.")

    def _open_pdf_only_window(self):
        # Bring existing window to front if exists
        if getattr(self, 'pdf_only_win', None):
            try:
                self.pdf_only_win.lift()
                return
            except Exception:
                self.pdf_only_win = None

        self.pdf_only_win = tk.Toplevel(self.root)
        self.pdf_only_win.title("PDF Only View")
        # larger default size for comfortable viewing
        self.pdf_only_win.geometry("1300x900")

        canvas = tk.Canvas(self.pdf_only_win, bg="#333333")
        vbar = ttk.Scrollbar(self.pdf_only_win, orient=tk.VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=vbar.set)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        frame = tk.Frame(canvas, bg="#333333")
        canvas.create_window((0, 0), window=frame, anchor="nw")

        def _on_config(e):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame.bind("<Configure>", _on_config)

        self.pdf_only_canvas = canvas
        self.pdf_only_frame = frame
        self.pdf_only_images = []

        # Render current PDF into the new window
        try:
            pdf_bytes = self.build_pdf_bytes()
            self._update_pdf_only_window(pdf_bytes)
        except Exception:
            pass

        def on_close():
            try:
                self.pdf_only_win.destroy()
            finally:
                self.pdf_only_win = None

        self.pdf_only_win.protocol("WM_DELETE_WINDOW", on_close)

    def _update_pdf_only_window(self, pdf_bytes):
        if getattr(self, 'pdf_only_win', None) is None:
            return
        try:
            for w in self.pdf_only_frame.winfo_children():
                w.destroy()
            self.pdf_only_images = []

            pdf_doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            for idx in range(len(pdf_doc)):
                page = pdf_doc.load_page(idx)
                pix = page.get_pixmap(matrix=fitz.Matrix(2.0 * self.preview_scale, 2.0 * self.preview_scale))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                photo = ImageTk.PhotoImage(img)
                self.pdf_only_images.append(photo)

                p_label = tk.Label(self.pdf_only_frame, text=f"Page {idx+1}", font=("Helvetica", 10, "bold"), bg="#333333", fg="white")
                p_label.pack(anchor="center", pady=(10, 2))
                img_label = tk.Label(self.pdf_only_frame, image=photo, bg="#333333")
                img_label.pack(anchor="center", pady=(0, 10))

            pdf_doc.close()
        except Exception:
            pass

    def _on_ctrl_wheel_preview(self, event):
        # Ctrl + MouseWheel: zoom in/out
        if event.delta > 0:
            self._zoom_in()
        else:
            self._zoom_out()
        return "break"

    def _on_editor_mousewheel(self, event):
        move = int(-1 * (event.delta / 120))
        self.editor_canvas.yview_scroll(move, "units")

    def _global_undo(self, event):
        w = event.widget
        try:
            if isinstance(w, tk.Text):
                w.edit_undo()
                return "break"
        except Exception:
            pass

    def _global_redo(self, event):
        w = event.widget
        try:
            if isinstance(w, tk.Text):
                w.edit_redo()
                return "break"
        except Exception:
            pass

    # --- Zoom controls ---
    def _zoom_in(self):
        self.preview_scale = min(self.preview_scale + 0.1, 3.0)
        self.zoom_label.config(text=f"{int(self.preview_scale*100)}%")
        self.update_live_preview()

    def _zoom_out(self):
        self.preview_scale = max(self.preview_scale - 0.1, 0.3)
        self.zoom_label.config(text=f"{int(self.preview_scale*100)}%")
        self.update_live_preview()

    def _zoom_reset(self):
        self.preview_scale = 1.0
        self.zoom_label.config(text="100%")
        self.update_live_preview()

    # --- Section maximize / popup editors ---
    def _add_section_header(self, parent, text, open_callback):
        f = ttk.Frame(parent)
        f.pack(fill=tk.X, pady=(5, 2))
        ttk.Label(f, text=text, font=("Helvetica", 11, "bold")).pack(side=tk.LEFT, anchor="w")
        ttk.Button(f, text="Open", command=open_callback).pack(side=tk.RIGHT)

    def _open_text_editor(self, key, title):
        # key maps to self.data keys; show a large Text widget and update on close
        top = tk.Toplevel(self.root)
        top.title(title)
        top.geometry("800x600")
        txt = tk.Text(top, wrap=tk.WORD)
        # fill with current content
        if key == "competencies":
            txt.insert("1.0", "\n".join(self.data.get(key, [])))
        elif key == "languages":
            txt.insert("1.0", "\n".join(self.data.get(key, [])))
        else:
            val = self.data.get(key, "")
            if isinstance(val, list):
                txt.insert("1.0", "\n".join(val))
            else:
                txt.insert("1.0", val)
        txt.pack(fill=tk.BOTH, expand=True)

        def save_and_close():
            content = txt.get("1.0", tk.END).strip()
            if key == "competencies":
                self.comp_text.delete("1.0", tk.END)
                self.comp_text.insert("1.0", content)
            elif key == "languages":
                self.lang_entry.delete(0, tk.END)
                self.lang_entry.insert(0, " | ".join([l.strip() for l in content.splitlines() if l.strip()]))
            elif key == "education":
                self.edu_text.delete("1.0", tk.END)
                self.edu_text.insert("1.0", content)
            elif key == "publications_and_achievements":
                self.achieve_text.delete("1.0", tk.END)
                self.achieve_text.insert("1.0", content)
            elif key == "summary":
                self.summary_text.delete("1.0", tk.END)
                self.summary_text.insert("1.0", content)
            else:
                # generic replace
                if isinstance(self.data.get(key, None), list):
                    # update relevant widget if present
                    pass
            # reflect in data and preview
            self.data = self.extract_form_data()
            self.update_live_preview()
            top.destroy()

        btn = ttk.Button(top, text="Save & Close", command=save_and_close)
        btn.pack(pady=6)

    def _open_header_editor(self):
        top = tk.Toplevel(self.root)
        top.title("Header Editor")
        top.geometry("700x300")
        entries = {}
        hdr = self.extract_form_data().get("header", {})
        for key in ["name", "title", "location", "phone", "email", "linkedin"]:
            f = ttk.Frame(top)
            f.pack(fill=tk.X, pady=3, padx=6)
            ttk.Label(f, text=f"{key.capitalize()}:", width=12).pack(side=tk.LEFT)
            ent = ttk.Entry(f)
            ent.insert(0, hdr.get(key, ""))
            ent.pack(side=tk.LEFT, fill=tk.X, expand=True)
            entries[key] = ent

        def save_hdr():
            for k, e in entries.items():
                self.hdr_entries[k].delete(0, tk.END)
                self.hdr_entries[k].insert(0, e.get())
            self.data = self.extract_form_data()
            self.update_live_preview()
            top.destroy()

        ttk.Button(top, text="Save & Close", command=save_hdr).pack(pady=6)

    def _open_job_editor(self, job, parent_frame):
        # find index of job in data
        idx = None
        for i, j in enumerate(self.data.get("experience", [])):
            if j.get("company") == job.get("company") and j.get("role") == job.get("role"):
                idx = i
                break
        if idx is None:
            messagebox.showerror("Error", "Could not locate the job entry to edit.")
            return

        top = tk.Toplevel(self.root)
        top.title(job.get("company", "Job Editor"))
        top.geometry("800x500")

        f1 = ttk.Frame(top); f1.pack(fill=tk.X, pady=4, padx=6)
        ttk.Label(f1, text="Company:", width=12).pack(side=tk.LEFT)
        comp_e = tk.Entry(f1); comp_e.insert(0, job.get("company", "")); comp_e.pack(side=tk.LEFT, fill=tk.X, expand=True)

        f2 = ttk.Frame(top); f2.pack(fill=tk.X, pady=4, padx=6)
        ttk.Label(f2, text="Role:", width=12).pack(side=tk.LEFT)
        role_e = tk.Entry(f2); role_e.insert(0, job.get("role", "")); role_e.pack(side=tk.LEFT, fill=tk.X, expand=True)

        f3 = ttk.Frame(top); f3.pack(fill=tk.X, pady=4, padx=6)
        ttk.Label(f3, text="Meta:", width=12).pack(side=tk.LEFT)
        meta_e = tk.Entry(f3); meta_e.insert(0, job.get("meta", "")); meta_e.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(top, text="Bullets (one per line):").pack(anchor="w", padx=6)
        bullets_txt = tk.Text(top, height=12)
        bullets_txt.insert("1.0", "\n".join(job.get("bullets", [])))
        bullets_txt.pack(fill=tk.BOTH, expand=True, padx=6, pady=4)

        def save_job():
            self.data["experience"][idx]["company"] = comp_e.get().strip()
            self.data["experience"][idx]["role"] = role_e.get().strip()
            self.data["experience"][idx]["meta"] = meta_e.get().strip()
            self.data["experience"][idx]["bullets"] = [b.strip() for b in bullets_txt.get("1.0", tk.END).strip().splitlines() if b.strip()]
            # repopulate form to reflect updated labels and values
            self.populate_form()
            self.update_live_preview()
            top.destroy()

        ttk.Button(top, text="Save & Close", command=save_job).pack(pady=6)

    def _global_save_json(self, event=None):
        # quick save JSON via Ctrl+S; reuse save_json logic
        try:
            self.save_json()
        except Exception as e:
            messagebox.showerror("Save Error", str(e))
        return "break"

    def _open_json_editor(self):
        top = tk.Toplevel(self.root)
        top.title("JSON Editor")
        # reduced size per user request
        top.geometry("700x500")

        # horizontal and vertical scrollbars
        vbar = ttk.Scrollbar(top, orient=tk.VERTICAL)
        hbar = ttk.Scrollbar(top, orient=tk.HORIZONTAL)
        txt = tk.Text(top, wrap=tk.NONE, undo=True, xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        vbar.config(command=txt.yview)
        hbar.config(command=txt.xview)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        txt.pack(fill=tk.BOTH, expand=True)

        # prefill with current data
        try:
            txt.delete("1.0", tk.END)
            txt.insert("1.0", json.dumps(self.extract_form_data(), indent=2, ensure_ascii=False))
        except Exception:
            txt.insert("1.0", "{}")

        btn_frame = ttk.Frame(top)
        btn_frame.pack(fill=tk.X, pady=6)

        def apply_json():
            raw = txt.get("1.0", tk.END).strip()
            if not raw:
                messagebox.showwarning("Empty", "JSON text is empty.")
                return
            try:
                parsed = json.loads(raw)
            except Exception as e:
                messagebox.showerror("JSON Error", f"Failed to parse JSON: {e}")
                return
            # Basic validation: must be a dict with expected keys optional
            if not isinstance(parsed, dict):
                messagebox.showerror("JSON Error", "Top-level JSON must be an object/dictionary.")
                return
            # update internal data and repopulate form
            self.data = parsed
            self.populate_form()
            self.update_live_preview()
            messagebox.showinfo("Applied", "JSON applied to form successfully.")

        ttk.Button(btn_frame, text="Apply JSON", command=apply_json).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_frame, text="Save JSON to file", command=lambda: self._save_text_to_file(txt)).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_frame, text="Close", command=top.destroy).pack(side=tk.RIGHT, padx=6)

    def _save_text_to_file(self, text_widget):
        filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text_widget.get("1.0", tk.END))

    def load_json(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if filepath:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            self.populate_form()

    def save_json(self):
        name = self.filename_entry.get().strip() if hasattr(self, 'filename_entry') else ""
        if name:
            folder = filedialog.askdirectory(title="Choose folder to save JSON")
            if folder:
                filepath = f"{folder}/{name}.json"
            else:
                return
        else:
            filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])

        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.extract_form_data(), f, indent=2)

    def generate_pdf(self):
        name = self.filename_entry.get().strip() if hasattr(self, 'filename_entry') else ""
        if name:
            folder = filedialog.askdirectory(title="Choose folder to save PDF and JSON")
            if not folder:
                return
            pdf_path = f"{folder}/{name}.pdf"
            json_path = f"{folder}/{name}.json"
            pdf_bytes = self.build_pdf_bytes()
            with open(pdf_path, "wb") as f:
                f.write(pdf_bytes)
            # also save JSON representation
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(self.extract_form_data(), f, indent=2)
            self.update_live_preview()
            messagebox.showinfo("Success", f"Saved {name}.pdf and {name}.json to {folder}")
        else:
            filepath = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
            if filepath:
                pdf_bytes = self.build_pdf_bytes()
                with open(filepath, "wb") as f:
                    f.write(pdf_bytes)
                self.update_live_preview()
                messagebox.showinfo("Success", "PDF exported successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeApp(root)
    root.mainloop()