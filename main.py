import sys
import threading

from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout
import PyQt5
import os,re
from PyQt5.QtCore import Qt
import concurrent.futures

from threading import Thread
n=0
lennn = 0
def partition_list():
    regex = r"([^\\s]*:)"
    driver = os.popen("wmic logicaldisk get name").read()
    drives = re.findall(regex, driver)

    partition_list = [partition.strip() for drive in drives for partition in drive.split(":") if partition.strip()]
    partition_list[0] = partition_list[0].strip("Name  \n\n")
    return partition_list
def file_list(drive):
    user_name = os.getlogin()
    path = f"{drive}:\\Users\\{user_name}\\AppData\\)"

    def convert_bytes_to_gb(bytes):
        gb = bytes / (1024 ** 3)  # 1024 bytes = 1 kilobyte, 1024 kilobytes = 1 megabyte, 1024 megabytes = 1 gigabyte
        return gb

    def list_files_by_size(directory):
        files = []

        for root, dir, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                if os.path.isfile(filepath):
                    filesize = os.path.getsize(filepath)
                    files.append((filepath, filesize))

        files.sort(key=lambda x: x[1])

        return files

    if __name__ == "__main__":
        c_drive_directory = path
        files = list_files_by_size(c_drive_directory)

        # print("Files on C drive sorted by size:")
        for file, size in files:
            size_gb = convert_bytes_to_gb(size)
            # print(f"{file}: {size_gb:.2f} GB")
        global lennn
        lennn = len(files)
        return files
all_files = []
def scan_button():
    selected_drive = my_combobox.currentText()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(file_list, str(selected_drive))
        return_value = future.result()
        file_name = return_value

    # print(file_name)
    # file_name = file_list(str(selected_drive))
    count = 0
    for trans_one in reversed(file_name):
        for trans_two in trans_one:
            if count / 2 == 0:
                # path.addItem(str(trans_two))
                item = PyQt5.QtWidgets.QListWidgetItem(str(trans_two))
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Unchecked)  # Initially unchecked
                path.addItem(item)
                all_files.append(str(trans_two))
            else:
                trans_two = (trans_two / (1024 ** 3))
                size.addItem(f"{trans_two:.2f} GB")
            count = count + 1
        count = 0
def move():
    linked = []
    global all_files
    moved_path = path_select.currentText()
    # print(moved_path)
    for new in range(path.count()):
        # print(new)
        itemm = path.item(new)

        if itemm.checkState() == Qt.CheckState():
            pass
        else:
            # print(all_files[new])
            new_path_one_with_new_drive_added =str(moved_path) +(str(all_files[new]))[1:]
            # print(new_path_one_with_new_drive_added)

            def remove_last_element(path):
                # Split the path into a list of elements
                path_elements = path.split(os.sep)
                # Remove the last element from the list
                path_elements.pop()
                # Join the elements back into a path
                directory_path = os.sep.join(path_elements)
                return directory_path
            parent_path_with_new_drive_added = remove_last_element(new_path_one_with_new_drive_added) # useless
            parent_path_old = remove_last_element(str(all_files[new])) # useless
            try:
                os.mkdir(parent_path_with_new_drive_added)

            except:
                print("failed MKDIR")
                pass
            try:
                os.system(f"move /y {str(all_files[new])} {new_path_one_with_new_drive_added}")
            except:
                print("failed move")
            command = f"mklink \"{new_path_one_with_new_drive_added}\" \"{(str(all_files[new]))}\""
            os.system(command)
            print(command)
            pass
        # if PyQt5.QtWidgets.QListWidgetItem(new).checkState() == Qt.Checked:
        #     print(new)


# Create a QApplication instance
app = QApplication(sys.argv)

# Create a QWidget (window)
window = QWidget()
window.setWindowTitle("My Simple Window")
window.setGeometry(100, 100, 300, 200)


my_combobox = QComboBox()
my_combobox.addItem("Select Your Drive")
drives = partition_list()
my_combobox.addItems(drives)
scan = PyQt5.QtWidgets.QPushButton("Scan")
scan.clicked.connect(scan_button)
progress_bar = PyQt5.QtWidgets.QProgressBar()
progress_bar.setMinimum(0)
progress_bar.setMaximum(lennn)
path = PyQt5.QtWidgets.QListWidget()

size = PyQt5.QtWidgets.QListWidget()

spliter = PyQt5.QtWidgets.QSplitter(Qt.Horizontal)
spliter.addWidget(path)
spliter.addWidget(size)
#       move part
move_button = PyQt5.QtWidgets.QPushButton("Move")
move_button.clicked.connect(move)
path_select = PyQt5.QtWidgets.QComboBox()
path_select.addItem("Select Your New Drive")
path_select.addItems(drives)
# scrool
path.verticalScrollBar().valueChanged.connect(size.verticalScrollBar().setValue)
size.verticalScrollBar().valueChanged.connect(path.verticalScrollBar().setValue)
# Layout setup (for better organization)
layout = QVBoxLayout()

layout.addWidget(my_combobox)
layout.addWidget(scan)
layout.addWidget(progress_bar)

layout.addWidget(spliter)
layout.addWidget(path_select)
layout.addWidget(move_button)
window.setLayout(layout)
# layout.addStretch(1)
# Show the window
window.show()

# Start the event loop
sys.exit(app.exec_())
