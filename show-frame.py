import tkinter as tk
from tkinter import ttk
import xml.etree.ElementTree as ET



def create_frames(root, group_var):
    style = ttk.Style()
    style.theme_use('xpnative')

    checkboxes = [[], []]
    current_count = [0, 0]

    frame1 = ttk.Frame(root)
    frame2 = ttk.Frame(root)

    label_frame1 = ttk.Frame(frame1)
    label_frame2 = ttk.Frame(frame2)

    canvas1 = tk.Canvas(frame1, height=300)
    canvas2 = tk.Canvas(frame2, height=300)
    scrollbar1 = ttk.Scrollbar(frame1, orient="vertical", command=canvas1.yview)
    scrollbar2 = ttk.Scrollbar(frame2, orient="vertical", command=canvas2.yview)
    scrollable_frame1 = ttk.Frame(canvas1)
    scrollable_frame2 = ttk.Frame(canvas2)

    scrollable_frame1.bind(
        "<Configure>",
        lambda e: canvas1.configure(
            scrollregion=canvas1.bbox("all")
        )
    )
    scrollable_frame2.bind(
        "<Configure>",
        lambda e: canvas2.configure(
            scrollregion=canvas2.bbox("all")
        )
    )

    canvas1.create_window((0, 0), window=scrollable_frame1, anchor="nw")
    canvas2.create_window((0, 0), window=scrollable_frame2, anchor="nw")
    canvas1.configure(yscrollcommand=scrollbar1.set)
    canvas2.configure(yscrollcommand=scrollbar2.set)

    # 使用grid布局管理器
    scrollbar1.grid(row=1, column=15, sticky='ns')
    scrollbar2.grid(row=1, column=15, sticky='ns')
    canvas1.grid(row=1, column=0, sticky='nsew', columnspan=15)
    canvas2.grid(row=1, column=0, sticky='nsew', columnspan=15)

    # 将标签添加到标签框架中
    for frame in [label_frame1, label_frame2]:
        tk.Label(frame, text="Include", bg='white', width=7, bd=0, relief="flat").grid(row=0, column=0, padx=1, pady=(5, 0))  # 设置间距为0
        tk.Label(frame, text="Well", bg='white', width=7, bd=0, relief="flat").grid(row=0, column=1, padx=1, pady=(5, 0))  # 设置间距为0
        tk.Label(frame, text="Cycle", bg='white', width=7, bd=0, relief="flat").grid(row=0, column=2, padx=1, pady=(5, 0))  # 设置间距为0
        characters = ['M', 'C', 'E', 'M', 'C', 'E', 'M', 'C', 'E', 'M', 'C', 'E']
        for i in range(12):
            tk.Label(frame, text=f"{characters[i]}", bg='white', width=7, bd=0, relief="flat").grid(row=0,
                                                                                                            column=i + 3,
                                                                                                            padx=1,
                                                                                                            pady=(5,
                                                                                                                  0))  # 设置间距为0

    label_frame1.grid(row=0, column=0, sticky='ew', columnspan=15)
    label_frame2.grid(row=0, column=0, sticky='ew', columnspan=15)

    def update_count(var, label, group):
        label_dict = {}
        if var.get() == 1:
            current_count[group] += 1
        elif current_count[group] > 0:
            current_count[group] -= 1
        count = 1
        for checkbox in checkboxes[group]:
            if checkbox[0].get() == 1:
                checkbox[2].config(text=f"{count}")
                label_dict[checkbox[1]] = count  # 更新字典
                count += 1
            else:
                checkbox[2].config(text=f"0")
                label_dict[checkbox[1]] = 0  # 更新字典
        # 更新标签的文本
        count_label.config(text=f"Cycles: {current_count[group]}")

    select_all_status = [False, False]

    def select_all():
        selected_group = 0 if group_var.get() == "Group 1" else 1
        select_all_status[selected_group] = not select_all_status[selected_group]
        current_count[selected_group] = 0  # 重置计数器
        for checkbox in checkboxes[selected_group]:
            checkbox[0].set(1 if select_all_status[selected_group] else 0)
        select_deselect_button.config(text="Deselect All" if select_all_status[selected_group] else "Select All")

    checkboxes_disabled = tk.BooleanVar()

    def toggle_checkboxes():
        # Toggle the disable state of the checkboxes
        checkboxes_disabled.set(not checkboxes_disabled.get())
        # Change the style of the checkboxes
        if checkboxes_disabled.get():
            style.configure('TCheckbutton', background='#ffffff')
            toggle_button.config(text="Check On")  # 修改按钮文本为"Check off"
        else:
            style.configure('TCheckbutton', background='#e1e1e1')
            toggle_button.config(text="Check Off")  # 修改按钮文本为"Check on"



    style = ttk.Style()
    style.configure('TCheckbutton', background='#e1e1e1', padding=(1.5, -0.2), borderwidth=0, highlightthickness=0)

    # 创建control_frame
    control_frame = tk.Frame(root)
    control_frame.pack(anchor='w')
    # 创建下拉列表和输入框
    start_var = tk.StringVar()
    count_var = tk.StringVar()
    label = tk.Label(control_frame, text="Start well:")
    label.grid(row=0, column=0, padx=(85, 0))
    start_combobox = ttk.Combobox(control_frame, textvariable=start_var)
    start_combobox.grid(row=1, column=0, padx=(190, 5))
    labe2 = tk.Label(control_frame, text="Cycle+:")
    labe2.grid(row=0, column=1, sticky='w', padx=(5, 0))
    count_entry = ttk.Entry(control_frame, textvariable=count_var)
    count_entry.grid(row=1, column=1, padx=(5, 5))
    select_deselect_button = ttk.Button(control_frame, text="Select All", command=select_all)
    select_deselect_button.grid(row=1, column=2, padx=(5, 5))
    toggle_button = ttk.Button(control_frame, text="Check Off", command=toggle_checkboxes)
    toggle_button.grid(row=1, column=3, padx=(5, 5))
    count_label = tk.Label(control_frame, text="Cycles: 0")
    count_label.grid(row=1, column=4, padx=(5, 0))



    def select_from_start(*args):
        selected_group = 0 if group_var.get() == "Group 1" else 1
        start = start_combobox.get()
        count = int(count_entry.get())
        current_count[selected_group] = 0  # 重置计数器
        for i, checkbox in enumerate(checkboxes[selected_group]):
            if checkbox[1].cget("text") == start:
                for j in range(i, min(i + count, len(checkboxes[selected_group]))):
                    checkboxes[selected_group][j][0].set(1)
                break

    # 绑定回车事件
    count_entry.bind("<Return>", select_from_start)

    def show_frame(*args):
        selected_frame = group_var.get()
        if selected_frame == "Group 1":
            frame2.pack_forget()
            for var, _, _, *entries in checkboxes[1]:
                var.set(0)
                for entry in entries:
                    entry.delete(0, 'end')
            select_all_status[1] = False
            frame1.pack(fill='both', expand=True)
        else:
            frame1.pack_forget()
            for var, _, _, *entries in checkboxes[0]:
                var.set(0)
                for entry in entries:
                    entry.delete(0, 'end')
            select_all_status[0] = False
            frame2.pack(fill='both', expand=True)
        select_deselect_button.config(
            text="Select All" if not select_all_status[0 if group_var.get() == "Group 1" else 1] else "Deselect All")
        # 清空下拉列表和输入框
        start_combobox.set('')
        count_entry.delete(0, 'end')  # 修改这里
        # 更新下拉列表的值
        selected_group = 0 if group_var.get() == "Group 1" else 1
        start_combobox['values'] = [checkbox[1].cget("text") for checkbox in checkboxes[selected_group]]

    # 初始化下拉列表的值
    start_combobox['values'] = [checkbox[1].cget("text") for checkbox in checkboxes[0]]

    vars = []
    for i in range(96):
        name = f"A96{i+1}"
        var = tk.IntVar()
        label = tk.Label(scrollable_frame1, text=f"{name}", bg='white', bd=0, relief="flat", width=7)  # 设置背景颜色为白色，去除边框
        label.grid(row=i + 1, column=1, padx=1)
        var.trace("w", lambda *args, var=var, label=label, group=0: update_count(var, label, group))
        style = ttk.Style()
        style.configure('TCheckbutton', background='#e1e1e1', padding=(1.5, -0.2), borderwidth=0, highlightthickness=0)
        cb = ttk.Checkbutton(scrollable_frame1, style='TCheckbutton', variable=var, width=4,
                             command=lambda var=var: var.set(not var.get()) if not checkboxes_disabled.get() else None)
        cb.grid(row=i + 1, column=0, padx=1, pady=1, sticky='nsew')
        cycle = tk.Label(scrollable_frame1, text="0", bg='white', bd=0, relief="flat", width=7)  # 设置背景颜色为白色，去除边框
        cycle.grid(row=i + 1, column=2, padx=1)
        entries = [tk.Entry(scrollable_frame1, width=7, bg='white', bd=0, relief="flat", highlightthickness=0) for j in range(12)]  # 设置列宽，背景颜色为白色，去除边框
        for j, entry in enumerate(entries):
            entry.grid(row=i + 1, column=j + 3, padx=1)
        checkboxes[0].append((var, label, cycle, *entries))
        vars.append(var)

    for i in range(48):
        name = f"A48{i+1}"
        var = tk.IntVar()
        label = tk.Label(scrollable_frame2, text=f"{name}", bg='white', bd=0, relief="flat", width=7)  # 设置背景颜色为白色，去除边框
        label.grid(row=i+1, column=1, padx=1)
        var.trace("w", lambda *args, var=var, label=label, group=1: update_count(var, label, group))
        style = ttk.Style()
        style.configure('TCheckbutton', background='#e1e1e1', padding=(1.5, -0.2), borderwidth=0, highlightthickness=0)
        cb = ttk.Checkbutton(scrollable_frame2, style='TCheckbutton', variable=var, width=4,
                             command=lambda var=var: var.set(not var.get()) if not checkboxes_disabled.get() else None)
        cb.grid(row=i + 1, column=0, padx=1, pady=1, sticky='nsew')
        cycle = tk.Label(scrollable_frame2, text="0", bg='white', bd=0, relief="flat", width=7)  # 设置背景颜色为白色，去除边框
        cycle.grid(row=i+1, column=2, padx=1)
        entries = [tk.Entry(scrollable_frame2, width=7, bg='white', bd=0, relief="flat", highlightthickness=0) for j in range(12)]  # 设置列宽，背景颜色为白色，去除边框
        for j, entry in enumerate(entries):
            entry.grid(row=i + 1, column=j + 3, padx=1)
        checkboxes[1].append((var, label, cycle, *entries))
        vars.append(var)

    def save_to_xml():
        root = ET.Element("root")
        for group in checkboxes:
            for checkbox in group:
                if checkbox[0].get() == 1:
                    entry = ET.SubElement(root, "entry")
                    entry.set("label", checkbox[1].cget("text"))
                    entry.text = ','.join(e.get() for e in checkbox[3:])  # 将所有输入框的内容连接成一个字符串
        tree = ET.ElementTree(root)
        tree.write("data.xml")

    def load_from_xml():
        tree = ET.parse("data.xml")
        root = tree.getroot()
        for entry in root.findall("entry"):
            label = entry.get("label")
            text = entry.text.split(',') if entry.text else []  # 如果entry.text是None，将text设置为一个空列表
            for group in checkboxes:
                for checkbox in group:
                    if checkbox[1].cget("text") == label:
                        checkbox[0].set(1)
                        for i, entry in enumerate(checkbox[3:]):
                            entry.delete(0, tk.END)
                            if i < len(text):  # 检查是否有足够的文本来插入到输入框中
                                entry.insert(0, text[i])

    # 在界面上添加两个按钮
    save_button = tk.Button(root, text="Save", command=save_to_xml)
    save_button.pack()
    load_button = tk.Button(root, text="Load", command=load_from_xml)
    load_button.pack()

    return frame1, frame2, vars, show_frame
