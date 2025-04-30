from ui_window import TeamGenerator

if __name__ == "__main__":
    tg = TeamGenerator()
    tg.run()

'''
to do list:
- implement sliders
- refine algo to be able to customize weights
- view results and save results buttobn
- 
'''

# nuitka --standalone --macos-create-app-bundle --enable-plugin=tk-inter \
# --include-data-dir=files=files \
# --include-data-dir=results_page=results_page \
# --include-data-dir=directions=directions \
# --include-data-dir=style=style \
# --include-module=pandas \
# --include-module=pulp \
# --include-module=ttkbootstrap \
# --include-module=PIL \
# --include-module=matplotlib \
# main.py