import const.game as GAME
import const.creature_actions as CC


class Creature(object):

	def __init__(self, creature_file):
		self.name = creature_file.name
		self.char = creature_file.char
		self.level = None
		self.coord = None
		self.target_coord = None
		self.chase_vector = None

		self.energy = 0

		self.strength = 10
		self.dexterity = 10
		self.toughness = 10
		self.learning = 10
		self.perception = 10

		self.hp = self.max_hp

	def get_damage_info(self):
		dice = self.unarmed_dice
		sides = self.unarmed_sides
		addition = self.dmg_bonus
		return dice, sides, addition

	def receive_damage(self, amount):
		if amount > 0:
			self.hp -= amount

	def is_dead(self):
		return self.hp <= 0

	def recover_energy(self):
		self.energy += self.speed
		if self.energy > 0:
			self.energy = 0

	def can_act(self):
		return self.energy >= 0

	def update_energy(self, amount):
		self.energy -= amount

	def update_energy_action(self, action):
		if action == CC.ATTACK:
			amount = self.attack_energy_cost
		else:
			assert False
		self.energy -= amount
		return amount

	def is_idle(self):
		return self.target_coord is None and self.chase_vector is None

	@property
	def st(self):
		return self.strength

	@property
	def dx(self):
		return self.dexterity

	@property
	def to(self):
		return self.toughness

	@property
	def le(self):
		return self.learning

	@property
	def pe(self):
		return self.perception

	@property
	def sight(self):
		return int((2 * self.pe) ** 0.5 + 1)

	@property
	def max_hp(self):
		return self.to + self.st // 2

	@property
	def dmg_bonus(self):
		return self.st // 5 + self.dx // 10

	@property
	def pv(self):
		return self.to // 10

	@property
	def ar(self):
		return self.dx + self.le // 2

	@property
	def dr(self):
		return self.dx + self.le // 2

	@property
	def unarmed_dice(self):
		return self.st // 20 + 1

	@property
	def unarmed_sides(self):
		return self.st // 3 + self.dx // 6

	@property
	def speed(self):
		return 93 + self.dx // 2 + self.strength // 5

	@property
	def attack_energy_cost(self):
		return GAME.ATTACK_COST
