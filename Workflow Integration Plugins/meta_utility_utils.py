# Utility functions for UI Meta utility. Requires DaVinci Resolve Studio 17.4.x
# Copyright (c) 2021 Bryan Randell

from python_get_resolve import GetResolve
import time

resolve = GetResolve()

project_manager = resolve.GetProjectManager()
current_project = project_manager.GetCurrentProject()
mediapool = current_project.GetMediaPool()
root_folder = mediapool.GetRootFolder()


def go_to_next_video_item_and_get_metadata(current_timeline):
	current_video_item = current_timeline.GetCurrentVideoItem()
	next_video_item_start_frame = current_video_item.GetEnd() + 1
	next_video_item_start_TC = convert_frame_to_timecode(next_video_item_start_frame,
	                                                     current_project.GetSetting()['timelineFrameRate'])
	current_timeline.SetCurrentTimecode(next_video_item_start_TC)
	return get_scene_slate_take_from_current_video_item(current_timeline.GetCurrentVideoItem())


def go_to_previous_video_item_and_get_metadata(current_timeline):
	previous_video_item_end_frames = current_timeline.GetCurrentVideoItem().GetStart() - 1
	previous_video_item_end_TC = convert_frame_to_timecode(previous_video_item_end_frames,
	                                                       current_project.GetSetting()['timelineFrameRate'])
	current_timeline.SetCurrentTimecode(previous_video_item_end_TC)
	previous_video_item_start_frames = current_timeline.GetCurrentVideoItem().GetStart()
	previous_video_item_start_TC = convert_frame_to_timecode(previous_video_item_start_frames,
	                                                         current_project.GetSetting()['timelineFrameRate'])
	current_timeline.SetCurrentTimecode(previous_video_item_start_TC)
	return get_scene_slate_take_from_current_video_item(current_timeline.GetCurrentVideoItem())


def get_scene_slate_take_from_current_video_item(current_timeline):
	current_video_item = current_timeline.GetCurrentVideoItem()
	scene_letters = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "O", "P", "Q", "R", "S", "T", "U",
	                 "V", "W", "X", "Y", "Z", " ")
	if current_video_item.GetMediaPoolItem().GetClipProperty()['Scene'] != "":
		# todo non logical, useless logic for clap variable
		if any(letter in current_video_item.GetMediaPoolItem().GetClipProperty()['Scene'] for letter in scene_letters):
			scene = current_video_item.GetMediaPoolItem().GetClipProperty()['Scene'][:4]
			if len(current_video_item.GetMediaPoolItem().GetClipProperty()['Scene']) < 6:
				clap = current_video_item.GetMediaPoolItem().GetClipProperty()['Scene'][4:]
			elif len(current_video_item.GetMediaPoolItem().GetClipProperty()['Scene']) > 6:
				clap = current_video_item.GetMediaPoolItem().GetClipProperty()['Scene'][4:]
			else:
				clap = current_video_item.GetMediaPoolItem().GetClipProperty()['Scene'][4:]

		else:
			scene = current_video_item.GetMediaPoolItem().GetClipProperty()['Scene'][:3]
			if len(current_video_item.GetMediaPoolItem().GetClipProperty()['Scene']) < 6:
				clap = current_video_item.GetMediaPoolItem().GetClipProperty()['Scene'][3:]
			elif len(current_video_item.GetMediaPoolItem().GetClipProperty()['Scene']) > 6:
				clap = current_video_item.GetMediaPoolItem().GetClipProperty()['Scene'][3:]
			else:
				clap = current_video_item.GetMediaPoolItem().GetClipProperty()['Scene'][3:]

		take = current_video_item.GetMediaPoolItem().GetClipProperty()['Take'][1:]
		camera = current_video_item.GetName()[0]
		return scene, clap, take, camera


def write_scene_slate_take_to_metadata(current_timeline, scene, slate, take):
	current_video_item = current_timeline.GetCurrentVideoItem()
	current_video_item.GetMediaPoolItem().SetClipProperty('Scene', "{}{}".format(scene, slate))
	current_video_item.GetMediaPoolItem().SetClipProperty('Take', "t{}".format(take))


def timecode_tool_resolve(current_timeline_timecode, num_of_frame, project_fps):
	frames = int(current_timeline_timecode.split(':')[3])
	seconds = int(current_timeline_timecode.split(':')[2])
	minutes = int(current_timeline_timecode.split(':')[1])
	hours = int(current_timeline_timecode.split(':')[0])
	for i in range(num_of_frame):
		if frames == project_fps:
			seconds += 1
			frames = 0
		if seconds == 60:
			minutes += 1
			seconds = 0
		# print(i, minutes, sep=" mins-- ")
		if minutes == 60:
			hours += 1
			minutes = 0
		# print(i, hours, sep=" hours-- ")
		# print("{} - {} - {} - {}".format(hours, minutes, seconds, frames), end='\r')
		frames += 1
		time.sleep(0.004)
		yield "{:02d}:{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds, frames)


def convert_frame_to_timecode(number_of_frames, project_fps):
	hours, minutes, seconds, frames = 0, 0, 0, 0
	for i in range(number_of_frames):
		if frames == project_fps:
			seconds += 1
			frames = 0
		if seconds == 60:
			minutes += 1
			seconds = 0
		if minutes == 60:
			hours += 1
			minutes = 0
		frames += 1
	return "{:02d}:{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds, frames)
