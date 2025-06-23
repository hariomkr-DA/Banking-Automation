from tkinter import Tk,Label,Frame,Image,ttk,Entry,Button,messagebox,filedialog,LabelFrame,RIDGE,W,END,Text,StringVar,Toplevel

from PIL import Image,ImageTk
import time
import random
import os
import shutil
from datetime import datetime
import smtplib
import sqlite3
import requests
import re
import threading
import mail_messages
import project_table

aadhaar_pattern=re.compile( r'^\d{12}$')
pan_pattern = re.compile(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$')

email_pattern=re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
mob_pattern=re.compile(r"^[6-9]\d{9}$")


bal_pattern = re.compile(r"^(?!0+(?:\.0{1,2})?$)\d{1,3}(,\d{3})*(\.\d{1,2})?$|^(?!0+(?:\.0{1,2})?$)\d+(\.\d{1,2})?$")

bg_root="powder blue"
entry_relx=.440
lbl_relx=.350


project_table.create_db_and_table()
class Bank:
    # ===========================constructor====================
    def __init__(self,win):
        
        self.win=win
        # ===========title root window============
        self.win.title("ABC Bank")
        
        # =======this is defined for right and left logo===========
        
 
        self.left_logo_lbl=Label(self.win)
        self.left_logo_lbl.place(relx=0,rely=0)
        
        
        
        
        self.right_logo_lbl1=Label(self.win)
        self.right_logo_lbl1.place(relx=.8,rely=0)


        # =======root window size ,height,color related code==========
        self.win.state("zoomed")
        self.win.resizable(width=False,height=False )
        self.win.configure(bg=bg_root)

        # ======this is Project title label and display date==========
        title_lbl=Label(self.win,text="Banking Automation",font=("arial",40,'bold','underline'),bg=bg_root)
        title_lbl.pack()
        tody_lbl=Label(self.win,text=time.strftime("%d~%B~%Y"),font=("arial",15,'bold'),bg=bg_root,fg="purple")
        tody_lbl.pack(pady=5)
        
        # self.help_win = Toplevel(self.win)  # create dummy, will be destroyed immediately
        # self.help_win.destroy()              # ensures help_win always exists as a handle
        
            
        
        self.help_btn=Button(self.win,text="Help & Support",font=("Arial",13,"bold"),bg=bg_root,width=15,command=self.help_desk)
        self.help_btn.place(relx=.86,rely=.920)
        self.help_sup=None
        
        
        
        # ====Created child window for Home screen==========
        self.frm=Frame(self.win,bd=5,relief="ridge")
        self.frm.place(relx=0,rely=.160,relheight=.75,relwidth=1)
        
        
        
        
        
        # ===========Developer Details===============
        self.develop=Label(self.win,text="Developed By:Hariom Kumar",font=("Arial",13,"bold"),bg=bg_root)
        self.develop.place(relx=.440,rely=.920)
        mail_lbl=Label(self.win,text="mail:",font=("Arial",13,"bold"),bg=bg_root)
        mail_lbl.place(relx=.440,rely=.950)
        develop_mail=Label(self.win,text="hariomkr752@gmail.com",font=("Arial",13,"bold","underline"),bg=bg_root,fg="blue")
        develop_mail.place(relx=.470,rely=.950)
        
        self.clock_label=Label(self.win,font=("Helvetica", 13,"bold"), fg="blue",bg=bg_root)
        self.clock_label.place(relx=.58,rely=.107)
        
        self.update_time()
       
        self.img_slider()
        self.main_win()
        
        
        self.name=StringVar()
        self.gender=StringVar()
        self.dob=StringVar()
        self.mob=StringVar()
        self.email=StringVar()
        self.aadhaar=StringVar()
        self.pan=StringVar()
        self.ac_type=StringVar()
        
        self.otp_timer_id=None
        # --created help window for help--
        
        

# --help desk--        
    def help_desk(self):
        if self.help_sup:
            messagebox.showwarning("Help & Support","Already Open help window!")
            return
        self.help_win=Frame(self.win,bd=5,relief="ridge")
        self.help_win.place(relx=0,rely=.160,relheight=.75,relwidth=1)
        
        help_text = """\
Welcome to the Help Desk!

• Enter your correct A/c number and Email in the field above.
• Make sure your account exists in the system.
• Contact support if you face any issues.
"""
        Label(self.help_win, text=help_text, font=("Arial", 13,'bold')).pack()
        
        Label(self.help_win,text="Enter A/c No.:",font=("Arial",13,"bold")).pack()
        acn_entry=Entry(self.help_win,font=("Arial",13,"bold"))
        acn_entry.pack()
        
        Label(self.help_win,text="Enter Email:",font=("Arial",13,"bold")).pack()
        mail_entry=Entry(self.help_win,font=("Arial",13,"bold"))
        mail_entry.pack()
        
        Label(self.help_win,text="Describe Your Problem upto 150 word:",font=("Arial",13,"bold")).pack()
        
        msg=Text(self.help_win,font=("Arial",13,"bold"),height=7,width=50)
        msg.pack()
        
        acn_entry.focus()
        acn_entry.bind("<Return>",lambda e:mail_entry.focus_set())
        mail_entry.bind("<Return>",lambda e:msg.focus_set())
        
        def submit():
            mail=mail_entry.get().strip()
            acn=acn_entry.get().strip()
            message=msg.get("1.0",END).strip()
            word_count=len(message.split())
            if acn=="" or not acn.isdigit():
                messagebox.showerror("Help & Support","Please Enter Valid A/c No.!")
                return
            elif not email_pattern.fullmatch(mail):
                messagebox.showerror("Help & Support","Enter Valid Email!")
                return
            elif message=="":
                messagebox.showerror("Help & Support","Please Write your issue!")
                return
            elif word_count>150:
                messagebox.showerror("Help & Support",f"Problem description too long! Limit is 150 words. (Current: {word_count})")
                return
            bank_db=self.connect_database()
            cursor=bank_db.cursor()
            cursor.execute("select name from user where ac_number=?",(acn,))
            result=cursor.fetchone()
            cursor.execute("insert into user_issue(ac_number,email,issue) values(?,?,?)",(acn,mail,message))
            bank_db.commit()
            bank_db.close()
            
            if result:
                name=result[0]
            else:
                name=f"Your A/c No.{acn} does not exixts Our System, But Requset Accepted!"
    
            issue_msg=mail_messages.help_msg(acn=acn,issue=message,name=name)
            
            try:
                self.send_mail(subject="Help & Support",user_mail=mail,message=issue_msg)
            except:
                pass
            messagebox.showinfo("Help & Support", "Your request has been submitted!")
            
            Label(self.help_win,text= "Your request has been submitted!",font=("Arial",15,"bold"),fg="green").place(relx=.575,rely=.8)
            acn_entry.delete(0,END)
            mail_entry.delete(0,END)
            msg.delete("1.0",END)
            acn_entry.focus_set()
            
        def destroy_help_win():
            if self.help_win.winfo_exists():
                self.help_win.destroy()
                self.help_sup=None
        submit_btn=Button(self.help_win,text="Submit",font=("Arial",13,"bold"),fg="white",bg="green",width=9,command=submit)
                
        submit_btn.pack(pady=30)
        
        close_btn=Button(self.help_win,text="Close",font=("Arial",13,"bold"),fg="white",bg="green",width=9,command=destroy_help_win)
        close_btn.pack()
        self.help_sup=True
  
# --this function to update logo in 1 sec--
    def img_slider(self):
    # Step 1: this is list of images
        if not hasattr(self, 'left_images'):
            self.left_image_paths = ["bank.jpg","hand.jpeg","tech.jpeg","mech.jpeg","mony.jpg","coin.jpeg"]
            self.right_image_paths = ["hand.jpeg","bank.jpg","mech.jpeg","tech.jpeg","coin.jpeg","mony.jpg"]

            self.left_images = [self.convert_bitmap(cwd_path=img, size=(260,110), master=self.win) for img in self.left_image_paths]
            self.right_images = [self.convert_bitmap(cwd_path=img, size=(260,110), master=self.win) for img in self.right_image_paths]
            
            self.img_index = 0

        # Step 2: this is set image on label
        self.left_logo_lbl.configure(image=self.left_images[self.img_index])
        self.right_logo_lbl1.configure(image=self.right_images[self.img_index])

        # Step 3: this set next image inedx
        self.img_index = (self.img_index + 1) % len(self.left_images)

        # Step 4: calling after 1 second
        self.win.after(1700, self.img_slider)

            
        
        
        
        
    
# --this function to countdown time waiting fro otp--
    def otp_timer(self,label_name=None,frame=None,time_in_sec=None):
        self.left_time=time_in_sec
        self.otp_expired=False
        def countdown():
            if not label_name.winfo_exists():  # <- Yeh check label ke destroy hone pe crash se bachaata hai
                return
            if self.left_time>0:
                self.send_otp_btn.config(state="disabled",bg="white",fg="black")
                minutes = self.left_time // 60
                seconds = self.left_time % 60
                label_name.configure(text=f"Time left: {minutes:02}:{seconds:02}", fg="black", width=18)
                self.left_time -= 1
                self.otp_timer_id=frame.after(1000,countdown)
            else:
                if label_name.winfo_exists():
                    label_name.configure(text="OTP expired!", fg="red")
                    self.send_otp_btn.config(state="normal",bg="green",fg="white")
                    #label_name.destroy()
                    #verify_btn.config(state="disabled")
                self.otp_expired = True
                
        if hasattr(self, 'otp_timer_id'):
            try:
                frame.after_cancel(self.otp_timer_id)
            except:
                pass  # In case it was already called or frame is gone
        countdown()
# --this function for live time on home screen ya root window--
    def update_time(self):
        current_time = time.strftime("%I:%M:%S %p")  # Format: Hour:Minute:Second
        self.clock_label.config(text=current_time)
        self.win.after(1000, self.update_time)  # Call this function again after 1000ms (1 second)

# ===this function connect to database===
    def connect_database(self):
        return sqlite3.connect(database="my_bank_database.sqlite")

# =====this function store user transaction histroy==
    def store_txt_history(self,*,amount=None,mode=None,desc=None,acn=None,ref=None):
        bank_db=self.connect_database()
        cursor=bank_db.cursor()
        randm_ref=random.randint(1000,9999)
        rndm=(random.randint(65,90))
        char=chr(rndm)
        if ref:
            ref_no=ref 
        else:
            ref_no=f"R-{str(randm_ref)+str(acn)+char}"
        try:
            cursor.execute("insert into user_txn_history(ref_no,amount,mode,desc,ac_number) values(?,?,?,?,?)",(ref_no,amount,mode,desc,acn))
            bank_db.commit()
            bank_db.close()
        except Exception as e:
            messagebox.showwarning("Transaction History",f"Error store User Transaction History\n{e}")
            return
        else:
            return ref_no
        
# ======this function check internt===
    def check_internet(self):
        try:
            requests.get("https://www.google.com")
            return True
        except requests.exceptions.ConnectionError:
            return False
# =====this function to focus cursor on next entrybox===
    def focus_next_widgets(self,event):
        event.widget.tk_focusNext().focus()
        return 'break'
        
# ===this function input 3 arg user mail,subject and message then send mail==
    def send_mail(self,*,user_mail="",subject="",message=""):
        def send():
            bank_db=self.connect_database()
            cursor=bank_db.cursor()
            cursor.execute("select email,password from mail")
            detail=cursor.fetchone()
            bank_db.close()
            if not detail:
                messagebox.showwarning("Email","Go to Admin Dasboard and Update Email or Password")
                return
            sender_mail,sender_mail_pw=detail
            try:
                with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
                    server.login(sender_mail,sender_mail_pw)
                    full_message=f"Subject:{subject}\n\n{message}\nDate:{time.strftime('%d-%m-%Y %r')}"
                    server.sendmail(sender_mail,user_mail,full_message.encode('utf-8'))
            except Exception as e:
                messagebox.showerror("Send mail",f"Failed to send mail!\n{e}")
        threading.Thread(target=send).start()
# ======this function convert image to bitmap and return bitmap image path=====
    def convert_bitmap(self,*,cwd_path="",size=(100,100),master=""):
        if not cwd_path:
            return None,messagebox.showerror("error","Path not found!")
        try:
            img=Image.open(f"Images/{cwd_path}").resize(size)
            img_bitmap=ImageTk.PhotoImage(img,master=master)
        except Exception as e:
            messagebox.showwarning("convert_bitmap fun error",f"{e}")
        else:
            return img_bitmap
            
# ==this function change icon and show/hide password==
    def hide_show_password(self):
        if not self.show_password:
            self.pw_entry.config(show="")
            self.show_hide_pw_btn.config(image=self.show_pw_icon)
            self.show_password=True
    
        else:
            self.pw_entry.config(show="*")
            self.show_hide_pw_btn.config(image=self.hide_pw_icon)
            self.show_password=False
            
# ====================this function use clear all widgets of child frame===============================
    def clear_frame_child_win(self):
        for row in self.frm.winfo_children():
            row.destroy()

# ====================main Window or Login screen====================================
    def main_win(self):
        self.clear_frame_child_win()
        
        all_lbl_bg="#0c1d26"
        all_lbl_fg="#00f7ff"
        
        bg_img=self.convert_bitmap(cwd_path="user_type.jpg",master=self.frm,size=(1280,520))
        
        bg_lbl=Label(self.frm,image=bg_img)
        bg_lbl.place(relx=0,rely=0,relheight=1,relwidth=1)
        bg_lbl.image=bg_img
        
        home_screen=Label(self.frm,text="Home Screen",font=("Arial",19,"bold"),fg=all_lbl_fg,bg=all_lbl_bg)
        home_screen.pack()
        
        
        select_lbl=Label(self.frm,text="Select Option:",font=("Arial",15,"bold"),fg=all_lbl_fg,bg=all_lbl_bg)
        select_lbl.place(relx=.300,rely=0.15)
        
        # ====this cobobox is identified user================
        self.user_type=ttk.Combobox(self.frm,state="readonly",font=("Arial",13,"bold"),width=30,values=("Admin","User"))
        #self.user_type["values"]=("Admin","User")
        #self.user_type.current(1)
        self.user_type.set("----------------Select--------------------")
        self.user_type.place(relx=entry_relx,rely=0.15)
        
        # ================input Acn Number from user===============
        acn_lbl=Label(self.frm,text="A/C No:",font=("Arial",13,"bold"),fg=all_lbl_fg,bg=all_lbl_bg)
        acn_lbl.place(relx=lbl_relx,rely=0.25)
        self.acn_entry=Entry(self.frm,font=("Arial",13,"bold"))
        self.acn_entry.place(relx=entry_relx,rely=0.25)
        # ============Default focus cursor on Account number entry box===========
        
        
        # ===========input password from user==============
        pw_lbl=Label(self.frm,text="Password:",font=("Arial",13,"bold"),pady=10,fg=all_lbl_fg,bg=all_lbl_bg)
        pw_lbl.place(relx=lbl_relx,rely=.30)
        self.pw_entry=Entry(self.frm,font=("Arial",13,"bold"),show="*",width=17)
        self.pw_entry.place(relx=entry_relx,rely=.32)
        
        # =====this show and hide password icon button==
        self.show_pw_icon=self.convert_bitmap(cwd_path="show-password.png",size=(20,20),master=self.frm)
        self.hide_pw_icon=self.convert_bitmap(cwd_path="hide password.webp",master=self.frm,size=(21,21))
        
        self.show_hide_pw_btn=Button(self.frm,bg="white",image=self.hide_pw_icon,bd=-1,command=self.hide_show_password)
        self.show_hide_pw_btn.place(relx=.567,rely=.3212)
        self.show_password=False
        
        # ---this is captcha label show 2 digit random  number--
        self.numbr=Label(self.frm,font=("Arial",13,"bold"),fg=all_lbl_fg,bg=all_lbl_bg)
        self.numbr.place(relx=.440,rely=.38)
        self.captcha()  #=========== this function Display Random number for numeric captcha
        
        
        # =====================captcha related======================
        captcha_lbl=Label(self.frm,text=f"Solve this:",font=("Arial",13,"bold"),fg=all_lbl_fg,bg=all_lbl_bg) 
        captcha_lbl.place(relx=lbl_relx,rely=.38)
        self.captcha_entry=Entry(self.frm,font=("Arial",13,"bold"),fg="green",width=5)
        self.captcha_entry.place(relx=.510,rely=.38)
       
        # =======================refresh icon  in child frame for captcha======================================================================
        
        
        self.refresh_icon=self.convert_bitmap(cwd_path="refresh icon.png",size=(20,20),master=self.frm)
        refresh_btn=Button(self.frm,image=self.refresh_icon,command=self.captcha,bd=-1,bg="white")
        refresh_btn.place(relx=.560,rely=.38)
        
        
        # =====this label frame for all beleow button ==========
        butn_frm=LabelFrame(self.frm,relief="ridge",width=560,bd=5,height=50)
        butn_frm.place(relx=.30,rely=.470)
        
        #==this variable store backgraound and foreignground  color for all main window button====
        btn_bg_color="green"
        btn_fg_color="white"
        
        # =================New account open button===================
        open_ac_btn=Button(butn_frm,text="Open Account",bd=3,font=("Arial",13,"bold")
                           ,padx=6,bg=btn_bg_color,fg=btn_fg_color,command=self.open_account_by_user)
        open_ac_btn.grid(row=0,column=0)
        
        # =================this button to recovery password================
        forgt_pw_btn=Button(butn_frm,text="forgot password",bd=3,font=("Arial",13,"bold")
                            ,command=self.forgot_pw,padx=20,bg=btn_bg_color,fg=btn_fg_color)
        forgt_pw_btn.grid(row=0,column=1)
        
        # ===============reset button to clear all entry box===========
        reset_btn=Button(butn_frm,text="reset",bd=3,font=("Arial",13,"bold"),
                         command=self.main_win,padx=10,bg=btn_bg_color,fg=btn_fg_color)
        reset_btn.grid(row=0,column=2)
        
        # =======this button to verify all details correctly===========
        login_btn=Button(butn_frm,text="Login",bd=3,font=("Arial",13,"bold")
                         ,bg=btn_bg_color,fg=btn_fg_color,command=self.login_process,padx=10)
        login_btn.grid(row=0,column=3)
        
        self.acn_entry.focus()
        self.user_type.bind("<Return>",lambda e:self.acn_entry.focus_set())
        self.acn_entry.bind("<Return>",lambda e:self.pw_entry.focus_set())
        self.pw_entry.bind("<Return>",lambda e:self.captcha_entry.focus_set())
        
   
             
# ===================this function generate random captcha ====================
    def captcha(self):
        self.rndm_number=random.randint(1,10)
        self.rndm_number2=random.randint(1,10)
        self.numbr.configure(text=f"{self.rndm_number } + { self.rndm_number2} =? ")
        
# --this function to collect ac No from user and fetch registerd mail then send otp on their mail, after verify set new password--
    def forgot_pw(self):
        self.clear_frame_child_win()   #this function clear all widgets of child frame 
        # ===========Display user top in child frame========== 
        Label(self.frm,text="Forgot Password Screen",font=("arial",18,'bold'),fg="green").pack()
        timer_lbl=Label(self.frm,text="",font=("arial",13,'bold'))
        timer_lbl.place(relx=.640,rely=.4)
        
        def send_otp(): #this function send opt on registerd email and inside nested function verify and collect password and set 
            
            acn=acn_entry.get()
            bank_db=self.connect_database()
            cursor=bank_db.cursor()
            cursor.execute("select name,email from user where ac_number=?",(acn,))
            result=cursor.fetchone()
            
            if not result:
                messagebox.showerror("Forgot Password","Account Number Does Not Exists!")
                return
           
            name,email=result
            
            wait=Label(self.frm,text="Wait sending OTP....",font=("",12,'bold'),fg="red")
            wait.place(relx=.640,rely=.3)
            self.frm.update()
            
            if not self.check_internet():
                messagebox.showerror("Forgot Password","No Internet!")
                wait.destroy()
                return
            
            
            otp=str(random.randint(1000,9999))
            acn_entry.config(state="disabled")
            
            send_msg_otp=mail_messages.send_otp(otp=otp,name=name)#---imported message from mail_messages.py
        
            try:
                self.send_mail(user_mail=email,subject="Your OTP Code for Password Reset",message=send_msg_otp)
                
            except Exception as e:
                messagebox.showerror("send otp",f"Send mail Error!\n{e}")
                
                wait.destroy()
                return
            wait.config(text="Sent Successfuly!",fg="green")
            messagebox.showinfo("Forgot Password",f"Sent OTP On {email} ")
        
            if self.otp_timer_id: #this code to verify timer function active or close
                try:
                    self.frm.after_cancel(self.otp_timer_id)
                except:
                    pass
            
            self.otp_timer(label_name=timer_lbl,frame=self.frm,time_in_sec=120)
            wait.destroy()
            
            user_otp=StringVar()
            
            otp_lbl=Label(self.frm,text="Enter OTP: ",font=("arial",13,'bold'))
            otp_lbl.place(relx=lbl_relx,rely=.4)
            otp_entry=Entry(self.frm,font=("arial",13,'bold'),textvariable=user_otp)
            otp_entry.place(relx=entry_relx,rely=.4)
            otp_entry.delete(0,END)
            otp_entry.focus()
            otp_entry.bind("<Return>",lambda e:verfiy_otp())
            self.send_otp_btn.config(text="Resend OTP")
        
            # =this function verfiy otp and collect password inside nested function set new password=
            def verfiy_otp():
                if self.otp_expired:
                    messagebox.showerror("Forgot Password","OTP Expired!")
                    return
                if user_otp.get()!=otp:
                    messagebox.showerror("Forgot Password","OTP not Match!")
                    return
                self.frm.update()
                verify_btn.destroy()
                timer_lbl.destroy()
                self.send_otp_btn.destroy()
                otp_entry.config(state="disabled")
                messagebox.showinfo("Forgot Password","OTP Verified!")
                
                if hasattr(self, 'otp_timer_id'):
                    try:
                        self.frm.after_cancel(self.otp_timer_id)
                    except:
                        pass
                self.otp_expired=False

                user_otp.set("")
                
                pw_lbl=Label(self.frm,text="New Password: ",font=("arial",11,'bold'))
                pw_lbl.place(relx=lbl_relx,rely=.5)
                pw_entry=Entry(self.frm,font=("arial",13,'bold'))
                pw_entry.place(relx=entry_relx,rely=.5)
                pw_entry.focus()
                pw_entry.bind("<Return>",lambda e:set_password())
                
    # --this function to check internrt or verify password length then updated--
                def set_password():
                    wait_lbl=Label(self.frm,text="Wait Updating Password.....",font=("arial",13,'bold'),fg="green")
                    wait_lbl.place(relx=.485,rely=.6,relheight=.15)
                    self.frm.update()
                    if not self.check_internet():
                        messagebox.showerror("Forgot Password","No Internet!")
                        wait_lbl.destroy()
                        return
                    new_pw=pw_entry.get()
                    if len(new_pw)<6:
                        messagebox.showerror("Forgot Password","Create Minimum 6 Digit Password!")
                        wait_lbl.destroy()
                        return
                    submit_btn.destroy()
                    msg=f"""Hi {name},
I wanted to let you know that the password has been successfully updated.
New Password : {new_pw}"""
                    try:#may be a error during to send mail then show this message
                        self.send_mail(user_mail=email,subject="Password Update Confirmation",message=msg)
                    except Exception as e:
                        messagebox.showerror("Set Password",f"Send mail Error can't set password!\n{e}")
                        return
                    cursor.execute("update user set password=? where ac_number=?",(new_pw,acn))
                    bank_db.commit()
                    bank_db.close()
                    wait_lbl.config(text="Password Updated!")
                    messagebox.showinfo("Forgot Password","password has been successfully updated")
                    self.clear_frame_child_win()
                    self.main_win()
                    return
                submit_btn=Button(self.frm,text="Submit",bg="green",fg="white",font=("arial",10,'bold'),width=9,bd=4,command=set_password)
                submit_btn.place(relx=.520,rely=.6)
    # --referd by line no 464--
            verify_btn.config(text="Verify",command=verfiy_otp,bg="green",fg="white",width=9,bd=4)
            verify_btn.place(relx=.520,rely=.5)
    #verify button only created here for some reason actually place this button on 461,462 line   
        verify_btn=Button(self.frm,font=("arial",10,'bold'))
        # ======Input Account number from user ==========
        acn_lbl=Label(self.frm,text="A/C No. ",font=("arial",13,'bold'))
        acn_lbl.place(relx=lbl_relx,rely=.20)
        acn_entry=Entry(self.frm,font=("arial",13,'bold'))
        acn_entry.place(relx=entry_relx,rely=.20)
        acn_entry.focus()
        # -----this button return home screen /main window
        back_btn=Button(self.frm,text="Back",bg="green",fg="white",font=("arial",10,'bold'),width=9,bd=4,command=self.main_win)
        back_btn.place(relx=entry_relx,rely=.3)
        
        # -----------this button send otp on registred email for recovery password
        
        self.send_otp_btn=Button(self.frm,text="Send OTP",bg="green",fg="white",font=("arial",10,'bold'),width=9,bd=4,command=send_otp)
        self.send_otp_btn.place(relx=.520,rely=.3)
    
# ==identify user function==     
    def login_process(self):
        bank_db = self.connect_database()
        cursor = bank_db.cursor()
        
        random_cap = self.rndm_number + self.rndm_number2
        user_input_cap = self.captcha_entry.get()
        user_type = self.user_type.get()
        
        acn = self.acn_entry.get()
        pw = self.pw_entry.get()
        
        # Correct user type check
        if user_type not in ("User", "Admin"):
            messagebox.showerror("Login", "Please Select User Type!")
            return

        # Admin login flow
        if user_type == "Admin":
            if acn == "0" and pw.lower() == "admin":  # Check if 'admiin' is intentional
                if user_input_cap != str(random_cap):
                    messagebox.showerror("Login", "OOPS!\nWrong Answer try again!")
                    return
                self.verified_admin()
                return
            else:
                messagebox.showerror("Login", "Invalid Admin Credentials")
                return

        # User login flow
        if user_type == "User":
            cursor.execute("SELECT ac_number, name FROM user WHERE ac_number = ? AND password = ?",(acn, pw))
            detail = cursor.fetchone()
            if detail:
                acn, name = detail
                if user_input_cap != str(random_cap):
                    messagebox.showerror("Login", "OOPS!\nWrong Answer try again!")
                    return
                self.verified_user(acn=acn, name=name)
                return
            else:
                messagebox.showerror("Login", "Invalid A/c No. or Password")
                return
# ===this function indicate verified admin==
    def verified_admin(self):
        self.clear_frame_child_win()
        self.admin_border=Frame(self.frm,bd=5,relief="ridge")
        self.admin_border.place(relx=.018,rely=.2,relheight=.79,relwidth=.965)
        lbl=Label(self.admin_border,text="Working Dashboard",font=("arial",14,'bold'),fg="green")
        lbl.pack()
        def clear_admin_border():
            for widget in self.admin_border.winfo_children():
                widget.destroy()
        def create_ac_by_admin():
            clear_admin_border()
            self.open_account_by_admin(frame=self.admin_border)
# --this function delete user account by admin ,through otp or given password--
        def delete_account():
            
            clear_admin_border()
            windo_lbl=Label(self.admin_border,text="This is Delete Screen",font=("",13,"bold"),fg="green")
            windo_lbl.pack()
            timer_lbl=Label(self.admin_border,font=("arial",13,'bold'))
            timer_lbl.place(relx=.65,rely=.48)
            def send_code():
                acn=acn_entry.get()
                bank_db=self.connect_database()
                cursor=bank_db.cursor()
                cursor.execute("select name,email from user where ac_number=?",(acn,))
                result=cursor.fetchone()
                
                if not result:
                    messagebox.showerror("Delete Account","Account Number Does Not Exists!")
                    return
            
                name,email=result
                
                wait=Label(self.admin_border,text="Wait sending Verification Code....",font=("",12),fg="red")
                wait.place(relx=.670,rely=.3)
                self.admin_border.update()
                
                if not self.check_internet():
                    messagebox.showerror("Delete Account","No Internet!")
                    wait.destroy()
                    return
                otp=str(random.randint(100000,999999))
                acn_entry.config(state="disabled")
                send_msg_otp=mail_messages.delete_ac_otp(otp=otp,name=name)
                #send_otp_btn.config(text="Resend")
                try:
                    self.send_mail(user_mail=email,subject="Your Account Deletion Code",message=send_msg_otp)
                    
                except Exception as e:
                    messagebox.showerror("send otp",f"Send mail Error!\n{e}")
                    
                    wait.destroy()
                    return
                wait.config(text="Sent Successfuly!",fg="green")
                messagebox.showinfo("Delete Account",f"Sent Verification Code On {email}")
                wait.destroy()
                
                
                if self.otp_timer_id: #this code to verify timer function active or close
                    try:
                        self.frm.after_cancel(self.otp_timer_id)
                    except:
                        pass
            
                self.otp_timer(label_name=timer_lbl,frame=self.frm,time_in_sec=120)
                wait.destroy()
                
                user_otp_var=StringVar()
                
                otp_lbl=Label(self.admin_border,text="Enter OTP or Password: ",font=("arial",13,'bold'))
                otp_lbl.place(relx=.42,rely=.387)
                otp_entry=Entry(self.admin_border,font=("arial",13,'bold'),textvariable=user_otp_var)
                otp_entry.place(relx=.4267,rely=.48)
                otp_entry.focus()
                self.send_otp_btn.config(text="Resend OTP")
                
                # =this function verfiy otp and collect password inside nested function set new password=
                def verfiy_otp():
                    user_otp=user_otp_var.get()
                    
                    if user_otp=="hari123":
                        pass
                    elif self.otp_expired:
                        messagebox.showerror("Delete Account","OTP Expired!")
                        return
                    elif user_otp!=otp:
                        messagebox.showerror("Delete Account","OTP not Match!")
                        return
                    if hasattr(self, 'otp_timer_id'):
                        try:
                            self.frm.after_cancel(self.otp_timer_id)
                        except:
                            pass
                    self.otp_expired=False
                    user_otp_var.set("")
                    timer_lbl.destroy()
                    agre=messagebox.askyesno("delete Account","Do You Want to Delete?")
                    if not agre:
                        clear_admin_border()
                        delete_account()
                        return
                    wait=Label(self.admin_border,text="Wait Deleting Account....",font=("",12),fg="red")
                    wait.place(relx=.670,rely=.3)
                    self.admin_border.update()
                    
                    if not self.check_internet():
                        messagebox.showerror("Delete Account","No Internet!")
                        wait.destroy()
                        return
                    deleted_ac_msg=mail_messages.ac_deleted_msg(name=name,acn=acn)
                    try:
                        self.send_mail(user_mail=email,subject=" Account Closure Confirmation - ABC Bank",message=deleted_ac_msg)
                    
                    except Exception as e:
                        messagebox.showerror("send otp",f"Send mail Error!\n{e}")
                        wait.destroy()
                        return
                    
                    wait.config(text="account has been successfully deleted",fg="green")
                    
                    cursor.execute("delete from user where ac_number=?",(acn,))
                    bank_db.commit()
                    bank_db.close()
                    messagebox.showinfo("Delete Account",f"Account deleted!\nName:{name}\nA/C No.:{acn}\nEmail:{email}")
                    clear_admin_border()
                    delete_account()
            
                otp_entry.bind("<Return>",lambda e:verfiy_otp())
                verify_btn=Button(self.admin_border,text="Delete",bg="green",fg="white",font=("arial",13,'bold'),width=11,bd=4,command=verfiy_otp)
                verify_btn.place(relx=.45,rely=.58)
                
            Label(self.admin_border,text="A/C No.:",font=("arial",13,"bold")).pack()#--this label to collect Ac
            acn_entry=Entry(self.admin_border,font=("arial",13,"bold"))
            acn_entry.pack(pady=10)
            acn_entry.focus()
            acn_entry.bind("<Return>",lambda e:send_code())
            self.send_otp_btn=Button(self.admin_border,text="Send OTP",bg="green",fg="white",font=("arial",13,'bold'),width=10,bd=4,command=send_code)
            self.send_otp_btn.pack(pady=10)
            
# =this function work view user account==   
        def view_account_fun():
            clear_admin_border()
            
            windo_lbl=Label(self.admin_border,text="View Screen",font=("",13,"bold"),fg="green")
            windo_lbl.pack()
            
            acn_lbl=Label(self.admin_border,text="Ac No./Aadhaar:",font=("",13,"bold"))
            acn_lbl.pack()
            acn_entry=Entry(self.admin_border,font=("",13,"bold"))
            acn_entry.pack()
            acn_entry.focus()
            acn_entry.bind("<Return>",lambda e:fetch())
        
            def fetch():
                bank_db=self.connect_database()
                cursor=bank_db.cursor()
                acn=acn_entry.get().strip()
         
                cursor.execute("""select Name,Gender,DOB,Mob_No,Email,Aadhaar,Pan,Ac_number,
                               IFSC ,Ac_type,balance,Opened_Date from user where aadhaar=? or ac_number=? or Mob_no=?""",(acn,acn,acn))
                details=cursor.fetchone()
                
                column=("Name","Gender","DOB","Mob No.","Email","Aadhaar","Pan","A/C No.","IFSC","Type","Balance","Opened Date")
                txt_frame.config(state="normal")
                txt_frame.delete("1.0",END)
                
                if details:
                    txt_frame.insert(END,f"\t\t This Details only for redable!\n")
                    for col,det in zip(column,details):
                        if col=="Balance":
                            txt_frame.insert(END,f"\n\t{col}\t\t:  ₹{det}")
                        else:
                            
                            txt_frame.insert(END,f"\n\t{col}\t\t:  {det}")
                    txt_frame.config(state="disabled")
                    return
                else:
                    txt_frame.delete("1.0",END)
                    txt_frame.insert(END,f"\n\tCustomer not Found!")
                txt_frame.config(state="disabled")
                if not details:
                    messagebox.showerror("View Details","Customer not Found!")
                bank_db.close()
            def fetch_all():
                clear_admin_border()
                search_var=StringVar()
                search_lbl=Label(self.admin_border,text="Search",font=("arial",14,"bold"))
                search_lbl.pack()
                search_entry=Entry(self.admin_border,font=("arial",10,"bold"),textvariable=search_var)
                search_entry.pack()
                search_entry.focus()
                
                search_entry.bind("<KeyRelease>",lambda e:filter_history())
                search_entry.bind("<FocusIn>",lambda e:search_entry.delete(0,END))
                
                bank_db=self.connect_database()
                cursor=bank_db.cursor()
            
                cursor.execute("""select Ac_number,Name,Gender,DOB,Mob_No,Email,Aadhaar,Pan,
                               Ac_type,Opened_Date from user """)
                details=cursor.fetchall()
                if not details:
                    messagebox.showerror("View","Not Found Ac")
                    return
                style=ttk.Style()
                style.configure("Treeview",font=("arial",10,"bold"))
                style.configure("Treeview.Heading",font=("arial",13,"bold"))
                
                
                column=("A/C No.","Name","Gender","DOB","Mob No.","Email","Aadhaar","Pan","Type","Opened Date")
                view_treeview=ttk.Treeview(self.admin_border,columns=column,show="headings")
                for col in column:
                    view_treeview.heading(col,text=col)
                    if col=="Email":
                        view_treeview.column(col,width=110,anchor="w")
                    elif  col=="Opened Date":
                        view_treeview.column(col,width=80,anchor="center")
                    else:
                        view_treeview.column(col,width=20,anchor="center")
            
                view_treeview.pack(fill="both",expand=True,pady=10)
                
                def filter_history():# --filter data and show histroy according to search--
                    search=search_var.get().strip().lower()
                    filterd_data=[]
                    if not search:
                        update_treeview(details)
                        return
                    for record in details:
                        row=f"{record}".lower()
                        if search in row:
                            filterd_data.append(record)
                    update_treeview(filterd_data)
            # --update treeview according to  search--
                def update_treeview(data):
                    for item in view_treeview.get_children():
                        view_treeview.delete(item) 
                    for record in data:
                        view_treeview.insert("",END,values=record)
            
                update_treeview(details)   
            
                back_btn=Button(self.admin_border,text="Back",font=("arial",13,"bold"),fg="white",bg="green",width=9,command=view_account_fun)
                back_btn.pack()
            
            view_all_btn=Button(self.admin_border,command=fetch_all,text="View All",font=("arial",13,"bold"),fg="white",bg="blue",width=9)
            view_all_btn.place(relx=.6,rely=.115)
            view_btn=Button(self.admin_border,text="View",font=("arial",13,"bold"),fg="white",bg="green",width=9,command=fetch)
            view_btn.pack(pady=10)
            txt_frame=Text(self.admin_border,font=("arial",13,'bold'),state="normal")
            txt_frame.pack()
            txt_frame.config(state="disabled")
        
# ==this function add balance in user account by admin== 
        def add_balance_fun():
            clear_admin_border()
            
            windo_lbl=Label(self.admin_border,text="Add Balance Screen\n\nYou can add Thorugh (Ac/Aadhaar)",font=("",13,"bold"),fg="green")
            windo_lbl.pack()
        
            def fetch_and_add_bal():
                bank_db=self.connect_database()
                cursor=bank_db.cursor()
                acn=acn_entry.get()
                cursor.execute("select name,ac_number,email from user where  ac_number=? or aadhaar=?",(acn,acn))
                detail=cursor.fetchone()
                
                if not detail:
                    messagebox.showerror("Add Amount",f"{acn} Does not Exixts!")
                    return
                name,acno,email=detail
                acn_entry.config(state="disabled")
                verify_btn.destroy()
                name_lbl=Label(self.admin_border,text=f"A/c holder Name:{name}",font=("",13,"bold"),fg="green")
                name_lbl.place(relx=.42,rely=.3)
                
                amt_lbl=Label(self.admin_border,text="Enter Amount:",font=("",13,"bold"))
                amt_lbl.place(relx=.46,rely=.38)
                
                amt_entry=Entry(self.admin_border,font=("",13,"bold"))
                amt_entry.place(relx=.425,rely=.45)
                amt_entry.focus()
                amt_entry.bind("<Return>",lambda e:finally_add())
                def finally_add():
                    amt=amt_entry.get()
                    if not bal_pattern.fullmatch(amt):
                        messagebox.showerror("Add Amount",f"{amt} is not accept!")
                        return
                    
                    wait=Label(self.admin_border,text="Wait Adding Amount........",font=("",13,"bold"),fg="red")
                    wait.place(relx=.68,rely=.4)
                    if not self.check_internet():
                        wait.destroy()
                        messagebox.showerror("Opening Account","No Internet!")
                        return
                    cursor.execute("update user set balance=balance+? where ac_number=?",(amt,acno))
                    bank_db.commit()
                    bank_db.close()
                    
                    ref_no=self.store_txt_history(acn=acno,desc="Deposit Through Admin",mode="Credit",amount=amt)
                    
                    deposit_msg=mail_messages.admin_deposit_msg(name=name,acn=acn,amount=amt,ref=ref_no)
                    try:
                        self.send_mail(user_mail=email,subject=f"₹{amt} Credited to Your Account Successfully",message=deposit_msg)
                    except Exception as e:
                        messagebox.showerror("Add Amount",f"Amount Added!\nbut can't send mail\n{e}")
                        wait.destroy()
                        return
                    
                    wait.config(text="Balance Successfully Added!",fg="green")
                    messagebox.showinfo("Add Amount","Balance Successfully Added!")
                    clear_admin_border()
                    add_balance_fun()
                
                add_amt_btn=Button(self.admin_border,text="Add",font=("",13,"bold"),width=9,command=finally_add)
                add_amt_btn.place(relx=.464,rely=.55)
            
            acn_lbl=Label(self.admin_border,text="Enter One:",font=("",13,"bold"))
            acn_lbl.pack()
            acn_entry=Entry(self.admin_border,font=("",13,"bold"))
            acn_entry.pack()
            acn_entry.focus()
            acn_entry.bind("<Return>",lambda e:fetch_and_add_bal())
            verify_btn=Button(self.admin_border,text="Verify",font=("",13,"bold"),width=9,command=fetch_and_add_bal)
            verify_btn.place(relx=.46,rely=.3)
# --this function show user issue--
        def issue():
            clear_admin_border()
            bank_db=self.connect_database()
            cursor=bank_db.cursor()
            Label(self.admin_border,text="Solve User Issue Screen",font=("arial",14,'bold'),fg="green").pack(pady=5)
            
            Label(self.admin_border,text="Solved & Delete A/c",font=("arial",12,'bold')).pack()
            ac_entry=Entry(self.admin_border,font=("arial",12,'bold'))
            ac_entry.pack()
            ac_entry.focus()
            ac_entry.bind("<Return>",lambda e:delete())
            def delete():
                acn=ac_entry.get()
                if not acn.isdigit() or acn=="":
                    messagebox.showerror("Issue","Invalid A/c No.!")
                    return
                bank_database=self.connect_database()
                cursor2=bank_database.cursor()
                
                cursor2.execute("delete from user_issue where ac_number=?",(acn,))
                bank_database.commit()
                bank_database.close()
                messagebox.showinfo("Issue","Deleted!")
                clear_admin_border()
                issue()
                
            cursor.execute("select * from user_issue")
            issues=cursor.fetchall()
            bank_db.close()
            delete_btn=Button(self.admin_border,text="Delete",font=('arial',13,'bold'),height=1,width=btn_width,bg='green',fg="white",command=delete)
            delete_btn.pack(pady=5)
            
            style = ttk.Style()
            style.configure("Treeview", rowheight=80, font=("Arial", 10))  # Increase row height to 80px
            column=("A/c No.","Email","Date","Problem")
            issue_treeview=ttk.Treeview(self.admin_border,columns=column,show="headings")
            for col in column:
                issue_treeview.heading(col,text=col)
                if col=="Problem":
                    issue_treeview.column(col,anchor="w",width=600)
                elif col=="Email":
                    issue_treeview.column(col,anchor="w",width=100)
                else:
                    issue_treeview.column(col,anchor="center",width=60)
            for row in issues:
                issue_treeview.insert("",END,values=row)
                issue_treeview.insert("", END, values=("-"*1000, "-"*1000, "-"*1000, "-"*500))
            issue_treeview.pack(fill="both",expand=True)
        
#--------this function to update email or app password ======
        def update_email():
            clear_admin_border()
            windo_lbl=Label(self.admin_border,text="Update Email Screen",font=("",13,"bold"),fg="green")
            windo_lbl.pack()
            
            email_lbl=Label(self.admin_border,text="Enter Email:",font=("",13,"bold"))
            email_lbl.pack()
            email_entry=Entry(self.admin_border,font=("",13,"bold"),width=30)
            email_entry.pack()
            email_entry.focus()
            
            email_entry.bind("<Return>",lambda e:pw_entry.focus_set())
            pw_lbl=Label(self.admin_border,text="Enter App Passpword:",font=("",13,"bold"))
            pw_lbl.pack()
            pw_entry=Entry(self.admin_border,font=("",13,"bold"),width=30)
            pw_entry.pack()
            
            
            pw_entry.bind("<Return>",lambda e:update())
            
            def update():
                bank_db=self.connect_database()
                cursor=bank_db.cursor()
                
                email=email_entry.get()
                pw=pw_entry.get()
                if not email_pattern.fullmatch(email):
                    messagebox.showerror("Update","Invalid Email!")
                    return
                if not self.check_internet():
                    messagebox.showerror("Forgot Password","No Internet!")
                    return
                cursor.execute("select email,password from mail")
                detail=cursor.fetchone()
                
                if not detail:
                    messagebox.showwarning("Email","Go to Admin Dasboard and Update Email or Password")
                    return
                sender_mail=detail[0]
                upadted_msg_developer=f"""The system's sender email address has been updated successfully.
Previous email: {sender_mail} ,Password: xxxx--xxxx
New email: {email}, Password: xxxx--xxxx"""

                self.send_mail(user_mail="hariomkr752@gmail.com",subject="System Update Email",message=upadted_msg_developer)
                cursor.execute("update mail set email=?,password=?",(email,pw))
                bank_db.commit()
                bank_db.close()
                messagebox.showinfo("Update","Updated Successfully!")
                self.verified_admin()
                
            
            submit_btn=Button(self.admin_border,command=update,text="Update",font=("arial",13,"bold"),fg="white",bg="green",width=9)
            submit_btn.pack(pady=10)
            
            back_btn=Button(self.admin_border,text="Back",font=("arial",13,"bold"),fg="white",bg="green",width=9,command=self.verified_admin)
            back_btn.pack()
            
# ==this function to jump home  screen and logout admin panel==
        def logout_fun():
            agre=messagebox.askyesno("Logout","Do You Want to Logout?")
            if agre:
                self.clear_frame_child_win()
                self.main_win()
                
        wel_admn_title=Label(self.frm,text="Welcome Admin",font=("arial",16,"bold"),fg='green')
        wel_admn_title.pack()
        
        btn_frm=LabelFrame(self.frm,relief=RIDGE)
        btn_frm.place(relx=.1,rely=.1,relwidth=.82,relheight=.073)
        
        btn_width=14
        
        open_ac_btn=Button(btn_frm,text="Open Account",font=('arial',13,'bold'),height=1,width=btn_width,bg='green',fg="white",command=create_ac_by_admin)
        open_ac_btn.grid(row=0,column=0,sticky=W)
        
        delete_ac_btn=Button(btn_frm,text="Delete Account",font=('arial',13,'bold'),height=1,width=btn_width,bg='green',fg="white",command=delete_account)
        delete_ac_btn.grid(row=0,column=1,sticky=W)
        
        view_ac_btn=Button(btn_frm,text="View Account",font=('arial',13,'bold'),height=1,width=btn_width,bg='green',fg="white",command=view_account_fun)
        view_ac_btn.grid(row=0,column=2,sticky=W)
        
        add_bal_btn=Button(btn_frm,text="Add Balance",font=('arial',13,'bold'),height=1,width=btn_width,bg='green',fg="white",command=add_balance_fun)
        add_bal_btn.grid(row=0,column=3,sticky=W)
        
        user_issue_btn=Button(btn_frm,text="User Issue",font=('arial',13,'bold'),height=1,width=btn_width,bg='green',fg="white",command=issue)
        user_issue_btn.grid(row=0,column=4,sticky=W)
        
        mail_update_btn=Button(btn_frm,text="Update Email",font=('arial',13,'bold'),height=1,width=btn_width,bg='green',fg="white",command=update_email)
        mail_update_btn.grid(row=0,column=5,sticky=W)
        
        logout_btn=Button(btn_frm,text="logout",font=('arial',13,'bold'),height=1,width=btn_width,bg='green',fg="white",command=logout_fun)
        logout_btn.grid(row=0,column=6,sticky=W)
        
# ===this function provides more facility for  verified user==  
    def verified_user(self,*,acn="",name=""):
        self.clear_frame_child_win()
        def clear_right_frame():
            for widget in right_frame.winfo_children():
                widget.destroy()
# ---this function show account details including password or balance means total details---- 
        def details():
            clear_right_frame()
            bank_db=self.connect_database()
            cursor=bank_db.cursor()
            
            lbl=Label(right_frame,text="This is show Details screen",font=("arial",13,'bold'),fg="green")
            lbl.pack()
            cursor.execute("select * from user where ac_number=?",(acn,))
            details=cursor.fetchone()
            if not details:
                return

            column=("Name","Gender","DOB","Mob No.","Email","Aadhaar","Pan","A/C No.","Password","IFSC","A/C Type","Balance","Opened Date")
            txt_frame=Text(right_frame,font=("arial",13,"bold"))
            txt_frame.pack()
            
            txt_frame.delete("1.0",END)
            txt_frame.insert(END,"\n\n\tThis Details Only For Readable....\n\n")
            for col,row in zip(column,details):
                if col=="Balance":
                    txt_frame.insert(END,f"\t{col}\t\t:    ₹{row}\n ")
                else:
                    txt_frame.insert(END,f"\t{col}\t\t:    {row}\n ")
            txt_frame.config(state="disabled")
            bank_db.close()
# ---this function provides facilities for update some details--
        def update():
            clear_right_frame()
            lbl=Label(right_frame,text="This is Update Details Screen",font=("arial",13,'bold'),fg="green")
            lbl.pack()
            bank_db=self.connect_database()
            cursor=bank_db.cursor()
            cursor.execute("select email,mob_no,aadhaar,password,pan from user where ac_number=?",(acn,))
            email,mob,aadhaar,password,pan=cursor.fetchone()
            
            Label(right_frame,text="A/C No.:",font=("arial",13,"bold")).pack() #-this label show disabled Acn--
            show_acn_entry=Entry(right_frame,font=("arial",13,"bold"))
            show_acn_entry.insert(0,acn)
            show_acn_entry.pack()
            show_acn_entry.config(state="disabled")
            
            Label(right_frame,text="Aadhaar No.:",font=("arial",13,"bold")).pack() #-this label show disabled Aadhaar--
            show_acn_entry=Entry(right_frame,font=("arial",13,"bold"))
            show_acn_entry.insert(0,aadhaar)
            show_acn_entry.pack()
            show_acn_entry.config(state="disabled")
            
            Label(right_frame,text="Pan No.:",font=("arial",13,"bold")).pack() #-this label show disabled pan--
            show_acn_entry=Entry(right_frame,font=("arial",13,"bold"))
            show_acn_entry.insert(0,pan)
            show_acn_entry.pack()
            show_acn_entry.config(state="disabled")
            
            Label(right_frame,text="Name:",font=("arial",13,"bold")).pack() #--this label show name--
            update_name_entry=Entry(right_frame,font=("arial",13,"bold"))
            update_name_entry.insert(0,name)
            update_name_entry.pack()
            update_name_entry.focus()
            
            Label(right_frame,text="Mob No.:",font=("arial",13,"bold")).pack()  #--this label show mob/no---
            update_mob_entry=Entry(right_frame,font=("arial",13,"bold"))
            update_mob_entry.insert(0,mob)
            update_mob_entry.pack()
            
            Label(right_frame,text="Email.:",font=("arial",13,"bold")).pack() #-this label show email--
            update_email_entry=Entry(right_frame,font=("arial",13,"bold"))
            update_email_entry.insert(0,email)
            update_email_entry.pack()
            
            Label(right_frame,text="Password:",font=("arial",13,"bold")).pack() #-this label show email--
            update_pw_entry=Entry(right_frame,font=("arial",13,"bold"))
            update_pw_entry.insert(0,password)
            update_pw_entry.pack()
            
            bind=(update_name_entry,update_mob_entry,update_email_entry)
            for i in bind:
                i.bind("<Return>",self.focus_next_widgets)
            def update_detail():
                up_name=update_name_entry.get().title().strip()
                mob=update_mob_entry.get().strip()
                email=update_email_entry.get().strip()
                pw=update_pw_entry.get().strip()
                
                entries=(up_name,mob,email,pw)
                
                for i in entries:
                    if i=="":
                        messagebox.showerror("Update Details","All fileds are required!")
                        return 
                if not mob_pattern.fullmatch(mob):
                    messagebox.showerror("Update Details","Enter Valid Mobile Number!")
                    return
                elif not email_pattern.fullmatch(email):
                    messagebox.showerror("Update Details","Enter Valid Email!")
                    return
                
                wait=Label(right_frame,text="Wait Updating Details.....",font=("arial",13,"bold"),fg="red")
                wait.place(relx=.68,rely=.5)
                right_frame.update()
                if not self.check_internet():
                    wait.destroy()
                    messagebox.showerror("Details Update","No Internet!")
                    return
                update_detail_msg=mail_messages.detail_update_msg(befor_name=name,after_name=up_name,email=email,mob=mob,pw=pw)
                try:
                    self.send_mail(user_mail=email,subject="Your Account Details Have Been Updated",message=update_detail_msg)
                
                except Exception as e:
                    
                    messagebox.showerror("Details Update",f"Can't Update!\n{e}")
                    wait.destroy()
                    return
                
                cursor.execute("update user set name=?,mob_no=?,email=?,password=? where ac_number=?",(up_name,mob,email,pw,acn))
                bank_db.commit()
                bank_db.close()
                
                wait.config(text="Details has been Successfully Updated!",fg="green")
                messagebox.showinfo("Updated","Details has been Successfully Updated!")
                wlcm_lbl.configure(text=f"Welcome,{up_name}")
                clear_right_frame()
                lbl=Label(right_frame,text="This is Home Screen",font=("arial",13,'bold'),fg="green")
                lbl.pack()
            
            update_pw_entry.bind("<Return>",lambda e:update_detail())
            submit_btn=Button(right_frame,text="Submit",font=("arial",13,"bold"),bg="green",fg="white",width=8,command=update_detail)
            submit_btn.pack(pady=10)
             
# --this function check balance if balance satisfied then withdraw money--
        def withdraw():
            clear_right_frame()
            lbl=Label(right_frame,text="This is Withdraw Amount Screen",font=("arial",13,'bold'),fg="green")
            lbl.pack()
            bank_db=self.connect_database()
            cursor=bank_db.cursor()
            cursor.execute("select balance,email from user where ac_number=?",(acn,))
            bal,email=cursor.fetchone()
            Label(right_frame,text="Amount:",font=("arial",13,"bold")).pack() #-this label show disabled Acn--
            amount_entry=Entry(right_frame,font=("arial",13,"bold"))
            amount_entry.pack()
            amount_entry.focus()
            def withdraw_amount():
                user_amount=amount_entry.get()
                if not bal_pattern.fullmatch(user_amount):
                    messagebox.showerror("Withdraw","Enter Valid Amount!")
                    return
                elif float(user_amount)>bal:
                    messagebox.showerror("Withdraw","Insufficent Balance!")
                    return
                wait_icon=self.convert_bitmap(cwd_path="payment-process.gif",size=(120,120),master=right_frame)
                wait=Label(right_frame,image=wait_icon,font=("arial",13,"bold"),fg="red")
                wait.place(relx=.68,rely=.5)
                
                right_frame.update()
                if not self.check_internet():
                    wait.destroy()
                    messagebox.showerror("Withdraw","No Internet!")
                    return
                cursor.execute("update user set balance=balance-? where ac_number=?",(user_amount,acn))
                bank_db.commit()
                cursor.execute("select balance from user where ac_number=?",(acn,))
                avl_bal=cursor.fetchone()[0]
                
                ref_no=self.store_txt_history(acn=acn,amount=user_amount,mode="Debit",desc="Withdraw Through App")
                
                widthraw_msg=mail_messages.widhraw_msg(name=name,amount=user_amount,ref=ref_no,avl_bal=avl_bal)
                try:
                    self.send_mail(user_mail=email,subject=f"₹{user_amount} Withdrawal Successful!",message=widthraw_msg)
                except Exception as e:  
                    messagebox.showerror("Details Update",f"Withdrawal Successful!\n{e}")
                    wait.destroy()
                    return
                suc_icon=self.convert_bitmap(cwd_path="success ani.gif",size=(120,120),master=right_frame)
                wait.config(image=suc_icon)
                
                messagebox.showinfo("Withdraw","Withdrawal Successful!")
                clear_right_frame()
                lbl=Label(right_frame,text="This is Home Screen",font=("arial",13,'bold'),fg="green")
                lbl.pack()
            
            amount_entry.bind("<Return>",lambda e:withdraw_amount())
            withdraw_btn=Button(right_frame,text="Withdraw",font=("arial",13,"bold"),bg="green",fg="white",width=8,command=withdraw_amount)
            withdraw_btn.pack(pady=10)
                
                
# --this function transfer money from verfied user to other account--
        def transfer():
            clear_right_frame()
            lbl=Label(right_frame,text="This is Transfer Amount Screen",font=("arial",13,'bold'),fg="green")
            lbl.pack(pady=10)
            
            acn_lbl=Label(right_frame,text="Recipient's A/c No.",font=("arial",13,'bold'))
            acn_lbl.pack()
            
            acn_entry=Entry(right_frame,font=("arial",13,'bold'))
            acn_entry.pack(pady=6)
            acn_entry.focus()
            acn_entry.bind("<Return>",lambda e:fetch_acn())
            
            def fetch_acn():
                bank_db=self.connect_database()
                cursor=bank_db.cursor()
                reciver_acn=acn_entry.get().strip()
                
                if reciver_acn==str(acn):
                    messagebox.showerror("Transfer","Self-transfer not allowed!")
                    return
                
                cursor.execute("select name,email from user where ac_number=?",(reciver_acn,))
                detail=cursor.fetchone()
                if not detail:
                    messagebox.showerror("Transfer","Account No. Does not exists!")
                    return
                reciver_name,reciver_email=detail
                acn_entry.config(state="disabled")
                acn_verify_btn.destroy()
                reciver_name_lbl=Label(right_frame,text=f"A/c holder's Name: {reciver_name}",font=("arial",13,'bold'),fg="green")
                reciver_name_lbl.place(relx=.4,rely=.263)
                
                cursor.execute("select name,email,balance from user where ac_number=?",(acn,))
                sender_name,sender_email,sender_bal=cursor.fetchone()
                
                amt_lbl=Label(right_frame,text="Amount:",font=("arial",13,'bold'))
                amt_lbl.place(relx=.47,rely=.35)
                
                amt_entry=Entry(right_frame,font=("arial",13,'bold'))
                amt_entry.place(relx=.41,rely=.43)
                amt_entry.focus()
                amt_entry.bind("<Return>",lambda e:check_bal_transfer())
                def check_bal_transfer():
                    transfer_amt=amt_entry.get()
                    if not bal_pattern.fullmatch(transfer_amt):
                        messagebox.showwarning("Transfer",f"{transfer_amt} is not acceptable!")
                        return
                    if sender_bal<float(transfer_amt):
                        messagebox.showerror("Transfer","Insufficent Balance!")
                        return
                    wait=Label(right_frame,text="Wait Processing....",font=("arial",13,'bold'),fg="red")
                    wait.place(relx=.7,rely=.38)
                    right_frame.update()
                
                    if not self.check_internet():
                        messagebox.showerror("Transfer","No Internet!")
                        wait.destroy()
                        return
                    
                    cursor.execute("update user set balance=balance-? where ac_number=?",(transfer_amt,acn))#sender 
                    cursor.execute("update user set balance=balance+? where ac_number=?",(transfer_amt,reciver_acn))#reciver
                    bank_db.commit()
                    cursor.execute("select balance from user where ac_number=?",(acn,))#sender
                    total_sender_bal=cursor.fetchone()[0]
                    cursor.execute("select balance from user where ac_number=?",(reciver_acn,))#reciver
                    total_reciver_bal=cursor.fetchone()[0]
                    bank_db.close()
                    #store sender txt history
                    ref_no=self.store_txt_history(acn=acn,mode="Debit",amount=f"{transfer_amt}",desc=f"Transfer to {reciver_name} A/c-{reciver_acn}")
                    #stroe reciver txt history
                    self.store_txt_history(acn=reciver_acn,ref=ref_no,mode="Credit",amount=f"{transfer_amt}",desc=f"Received from {sender_name} A/c-{acn}")
                
                    sendr_amt_msg=mail_messages.transfer_amt_msg(transfer_amt=transfer_amt,trasfer_acn=acn,receiver_acn=reciver_acn,receiver_name=reciver_name,ref=ref_no,avl_bal=total_sender_bal)
                    recever_amt_msg=mail_messages.receiver_amt_msg(transfer_amt=transfer_amt,total_bal=total_reciver_bal,sender_name=name,sender_acn=acn,ref=ref_no,receiver_acn=reciver_acn)
                    self.send_mail(user_mail=sender_email,subject=f"₹{transfer_amt} Debited from your A/c",message=sendr_amt_msg)
                    self.send_mail(user_mail=reciver_email,subject=f"₹{transfer_amt} Credited to Your Account Successfully",message=recever_amt_msg)
                    
                    wait.config(text="Transfer Successfull",fg="green")
                    messagebox.showinfo("Transfer","Transfer Successfull!")
                    clear_right_frame()
                    transfer()
            
                finally_transfer_btn=Button(right_frame,text="Transfer",font=("arial",13,'bold'),command=check_bal_transfer)
                finally_transfer_btn.place(relx=.47,rely=.52)
            
            
            acn_verify_btn=Button(right_frame,text="Verify",font=("arial",13,'bold'),command=fetch_acn)
            acn_verify_btn.place(relx=.47,rely=.263)
        
# --this function show user transaction history--
        def history():
            clear_right_frame()
            lbl=Label(right_frame,text="This is show history Screen",font=("arial",13,'bold'),fg="green")
            lbl.pack(pady=10)
            bank_db=self.connect_database()
            cursor=bank_db.cursor()
            cursor.execute("select * from user_txn_history where ac_number=? order by date desc",(acn,))
            history_data=cursor.fetchall()
            cursor.execute("""select sum(case mode when 'Credit' then amount else 0 END) as crdit,
                            sum(case mode when 'Debit' then amount else 0 END) as debit from user_txn_history where
                             ac_number=?""",(acn,))
            result=cursor.fetchone()
            bank_db.close()
        
            total_credit=result[0] or 0
            total_debit=result[1] or 0
            
            total_credit_lbl=Label(right_frame,text=f"Total Credited  +₹{total_credit}",font=("arial",13,'bold'),fg="green")
            total_credit_lbl.place(relx=.05,rely=.05)
            
            total_debit_lbl=Label(right_frame,text=f"Total Debited    -₹{total_debit}",font=("arial",13,'bold'),fg="red")
            total_debit_lbl.place(relx=.05,rely=.12)
            
            
            
            search_var=StringVar()
            search_lbl=Label(right_frame,text="Search",font=("arial",13,'bold'))
            search_lbl.place(relx=.465,rely=.09)
            search_entry=Entry(right_frame,font=("arial",13,'bold'),textvariable=search_var)
            search_entry.pack(pady=20)
            
            search_entry.focus()
            search_entry.bind("<KeyRelease>",lambda e:filter_history())
            search_entry.bind("<FocusIn>",lambda e:search_entry.delete(0,END))
            
            
            style=ttk.Style()
            style.configure("Treeview",font=("varennes", 11))
            style.configure("Treeview.Heading",font=("Arial", 13,'bold'))
            
            
            
            
            column=("Date","Ref-No.","Mode","Amount","Description")
            
            history_treeview=ttk.Treeview(right_frame,columns=column,show="headings")
            
            # --inserting data to treeview ---
            for col in column:
                
                history_treeview.heading(col,text=col)
                if col=="Description":
                    history_treeview.column(col,anchor="center",width=200)
                elif col=="Amount":
                    history_treeview.column(col,anchor="s",width=100)
                else:
                    history_treeview.column(col,anchor="center",width=100)
            
            history_treeview.pack(fill="both",expand=True)
            
            def filter_history():# --filter data and show histroy according to search--
                search=search_var.get().strip().lower()
                filterd_data=[]
                if not search:
                    update_treeview(history_data)
                    return
                for record in history_data:
                    ac_no,ref,mode,amount,desc,date=record
                    row=f"{ref} {mode} {amount} {desc} {date}".lower()
                    if search in row:
                        filterd_data.append(record)
                update_treeview(filterd_data)
            # --update treeview according to  search--
            def update_treeview(data):
                for item in history_treeview.get_children():
                    history_treeview.delete(item) 
                    
                for record in data:
                    ac_no,ref,mode,amount,desc,date=record
                    amt_display=f"+ {amount}" if mode=="Credit" else f"- {amount}"
                    
                    history_treeview.insert("",END,values=(date,ref,mode,amt_display,desc))
        
            update_treeview(history_data)   
            
        # --this functio get response from user and logout his profile ,back to home--
        def logout():
            agre=messagebox.askyesno("Logout","Do You Want to Logout?")
            if not agre:
                return
            self.clear_frame_child_win()
            self.main_win()
          
        
            
        wlcm_lbl=Label(self.frm,text=f"Welcome, {name}",font=("arial",14,'bold'),fg="green")
        wlcm_lbl.place(relx=.02,rely=.02)
        left_frame=Frame(self.frm,highlightthickness=2,bd=4,highlightbackground="pink")
        left_frame.place(relx=.01,rely=.1,relwidth=.15,relheight=.83)
        
        right_frame=Frame(self.frm,highlightthickness=2,bd=4,highlightbackground="white")
        right_frame.place(relx=.2,rely=.1,relwidth=.79,relheight=.83)
        
        lbl=Label(right_frame,text="This is Home Screen",font=("arial",13,'bold'),fg="green")
        lbl.pack()
        
        def change_profile_pic():
            filetype=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.webp")]
            img_path=filedialog.askopenfilename(title="Choose Photo",filetypes=filetype)
            if not img_path:
                return
           #  Copy the file correctly (src -> dest)
            shutil.copyfile(img_path,f"Images/{acn}.png")
            self.bitmap_img=self.convert_bitmap(cwd_path=f"{acn}.png",size=(120,120),master=self.frm)
            self.profile_img.configure(image=self.bitmap_img)
        
        if os.path.exists(f"Images/{acn}.png"):
            profile_img=f"{acn}.png"
        else:
            profile_img="default img.jpg"
            
        self.profile_pic_bitmap=self.convert_bitmap(cwd_path=profile_img,size=(120,120),master=self.frm)
        
        self.profile_img=Label(left_frame,image=self.profile_pic_bitmap)
        self.profile_img.grid(row=0,column=0,padx=26,sticky=W)
        
        #self.image_load(default_img)
        self.update_pic_icon=self.convert_bitmap(cwd_path="update pic icon.webp",size=(20,20),master=left_frame)
        # ======this button change profile picture=======
        change_profile_pic_btn=Button(left_frame,image=self.update_pic_icon,command=change_profile_pic,bd=-1)
        change_profile_pic_btn.grid(row=1,column=0,sticky=W,padx=80,pady=2)
        
        ac_details_btn=Button(left_frame,text="Details",font=("arial",14,'bold'),width=14,bg="blue",fg="white",command=details)
        ac_details_btn.grid(row=2,column=0,sticky=W)
        
        update_btn=Button(left_frame,text="Update",font=("arial",14,'bold'),width=14,bg="blue",fg="white",command=update)
        update_btn.grid(row=3,column=0,sticky=W,pady=5)
        
        withdraw_btn=Button(left_frame,text="Withdraw",font=("arial",14,'bold'),width=14,bg="blue",fg="white",command=withdraw)
        withdraw_btn.grid(row=4,column=0,sticky=W)
        
        transfer_btn=Button(left_frame,text="Transfer",font=("arial",14,'bold'),width=14,bg="blue",fg="white",command=transfer)
        transfer_btn.grid(row=5,column=0,sticky=W,pady=5)
        
        history_btn=Button(left_frame,text="History",font=("arial",14,'bold'),width=14,bg="blue",fg="white",command=history)
        history_btn.grid(row=6,column=0,sticky=W)
        
        logout_btn=Button(left_frame,text="Logout",font=("arial",14,'bold'),width=14,bg="blue",fg="white",command=logout)
        logout_btn.grid(row=7,column=0,sticky=W,pady=5)

# ==this function auto generate random password for new user ======
    def auto_generate_pw(self):
        store_pw=[]
        for i in range(3):
            char=chr(random.randint(65,90))
            store_pw.append(char)
            num=random.randint(0,9)
            store_pw.append(str(num))
        random.shuffle(store_pw)
        join_pw=" ".join(store_pw)
        final_pasword=join_pw.replace(" ","")
        return final_pasword

#  ==this function provides open new account for random users==
    def open_account_by_user(self):
        # messagebox.showinfo("Feature","This feature coming soon!")
        # return
        self.clear_frame_child_win()
        # =================welcome new user label==============
        self.user_border=Frame(self.frm,bd=5,relief="ridge")
        self.user_border.place(relx=.018,rely=.2,relheight=.79,relwidth=.965)
        Label(self.frm,text="Create Your Own Account",font=("",14,'bold'),fg="green").pack(pady=35) 
        self.open_account_by_admin(frame=self.user_border)
    
# ===this function destroy welcome frame or hide details frame ==
    def clear_welcome_frame(self):
        self.welcome_lbl_frame.destroy()
        self.login_close_btn_frm.destroy()
        self.welcome_title.destroy()

#  ==this function provides open new account for random users from admin==

    def open_account_by_admin(self,*,frame=None):
        
        self.border=frame
    # ============this function reset all entry box and clear box empty===========
        def reset_entry_box():
            #self.name_entry.focus()
            self.gender.set("Select")
            self.ac_type.set("Select")
            pan_entry.config(state="normal")
            entry_boxes=(self.name,self.dob,self.mob,self.email,self.aadhaar,self.pan)
            for entry_box in entry_boxes:
                entry_box.set("")
    # =====this function create a text box and show details after submit,like A/C No,password=============
    
        def show_and_save_details():
            
            name=self.name.get().strip().title()
            gender=self.gender.get()
            mob=self.mob.get().strip()
            email=self.email.get().strip()
            aadhaar=self.aadhaar.get().strip()
            pan=self.pan.get().strip()
            ac_type=self.ac_type.get()
            password=self.auto_generate_pw()
            
            
            if not mob_pattern.fullmatch(mob):
                messagebox.showerror("opening Account","Enter Valid Mobile Number!")
                return
            elif not email_pattern.fullmatch(email):
                messagebox.showerror("opening Account","Enter Valid Email!")
                return
            elif not aadhaar_pattern.fullmatch(aadhaar):
                messagebox.showerror("opening Account","Enter Valid Aadhaar No.!")
                return
            elif pan!="Unverified!" and not pan_pattern.fullmatch(pan):
                messagebox.showerror("opening Account","Enter Valid Pan No.!")
                return
            
            entry_boxes=(self.name,self.gender,self.dob,self.mob,self.email,self.aadhaar,self.pan,self.ac_type)
            for box in entry_boxes:
                if box.get()=="":
                    messagebox.showerror("opening Account","All Fields are required!")
                    return
            if self.gender.get()=="Select":
                messagebox.showerror("opening Account","Select Gender!")
                return
            elif self.ac_type.get()=="Select":
                messagebox.showerror("opening Account","Select Account Type!")
                return    
            try:
                dob_format=self.dob.get().replace("/","-")
                dob_format2=datetime.strptime(dob_format,"%d-%m-%Y")
                dob=dob_format2.strftime("%Y-%m-%d")
            except Exception as e:
                messagebox.showwarning("Error",f"Invailid Date\n{e}")
                return
            # ===this label frame congrats new user and show details after create account like name,A/C No.,password
            agre=messagebox.askyesno("Opening Account","Have you filled out the form correctly?")
            if not agre :
                return
            self.wait_title=Label(self.border,text="Verifying Details.................",font=("",13,'bold'),width=50) #title for frame
            self.wait_title.place(relx=.55,rely=.01)
            self.border.update()
            
            if not self.check_internet():
                self.wait_title.destroy()
                messagebox.showerror("Opening Account","No Internet!")
                return
    
            
            
            bank_database=self.connect_database()
            cursor=bank_database.cursor()
            cursor.execute("select * from user where Aadhaar=?",(aadhaar,))
            verify_aadhaar=cursor.fetchone()
            if verify_aadhaar:
                self.wait_title.configure(text="Customer has already opened an account!",fg="red")
                messagebox.showwarning("Opening Account","Already Exists!!")
                self.wait_title.destroy()
                bank_database.close()
                return
            
            cursor.execute("""insert into user(password,name,gender,dob,mob_no,email,aadhaar,pan,ac_type) values
                           (?,?,?,?,?,?,?,?,?)""",(password,name,gender,dob,mob,email,aadhaar,pan,ac_type))
            bank_database.commit()
            cursor.execute("select ac_number,ifsc from user order by opened_date desc limit 1")
            
            ac_number,ifsc=cursor.fetchone()
            
            ac_opening_msg=mail_messages.ac_opening_msg(name=name,acn=ac_number,ac_type=ac_type,password=password,ifsc=ifsc)
            try:
                self.send_mail(user_mail=email,subject="Account Opening",message=ac_opening_msg)
            except Exception as e:
                self.wait_title.destroy()
                cursor.execute("delete from user where ac_number=?",(ac_number,))
                bank_database.commit()
                messagebox.showerror("send Email",f"Send mail Error can't open Account!\n\n{e}")
                self.open_account_by_admin(frame=self.border)
                return
            
            show_message=f"""\nCongratulations! Your account has been opened.\n
Name     \t\t: {name} 
A/C No.  \t\t: {ac_number} 
Password \t\t: ******
Date     \t\t: {time.strftime("%d-%B-%Y")}
\n\nYour password has been sent to your email. Please check."""

            bank_database.close()
            self.open_account_by_admin(frame=self.border)
            
            self.wait_title.destroy()
            self.welcome_title=Label(self.border,text="Welcome! Your Account is Ready",font=("",12,'bold')) #title for frame
            self.welcome_title.place(relx=.55,rely=.01)
        
            self.welcome_lbl_frame=LabelFrame(self.border,relief=RIDGE,bd=2) 
            self.welcome_lbl_frame.place(relx=.55,rely=.07,relheight=.75,relwidth=.4) 
            
            # =========this label frame for  close,login============
            self.login_close_btn_frm=LabelFrame(self.border,relief=RIDGE)
            self.login_close_btn_frm.place(relx=.55,rely=.82,relheight=.08,relwidth=.4)
            
# ==this text frame show details after opened account===
            txt_frame_box=Text(self.welcome_lbl_frame,font=("",13))
            txt_frame_box.place(relx=0,rely=0,relheight=.999,relwidth=.999)
            txt_frame_box.delete("1.0",END)
            
            txt_frame_box.insert(END,show_message)
            txt_frame_box.config(state="disabled")
            
                # =====this button to close welcome frame /close details ==
            close_btn=Button(self.login_close_btn_frm,text="Close",width=25,bg="green",fg="white",font=("arial",13,'bold'),command=self.clear_welcome_frame)
            close_btn.grid(row=0,column=0)
            
            # this button redirect to login screen===
            login_btn=Button(self.login_close_btn_frm,text="login",width=25,bg="green",fg="white",font=("arial",13,'bold'),command=self.main_win)
            login_btn.grid(row=0,column=1)
            reset_entry_box()
        
        # -this function confirm user has pan card or No--
        def pan_confirm():
            pan_conf=messagebox.askyesno("Account Opening","Do You have Pan Card?")
            if not pan_conf:
                self.pan.set("Unverified!")
                ac_type_entry.focus()
                pan_entry.config(state="disabled")
            else:
                pan_entry.focus()
                pan_entry.bind("<Return>",lambda e:ac_type_entry.focus_set())
    # custmer detail form=
        # ====this label indicate to form title======
        form_title=Label(self.border,text="Customer Details Form",font=("",12,'bold'))
        form_title.place(relx=.06,rely=.01)
        # ==============this is  label frame for entry all Details from user in child frame============
        entry_lbl_frame=LabelFrame(self.border,relief=RIDGE,bd=2) 
        entry_lbl_frame.place(relx=.06,rely=.07,relheight=.75,relwidth=.4) 
            
        # =========this label frame for  back,submit ,reset button============
        btn_frm=LabelFrame(self.border,relief=RIDGE)
        btn_frm.place(relx=.06,rely=.82,relheight=.08,relwidth=.4)
        
        # ==this varible store padx all label=================
        lbl_padx=50
        # ======this variable store font for all entry box============
        entry_box_font=('arail',12,'bold')
        # ======this variable store font size for all label==============
        lbl_font=('arail',12,'bold')
        
        # ====This is input name froma user and display label============================
        name_lbl=Label(entry_lbl_frame,text="Name:",padx=lbl_padx,pady=10,font=lbl_font)
        name_lbl.grid(row=0,column=0,sticky=W)
        self.name_entry=Entry(entry_lbl_frame,font=entry_box_font,textvariable=self.name)
        self.name_entry.grid(row=0,column=1,sticky=W)
        self.name_entry.focus()

        # =======this to select gender from user and display label=============
        gender_lbl=Label(entry_lbl_frame,text="Gender:",padx=lbl_padx,font=lbl_font)
        gender_lbl.grid(row=1,column=0,sticky=W)
        gender_entry=ttk.Combobox(entry_lbl_frame,state="readonly",values=("Male","Female","Others"),width=18,font=entry_box_font,textvariable=self.gender)
        gender_entry.set("Select")
        #gender_entry["values"]=("Male","Female")
        gender_entry.grid(row=1,column=1,sticky=W)
        
        # ============this line for input date of birth from user and display label==============
        dob_lbl=Label(entry_lbl_frame,text="DOB:",padx=lbl_padx,pady=10,font=lbl_font)
        dob_lbl.grid(row=2,column=0,sticky=W)
        dob_entry=Entry(entry_lbl_frame,font=entry_box_font,textvariable=self.dob)
        dob_entry.grid(row=2,column=1,sticky=W) 
        # ============this line for input mobile no. from user and display label==============
        mob_lbl=Label(entry_lbl_frame,text="Mob/No:",padx=lbl_padx,font=lbl_font)
        mob_lbl.grid(row=3,column=0,sticky=W)
        mob_entry=Entry(entry_lbl_frame,font=entry_box_font,textvariable=self.mob)
        mob_entry.grid(row=3,column=1,sticky=W)
        
        # ============this line for input Email from user and display label==============
        email_lbl=Label(entry_lbl_frame,text="Email:",padx=lbl_padx,pady=10,font=lbl_font)
        email_lbl.grid(row=4,column=0,sticky=W)
        email_entry=Entry(entry_lbl_frame,font=entry_box_font,textvariable=self.email)
        email_entry.grid(row=4,column=1,sticky=W)
        
        # ============this line for input Aadhaar No. from user and display label==============
        adhar_lbl=Label(entry_lbl_frame,text="Aadhaar:",padx=lbl_padx,font=lbl_font)
        adhar_lbl.grid(row=5,column=0,sticky=W)
        adhar_entry=Entry(entry_lbl_frame,font=entry_box_font,textvariable=self.aadhaar)
        adhar_entry.grid(row=5,column=1,sticky=W)
        
        
        # ============this line for input pan no. from user and display label==============
        pan_lbl=Label(entry_lbl_frame,text="Pan:",padx=lbl_padx,pady=10,font=lbl_font)
        pan_lbl.grid(row=6,column=0,sticky=W)
        pan_entry=Entry(entry_lbl_frame,font=entry_box_font,textvariable=self.pan)
        pan_entry.grid(row=6,column=1,sticky=W)
        
        
        # ======this for select account type from user and display label=========
        ac_type_lbl=Label(entry_lbl_frame,text="A/C Type:",padx=lbl_padx,font=lbl_font)
        ac_type_lbl.grid(row=7,column=0,sticky=W)
        ac_type_entry=ttk.Combobox(entry_lbl_frame,state="readonly",values=("Saving","Current"),width=18,font=entry_box_font,textvariable=self.ac_type)
        ac_type_entry.set("Select")
        #ac_type_entry["values"]=("Saving","Current")
        ac_type_entry.grid(row=7,column=1,sticky=W)
        
        ac_type_entry.bind("<Return>",lambda e:show_and_save_details())
        
        # ======this variable store button width for back button,reset,submit button=======
        btn_width=16
        # ======this button work as back home screen========
        back_btn=Button(btn_frm,text="Back",font=('arial',13,'bold'),bg="green",fg="white",width=btn_width,command=self.main_win)
        back_btn.grid(row=0,column=0)
        
        # ========this button clear all entry box =======
        reset_btn=Button(btn_frm,text="reset",font=("arial",13,'bold'),bg="green",fg="white",width=btn_width,command=reset_entry_box)
        reset_btn.grid(row=0,column=1)
        
        # ====this button to store details in database========
        submit_btn=Button(btn_frm,text="Submit",font=("arial",13,'bold'),bg="green",fg="white",width=btn_width,command=show_and_save_details)
        submit_btn.grid(row=0,column=2)
        
        bind1=[self.name_entry,gender_entry,dob_entry,mob_entry,email_entry]
        for widget in bind1:
            widget.bind("<Return>",self.focus_next_widgets)
            
        adhar_entry.bind("<Return>",lambda e:pan_confirm())
        
# end form details code=
root=Tk()
bank=Bank(root)
root.mainloop()
