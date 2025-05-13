import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from typing import List, Tuple
from core.log_reader import read_log

class HTTPLogViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("HTTP Log Viewer - http_first_100k.log")
        self.root.geometry("1200x800")
        
        self.log_entries: List[Tuple] = []
        self.filtered_entries: List[Tuple] = []
        self.current_index: int = -1
        
        self.create_widgets()
        self.setup_layout()
        
        # Automatyczne wczytanie pliku przy starcie
        self.auto_load_file("http_first_100k.log")
    
    def auto_load_file(self, filename):
        try:
            self.log_entries = read_log(filename)
            self.filtered_entries = self.log_entries
            self.populate_log_list()
            self.update_nav_buttons()
            messagebox.showinfo("Success", f"Loaded {len(self.log_entries)} log entries")
        except FileNotFoundError:
            messagebox.showerror("Error", f"File {filename} not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def create_widgets(self):
        # Panel filtrowania
        self.filter_frame = ttk.LabelFrame(self.root, text="Filters")
        
        # Filtry czasowe
        self.from_date_label = ttk.Label(self.filter_frame, text="From:")
        self.from_date_entry = ttk.Entry(self.filter_frame)
        
        self.to_date_label = ttk.Label(self.filter_frame, text="To:")
        self.to_date_entry = ttk.Entry(self.filter_frame)
        
        self.filter_button = ttk.Button(
            self.filter_frame, 
            text="Apply Filters", 
            command=self.apply_filters
        )
        
        # Lista logów (master)
        self.log_list_frame = ttk.Frame(self.root)
        self.log_list = ttk.Treeview(
            self.log_list_frame,
            columns=('timestamp', 'source_ip', 'method', 'host', 'status'),
            show='headings'
        )
        self.log_list.heading('timestamp', text='Timestamp')
        self.log_list.heading('source_ip', text='Source IP')
        self.log_list.heading('method', text='Method')
        self.log_list.heading('host', text='Host')
        self.log_list.heading('status', text='Status')
        
        self.log_list.bind('<<TreeviewSelect>>', self.on_log_select)
        
        # Szczegóły loga (detail)
        self.detail_frame = ttk.LabelFrame(self.root, text="Log Details")
        self.detail_text = tk.Text(
            self.detail_frame,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=('Consolas', 10)
        )
        
        # Nawigacja
        self.nav_frame = ttk.Frame(self.root)
        self.prev_button = ttk.Button(
            self.nav_frame,
            text="Previous",
            command=self.prev_log,
            state=tk.DISABLED
        )
        self.next_button = ttk.Button(
            self.nav_frame,
            text="Next",
            command=self.next_log,
            state=tk.DISABLED
        )
        
    def setup_layout(self):
        # Filtry
        self.filter_frame.pack(fill=tk.X, padx=5, pady=5)
        self.from_date_label.grid(row=0, column=0, padx=5, pady=5)
        self.from_date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.to_date_label.grid(row=0, column=2, padx=5, pady=5)
        self.to_date_entry.grid(row=0, column=3, padx=5, pady=5)
        self.filter_button.grid(row=0, column=4, padx=5, pady=5)
        
        # Podział na master-detail
        paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned_window.add(self.log_list_frame, weight=1)
        paned_window.add(self.detail_frame, weight=2)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.log_list_frame.pack_propagate(False)
        self.log_list_frame.pack(fill=tk.BOTH, expand=True)
        self.log_list.pack(fill=tk.BOTH, expand=True)
        
        self.detail_frame.pack_propagate(False)
        self.detail_frame.pack(fill=tk.BOTH, expand=True)
        self.detail_text.pack(fill=tk.BOTH, expand=True)
        
        # Nawigacja
        self.nav_frame.pack(fill=tk.X, padx=5, pady=5)
        self.prev_button.pack(side=tk.LEFT, padx=5)
        self.next_button.pack(side=tk.LEFT)
        
    def populate_log_list(self):
        self.log_list.delete(*self.log_list.get_children())
        
        for entry in self.filtered_entries:
            ts, _, id_orig_h, id_orig_p, _, _, _, method, host, _, _, _, _, _, status_code, *_ = entry
            
            self.log_list.insert('', tk.END, values=(
                ts.strftime("%Y-%m-%d %H:%M:%S"),
                f"{id_orig_h}:{id_orig_p}",
                method or "-",
                host or "-",
                f"{status_code}" if status_code else "-"
            ))
    
    def on_log_select(self, event):
        selected = self.log_list.selection()
        if selected:
            self.current_index = self.log_list.index(selected[0])
            self.show_log_details()
            self.update_nav_buttons()
    
    def show_log_details(self):
        if 0 <= self.current_index < len(self.filtered_entries):
            entry = self.filtered_entries[self.current_index]
            self.detail_text.config(state=tk.NORMAL)
            self.detail_text.delete(1.0, tk.END)
            
            details = (
                f"Timestamp: {entry[0]}\n"
                f"UID: {entry[1]}\n"
                f"Source: {entry[2]}:{entry[3]}\n"
                f"Destination: {entry[4]}:{entry[5]}\n"
                f"Method: {entry[7] or '-'}\n"
                f"Host: {entry[8] or '-'}\n"
                f"URI: {entry[9] or '-'}\n"
                f"Referrer: {entry[10] or '-'}\n"
                f"User Agent: {entry[11] or '-'}\n"
                f"Request Body Length: {entry[12]}\n"
                f"Response Body Length: {entry[13]}\n"
                f"Status: {entry[14] or '-'} {entry[15] or '-'}\n"
                f"Tags: {entry[18] or '-'}\n"
                f"Username: {entry[19] or '-'}\n"
            )
            
            self.detail_text.insert(tk.END, details)
            self.detail_text.config(state=tk.DISABLED)
    
    def prev_log(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.log_list.selection_set(self.log_list.get_children()[self.current_index])
            self.log_list.see(self.log_list.get_children()[self.current_index])
            self.show_log_details()
            self.update_nav_buttons()
    
    def next_log(self):
        if self.current_index < len(self.filtered_entries) - 1:
            self.current_index += 1
            self.log_list.selection_set(self.log_list.get_children()[self.current_index])
            self.log_list.see(self.log_list.get_children()[self.current_index])
            self.show_log_details()
            self.update_nav_buttons()
    
    def update_nav_buttons(self):
        self.prev_button.config(state=tk.NORMAL if self.current_index > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.current_index < len(self.filtered_entries) - 1 else tk.DISABLED)
    
    def apply_filters(self):
        from_date_str = self.from_date_entry.get()
        to_date_str = self.to_date_entry.get()
        
        try:
            from_date = datetime.strptime(from_date_str, "%Y-%m-%d") if from_date_str else None
            to_date = datetime.strptime(to_date_str, "%Y-%m-%d") if to_date_str else None
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
            return
        
        self.filtered_entries = [
            entry for entry in self.log_entries
            if (from_date is None or entry[0] >= from_date) and
               (to_date is None or entry[0] <= to_date)
        ]
        
        self.populate_log_list()
        self.current_index = -1
        self.update_nav_buttons()
        messagebox.showinfo("Filter Applied", f"Showing {len(self.filtered_entries)} of {len(self.log_entries)} entries")

def main():
    root = tk.Tk()
    app = HTTPLogViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()