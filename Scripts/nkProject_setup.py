import re
import os
import shutil
import nuke


def project_setup():


    try:


        plate = nuke.selectedNode()
        
        if plate.Class() == "Read":


            read = plate["file"].getValue()

            def get_shot_name(path):

                # ShotName
                regex = re.search(r"[Ss]h\d+", path)
                shot = regex.group()

                # SequenceName
                try:
                    regex_sq = re.search(r"[Ss][cq]\d+", path)
                    sq = regex_sq.group()

                except:
                    sq = ""

                # check if episod
                if "Ep" in path:

                    regex_ep = re.search(r"[Ee][p]\d+", path)
                    ep = regex_ep.group() + "/"
                    print(ep)

                elif "ep" in path:

                    regex_ep = re.search(r"[Ee][p]\d+", path)
                    ep = regex_ep.group() + "/"
                    print(ep)

                else:
                    ep = ""
                    pass

                # check if Reel
                if "Reel" in path:

                    regex_reel = re.search(r"[Rr]eel\d+", path)
                    reel = regex_reel.group() + "/"
                    print(reel)

                elif "reel" in path:

                    regex_reel = re.search(r"[Rr]eel\d+", path)
                    reel = regex_reel.group() + "/"
                    print(reel)

                else:
                    reel = ""
                    pass

                # RootDir
                footage = re.search(r"[Ff]ootage", path)
                proj_dir = re.split(regex.group(), path)[0]
                root = re.split(footage.group(), proj_dir)[0]

                # ImageSequenceName
                file_name = os.path.basename(read)
                sh = re.search(r"[Ss]h\d+", file_name)
                sh = sh.group()
                file_name = re.split(sh, file_name)[0] + sh

                ###shot_data = shot_data.append(shot, proj_dir, file_name)

                #print ("project is " + root)
                #print ("shot is " + shot)
                #print ("shot name is " + file_name)
                #print ("seq name is " + sq)

                shot_data = [root, ep, reel, sq, shot, file_name]
                return shot_data

            print(get_shot_name(read))

            shotRoot = get_shot_name(read)[0]
            shotEp = get_shot_name(read)[1]
            shotReel = get_shot_name(read)[2]
            shotSq = get_shot_name(read)[3]
            shotName = get_shot_name(read)[4]
            shotFile = get_shot_name(read)[5]





            
            # New script category
            p = nuke.Panel('Script category')

            p.addEnumerationPulldown(
                'Select', 'Keying Rotoscoping Compositing Cleanup')

            p.show()

            selectType = p.value('Select')

            if selectType == 'Keying':
                category = 'Keying'

            if selectType == 'Rotoscoping':
                category = 'Rotoscoping'

            if selectType == 'Compositing':
                category = 'Compositing'

            if selectType == 'Cleanup':
                category = 'Cleanup'


            ###############################################

            # Project settings

            #read = nuke.toNode("Read1")["file"].getValue()

            footage = os.path.basename(read)

            #ext = re.split("\.", footage)[1]

            ext = (os.path.splitext(footage)[-1]).replace(".","")

            # Set color space
            if ext == "exr":

                nuke.root().knob("colorManagement").setValue("OCIO")
                nuke.root().knob("OCIO_config").setValue("aces_1.1")
                plate["colorspace"].setValue("6.0")
                OCIO_CS = "ASEC Colorspace"

            elif ext == "mov":

                nuke.root().knob("colorManagement").setValue("Nuke")
                nuke.root().knob("OCIO_config").setValue("nuke-default")
                plate["colorspace"].setValue("2.0")
                OCIO_CS = "sRGB Colorspace"

            else:

                print("WTF!!")

            # Project range

            f_in = int(plate["first"].getValue())
            f_out = int(plate["last"].getValue())

            nuke.root().knob("first_frame").setValue(f_in)
            nuke.root().knob("last_frame").setValue(f_out)

            # Project format
            current_format = nuke.knob('root.format')
            current_format = re.split(" ", current_format)

            read_width = plate.width()
            read_height = plate.height()
            read_pixel = plate.pixelAspect()

            new_proj_format = '%s %s 0 0 %s %s %s' % (
                read_width, read_height, read_width, read_height, read_pixel)

            nuke.knob('root.format', new_proj_format)

            print("new project format is " + new_proj_format)

            # FPS

            if ext == "mov":

                fps = 25

            elif len(re.findall("TVC/", read)) <= 1:

                fps = 25

            else:

                fps = 24

            nuke.knob("root.fps", str(fps))

            #nk_dir = root/VFX_Projects/ep/sq/sh/category
            nk_dir = ("{}VFX_Projects/{}{}{}/{}/{}").format(shotRoot,
                                                            shotEp, shotReel, shotSq, shotName, category)
            print("new directory is " + nk_dir)

            if not os.path.exists(nk_dir):
                os.makedirs(nk_dir)

            #nk_name = root/VFX_Projects/ep/sq/sh/category/shotfile_category_v001.nk
            nk_name = ("{}/{}_{}_v001.nk").format(nk_dir, shotFile, category)
            print("new name is " + nk_name)

            nuke.scriptSaveAs(nk_name, -1)


            ###################################################


            message = ("""

        Done.\n{} {} script is saved in {}
            
            """).format(category, OCIO_CS, nk_name)

            nuke.message(message)

        else:

            nuke.message("Please Select a Read node")


    except:
        nuke.message("Please Select a Read node")
