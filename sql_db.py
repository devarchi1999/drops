import sqlite3

class SqlDb:
    def create_connect_db(self):
        # to create a database if the db is not there or to connect to an existing db
        conn = sqlite3.connect('userPlaylist.db')
        # to fetch, update, delete records in the database
        cur = conn.cursor()

        cur.execute('''
               create table if not exists registerTable (
               username text,
               email text,
               password text,
               confirmPassword text,
               playlistName text
               )
               ''')
        cur.execute('''
        create table if not exists playlistTable (
        playlistName text,
        songName text,
        songUrl text
        )
        ''')


        # commit changes
        conn.commit()
        # close connection
        conn.close()
        return 1

    def submit_db_data(self,t_username,t_email,t_password,t_confirm_password,t_playlist_name):


        conn = sqlite3.connect('userPlaylist.db')
        cur = conn.cursor()

        cur.execute(
            "insert into registerTable values (:t_username,:t_email,:t_password,:t_confirm_password,:t_playlist_name)",
        {
            't_username': t_username,
            't_email':t_email,
            't_password': t_password,
            't_confirm_password':t_confirm_password,
            't_playlist_name':t_playlist_name
        }
        )
        # cur.execute(
        #     "inset into playlistTable values (:t_playlist_name,:t_song_name,:t_song_url)",
        #     {
        #         't_playlist_name': t_playlist_name,
        #         't_song_name':t_song_name,
        #         't_song_url':t_song_url
        #     }
        # )
        conn.commit()
        conn.close()
        return 1

    def login_validation_email(self,email,password):
        conn = sqlite3.connect('userPlaylist.db')
        cur = conn.cursor()

        cur.execute('''
                select username from registerTable where email=? and not password=?''', (email, password))

        result = cur.fetchall()
        conn.commit()
        conn.close()
        return result


    def login_validation(self,email,password):
        conn  = sqlite3.connect('userPlaylist.db')
        cur = conn.cursor()

        cur.execute('''
        select username from registerTable where email=? and password=?''',(email,password))

        result = cur.fetchall()
        conn.commit()
        conn.close()
        return result

    def already_user(self,email):
        conn = sqlite3.connect('userPlaylist.db')
        cur = conn.cursor()

        cur.execute('''
                select username from registerTable where email=?
                ''', (email,))

        result = cur.fetchall()
        conn.commit()
        conn.close()
        return result


    def fetch_test(self):
        conn = sqlite3.connect('userPlaylist.db')
        cur = conn.cursor()

        cur.execute("select * from registerTable")
        result = cur.fetchall()


        conn.commit()
        conn.close()

        return result