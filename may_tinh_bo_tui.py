import tkinter as tk
from tkinter import messagebox
import ast
import operator

def them_ky_tu(ky_tu):
    hien_tai = bieu_thuc.get()

    if hien_tai == "Loi":
        hien_tai = ""

    bieu_thuc.set(hien_tai + ky_tu)

def xoa_tat_ca():
    bieu_thuc.set("")

def xoa_mot_ky_tu():
    hien_tai = bieu_thuc.get()

    if hien_tai == "Loi":
        bieu_thuc.set("")
    else:
        bieu_thuc.set(hien_tai[:-1])

def tinh_node(node):
    phep_toan = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    if isinstance(node, ast.Constant):
        if type(node.value) in (int, float):
            return node.value

    if isinstance(node, ast.BinOp):
        if type(node.op) in phep_toan:
            trai = tinh_node(node.left)
            phai = tinh_node(node.right)

            return phep_toan[type(node.op)](trai, phai)

    if isinstance(node, ast.UnaryOp):
        if type(node.op) in phep_toan:
            return phep_toan[type(node.op)](
                tinh_node(node.operand)
            )
    raise ValueError("Bieu thuc khong hop le")
def tinh_toan():
    bieu_thuc_goc = bieu_thuc.get().strip()

    if not bieu_thuc_goc:
        return

    ky_tu_hop_le = "0123456789+-*/(). "

    if any(ky_tu not in ky_tu_hop_le
           for ky_tu in bieu_thuc_goc):
        messagebox.showerror(
            "Loi", "Bieu thuc khong hop le!"
        )
        return

    try:
        cay = ast.parse(bieu_thuc_goc, mode="eval")
        ket_qua = tinh_node(cay.body)

        if isinstance(ket_qua, float) and ket_qua.is_integer():
            ket_qua = int(ket_qua)

        bieu_thuc.set(str(ket_qua))

    except ZeroDivisionError:
        messagebox.showerror(
            "Loi", "Khong the chia cho 0!"
        )

    except (SyntaxError, ValueError, TypeError, OverflowError):
        messagebox.showerror(
            "Loi", "Bieu thuc khong hop le!"
        )
def xu_ly_phim(event):
    if event.keysym == "Return":
        tinh_toan()
    elif event.keysym == "Escape":
        xoa_tat_ca()
    elif event.keysym == "BackSpace":
        xoa_mot_ky_tu()
cua_so = tk.Tk()
cua_so.title("May tinh bo tui")
cua_so.geometry("340x460")
cua_so.resizable(False, False)

bieu_thuc = tk.StringVar()

tieu_de = tk.Label(
    cua_so,
    text="MAY TINH BO TUI",
    font=("Arial", 16, "bold")
)
tieu_de.pack(pady=(15, 10))

o_hien_thi = tk.Entry(
    cua_so,
    textvariable=bieu_thuc,
    font=("Arial", 20),
    justify="right",
    bd=5,
    relief="sunken"
)
o_hien_thi.pack(
    fill="x",
    padx=15,
    ipady=10
)

o_hien_thi.focus_set()

khung_phim = tk.Frame(cua_so)
khung_phim.pack(
    padx=12,
    pady=15,
    fill="both",
    expand=True
)
# Danh sach cac nut bam
cac_nut = [
    ("C", 0, 0),
    ("⌫", 0, 1),
    ("(", 0, 2),
    (")", 0, 3),

    ("7", 1, 0),
    ("8", 1, 1),
    ("9", 1, 2),
    ("/", 1, 3),

    ("4", 2, 0),
    ("5", 2, 1),
    ("6", 2, 2),
    ("*", 2, 3),

    ("1", 3, 0),
    ("2", 3, 1),
    ("3", 3, 2),
    ("-", 3, 3),

    ("0", 4, 0),
    (".", 4, 1),
    ("=", 4, 2),
    ("+", 4, 3),
]
# Chia deu cac hang va cot
for hang in range(5):
    khung_phim.grid_rowconfigure(
        hang, weight=1
    )

for cot in range(4):
    khung_phim.grid_columnconfigure(
        cot, weight=1
    )
for chu, hang, cot in cac_nut:

    if chu == "C":
        lenh = xoa_tat_ca

    elif chu == "⌫":
        lenh = xoa_mot_ky_tu

    elif chu == "=":
        lenh = tinh_toan
    else:
        lenh = lambda ky_tu=chu: them_ky_tu(ky_tu)
    nut = tk.Button(
        khung_phim,
        text=chu,
        font=("Arial", 15, "bold"),
        command=lenh,
        width=4,
        height=2
    )
    nut.grid(
        row=hang,
        column=cot,
        padx=4,
        pady=4,
        sticky="nsew"
    )
cua_so.bind("<Return>", xu_ly_phim)
cua_so.bind("<Escape>", xu_ly_phim)
cua_so.bind("<BackSpace>", xu_ly_phim)
cua_so.mainloop()
