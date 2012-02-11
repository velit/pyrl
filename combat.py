from random import randint
from dice import dice_roll

def get_melee_attack(ar, damage_info, dr, pv):
	roll = randint(1, 100) + ar - dr
	if roll > 25:
		return (True, max(dice_roll(*damage_info) - pv, 0))
	else:
		return (False, 0)


def get_combat_message(attack_succeeds, damage, dies, personity, attacker_name=None, defender_name=None):
	subject_is_player, object_is_player = personity
	message = u""
	if subject_is_player:
		A = u"You"
		s = u""
		s2 = u""
	else:
		A = u"The {}".format(attacker_name)
		s = u"s"
		s2 = u"es"
	if object_is_player:
		t = u"you"
		i = u"you"
	else:
		t = u"the {}".format(defender_name)
		i = u"it"
	if subject_is_player and object_is_player:
		t = u"yourself"
		i = u"yourself"
		mv = u"trying to hit "
	else:
		mv = u""

	if damage:
		message += u"{} hit{} {} for {} damage".format(A, s, t, damage)
		message += u" and kill{} {}.".format(s, i) if dies else u"."
	elif attack_succeeds:
		message += u"{} fail{} to hurt {}.".format(A, s, t)
	else:
		message += u"{} miss{} {}{}.".format(A, s2, mv, t)
	return message
