import maya.cmds as cmds
import os
import time
import psutil


global resolution_width, resolution_height
def prepare_render_submission():

    #get the process id of maya
    maya_id = os.getpid()
    process = psutil.Process(maya_id)

    #only renderable cameras and cameras starts with CAM
    cameras = cmds.ls(type="camera")
    renderable_cameras = [cam for cam in cameras if cmds.getAttr(f"{cam}.renderable") and cam.startswith("CAM_")]
    if not renderable_cameras:
        print("Error: Not a renderable camera. Pick another one")
        return
    
    render_camera = renderable_cameras[0]
    print(f"1. Renderable camera: {renderable_cameras}")



    # Set the output path to a directory on the desktop
    the_path = os.path.join("C:/Users/aluaa/Desktop/TestProject/New_Project/images")
    # checking if directory does not exist
    os.makedirs(the_path, exist_ok=True)
    
    output_file_prefix = renderable_cameras
    # Set the image file prefix in the render settings to ensure correct output directory
    #cmds.setAttr("defaultRenderGlobals.imageFilePrefix", output_file_prefix.replace("\\", "/"), type="string")
    print(f"2. Output path: {output_file_prefix}")

    

    # Set the render camera
    try:
        # Ensure the camera is active for rendering
        cmds.setAttr(f"{render_camera}.renderable", True)
        
        # frames (start and end)
        start_frame = 1
        end_frame = 1
        cmds.setAttr("defaultRenderGlobals.startFrame", start_frame)
        cmds.setAttr("defaultRenderGlobals.endFrame", end_frame)
        
        # render attributes
        cmds.setAttr("defaultRenderGlobals.currentRenderer", "mayaSoftware", type="string")
        cmds.setAttr("defaultRenderGlobals.animation", False)  # Single frame render
        cmds.setAttr("defaultRenderGlobals.extensionPadding", 4)  # Use 4 digits for frame numbers

        resolution_width = cmds.getAttr("defaultResolution.width")
        resolution_height = cmds.getAttr("defaultResolution.height")
        
        # Render the frame directly using the batch render command
        print(f"3. Starting frame {start_frame}.")
        print(f"4. Ending frame {end_frame}.")
        print(f"5. Resolution is: {resolution_width} x {resolution_height}")

        start_time = time.time()

        #memory usage before rendering
        initial_memory = process.memory_info().rss / (1024 ** 2)
        


        cmds.render(batch=True)

        end_time = time.time()
        time_range = end_time - start_time
        final_memory = process.memory_info().rss / (1024 ** 2)
        difference = final_memory - initial_memory
        print(f"6. Time spent: {time_range}")
        print(f"7. Initial Memory Usage: {initial_memory:.2f} MB")
        print(f"8. Final Memory Usage: {final_memory:.2f}MB")
        print(f"9. Memory Difference: {final_memory:.2f}MB")
        print(f"10. Rendering complete. Check the output at: {the_path}")
        
        
    except Exception as e:
        print(f"Error occurred during rendering: {e}")

# UI 
def create_render_tool_ui():

    if cmds.window("renderToolUI", exists=True):
        cmds.deleteUI("renderToolUI")

    window = cmds.window("renderToolUI", title="Render Diagnostics & Submission", widthHeight=(300, 150))
    cmds.columnLayout(adjustableColumn=True)
    
    cmds.button(label="Run Render Diagnostics & Submit", command=lambda x: prepare_render_submission())
    cmds.separator(height=10, style='in')
    cmds.text(label="Render Diagnostics & Submission Tool")
    
    cmds.showWindow(window)

create_render_tool_ui()
