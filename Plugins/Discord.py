from Notifications import Notifications
from Config import Config
import time


class Discord():

	# Initialize Module
	# Pre-Condition: Streamer Dict. Has Been Generated and Discord Module Has Been Enabled in Config File
	def init(streamer_dict):

		# Incorperate Discord Into Notifications Module
		Notifications.discord = Discord.discord
		Notifications.DISCORD = 3

		# Parse Global Settings
		Notifications.DISCORD_GLOBAL_SETTINGS = Config.parse_preferences("GLOBAL", "Discord")

		# Generate Streamer Settings
		for user in streamer_dict:

			streamer_dict[user].module_preferences["Discord"] = Config.parse_preferences(user, "Discord")
			streamer_dict[user].module_last_change["Discord"] = 0



	# Generate a Discord Notification
	# Pre-Condition: An Alert Has Been Generated
	# Post-Condition: A Valid Notification Payload Has Been Sent to Notifications.send()
	async def discord(streamer_obj, message):

		# Don't Send Messages That the User Doesn't Want
		if not Notifications.preference_resolver("Alerts", message, Notifications.DISCORD_GLOBAL_SETTINGS, streamer_obj.module_preferences["Discord"]):
			return

		# Check & Reset the Soon Cooldown if Needed
		elif message == "title" or message == "game":

			cooldown = Notifications.DISCORD_GLOBAL_SETTINGS["Soon Cooldown"]
			if time.time() > streamer_obj.module_last_change["Discord"] + cooldown:
				streamer_obj.module_last_change["Discord"] = time.time()
			else:
				return

		# Resolve User Preferences
		preferences = {}
		for keyword in ("Discord ID", "Message Text", "Webhook URL", "Bot Username", "Avatar URL"):
			preferences[keyword] = Notifications.preference_resolver(keyword, message, Notifications.DISCORD_GLOBAL_SETTINGS, streamer_obj.module_preferences["Discord"])

		# Format Message and Bot Username 
		for pref in ("Discord ID", "Message Text", "Webhook URL", "Bot Username", "Avatar URL"):
			if preferences[pref] != None:
				preferences[pref] = Notifications.special_format(
					str(preferences[pref]),

					name  = streamer_obj.name,
					title = streamer_obj.last_title,
					game  = streamer_obj.last_game,
					message = str(message),
					discord_id = "[Null ID]" if preferences["Discord ID"] == None else preferences["Discord ID"]
				)

		# Construct Body
		data = {}
		data["content"] = preferences["Message Text"]
			
		if preferences["Bot Username"] != None: data["username"]   = preferences["Bot Username"]
		if preferences["Avatar URL"]   != None: data["avatar_url"] = preferences["Avatar URL"]
			
		# Send Message to Discord
		await Notifications.send(preferences["Webhook URL"], Notifications.DISCORD, data)
