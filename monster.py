from creature import Creature


def Monster(monster_file):
	monster = Creature()
	monster.name = monster_file.name
	monster.char = monster_file.char
	monster.hp = monster_file.base_hp
	return monster
