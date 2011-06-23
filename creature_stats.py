class Stats:
	def __init__(self):
		self._base_str = 10
		self._base_dex = 10
		self._base_con = 10
		self._base_int = 10

		self.str = None
		self.dex = None
		self.con = None
		self.int = None

		self.sight = None
		self.max_hp = None
		self.dmg = None
		self.pv = None
		self.ar = None
		self.dr = None

		self.head = None
		self.body = None
		self.left_hand = None
		self.right_hand = None
		self.feet = None
		self.inventory = []

		self.update_stats()

	def update_stats(self):
		self.str = self.base_str
		self.dex = self.base_dex
		self.con = self.base_con
		self.int = self.base_int

		self.sight = self.str // 2 + self.dex // 2 + self.con // 2
		self.max_hp = self.con + self.str // 2
		self.dmg = self.str // 5
		self.pv = self.con // 10
		self.ar = self.dex + self.int // 2
		self.dr = self.dex + self.int // 2

	def equip(self, slot, item):
		self.update_stats()

	def unequip(self, slot):
		self.update_stats()


BASE_STATS = ("base_str", "base_dex", "base_con", "base_int")

def add_base_stat_properties(cls, stat):
	real_attribute = "_" + stat
	def g(self):
		return getattr(self, real_attribute)
	def s(self, value):
		setattr(self, real_attribute, value)
		self.update_stats()
	def d(self):
		delattr(self, real_attribute)
	setattr(cls, stat, property(g, s, d))


for stat in BASE_STATS:
	add_base_stat_properties(Stats, stat)
