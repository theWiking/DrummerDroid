from scripts.full.pattern_drum import Pattern
import resource as res

print("start")
path = res.ROOT_DIR + "\\date\\"
print(path)

pattern = Pattern(['kick', 'snare'])
pattern.prepere_date()
pattern.read_pattern()
pattern.save_date()

pattern.__del__()

