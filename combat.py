#def attack(attacker, defender, output=False, is_player=False):
#	attack_succeeds, damage = get_attack(attacker, defender)
#	if attack_succeeds:
#		if output:
#			if is_player:
#				if damage > 0:
#					msg = "The {} hits you for {} damage."
#					io.msg(msg.format(attacker.name, damage))
#				else:
#					msg = "The {} fails to hurt you."
#					io.msg(msg.format(attacker.name))
#			else:
#				if damage > 0:
#					msg = "The {} hits the {} for {} damage."
#					io.msg(msg.format(attacker.name, defender.name, damage))
#				else:
#					msg = "The {} fails to hurt {}."
#					io.msg(msg.format(attacker.name, defender.name))
#			defender.lose_hp(damage)
#	elif defender is attacker.g.player:
#		msg = "The {} misses you."
#		io.msg(msg.format(attacker.name))
#	else:
#		msg = "The {} misses the {}."
#		io.msg(msg.format(attacker.name, defender.name))

from random import randint
from dice import dice_roll

def get_melee_attack(ar, damage_info, dr, pv):
	roll = randint(1, 100) + ar - dr
	if roll > 25:
		return (True, max(dice_roll(*damage_info) - pv, 0))
	else:
		return (False, 0)
