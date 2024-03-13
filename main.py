import sys
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout
import PyQt5
import os,re
from PyQt5.QtCore import Qt

def partition_list():
    regex = r"([^\\s]*:)"
    driver = os.popen("wmic logicaldisk get name").read()
    drives = re.findall(regex, driver)

    partition_list = [partition.strip() for drive in drives for partition in drive.split(":") if partition.strip()]
    partition_list[0] = partition_list[0].strip("Name  \n\n")
    return partition_list
def file_list(drive):
    user_name = os.getlogin()
    path = f"{drive}:\\Users\\{user_name}\\AppData\\"

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

        print("Files on C drive sorted by size:")
        for file, size in files:
            size_gb = convert_bytes_to_gb(size)
            # print(f"{file}: {size_gb:.2f} GB")
        return files
all_files = []
def scan_button():
    selected_drive = my_combobox.currentText()
    file_name = file_list(str(selected_drive))
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
    global all_files

    # print(all_files)
    for new in range(path.count()):
        # print(new)
        itemm = path.item(new)
        # print(itemm)
        if itemm.checkState() == Qt.CheckState():
            pass
        else:
            print(all_files[new])
        # if PyQt5.QtWidgets.QListWidgetItem(new).checkState() == Qt.Checked:
        #     print(new)

        pass
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
# Layout setup (for better organization)
layout = QVBoxLayout()

layout.addWidget(my_combobox)
layout.addWidget(scan)

layout.addWidget(spliter)
layout.addWidget(path_select)
layout.addWidget(move_button)
window.setLayout(layout)
# layout.addStretch(1)
# Show the window
window.show()

# Start the event loop
sys.exit(app.exec_())
