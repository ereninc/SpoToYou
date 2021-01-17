'''
Using Spotipy to make calls to the Spotify Web API.
Control variables - [All are either global or in main()]
	* CLI_ID and CLI_KEY	(string)
	* overwrite 			(boolean)
	* mode 					(string)
	* playlist 				(list of strings)
'''

import spotipy
import spotipy.oauth2 as oauth2
import os


# client ID and secret key to authorize querying of spotify data through the API
CLI_ID 	= 'beb0c3e0dd5c4e1f87292d36f4892b32'
CLI_KEY = '81d9a2c660274df5b22c3191e321f49a'

# whether you want to overwrite existing files or not
OVERWRITE = True

def main():
	global spotify
	# Choose whether you want to export playlist to a txt file, csv file or if you just want to view the playlist data structure or get a random song.
	modes = ["txt", "nan"]
	mode = modes[0]

	# dictionary of playlists with their IDs and owner IDs
	playlists_info = { "while Coding" : ["3wTv5UvNA0Cuu5juX3r2G0", "11135497545"]}
	playlist = playlists_info['while Coding']

	# step 1 - get the token to get authorized by the spotify API
	token = get_token()
	spotify = spotipy.Spotify(auth=token)

	# write playlist contents to file and other playlist-operations
	write_playlist(playlist[1], playlist[0], mode)


def get_token():
	'''
	Your client ID and client secret key are used to get a token.
	If both your credentials were legitimate, you will get and return a valid token.
	'''
	credentials = oauth2.SpotifyClientCredentials(
		client_id = CLI_ID,
		client_secret = CLI_KEY)
	token = credentials.get_access_token()
	return token


def write_playlist(username, uri, mode):
	'''
	Query the spotify API and receive the playlist information. If mode is 'nan' you can view this information data structure in its raw form.
	Obtain the list of tracks from the playlist information data structure and write it to a txt or csv file.
	Select a random song from the list of tracks and print general information to the console.
	'''
	playlist_info = spotify.user_playlist(username, uri) 						#, fields='tracks,next,name'
	tracks = playlist_info['tracks']
	if mode == 'txt':
		filename = "{0}.txt".format(playlist_info['name'])
		old_total = write_txt(username, filename, tracks)
	elif mode == 'nan':
		pass
	"""
	# print randomly selected song!
	song = random.choice(tracks['items'])
	print("Number of tracks = {} --> {} ".format(old_total, tracks['total']))
	print("Randomly selected song for you - {0} by {1}\n".format(song['track']['name'], song['track']['artists'][0]['name']))
	"""



def write_txt(username, filename, tracks):
	'''
	ADD TO TXT FILE
	View the playlist information data structure if this is confusing!
	Specify the destination file path and check if the file exists already. If the file exists and you selected to not overwrite, the program will end here.
	Open the file and read the contents of the file to get the number of songs that are already recorded.
	Seek the file pointer back to the beginning and overwrite the file contents with the track information as required.
	Finally, truncate any extra bytes of the file, if the overwritten portion is less than the original portion.
	Return the original number of songs to the calling function.
	Exceptions handle the cases where the characters in the track info cannot be understood by the system and where the key is invalid (usually due to local files in the playlist).
	'''
	filepath = "C:\\Users\\ASUS\\Desktop\\SpoToYou\\{0}".format(filename)
	if os.path.isfile(filepath):
		print("File already exists!")
		ex = True
		filemode = 'r+'
		if not OVERWRITE:
			return
		else:
			print("Rewriting...")
	else:
		ex = False
		filemode = 'w'
	with open(filepath, filemode) as file:
		# reading number of songs from the file if it exists
		if ex:
			content = file.readlines()
			curr_tot = content[-2][14:]
			curr_tot = curr_tot.strip() 						# to remove the trailing newline character
			file.seek(0)
		else:
			curr_tot = None
		# write new songs to the file
		while True:
			for item in tracks['items']:
				if 'track' in item:
					track = item['track']
				else:
					track = item
				try:
					track_url = track['external_urls']['spotify']
					file.write("{0:<60} - {1:<90} - {2} \n".format(track_url, track['name'], track['artists'][0]['name']))
				except KeyError:
					print("Skipping track (LOCAL FILE) - {0} by {1}".format(track['name'], track['artists'][0]['name']))
				except UnicodeEncodeError:
					print("Skipping track (UNDEFINED CHARACTERS) - {0} by {1}".format(track['name'], track['artists'][0]['name']))
			# 1 page = 50 results
			# check if there are more pages
			if tracks['next']:
				tracks = spotify.next(tracks)
			else:
				break
		#file.write("\n\nTotal Songs - {0}\nUser - {1}".format(tracks['total'], username))
		file.truncate()
	print("Playlist written to file.", end="\n\n")
	print("-----\t\t\t-----\t\t\t-----\n")
	return curr_tot

if __name__ == "__main__":
	main()