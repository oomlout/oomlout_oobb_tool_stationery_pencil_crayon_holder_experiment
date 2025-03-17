import copy
import opsc
import oobb
import oobb_base
import yaml
import os
import scad_help

def main(**kwargs):
    make_scad(**kwargs)

def make_scad(**kwargs):
    parts = []

    typ = kwargs.get("typ", "")

    if typ == "":
        #setup    
        #typ = "all"
        typ = "fast"
        #typ = "manual"

    oomp_mode = "project"
    #oomp_mode = "oobb"

    if typ == "all":
        filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr"]; oomp_run = True
        #filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr", "laser", "true"]
    elif typ == "fast":
        filter = ""; save_type = "none"; navigation = False; overwrite = True; modes = ["3dpr"]; oomp_run = False
    elif typ == "manual":
    #filter
        filter = ""
        #filter = "test"

    #save_type
        save_type = "none"
        #save_type = "all"
        
    #navigation        
        #navigation = False
        navigation = True    

    #overwrite
        overwrite = True
                
    #modes
        #modes = ["3dpr", "laser", "true"]
        modes = ["3dpr"]
        #modes = ["laser"]    

    #oomp_run
        oomp_run = True
        #oomp_run = False    

    #adding to kwargs
    kwargs["filter"] = filter
    kwargs["save_type"] = save_type
    kwargs["navigation"] = navigation
    kwargs["overwrite"] = overwrite
    kwargs["modes"] = modes
    kwargs["oomp_mode"] = oomp_mode
    kwargs["oomp_run"] = oomp_run
    
       
    # project_variables
    if True:
        pass
    
    # declare parts
    if True:

        directory_name = os.path.dirname(__file__) 
        directory_name = directory_name.replace("/", "\\")
        project_name = directory_name.split("\\")[-1]
        #max 60 characters
        length_max = 40
        if len(project_name) > length_max:
            project_name = project_name[:length_max]
            #if ends with a _ remove it 
            if project_name[-1] == "_":
                project_name = project_name[:-1]
                
        #defaults
        kwargs["size"] = "oobb"
        kwargs["width"] = 1
        kwargs["height"] = 1
        kwargs["thickness"] = 3
        #oomp_bits
        if oomp_mode == "project":
            kwargs["oomp_classification"] = "project"
            kwargs["oomp_type"] = "github"
            kwargs["oomp_size"] = "oomlout"
            kwargs["oomp_color"] = project_name
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""
        elif oomp_mode == "oobb":
            kwargs["oomp_classification"] = "oobb"
            kwargs["oomp_type"] = "part"
            kwargs["oomp_size"] = ""
            kwargs["oomp_color"] = ""
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""

        part_default = {} 
       
        part_default["project_name"] = project_name
        part_default["full_shift"] = [0, 0, 0]
        part_default["full_rotations"] = [0, 0, 0]
        

        number_pencil_crayons = [3]
        styles = ["beside", "stacked"]
        
        types = []
        #3 wide beside
        typ = {}
        typ["width"] = 3
        typ["height"] = 2
        typ["thickness"] = 9
        typ["number_pencil_crayon"] = 3
        typ["style"] = "beside"
        types.append(typ)

        #3 wide stacked
        typ = {}
        typ["width"] = 3
        typ["height"] = 2
        typ["thickness"] = 15
        typ["number_pencil_crayon"] = 3
        typ["style"] = "stacked"
        types.append(typ)

        #5 wide beside
        typ = {}
        typ["width"] = 5
        typ["height"] = 2
        typ["thickness"] = 9
        typ["number_pencil_crayon"] = 5
        typ["style"] = "beside"
        types.append(typ)

        #5 wide stacked
        typ = {}
        typ["width"] = 3
        typ["height"] = 2
        typ["thickness"] = 15
        typ["number_pencil_crayon"] = 5
        typ["style"] = "stacked"
        types.append(typ)



        for typ in types:
            wid = typ.get("width", 1)
            hei = typ.get("height", 1)
            thick = typ.get("thickness", 3)
            style = typ.get("style", "beside")
            number_pencil_crayon = typ.get("number_pencil_crayon", 3)

            part = copy.deepcopy(part_default)
            p3 = copy.deepcopy(kwargs)
            p3["width"] = wid
            p3["height"] = hei
            p3["thickness"] = thick
            p3["number_pencil_crayon"] = number_pencil_crayon
            p3["style"] = style
            p3["extra"] = f"{number_pencil_crayon}_pencil_crayon_{style}_style"
            part["kwargs"] = p3
            nam = "base"
            part["name"] = nam
            if oomp_mode == "oobb":
                p3["oomp_size"] = nam
            parts.append(part)


    kwargs["parts"] = parts

    scad_help.make_parts(**kwargs)

    #generate navigation
    if navigation:
        sort = []
        sort.append("number_pencil_crayon")
        sort.append("style")
        #sort.append("extra")        
        #sort.append("width")
        #sort.append("height")
        #sort.append("thickness")
        
        scad_help.generate_navigation(sort = sort)


def get_base(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", True)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    style = kwargs.get("style", "")
    number_pencil_crayon = kwargs.get("number_pencil_crayon", 3)


    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    p3["holes"] = ["top", "bottom"]
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    #add screw_countersunk
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_screw_countersunk"
    p3["depth"] = depth
    p3["radius_name"] = "m3"
    p3["nut"] = True
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[2] += depth
    poss = []
    shift_x = (width-1)/2 * 15
    shift_y = 0
    pos11 = copy.deepcopy(pos1)
    pos11[0] += -shift_x
    pos11[1] += shift_y
    pos12 = copy.deepcopy(pos1)
    pos12[0] += shift_x
    pos12[1] += shift_y    
    poss.append(pos11)
    poss.append(pos12)
    p3["pos"] = poss
    oobb_base.append_full(thing,**p3)

    if style == "beside":

        #add pencil crayons
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_cylinder"
        dep = 175
        p3["depth"] = dep
        clear = -0.5
        pencil_crayon_radius = 7.5/2
        p3["radius"] = pencil_crayon_radius + clear/2
        p3["m"] = "#"
        rot1 = copy.deepcopy(rot)
        rot1[0] = 90
        p3["rot"] = rot1
        pos1 = copy.deepcopy(pos)
        pos1[2] += dep/2 + depth / 2
        pos1[1] += dep/2
        start_x = -((number_pencil_crayon-1)/2) * pencil_crayon_radius * 2
        for i in range(number_pencil_crayon):
            pos11 = copy.deepcopy(pos1)
            pos11[0] += start_x + i * pencil_crayon_radius * 2
            p3["pos"] = pos11
            oobb_base.append_full(thing,**p3)

    elif style == "stacked":

        #add pencil crayons
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_cylinder"
        dep = 175
        p3["depth"] = dep
        clear = -0.5
        pencil_crayon_radius = 7.5/2
        p3["radius"] = pencil_crayon_radius + clear/2
        p3["m"] = "#"
        rot1 = copy.deepcopy(rot)
        rot1[0] = 90
        p3["rot"] = rot1
        pos1 = copy.deepcopy(pos)
        pos1[2] += dep/2 + depth / 2
        pos1[1] += dep/2
        start_x = -(((number_pencil_crayon-1)/2) * pencil_crayon_radius * 2)/2
        for i in range(number_pencil_crayon):
            pos11 = copy.deepcopy(pos1)
            pos11[0] += start_x + i * pencil_crayon_radius            
            if i % 2 == 1:
                pos11[2] += pencil_crayon_radius/1.25
            else:
                pos11[2] += -pencil_crayon_radius/1.25


            p3["pos"] = pos11
            oobb_base.append_full(thing,**p3)


    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        pos1[2] += depth
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 0
        pos1[1] += 0
        pos1[2] += depth/2
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)
    
if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)