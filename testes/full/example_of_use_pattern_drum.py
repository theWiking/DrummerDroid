from scripts.full.pattern_drum import Pattern
import resource as res
import os

print("start")
path = res.ROOT_DIR+"\\date\\"
#os.makedirs(path)
print(path)
#res.remove_folder(path)
#os.makedirs(path)

pattern = Pattern(['kick','snare'])
#pattern.prepere_date()
pattern.read_pattern()
#pattern.record()

pattern.__del__()

#pattern = Pattern().load_date(path_to_save=path)
