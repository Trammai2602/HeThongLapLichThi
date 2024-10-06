from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox,QApplication
import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
import math
import numpy as np

class ToiUu():
    

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

        df_phanphongthi['Ngày thi'] = pd.to_datetime(df_phanphongthi['Ngày thi'], format='%d/%m/%Y')
        df_phanphongthi['Ngày thi'] = df_phanphongthi['Ngày thi'].dt.strftime("%d/%m/%Y")

        return df_phanphongthi
    
    
        
    def show_result_phan_ca_thi(self):
        self.df_phancathi = self.assign_exam_schedule(self.df_cbdl,self.max_shifts, self.max_rooms, self.students_per_room)
        self.df_phancathi = self.assign_rooms(self.df_phancathi, self.df_dspt, self.students_per_room)
        self.df_phancathi = self.assign_calendar(self.df_phancathi, self.df_dsnt, self.shift_per_day)
        self.df_phancathi.to_excel('e:\dulieuoc\Downloads\output_with_ca.xlsx', index=False)

    def load_data(self):
        self.df_cbdl = pd.read_excel('e:\dulieuoc\Downloads\OutputCBDL.xlsx')
        self.df_dspt = pd.read_excel('e:\dulieuoc\Downloads\Dữ liệu phòng thi.xlsx')
        self.df_dsnt = pd.read_excel('e:\dulieuoc\Downloads\Dữ liệu ngày thi.xlsx')

    def run_processing(self):
        self.load_data()
        self.show_result_phan_ca_thi()

if __name__ == "__main__":
    widget = ToiUu()  # Tạo đối tượng ToiUu (QWidget)
    widget.run_processing()