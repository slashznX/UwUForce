import ctypes
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance
import zipfile
import itertools
import threading
import string
import time
import random
import os
import queue
import multiprocessing
import psutil
import shutil

try:
    import GPUtil
    HAS_GPU = True
except Exception:
    HAS_GPU = False

BG = "#181a1b"
BG2 = "#1b1f22"
FG = "#e8e6e3"
MUTED = "#c2a0bd"
RULE = "#5e3a4d"
PINK = "#ff9ec9"
PINK_D = "#ff6fae"
BLUE = "#9ad4ff"
BLUE_D = "#6fc1f7"
CARD = "#1f2224"
WARN = "#ff7a9c"
GREEN = "#00ff88"
FONT = ("Comic Sans MS", 10)
FONT_BOLD = ("Comic Sans MS", 10, "bold")
FONT_TITLE = ("Comic Sans MS", 20, "bold")
FONT_SUB = ("Comic Sans MS", 8)
FONT_MONO = ("Consolas", 9)
FONT_MONO_SM = ("Consolas", 8)
FONT_BIG = ("Comic Sans MS", 13, "bold")

WAIFU_DIR = "waifus"
WAIFU_FILES = [
    "anime-angel-angels-f4fedc8bdece753d52194942c9208a0c.png",
    "anime-catgirl-female-manga-anime-5f05a0d6d2365127d56b3201347bb931.png",
    "anime-female-manga-deviantart-anime-c21040575c55246776c9eaa04358e794.png",
    "anime-girl-desktop-wallpaper-deviantart-cute-girl-e106054dd70335cdbb959d7df059c792.png",
    "anime-tsundere-manga-yandere-anime-e0c76b7422d8e70fdf5341da4c533320.png",
    "black-hair-hime-cut-art-long-hair-asuna-c6ea18bb84fcb8462a74dd7ebc891a26.png",
    "catgirl-anime-cosplay-drawing-anime-girl-f34129e138c3da47bf75cab82eaddf35.png",
    "catgirl-anime-kemonomimi-ecchi-maneki-neko-b19029eac52c94818becb18638400ffd.png",
    "danganronpa-trigger-happy-havoc-desktop-wallpaper-anime-cute-girl-be9a0be822c44b3e5f11acca1109f537.png",
    "kashiwazaki-deviantart-haganai-anime-quiet-girl-e594b796e3385ff299acb51a3b4b4ee8.png",
    "nekopara-chocolate-neko-works-anime-catgirl-vanilla-65acdf9d7b8748c148f4a807beba93eb.png",
]
FALLBACK_WAIFU = "catgirl-anime-manga-cat-5b251b20bbdb5ad6533b7a68ba2954ad.png"

LANGS = {
    "English": {
        "subtitle": "zip password recovery ~ nyaa~",
        "zip_file": "ZIP File:", "select": "Select",
        "no_file": "no file selected...",
        "charset": " Charset ", "lower": "abc  Lowercase (a-z)",
        "upper": "ABC  Uppercase (A-Z)", "digits": "123  Numbers (0-9)",
        "special": "@#$  Special (!@#$%...)", "space": "       Space",
        "pwd_len": "Password length:", "threads": "Threads:",
        "auto": "Auto", "detected": "detected", "cores": "cores",
        "estimate": " Estimate ", "charset_size": "Charset:",
        "combinations": "Combinations:", "est_time": "Estimated time:",
        "start": "START", "stop": "STOP",
        "waiting": "waiting...", "attacking": "attacking...",
        "remaining": "remaining",
        "found": "PASSWORD FOUND:", "found_status": "FOUND! nyaa~!",
        "exhausted": "all combinations tested... not found",
        "stopped": "stopped by user", "chars": "characters",
        "select_warn": "Select a ZIP file first! (>_<)",
        "charset_warn": "Select at least one character type! uwu",
        "len_warn": "Invalid password length!",
        "zip_err": "Invalid ZIP file:",
        "starting": "starting attack with", "threads_log": "threads",
        "chars_log": "chars", "size_log": "size", "combos_log": "combos",
        "attack_stopped": "attack stopped.",
        "total_time": "total time:", "attempts_lbl": "attempts:",
        "time_lbl": "time:", "instant": "instant",
        "good_luck": "good luck uwu",
        "seconds": "seconds", "minutes": "minutes", "hours": "hours",
        "days": "days", "months": "months", "years": "years",
        "select_chars": "select something!",
        "file_selected": "file selected:",
        "exhausted_log": "search space exhausted.",
        "lang": "Language:",
        "mascot_text": "~ nyaa~ good luck! ~",
        "mask": " Known Chars ",
        "mask_hint": "# = unknown",
        "mask_preview": "Mask:",
        "unknown_pos": "unknown",
        "after_find": "After find:",
        "notif": "Notification",
        "extract": "Extract ZIP",
        "pop_out": "Pop Out",
        "dock": "Dock",
        "copy_pwd": "Copy Password ~uwu~",
        "extract_btn": "Extract Files",
        "dismiss": "Dismiss",
        "extracted_to": "extracted to:",
        "extract_fail": "extraction failed:",
        "extract_done": "files extracted!",
    },
    "Portugues": {
        "subtitle": "recuperador de senha zip ~ nyaa~",
        "zip_file": "Arquivo ZIP:", "select": "Selecionar",
        "no_file": "nenhum arquivo selecionado...",
        "charset": " Charset ", "lower": "abc  Minusculas (a-z)",
        "upper": "ABC  Maiusculas (A-Z)", "digits": "123  Numeros (0-9)",
        "special": "@#$  Especiais (!@#$%...)", "space": "       Espaco",
        "pwd_len": "Tamanho da senha:", "threads": "Threads:",
        "auto": "Auto", "detected": "detectado", "cores": "cores",
        "estimate": " Estimativa ", "charset_size": "Charset:",
        "combinations": "Combinacoes:", "est_time": "Tempo estimado:",
        "start": "INICIAR", "stop": "PARAR",
        "waiting": "esperando...", "attacking": "atacando...",
        "remaining": "restante",
        "found": "SENHA ENCONTRADA:", "found_status": "ENCONTROU! nyaa~!",
        "exhausted": "todas combinacoes testadas... nao encontrada",
        "stopped": "parado pelo usuario", "chars": "caracteres",
        "select_warn": "Selecione um arquivo ZIP primeiro! (>_<)",
        "charset_warn": "Selecione pelo menos um tipo de caractere! uwu",
        "len_warn": "Tamanho de senha invalido!",
        "zip_err": "Arquivo ZIP invalido:",
        "starting": "iniciando ataque com", "threads_log": "threads",
        "chars_log": "chars", "size_log": "tamanho", "combos_log": "combos",
        "attack_stopped": "ataque interrompido.",
        "total_time": "tempo total:", "attempts_lbl": "tentativas:",
        "time_lbl": "tempo:", "instant": "instantaneo",
        "good_luck": "boa sorte uwu",
        "seconds": "segundos", "minutes": "minutos", "hours": "horas",
        "days": "dias", "months": "meses", "years": "anos",
        "select_chars": "selecione algo!",
        "file_selected": "arquivo selecionado:",
        "exhausted_log": "espaco de busca esgotado.",
        "lang": "Idioma:",
        "mascot_text": "~ nyaa~ boa sorte! ~",
        "mask": " Chars Conhecidos ",
        "mask_hint": "# = desconhecido",
        "mask_preview": "Mascara:",
        "unknown_pos": "desconhecidos",
        "after_find": "Apos encontrar:",
        "notif": "Notificacao",
        "extract": "Extrair ZIP",
        "pop_out": "Destacar",
        "dock": "Fixar",
        "copy_pwd": "Copiar Senha ~uwu~",
        "extract_btn": "Extrair Arquivos",
        "dismiss": "Fechar",
        "extracted_to": "extraido em:",
        "extract_fail": "falha na extracao:",
        "extract_done": "arquivos extraidos!",
    },
    "Russian": {
        "subtitle": "vosstanovleniye parolya zip ~ nyaa~",
        "zip_file": "ZIP Fayl:", "select": "Vybrat'",
        "no_file": "fayl ne vybran...",
        "charset": " Charset ", "lower": "abc  Strochnyye (a-z)",
        "upper": "ABC  Zaglavnyye (A-Z)", "digits": "123  Tsifry (0-9)",
        "special": "@#$  Spetsial'nyye (!@#$%...)", "space": "       Probel",
        "pwd_len": "Dlina parolya:", "threads": "Potoki:",
        "auto": "Avto", "detected": "obnaruzheno", "cores": "yader",
        "estimate": " Otsenka ", "charset_size": "Charset:",
        "combinations": "Kombinatsii:", "est_time": "Otsenochnoe vremya:",
        "start": "ZAPUSK", "stop": "STOP",
        "waiting": "ozhidaniye...", "attacking": "ataka...",
        "remaining": "ostalos'",
        "found": "PAROL' NAYDEN:", "found_status": "NASHLI! nyaa~!",
        "exhausted": "vse kombinatsii provyereny... ne nayden",
        "stopped": "ostanovleno pol'zovatelem", "chars": "simvolov",
        "select_warn": "Snachala vyberite ZIP fayl! (>_<)",
        "charset_warn": "Vyberite khotya by odin tip simvolov! uwu",
        "len_warn": "Nevernaya dlina parolya!",
        "zip_err": "Nevernyy ZIP fayl:",
        "starting": "zapusk ataki s", "threads_log": "potokami",
        "chars_log": "chars", "size_log": "razmer", "combos_log": "kombo",
        "attack_stopped": "ataka ostanovlena.",
        "total_time": "obsheye vremya:", "attempts_lbl": "popytki:",
        "time_lbl": "vremya:", "instant": "mgnovenno",
        "good_luck": "udachi uwu",
        "seconds": "sekund", "minutes": "minut", "hours": "chasov",
        "days": "dney", "months": "mesyatsev", "years": "let",
        "select_chars": "vyberite chto-nibud'!",
        "file_selected": "fayl vybran:",
        "exhausted_log": "prostranstvo poiska ischerpano.",
        "lang": "Yazyk:",
        "mascot_text": "~ nyaa~ udachi! ~",
        "mask": " Izvestnyye simvoly ",
        "mask_hint": "# = neizvestno",
        "mask_preview": "Maska:",
        "unknown_pos": "neizvestnykh",
        "after_find": "Posle nahozhdeniya:",
        "notif": "Uvedomleniye",
        "extract": "Raspakovat' ZIP",
        "pop_out": "Otdelit'",
        "dock": "Zakrepit'",
        "copy_pwd": "Kopirovat' parol' ~uwu~",
        "extract_btn": "Raspakovat' fayly",
        "dismiss": "Zakryt'",
        "extracted_to": "raspakovan v:",
        "extract_fail": "oshibka raspakovki:",
        "extract_done": "fayly raspakovany!",
    },
    "Chinese": {
        "subtitle": "zip mima huifu ~ nyaa~",
        "zip_file": "ZIP wenjian:", "select": "Xuanze",
        "no_file": "wei xuanze wenjian...",
        "charset": " Charset ", "lower": "abc  Xiaoxie (a-z)",
        "upper": "ABC  Daxie (A-Z)", "digits": "123  Shuzi (0-9)",
        "special": "@#$  Teshu (!@#$%...)", "space": "       Kongge",
        "pwd_len": "Mima changdu:", "threads": "Xiancheng:",
        "auto": "Zidong", "detected": "jiance dao", "cores": "he",
        "estimate": " Guji ", "charset_size": "Charset:",
        "combinations": "Zuhe:", "est_time": "Guji shijian:",
        "start": "KAISHI", "stop": "TINGZHI",
        "waiting": "dengdai...", "attacking": "gongji zhong...",
        "remaining": "shengyu",
        "found": "MIMA ZHAODAO:", "found_status": "ZHAODAO LE! nyaa~!",
        "exhausted": "suoyou zuhe yi ceshi... wei zhaodao",
        "stopped": "yonghu tingzhi", "chars": "zifu",
        "select_warn": "Qing xian xuanze ZIP wenjian! (>_<)",
        "charset_warn": "Qing xuanze zhishao yizhong zifu leixing! uwu",
        "len_warn": "Mima changdu wuxiao!",
        "zip_err": "Wuxiao ZIP wenjian:",
        "starting": "kaishi gongji, xiancheng:", "threads_log": "",
        "chars_log": "chars", "size_log": "changdu", "combos_log": "zuhe",
        "attack_stopped": "gongji yi tingzhi.",
        "total_time": "zong shijian:", "attempts_lbl": "changshi:",
        "time_lbl": "shijian:", "instant": "shunshi",
        "good_luck": "zhu ni hao yun uwu",
        "seconds": "miao", "minutes": "fenzhong", "hours": "xiaoshi",
        "days": "tian", "months": "ge yue", "years": "nian",
        "select_chars": "qing xuanze!",
        "file_selected": "wenjian yi xuanze:",
        "exhausted_log": "sousuo kongjian yijing yongwan.",
        "lang": "Yuyan:",
        "mascot_text": "~ nyaa~ zhu ni hao yun! ~",
        "mask": " Yizhi zifu ",
        "mask_hint": "# = weizhi",
        "mask_preview": "Yanma:",
        "unknown_pos": "weizhi",
        "after_find": "Zhaodao hou:",
        "notif": "Tongzhi",
        "extract": "Jieya ZIP",
        "pop_out": "Tanchu",
        "dock": "Guding",
        "copy_pwd": "Fuzhi mima ~uwu~",
        "extract_btn": "Jieya wenjian",
        "dismiss": "Guanbi",
        "extracted_to": "jieya dao:",
        "extract_fail": "jieya shibai:",
        "extract_done": "wenjian yi jieya!",
    },
}


def smart_thread_count():
    cores = multiprocessing.cpu_count()
    try:
        mem_gb = psutil.virtual_memory().total / (1024 ** 3)
    except Exception:
        mem_gb = 4
    thread_per_core = 2 if mem_gb >= 8 else 1
    return max(2, min(cores * thread_per_core, 64))


class UwUForce:
    def __init__(self, root):
        self.root = root
        self.root.title("UwUForce")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.running = False
        self.found_password = None
        self.attempts = 0
        self.start_time = 0
        self.total_combinations = 0
        self.msg_queue = queue.Queue()
        self.current_lang = "English"
        self.zip_path = ""
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.mask_vars = []
        self.mask_entries = []
        self.live_speed = 0
        self.process = psutil.Process(os.getpid())
        self.log_floating = False
        self.log_window = None
        self.found_banner = None

        self._setup_styles()
        self._build_ui()
        self._load_bg_waifu()
        self._rebuild_mask_slots()
        self.update_estimate()
        self.root.after(50, self._process_queue)
        self._start_hw_monitor()

    def t(self, key):
        return LANGS[self.current_lang].get(key, key)

    def _setup_styles(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("Card.TCheckbutton", background=CARD, foreground=FG, font=FONT)
        s.map("Card.TCheckbutton", background=[("active", CARD)], foreground=[("active", PINK_D)])
        s.configure("Start.TButton", background=PINK_D, foreground=BG, font=FONT_BOLD, padding=(20, 8))
        s.map("Start.TButton", background=[("active", PINK), ("disabled", RULE)])
        s.configure("Stop.TButton", background=WARN, foreground="#fff", font=FONT_BOLD, padding=(20, 8))
        s.map("Stop.TButton", background=[("active", "#ff8ca8"), ("disabled", RULE)])
        s.configure("File.TButton", background=RULE, foreground=PINK, font=("Comic Sans MS", 9), padding=(12, 4))
        s.map("File.TButton", background=[("active", "#7a4a60")])
        s.configure("pink.Horizontal.TProgressbar", troughcolor=BG2, background=PINK_D,
                     darkcolor=PINK_D, lightcolor=PINK, bordercolor=BG)

    def _build_ui(self):
        self.bg_canvas = tk.Canvas(self.root, bg=BG, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        outer = tk.Frame(self.root, bg=BG)
        outer.place(x=15, y=10, relwidth=1, relheight=1)

        header = tk.Frame(outer, bg=BG)
        header.pack(fill="x", padx=(0, 30), pady=(0, 2))
        tl = tk.Frame(header, bg=BG)
        tl.pack(side="left")
        tk.Label(tl, text="UwU", bg=BG, fg=PINK_D, font=("Comic Sans MS", 22, "bold")).pack(side="left")
        tk.Label(tl, text="Force", bg=BG, fg=BLUE_D, font=("Comic Sans MS", 22, "bold")).pack(side="left")

        lf = tk.Frame(header, bg=BG)
        lf.pack(side="right", pady=(6, 0))
        self.lang_label = tk.Label(lf, text="Language:", bg=BG, fg=MUTED, font=FONT_SUB)
        self.lang_label.pack(side="left", padx=(0, 4))
        self.lang_var = tk.StringVar(value="English")
        self.lang_combo = ttk.Combobox(lf, textvariable=self.lang_var, values=list(LANGS.keys()),
                                       state="readonly", width=10, font=("Comic Sans MS", 9))
        self.lang_combo.pack(side="left")
        self.lang_combo.bind("<<ComboboxSelected>>", self._change_lang)

        self.subtitle_label = tk.Label(outer, bg=BG, fg=MUTED, font=FONT_SUB, text=self.t("subtitle"))
        self.subtitle_label.pack(anchor="w", pady=(0, 4))

        hr = tk.Canvas(outer, height=2, bg=BG, highlightthickness=0, width=880)
        hr.pack(anchor="w", pady=(0, 6))
        hr.create_line(0, 1, 880, 1, fill=RULE, dash=(6, 4), width=2)

        content = tk.Frame(outer, bg=BG)
        content.pack(fill="both", expand=True)

        self.left = tk.Frame(content, bg=BG)
        self.left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right = tk.Frame(content, bg=BG)
        right.pack(side="right", fill="y", padx=(0, 20))

        left = self.left

        # --- file ---
        fc = self._card(left)
        fi = tk.Frame(fc, bg=CARD)
        fi.pack(fill="x")
        self.file_label = tk.Label(fi, text=self.t("zip_file"), bg=CARD, fg=PINK_D, font=FONT_BOLD)
        self.file_label.pack(side="left")
        self.file_path_var = tk.StringVar(value=self.t("no_file"))
        tk.Label(fi, textvariable=self.file_path_var, bg=CARD, fg=MUTED, font=FONT).pack(side="left", padx=(8, 8))
        self.select_btn = ttk.Button(fi, text=self.t("select"), style="File.TButton", command=self.select_file)
        self.select_btn.pack(side="right")

        # --- charset ---
        cc = self._card(left)
        self.charset_title = tk.Label(cc, text=self.t("charset"), bg=CARD, fg=PINK_D, font=FONT_BOLD)
        self.charset_title.pack(anchor="w", pady=(0, 2))
        self.use_lower = tk.BooleanVar(value=True)
        self.use_upper = tk.BooleanVar(value=False)
        self.use_digits = tk.BooleanVar(value=False)
        self.use_special = tk.BooleanVar(value=False)
        self.use_space = tk.BooleanVar(value=False)
        cbs = [
            ("lower", self.use_lower), ("upper", self.use_upper),
            ("digits", self.use_digits), ("special", self.use_special),
            ("space", self.use_space),
        ]
        self.charset_cbs = {}
        for key, var in cbs:
            cb = ttk.Checkbutton(cc, text=self.t(key), variable=var, style="Card.TCheckbutton",
                                 command=self.update_estimate)
            cb.pack(anchor="w", padx=8, pady=0)
            self.charset_cbs[key] = cb

        # --- settings ---
        sc = self._card(left)
        r1 = tk.Frame(sc, bg=CARD)
        r1.pack(fill="x", pady=(0, 4))
        self.len_label = tk.Label(r1, text=self.t("pwd_len"), bg=CARD, fg=PINK_D, font=FONT_BOLD)
        self.len_label.pack(side="left")
        self.length_var = tk.IntVar(value=5)
        self.length_spin = tk.Spinbox(r1, from_=1, to=20, textvariable=self.length_var, width=4,
                                      font=("Comic Sans MS", 11), bg=BG2, fg=FG,
                                      buttonbackground=RULE, insertbackground=PINK_D,
                                      selectbackground=PINK_D, selectforeground=BG,
                                      highlightthickness=1, highlightcolor=RULE, relief="flat",
                                      command=self._on_length_change)
        self.length_spin.pack(side="left", padx=(8, 0))
        self.length_spin.bind("<KeyRelease>", lambda e: self._on_length_change())

        r2 = tk.Frame(sc, bg=CARD)
        r2.pack(fill="x")
        self.threads_label = tk.Label(r2, text=self.t("threads"), bg=CARD, fg=PINK_D, font=FONT_BOLD)
        self.threads_label.pack(side="left")
        self.auto_threads = tk.BooleanVar(value=True)
        self.auto_cb = ttk.Checkbutton(r2, text=self.t("auto"), variable=self.auto_threads,
                                       style="Card.TCheckbutton", command=self.toggle_thread_input)
        self.auto_cb.pack(side="left", padx=(8, 4))
        optimal = smart_thread_count()
        self.thread_var = tk.IntVar(value=optimal)
        self.thread_spin = tk.Spinbox(r2, from_=1, to=512, textvariable=self.thread_var, width=4,
                                      font=("Comic Sans MS", 11), bg=BG2, fg=FG,
                                      buttonbackground=RULE, insertbackground=PINK_D,
                                      selectbackground=PINK_D, selectforeground=BG,
                                      highlightthickness=1, highlightcolor=RULE, relief="flat",
                                      state="disabled")
        self.thread_spin.pack(side="left", padx=(4, 0))
        cpu_c = multiprocessing.cpu_count()
        self.thread_info_var = tk.StringVar(value=f"({optimal}t / {cpu_c}c)")
        tk.Label(r2, textvariable=self.thread_info_var, bg=CARD, fg=MUTED, font=FONT_SUB).pack(side="left", padx=(6, 0))

        # --- mask ---
        mc = self._card(left)
        mh = tk.Frame(mc, bg=CARD)
        mh.pack(fill="x", pady=(0, 3))
        self.mask_title = tk.Label(mh, text=self.t("mask"), bg=CARD, fg=PINK_D, font=FONT_BOLD)
        self.mask_title.pack(side="left")
        self.mask_hint_label = tk.Label(mh, text=self.t("mask_hint"), bg=CARD, fg=MUTED, font=FONT_SUB)
        self.mask_hint_label.pack(side="right")
        self.mask_slots_frame = tk.Frame(mc, bg=CARD)
        self.mask_slots_frame.pack(fill="x", pady=(0, 3))
        mp = tk.Frame(mc, bg=CARD)
        mp.pack(fill="x")
        self.mask_preview_label = tk.Label(mp, text=self.t("mask_preview"), bg=CARD, fg=MUTED, font=FONT)
        self.mask_preview_label.pack(side="left")
        self.mask_preview_var = tk.StringVar(value="#####")
        tk.Label(mp, textvariable=self.mask_preview_var, bg=CARD, fg=BLUE_D,
                 font=("Consolas", 13, "bold")).pack(side="left", padx=(6, 0))
        self.mask_unknown_var = tk.StringVar(value="")
        tk.Label(mp, textvariable=self.mask_unknown_var, bg=CARD, fg=MUTED, font=FONT_SUB).pack(side="right")

        # --- estimate + after find ---
        ec = self._card(left)
        est_row = tk.Frame(ec, bg=CARD)
        est_row.pack(fill="x")

        est_left = tk.Frame(est_row, bg=CARD)
        est_left.pack(side="left", fill="x", expand=True)
        self.est_title = tk.Label(est_left, text=self.t("estimate"), bg=CARD, fg=PINK_D, font=FONT_BOLD)
        self.est_title.pack(anchor="w", pady=(0, 2))
        eg = tk.Frame(est_left, bg=CARD)
        eg.pack(fill="x")
        self.est_charset_size = tk.StringVar(value="-")
        self.est_combinations = tk.StringVar(value="-")
        self.est_time = tk.StringVar(value="-")
        self.est_cs_label = tk.Label(eg, text=self.t("charset_size"), bg=CARD, fg=MUTED, font=FONT)
        self.est_cs_label.grid(row=0, column=0, sticky="w")
        tk.Label(eg, textvariable=self.est_charset_size, bg=CARD, fg=FG, font=FONT).grid(row=0, column=1, sticky="w", padx=(8, 0))
        self.est_comb_label = tk.Label(eg, text=self.t("combinations"), bg=CARD, fg=MUTED, font=FONT)
        self.est_comb_label.grid(row=1, column=0, sticky="w")
        tk.Label(eg, textvariable=self.est_combinations, bg=CARD, fg=FG, font=FONT).grid(row=1, column=1, sticky="w", padx=(8, 0))
        self.est_time_label = tk.Label(eg, text=self.t("est_time"), bg=CARD, fg=MUTED, font=FONT)
        self.est_time_label.grid(row=2, column=0, sticky="w")
        tk.Label(eg, textvariable=self.est_time, bg=CARD, fg=BLUE_D,
                 font=("Comic Sans MS", 11, "bold")).grid(row=2, column=1, sticky="w", padx=(8, 0))

        af_sep = tk.Frame(est_row, width=1, bg=RULE)
        af_sep.pack(side="left", fill="y", padx=(12, 12), pady=2)

        af_right = tk.Frame(est_row, bg=CARD)
        af_right.pack(side="left", fill="y")
        self.af_label = tk.Label(af_right, text=self.t("after_find"), bg=CARD, fg=PINK_D, font=FONT_BOLD)
        self.af_label.pack(anchor="w", pady=(0, 4))
        self.af_notif = tk.BooleanVar(value=True)
        self.af_extract = tk.BooleanVar(value=False)
        self.af_notif_cb = ttk.Checkbutton(af_right, text=self.t("notif"), variable=self.af_notif,
                                           style="Card.TCheckbutton")
        self.af_notif_cb.pack(anchor="w")
        self.af_extract_cb = ttk.Checkbutton(af_right, text=self.t("extract"), variable=self.af_extract,
                                             style="Card.TCheckbutton")
        self.af_extract_cb.pack(anchor="w")

        # --- buttons ---
        bf = tk.Frame(left, bg=BG)
        bf.pack(fill="x", pady=(0, 2))
        self.start_btn = ttk.Button(bf, text=self.t("start"), style="Start.TButton", command=self.start_attack)
        self.start_btn.pack(side="left", expand=True, fill="x", padx=(0, 4))
        self.stop_btn = ttk.Button(bf, text=self.t("stop"), style="Stop.TButton", command=self.stop_attack, state="disabled")
        self.stop_btn.pack(side="right", expand=True, fill="x", padx=(4, 0))

        # --- progress ---
        self.progress_var = tk.DoubleVar(value=0)
        ttk.Progressbar(left, variable=self.progress_var, maximum=100,
                        style="pink.Horizontal.TProgressbar").pack(fill="x", pady=(0, 1))

        sr = tk.Frame(left, bg=BG)
        sr.pack(fill="x")
        self.status_var = tk.StringVar(value=self.t("waiting"))
        tk.Label(sr, textvariable=self.status_var, bg=BG, fg=MUTED, font=FONT).pack(side="left")
        self.speed_var = tk.StringVar(value="")
        tk.Label(sr, textvariable=self.speed_var, bg=BG, fg=BLUE_D, font=FONT_SUB).pack(side="right")
        self.attempts_var = tk.StringVar(value="")
        tk.Label(left, textvariable=self.attempts_var, bg=BG, fg=MUTED, font=FONT_SUB).pack(anchor="w")

        # --- found banner placeholder ---
        self.found_banner_slot = tk.Frame(left, bg=BG)
        self.found_banner_slot.pack(fill="x")

        # --- log with pop out button ---
        self.log_dock_frame = tk.Frame(left, bg=BG)
        self.log_dock_frame.pack(fill="both", expand=True, pady=(2, 0))
        self._build_log_widget(self.log_dock_frame)

        # --- right: mascot + hw monitor ---
        self._load_mascot(right)

        hw_card = tk.Frame(right, bg=CARD, highlightbackground=RULE, highlightthickness=2, padx=10, pady=8)
        hw_card.pack(fill="x", pady=(8, 0))
        tk.Label(hw_card, text="System", bg=CARD, fg=PINK_D, font=FONT_BOLD).pack(anchor="w")

        self.hw_cpu_var = tk.StringVar(value="CPU: ---%")
        self.hw_ram_var = tk.StringVar(value="RAM: --- / ---")
        self.hw_gpu_var = tk.StringVar(value="GPU: ---")

        tk.Label(hw_card, textvariable=self.hw_cpu_var, bg=CARD, fg=BLUE_D, font=FONT_MONO_SM).pack(anchor="w", pady=(2, 0))
        self.cpu_bar_canvas = tk.Canvas(hw_card, height=8, bg=BG2, highlightthickness=0, width=220)
        self.cpu_bar_canvas.pack(fill="x", pady=(2, 4))

        tk.Label(hw_card, textvariable=self.hw_ram_var, bg=CARD, fg=BLUE_D, font=FONT_MONO_SM).pack(anchor="w")
        self.ram_bar_canvas = tk.Canvas(hw_card, height=8, bg=BG2, highlightthickness=0, width=220)
        self.ram_bar_canvas.pack(fill="x", pady=(2, 4))

        tk.Label(hw_card, textvariable=self.hw_gpu_var, bg=CARD, fg=BLUE_D, font=FONT_MONO_SM).pack(anchor="w")
        self.gpu_bar_canvas = tk.Canvas(hw_card, height=8, bg=BG2, highlightthickness=0, width=220)
        self.gpu_bar_canvas.pack(fill="x", pady=(2, 0))

        sep = tk.Frame(hw_card, height=1, bg=RULE)
        sep.pack(fill="x", pady=(8, 6))
        tk.Label(hw_card, text="UwUForce", bg=CARD, fg=PINK, font=FONT_BOLD).pack(anchor="w")

        self.app_cpu_var = tk.StringVar(value="CPU: ---%")
        self.app_ram_var = tk.StringVar(value="RAM: ---")

        tk.Label(hw_card, textvariable=self.app_cpu_var, bg=CARD, fg=PINK_D, font=FONT_MONO_SM).pack(anchor="w", pady=(2, 0))
        self.app_cpu_bar = tk.Canvas(hw_card, height=8, bg=BG2, highlightthickness=0, width=220)
        self.app_cpu_bar.pack(fill="x", pady=(2, 4))

        tk.Label(hw_card, textvariable=self.app_ram_var, bg=CARD, fg=PINK_D, font=FONT_MONO_SM).pack(anchor="w")
        self.app_ram_bar = tk.Canvas(hw_card, height=8, bg=BG2, highlightthickness=0, width=220)
        self.app_ram_bar.pack(fill="x", pady=(2, 0))

    def _build_log_widget(self, parent):
        log_header = tk.Frame(parent, bg=BG2)
        log_header.pack(fill="x")
        tk.Label(log_header, text="Logs", bg=BG2, fg=MUTED, font=("Comic Sans MS", 8, "bold")).pack(side="left", padx=(6, 0))
        self.log_toggle_btn = tk.Button(log_header, text=self.t("pop_out"), bg=RULE, fg=PINK,
                                        font=("Comic Sans MS", 7, "bold"), relief="flat",
                                        activebackground="#7a4a60", activeforeground=PINK,
                                        padx=8, pady=1, cursor="hand2",
                                        command=self._toggle_log_float)
        self.log_toggle_btn.pack(side="right", padx=(0, 2), pady=1)

        log_outer = tk.Frame(parent, bg=BG2, highlightbackground=RULE, highlightthickness=1)
        log_outer.pack(fill="both", expand=True)
        log_scroll = tk.Scrollbar(log_outer, orient="vertical", bg=RULE, troughcolor=BG2, activebackground=PINK_D)
        log_scroll.pack(side="right", fill="y")
        self.log_text = tk.Text(log_outer, height=10, bg=BG2, fg=MUTED, font=FONT_MONO,
                                insertbackground=PINK_D, selectbackground=PINK_D, selectforeground=BG,
                                highlightthickness=0, relief="flat", padx=8, pady=4, wrap="word",
                                yscrollcommand=log_scroll.set)
        self.log_text.pack(side="left", fill="both", expand=True)
        log_scroll.config(command=self.log_text.yview)
        self.log_text.tag_configure("pink", foreground=PINK_D)
        self.log_text.tag_configure("blue", foreground=BLUE_D)
        self.log_text.tag_configure("green", foreground=GREEN)
        self.log_text.tag_configure("warn", foreground=WARN)
        self.log_text.configure(state="disabled")
        self.log_outer_frame = log_outer

    def _toggle_log_float(self):
        if not self.log_floating:
            self._pop_out_log()
        else:
            self._dock_log()

    def _pop_out_log(self):
        old_content = self._get_log_content()

        for w in self.log_dock_frame.winfo_children():
            w.destroy()

        placeholder = tk.Label(self.log_dock_frame, text="~ logs floating ~", bg=BG, fg=RULE,
                               font=("Comic Sans MS", 9, "italic"))
        placeholder.pack(expand=True)

        self.log_window = tk.Toplevel(self.root)
        self.log_window.title("UwUForce ~ Logs")
        self.log_window.configure(bg=BG)
        self.log_window.geometry("650x300")
        mx = self.root.winfo_x() + self.root.winfo_width() + 10
        my = self.root.winfo_y()
        self.log_window.geometry(f"+{mx}+{my}")
        self.log_window.protocol("WM_DELETE_WINDOW", self._dock_log)

        self._build_log_widget(self.log_window)
        self.log_toggle_btn.configure(text=self.t("dock"))
        self.log_floating = True

        self._restore_log_content(old_content)

    def _dock_log(self):
        old_content = self._get_log_content()

        if self.log_window:
            self.log_window.destroy()
            self.log_window = None

        for w in self.log_dock_frame.winfo_children():
            w.destroy()

        self._build_log_widget(self.log_dock_frame)
        self.log_toggle_btn.configure(text=self.t("pop_out"))
        self.log_floating = False

        self._restore_log_content(old_content)

    def _get_log_content(self):
        self.log_text.configure(state="normal")
        content = self.log_text.dump("1.0", "end", tag=True, text=True)
        self.log_text.configure(state="disabled")
        return content

    def _restore_log_content(self, content):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        current_tags = []
        for item in content:
            kind = item[0]
            val = item[1]
            if kind == "tagon":
                current_tags.append(val)
            elif kind == "tagoff":
                if val in current_tags:
                    current_tags.remove(val)
            elif kind == "text":
                if val:
                    if current_tags:
                        self.log_text.insert("end", val, tuple(current_tags))
                    else:
                        self.log_text.insert("end", val)
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _card(self, parent, pady=(0, 4)):
        f = tk.Frame(parent, bg=CARD, highlightbackground=RULE, highlightthickness=2, padx=12, pady=6)
        f.pack(fill="x", pady=pady)
        return f

    # ─── found banner (in-app) ───
    def _show_found_banner(self, password, elapsed):
        self._dismiss_found_banner()

        banner = tk.Frame(self.found_banner_slot, bg=CARD, highlightbackground=GREEN,
                          highlightthickness=2, padx=12, pady=8)
        banner.pack(fill="x", pady=(2, 2))
        self.found_banner = banner

        top_row = tk.Frame(banner, bg=CARD)
        top_row.pack(fill="x")

        tk.Label(top_row, text="~  nyaa~!  ~", bg=CARD, fg=PINK,
                 font=("Comic Sans MS", 8, "italic")).pack(side="left")
        tk.Label(top_row, text=self.t("found_status"), bg=CARD, fg=GREEN,
                 font=("Comic Sans MS", 14, "bold")).pack(side="left", padx=(8, 0))

        dismiss_btn = tk.Button(top_row, text="X", bg=CARD, fg=MUTED,
                                font=("Consolas", 9, "bold"), relief="flat",
                                activebackground=RULE, activeforeground=FG,
                                padx=6, pady=0, cursor="hand2",
                                command=self._dismiss_found_banner)
        dismiss_btn.pack(side="right")

        pwd_row = tk.Frame(banner, bg=CARD)
        pwd_row.pack(fill="x", pady=(6, 4))

        tk.Label(pwd_row, text=self.t("found"), bg=CARD, fg=MUTED, font=FONT).pack(side="left")

        pwd_box = tk.Frame(pwd_row, bg=BG2, highlightbackground=PINK_D, highlightthickness=2,
                           padx=10, pady=4)
        pwd_box.pack(side="left", padx=(8, 0))
        tk.Label(pwd_box, text=password, bg=BG2, fg=PINK_D,
                 font=("Consolas", 15, "bold")).pack()

        info_text = (f"{self.t('total_time')} {self._format_time(elapsed)}  |  "
                     f"{self._format_number(self.attempts)} {self.t('attempts_lbl').rstrip(':')}")
        tk.Label(banner, text=info_text, bg=CARD, fg=MUTED, font=FONT_SUB).pack(anchor="w", pady=(2, 6))

        btn_row = tk.Frame(banner, bg=CARD)
        btn_row.pack(fill="x")

        copy_btn = tk.Button(btn_row, text=self.t("copy_pwd"), bg=PINK_D, fg=BG,
                             font=("Comic Sans MS", 10, "bold"), relief="flat",
                             activebackground=PINK, activeforeground=BG,
                             padx=14, pady=4, cursor="hand2",
                             command=lambda: self._copy_password(password))
        copy_btn.pack(side="left", padx=(0, 6))

        if self.af_extract.get():
            ext_btn = tk.Button(btn_row, text=self.t("extract_btn"), bg=BLUE_D, fg=BG,
                                font=("Comic Sans MS", 10, "bold"), relief="flat",
                                activebackground=BLUE, activeforeground=BG,
                                padx=14, pady=4, cursor="hand2",
                                command=lambda: self._extract_zip(password))
            ext_btn.pack(side="left", padx=(0, 6))

        close_btn = tk.Button(btn_row, text=self.t("dismiss"), bg=RULE, fg=FG,
                              font=("Comic Sans MS", 10), relief="flat",
                              activebackground="#7a4a60", activeforeground=FG,
                              padx=14, pady=4, cursor="hand2",
                              command=self._dismiss_found_banner)
        close_btn.pack(side="left")

    def _dismiss_found_banner(self):
        if self.found_banner:
            self.found_banner.destroy()
            self.found_banner = None

    def _copy_password(self, password):
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self._log("password copied to clipboard!", "green")

    def _extract_zip(self, password):
        out_dir = os.path.join(os.path.dirname(self.zip_path),
                               os.path.splitext(os.path.basename(self.zip_path))[0] + "_extracted")
        try:
            os.makedirs(out_dir, exist_ok=True)
            with zipfile.ZipFile(self.zip_path) as zf:
                zf.extractall(out_dir, pwd=password.encode("utf-8"))
            self._log(f"{self.t('extract_done')} {self.t('extracted_to')} {out_dir}", "green")
        except Exception as e:
            self._log(f"{self.t('extract_fail')} {e}", "warn")

    # ─── hw monitor ───
    def _start_hw_monitor(self):
        self._update_hw()

    def _update_hw(self):
        try:
            cpu_pct = psutil.cpu_percent(interval=0)
            mem = psutil.virtual_memory()
            ram_used = mem.used / (1024 ** 3)
            ram_total = mem.total / (1024 ** 3)
            ram_pct = mem.percent

            self.hw_cpu_var.set(f"CPU: {cpu_pct:.0f}%")
            self.hw_ram_var.set(f"RAM: {ram_used:.1f} / {ram_total:.1f} GB")

            self._draw_bar(self.cpu_bar_canvas, cpu_pct)
            self._draw_bar(self.ram_bar_canvas, ram_pct)

            if HAS_GPU:
                try:
                    gpus = GPUtil.getGPUs()
                    if gpus:
                        g = gpus[0]
                        self.hw_gpu_var.set(f"GPU: {g.load * 100:.0f}% | {g.memoryUsed:.0f}/{g.memoryTotal:.0f}MB")
                        self._draw_bar(self.gpu_bar_canvas, g.load * 100)
                    else:
                        self.hw_gpu_var.set("GPU: N/A")
                        self._draw_bar(self.gpu_bar_canvas, 0)
                except Exception:
                    self.hw_gpu_var.set("GPU: N/A")
                    self._draw_bar(self.gpu_bar_canvas, 0)
            else:
                self.hw_gpu_var.set("GPU: N/A")
                self._draw_bar(self.gpu_bar_canvas, 0)

            try:
                app_cpu = self.process.cpu_percent(interval=0) / multiprocessing.cpu_count()
                app_mem = self.process.memory_info()
                app_ram_mb = app_mem.rss / (1024 ** 2)
                app_ram_pct = (app_mem.rss / mem.total) * 100

                self.app_cpu_var.set(f"CPU: {app_cpu:.1f}%")
                self.app_ram_var.set(f"RAM: {app_ram_mb:.1f} MB ({app_ram_pct:.1f}%)")
                self._draw_bar(self.app_cpu_bar, app_cpu)
                self._draw_bar(self.app_ram_bar, app_ram_pct)
            except Exception:
                pass
        except Exception:
            pass

        self.root.after(1500, self._update_hw)

    def _draw_bar(self, canvas, pct):
        canvas.delete("all")
        w = canvas.winfo_width() or 220
        h = canvas.winfo_height() or 8
        fill_w = max(1, int(w * min(pct, 100) / 100))
        if pct > 80:
            color = WARN
        elif pct > 50:
            color = PINK_D
        else:
            color = BLUE_D
        canvas.create_rectangle(0, 0, fill_w, h, fill=color, outline="")

    # ─── mask ───
    def _on_length_change(self):
        self._rebuild_mask_slots()
        self.update_estimate()

    def _rebuild_mask_slots(self):
        for w in self.mask_slots_frame.winfo_children():
            w.destroy()
        self.mask_entries.clear()
        self.mask_vars.clear()
        try:
            pwd_len = self.length_var.get()
        except (tk.TclError, ValueError):
            pwd_len = 1
        pwd_len = max(1, min(pwd_len, 20))
        row_frame = None
        for i in range(pwd_len):
            if i % 10 == 0:
                row_frame = tk.Frame(self.mask_slots_frame, bg=CARD)
                row_frame.pack(fill="x", pady=(0, 2))
            slot = tk.Frame(row_frame, bg=CARD)
            slot.pack(side="left", padx=(0, 2))
            tk.Label(slot, text=str(i + 1), bg=CARD, fg=RULE, font=("Consolas", 7)).pack()
            var = tk.StringVar(value="#")
            entry = tk.Entry(slot, textvariable=var, width=2, justify="center",
                             font=("Consolas", 14, "bold"), bg=BG2, fg=PINK_D,
                             insertbackground=PINK_D, highlightthickness=1,
                             highlightcolor=RULE, relief="flat",
                             selectbackground=PINK_D, selectforeground=BG)
            entry.pack()
            var.trace_add("write", lambda *a, v=var: self._on_mask_edit(v))
            self.mask_vars.append(var)
            self.mask_entries.append(entry)
        self._update_mask_preview()

    def _on_mask_edit(self, var):
        val = var.get()
        if len(val) > 1:
            var.set(val[-1])
            return
        if val == "":
            var.set("#")
            return
        self.root.after_idle(self._update_mask_preview)
        self.root.after_idle(self.update_estimate)

    def _update_mask_preview(self):
        mask = ""
        unknown = 0
        for var in self.mask_vars:
            c = var.get()
            if not c or c == "#":
                mask += "#"
                unknown += 1
            else:
                mask += c
        self.mask_preview_var.set(mask)
        self.mask_unknown_var.set(f"({unknown} {self.t('unknown_pos')})")

    def _get_mask(self):
        return [None if (not v.get() or v.get() == "#") else v.get() for v in self.mask_vars]

    def _count_unknown(self):
        return sum(1 for v in self.mask_vars if not v.get() or v.get() == "#")

    # ─── waifu ───
    def _get_waifu_list(self):
        available = []
        wd = os.path.join(self.script_dir, WAIFU_DIR)
        if os.path.isdir(wd):
            for f in WAIFU_FILES:
                p = os.path.join(wd, f)
                if os.path.isfile(p) and os.path.getsize(p) > 1000:
                    available.append(p)
        if not available:
            fb = os.path.join(self.script_dir, FALLBACK_WAIFU)
            if os.path.isfile(fb):
                available.append(fb)
        return available

    def _load_bg_waifu(self):
        available = self._get_waifu_list()
        if not available:
            return
        pick = random.choice(available)
        try:
            img = Image.open(pick).convert("RGBA")
            cw, ch = 920, 850
            th = int(ch * 0.92)
            ratio = th / img.height
            tw = int(img.width * ratio)
            if tw > int(cw * 0.46):
                tw = int(cw * 0.46)
                ratio = tw / img.width
                th = int(img.height * ratio)
            img = img.resize((tw, th), Image.LANCZOS)
            alpha = img.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(0.15)
            img.putalpha(alpha)
            bg_img = Image.new("RGBA", (cw, ch), (24, 26, 27, 255))
            bg_img.paste(img, (cw - tw - int(cw * 0.02), ch - th), img)
            self.bg_photo = ImageTk.PhotoImage(bg_img)
            self.bg_canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)
        except Exception:
            pass

    def _load_mascot(self, parent):
        available = self._get_waifu_list()
        if not available:
            tk.Label(parent, text="UwU\n~ nyaa ~", bg=BG, fg=PINK_D,
                     font=FONT_TITLE, justify="center").pack(pady=(60, 0))
            return
        pick = random.choice(available)
        try:
            img = Image.open(pick).convert("RGBA")
            img = img.resize((220, 300), Image.LANCZOS)
            self.mascot_photo = ImageTk.PhotoImage(img)
            canvas = tk.Canvas(parent, width=220, height=360, bg=BG, highlightthickness=0)
            canvas.pack(pady=(10, 0))
            canvas.create_image(110, 150, image=self.mascot_photo)
            self.mascot_text_id = canvas.create_text(110, 320, text=self.t("mascot_text"),
                                                     fill=PINK_D, font=("Comic Sans MS", 10, "italic"))
            canvas.create_text(110, 345, text="uwu", fill=MUTED, font=("Comic Sans MS", 9))
            self.mascot_canvas = canvas
        except Exception:
            tk.Label(parent, text="UwU\n~ nyaa ~", bg=BG, fg=PINK_D,
                     font=FONT_TITLE, justify="center").pack(pady=(60, 0))

    # ─── lang ───
    def _change_lang(self, event=None):
        self.current_lang = self.lang_var.get()
        self.subtitle_label.configure(text=self.t("subtitle"))
        self.file_label.configure(text=self.t("zip_file"))
        self.select_btn.configure(text=self.t("select"))
        if not self.zip_path:
            self.file_path_var.set(self.t("no_file"))
        self.charset_title.configure(text=self.t("charset"))
        for key, cb in self.charset_cbs.items():
            cb.configure(text=self.t(key))
        self.len_label.configure(text=self.t("pwd_len"))
        self.threads_label.configure(text=self.t("threads"))
        self.auto_cb.configure(text=self.t("auto"))
        self.mask_title.configure(text=self.t("mask"))
        self.mask_hint_label.configure(text=self.t("mask_hint"))
        self.mask_preview_label.configure(text=self.t("mask_preview"))
        self.est_title.configure(text=self.t("estimate"))
        self.est_cs_label.configure(text=self.t("charset_size"))
        self.est_comb_label.configure(text=self.t("combinations"))
        self.est_time_label.configure(text=self.t("est_time"))
        self.start_btn.configure(text=self.t("start"))
        self.stop_btn.configure(text=self.t("stop"))
        self.lang_label.configure(text=self.t("lang"))
        self.af_label.configure(text=self.t("after_find"))
        self.af_notif_cb.configure(text=self.t("notif"))
        self.af_extract_cb.configure(text=self.t("extract"))
        self.log_toggle_btn.configure(text=self.t("dock") if self.log_floating else self.t("pop_out"))
        if not self.running:
            self.status_var.set(self.t("waiting"))
        if hasattr(self, "mascot_canvas") and hasattr(self, "mascot_text_id"):
            self.mascot_canvas.itemconfig(self.mascot_text_id, text=self.t("mascot_text"))
        self._update_mask_preview()
        self.update_estimate()

    # ─── core ───
    def _build_charset(self):
        cs = ""
        if self.use_lower.get(): cs += string.ascii_lowercase
        if self.use_upper.get(): cs += string.ascii_uppercase
        if self.use_digits.get(): cs += string.digits
        if self.use_special.get(): cs += "!@#$%^&*()-_=+[]{}|;:',.<>?/`~\""
        if self.use_space.get(): cs += " "
        return cs

    def _format_number(self, n):
        if n < 1_000: return str(n)
        if n < 1_000_000: return f"{n:,.0f}".replace(",", ".")
        if n < 1_000_000_000: return f"{n / 1e6:.2f}M"
        if n < 1_000_000_000_000: return f"{n / 1e9:.2f}B"
        if n < 1e15: return f"{n / 1e12:.2f}T"
        return f"{n:.2e}"

    def _format_time(self, seconds):
        if seconds < 0.001: return f"< 1ms ({self.t('instant')})"
        if seconds < 1: return f"{seconds * 1000:.0f}ms"
        if seconds < 60: return f"{seconds:.1f} {self.t('seconds')}"
        if seconds < 3600: return f"{seconds / 60:.1f} {self.t('minutes')}"
        if seconds < 86400: return f"{seconds / 3600:.1f} {self.t('hours')}"
        if seconds < 86400 * 365:
            d = seconds / 86400
            return f"{d:.1f} {self.t('days')}" if d < 30 else f"{d / 30:.1f} {self.t('months')}"
        y = seconds / (86400 * 365)
        if y > 1e6: return f"{y:.2e} {self.t('years')} ({self.t('good_luck')})"
        if y > 1000: return f"{y:,.0f} {self.t('years')}"
        return f"{y:.1f} {self.t('years')}"

    def update_estimate(self, *_):
        charset = self._build_charset()
        cs_size = len(charset)
        unknown = self._count_unknown()
        if cs_size == 0:
            self.est_charset_size.set(f"0 {self.t('chars')} ({self.t('select_chars')})")
            self.est_combinations.set("-")
            self.est_time.set("-")
            self.total_combinations = 0
            return
        self.total_combinations = cs_size ** unknown if unknown > 0 else 1
        speed = self.live_speed if self.live_speed > 0 else 800 * self._get_thread_count()
        est_sec = self.total_combinations / speed if speed > 0 else float("inf")
        self.est_charset_size.set(f"{cs_size} {self.t('chars')}")
        self.est_combinations.set(self._format_number(self.total_combinations))
        self.est_time.set(self._format_time(est_sec))

    def _get_thread_count(self):
        if self.auto_threads.get():
            return smart_thread_count()
        try:
            return max(1, self.thread_var.get())
        except (tk.TclError, ValueError):
            return 4

    def toggle_thread_input(self):
        if self.auto_threads.get():
            self.thread_spin.configure(state="disabled")
            opt = smart_thread_count()
            self.thread_var.set(opt)
            cpu_c = multiprocessing.cpu_count()
            self.thread_info_var.set(f"({opt}t / {cpu_c}c)")
        else:
            self.thread_spin.configure(state="normal")
            self.thread_info_var.set("")
        self.update_estimate()

    def select_file(self):
        path = filedialog.askopenfilename(title="Select ZIP",
                                          filetypes=[("ZIP files", "*.zip"), ("All", "*.*")])
        if path:
            self.file_path_var.set(os.path.basename(path))
            self.zip_path = path
            self._log(f"{self.t('file_selected')} {os.path.basename(path)}", "blue")

    def _log(self, msg, tag=None):
        self.log_text.configure(state="normal")
        ts = time.strftime("%H:%M:%S")
        prefix = f"[{ts}] "
        self.log_text.insert("end", prefix)
        if tag:
            self.log_text.insert("end", f"{msg}\n", tag)
        else:
            self.log_text.insert("end", f"{msg}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def start_attack(self):
        if not self.zip_path:
            messagebox.showwarning("UwUForce", self.t("select_warn"))
            return
        charset = self._build_charset()
        if not charset:
            messagebox.showwarning("UwUForce", self.t("charset_warn"))
            return
        try:
            pwd_len = self.length_var.get()
            if pwd_len < 1: raise ValueError
        except (tk.TclError, ValueError):
            messagebox.showwarning("UwUForce", self.t("len_warn"))
            return
        try:
            zipfile.ZipFile(self.zip_path).close()
        except (zipfile.BadZipFile, FileNotFoundError) as e:
            messagebox.showerror("UwUForce", f"{self.t('zip_err')} {e}")
            return

        self._dismiss_found_banner()
        mask = self._get_mask()
        self.running = True
        self.found_password = None
        self.attempts = 0
        self.live_speed = 0
        self.start_time = time.time()
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.progress_var.set(0)

        nt = self._get_thread_count()
        mask_str = "".join(c if c else "#" for c in mask)
        self._log(f"{self.t('starting')} {nt} {self.t('threads_log')}", "pink")
        self._log(f"mask: {mask_str} | charset: {len(charset)} | "
                  f"{self.t('combos_log')}: {self._format_number(self.total_combinations)}")
        self.status_var.set(self.t("attacking"))
        threading.Thread(target=self._attack_controller, args=(charset, mask, nt), daemon=True).start()

    def stop_attack(self):
        self.running = False
        self.status_var.set(self.t("stopped"))
        self._log(self.t("attack_stopped"), "warn")
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")

    def _try_password_read(self, zf_path, password):
        try:
            with zipfile.ZipFile(zf_path) as zf:
                pwd_bytes = password.encode("utf-8")
                for info in zf.infolist():
                    if not info.is_dir():
                        zf.read(info.filename, pwd=pwd_bytes)
                        return True
                return False
        except (RuntimeError, zipfile.BadZipFile, Exception):
            return False

    def _worker(self, zf_path, chunk):
        for password in chunk:
            if not self.running or self.found_password:
                return
            self.attempts += 1
            if self._try_password_read(zf_path, password):
                self.found_password = password
                self.running = False
                return

    def _generate_from_mask(self, charset, mask):
        unknown_idx = [i for i, c in enumerate(mask) if c is None]
        if not unknown_idx:
            yield "".join(c for c in mask)
            return
        for combo in itertools.product(charset, repeat=len(unknown_idx)):
            result = list(mask)
            for idx, ch in zip(unknown_idx, combo):
                result[idx] = ch
            yield "".join(result)

    def _attack_controller(self, charset, mask, num_threads):
        gen = self._generate_from_mask(charset, mask)
        batch_size = max(200, 800 * num_threads)
        zf_path = self.zip_path

        while self.running and not self.found_password:
            batch = []
            try:
                for _ in range(batch_size):
                    batch.append(next(gen))
            except StopIteration:
                if not batch:
                    break

            chunk_size = max(1, len(batch) // num_threads)
            chunks = [batch[i:i + chunk_size] for i in range(0, len(batch), chunk_size)]
            threads = []
            for chunk in chunks:
                t = threading.Thread(target=self._worker, args=(zf_path, chunk), daemon=True)
                threads.append(t)
                t.start()
            for t in threads:
                t.join()

            now = time.time()
            elapsed = now - self.start_time
            speed = self.attempts / elapsed if elapsed > 0 else 0
            self.live_speed = speed
            progress = (self.attempts / self.total_combinations * 100) if self.total_combinations > 0 else 0
            self.msg_queue.put(("update", {
                "attempts": self.attempts, "speed": speed,
                "progress": min(progress, 100), "elapsed": elapsed,
            }))

            if len(batch) < batch_size:
                break

        elapsed = time.time() - self.start_time
        speed = self.attempts / elapsed if elapsed > 0 else 0
        self.msg_queue.put(("update", {
            "attempts": self.attempts, "speed": speed,
            "progress": min((self.attempts / self.total_combinations * 100) if self.total_combinations > 0 else 100, 100),
            "elapsed": elapsed,
        }))

        if self.found_password:
            self.msg_queue.put(("found", self.found_password))
        elif self.running:
            self.msg_queue.put(("exhausted", None))
        self.running = False
        self.msg_queue.put(("done", None))

    def _process_queue(self):
        try:
            while True:
                mt, data = self.msg_queue.get_nowait()
                if mt == "update":
                    self.progress_var.set(data["progress"])
                    self.speed_var.set(f"{data['speed']:.0f} pwd/s")
                    self.attempts_var.set(
                        f"{self.t('attempts_lbl')} {self._format_number(data['attempts'])} / "
                        f"{self._format_number(self.total_combinations)}  |  "
                        f"{self.t('time_lbl')} {self._format_time(data['elapsed'])}")
                    if data["speed"] > 0:
                        rem = max(0, self.total_combinations - data["attempts"]) / data["speed"]
                        self.status_var.set(f"{self.t('attacking')} ~{self._format_time(rem)} {self.t('remaining')}")
                        self.live_speed = data["speed"]
                        self.update_estimate()
                elif mt == "found":
                    self._log(f"{self.t('found')} {data}", "green")
                    elapsed = time.time() - self.start_time
                    self._log(f"{self.t('total_time')} {self._format_time(elapsed)} | "
                              f"{self.t('attempts_lbl')} {self._format_number(self.attempts)}", "pink")
                    self.progress_var.set(100)
                    self.status_var.set(self.t("found_status"))
                    if self.af_notif.get():
                        self._show_found_banner(data, elapsed)
                    if self.af_extract.get():
                        self._extract_zip(data)
                elif mt == "exhausted":
                    self.status_var.set(self.t("exhausted"))
                    self._log(self.t("exhausted_log"), "warn")
                    self.progress_var.set(100)
                elif mt == "done":
                    self.start_btn.configure(state="normal")
                    self.stop_btn.configure(state="disabled")
        except queue.Empty:
            pass
        self.root.after(50, self._process_queue)


def main():
    root = tk.Tk()
    w, h = 920, 850
    sx = (root.winfo_screenwidth() - w) // 2
    sy = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{sx}+{sy}")
    UwUForce(root)
    root.mainloop()


if __name__ == "__main__":
    main()
