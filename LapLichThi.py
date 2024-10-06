from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox,QApplication
import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
import math
import numpy as np

class ToiUu():
    
    # def choose_excel_file():
    #     Tk().withdraw()  # Ẩn cửa sổ chính của tkinter
    #     file_path = askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])  # Chỉ cho phép chọn file Excel
    #     return file_path

    # # Hàm chính để thực thi các hàm trên dữ liệu từ file Excel đã chọn
    # def process_excel_files(self):
    #     if self.df_cbdl is None or self.df_dspt is None or self.df_dsnt is None:
    #         QMessageBox.warning(None, "Lỗi", "Chưa tải đủ dữ liệu")
    #         return
        
    #     df_assigned_schedule = self.assign_exam_schedule(self.df_cbdl.copy(), self.max_shifts, self.max_rooms, self.students_per_room, self.max_shift_per_day)
    #     df_assigned_rooms = self.assign_rooms(df_assigned_schedule.copy(),self.df_dspt,self.students_per_room)
    #     df_assigned_calendar = self.assign_calendar(df_assigned_rooms.copy(),self.df_dspt, self.df_dsnt, self.max_shift_per_day)

    #     file_dialog = QFileDialog()
    #     file_path, _ = file_dialog.getSaveFileName(None, "Lưu file", "", "Excel Files (*.xlsx *.xls)")
    #     if not file_path:  # Kiểm tra nếu người dùng không chọn vị trí lưu file
    #         QMessageBox.warning(None, "Lỗi", "Bạn chưa chọn vị trí để lưu tập tin. Vui lòng chọn một vị trí để lưu.")
    #         return

    #     df_assigned_calendar.to_excel(file_path, index=False)
    #     QMessageBox.information(None, "Thông báo", f"Đã lưu kết quả vào file: {file_path}")

    # def Load_data(self):
    #     # Yêu cầu người dùng chọn tệp dữ liệu Excel
        
    #             file_dialog = QFileDialog()

    #             file_path_1, _ = file_dialog.getOpenFileName(None, "Chọn file dữ liệu đã được xử lý ", "", "Excel Files (*.xlsx *.xls)")
    #             if not file_path_1:
    #                     QMessageBox.warning(None, "Lỗi", "Chưa chọn dữ liệu")
    #                     return
                

                
    #             file_path_2, _ = file_dialog.getOpenFileName(None, "Chọn file dữ liệu phòng thi ", "", "Excel Files (*.xlsx *.xls)")
    #             if not file_path_2:
    #                     QMessageBox.warning(None, "Lỗi", "Chưa chọn dữ liệu")
    #                     return
                
                
    #             file_path_3, _ = file_dialog.getOpenFileName(None, "Chọn file dữ liệu ngày thi ", "", "Excel Files (*.xlsx *.xls)")
    #             if not file_path_3:
    #                     QMessageBox.warning(None, "Lỗi", "Chưa chọn dữ liệu")
    #                     return
    #             df_cbdl= pd.read_excel(file_path_1)
    #             df_dspt= pd.read_excel(file_path_2)       
    #             df_dsnt= pd.read_excel(file_path_3)
    #             self.df_cbdl=df_cbdl
    #             self.df_dspt=df_dspt
    #             self.df_dsnt=df_dsnt
    # Đếm số sinh viên theo mỗi học phần
    def __init__(self):
        self.max_shifts=40
        self.max_rooms=35
        self.students_per_room=40
        self.max_shift_per_day=2
        self.shift_per_day=4
        self.df_cbdl = None
        self.df_dspt = None
        self.df_dsnt = None


    from collections import defaultdict

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
                            if student_exam_count[student][exam_group] >= 2:
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
                    if not any(student_exam_count[student][exam_group] >= 2 for student in students_in_node):  
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
                

            i += 1
        


        self.check_exam_schedule(self.df_cbdl)
        unassigned_courses = df_cbdl[df_cbdl['Ca thi'].isnull()]['Mã học phần mở rộng'].unique()
        print(unassigned_courses)
        
        # for node in unassigned_courses:
        #     assigned = False
        #     jn = 1
        #     while jn <= max_shifts:
        #         current_shift_count = df_cbdl[df_cbdl['Ca thi'] == jn]['MSV mở rộng'].count()
        #         course_students_count = course_students[node]
        #         if (current_shift_count + course_students_count) <= students_per_shift:
        #             exam_group = get_exam_group(jn)
        #             colored_nodes = set(df_cbdl[df_cbdl['Ca thi'] == jn]['Mã học phần mở rộng'].tolist())
        #             students_in_node = df_cbdl[df_cbdl['Mã học phần mở rộng'] == node]['MSV mở rộng']
        #             if all((node, colored_node) not in edges and (colored_node, node) not in edges for colored_node in colored_nodes):
        #                     if not any(student_exam_count[student][exam_group] >= 2 for student in students_in_node):
        #                         df_cbdl.loc[df_cbdl['Mã học phần mở rộng'] == node, 'Ca thi'] = jn
        #                         df_cbdl.loc[df_cbdl['Mã học phần mở rộng'] == node, 'Nhóm ca thi'] = exam_group
        #                         shifts[jn] += course_rooms[node]
                                
        #                         # Cập nhật số lần thi của sinh viên trong nhóm ca thi
        #                         for student in students_in_node:
        #                             student_exam_count[student][exam_group] += 1
                                
        #                         assigned = True
        #                         unassigned_courses = [course for course in unassigned_courses if course != node]
        #                         break
        #         jn+=1
        return df_cbdl





    def check_exam_schedule(self, df_cbdl):

        from collections import defaultdict
        
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






    def assign_rooms(self, df_phancathi, df_dsphongthi, students_per_room):
        df_phancathi['Mã phòng'] = ""
        count_shifts = sorted(df_phancathi['Ca thi'].unique())
        count_rooms = df_dsphongthi['Mã phòng'].unique()
        assigned_rooms_per_shift = {shift: set() for shift in count_shifts}
        for shift in count_shifts:
            course_counts = df_phancathi[df_phancathi['Ca thi'] == shift].groupby('Mã học phần mở rộng')['MSV'].count()
            sorted_courses = course_counts.sort_values(ascending=False).index.tolist()
            for course in sorted_courses:
                no_students = len(df_phancathi[(df_phancathi['Mã học phần mở rộng'] == course) & (df_phancathi['Ca thi'] == shift)])
                rooms_needed = math.ceil(no_students / students_per_room)
                students_per_room_now = math.ceil(no_students / rooms_needed)
                assigned_rooms = 0
                for room in count_rooms:
                    if room not in assigned_rooms_per_shift[shift]:
                        available_students = df_phancathi[(df_phancathi['Mã học phần mở rộng'] == course) & (df_phancathi['Ca thi'] == shift) & (df_phancathi['Mã phòng'] == '')]
                        available_student_count = len(available_students)
                        if available_student_count > 0:
                            df_phancathi.loc[available_students.index[:students_per_room_now], 'Mã phòng'] = room
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

    #         # Xác định các ngày thi duy nhất
    #     unique_days = df_phanphongthi['Ngày thi'].unique()
    #     time_pairs = [['07h00', '09h00'], ['13h30', '15h30']]

    #     # Lặp qua từng ngày để điều chỉnh giờ thi cho các học phần có nhiều hơn 1 ca thi
    #     for day in unique_days:
    #         # Lấy tất cả các ca thi trong ngày hiện tại
    #         day_data = df_phanphongthi[df_phanphongthi['Ngày thi'] == day]

    #         # Nhóm theo học phần và lọc các học phần có nhiều hơn 1 ca thi
    #         courses_with_multiple_shifts = day_data.groupby('Mã học phần mở rộng').filter(lambda x: x['Ca thi'].nunique() > 1)

    #         if not courses_with_multiple_shifts.empty:
    #             # Danh sách các học phần đã phân bổ cặp giờ thi
    #             assigned_courses = {}
    #             used_pairs = set()

    #             # Lặp qua các học phần và phân bổ cặp giờ thi
    #             for course in courses_with_multiple_shifts['Mã học phần mở rộng'].unique():
    #                 if course not in assigned_courses:
    #                     # Đảm bảo danh sách cặp giờ thi luôn có sẵn
    #                     for pair in time_pairs:
    #                         if tuple(pair) not in used_pairs:
    #                             assigned_courses[course] = pair
    #                             used_pairs.add(tuple(pair))
    #                             break

    #                 # Gán cặp giờ thi cho các ca thi của học phần
    #                 course_rows = courses_with_multiple_shifts[courses_with_multiple_shifts['Mã học phần mở rộng'] == course]
    #                 shifts = course_rows['Ca thi'].unique()

    #                 for idx, shift in enumerate(shifts):
    #                     time_slot = assigned_courses[course][idx % len(assigned_courses[course])]
    #                     df_phanphongthi.loc[course_rows[course_rows['Ca thi'] == shift].index, 'Giờ thi'] = time_slot

    # # Kiểm tra các học phần có sinh viên thi hơn 2 ca trong một ngày
    #     def adjust_student_shifts(df, count_day):
    #         students_excess = df.groupby(['MSV mở rộng', 'Ngày thi']).size().reset_index(name='count')
    #         students_excess = students_excess[students_excess['count'] > 2]

    #         for index, row in students_excess.iterrows():
    #             student = row['MSV mở rộng']
    #             day = row['Ngày thi']
    #             shifts_today = df[(df['MSV mở rộng'] == student) & (df['Ngày thi'] == day)]

    #             if len(shifts_today) > 2:
    #                 available_days = [d for d in count_day if d != day]
    #                 found_new_day = False

    #                 for new_day in available_days:
    #                     student_rows = df[(df['Ngày thi'] == new_day) & (df['MSV mở rộng'] == student)]
    #                     if student_rows.groupby('MSV mở rộng').size().le(2).all():
    #                         shift_to_move = shifts_today.iloc[2]
    #                         df.at[shift_to_move.name, 'Ngày thi'] = new_day
    #                         found_new_day = True
    #                         break

    #                 if not found_new_day:
    #                     raise ValueError(f"Không tìm thấy ngày thi mới cho sinh viên {student}.")

    #         return df

    #     df_phanphongthi = adjust_student_shifts(df_phanphongthi, count_day)
        df_phanphongthi['Ngày thi'] = pd.to_datetime(df_phanphongthi['Ngày thi'], format='%d/%m/%Y')
        df_phanphongthi['Ngày thi'] = df_phanphongthi['Ngày thi'].dt.strftime("%d/%m/%Y")

        return df_phanphongthi
    
    
        
    def show_result_phan_ca_thi(self):
        self.df_phancathi = self.assign_exam_schedule(self.df_cbdl,self.max_shifts, self.max_rooms, self.students_per_room)
        # self.df_phancathi = self.assign_exam_schedule(self.df_cbdl)
        # self.check_exam_schedule(self.df_cbdl, self.max_shifts)
        self.df_phancathi = self.assign_rooms(self.df_phancathi, self.df_dspt, self.students_per_room)
        self.df_phancathi = self.assign_calendar(self.df_phancathi, self.df_dsnt, self.shift_per_day)
        
        # self.df_phancathi = self.check_and_adjust_day(self.df_phancathi, self.df_dsnt, self.shift_per_day)
        self.df_phancathi.to_excel('e:\dulieuoc\Downloads\output_with_ca.xlsx', index=False)






    # def assign_rooms(self, df_cbdl, df_dsphongthi, students_per_room):
    #     df_cbdl['Mã phòng'] = ""
    #     count_shifts = sorted(df_cbdl['Ca thi'].unique())
    #     count_rooms = df_dsphongthi['Mã phòng'].unique()
    #     assigned_rooms_per_shift = {shift: set() for shift in count_shifts}

    #     for shift in count_shifts:
    #         course_counts = df_cbdl[df_cbdl['Ca thi'] == shift].groupby('Mã học phần mở rộng')['MSV'].count()
    #         sorted_courses = course_counts.sort_values(ascending=False).index.tolist()
    #         for course in sorted_courses:
    #             no_students = len(df_cbdl[(df_cbdl['Mã học phần mở rộng'] == course) & (df_cbdl['Ca thi'] == shift)])
    #             rooms_needed = math.ceil(no_students / students_per_room)
    #             students_per_room_now = math.ceil(no_students / rooms_needed)
    #             assigned_rooms = 0
    #             for room in count_rooms:
    #                 if room not in assigned_rooms_per_shift[shift]:
    #                     available_students = df_cbdl[(df_cbdl['Mã học phần mở rộng'] == course) & (df_cbdl['Ca thi'] == shift) & (df_cbdl['Mã phòng'] == '')]
    #                     available_student_count = len(available_students)
    #                     if available_student_count > 0:
    #                         df_cbdl.loc[available_students.index[:students_per_room_now], 'Mã phòng'] = room
    #                         assigned_rooms_per_shift[shift].add(room)
    #                         assigned_rooms += 1
    #                     if assigned_rooms == rooms_needed:
    #                         break
    #     return df_cbdl

    # def assign_calender(self, df_cbdl, df_dsngaythi, shift_per_day):
    #     df_cbdl['Ngày thi'] = ""
    #     count_shifts = sorted(df_cbdl['Ca thi'].dropna().unique())
    #     count_shifts_len = len(count_shifts)
    #     count_day = df_dsngaythi['Ngày thi'].unique()
    #     count_time = df_dsngaythi['Giờ thi'].unique().tolist()
    #     day_needed = math.ceil(count_shifts_len / shift_per_day)

    #     shifts_per_day = []
    #     for i in range(day_needed):
    #         shifts_per_day.append(count_shifts[i * shift_per_day : (i + 1) * shift_per_day])
    #     assigned_day = 0
    #     for day in count_day:
    #         if assigned_day == day_needed:
    #             break
    #         for shift in shifts_per_day[assigned_day]:
    #             available_shifts = df_cbdl[(df_cbdl['Ca thi'] == shift) & (df_cbdl['Ngày thi'] == '')]
    #             df_cbdl.loc[available_shifts.index, 'Ngày thi'] = day
    #             df_cbdl.loc[available_shifts.index, 'Giờ thi'] = count_time[(int(shift) - 1) % shift_per_day]
    #         assigned_day += 1

    #     df_cbdl['Ngày thi'] = pd.to_datetime(df_cbdl['Ngày thi'])
    #     df_cbdl['Ngày thi'] = df_cbdl['Ngày thi'].dt.strftime("%d/%m/%Y")
    #     return df_cbdl
    
    def load_data(self):
        self.df_cbdl = pd.read_excel('e:\dulieuoc\Downloads\OutputCBDL.xlsx')
        self.df_dspt = pd.read_excel('e:\dulieuoc\Downloads\Dữ liệu phòng thi.xlsx')
        self.df_dsnt = pd.read_excel('e:\dulieuoc\Downloads\Dữ liệu ngày thi.xlsx')

    def run_processing(self):
        self.load_data()
        self.show_result_phan_ca_thi()
        # self.df_cbdl = self.assign_rooms(self.df_cbdl, self.df_dsphongthi, self.students_per_room)  
        # self.df_cbdl.to_excel('e:\dulieuoc\Downloads\output_with_ca_and_rooms.xlsx', index=False)  
# if __name__ == "__main__":
#     app = QApplication(sys.argv)  # Khởi tạo QApplication
#     widget = ToiUu()  # Tạo đối tượng ToiUu (QWidget)
#     widget.run_processing()  # Chạy xử lý dữ liệu
#     sys.exit(app.exec_()) 
if __name__ == "__main__":
    # scheduler = ToiUu()

    # # # Đọc từ file Excel
    # scheduler.df_cbdl = pd.read_excel('e:\dulieuoc\Downloads\OutputCBDL.xlsx')
    # scheduler.df_dspt = pd.read_excel('e:\dulieuoc\Downloads\Dữ liệu phòng thi.xlsx')
    # scheduler.df_dsnt = pd.read_excel('e:\dulieuoc\Downloads\Dữ liệu ngày thi.xlsx')
    

    # # Thực hiện lập lịch thi
    # scheduler.df_phancathi = scheduler.assign_exam_schedule(scheduler.df_phancathi, scheduler.max_shifts, scheduler.max_rooms, scheduler.students_per_room)
    # print("\nAfter assign_exam_schedule:")
    # print(scheduler.df_phancathi.head())
    # scheduler.df_phancathi = scheduler.assign_rooms(scheduler.df_phancathi, scheduler.df_dspt, scheduler.students_per_room)
    # print("\nAfter assign_rooms:")
    # print(scheduler.df_phancathi.head())
    # scheduler.df_phancathi = scheduler.assign_calender(scheduler.df_phancathi, scheduler.df_dsnt, scheduler.max_shift_per_day)
    # print("\nAfter assign_calender:")
    # print(scheduler.df_phancathi.head())
    # # Ghi kết quả vào file Excel
    # scheduler.df_phancathi.to_excel('e:\dulieuoc\Downloads\output.xlsx', index=False)
    # print(scheduler.df_cbdl.head())
    # # Thực hiện lập lịch thi và lưu kết quả vào file Excel sau mỗi bước
    # scheduler.df_phancathi = scheduler.assign_exam_schedule(scheduler.df_cbdl, scheduler.max_shifts, scheduler.max_rooms, scheduler.students_per_room)
    # scheduler.df_phancathi.to_excel('e:\dulieuoc\Downloads\output_with_ca.xlsx', index=False)  # Lưu file với cột Ca thi
    # print(scheduler.df_phancathi.head())
    # # Đọc file đã có cột Ca thi để tiếp tục gán phòng
    # scheduler.df_phancathi = pd.read_excel('e:\dulieuoc\Downloads\output_with_ca.xlsx')
    # scheduler.df_phancathi = scheduler.assign_rooms(scheduler.df_phancathi, scheduler.df_dspt, scheduler.students_per_room)
    # scheduler.df_phancathi.to_excel('e:\dulieuoc\Downloads\output_with_rooms.xlsx', index=False)  # Lưu file với cột Mã phòng

    # # Đọc file đã có cột Mã phòng để tiếp tục gán ngày thi và giờ thi
    # scheduler.df_phancathi = pd.read_excel('e:\dulieuoc\Downloads\output_with_rooms.xlsx')
    # scheduler.df_phancathi = scheduler.assign_calender(scheduler.df_phancathi, scheduler.df_dsnt, scheduler.max_shift_per_day)
    # scheduler.df_phancathi.to_excel('e:\dulieuoc\Downloads\output_final.xlsx', index=False)  # Lưu file cuối cùng với cột Ngày thi và Giờ thi
    widget = ToiUu()  # Tạo đối tượng ToiUu (QWidget)
    widget.run_processing()