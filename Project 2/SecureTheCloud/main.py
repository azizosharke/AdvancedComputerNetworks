import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import filedialog
from secure_cloud_storage import SecureCloudStorage
from user import User
from google_auth_oauthlib.flow import InstalledAppFlow

def get_user_credentials():
    client_secret_file_path = 'user.json'
    flow = InstalledAppFlow.from_client_secrets_file(client_secret_file_path, scopes=['https://www.googleapis.com/auth/drive'])
    return flow.run_local_server(port=0)

scs = SecureCloudStorage()

def authenticate_and_add_user():
    email = email_entry.get()
    credentials = get_user_credentials()
    user = User(email, credentials)
    scs.add_user(user)
    status_label.config(text=f'User {email} authenticated and added.')

def browse_file():
    file_path = filedialog.askopenfilename()
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)

def upload_file():
    file_path = file_path_entry.get()
    encrypted_file_path = 'encrypted_' + file_path.split('/')[-1]
    user_email = email_entry.get()
    file_id = scs.upload_to_drive(user_email, file_path, encrypted_file_path)
    status_label.config(text=f'File uploaded with ID: {file_id}')
def remove_user():
    email = email_entry.get()
    scs.remove_user(email)
    status_label.config(text=f'User {email} removed.')    

def download_file():
    file_id = file_id_entry.get()
    user_email = email_entry.get()
    decrypted_file_path = 'decrypted_' + file_path_entry.get().split('/')[-1]
    scs.download_from_drive(user_email, file_id, decrypted_file_path)
    status_label.config(text=f'File downloaded and decrypted: {decrypted_file_path}')

root = ThemedTk(theme="arc")
root.title(' Key management system')

main_frame = ttk.Frame(root, padding="30 30 30 30")
main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

email_label = ttk.Label(main_frame, text='Email:')
email_label.grid(column=0, row=0, padx=5, pady=10, sticky=tk.W)
email_entry = ttk.Entry(main_frame)
email_entry.grid(column=1, row=0, padx=5, pady=10, sticky=(tk.W, tk.E))

authenticate_button = ttk.Button(main_frame, text='Authenticate & Add User', command=authenticate_and_add_user)
authenticate_button.grid(column=0, row=1, columnspan=2, pady=10)

file_path_label = ttk.Label(main_frame, text='File path:')
file_path_label.grid(column=0, row=2, padx=5, pady=10, sticky=tk.W)
file_path_entry = ttk.Entry(main_frame)
file_path_entry.grid(column=1, row=2, padx=5, pady=10, sticky=(tk.W, tk.E))

browse_button = ttk.Button(main_frame, text='Browse', command=browse_file)
browse_button.grid(column=0, row=3, columnspan=2, pady=10)

upload_button = ttk.Button(main_frame, text='Upload File', command=upload_file)
upload_button.grid(column=0, row=4, columnspan=2, pady=10)

file_id_label = ttk.Label(main_frame, text='File ID:')
file_id_label.grid(column=0, row=5, padx=5, pady=10, sticky=tk.W)
file_id_entry = ttk.Entry(main_frame)
file_id_entry.grid(column=1, row=5, padx=5, pady=10, sticky=(tk.W, tk.E))

download_button = ttk.Button(main_frame, text='Download File', command=download_file)
download_button.grid(column=0, row=6, columnspan=2, pady=10)

status_label = ttk.Label(main_frame, text='Status: Ready')
status_label.grid(column=0, row=7, columnspan=2, pady=10)

remove_button = ttk.Button(main_frame, text='Remove User', command=remove_user)
remove_button.grid(column=0, row=8, columnspan=2, pady=10)

root.mainloop()

