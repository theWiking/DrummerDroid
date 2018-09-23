from scripts.full.pattern_drum import Pattern
import resource as res

print("start")
path = res.ROOT_DIR + "\\data\\"
print(path)

pattern = Pattern(['kick', 'snare'])
pattern.prepere_data()
pattern.read_pattern()
pattern.save_date()

pattern.__del__()

