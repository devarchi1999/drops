from tkinter import *
from tkinter import messagebox
# from tkinter.ttk import *
from PIL import ImageTk, Image
import response
import create_ss
import media_m
import request_maker
import displaySearchResults
import validate_login_details
import validate_register_details
import sql_db
import validate_login_details
import math


request = None
video_desp = None
id_list = None

video_name_list = []
options_box=None
l = None
player = None
new_frame2_in_3=None
select_song_list = None
# functions required by the buttons

def return_login_layout():
    global frame2_in_3
    global new_frame2_in_3
    new_frame2_in_3.grid_remove()
    frame2_in_3.grid()

    global return_button
    return_button.config(state=DISABLED)

def add_song_func():
    global options_box
    global select_song_list
    global video_name_list
    song_list = []
    if options_box.curselection()!=():
        song_list.append(options_box.get(options_box.curselection()))
    for id,song in enumerate(song_list):
        select_song_list.insert(id,song)

        for item in song_list:
            print(item)



def add_playlist_func():
    global new_frame2_in_3
    global select_song_list
    frame_dict = new_frame2_in_3.grid_info()
    new_frame2_in_3.grid_remove()
    playlist_frame2_in_3 = Frame(frame3, highlightbackground='blue', highlightthickness=1)
    playlist_frame2_in_3.grid(row=frame_dict['row'], column=frame_dict['column'], columnspan=frame_dict['columnspan'],
                         rowspan=frame_dict['rowspan'], sticky=frame_dict['sticky'])
    playlist_frame2_in_3.columnconfigure(0,weight=5)
    playlist_frame2_in_3.columnconfigure(1, weight=1)
    # playlist_frame2_in_3.rowconfigure(0, weight=1)

    add_playlist_entry = Entry(playlist_frame2_in_3)
    add_playlist_entry.grid(row=0,column=0,sticky='ew',padx=2,pady=2)

    add_playlist_button = Button(playlist_frame2_in_3,text='Add',fg='blue')
    add_playlist_button.grid(row=0,column=1,sticky='ew',padx=2,pady=2)

    add_song_label = Label(playlist_frame2_in_3, text='')
    add_song_label.grid(row=1, column=0, sticky='ew', padx=5, pady=5)

    add_song_label = Label(playlist_frame2_in_3,text='Songs',font='ComicSans 16 bold')
    add_song_label.grid(row=2,column=0,sticky='ew',padx=2,pady=2)

    select_song_list = Listbox(playlist_frame2_in_3,selectmode=MULTIPLE)
    select_song_list.grid(row=3,column=0,sticky='nsew',padx=2,pady=2)

    add_song_button = Button(playlist_frame2_in_3, text='Add Song', fg='blue',command=add_song_func)
    add_song_button.grid(row=4, column=0, sticky='nw', padx=2, pady=5,ipadx=5)


def create_playlist_screen():
    global frame2_in_3
    global new_frame2_in_3
    frame_dict = frame2_in_3.grid_info()
    frame2_in_3.grid_remove()
    new_frame2_in_3=Frame(frame3,highlightbackground='blue',highlightthickness=1)
    new_frame2_in_3.grid(row=frame_dict['row'],column=frame_dict['column'],columnspan=frame_dict['columnspan'],rowspan=frame_dict['rowspan'],sticky=frame_dict['sticky'])
    new_frame2_in_3.columnconfigure(0,weight=1)
    new_frame2_in_3.columnconfigure(1, weight=1)
    new_frame2_in_3.rowconfigure(0, weight=1)

    add_button = Button(new_frame2_in_3,text='Add',command=add_playlist_func)
    add_button.grid(row=0,column=0,pady=1,padx=5,ipadx=5,sticky='ew')
    play_playlist_button = Button(new_frame2_in_3, text='Play')
    play_playlist_button.grid(row=0, column=1, pady=1, padx=5,ipadx=5,sticky='ew')


def login_details_func(email,password):
    sql = sql_db.SqlDb()
    ob = validate_login_details.ValidateLoginDetails()
    val = ob.validate(email,password)
    if val==0:
        messagebox.showwarning('Warning!','Please enter correct email-id.')
    elif val==1:
        messagebox.showwarning('Warning!', 'Password should be greater than 6 digits.')
    elif val==2:
        if sql.login_validation_email(email, password) != []:
            # here write the new logged in page in tkinter and the page functionality
            messagebox.showwarning('Wrong Password','Please try again')
        elif sql.login_validation(email,password)!=[]:
            messagebox.showinfo('Congrats', 'You have successfully logged in.')
            print(sql.fetch_test())
            global return_button
            return_button.config(state=ACTIVE,command=return_login_layout)
            create_playlist_screen()

        else:
            messagebox.showwarning('Not Found', 'Please register your account.')



def register_details_func(email,password,confirm_password,username,playlist):
    ob = validate_register_details.ValidateRegisterDetails()
    val = ob.validate(email, password,confirm_password,username,playlist)
    if val == -2:
        messagebox.showwarning('Warning!', 'Please enter a username.')
    elif val == -1:
        messagebox.showwarning('Warning!', 'Email id not given in proper format.')
    elif val == 0:
        messagebox.showwarning('Warning!', 'Length of password should be greater than 6.')
    elif val == 1:
        messagebox.showwarning('Warning!', 'Password and Confirm Password should match.')
    elif val == 2:
        messagebox.showwarning('Warning!', 'Enter a playlist name to store songs.')
    else:
        sql = sql_db.SqlDb()
        if sql.create_connect_db()==1:
            if sql.already_user(email)!=[]:
                messagebox.showinfo('Registered User', 'Already registered. Please login.')
                print(sql.fetch_test())

            else:
                if sql.submit_db_data(username,email,password,confirm_password,playlist):
                    messagebox.showinfo('Thanks', 'Successfully Registered.')
                    global return_button
                    return_button.config(state=ACTIVE, command=return_login_layout)
                    create_playlist_screen()



def pause_stop_func(toggle):
    if toggle==1:
        player.pause()
    if toggle==2:
        player.stop()

def Create_Search_String():
    global options_box
    if options_box.curselection()!=():
        video_name = options_box.get(options_box.curselection())
        css = create_ss.Create_Search_String()
        mm = media_m.Media_Maker()
        global player
        player = mm.media_maker(css.create_search_string(video_name,video_desp))
        player.play()
        global pause_button
        global stop_button
        pause_button.config(state=ACTIVE,command = lambda : pause_stop_func(1))
        stop_button.config(state=ACTIVE, command = lambda : pause_stop_func(2))



def display_Results(video_desp,id_list):
    dr = displaySearchResults.DisplayResults()
    global video_name_list
    video_name_list = dr.display_results(video_desp,id_list)
    global options_box


    options_box = Listbox(frame3_in_2,selectmode = SINGLE)
    options_box.grid(row=0, column=0, sticky='nsew', padx=2)



    for item, option in enumerate(video_name_list):
        options_box.insert(item, option[0])


def Response(req):
    re = response.Response()
    global video_desp,id_list
    video_desp,id_list = re.response_func(req)
    display_Results(video_desp,id_list)



def Search(search):
    rm = request_maker.Request_Maker()
    global request
    request = rm.search_song(search)
    Response(request)



#initial window setup
root = Tk()
root.title('drops')
p = ImageTk.PhotoImage(file='tubedesk_icon.png')
root.iconphoto(False,p)
root.geometry('600x500')
root.grid_columnconfigure(0,weight=1)
root.grid_columnconfigure(1,weight=1)
root.grid_rowconfigure(1,weight=1)

# resizing the banner according to the size of the window
# def resizer(e):
#     global image,resized_image,banner
#     image = Image.open('drops_banner2.png')
#     resized_image = image.resize((int(e.width),int(e.height)),Image.ANTIALIAS)
#     banner = ImageTk.PhotoImage(resized_image)
#     canva.create_image(0, 0, image=banner, anchor='nw')
#
# # initial banner setup
# banner_path = 'drops_banner2.png'
# banner = ImageTk.PhotoImage(Image.open(banner_path))


# new banner placement
# canva = Canvas(root,width=600,height=100)
# canva.grid(row=0,column=0,columnspan=2,sticky=N+S+E+W)
# canva.create_image(0,0,image = banner,anchor='nw')

# creating all the other frames that are needed to make the login and search forms
# frame 2 configuration
frame2 = Frame(root,highlightbackground='red',highlightthickness=3)
frame2.grid(row=1,column=0,pady=2,sticky=N+S+E+W)
frame2.grid_columnconfigure(0,weight=1)
frame2.grid_rowconfigure(0,weight=0)
frame2.grid_rowconfigure(1,weight=1)
frame2.grid_rowconfigure(2,weight=5)

# frame 3 configuration
frame3 = Frame(root,highlightbackground='blue',highlightthickness=3)
frame3.grid(row=1,column=1,pady=2,sticky=N+S+E+W)
frame3.grid_columnconfigure(0,weight=1)
frame3.grid_rowconfigure(0,weight=1)
frame3.grid_rowconfigure(1,weight=3)
frame3.grid_rowconfigure(2,weight=3)

# frames configuration inside frame 2
frame1_in_2 = Frame(frame2,highlightbackground='blue',highlightthickness=1)
frame1_in_2.grid(row=0,column=0,sticky=N+S+E+W)
frame1_in_2.columnconfigure(0,weight=1)

frame2_in_2 = Frame(frame2,highlightbackground='blue',highlightthickness=1)
frame2_in_2.grid(row=1,column=0,sticky=N+S+E+W)
frame2_in_2.columnconfigure(0,weight=2)
frame2_in_2.columnconfigure(1,weight=1)
frame2_in_2.rowconfigure(0,weight=1)

frame3_in_2 = Frame(frame2,highlightbackground='blue',highlightthickness=1)
frame3_in_2.grid(row=2,column=0,sticky=N+S+E+W)
frame3_in_2.columnconfigure(0,weight=1)
frame3_in_2.rowconfigure(0,weight=1)


# frames configuration inside frame 3

# frame 1 inside frame 3
frame1_in_3 = Frame(frame3,highlightbackground='blue',highlightthickness=1)
frame1_in_3.grid(row=0,column=0,sticky=N+S+E+W)
frame1_in_3.columnconfigure(0,weight=1)
frame1_in_3.columnconfigure(1,weight=1)
frame1_in_3.columnconfigure(2,weight=1)
frame1_in_3.rowconfigure(0,weight=1)

# frame 2 inside frame 3
frame2_in_3 = Frame(frame3,highlightbackground='blue',highlightthickness=1)
frame2_in_3.grid(row=1,column=0,sticky=N+S+E+W)
frame2_in_3.columnconfigure(0,weight=1)
frame2_in_3.columnconfigure(1,weight=3)

# frame 3 inside frame 3
frame3_in_3 = Frame(frame3,highlightbackground='blue',highlightthickness=1)
frame3_in_3.grid(row=2,column=0,sticky=N+S+E+W)
frame3_in_3.columnconfigure(0,weight=1)
frame3_in_3.rowconfigure(0,weight=1)



# Search label inside frame1_in_2
search_label = Label(frame1_in_2,text='Search Songs Here',fg='black',font='ComicSans 20 bold')
search_label.grid(row=0,column=0)


# Search bar and search button inside frame2_in_2
search_bar = Entry(frame2_in_2,width=35)
search_bar.grid(row=0,column=0,sticky='ew',padx=2)


search_button = Button(frame2_in_2,text='Search',command = lambda : Search(search_bar))
search_button.grid(row=0,column=1,sticky='ew',padx=2)

# play, pause and stop button creation in frame_1_in_3
play_button = Button(frame1_in_3,text='Play',command = Create_Search_String)
play_button.grid(row=0,column=0,sticky='ew',padx=2)
pause_button = Button(frame1_in_3,text='Pause',state = DISABLED)
pause_button.grid(row=0,column=1,sticky='ew',padx=2)
stop_button = Button(frame1_in_3,text='Stop', state = DISABLED)
stop_button.grid(row=0,column=2,sticky='ew',padx=2)

# login menu creation in frame2_in_3
login_label = Label(frame2_in_3,text = 'Login to Playlist', font= 'ComicSans 10 bold', fg='black')
login_label.grid(row=0,column=0,sticky='ew',columnspan=2, pady=10)

login_email = Label(frame2_in_3,text = 'Email id *', fg='blue')
login_email.grid(row=1,column=0,sticky='ew')
login_email_entry = Entry(frame2_in_3)
login_email_entry.grid(row=1,column=1,sticky='ew',padx=7,pady=3)

login_password = Label(frame2_in_3,text = 'Password *', fg='red')
login_password.grid(row=2,column=0,sticky='ew')
login_password_entry = Entry(frame2_in_3,show='*')
login_password_entry.grid(row=2,column=1,sticky='ew',padx=7,pady=3)

login_submit_button = Button(frame2_in_3,text = 'Login',command = lambda : login_details_func(login_email_entry.get(),
                                                                                              login_password_entry.get()))
login_submit_button.grid(row=3,column=0,sticky='ew',padx=7,pady=5)



# register menu creation in frame2_in_3
register_label = Label(frame2_in_3,text = 'New User? Register here.', font= 'ComicSans 10 bold', fg='black')
register_label.grid(row=4,column=0,sticky='ew',columnspan=2,pady=10)

register_name = Label(frame2_in_3,text = 'Username *', fg='blue')
register_name.grid(row=5,column=0,sticky='ew')
register_name_entry = Entry(frame2_in_3)
register_name_entry.grid(row=5,column=1,sticky='ew',padx=7,pady=3)


register_email = Label(frame2_in_3,text = 'Email id *', fg='blue')
register_email.grid(row=6,column=0,sticky='ew')
register_email_entry = Entry(frame2_in_3)
register_email_entry.grid(row=6,column=1,sticky='ew',padx=7,pady=3)

register_password = Label(frame2_in_3,text = 'Password *', fg='red')
register_password.grid(row=7,column=0,sticky='ew')
register_password_entry = Entry(frame2_in_3,show='*')
register_password_entry.grid(row=7,column=1,sticky='ew',padx=7,pady=3)

register_confirm_password = Label(frame2_in_3,text = 'Confirm Password *', fg='red')
register_confirm_password.grid(row=8,column=0,sticky='ew')
register_confirm_password_entry = Entry(frame2_in_3,show='*')
register_confirm_password_entry.grid(row=8,column=1,sticky='ew',padx=7,pady=3)


register_playlist = Label(frame2_in_3,text = 'Add Playlist *', fg='red')
register_playlist.grid(row=9,column=0,sticky='ew')
register_playlist_entry = Entry(frame2_in_3)
register_playlist_entry.grid(row=9,column=1,sticky='ew',padx=7,pady=3)

register_submit_button = Button(frame2_in_3,
    text = 'Register',command= lambda : register_details_func(register_email_entry.get(),register_password_entry.get(),register_confirm_password_entry.get(),register_name_entry.get(),
                                                              register_playlist_entry.get()))
register_submit_button.grid(row=10,column=0,sticky='ew',padx=7,pady=5)

# creating the return to login tab in frame3_in_3
return_button = Button(frame3_in_3,text='Return to Login Menu',state=DISABLED)
return_button.grid(row=0,column=0,sticky='ew',padx=7)


# root.bind('<Configure>',resizer)
root.mainloop()