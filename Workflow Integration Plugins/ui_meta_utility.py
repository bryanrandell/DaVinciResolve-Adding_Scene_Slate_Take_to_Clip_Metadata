# UI Meta utility. Requires DaVinci Resolve Studio 17.4.x
# Copyright (c) 2021 Bryan Randell

from python_get_resolve import GetResolve
from meta_utility_utils import go_to_next_video_item_and_get_metadata, go_to_previous_video_item_and_get_metadata, \
    get_scene_slate_take_from_current_video_item, write_scene_slate_take_to_metadata
resolve = GetResolve()

project_manager = resolve.GetProjectManager()
current_project = project_manager.GetCurrentProject()
current_project_mediapool = current_project.GetMediaPool()
current_project_root_folder = current_project_mediapool.GetRootFolder()
# print(current_project.GetName())
current_timeline = current_project.GetCurrentTimeline()

# some element IDs
winID = "com.blackmagicdesign.resolve.meta.change.utils"	# should be unique for single instancing
line_edit_sceneID = 'LineEditSceneID'
line_edit_slateID = 'LineEditSlateID'
line_edit_takeID = 'LineEditTakeID'
button_previous_slateID = 'ButtonPreviousSlateID'
button_next_slateID = 'ButtonNextSlateID'
button_previous_takeID = 'ButtonPreviousTakeID'
button_next_takeID = 'ButtonNextTakeID'
button_get_metaID = 'ButtonGetMetaID'
button_write_metaID = 'ButtonWriteMetaId'
button_refresh_timeline = "ButtonRefreshTimeline"

# calling DavinciResolve UI in Workflow Integration
ui = fusion.UIManager
dispatcher = bmd.UIDispatcher(ui)

# check for existing instance
main_window = ui.FindWindow(winID)
if main_window:
    main_window.Show()
    main_window.Raise()
    exit()

# define the window UI layout
main_window = dispatcher.AddWindow\
    ({'ID': winID,
    'Geometry': [300, 100, 350, 200], # [posV, posH, width, height]
    'WindowTitle': "DaVinci Meta change utils", },

   ui.VGroup({ 'Weight': 0.1 }, [
       ui.Button({"ID": button_refresh_timeline, "Text": "Refresh timeline"}),

   ui.HGroup({ 'Weight': 0.1 }, [
        ui.Button({'ID': button_get_metaID, 'Text': 'Get Metadata from clip'}),
        ui.Button({'ID': button_write_metaID, 'Text': 'Overwrite Metadata clip'})
   ]),
   ui.HGroup({ 'Weight': 0.1 }, [
    ui.VGroup({ 'Weight': 0.1 }, [
       ui.Label({'Text': 'Scene', 'Alignment': {'AlignHCenter': True}}),
       ui.LineEdit({'ID' : line_edit_sceneID,
                    'Text':"",
                    "PlaceholderText": "Scene",
                    "Events": {'EditingFinished' : True}})
        ]),
    ui.VGroup({ 'Weight': 0.1 }, [
       ui.Label({'Text': 'Slate', 'Alignment': {'AlignHCenter': True}}),
       ui.LineEdit({'ID': line_edit_slateID,
                    'Text': "",
                    "PlaceholderText": "Slate",
                    "Events": {'EditingFinished': True}}),
        ]),
    ui.VGroup({ 'Weight': 0.1 }, [
       ui.Label({'Text': 'Take', 'Alignment': {'AlignHCenter': True}}),
       ui.LineEdit({'ID': line_edit_takeID,
                    'Text': "",
                    "PlaceholderText": "Take",
                    "Events": {'EditingFinished': True}})
    ]),
    ]),
   ui.HGroup({ 'Weight': 0.1 }, [
       ui.Button({'ID': button_previous_slateID, 'Text': "Previous Slate"},),
       ui.Button({'ID': button_next_slateID, 'Text': 'Next Slate'})
   ]),
   ui.HGroup({'Weight': 0.1}, [
       ui.Button({'ID': button_previous_takeID, 'Text': "Previous Take"}, ),
       ui.Button({'ID': button_next_takeID, 'Text': 'Next Take'})
   ])
   ])
   )

# Tree Item definition
main_window_item = main_window.GetItems()

#Initialize the scene take slate from the current video item in timeline
try:
    scene, slate, take, _ = get_scene_slate_take_from_current_video_item(current_project.GetCurrentTimeline())

except:
    scene, slate, take = "scene", "slate", "take"

main_window_item[line_edit_sceneID].Text = scene
main_window_item[line_edit_slateID].Text = slate
main_window_item[line_edit_takeID].Text = take

def OnClose(ev):
    dispatcher.ExitLoop()

def OnClickRefreshTimeline(ev):
    global current_timeline
    current_timeline = current_project.GetCurrentTimeline()

def OnEditLineScene(ev):
    print(main_window_item[line_edit_sceneID].Text)


def OnEditLineSlate(ev):
    print(main_window_item[line_edit_slateID].Text)

def OnEditLineTake(ev):
    print(main_window_item[line_edit_takeID].Text)

def OnClickGetMeta(ev):
    scene, slate, take, _ = get_scene_slate_take_from_current_video_item(current_project.GetCurrentTimeline())
    main_window_item[line_edit_sceneID].Text = scene
    main_window_item[line_edit_slateID].Text = slate
    main_window_item[line_edit_takeID].Text = take

def OnClickWriteMeta(ev):
    scene = main_window_item[line_edit_sceneID].Text
    slate = main_window_item[line_edit_slateID].Text
    take = main_window_item[line_edit_takeID].Text
    write_scene_slate_take_to_metadata(current_project.GetCurrentTimeline(), scene, slate, take)

def OnClickPreviousSlate(ev):
    scene, slate, take, _ = go_to_previous_video_item_and_get_metadata(current_project.GetCurrentTimeline())

    # new_value = int(main_window_item[line_edit_slateID].Text) - 1
    # print(new_value)
    main_window_item[line_edit_slateID].Text = str(int(main_window_item[line_edit_slateID].Text) - 1)

def OnClickNextSlate(ev):
    scene, slate, take, _ = go_to_next_video_item_and_get_metadata(current_project.GetCurrentTimeline())
    # new_value = int(main_window_item[line_edit_slateID].Text) + 1
    # print(new_value)
    main_window_item[line_edit_slateID].Text = str(int(main_window_item[line_edit_slateID].Text) + 1)
    main_window_item[line_edit_takeID].Text = "1"

def OnClickPreviousTake(ev):
    scene, slate, take, _ = go_to_previous_video_item_and_get_metadata(current_project.GetCurrentTimeline())
    # new_value = int(main_window_item[line_edit_takeID].Text) - 1
    # print(new_value)
    if int(main_window_item[line_edit_takeID].Text) > 0:
        main_window_item[line_edit_takeID].Text = str(int(main_window_item[line_edit_takeID].Text) - 1)

def OnClickNextTake(ev):
    scene, slate, take, _ = go_to_next_video_item_and_get_metadata(current_project.GetCurrentTimeline())
    # new_value = int(main_window_item[line_edit_takeID].Text) + 1
    # print(new_value)
    main_window_item[line_edit_takeID].Text = str(int(main_window_item[line_edit_takeID].Text) + 1)




main_window.On[winID].Close = OnClose
main_window.On[line_edit_sceneID].EditingFinished = OnEditLineScene
main_window.On[line_edit_slateID].EditingFinished = OnEditLineSlate
main_window.On[line_edit_takeID].EditingFinished = OnEditLineTake
main_window.On[button_previous_slateID].Clicked = OnClickPreviousSlate
main_window.On[button_next_slateID].Clicked = OnClickNextSlate
main_window.On[button_previous_takeID].Clicked = OnClickPreviousTake
main_window.On[button_next_takeID].Clicked = OnClickNextTake
main_window.On[button_get_metaID].Clicked = OnClickGetMeta
main_window.On[button_write_metaID].Clicked = OnClickWriteMeta
main_window.On[button_refresh_timeline].Clicked = OnClickRefreshTimeline

# Main dispatcher loop
main_window.Show()
dispatcher.RunLoop()