from random import randint
from dice import dice_roll

def get_melee_attack(ar, damage_info, dr, pv):
	roll = randint(1, 100) + ar - dr
	if roll > 25:
		return (True, max(dice_roll(*damage_info) - pv, 0))
	else:
		return (False, 0)


def get_combat_message(attack_succeeds, damage, dies, playerity_matrix, attacker_name=None, defender_name=None):
	first_person1, first_person2 = playerity_matrix
	message = ""
	mv = ""
	if first_person1:
		A = "You"
		s = ""
		s2 = ""
	else:
		A = "The {}".format(attacker_name)
		s = "s"
		s2 = "es"
	if first_person2:
		t = "you"
		i = "you"
	else:
		t = "the {}".format(defender_name)
		i = "it"
	if first_person1 and first_person2:
		t = "yourself"
		i = "yourself"
		mv = "trying to hit "

	if damage:
		message += "{} hit{} {} for {} damage".format(A, s, t, damage)
		message += " and kill{} {}.".format(s, i) if dies else "."
	elif attack_succeeds:
		message += "{} fail{} to hurt {}.".format(A, s, t)
	else:
		message += "{} miss{} {}{}.".format(A, s2, mv, t)
	return message


#def player_attacks_creature_message(attack_succeeds, damage, dies, creature_name):
#	message = ""
#	if damage:
#		message += "You hit the {} for {} damage".format(creature_name, damage)
#		message += " and kill it." if dies else "."
#	elif attack_succeeds:
#		message += "You fail to hurt the {}.".format(creature_name)
#		if dies:
#			message += " The {} suddenly collapses!".format(creature_name)
#	else:
#		message += "You miss the {}.".format(creature_name)
#	return message


#def creature_attacks_player_message(attack_succeeds, damage, creature_name):
#	message = ""
#	if damage:
#		message += "The {} hits you for {} damage.".format(creature_name, damage)
#	elif attack_succeeds:
#		message += "The {} fails to hurt you.".format(creature_name)
#	else:
#		message += "The {} misses you.".format(creature_name)
#	return message


#def creature_attacks_creature_message(attack_succeeds, damage, dies, attacker_name, defender_name):
#	message = ""
#	if damage:
#		message += "The {} hits the {} for {} damage".format(attacker_name, defender_name, damage)
#		message += " and kills it." if dies else "."
#	elif attack_succeeds:
#		message += "The {} fails to hurt the {}.".format(attacker_name, defender_name)
#		if dies:
#			message += " The {} suddenly collapses!".format(defender_name)
#	else:
#		message += "The {} misses the {}.".format(attacker_name, defender_name)
#	return message
