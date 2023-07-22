import json

class Default:
    export_path = "output/out.svg"
    show_bitmap = False
    draw_contours = True
    draw_hatch = True
    no_cv = False
    hatch_size = 16
    contour_simplify = 2
    resolution = 1024
    save_settings = False

    def save(self,settings_path):
        print("Savings settings to a JSON file")
        file = open(settings_path, 'w')
        data = {
            "resolution": self.resolution,
            "show_bitmap": self.show_bitmap,
            "draw_contours": self.draw_contours,
            "draw_hatch": self.draw_hatch,
            "use_opencv": not self.no_cv,
            "hatch_size": self.hatch_size,
            "contour_simplify": self.contour_simplify
        }
        json.dump(data,file)
        file.close()

argument = Default()