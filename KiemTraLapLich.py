from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
import pandas as pd
from ui_main import Ui_MainWindow
import concurrent.futures
import math
import numpy as np
from collections import defaultdict
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.df_input_tab1 = None
        self.df_CT2 = None
        self.df_cbdl=None
        self.df_alter_subject = None
        self.df_input_tab2=None
        self.df_cbdl_tab2 = None
        self.df_date_tab2 = None
        self.df_object_tab2=None
        self.df_room_tab2=None
        self.df_input_tab3=None
        self.df_CT2_tab3 = None
        self.df_alter_subject_tab3 = None
        self.df_cbdl_tab4 = None
        self.df_date_tab4 = None
        self.df_room_tab4=None
        self.MAX_STUDENTS_PER_SHIFT = 1400
        self.THRESHOLD = 50
        self.STUDENTS_PER_ROOM = 40
        self.LOW_OCCUPANCY_THRESHOLD=25
        self.max_shifts=45
        self.max_rooms=35
        self.max_shift_per_day=2
        self.shift_per_day=4
        self.SHIFT = ['07h00', '09h00', '13h30', '15h30']
        self.shift_pairs = [('07h00', '09h00'), ('13h30', '15h30')]
        self.tab1_setup()
        self.tab2_setup()
        self.tab3_setup()
        self.tab4_setup()
        # tab1 được hiển thị khi khởi động
        self.tabWidget.setCurrentIndex(0)

    def tab1_setup(self):
        self.fileSVthiHK.clicked.connect(self.load_file_PhanLich)
        self.file2CT.clicked.connect(self.load_file_Student_CT2)
        self.file_alter_subject.clicked.connect(self.load_file_Alter_Subject)
        self.file_cbdl.clicked.connect(self.load_file_ChuanBiDuLieu)
        self.KtrCBDL.clicked.connect(self.Show_KtrDL)
        self.XuatfileCBDL.clicked.connect(self.export_differences)


    def tab2_setup(self):
        self.file_PhanLich.clicked.connect(self.load_file_PhanLich_tab2)
        self.fileCBDL.clicked.connect(self.load_file_CBDL)
        self.file_date.clicked.connect(self.load_file_date)
        self.file_object.clicked.connect(self.load_file_object)
        self.file_room.clicked.connect(self.load_file_room)
        self.KtrPhanLich.clicked.connect(self.Show_KtrPhanLich)
        self.XuatfileKtr.clicked.connect(self.export_file_KtrDl)
        self.XuatfileLichthi.clicked.connect(self.create_summary_excel)


    def tab3_setup(self):
        self.fileSVthiHK_3.clicked.connect(self.load_file_PhanLich_tab3)
        self.file2CT_3.clicked.connect(self.load_file_CBDL_3)
        self.file_alter_subject_3.clicked.connect(self.load_file_Alter_Subject_3)
        self.TienXuLyDL.clicked.connect(self.show_result_CBDL)
        self.XuatfileTienXuLy.clicked.connect(self.save_data_CBDL)


    def tab4_setup(self):
        self.file_cbdl_4.clicked.connect(self.load_file_CBDL_tab4)
        self.file_room_4.clicked.connect(self.load_file_room_4)
        self.file_date_4.clicked.connect(self.load_file_date_4)
        self.Phanlich.clicked.connect(self.show_result_PhanLich)
        self.XuatfilePL.clicked.connect(self.export_file_Phanlich)
    # Tab 4 methods
    def load_file_CBDL_tab4(self):
        self.load_file_and_update_label('label_cbdl_4', 'Danh sách tiền xử lý dữ liệu')

    def load_file_room_4(self):
        self.load_file_and_update_label('label_room_4', 'Danh sách phòng thi')

    def load_file_date_4(self):
        self.load_file_and_update_label('label_date_4', 'Danh sách ngày thi')

    def assign_exam_schedule(self, df_cbdl, max_shifts, max_rooms, students_per_room):
        # Initial setup
        from collections import defaultdict
        course_students = df_cbdl.groupby('Mã học phần mở rộng')['MSV mở rộng'].count()
        course_rooms = {kcs: math.ceil(course_students[kcs] / students_per_room) for kcs in course_students.keys()}
        
        count_node = df_cbdl.groupby('Mã học phần mở rộng')['MSV mở rộng'].nunique().reset_index(name='Bậc')
        students_per_shift = students_per_room * max_rooms
        shifts = np.zeros(max_shifts)
        df_cbdl['Ca thi'] = np.nan
        df_cbdl['Nhóm ca thi'] = np.nan
        df_cbdl['Nhóm ngành'] = df_cbdl['Mã học phần mở rộng'].str[:3]
        sorted_nodes = count_node.sort_values(by='Bậc', ascending=False)['Mã học phần mở rộng'].tolist()
        edges = set()
        student_exam_count = defaultdict(lambda: defaultdict(int))  # Từ điển lưu số lần thi của mỗi sinh viên trong mỗi nhóm ca thi

        # Tạo các cạnh nối giữa các mã học phần
        for _, group in df_cbdl.groupby('MSV mở rộng'):
            subjects = group['Mã học phần mở rộng'].tolist()
            edges.update([(subjects[i], subjects[j]) for i in range(len(subjects)) for j in range(i + 1, len(subjects))])

        def get_exam_group(ca_thi):
            return (ca_thi - 1) // 4 + 1

        i = 1
        while sorted_nodes and i <= max_shifts:
            start_node = sorted_nodes[0]
            no_students = len(df_cbdl.loc[df_cbdl['Mã học phần mở rộng'] == start_node, 'Ca thi'])
            
            if no_students > students_per_shift:
                if shifts[i] == 0:
                    no_required_shifts = math.ceil(no_students / students_per_shift)
                    no_node_students_per_shift = math.ceil(no_students / no_required_shifts)
                    j = 0

                    # Lưu chỉ số ca thi ban đầu để có thể quay lại nếu cần thiết
                    initial_i = i
                    assigned = False

                    while not assigned:
                        potential_conflict = False
                        students_in_node = df_cbdl[df_cbdl['Mã học phần mở rộng'] == start_node]['MSV mở rộng']
                        shift_index = i + int(j / no_node_students_per_shift)
                        exam_group = get_exam_group(shift_index)

                        # Kiểm tra xung đột
                        for student in students_in_node:
                            if student_exam_count[student][exam_group] >= 3:
                                potential_conflict = True
                                break

                        if potential_conflict:
                            # Tăng i lên 2 và thử lại
                            i += 2
                            if i > max_shifts:
                                print("Không còn ca thi nào có sẵn để gán lại.")
                                i = initial_i
                                break
                            # Kiểm tra nếu ca thi mới có số lượng ca thi còn lại là 0
                            if shifts[i] == 0:
                                continue  # Tiếp tục vòng lặp với ca thi mới
                            else:
                                i = initial_i  # Quay lại chỉ số ca thi ban đầu nếu không đủ điều kiện
                                break
                        else:
                            # Gán sinh viên vào ca thi nếu không có xung đột
                            for k, r in df_cbdl.loc[df_cbdl['Mã học phần mở rộng'] == start_node].iterrows():
                                shift_index = i + int(j / no_node_students_per_shift)
                                df_cbdl.loc[k, 'Ca thi'] = shift_index
                                df_cbdl.loc[k, 'Nhóm ca thi'] = get_exam_group(shift_index)
                                j += 1

                            # Cập nhật số lượng sinh viên và số ca thi
                            for j in range(no_required_shifts):
                                shifts[i + j] += math.ceil(no_node_students_per_shift / students_per_room)
                            for student in students_in_node:
                                student_exam_count[student][exam_group] += 1

                            assigned = True
                            sorted_nodes = sorted_nodes[1:]

                    # Quay lại chỉ số ca thi ban đầu sau khi gán xong
                    i = initial_i

            elif no_students <= students_per_shift:
                unassigned_course = df_cbdl[df_cbdl['Ca thi'].isnull()]['Mã học phần mở rộng'].unique()
                new_edges = set()
                
                for _, group in df_cbdl[df_cbdl['Mã học phần mở rộng'].isin(unassigned_course)].groupby('MSV mở rộng'):
                    subjects = group['Mã học phần mở rộng'].tolist()
                    new_edges.update([(subjects[i], subjects[j]) for i in range(len(subjects)) for j in range(i + 1, len(subjects))])
                
                node_edge_counts = {}
                
                for edge in new_edges:
                    for node in edge:
                        if node in node_edge_counts:
                            node_edge_counts[node] += 1
                        else:
                            node_edge_counts[node] = 1
                
                sorted_nodes_by_edge_count = sorted(node_edge_counts.keys(), key=lambda x: node_edge_counts[x], reverse=True)
                if len(sorted_nodes_by_edge_count) > 0:
                    # for first_node in sorted_nodes_by_edge_count:
                        first_node=sorted_nodes_by_edge_count[0]
                        students_in_first_node = df_cbdl[df_cbdl['Mã học phần mở rộng'] == first_node]['MSV mở rộng']
                        can_assign = True
                        remaining_room = max_rooms - shifts[i] if i < len(shifts) else max_rooms
                        colored_nodes = set(df_cbdl[df_cbdl['Ca thi'] == i]['Mã học phần mở rộng'].tolist())
                        exam_group = get_exam_group(i)
                        
                        if all((first_node, colored_node) not in edges and (colored_node, first_node) not in edges for colored_node in colored_nodes):
                            if course_rooms[first_node] <= remaining_room:
                                for student in students_in_first_node:
                                    if student_exam_count[student][exam_group] >= 2:  # Đảm bảo kiểm tra đúng nhóm ca thi
                                        can_assign = False
                                        break

                                if can_assign:
                                    df_cbdl.loc[df_cbdl['Mã học phần mở rộng'] == first_node, 'Ca thi'] = i
                                    df_cbdl.loc[df_cbdl['Mã học phần mở rộng'] == first_node, 'Nhóm ca thi'] = exam_group
                                    shifts[i] += course_rooms[first_node]
                                    sorted_nodes = [node for node in sorted_nodes if node != first_node]
                                    sorted_nodes_by_edge_count = sorted_nodes_by_edge_count[1:]
                                    
                                    # Cập nhật số lần thi của sinh viên trong nhóm ca thi
                                    for student in students_in_first_node:
                                        student_exam_count[student][exam_group] += 1
                                    
            jn = 0
            remaining_room = max_rooms - shifts[i] if i < len(shifts) else max_rooms
            while jn < len(sorted_nodes) and remaining_room > 0:
                node = sorted_nodes[jn]
                colored_nodes = set(df_cbdl[df_cbdl['Ca thi'] == i]['Mã học phần mở rộng'].tolist())
                exam_group = get_exam_group(i)
                if all((node, colored_node) not in edges and (colored_node, node) not in edges for colored_node in colored_nodes):
                    students_in_node = df_cbdl[df_cbdl['Mã học phần mở rộng'] == node]['MSV mở rộng']
                    if not any(student_exam_count[student][exam_group] >= 3 for student in students_in_node):  
                        if course_rooms[node] <= remaining_room:
                            
                            df_cbdl.loc[df_cbdl['Mã học phần mở rộng'] == node, 'Ca thi'] = i
                            df_cbdl.loc[df_cbdl['Mã học phần mở rộng'] == node, 'Nhóm ca thi'] = exam_group
                            shifts[i] += course_rooms[node]
                            sorted_nodes = sorted_nodes[:jn] + sorted_nodes[jn + 1:]
                            for student in students_in_node:
                                student_exam_count[student][exam_group] += 1
                            remaining_room = max_rooms - shifts[i] if i < len(shifts) else max_rooms      
                            jn -= 1 
                            
                            # Cập nhật số lần thi của sinh viên trong nhóm ca thi
                          
                jn += 1
                remaining_room = max_rooms - shifts[i] if i < len(shifts) else max_rooms      


            i += 1
        



        unassigned_courses = df_cbdl[df_cbdl['Ca thi'].isnull()]['Mã học phần mở rộng'].unique()
        print(unassigned_courses)
        
        for node in unassigned_courses:
            assigned = False
            jn = 1
            while jn < max_shifts:
                current_shift_count = df_cbdl[df_cbdl['Ca thi'] == jn]['MSV mở rộng'].count()
                course_students_count = course_students[node]
                if (current_shift_count + course_students_count) <= students_per_shift:
                    exam_group = get_exam_group(jn)
                    colored_nodes = set(df_cbdl[df_cbdl['Ca thi'] == jn]['Mã học phần mở rộng'].tolist())
                    students_in_node = df_cbdl[df_cbdl['Mã học phần mở rộng'] == node]['MSV mở rộng']
                    if all((node, colored_node) not in edges and (colored_node, node) not in edges for colored_node in colored_nodes):
                            if not any(student_exam_count[student][exam_group] >= 3 for student in students_in_node):
                                df_cbdl.loc[df_cbdl['Mã học phần mở rộng'] == node, 'Ca thi'] = jn
                                df_cbdl.loc[df_cbdl['Mã học phần mở rộng'] == node, 'Nhóm ca thi'] = exam_group
                                shifts[jn] += course_rooms[node]
                                
                                # Cập nhật số lần thi của sinh viên trong nhóm ca thi
                                for student in students_in_node:
                                    student_exam_count[student][exam_group] += 1
                                
                                assigned = True
                                unassigned_courses = [course for course in unassigned_courses if course != node]
                                break
                jn+=1

        return df_cbdl












    def check_exam_schedule(self, df_cbdl):

        
        # Tạo từ điển lưu lịch thi của sinh viên
        student_exam_schedules = defaultdict(list)
        # Tạo từ điển lưu số lần xuất hiện của sinh viên trong mỗi ca thi
        student_shift_counts = defaultdict(lambda: defaultdict(int))
        
        # Lưu thông tin lịch thi của từng sinh viên
        for _, row in df_cbdl.iterrows():
            student_id = row['MSV mở rộng']
            shift = row['Ca thi']
            if pd.notna(shift):
                student_exam_schedules[student_id].append(shift)
                student_shift_counts[student_id][shift] += 1
        
        # Kiểm tra số lượng ca thi trong mỗi block và vi phạm quy tắc
        violations = []
        for student_id, shifts in student_exam_schedules.items():
            blocks = {}
            for shift in shifts:
                block = (shift - 1) // 4
                if block in blocks:
                    blocks[block] += 1
                else:
                    blocks[block] = 1
            for block, count in blocks.items():
                if count > 2:
                    violations.append((student_id, block, count))
        
        # Kiểm tra xem có sinh viên nào xuất hiện nhiều lần trong một ca thi
        duplicate_shift_violations = []
        for student_id, shift_count in student_shift_counts.items():
            for shift, count in shift_count.items():
                if count > 1:
                    duplicate_shift_violations.append((student_id, shift, count))
        
        # In thông báo về các vi phạm quy tắc
        if violations:
            print("Students violating the 2 exams per block rule:")
            for violation in violations:
                print(f"Student {violation[0]} has {violation[2]} exams in block {violation[1] + 1}")
        else:
            print("No block violations found.")
        
        if duplicate_shift_violations:
            print("Students appearing multiple times in the same shift:")
            for violation in duplicate_shift_violations:
                print(f"Student {violation[0]} appears {violation[2]} times in shift {violation[1]}")
        else:
            print("No duplicate appearances in shifts found.")






    def assign_rooms(self, df_phancathi, df_dsphongthi, STUDENTS_PER_ROOM):
        df_phancathi['Mã phòng'] = ""
        count_shifts = sorted(df_phancathi['Ca thi'].unique())
        count_rooms = df_dsphongthi['Mã phòng'].unique()
        assigned_rooms_per_shift = {shift: set() for shift in count_shifts}
        for shift in count_shifts:
            course_counts = df_phancathi[df_phancathi['Ca thi'] == shift].groupby('Mã học phần mở rộng')['MSV'].count()
            sorted_courses = course_counts.sort_values(ascending=False).index.tolist()
            for course in sorted_courses:
                no_students = len(df_phancathi[(df_phancathi['Mã học phần mở rộng'] == course) & (df_phancathi['Ca thi'] == shift)])
                rooms_needed = math.ceil(no_students / STUDENTS_PER_ROOM)
                STUDENTS_PER_ROOM_now = math.ceil(no_students / rooms_needed)
                assigned_rooms = 0
                for room in count_rooms:
                    if room not in assigned_rooms_per_shift[shift]:
                        available_students = df_phancathi[(df_phancathi['Mã học phần mở rộng'] == course) & (df_phancathi['Ca thi'] == shift) & (df_phancathi['Mã phòng'] == '')]
                        available_student_count = len(available_students)
                        if available_student_count > 0:
                            df_phancathi.loc[available_students.index[:STUDENTS_PER_ROOM_now], 'Mã phòng'] = room
                            assigned_rooms_per_shift[shift].add(room)
                            assigned_rooms += 1
                        if assigned_rooms == rooms_needed:
                            break
        return df_phancathi


    def assign_calendar(self, df_phanphongthi, df_dsngaythi, shift_per_day):
        df_phanphongthi['Ngày thi'] = ""
        df_phanphongthi['Giờ thi'] = ""

        count_shifts = sorted(df_phanphongthi['Ca thi'].unique())
        count_shifts_len = len(count_shifts)
        count_day = df_dsngaythi['Ngày thi'].unique()
        count_time = df_dsngaythi['Giờ thi'].unique().tolist()

        day_needed = math.ceil(count_shifts_len / shift_per_day)
        shifts_per_day = [count_shifts[i * shift_per_day: (i + 1) * shift_per_day] for i in range(day_needed)]

        # Phân bổ ngày và giờ thi
        assigned_day = 0
        for day in count_day:
            if assigned_day == day_needed:
                break

            for shift in shifts_per_day[assigned_day]:
                available_shifts = df_phanphongthi[(df_phanphongthi['Ca thi'] == shift) & (df_phanphongthi['Ngày thi'] == '')]

                df_phanphongthi.loc[available_shifts.index, 'Ngày thi'] = day
                df_phanphongthi.loc[available_shifts.index, 'Giờ thi'] = count_time[(int(shift) - 1) % shift_per_day]

            assigned_day += 1

        df_phanphongthi['Ngày thi'] = pd.to_datetime(df_phanphongthi['Ngày thi'], format='%d/%m/%Y')
        df_phanphongthi['Ngày thi'] = df_phanphongthi['Ngày thi'].dt.strftime("%d/%m/%Y")

        return df_phanphongthi
    def show_result_PhanLich(self):
        self.textBrowser_4.clear() 
        if not all([self.label_cbdl_4.text(), self.label_room_4.text(), self.label_date_4.text()]):
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn đầy đủ các file đầu vào.")
            return
        self.df_cbdl_tab4 = pd.read_excel(self.label_cbdl_4.text())
        self.df_room = pd.read_excel(self.label_room_4.text())
        self.df_date = pd.read_excel(self.label_date_4.text())
        self.df_phancathi = self.assign_exam_schedule(self.df_cbdl_tab4,self.max_shifts, self.max_rooms, self.STUDENTS_PER_ROOM)
        
        self.df_phancathi = self.assign_rooms(self.df_phancathi, self.df_room, self.STUDENTS_PER_ROOM)
        self.df_phancathi = self.assign_calendar(self.df_phancathi, self.df_date, self.shift_per_day)
        count_shifts = sorted(self.df_phancathi['Ca thi'].unique())
        count_shifts_len=len(count_shifts)
        day_needed=math.ceil(count_shifts_len/self.shift_per_day)

        # Hiển thị số ngày thi cần
        day_count = 1
        self.textBrowser_4.insertPlainText(f"Tổng số ngày thi: {day_needed}\n")

        # Lặp qua từng ngày thi
        for days in sorted(self.df_phancathi['Ngày thi'].unique()):

            df_day = self.df_phancathi[self.df_phancathi['Ngày thi'] == days]

                # Đếm số ca thi của ngày thi
            num_shifts = len(df_day['Ca thi'].unique())

                # Hiển thị kết quả
            self.textBrowser_4.insertPlainText(f"{day_count}. Ngày thi: {days}\n")
            self.textBrowser_4.insertPlainText(f"     Số ca thi của ngày thi: {num_shifts}\n")
                        # Lặp qua từng ca thi trong ngày
            for shift in sorted(df_day['Ca thi'].astype(int).unique()):
                # Lọc df_day theo ca thi hiện tại
                df_shift = df_day[df_day['Ca thi'] == shift]
                                
                df_time=df_shift['Giờ thi'].iloc(0)
                #
                df_course = len(df_shift['Mã học phần'].unique())
                # Đếm số phòng thi của ca thi
                num_rooms = len(df_shift['Mã phòng'].unique())

                # Hiển thị số phòng thi của ca thi
                self.textBrowser_4.insertPlainText(f"      Ca thi: {shift}, Tổng số học phần thi: {df_course}, Tổng số phòng thi được sử dụng: {num_rooms}\n")

            day_count += 1
                # Xuống dòng sau khi kết thúc thông tin về mỗi ngày thi
                
            self.textBrowser_4.insertPlainText("\n")
    def export_file_Phanlich(self):
                # Kiểm tra xem df_sv2ct và df_2 đã được khởi tạo chưa
                if self.df_phancathi is None:
                        QMessageBox.warning(None, "Lỗi", "Chưa thực hiện phân lịch thi")
                        return

                
                # Mở hộp thoại để chọn vị trí lưu file
                file_dialog = QFileDialog()
                file_path, _ = file_dialog.getSaveFileName(None, "Lưu file", "", "Excel Files (*.xlsx *.xls)")
                if not file_path:  # Kiểm tra nếu người dùng không chọn vị trí lưu file
                        QMessageBox.warning(self, "Lỗi", "Bạn chưa chọn vị trí để lưu tập tin. Vui lòng chọn một vị trí để lưu.")
                        return
                # Lưu dữ liệu đã xử lý ra file Excel
                self.df_phancathi.to_excel(file_path, index=False)
                QMessageBox.information(None, "Thành công", "Dữ liệu đã được lưu thành công")


    # Tab 3 methods
    def load_file_PhanLich_tab3(self):
        self.load_file_and_update_label('label_SVthiHK_3', 'Danh sách sinh viên thi học kì')

    def load_file_CBDL_3(self):
        self.load_file_and_update_label('label_2CT_3', 'Danh sách sinh viên CT2')

    def load_file_Alter_Subject_3(self):
        self.load_file_and_update_label('label_alter_subject_3', 'Danh sách học phần thay thế')
    def XLTL(self,df_svthihk):
        df_svthihk = df_svthihk.drop_duplicates(subset=['MSV', 'Mã học phần'], keep='first')
        return df_svthihk
    def process_SV_2_CT(self,df_svthihk,df_sv2ct):
        # Xử lý các giá trị nan và đổi kiểu dữ liệu của cột sang int
        df_svthihk['MSV mở rộng'] = df_svthihk['MSV'].copy()
                
        df_sv2ct['MSV_CT1'] = df_sv2ct['MSV_CT1'].fillna(0).astype(int)
        # Tạo danh sách các MSV CT 1 từ df2
        msv_ct1_values = set(df_sv2ct['MSV_CT1'])
        # Tạo từ điển mapping giữa MSV CT 1 và MSV CT 2
        msv_mapping = dict(zip(df_sv2ct['MSV_CT1'], df_sv2ct['MSV_CT2']))
        df_svthihk['MSV mở rộng'] = df_svthihk['MSV mở rộng'].apply(lambda x: msv_mapping[x] if x in msv_ct1_values else x)
        return df_svthihk   
    def process_HPTT(self,df_svthihk,df_hptt):
        # Tạo danh sách các mã học phần cũ ở cột MHP ở df3
        df_svthihk['Mã học phần mở rộng']=df_svthihk['Mã học phần'].copy()
        mhp_old = set(df_hptt['Mã học phần'])
        # Tạo từ điển mapping giữa mã học phần cũ và mã học phần thay thế
        mhptt_mapping = dict(zip(df_hptt['Mã học phần'], df_hptt['Mã học phần thay thế']))
        # Tạo danh sách các mã học phần ở df1 trùng với mã học phần cũ
        conditon = df_svthihk['Mã học phần'].isin(mhp_old)
        # Cập nhật vào cột Ghi chú ở df1 
        df_svthihk.loc[conditon, 'Ghi chú'] = df_svthihk.loc[conditon, 'Mã học phần'].map(lambda x: f"Mã học phần cũ: {x}")
        # Cập nhật trong cột Mã học phần ở df1
        df_svthihk['Mã học phần mở rộng'] = df_svthihk['Mã học phần'].apply(lambda x: mhptt_mapping[x] if x in mhp_old else x)
        return df_svthihk
    def process_sv_thoi_hoc(self, df_svthihk):
        conditions = ['SV đã thôi học', 'SV rút HP', 'SV tạm ngừng học']
        return df_svthihk[~df_svthihk['Ghi chú'].str.contains('|'.join(conditions), case=False, na=False)]
    def process_sv_mienTA(self,df_svthihk):
        condition = 'Miễn'
        return df_svthihk[~df_svthihk['HP miễn ngoại ngữ'].str.contains(condition, case=False, na=False)]
    def process_HPTA(self, df_svthihk):
        df_svthihk['Mã học phần mở rộng']=df_svthihk['Mã học phần'].copy()
        for index, row in df_svthihk.iterrows():
                        if isinstance(row['Đề thi TA'], str) and 'x' in row['Đề thi TA']:
                                if not row['Mã học phần mở rộng'].endswith('_Anh'):
                                        df_svthihk.at[index, 'Mã học phần mở rộng'] += '_Anh'
                                
        return df_svthihk
    def process_HPTA_HPTT(self,df_svthihk,df_hptt):
                df_svthihk['Mã học phần mở rộng']=df_svthihk['Mã học phần'].copy()
                mhp_old = set(df_hptt['Mã học phần'])
                # Tạo từ điển mapping giữa mã học phần cũ và mã học phần thay thế
                mhptt_mapping = dict(zip(df_hptt['Mã học phần'], df_hptt['Mã học phần thay thế']))
                # Tạo danh sách các mã học phần ở df1 trùng với mã học phần cũ
                conditon = df_svthihk['Mã học phần'].isin(mhp_old)
                # Cập nhật vào cột Ghi chú ở df1 
                df_svthihk.loc[conditon, 'Ghi chú'] = df_svthihk.loc[conditon, 'Mã học phần'].map(lambda x: f"Mã học phần cũ: {x}")
                # Cập nhật trong cột Mã học phần ở df1
                df_svthihk['Mã học phần mở rộng'] = df_svthihk['Mã học phần'].apply(lambda x: mhptt_mapping[x] if x in mhp_old else x)
                #
                for index, row in df_svthihk.iterrows():
                        if isinstance(row['Đề thi TA'], str) and 'x' in row['Đề thi TA']:
                                if not row['Mã học phần mở rộng'].endswith('_Anh'):
                                        df_svthihk.at[index, 'Mã học phần mở rộng'] += '_Anh'
                
                return df_svthihk
    def show_result_CBDL(self):
        self.textBrowser_3.clear() 
        if not all([self.label_SVthiHK_3.text(), self.label_2CT_3.text(), self.label_alter_subject_3.text()]):
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn đầy đủ các file đầu vào.")
            return
        self.df_input_tab3 = pd.read_excel(self.label_SVthiHK_3.text())
        self.df_CT2 = pd.read_excel(self.label_2CT_3.text())
        self.df_alter_subject = pd.read_excel(self.label_alter_subject_3.text())
        self.df_svthihk_processed = self.df_input_tab3.copy()
        self.df_svthihk_processed=self.process_HPTA_HPTT(self.df_svthihk_processed, self.df_alter_subject)
        self.df_svthihk_processed=self.process_SV_2_CT(self.df_svthihk_processed, self.df_CT2)
        self.df_svthihk_processed=self.XLTL(self.df_svthihk_processed)
        self.df_svthihk_processed=self.process_sv_mienTA(self.df_svthihk_processed)
        self.df_svthihk_processed=self.process_sv_thoi_hoc(self.df_svthihk_processed)
                # Tính tổng số mã học phần thi Tiếng Anh
        conditions_ruthp = ['SV đã thôi học', 'SV rút HP', 'SV tạm ngừng học']
        conditions_mienTA = 'Miễn'
                
        self.df_CT2['MSV_CT1'] = self.df_CT2['MSV_CT1'].fillna(0).astype(int)
        msv_ct1_values = self.df_CT2[self.df_CT2['MSV_CT1'] != 0]['MSV_CT1'].tolist()
        msv_len=len(msv_ct1_values)
                
        mhp_old = self.df_alter_subject['Mã học phần'].tolist()
        mhp_old_len=len(mhp_old)

        unique_values_hpta = self.df_svthihk_processed[self.df_svthihk_processed['Mã học phần mở rộng'].str.endswith("Anh")]['Mã học phần mở rộng'].unique()
                
        sv_mienTA = self.df_input_tab3[self.df_input_tab3['HP miễn ngoại ngữ'].str.contains(conditions_mienTA, case=False, na=False)]
                
        sv_ruthp = self.df_input_tab3[self.df_input_tab3['Ghi chú'].str.contains('|'.join(conditions_ruthp), case=False, na=False)]
                # msv_values = len(df_1[df_1['Mã học phần'].str.endswith("Anh")]['MSV'].unique())
        total_hpta_anh = len(unique_values_hpta)
        
                
                # In ra tổng số mã học phần thi Tiếng Anh
        self.textBrowser_3.insertPlainText(f"Tổng số học phần thay thế đã được xử lý: {mhp_old_len}\n")
                
        self.textBrowser_3.insertPlainText(f"Tổng số sinh viên học 2 chương trình đã được xử lý: {msv_len}\n")
                
        self.textBrowser_3.insertPlainText(f"Tổng số mã học phần thi Tiếng Anh đã được xử lý: {total_hpta_anh}\n")     
                
        self.textBrowser_3.insertPlainText(f"Tổng số sinh viên miễn học phần Tiếng Anh đã được lọc: {len(sv_mienTA)}\n")   
                #
        self.textBrowser_3.insertPlainText(f"Tổng số sinh viên thôi học, tạm ngừng học, rút học phần đã được lọc: {len(sv_ruthp)}\n")

    def save_data_CBDL(self):
                # Kiểm tra xem df_sv2ct và df_2 đã được khởi tạo chưa
                if not all([self.label_SVthiHK_3.text(), self.label_2CT_3.text(), self.label_alter_subject_3.text()]):
                    QMessageBox.warning(self, "Lỗi", "Vui lòng chọn đầy đủ các file đầu vào.")
                    return
                elif self.df_svthihk_processed is None:
                        QMessageBox.warning(None, "Lỗi", "Chưa thực hiện chuẩn bị dữ liệu")
                        return

                
                # Mở hộp thoại để chọn vị trí lưu file
                file_dialog = QFileDialog()
                file_path, _ = file_dialog.getSaveFileName(None, "Lưu file", "", "Excel Files (*.xlsx *.xls)")
                if not file_path:  # Kiểm tra nếu người dùng không chọn vị trí lưu file
                        QMessageBox.warning(self, "Lỗi", "Bạn chưa chọn vị trí để lưu tập tin. Vui lòng chọn một vị trí để lưu.")
                        return
                # Lưu dữ liệu đã xử lý ra file Excel
                self.df_svthihk_processed.to_excel(file_path, index=False)
                QMessageBox.information(None, "Thành công", "Dữ liệu đã được lưu thành công")

    # Tab 1 methods
    def load_file_PhanLich(self):
        self.load_file_and_update_label('label_SVthiHK', 'Danh sách sinh viên thi học kì')

    def load_file_Student_CT2(self):
        self.load_file_and_update_label('label_2CT', 'Danh sách sinh viên CT2')

    def load_file_Alter_Subject(self):
        self.load_file_and_update_label('label_alter_subject', 'Danh sách học phần thay thế')

    def load_file_ChuanBiDuLieu(self):
        self.load_file_and_update_label('label_cbdl', 'Danh sách tiền xử lý dữ liệu')

    def load_file_and_update_label(self, label_name, dialog_title):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, dialog_title, "", "Excel Files (*.xlsx *.xls);;All Files (*)", options=options)
        if file_name:
            label = getattr(self, label_name)
            label.setText(file_name)
    def remove_duplicates(self):
        self.df_input_tab1 = self.df_input_tab1.drop_duplicates()

    def student_CT2(self):
        df_CT2_unique = self.df_CT2.drop_duplicates(subset='MSV_CT1')
        msv_ct1_to_ct2 = df_CT2_unique.set_index('MSV_CT1')['MSV_CT2'].to_dict()

        if 'MSV mở rộng' not in self.df_input_tab1.columns:
            self.df_input_tab1['MSV mở rộng'] = None

        self.df_input_tab1['MSV mở rộng'] = self.df_input_tab1['MSV'].map(msv_ct1_to_ct2).fillna(self.df_input_tab1['MSV'])

    def alter_subject(self):
        subject_mapping = self.df_alter_subject.set_index('Mã học phần')['Mã học phần thay thế'].to_dict()

        if 'Mã học phần mở rộng' not in self.df_input_tab1.columns:
            self.df_input_tab1['Mã học phần mở rộng'] = None

        self.df_input_tab1['Mã học phần mở rộng'] = self.df_input_tab1['Mã học phần'].map(subject_mapping).fillna(self.df_input_tab1['Mã học phần'])

        self.df_input_tab1['Ghi chú'] = self.df_input_tab1.apply(lambda row: f"Mã học phần cũ: {row['Mã học phần']}" if row['Mã học phần'] in subject_mapping else row['Ghi chú'], axis=1)

    def remove_foreign_language_exempted_students(self):
        self.df_input_tab1 = self.df_input_tab1[~self.df_input_tab1['HP miễn ngoại ngữ'].str.contains('Miễn', case=False, na=False)]

    def remove_discontinued_students(self):
        self.df_input_tab1 = self.df_input_tab1[~self.df_input_tab1['Ghi chú'].str.contains('SV tạm ngừng học|SV đã thôi học|SV rút HP', case=False, na=False)]

    def english_exam(self):
        self.df_input_tab1.loc[self.df_input_tab1['Đề thi TA'].str.contains('x', case=False, na=False), 'Mã học phần mở rộng'] += '_Anh'

    # def compare_files(self):
    #     common_columns = list(set(self.df_input_tab1.columns) & set(self.df_cbdl.columns))
    #     differences = pd.concat([self.df_input_tab1[common_columns], self.df_cbdl[common_columns]]).drop_duplicates(keep=False)

    #     if differences.empty:
    #         return "File dữ liệu tiền xử lý đã chính xác.", None
    #     else:
    #         return None, differences
    def compare_data(self, df_input, df_cbdl):
        conditions_ruthp = ['SV đã thôi học', 'SV rút HP', 'SV tạm ngừng học']
        conditions_mienTA = 'Miễn'

        # Tạo tập hợp các tuple (MSV, Mã học phần)
        df_input_ids = set(zip(df_input['MSV'], df_input['Mã học phần']))
        df_cbdl_ids = set(zip(df_cbdl['MSV'], df_cbdl['Mã học phần']))

        missing_in_cbdl = df_input_ids - df_cbdl_ids
        extra_in_cbdl = df_cbdl_ids - df_input_ids

        differences = pd.DataFrame(columns=['Thông điệp', 'MSV', 'Mã học phần', 'Tên học phần', 'Ghi chú'])

        # Xử lý sinh viên thiếu trong file CBdL
        if missing_in_cbdl:
            missing_students_info = df_input[df_input.apply(lambda x: (x['MSV'], x['Mã học phần']) in missing_in_cbdl, axis=1)]
            missing_students_info['Thông điệp'] = 'Sinh viên thiếu trong file chuẩn bị dữ liệu'
            differences = pd.concat([differences, missing_students_info[['Thông điệp', 'MSV', 'Mã học phần', 'Tên học phần', 'Ghi chú']]])

        if extra_in_cbdl:
            unnecessary_students_info = df_cbdl[df_cbdl.apply(lambda x: (x['MSV'], x['Mã học phần']) in extra_in_cbdl, axis=1)]
            unnecessary_students_info['Thông điệp'] = 'Sinh viên không có trong file chuẩn bị dữ liệu nhưng có trong file danh sách sinh viên thi học kì'
            differences = pd.concat([differences, unnecessary_students_info[['Thông điệp', 'MSV', 'Mã học phần', 'Tên học phần', 'Ghi chú']]])

        # Xử lý sinh viên được miễn thi ngoại ngữ
        sv_mienTA = df_input[df_input['HP miễn ngoại ngữ'].str.contains(conditions_mienTA, case=False, na=False)]
        if not sv_mienTA.empty:
            sv_mienTA['Thông điệp'] = 'Sinh viên được miễn ngoại ngữ vẫn còn trong file tiền xử lý dữ liệu'
            differences = pd.concat([differences, sv_mienTA[['Thông điệp', 'MSV', 'Mã học phần', 'Tên học phần', 'Ghi chú']]])

        # Xử lý sinh viên đã thôi học, rút học phần, tạm ngừng học
        sv_ruthp = df_input[df_input['Ghi chú'].str.contains('|'.join(conditions_ruthp), case=False, na=False)]
        if not sv_ruthp.empty:
            sv_ruthp['Thông điệp'] = 'Sinh viên tạm ngừng học | SV đã thôi học | SV rút HP vẫn còn trong file tiền xử lý dữ liệu'
            differences = pd.concat([differences, sv_ruthp[['Thông điệp', 'MSV', 'Mã học phần', 'Tên học phần', 'Ghi chú']]])

        return differences
    def Show_KtrDL(self):
        self.textBrowser.clear()

        # Check if all necessary files are loaded
        if not all([self.label_SVthiHK.text(), self.label_2CT.text(), self.label_alter_subject.text(), self.label_cbdl.text()]):
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn đầy đủ các file đầu vào.")
            return

        try:
            # Read the input files based on the paths in labels
            self.df_input_tab1 = pd.read_excel(self.label_SVthiHK.text())
            self.df_CT2 = pd.read_excel(self.label_2CT.text())
            self.df_alter_subject = pd.read_excel(self.label_alter_subject.text())
            self.df_cbdl = pd.read_excel(self.label_cbdl.text())

            # Perform data processing steps
            self.remove_duplicates()
            self.student_CT2()
            self.alter_subject()
            self.remove_foreign_language_exempted_students()
            self.remove_discontinued_students()
            self.english_exam()

            # Compare data and retrieve differences
            differences_data = self.compare_data(self.df_input_tab1, self.df_cbdl)

            # Show the results in textBrowser
            if not differences_data.empty:
                self.textBrowser.append("Thông tin chi tiết về sự khác biệt trong dữ liệu:\n")
                output_data = "Thông điệp\t\t\t\tMSV\tMã học phần\n"
                for index, row in differences_data.iterrows():
                    thong_diep = row['Thông điệp']
                    msv = row['MSV']
                    ma_hoc_phan = row['Mã học phần']
                    output_data += f"{thong_diep}\t{msv}\t{ma_hoc_phan}\n"
                self.textBrowser.append(output_data)

                # Store differences data for exporting
                self.differences = differences_data

            else:
                self.textBrowser.append("Không có sự khác biệt nào được tìm thấy.")

            # Display summary information if needed
            if hasattr(self, 'differences'):
                print(self.differences.head())

        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Lỗi xử lý dữ liệu: {str(e)}")


    def export_differences(self):
        save_path, _ = QFileDialog.getSaveFileName(None, "Lưu file khác biệt", "", "Excel Files (*.xlsx *.xls)")
        if not hasattr(self, 'differences') or self.differences is None:
            QMessageBox.warning(None, "Cảnh báo", "Không tìm thấy thông tin khác biệt. Vui lòng chạy phương thức 'Kiểm tra file CBDL'  trước khi xuất file.")
            return
        if not save_path:
            QMessageBox.warning(None, "Lỗi", "Chưa chọn nơi lưu file.")
            return
        
        
        try:
            desired_columns = [
                'Thông điệp', 'MSV', 'Mã học phần', 'Tên học phần',
                'Ghi chú'
            ]
            self.differences = self.differences[desired_columns]

            with pd.ExcelWriter(save_path, engine='xlsxwriter') as writer:
                self.differences.to_excel(writer, index=False, sheet_name='Sheet1')

                workbook = writer.book
                worksheet = writer.sheets['Sheet1']

                # Ghi tên cột vào sheet Excel
                for col_num, value in enumerate(self.differences.columns):
                    cell_format = workbook.add_format({'text_wrap': True, 'valign': 'top'})
                    worksheet.write(0, col_num, value, cell_format)
                for i, col in enumerate(desired_columns):
                    max_len = self.differences[col].astype(str).map(len).max()  # Tìm chiều dài lớn nhất của cột
                    max_len = max(max_len, len(col))  # Lấy max với chiều dài tên cột
                    worksheet.set_column(i, i, max_len)  # Đặt chiều rộng tối thiểu cho cột i
            QMessageBox.information(None, "Thông báo", "File đã được xuất thành công.")
        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Lỗi khi xuất file: {str(e)}")
    # tab2 methods
    def load_file_PhanLich_tab2(self):
        self.load_file_and_update_label_tab2('label_SVPhanLich', 'Danh sách sinh viên đã phân lịch thi')
    def load_file_CBDL(self):
        self.load_file_and_update_label_tab2('label_cbdl_tab2', 'Danh sách tiền xử lý dữ liệu')
    def load_file_date(self):
        self.load_file_and_update_label_tab2('label_date', 'Danh sách ngày thi')
    def load_file_object(self):
        self.load_file_and_update_label_tab2('label_subject', 'Danh sách học phần - khoa')
    def load_file_room(self):
        self.load_file_and_update_label_tab2('label_room', 'Danh sách phòng thi')
    def load_file_and_update_label_tab2(self, label_name, dialog_title):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, dialog_title, "", "Excel Files (*.xlsx *.xls);;All Files (*)", options=options)
        if file_name:
            label = getattr(self, label_name)
            label.setText(file_name)
    def add_violation(self, violations, violation_type, result_code, message, subject_id="", subject_name="", student_id="", exam_date="", exam_time="", extra_info=""):
        violation = {
            "Loại kiểm tra": violation_type,
            "Mã kết quả": result_code,
            "Thông điệp": message,
            "Mã học phần mở rộng": subject_id,
            "Tên học phần": subject_name,
            "Mã sinh viên mở rộng": student_id,
            "Ngày thi": exam_date,
            "Giờ thi": exam_time,
            "Ghi chú": extra_info,
        }
        violations.append(violation)
    #ktr số lượng sv mỗi ca
    def check_student_per_shift(self, df):
        count_student = df.groupby(['MSV mở rộng', 'Ngày thi', 'Giờ thi']).size().reset_index(name='count')
        violating_students = count_student[count_student['count'] > 1]
        violations = []

        if violating_students.empty:
            self.add_violation(violations, "check_student_per_shift", 0, "Tất cả sinh viên chỉ thi một môn trong một ca thi")
        else:
            for index, row in violating_students.iterrows():
                # Lấy danh sách các môn học mà sinh viên đã thi trong cùng một ca thi
                subjects_thi = df[(df['MSV mở rộng'] == row['MSV mở rộng']) & 
                                        (df['Ngày thi'] == row['Ngày thi']) & 
                                        (df['Giờ thi'] == row['Giờ thi'])]['Mã học phần'].unique()
                extra_info = f"Mã học phần: {', '.join(subjects_thi)}"
                self.add_violation(violations, "check_student_per_shift", 3, 'Sinh viên thi 2 môn trong 1 ca', 
                                student_id=row['MSV mở rộng'], exam_date=row['Ngày thi'], exam_time=row['Giờ thi'],
                                extra_info=extra_info)

        return pd.DataFrame(violations)
    #ktr có đầy đủ hp và sv
    def check_subject_student_list(self, df, df_cbdl):
        master_subjects = set(df_cbdl['Mã học phần mở rộng'].unique())
        missing_info = []

        for subject in master_subjects:
            current_students = set(df[df['Mã học phần mở rộng'] == subject]['MSV mở rộng'].unique())
            master_students = set(df_cbdl[df_cbdl['Mã học phần mở rộng'] == subject]['MSV mở rộng'].unique())
            missing_students = master_students - current_students
            if missing_students:
                missing_students = [str(student) for student in missing_students]
                for student_id in missing_students:
                    subject_name = df_cbdl[df_cbdl['Mã học phần mở rộng'] == subject]['Tên học phần'].iloc[0]  # Lấy tên học phần từ df_cbdl

                    self.add_violation(missing_info, "check_subject_student_list", 3, "MSV bị thiếu", subject_id=subject, subject_name=subject_name, student_id=student_id)

        missing_subjects = master_subjects - set(df['Mã học phần mở rộng'].unique())
        if missing_subjects:
            for subject_id in missing_subjects:
                subject_name = df_cbdl[df_cbdl['Mã học phần mở rộng'] == subject_id]['Tên học phần'].iloc[0]  # Lấy tên học phần từ df_cbdl

                self.add_violation(missing_info, "check_subject_student_list", 3, "Mã học phần bị thiếu", subject_id=subject_id, subject_name=subject_name)

        if missing_info:
            return pd.DataFrame(missing_info)
        else:
            self.add_violation(missing_info, "check_subject_student_list", 0, "Tất cả các học phần và sinh viên đã đủ")
            return pd.DataFrame(missing_info)
    #
    def check_student_in_room(self, df,df_room_tab2):
        violations = []

        for subject, subject_data in df.groupby('Mã học phần mở rộng'):
            students_of_subject = len(subject_data)
            subject_name = df[df['Mã học phần mở rộng'] == subject]['Tên học phần'].iloc[0]
            rooms_for_students = subject_data.groupby(['Giờ thi', 'Ngày thi', 'Mã phòng']).size().reset_index(name='num_students')

            num_rooms = len(rooms_for_students)
            if num_rooms>1:
                avg_STUDENTS_PER_ROOM = students_of_subject / num_rooms
                if avg_STUDENTS_PER_ROOM < self.LOW_OCCUPANCY_THRESHOLD:
                        room_info_list = []
                        for index, row in rooms_for_students.iterrows():
                            exam_time = row['Giờ thi']
                            exam_date = row['Ngày thi']
                            room = row['Mã phòng']
                            num_students = row['num_students']
                            max_seats = df_room_tab2[df_room_tab2['Mã phòng'] == room]['Chỗ ngồi'].iloc[0]
                            room_info_list.append(f"Mã phòng {room} có {num_students} sinh viên") 
                            
                        room_info = ", ".join(room_info_list)
                        self.add_violation(violations,
                                                    "check_student_in_room", 
                                                    1,
                                                    "Số lượng sinh viên của mã học phần ít nhưng được chia nhiều phòng",
                                                    subject_id=subject,
                                                    subject_name=subject_name,
                                                    exam_date=exam_date,
                                                    exam_time=exam_time,
                                                    extra_info=room_info)
                else:
                    for shift, shift_data in subject_data.groupby('Giờ thi'):
                        for room, students_of_room in shift_data.groupby('Mã phòng'):
                            num_students = len(students_of_room)
                            max_seats = df_room_tab2[df_room_tab2['Mã phòng'] == room]['Chỗ ngồi'].iloc[0]
                            if num_students>self.THRESHOLD or num_students > max_seats:
                                room_info = f"Mã phòng {room} có {num_students} sinh viên, vượt quá số chỗ ngồi {max_seats}"
                                self.add_violation(violations,
                                                "check_student_in_room", 
                                                3,
                                                "Phòng thi có số lượng sinh viên vượt quá quy mô của phòng",
                                                subject_id=subject,
                                                exam_date=students_of_room['Ngày thi'].iloc[0],  # Lấy ngày thi từ dòng đầu tiên
                                                exam_time=shift,
                                                extra_info=room_info)

        if violations:
            return pd.DataFrame(violations)
        else:
            self.add_violation(violations, 
                            "check_student_in_room", 
                            0, 
                            "Tất cả các phòng đều không có vượt quá quy mô")
            return pd.DataFrame(violations)

    def check_alter_subjects(self, df):
        alt_subject_dict = df.groupby('Mã học phần mở rộng')['Mã học phần'].apply(list).to_dict()
        notified_subjects = set()
        violations = []
        for main_subject, alt_subjects in alt_subject_dict.items():
        # Lấy dữ liệu các học phần chính và thay thế có cùng Mã học phần mở rộng, Giờ thi, và Ngày thi
            alt_sessions = df[df['Mã học phần mở rộng'].isin([main_subject] + alt_subjects)][['Mã học phần mở rộng', 'Giờ thi', 'Ngày thi']]
            
            # Tìm các học phần có số lượng sinh viên vượt quá MAX_STUDENTS_PER_SHIFT
            large_subjects = alt_sessions['Mã học phần mở rộng'].value_counts()
            large_subjects = large_subjects[large_subjects > self.MAX_STUDENTS_PER_SHIFT].index

            for subject in large_subjects:
                if subject in notified_subjects:
                    continue

                subject_df = alt_sessions[alt_sessions['Mã học phần mở rộng'] == subject]
                subject_name = df[df['Mã học phần mở rộng'] == subject]['Tên học phần'].iloc[0] 
                # Kiểm tra nếu học phần thi cùng ca
                if len(subject_df) <= self.MAX_STUDENTS_PER_SHIFT:
                    if subject_df.groupby(['Giờ thi', 'Ngày thi']).size().gt(1).any():
                        for index, row in subject_df.iterrows():
                            self.add_violation(violations, "check_alter_subjects", 2, "Các học phần thay thế không thi cùng ca", subject_id=subject, subject_name=subject_name, exam_date=row['Ngày thi'], exam_time=row['Giờ thi'])
                        notified_subjects.update(alt_subjects)
                else:
                    for exam_date, daily_sessions in subject_df.groupby('Ngày thi'):
                        sessions = daily_sessions['Giờ thi'].unique()
                        sorted_sessions = sorted(sessions, key=lambda x: self.SHIFT.index(x))
                        for i in range(len(sessions)-1):
                            if not ((sorted_sessions[i] == '07h00' and sorted_sessions[i+1] == '09h00') or (sorted_sessions[i] == '13h30' and sorted_sessions[i+1] == '15h30')):
                                self.add_violation(violations, "check_alter_subjects", 2, "Số lượng sinh viên vượt quá quy mô của 1 ca và không được chia vào các ca liên tiếp", subject_id=main_subject, subject_name=subject_name, exam_date=exam_date, exam_time=sessions[i])
                    notified_subjects.add(main_subject)

        if violations:
            return pd.DataFrame(violations)
        else:
            self.add_violation(violations, "check_alter_subjects", 0, "Tất cả học phần thay thế nhau thi cùng 1 ca")
            return pd.DataFrame(violations)


    def check_count_room_shift(self, df):
        reused_message_printed = False
        dates = df['Ngày thi'].unique()
        violations = []
        for date in dates:
            daily_sessions = df[df['Ngày thi'] == date]
            shifts = daily_sessions['Giờ thi'].unique()

            for shift_pair in [(self.SHIFT[0], self.SHIFT[1]), (self.SHIFT[2], self.SHIFT[3])]:
                shift1, shift2 = shift_pair
                if shift1 in shifts and shift2 in shifts:
                    shift1_rooms = daily_sessions[daily_sessions['Giờ thi'] == shift1]['Mã phòng'].unique()
                    shift2_rooms = daily_sessions[daily_sessions['Giờ thi'] == shift2]['Mã phòng'].unique()
                    shift1_count=len(shift1_rooms)
                    shift2_count=len(shift2_rooms)
                    shift_rooms_count = abs(len(shift1_rooms) - len(shift2_rooms))
                    if shift_rooms_count > 3:
                        self.add_violation(violations, "check_count_room_shift", 2, "Có sự chênh lệch phòng giữa các ca thi", exam_date=date, extra_info=f"Chênh lệch {shift_rooms_count} phòng giữa ca thi {shift1} và {shift2}. Số phòng ca {shift1}: {shift1_count}, Số phòng ca {shift2}: {shift2_count}.")
                        reused_message_printed = True

        if not violations:
            self.add_violation(violations, "check_count_room_shift", 0, "Số lượng phòng của 2 ca không có sự chênh lệch")

        return pd.DataFrame(violations)

    def check_room_reuse(self, df):
        reused_message_printed = False
        dates = df['Ngày thi'].unique()
        violations = []

        for date in dates:
            daily_sessions = df[df['Ngày thi'] == date]
            for shift_pair in [(self.SHIFT[0], self.SHIFT[1]), (self.SHIFT[2], self.SHIFT[3])]:
                current_shift = daily_sessions[daily_sessions['Giờ thi'] == shift_pair[0]]
                next_shift = daily_sessions[daily_sessions['Giờ thi'] == shift_pair[1]]

                current_shift_rooms = current_shift['Mã phòng'].unique()
                next_shift_rooms = next_shift['Mã phòng'].unique()

                reused_rooms = set(current_shift_rooms).intersection(next_shift_rooms)
                non_reused_rooms = set(next_shift_rooms) - reused_rooms

                if non_reused_rooms:
                    non_reused_rooms_list = ', '.join(map(str, non_reused_rooms))
                    room_count = len(non_reused_rooms)
                    message = f"Ca thi sau không sử dụng lại phòng của ca thi trước trong cùng buổi"
                    extra_info = f"Giờ thi {shift_pair[1]} không sử dụng lại {room_count} phòng từ giờ thi {shift_pair[0]}: {non_reused_rooms_list}"

                    # Thêm vi phạm một lần cho mỗi cặp ngày và ca thi
                    self.add_violation(violations, 
                                    "check_room_reuse", 
                                    2, 
                                    message, 
                                    exam_date=date, 
                                    exam_time=shift_pair[1], 
                                    extra_info=extra_info)
                    reused_message_printed = True

        if not violations:
            self.add_violation(violations, "check_room_reuse", 0, "Tất cả các mã phòng đều được sử dụng lại")

        return pd.DataFrame(violations)

    def check_exam_datetime(self, df, df_date):
        valid_times = df_date['Giờ thi'].tolist()
        valid_dates = pd.to_datetime(df_date['Ngày thi'], dayfirst=True).dt.date.tolist()
        violations = []

        for index, row in df.iterrows():
            exam_date = pd.to_datetime(row['Ngày thi'], dayfirst=True).date()
            exam_time = row['Giờ thi']

            if exam_date not in valid_dates:
                self.add_violation(violations, "check_exam_datetime", 2, "Ngày thi không hợp lệ", subject_id=row['Mã học phần mở rộng'], exam_date=row['Ngày thi'], exam_time=row['Giờ thi'], extra_info=f"Ngày thi {exam_date} không hợp lệ")
            if exam_time not in valid_times:
                self.add_violation(violations, "check_exam_datetime", 2, "Giờ thi không hợp lệ", subject_id=row['Mã học phần mở rộng'], exam_date=row['Ngày thi'], exam_time=row['Giờ thi'], extra_info=f"Ca thi {exam_time} không hợp lệ")

        if not violations:
            self.add_violation(violations, "check_exam_datetime", 0, "Ngày và giờ thi bình thường")

        return pd.DataFrame(violations)


    def calculate_required_rooms(self,df_cbdl):
        required_rooms = {}

        for ma_hoc_phan, group in df_cbdl.groupby('Mã học phần mở rộng'):
            total_students = len(group)

            if total_students <= self.THRESHOLD:
                # required_rooms[ma_hoc_phan] = (1, [total_students])       
                required_rooms[ma_hoc_phan] = 1       
            else:
                rooms_needed = (total_students + self.STUDENTS_PER_ROOM - 1) // self.STUDENTS_PER_ROOM
                if total_students > self.MAX_STUDENTS_PER_SHIFT and rooms_needed % 2 != 0:
                    rooms_needed += 1

                base_STUDENTS_PER_ROOM = total_students // rooms_needed
                students_distribution = [base_STUDENTS_PER_ROOM] * rooms_needed

                for i in range(total_students % rooms_needed):
                    students_distribution[i] += 1

                required_rooms[ma_hoc_phan] = rooms_needed
                # # Initial room calculation
                # rooms_needed = total_students// self.STUDENTS_PER_ROOM
                # if total_students > self.MAX_STUDENTS_PER_SHIFT and rooms_needed % 2 != 0:
                #     rooms_needed += 1
                # # Basic student distribution per room
                # base_STUDENTS_PER_ROOM = total_students // rooms_needed
                # students_distribution = [base_STUDENTS_PER_ROOM] * rooms_needed
                
                # # Calculate remaining students
                # remaining_students = total_students % rooms_needed
                
                # if remaining_students > 0:
                #     if remaining_students <= 20:
                #         for i in range(remaining_students):
                #             students_distribution[i] += 1
                #     else:
                #         rooms_needed += 1
                #         base_STUDENTS_PER_ROOM = total_students // rooms_needed
                #         students_distribution = [base_STUDENTS_PER_ROOM] * rooms_needed
                #         remaining_students = total_students % rooms_needed
                #         for i in range(remaining_students):
                #             students_distribution[i] += 1
                
                # # Ensure the rooms are as evenly distributed as possible
                # if rooms_needed > 1:
                #     while True:
                #         max_students = max(students_distribution)
                #         min_students = min(students_distribution)
                #         if max_students - min_students <= 5:
                #             break
                #         max_index = students_distribution.index(max_students)
                #         min_index = students_distribution.index(min_students)
                #         students_distribution[max_index] -= 1
                #         students_distribution[min_index] += 1
                # required_rooms[ma_hoc_phan] = (rooms_needed, students_distribution)


        return required_rooms


    # def check_room_assignment(self, df_cbdl, df):
    #     required_rooms_count = self.calculate_required_rooms(df_cbdl)
    #     violations = []

    #     # Loại bỏ các bản ghi trùng lặp dựa trên 'Ca thi', 'Mã học phần mở rộng' và 'Mã phòng'
    #     df_unique_rooms = df.drop_duplicates(subset=['Giờ thi', 'Mã học phần mở rộng', 'Mã phòng'])

    #     # Nhóm các sinh viên theo 'Mã học phần mở rộng' và tính tổng số lượng phòng duy nhất cho mỗi mã học phần mở rộng
    #     assigned_rooms = df_unique_rooms.groupby(['Mã học phần mở rộng', 'Giờ thi'])['Mã phòng'].nunique().reset_index()
    #     assigned_rooms_total = assigned_rooms.groupby('Mã học phần mở rộng')['Mã phòng'].sum()

    #     # for subject, (required_rooms, students_distribution) in required_rooms_count.items():
    #     for subject, required_rooms in required_rooms_count.items():
    #         if subject in assigned_rooms_total:
    #             assigned_rooms_count = assigned_rooms_total[subject]
    #             subject_rooms = df_unique_rooms[df_unique_rooms['Mã học phần mở rộng'] == subject]['Mã phòng'].unique()
    #         else:
    #             assigned_rooms_count = 0
    #             subject_rooms = []
    #         subject_name = df_cbdl[df_cbdl['Mã học phần mở rộng'] == subject]['Tên học phần'].iloc[0]
            
    #         for index, row in assigned_rooms.iterrows():
    #             if row['Mã học phần mở rộng'] == subject:
    #                 exam_time = row['Giờ thi']
    #                 exam_date = df_unique_rooms[(df_unique_rooms['Mã học phần mở rộng'] == subject) & (df_unique_rooms['Giờ thi'] == exam_time)]['Ngày thi'].iloc[0]
    #                 if assigned_rooms_count < required_rooms:
    #                     extra_info = f"Có thể cần thêm {abs(required_rooms - assigned_rooms_count)} phòng"
    #                     self.add_violation(violations, 
    #                                     "check_room_assignment", 
    #                                     1, 
    #                                     "Mã học phần mở rộng cần thêm phòng thi", 
    #                                     subject_id=subject, 
    #                                     subject_name=subject_name, 
    #                                     exam_date=exam_date, 
    #                                     exam_time=exam_time)
    #                 elif assigned_rooms_count > required_rooms:
    #                     excess_rooms = subject_rooms[-(assigned_rooms_count - required_rooms):]
    #                     remaining_rooms = set(subject_rooms) - set(excess_rooms)
    #                     extra_info = f"Phòng {' ,'.join(excess_rooms)}, {' ,'.join(remaining_rooms)} có thể gộp phòng"
    #                     self.add_violation(violations, 
    #                                     "check_room_assignment", 
    #                                     1, 
    #                                     "Các phòng thi của mã học phần mở rộng có thể gộp phòng", 
    #                                     subject_id=subject, 
    #                                     subject_name=subject_name, 
    #                                     exam_date=exam_date, 
    #                                     exam_time=exam_time, 
    #                                     extra_info=extra_info)

    #     if not violations:
    #         self.add_violation(violations, "check_room_assignment", 0, "Đã gán đủ phòng cho tất cả các mã học phần mở rộng")

    #     return pd.DataFrame(violations)
    def check_room_assignments_and_student_distribution(self, df_cbdl, df, df_room_tab2):
        required_rooms_count = self.calculate_required_rooms(df_cbdl)
        violations = []

        # Remove duplicate records based on 'Giờ thi', 'Mã học phần mở rộng' and 'Mã phòng'
        df_unique_rooms = df.drop_duplicates(subset=['Giờ thi', 'Mã học phần mở rộng', 'Mã phòng'])

        # Group students by 'Mã học phần mở rộng' and calculate the total number of unique rooms for each subject
        assigned_rooms = df_unique_rooms.groupby(['Mã học phần mở rộng', 'Giờ thi'])['Mã phòng'].nunique().reset_index()
        assigned_rooms_total = assigned_rooms.groupby('Mã học phần mở rộng')['Mã phòng'].sum()

        for subject, required_rooms in required_rooms_count.items():
            assigned_rooms_count = assigned_rooms_total.get(subject, 0)
            subject_rooms = df_unique_rooms[df_unique_rooms['Mã học phần mở rộng'] == subject]['Mã phòng'].unique()
            subject_name = df_cbdl[df_cbdl['Mã học phần mở rộng'] == subject]['Tên học phần'].iloc[0]

            # Check room assignments
            if assigned_rooms_count < required_rooms:
                extra_info = f"Có thể cần thêm {abs(required_rooms - assigned_rooms_count)} phòng"
                self.add_violation(violations,
                                "check_room_assignments_and_student_distribution",
                                1,
                                "Mã học phần mở rộng cần thêm phòng thi",
                                subject_id=subject,
                                subject_name=subject_name,
                                extra_info=extra_info)
            elif assigned_rooms_count > required_rooms:
                excess_rooms = subject_rooms[-(assigned_rooms_count - required_rooms):]
                remaining_rooms = set(subject_rooms) - set(excess_rooms)
                room_info=''
                # Thu thập thông tin chi tiết về số lượng sinh viên trong từng phòng, bất kể số lượng sinh viên có nhỏ hơn ngưỡng hay không
                room_students_info = []
                for room in subject_rooms:
                    num_students_in_room = len(df[(df['Mã học phần mở rộng'] == subject) & (df['Mã phòng'] == room)])
                    room_students_info.append(f"Phòng {room} có {num_students_in_room} sinh viên")

                # Thêm thông tin số lượng sinh viên trong từng phòng vào `room_info`
                room_info += f"{' ,'.join(room_students_info)}"

                # Kiểm tra nếu số lượng sinh viên trung bình trên mỗi phòng thấp hơn ngưỡng `LOW_OCCUPANCY_THRESHOLD`
                students_of_subject = len(df[df['Mã học phần mở rộng'] == subject])
                if assigned_rooms_count > 1:  # Chỉ thực hiện nếu có hơn một phòng
                    avg_students_per_room = students_of_subject / assigned_rooms_count
                    if avg_students_per_room < self.LOW_OCCUPANCY_THRESHOLD:
                        room_info += " Có thể gộp phòng "
                self.add_violation(violations,
                                "check_room_assignments_and_student_distribution",
                                1,
                                "Số lượng sinh viên ít nhưng được chia nhiều phòng",
                                subject_id=subject,
                                subject_name=subject_name,
                                extra_info=room_info)

            # Check student distribution in rooms
            students_of_subject = len(df[df['Mã học phần mở rộng'] == subject])
            rooms_for_students = df[df['Mã học phần mở rộng'] == subject].groupby(['Giờ thi', 'Ngày thi', 'Mã phòng']).size().reset_index(name='num_students')
            num_rooms = len(rooms_for_students)

            for shift, shift_data in df[df['Mã học phần mở rộng'] == subject].groupby('Giờ thi'):
                for room, students_of_room in shift_data.groupby('Mã phòng'):
                    num_students = len(students_of_room)
                    max_seats = df_room_tab2[df_room_tab2['Mã phòng'] == room]['Chỗ ngồi'].iloc[0]
                    if num_students > self.THRESHOLD or num_students > max_seats:
                        room_info = f"Mã phòng {room} có {num_students} sinh viên, vượt quá số chỗ ngồi {max_seats}"
                        self.add_violation(violations,
                                        "check_room_assignments_and_student_distribution",
                                        3,
                                        "Phòng thi có số lượng sinh viên vượt quá quy mô của phòng",
                                        subject_id=subject,
                                        exam_date=students_of_room['Ngày thi'].iloc[0],
                                        exam_time=shift,
                                        extra_info=room_info)

        if not violations:
            self.add_violation(violations,
                            "check_room_assignments_and_student_distribution",
                            0,
                            "Đã gán đủ phòng cho tất cả các mã học phần mở rộng và không có phòng nào vượt quá quy mô")
        return pd.DataFrame(violations)

    def check_schedule_per_day(self, df_input):
        
        shift_count = df_input.groupby(['MSV mở rộng', 'Ngày thi']).size().reset_index(name='số ca thi')

        # Lọc ra các sinh viên thi quá 2 ca trong một ngày
        violating_students = shift_count[shift_count['số ca thi'] > 2]

        # Đếm số lượng sinh viên vi phạm theo mã học phần mở rộng và ngày thi
        violation_count_per_course = df_input[df_input['MSV mở rộng'].isin(violating_students['MSV mở rộng'])]

        violations = []
        notified_violations = set()  

        # Lấy tất cả các mã học phần mở rộng có sinh viên vi phạm
        violating_courses = violation_count_per_course['Mã học phần mở rộng'].unique()

        for subject_id in violating_courses:
            subject_name = df_input[df_input['Mã học phần mở rộng'] == subject_id]['Tên học phần'].iloc[0]
            # Lọc ra các sinh viên vi phạm trong mã học phần mở rộng đó
            violating_students_in_course = violation_count_per_course[(violation_count_per_course['Mã học phần mở rộng'] == subject_id) & (violation_count_per_course['MSV mở rộng'].isin(violating_students['MSV mở rộng']))]

            # Kiểm tra xem có sinh viên nào thi quá 2 ca trong mã học phần đó không
            if not violating_students_in_course.empty:
                student_count = violating_students_in_course['MSV mở rộng'].nunique()
                violating_students_str = ", ".join(map(str, violating_students_in_course['MSV mở rộng'].unique()))

                # Lấy tất cả các ngày thi và giờ thi của sinh viên vi phạm trong mã học phần đó
                violating_times = violating_students_in_course[['Ngày thi', 'Giờ thi']].drop_duplicates()

                for _, time_row in violating_times.iterrows():
                    exam_date = time_row['Ngày thi']
                    violation_key = (subject_id, subject_name, exam_date, student_count)

                    
                    if violation_key not in notified_violations:
                        extra_info = f'Số lượng sinh viên thi hơn 2 ca thi là: {student_count}'
                        self.add_violation(violations, "check_schedule_per_day", 2, "Sinh viên thi quá 2 ca thi trong 1 ngày", subject_id=subject_id, subject_name=subject_name, exam_date=exam_date, extra_info=extra_info)
                        notified_violations.add(violation_key)

        if not violations:
            self.add_violation(violations, "check_schedule_per_day", 0, "Không có sinh viên nào thi quá 2 ca trong một ngày")

        return pd.DataFrame(violations)

    def read_input_files(self):
        if self.label_SVPhanLich.text():
            self.df_input_tab2 = pd.read_excel(self.label_SVPhanLich.text())
        if self.label_cbdl_tab2.text():
            self.df_cbdl_tab2 = pd.read_excel(self.label_cbdl_tab2.text())
        if self.label_date.text():
            self.df_date_tab2 = pd.read_excel(self.label_date.text())
        if self.label_subject.text():
            self.df_subject_tab2 = pd.read_excel(self.label_subject.text())
        if self.label_room.text():
            self.df_room_tab2=pd.read_excel(self.label_room.text())
        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #         future1 = executor.submit(pd.read_excel, self.label_SVPhanLich.text())
        #         future2 = executor.submit(pd.read_excel, self.label_cbdl_tab2.text())
        #         future3 = executor.submit(pd.read_excel, self.label_date.text())
        #         future4 = executor.submit(pd.read_excel, self.label_subject.text())

        #         self.df_input_tab2 = future1.result()
        #         self.df_cbdl_tab2 = future2.result()
        #         self.df_date_tab2 = future3.result()
        #         self.df_subject_tab2 = future4.result()

    def save_results_to_excel(self, results, output_file, sheet_name='Kết quả'):
        # Tạo DataFrame từ kết quả
        df_results = pd.DataFrame(results)
        columns_to_save = ['Loại kiểm tra', 'Mã kết quả', 'Thông điệp', 'Mã học phần mở rộng',
                        'Tên học phần', 'Mã sinh viên mở rộng', 'Ngày thi', 'Giờ thi', 'Ghi chú']

        # Kiểm tra và điền các cột thiếu vào DataFrame
        for col in columns_to_save:
            if col not in df_results.columns:
                df_results[col] = None 

        df_results.sort_values(by=['Mã kết quả','Loại kiểm tra'], inplace=True)

        try:
            with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
                df_results.to_excel(writer, sheet_name=sheet_name, index=False, header=True)
                # Đối tượng workbook và worksheet
                workbook  = writer.book
                worksheet = writer.sheets[sheet_name]

                # Thiết lập tự động điều chỉnh độ rộng của các cột
                for i, col in enumerate(columns_to_save):
                    max_len = df_results[col].astype(str).map(len).max()  # Tìm chiều dài lớn nhất của cột
                    max_len = max(max_len, len(col))  # Lấy max với chiều dài tên cột
                    worksheet.set_column(i, i, max_len)  # Đặt chiều rộng tối thiểu cho cột i
            print(f"Kết quả đã được lưu vào sheet '{sheet_name}' của file Excel: {output_file}")
        except Exception as e:
            print(f"Lỗi khi lưu file Excel: {e}")

    def Show_KtrPhanLich(self):
        self.textBrowser_2.clear()
        self.read_input_files()
        if self.df_input_tab2 is None or self.df_cbdl_tab2 is None or self.df_date_tab2 is None:
            self.textBrowser_2.setText("Chưa có dữ liệu. Vui lòng chọn dữ liệu đầu vào.")
            return
        printed_messages = set()
        results = []
        results.append(self.check_student_per_shift(self.df_input_tab2))
        results.append(self.check_subject_student_list(self.df_input_tab2, self.df_cbdl_tab2))
        # results.append(self.check_student_in_room(self.df_input_tab2,self.df_room_tab2))
        results.append(self.check_alter_subjects(self.df_input_tab2))
        results.append(self.check_count_room_shift(self.df_input_tab2))
        results.append(self.check_room_reuse(self.df_input_tab2))
        results.append(self.check_exam_datetime(self.df_input_tab2, self.df_date_tab2))
        results.append(self.check_room_assignments_and_student_distribution(self.df_cbdl_tab2, self.df_input_tab2, self.df_room_tab2))  # Sửa tên hàm gọi
        results.append(self.check_schedule_per_day(self.df_input_tab2))
        combined_results = pd.concat(results, ignore_index=True)
        # for index, row in combined_results.iterrows():
        #     message = f"Thông điệp: {row['Thông điệp']}, Mã kết quả: {row['Mã kết quả']}"

        #     # Kiểm tra xem thông điệp đã được in ra trước đó chưa
        #     if message not in printed_messages:
        #         self.textBrowser_2.append(message)
        #         printed_messages.append(message)
        # Tạo từ điển ánh xạ từng loại kiểm tra sang mô tả tương ứng
        detail_info_map = {
        "check_student_per_shift": "Kiểm tra sinh viên thi 1 học phần trong 1 ca",
        "check_subject_student_list": "Kiểm tra danh sách sinh viên theo học phần",
        "check_student_in_room": "Kiểm tra sinh viên trong phòng thi",
        "check_alter_subjects": "Kiểm tra các học phần thay thế",
        "check_count_room_shift": "Kiểm tra số lượng phòng giữa các ca thi",
        "check_room_reuse": "Kiểm tra sử dụng lại phòng thi",
        "check_exam_datetime": "Kiểm tra ngày giờ thi hợp lệ",
        "check_room_assignment": "Kiểm tra phân bổ phòng thi",
        "check_schedule_per_day": "Kiểm tra lịch thi của sinh viên"
    }
        count=1

        for index, row in combined_results.iterrows():
            message = f"{row['Loại kiểm tra']}_{row['Mã kết quả']}"
            
            if message not in printed_messages:
                # detail_info = f"{count}. {detail_info_map.get(row['Loại kiểm tra'], 'Không rõ')}"
                detail_info =f"{count}.Thông điệp: {row['Thông điệp']}\n Mã kết quả: {row['Mã kết quả']}"
                self.textBrowser_2.append(detail_info)
                printed_messages.add(message)

                count += 1  

        # Lưu kết quả vào thuộc tính 
        self.combined_results = combined_results
        # self.XuatfileKtr.setEnabled(True)

    def export_file_KtrDl(self):
        if self.combined_results is None:
            QMessageBox.warning(None, "Lỗi", "Chưa có kết quả kiểm tra để xuất.")
            return

        save_path, _ = QFileDialog.getSaveFileName(None, "Lưu file khác biệt", "", "Excel Files (*.xlsx)")

        if not save_path:
            QMessageBox.warning(None, "Lỗi", "Chưa chọn nơi lưu file.")
            return
        # Lưu kết quả vào file Excel
        self.save_results_to_excel(self.combined_results, save_path, sheet_name='Kết quả')

        QMessageBox.information(None, "Thông báo", "File đã được xuất thành công.")

    
    def create_summary_excel(self):
        self.textBrowser_2.clear()
        try:
            self.read_input_files()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi đọc file đầu vào: {str(e)}")
            return
        
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Lưu File lịch thi tổng hợp", "", "Excel Files (*.xlsx *);;All Files (*)", options=options)
        if file_name:
            if self.df_input_tab2 is None or self.df_subject_tab2 is None:
                QMessageBox.warning(self, "Lỗi", "Vui lòng chọn đầy đủ các file đầu vào cần thiết.")
                return
                
            df = self.df_input_tab2.copy()
            df.dropna(subset=['Mã học phần'], inplace=True)

            department_dict = self.df_subject_tab2.set_index('Mã HP')['Đơn vị'].to_dict()

            df['Khoa'] = df['Mã học phần'].map(department_dict)
            df['Mã học phần thay thế'] = df.apply(lambda row: row['Mã học phần mở rộng'] if row['Mã học phần'] != row['Mã học phần mở rộng'] else '', axis=1)
            
            df['Phòng Thi'] = df.groupby(['Mã học phần', 'Ngày thi', 'Giờ thi'])['Mã phòng'].transform(lambda x: ', '.join(x.unique()))

            df['Số lượng sinh viên của học phần'] = df.groupby('Mã học phần')['MSV mở rộng'].transform('nunique')

            df['Số lượng phòng thi của học phần'] = df.groupby(['Mã học phần', 'Ngày thi', 'Giờ thi'])['Mã phòng'].transform('nunique')

            df['Ghi chú'] = df.apply(lambda row: self.generate_notes(row), axis=1)

            summary_df = df.groupby(['Mã học phần', 'Tên học phần', 'Số tín chỉ', 'Ngày thi', 'Giờ thi', 'Khoa', 'Ghi chú', 'Mã học phần thay thế'], as_index=False).agg({
                'Phòng Thi': lambda x: ','.join(sorted(set(x))),
                'Số lượng sinh viên của học phần': 'first',
                'Số lượng phòng thi của học phần': 'first'
            })

            temp_df = df.groupby(['Ngày thi', 'Giờ thi'])['Mã phòng'].nunique().reset_index()
            temp_df.rename(columns={'Mã phòng': 'Tổng số phòng của ca thi'}, inplace=True)

            summary_df = summary_df.merge(temp_df, on=['Ngày thi', 'Giờ thi'], how='left')

            summary_df['Tổng số phòng của ca thi'] = summary_df['Tổng số phòng của ca thi'].fillna('')

            summary_df.sort_values(by=['Ngày thi', 'Giờ thi'], inplace=True)

            summary_df['STT'] = range(1, len(summary_df) + 1)
            summary_df = summary_df[['STT', 'Mã học phần', 'Tên học phần', 'Mã học phần thay thế', 'Số tín chỉ', 'Ngày thi', 'Giờ thi', 'Phòng Thi', 'Số lượng sinh viên của học phần', 'Số lượng phòng thi của học phần', 'Tổng số phòng của ca thi', 'Khoa', 'Ghi chú']]

            with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
                summary_df.to_excel(writer, index=False, sheet_name='Tổng hợp')

                workbook = writer.book
                worksheet = writer.sheets['Tổng hợp']
                for idx, col in enumerate(summary_df):
                    max_len = max((summary_df[col].astype(str).map(len).max(), len(str(col)))) + 1
                    worksheet.set_column(idx, idx, max_len)
                for col_num, value in enumerate(summary_df.columns.values):
                    worksheet.write(0, col_num, value)

            summary_info = f"File tổng hợp đã được tạo thành công tại: {file_name}\n"
            summary_info += f"Tổng số học phần: {summary_df['Mã học phần'].nunique()}\n"
            summary_info += f"Tổng số ca thi: {summary_df[['Ngày thi', 'Giờ thi']].drop_duplicates().shape[0]}"
            self.textBrowser_2.append(summary_info)

            QMessageBox.information(self, "Thành công", "File tổng hợp đã được tạo thành công.")

        
            
            # except Exception as e:
            #     QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi khi tạo file tổng hợp: {str(e)}")

    def generate_notes(self, row):
        notes = []
        if pd.notna(row.get('Mã học phần mở rộng', '')):  # Kiểm tra nếu giá trị không phải NaN
            if '_Anh' in str(row['Mã học phần mở rộng']):
                notes.append("Thi đề Tiếng Anh")
        if row['Mã học phần'] in ['HRM2001', 'MIS2002', 'MIS2902', 'MGT1902']:
            notes.append("SV làm bài thi trên Elearning")
        return ', '.join(notes) if notes else ''
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())


