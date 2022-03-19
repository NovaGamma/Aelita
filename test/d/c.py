import enchant
import os

print(enchant.get_user_config_dir())
dico = enchant.Dict("fr_FR")

print(dico.check('BONJOUR'))
