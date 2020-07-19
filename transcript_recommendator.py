from tkinter import *
from tkinter import ttk,filedialog
from recommendations import *
import PyPDF2,os,dbm,pickle,xlrd


class GUI(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent=parent
        self.grid()
        self.initializeGUI()
        self.no_database=True
        if "my_files_directions.db.dir" in os.listdir():
            with dbm.open("my_files_directions.db","c") as database:
                if len(database) != 0:
                    self.no_database=False
                    self.bool_var.set(True)
                    self.grades_file=pickle.loads(database['GRADES'])
                    self.excel_file=pickle.loads(database['DATASET'])
                    self.transcript_file=pickle.loads(database['TRANSCRIPT'])
                    self.load_grades_dataset()
                    self.load_excell_dataset()
                    self.read_transcript_file()
                    self.upload_letter.configure(bg="green")
                    self.upload_past.configure(bg="green")
                    self.upload_trans.configure(bg="green")
    def initializeGUI(self):
        """
        Labels:
            BIG_TEXT - SMART ADVISOR TEXT
            subject_label - Subject LabeL
            rec_text - Recommendation Filters Text
            estimated_label - Estimated Grades Label
            error_message - Error Message Label
            courses_label - Courses and Estimated Grades Label
            current_gpa_label - Current GPA Label
            new_gpa_label - New GPA label
            current_gpa_load - Percentage of changing gpa label
            select_some_label - Select some courses to see change label
            percentage_gpa - Show Percentage of Changing GPA
        
        Buttons:
            upload_letter - uploading letter form askfileopen
            upload_past - uploading past grades form askfileopen
            upload_trans - uploading transcript from askfileopen
            get_rec_button - Getting recommendation button

        BoolenVar:
            bool_var - To check remember_me

        CheckButton:
            remember_me - to check remember_me clicked

        Listboxes:
            coursses_listbox - Show Selected Courses and grades in listbox
            subject_listbox - All Lessons listing..

        """        
        self.estimated_list=[]

        self.BIG_TEXT=Label(self,text="Smart Advisor - Your Intelligent Agent",bg="blue",fg="white",font=("Helvetica",14,"bold"),anchor=CENTER)
        self.BIG_TEXT.grid(row=0,column=0,sticky=E+W+S+N,columnspan=3)

        self.upload_letter=Button(self,text="Upload Letter Grade Data",command=self.load_grades_dataset,bg="red")
        self.upload_letter.grid(row=1,column=0,sticky=E+W+S+N,padx=10,pady=10)

        self.upload_past=Button(self,text="Upload Past Course Data",command=self.load_excell_dataset,bg="red")
        self.upload_past.grid(row=1,column=1,sticky=E+W+S+N,pady=10)


        self.upload_trans=Button(self,text="Upload Transcript",command=self.read_transcript_file,bg="red")
        self.upload_trans.grid(row=1,column=2,sticky=E+W+S+N,padx=10,pady=10)

        self.recomend_filters_frame=Frame(self,borderwidth=3,relief=GROOVE)
        self.recomend_filters_frame.grid(row=2,column=1,sticky=E+W+S+N,pady=10)

        self.rec_text=Label(self.recomend_filters_frame,text="Recommendation Filters:",anchor=CENTER,font=("Helvatica",10,"bold"))
        self.rec_text.grid(row=0,column=0,sticky=E+W+S+N,columnspan=3,pady=5)

        self.subject_label=Label(self.recomend_filters_frame,text="Subject",anchor=CENTER)
        self.subject_label.grid(row=1,column=0,sticky=S)


        self.subject_listbox=Listbox(self.recomend_filters_frame,selectmode='multiple',width=20) # scroolbars olacak bu
        self.subject_listbox.grid(row=2,column=0,padx=20)
        self.subject_listbox.bind("<<ListboxSelect>>",self.listbox_capture_bind)
        
        self.scrool=Scrollbar(self.recomend_filters_frame)
        self.scrool.grid(row=2,column=0,sticky=E,ipady=55,padx=20)
        self.subject_listbox.configure(yscrollcommand=self.scrool.set)
        self.scrool.config(command=self.subject_listbox.yview)


        self.estimated_label=Label(self.recomend_filters_frame,text="\nEstimated\n grade should\n be at least",anchor=CENTER)
        self.estimated_label.grid(row=1,column=1,padx=20)

        self.estimated_combobox=ttk.Combobox(self.recomend_filters_frame,values=self.estimated_list,width=4)
        self.estimated_combobox.grid(row=1,column=2,padx=10)
        self.estimated_combobox.bind("<<ComboboxSelected>>",self.estimated_capture)

        self.get_rec_button=Button(self.recomend_filters_frame,text="Get Recommendations")
        self.get_rec_button.grid(row=2,column=1,columnspan=2,padx=50)
        self.get_rec_button.bind("<Button-1>",self.capture_get_recommendation)

        self.bool_var=BooleanVar()
        self.bool_var.set(False)
        self.remember_me=Checkbutton(self.recomend_filters_frame,text="Remember My Data",variable=self.bool_var,command=self.remember_me_)
        self.remember_me.grid(row=3,column=1,ipadx=50)
        
        self.error_messsage=Label(self.recomend_filters_frame,text="",anchor=CENTER)
        self.error_messsage.grid(row=4,column=1,pady=10,columnspan=2)

        self.show_GPA_Frame=Frame(self,borderwidth=3,relief=GROOVE)
        self.show_GPA_Frame.grid(row=5,column=1,sticky=E+W+S+N,pady=10)

        self.courses_label=Label(self.show_GPA_Frame,text="Courses & Est.Grades",anchor=CENTER)
        self.courses_label.grid(row=0,column=0,padx=20,sticky=E+W+S+N)

        self.current_gpa_label=Label(self.show_GPA_Frame,text="Current GPA")
        self.current_gpa_label.grid(row=0,column=1,padx=70)

        self.new_gpa_label=Label(self.show_GPA_Frame,text="New GPA")
        self.new_gpa_label.grid(row=0,column=2)

        self.courses_listbox=Listbox(self.show_GPA_Frame,selectmode=MULTIPLE) # scroolbox olcak
        self.courses_listbox.grid(row=1,column=0,pady=10,rowspan=2)
        self.scrool_courses=Scrollbar(self.show_GPA_Frame)
        self.scrool_courses.grid(row=1,column=0,sticky=E,rowspan=2,ipady=55)
        self.courses_listbox.configure(yscrollcommand=self.scrool_courses.set)
        self.scrool_courses.config(command=self.courses_listbox.yview)
        self.courses_listbox.bind("<<ListboxSelect>>",self.courses_selected)

        self.current_gpa_load=Label(self.show_GPA_Frame,text="",font=("Helvatica",10,"bold"))
        self.current_gpa_load.grid(row=1,column=1,padx=20)
        
        self.new_gpa_load=Label(self.show_GPA_Frame,text="",font=("Helvatica",10,"bold"))
        self.new_gpa_load.grid(row=1,column=2)

        self.select_some_label=Label(self.show_GPA_Frame,text="Select some\n courses to see\n the changes in \n your GPA!")
        self.select_some_label.grid(row=2,column=1)

        self.percentage_gpa=Label(self.show_GPA_Frame,text="0.00%")
        self.percentage_gpa.grid(row=2,column=2)
        self.selected_list=[]

    def remember_me_(self):
        """
        Notes:
            If the user clicked Checkbox , It will return True it means that
            Python will understand data's locations when restart the program.
        """        
        if self.bool_var.get():
            try:
                database=dbm.open("my_files_directionsss.db","c")
                database['GRADES']=pickle.dumps(self.grades_file)
                database['DATASET']=pickle.dumps(self.excel_file)
                database['TRANSCRIPT']=pickle.dumps(self.transcript_file)
                self.error_messsage.configure(text="Your Data Location will be Remembered",bg="blue")
                self.original_settings_label(self.error_messsage)
            except:
                self.error_messsage.configure(text="Select Data Location First!",bg="Yellow")
                self.original_settings_label(self.error_messsage)
                self.original_settings_label(self.bool_var,label_check=False)
        else:
            print("Your Data Location will be Remembered")
            database=dbm.open("my_files_directionsss.db","c")
            if len(database) != 0:
                print("Data Locations will be forget")
                get_keys=[a for a in database]
                for a in get_keys:
                    del database[a]
            database.close()
    def open_file(self,txt=False,xlsx=False,pdf=False):
        """
        
        Keyword Arguments:
            txt {bool} -- if the txt True python show only txt files (default: {False})
            xlsx {bool} -- if the xlsx True python show only xlsx files (default: {False})
            pdf {bool} -- if the pdf True python show only pdf files (default: {False})
        
        Returns:
            [str] -- file direction .
        """        
        get_current_directory=str(os.getcwd())
        if pdf:
            get_file=str(filedialog.askopenfilename(initialdir=get_current_directory,filetypes=(("pdf files","*.pdf"),("all files","*.*"))))
        elif txt:
            get_file=str(filedialog.askopenfilename(initialdir=get_current_directory,filetypes=(("txt files","*.txt"),("all files","*.*"))))
        elif xlsx:
            get_file=str(filedialog.askopenfilename(initialdir=get_current_directory,filetypes=(("xlsx files","*.xlsx"),("all files","*.*"))))
        return get_file
    def load_grades_dataset(self):
        """
            Notes:
                self.letter_dictionary = key = A+,B.. value:4.0 etc
                That means corressponding numerical value of letter grades.
        """
        if self.no_database:
            self.grades_file=self.open_file(txt=True)
        self.course_gr_data=CourseGradeData()
        self.course_gr_data.load_letters(self.grades_file)
        self.letter_dictionary=self.course_gr_data.letter_dictionary
        for key in self.letter_dictionary:
            self.estimated_list.append(key)
        self.estimated_combobox.configure(values=self.estimated_list)
        self.estimated_combobox.current(1)
        self.upload_letter.configure(bg="green")
    def load_excell_dataset(self):
        """
        Notes:
            self.all_lesson - [list] - include all_information with tuples (LESSON,LESSON_CODE,CREDIT,LETTER_GRADE)
            self.subject - [list] - include only subject name not OBJECT!
            self.object_course - [ list ] - include all lessons with an object!

        """
        if self.no_database:
            self.excel_file=self.open_file(xlsx=True)
        self.xlsx=xlrd.open_workbook(self.excel_file)
        self.xlsx_online=self.xlsx.sheet_by_index(0)
        column=0
        self.all_lesson=[] #[(UNI,111,4,F)]
        self.subject=[]
        for row in range(1,self.xlsx_online.nrows):
            course_name=self.xlsx_online.cell_value(row,column).split() #0.index lesson , #1.index leseon kod.
            course=course_name[0]
            course_code=course_name[1]
            grade=self.xlsx_online.cell_value(row,column+1)
            student_number=self.xlsx_online.cell_value(row,column+2)
            course_credit=self.xlsx_online.cell_value(row,column+3)
            self.all_lesson.append((course,course_code,course_credit,grade))
            if course not in self.subject:
                self.subject.append(course)
        self.subject.sort()
        self.all_lesson.sort()
        self.object_course=[]

        for course,course_code,course_credit,grade in self.all_lesson:
            obj=Course(course,course_code,course_credit,grade)
            self.object_course.append(obj)

        for a in self.subject:
            self.subject_listbox.insert(END,a)
    
        self.upload_past.configure(bg="green")
        self.other_students()

    def other_students(self):
        """
        Notes:
            In that part we are collecting all the students from excell file and
            Creating their OBJECT!.
        """        
        self.student_dictionary={} #prefs # {id : {course:number_grade}}
        my_list=[]
        column=0
        for row in range(1,self.xlsx_online.nrows):
            student_id=int(self.xlsx_online.cell_value(row,column+2))
            student_course_name_code=self.xlsx_online.cell_value(row,column).split()
            course_name=student_course_name_code[0]
            course_id=student_course_name_code[1]
            student_letter_grade=self.xlsx_online.cell_value(row,column+1)
            student_letter_grade=self.letter_dictionary[student_letter_grade]
            my_list.append((student_id,course_name+" "+course_id,student_letter_grade))


        for student_id,course,letter in my_list:
            self.student_dictionary.setdefault(student_id,{})
            self.student_dictionary[student_id][course]=letter
        
        for student_id,courses in self.student_dictionary.items():
            create_student=Student(student_id)
            create_student.taken_courses=courses


    def original_settings_label(self,label,label_check=True):
        if label_check:
            self.after(1500,lambda:label.configure(text="",bg="SystemButtonFace"))
        else:
            self.after(1500,lambda:label.set(False))
    def listbox_capture_bind(self,event):
        """
        Notes:
            If the clicked in any lesson in listbox:
            Python will transfer all the courses in selected_list list.
        """        
        self.capture_event=event.widget
        self.x=self.capture_event.curselection()
        self.selected_list=[self.subject_listbox.get(a) for a in self.x]
    def courses_selected(self,event):
        """
        Notes:
            When clicked recommended courses
            Python check this courses object credit and letter grades
            transfer into calculate_gpa function to calculation.
        """        
        course_selected=event.widget
        self.selected_course=course_selected.curselection()
        self.selected_c_list=[self.courses_listbox.get(a) for a in self.selected_course]
        self.selected_obj=[]
        if len(self.selected_c_list) != 0:
            for key,get_obj in self.test_dictionary.items():
                obj=get_obj['Object']
                for get_name in self.selected_c_list:
                    if get_name == obj.__str__():
                        self.selected_obj.append(obj)
            self.calculate_gpa()
        
    def calculate_gpa(self):
        """
        Notes:
            In that part python will do math part.
            Sum all the credit and calculation  to New GPA
            and redirect to get_percentage function to see
            change in GPA percentage.
        """        
        sum_obj_credit=0
        self.credit_multiply_with_letters=self.old_cr_letters['Get_Old']
        for obj in self.selected_obj:
            sum_obj_credit+=obj.course_credit
            self.credit_multiply_with_letters+=obj.course_credit*self.letter_dictionary[obj.letter_grade]
        total_cr=sum_obj_credit+self.total_credit
        self.new_gpa=(self.credit_multiply_with_letters/total_cr)
        self.new_gpa_load.configure(text=str(self.new_gpa)[0:4])
        self.percentage=((self.new_gpa/self.gpa)-1)*100
        self.get_percentage()
    def get_percentage(self):
        """
        Notes:
            if the new gpa > old gpa:
                label will be green and positive.
            else: red and - sign.
        """        
        if self.new_gpa >= self.gpa:
            self.percentage_gpa.configure(text=(f'+{str(self.percentage)[0:4]}%'),bg="green")
        else:
            self.percentage_gpa.configure(text=(f'{str(self.percentage)[0:6]}%'),bg="red")
    def capture_get_recommendation(self,event):
        """
        Notes:
            Getting Recommendation from the recommendation file.
            if the conditions True which is subject HAVE TO selected.
        """        
        clicked_button=event.widget
        self.get_lesson=[]
        if len(self.selected_list) != 0 :
            clicked_button.configure(bg="green")
            recommended=getRecommendations(self.student_dictionary,self.std_id,similarity=sim_distance)
            print(f'Selected = {self.selected_list}')
            for grade,course in recommended:
                course_splitted=course.split()
                course_name=course_splitted[0]
                for lessons in self.selected_list:
                    if lessons == course_name:
                        self.get_lesson.append((grade,course))
            print(f'Similarity List = {self.get_lesson}')
            self.courses_listbox.delete(0,END)
            self.find_lesson_object()
        else:
            self.error_messsage.configure(text="You Should Select Subject First!.",bg="red")
            self.original_settings_label(self.error_messsage)

    def read_transcript_file(self):
        """
        Notes:
            In that part python just reading the transcript file and trying to identify which courses student taking
            with their credit,letter grades.
        """        
        self.std_id=1234566789
        if self.no_database:
            self.transcript_file=self.open_file(pdf=True)
        read=PyPDF2.PdfFileReader(self.transcript_file)
        get_page=read.getPage(0)
        text=get_page.extractText()
        text=text.strip().split()
        # print(text)
        my_string='TitleCreditECTSGrade'
        end_string="Cr.CmECTSCr."
        not_include="TitleCreditECTSGrade-Cr.CmECTSCr."
        self.c_list=CreateListClass()
        for a in range(len(text)):
            if "Grade" in text[a]:
                if text[a] != not_include:
                    c_name=text[a][len(my_string):]
                    c_code=text[a+1][0:3]
                    while True:
                        try:
                            c_credit=int(text[a])
                        except :
                            a+=1
                        else:
                            new_variable=a+1
                            name=1
                            code=0
                            credit=0
                            if text[a+1][4:6] in self.letter_dictionary:
                                get_letter=text[a+1][4:6]
                            elif text[a+1][4:5] in self.letter_dictionary:
                                get_letter=text[a+1][4:5]
                            self.c_list.add_values(c_name,c_code,c_credit,get_letter)
                            break
                    for b in range(new_variable,len(text)):
                        if end_string in text[b]:
                            break
                        elif name==1:
                            if text[b][4:6] in self.letter_dictionary:
                                new_name=text[b][6:]
                            elif text[b][4:5] in self.letter_dictionary:
                                new_name=text[b][5:]
                            name=0
                            code=1
                            self.c_list.append(new_name)
                        elif code == 1:
                            new_code=text[b][0:3]
                            code=0
                            credit=1
                            self.c_list.append(new_code)
                        elif credit == 1:
                            try:
                                new_credit=int(text[b])
                            except :
                                continue
                            else:
                                credit=0
                                name=1
                                if text[b+1][4:6] in self.letter_dictionary:
                                    letter=text[b+1][4:6]
                                elif text[b+1][4:5] in self.letter_dictionary:
                                    letter=text[b+1][4:5]
                                self.c_list.add_values(new_credit,letter)
                    break
        for a in range(len(text)):
            if "Cumulative" in text[a]:
                if float(text[a][0:4]) != 0.00:
                    self.gpa=float(text[a][0:4])
                    self.current_gpa_load.configure(text=str(self.gpa))
                    break
        self.upload_trans.configure(bg="green")
        self.create_student_lessons()
    def create_student_lessons(self):
        """
        Notes:
            Adding current studen't taken courses to prefs dictioary which is self.students_dictionary.
        """        
        self.st_dct={}
        idx=0
        self.total_credit=0
        self.credit_multiply_with_letters=0
        while idx < len(self.c_list):
            try:
                c_name=self.c_list[idx]
                c_code=self.c_list[idx+1]
                letter_grade=self.c_list[idx+3]
                letter_grade=self.letter_dictionary[letter_grade]
            except:
                break
            else:
                if c_name == "PHYS":
                    if self.c_list[idx+2] == 1:
                        c_code=(f'{self.c_list[idx+1]}L')
                self.st_dct[c_name+" "+c_code]=letter_grade
                self.total_credit+=self.c_list[idx+2]
                self.credit_multiply_with_letters+=letter_grade*self.c_list[idx+2]
                idx+=4
        # print(self.st_dct)
        self.student_dictionary[self.std_id]=self.st_dct
        print(self.student_dictionary)
        # print(f'\nTranscript lessons = {self.st_dct}')
        # print(f'Letters dict = {self.letter_dictionary}')
        # print(f' Total credit = {self.total_credit}')
        # print(f' GPA : {self.gpa}')
        self.old_cr_letters={}
        self.old_cr_letters['Get_Old']=self.credit_multiply_with_letters

    def find_lesson_object(self):
        """
            Notes:
            self.test_dictionary - {dict} - storage get recommended lessons object.
                                            Ex - { UNI 117 :  {'Object': UNI117_Object } }
        """
        self.test_dictionary={}
        self.obj_l=[]
        for search in self.object_course:
            for similarity,course in self.get_lesson:
                course_splitted=course.split()
                course_name=course_splitted[0]
                course_code=course_splitted[1]
                if search.course_name == course_name and search.course_code == course_code:
                    get_letter_from_similarity=self.get_lessons_from_sim(similarity)
                    if get_letter_from_similarity == self.letter_dictionary[search.letter_grade]:
                        if self.letter_dictionary[search.letter_grade] >= self.letter_dictionary[self.estimated_combobox.get()]:
                            self.test_dictionary.setdefault(course_name+" "+course_code,{})
                            self.test_dictionary[course_name+" "+course_code]['Object']=search

        for key,value in self.test_dictionary.items():
            get_obj=value['Object']
            self.courses_listbox.insert(END,get_obj)

    def get_lessons_from_sim(self,between_numbers):
        """
        
        Arguments:
            between_numbers {float} -- between_numbers coming from recommendation similarity scores.
        
        Returns:
            {float} -- example -> if the between numbers 1.0 <between_numbers<1.29 python identify automatically
            it's letter D but its convert from the self.letter_dictionary to 1.0 !
        """        
        between_numbers=float(between_numbers)
        scores_list=[(4.1,4.1,'A+'),(4.0,4.09,'A'),(3.7,3.99,'A-'),(3.3,3.69,'B+'),
                     (3.0,3.29,'B'),(2.7,2.99,'B-'),(2.3,2.69,'C+'),(2.0,2.29,'C'),
                     (1.7,1.99,'C-'),(1.3,1.69,'D+'),(1.0,1.29,'D'),(0.5,0.99,'D-'),
                     (0.0,0.00,'F')]
        for lower,upper,letter_grade in scores_list:
            if lower <= between_numbers <= upper:
                return self.letter_dictionary[letter_grade]

    def estimated_capture(self,event):
        self.combobox_event=event.widget
        self.estimated_selected=self.combobox_event.get()

class CreateListClass(list):
    """
    Arguments:
        list [list] -- when sets up a variable its automatically turns into a list.

    Notes:
        This List can have an method for ex "add_values" method.
    """    
    def add_values(self,*values):
        """
        Arguments:
            *values (tuples) - if we don't want to deal with .append(arg) .append(arg2) we can use this method.
            It provide us to prevent code repetition. EX: my_list=CreateListClass()
                                                           my_list.append("Hello")
                                                           my_list.append("World")
                                                           my_list >>>["Hello","World"]
                                                      Thanks to this method we can just only
                                                      my_list.add_values("Hello","World")
                                                      my_list >>>["Hello","World"] as you can see same content.
        """        
        for value in values: self.append(value)

class CourseGradeData:
    dataset_students_object={}
    def __init__(self):
        """
            Notes:
                dataset_students_object - {dict} - key(student id) : value(student object)
                    when the student object created it will append automatically to dataset_students_object dictionary.
                
                self.letter_dictionary - {dict} -  When the CourseGradeData will created user should call
                    self.load_letters with a given file_name . File_name will come from the filedialog.
        """
        self.letter_dictionary={}
    def load_letters(self,file_name):
        with open(file_name,"r") as grades:
            collect=[a.strip() for a in grades]
            dictionary={a[:2].strip():a[2:].strip() for a in collect}
            self.letter_dictionary={key:float(value) for key,value in dictionary.items()}


class Course:
    def __init__(self,course_name,course_code,course_credit,letter_grade):
        """
        
        Arguments:
            course_name {str} -- course name ex- UNI 
            course_code {str} -- course code ex- 111
            course_credit {int} -- couse credit - 3
            letter_grade {str} -- letter grade - A+
        """        
        self.course_name=course_name
        self.course_code=course_code
        self.course_credit=course_credit
        self.letter_grade=letter_grade

    def __str__(self):
        return (f'{self.course_name} {self.course_code} - {self.letter_grade}')



class Student:    
    def __init__(self,student_id,gpa=None):
        """
        
        Arguments:
            student_id {integer} -- students id from dataset and parsed pdf file.
        
        Keyword Arguments:
            gpa {int-None} -- when the parsed pdf file readed gpa willnot default value. (default: {None})
        """        
        self.student_id=student_id
        self.gpa=gpa
        self.taken_courses={}
        CourseGradeData.dataset_students_object[self.student_id]=self

    def __repr__(self):
        return self.student_id

if __name__ == "__main__":
    root=Tk()
    system=GUI(root)
    root.mainloop()